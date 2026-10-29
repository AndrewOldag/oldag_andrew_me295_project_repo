"""Dispatcher: manifest -> root-by-window tasks -> tracking jobs, inside a budget.

Proposal `docs/proposals/2026-10-23_dispatcher.md` (approved 2026-10-23); settings
`config/dispatcher.yaml`. The agent returns typed actions; `Engine` carries them out
and enforces every limit itself: include-yes rows and usable windows only, the
shared-machine limits on the lab server, and the approved budget on the cluster.
The agent submits nothing itself.

One dispatcher call is one round of up to `step_limit` actions (`config/models.yaml`).
`wait`, `request_approval` and `finish` end a round; the batch loop then advances
the queue clock, pauses for Andrew, or stops. Actions take root ids, not window ids:
a batch has about 1200 windows, too many for a prompt; each action applies to the
eligible windows of the roots named.

Backends implement the `Queue` methods. `FakeQueue` is the test backend: a clock,
job times from the timing model, injected crash, timeout and preemption, a scripted
lab-server load. No real job is ever started from this module's tests.
"""
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .actions import ACTION_SETS, Action, ActionSet
from .orchestrator import Orchestrator, Outcome

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "config" / "dispatcher.yaml"
BACKENDS = ("lab_server", "cluster")
LIVE = ("submitted", "running")          # a job exists for the task


def load_config(path=CONFIG):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_budget(cfg, repo=REPO):
    """Approved cluster budget, or zero. Only a file with approved_by: Andrew counts."""
    p = repo / cfg["budget_file"]
    if not p.exists():
        return {"core_hours": 0.0, "usd": 0.0, "approved": False}
    b = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if b.get("approved_by") != "Andrew":
        return {"core_hours": 0.0, "usd": 0.0, "approved": False}
    return {"core_hours": float(b["core_hours"]), "usd": float(b["usd"]), "approved": True,
            "date": str(b.get("date", ""))}


# ── tasks ─────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    id: str
    root_id: str
    from_h: float
    to_h: float
    frames: int
    core_h: float                 # estimate, both copies
    state: str = "pending"        # pending | queued | submitted | running | done | failed | collected | gave_up
    backend: str = ""
    retries: int = 0
    job_id: str = ""
    cause: str = ""               # last job failure cause
    used_core_h: float = 0.0
    result: dict = field(default_factory=dict)


def windows(from_h, to_h, window_h, last_min_h):
    out, h = [], from_h
    while h + window_h <= to_h + 1e-9:
        out.append((h, h + window_h)); h += window_h
    if to_h - h >= last_min_h - 1e-9:
        out.append((h, to_h))
    return out


def manifest_rows(path=REPO / "manifest" / "root_manifest.csv"):
    """Rows with include yes only; the agent never sees any other row."""
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["include"] == "yes"]


def make_tasks(row, cfg):
    t = cfg["timing"]
    step_s = float(row["step_s"])
    out = []
    for a, b in windows(float(row["usable_from_h"]), float(row["usable_to_h"]),
                        cfg["window_h"], cfg["last_window_min_h"]):
        frames = int(round((b - a) * 3600 / step_s))
        core_h = frames * t["core_s_per_frame"] * t["moved_copy"] / 3600
        out.append(Task(f"{row['id']}__w{a:g}", row["id"], round(a, 3), round(b, 3), frames, core_h))
    return out


# ── queues ────────────────────────────────────────────────────────────────────

class FakeQueue:
    """Test backend. Minutes of simulated time; job wall time = core-hours (one single-thread
    worker per lab job; a cluster job gets `cluster_cpus` cores). `faults`: task id -> list of
    outcomes per attempt ("ok", "crash", "timeout", "preempt"); `load`: callable minute -> 1 min load."""

    def __init__(self, cores=32, load=None, faults=None, cluster_cpus=8):
        self.cores, self.now = cores, 0.0
        self._load = load or (lambda t: 1.0)
        self.faults = {k: list(v) for k, v in (faults or {}).items()}
        self.cluster_cpus = cluster_cpus
        self.jobs = {}                # job id -> dict
        self.started = []             # (minute, job id, backend), for tests

    def load(self):
        return float(self._load(self.now)), self.cores

    def start(self, task, backend):
        jid = f"j{len(self.jobs) + 1}"
        outcome = (self.faults.get(task.id) or ["ok"]).pop(0) if self.faults.get(task.id) else "ok"
        cpus = 1 if backend == "lab_server" else self.cluster_cpus
        run_min = task.core_h * 60 / cpus
        end = self.now + (run_min if outcome == "ok" else run_min / 2)
        self.jobs[jid] = {"task": task.id, "backend": backend, "start": self.now, "end": end,
                          "outcome": outcome, "cpus": cpus}
        self.started.append((self.now, jid, backend))
        return jid

    def advance(self, minutes):
        self.now += minutes

    def poll(self):
        """job id -> (state, cause, core-hours used so far)."""
        out = {}
        for jid, j in self.jobs.items():
            used = max(0.0, min(self.now, j["end"]) - j["start"]) / 60 * j["cpus"]
            if self.now < j["end"]:
                out[jid] = ("running", "", used)
            else:
                out[jid] = ("done", "", used) if j["outcome"] == "ok" else ("failed", j["outcome"], used)
        return out


# ── engine ────────────────────────────────────────────────────────────────────

class Engine:
    """Carries out dispatcher actions on a queue and enforces every limit."""

    def __init__(self, queue, cfg=None, rows=None, budget=None, collector=None, approvals_dir=None):
        self.cfg = cfg or load_config()
        self.queue = queue
        self.rows = {r["id"]: r for r in (rows if rows is not None else manifest_rows())}
        self.budget = budget if budget is not None else load_budget(self.cfg)
        self.collector = collector or (lambda task: {"collected": True})
        self.approvals_dir = Path(approvals_dir) if approvals_dir else None
        self.tasks = {}               # task id -> Task, in creation order
        self.lab_queue = []           # task ids waiting for a lab-server worker slot
        self.cluster_spent_h = 0.0    # estimate at submit, measured after
        self.lab_paused = False
        self.stats = {"refused": 0, "cluster_refused": 0, "approvals": 0, "retries": 0,
                      "retry_successes": 0, "lab_peak_workers": 0}

    # views ------------------------------------------------------------------
    def root_tasks(self, rid):
        return [t for t in self.tasks.values() if t.root_id == rid]

    def lab_workers(self):
        return sum(1 for t in self.tasks.values() if t.backend == "lab_server" and t.state in LIVE)

    def max_lab_workers(self):
        _, cores = self.queue.load()
        return max(1, min(self.cfg["lab_server"]["max_workers"], cores // 8))

    def cluster_left_h(self):
        return self.budget["core_hours"] - self.cluster_spent_h

    def view(self):
        """What the agent sees: per root, window counts by state; queue and budget."""
        roots = []
        for rid, r in self.rows.items():
            ts = self.root_tasks(rid)
            counts = {}
            for t in ts:
                counts[t.state] = counts.get(t.state, 0) + 1
            roots.append({"root_id": rid, "condition": r["condition"], "experiment_type": r["experiment_type"],
                          "usable_h": [float(r["usable_from_h"]), float(r["usable_to_h"])],
                          "windows": counts or "not split"})
        load1, cores = self.queue.load()
        return {"minute": round(self.queue.now, 1), "roots": roots,
                "lab_server": {"workers": self.lab_workers(), "max_workers": self.max_lab_workers(),
                               "queued": len(self.lab_queue), "load1": round(load1, 2), "cores": cores,
                               "paused_for_load": self.lab_paused},
                "cluster": {"budget_core_hours": self.budget["core_hours"], "budget_usd": self.budget["usd"],
                            "approved": self.budget["approved"],
                            "spent_core_hours": round(self.cluster_spent_h, 2),
                            "left_core_hours": round(self.cluster_left_h(), 2)}}

    # bookkeeping ------------------------------------------------------------
    def refresh(self):
        """Poll the queue, update task states, start lab jobs that may start now."""
        polled = self.queue.poll()
        for t in self.tasks.values():
            if t.state not in LIVE:
                continue
            state, cause, used = polled[t.job_id]
            t.used_core_h = used
            if state == "running":
                t.state = "running"
            elif state == "done":
                t.state = "done"
                if t.retries:
                    self.stats["retry_successes"] += 1
            else:
                t.state, t.cause = "failed", cause
            if t.backend == "cluster" and state != "running":
                self.cluster_spent_h += used - t.core_h      # estimate at submit -> measured at the end
        self._start_lab()

    def advance(self, minutes, step=1.0):
        """Let time pass. The worker pool runs between rounds: queued lab jobs start as soon as
        a slot frees and the load allows, not only when the agent next looks."""
        left = float(minutes)
        while left > 1e-9:
            dt = min(step, left)
            self.queue.advance(dt)
            self.refresh()
            left -= dt

    def _start_lab(self):
        ls = self.cfg["lab_server"]
        load1, cores = self.queue.load()
        if load1 > ls["pause_load_fraction"] * cores:
            self.lab_paused = True
        elif load1 <= ls["start_load_fraction"] * cores:
            self.lab_paused = False
        while self.lab_queue and not self.lab_paused and self.lab_workers() < self.max_lab_workers():
            t = self.tasks[self.lab_queue.pop(0)]
            t.job_id, t.state = self.queue.start(t, "lab_server"), "submitted"
        self.stats["lab_peak_workers"] = max(self.stats["lab_peak_workers"], self.lab_workers())

    def _usd(self, core_h):
        return core_h * self.cfg["timing"]["cluster_usd_per_core_h"]

    def _check_roots(self, root_ids):
        bad = [r for r in root_ids if r not in self.rows]
        if bad:
            raise ValueError(f"not include-yes roots: {bad}")

    # actions ----------------------------------------------------------------
    def split_root(self, args, _task=None):
        self._check_roots(args["root_ids"])
        made = []
        for rid in args["root_ids"]:
            if self.root_tasks(rid):
                continue
            for t in make_tasks(self.rows[rid], self.cfg):
                self.tasks[t.id] = t; made.append(t.id)
        return {"windows_made": len(made), "roots": args["root_ids"]}

    def _eligible(self, root_ids, states):
        self._check_roots(root_ids)
        return [t for rid in root_ids for t in self.root_tasks(rid) if t.state in states]

    def estimate_cost(self, args, _task=None):
        ts = self._eligible(args["root_ids"], ("pending", "failed"))
        core_h = sum(t.core_h for t in ts)
        out = {"windows": len(ts), "core_hours": round(core_h, 2)}
        if args["backend"] == "cluster":
            out.update(usd=round(self._usd(core_h), 2), wall_h=round(core_h / self.queue.cluster_cpus, 2),
                       budget_left_core_hours=round(self.cluster_left_h(), 2))
        else:
            out.update(wall_h_at_max_workers=round(core_h / self.max_lab_workers(), 2))
        return out

    def request_approval(self, args):
        self.stats["approvals"] += 1
        req = {"minute": self.queue.now, "root_ids": args.get("root_ids"), "core_hours": args["core_hours"],
               "reason": args["reason"], "usd": round(self._usd(args["core_hours"]), 2)}
        if self.approvals_dir:
            self.approvals_dir.mkdir(parents=True, exist_ok=True)
            n = len(list(self.approvals_dir.glob("request_*.json"))) + 1
            (self.approvals_dir / f"request_{n:03d}.json").write_text(json.dumps(req, indent=1))
        return req

    def submit(self, args, _task=None):
        ts = self._eligible(args["root_ids"], ("pending",))
        if args["backend"] == "cluster":
            need = sum(t.core_h for t in ts)
            if need > self.cluster_left_h() + 1e-9:
                self.stats["cluster_refused"] += 1
                return {"error": f"refused: {need:.2f} core-hours needed, {self.cluster_left_h():.2f} "
                                 f"left in the approved budget"}
            for t in ts:
                t.backend, t.state = "cluster", "submitted"
                t.job_id = self.queue.start(t, "cluster")
            self.cluster_spent_h += need
        else:
            for t in ts:
                t.backend, t.state = "lab_server", "queued"
                self.lab_queue.append(t.id)
            self._start_lab()
        return {"submitted_windows": len(ts), "backend": args["backend"]}

    def collect(self, args, _task=None):
        ts = self._eligible(args["root_ids"], ("done",))
        failed = []
        for t in ts:
            try:
                t.result = self.collector(t)
            except Exception as e:          # one window's error fails that window, not the batch (c022)
                t.state, t.cause = "failed", f"collect: {type(e).__name__}: {str(e)[:120]}"
                failed.append(t.id)
                continue
            t.state = "collected"
        out = {"collected_windows": len(ts) - len(failed)}
        if failed:
            out["failed_windows"] = failed
        return out

    def retry(self, args, _task=None):
        ts = self._eligible(args["root_ids"], ("failed",))
        again, gave_up = [], []
        for t in ts:
            if t.retries >= self.cfg["retries_per_task"]:
                t.state = "gave_up"; gave_up.append(t.id)
                continue
            t.retries += 1
            self.stats["retries"] += 1
            t.state = "pending"
            again.append(t)
        by_backend = {}
        for t in again:
            by_backend.setdefault(t.backend or "lab_server", []).append(t)
        out = {"retried_windows": len(again), "gave_up": gave_up}
        for b, group in by_backend.items():
            r = self.submit({"root_ids": sorted({t.root_id for t in group}), "backend": b})
            if "error" in r:
                out["error"] = r["error"]
        return out

    def live(self):
        return [t for t in self.tasks.values() if t.state in LIVE or t.state == "queued"]

    def summary(self):
        states = {}
        for t in self.tasks.values():
            states[t.state] = states.get(t.state, 0) + 1
        return {"minute": round(self.queue.now, 1), "windows": len(self.tasks), "states": states,
                "lab_core_hours": round(sum(t.used_core_h for t in self.tasks.values() if t.backend == "lab_server"), 2),
                "cluster_core_hours": round(sum(t.used_core_h for t in self.tasks.values() if t.backend == "cluster"), 2),
                **self.stats}


# ── the agent's action set ────────────────────────────────────────────────────

class DispatcherActions(ActionSet):
    """Built per batch: root ids are checked against the batch; finish is refused while jobs live."""

    def __init__(self, engine, cfg):
        self.engine = engine
        roots = {"type": "array", "items": {"type": "string"}}
        backend = {"type": "string", "enum": list(BACKENDS)}
        super().__init__("dispatcher", [
            Action("split_root", {"root_ids": roots}, description="make the root-by-window tasks of these roots"),
            Action("estimate_cost", {"root_ids": roots, "backend": backend},
                   description="core-hours, wall time and dollars for their pending or failed windows"),
            Action("submit", {"root_ids": roots, "backend": backend},
                   description="submit their pending windows; the cluster only inside the approved budget"),
            Action("collect", {"root_ids": roots}, description="collect their finished windows for checking"),
            Action("retry", {"root_ids": roots},
                   description=f"resubmit their failed windows (at most {cfg['retries_per_task']} retries each)"),
            Action("wait", {"minutes": {"type": "number", "enum": cfg["wait_minutes"]}}, terminal=True,
                   description="end the round and wait"),
            Action("request_approval", {"core_hours": {"type": "number", "minimum": 0}, "reason": {"type": "string"}},
                   {"root_ids": roots}, terminal=True,
                   description="ask Andrew for a cluster budget; the batch pauses until he answers"),
            Action("finish", {"summary": {"type": "string"}}, terminal=True,
                   description="end the batch; refused while any window is queued, submitted or running"),
        ], notes="Every root id must be one of the batch's roots.")

    @staticmethod
    def _check(name, s, v):
        if s.get("type") == "array":
            if not isinstance(v, list) or not v or not all(isinstance(x, str) for x in v):
                raise ValueError(f"{name} must be a non-empty list of root ids")
            return
        ActionSet._check(name, s, v)

    def describe(self):
        lines = []
        for a in self.actions:
            args = ", ".join(list(a.args) + [f"{n} (optional)" for n in a.optional]) or "no arguments"
            lines.append(f"- {a.name} ({args}){' [ends the round]' if a.terminal else ''}: {a.description}")
        for n, s in self.all_args().items():
            if "enum" in s:
                lines.append(f"Allowed {n}: {', '.join(str(v) for v in s['enum'])}")
        lines.append(self.notes)
        return "\n".join(lines)

    def validate(self, out):
        name, args = super().validate(out)
        if args.get("root_ids"):
            bad = [r for r in args["root_ids"] if r not in self.engine.rows]
            if bad:
                raise ValueError(f"unknown root ids: {bad[:5]}")
        if name == "finish" and self.engine.live():
            raise ValueError(f"finish refused: {len(self.engine.live())} windows queued, submitted or running")
        return name, args


# ── batch loops ───────────────────────────────────────────────────────────────

def run_agent_batch(engine, launcher, trace_path, round_limit=None):
    """The dispatcher agent drives the engine round by round. Returns the engine summary plus status."""
    cfg = engine.cfg
    ACTION_SETS["dispatcher"] = DispatcherActions(engine, cfg)
    orch = Orchestrator(launcher, trace_path)
    ex = {"split_root": engine.split_root, "estimate_cost": engine.estimate_cost, "submit": engine.submit,
          "collect": engine.collect, "retry": engine.retry}
    status, errors_in_row, rounds = "round_limit", 0, 0
    for n in range(1, (round_limit or cfg["round_limit"]) + 1):
        rounds = n
        engine.refresh()
        out = orch.run("dispatcher", f"round{n:03d}", engine.view(), ex)
        errors_in_row = errors_in_row + 1 if out.status == "error" else 0
        if out.status == "finish":
            status = "finish"; break
        if out.status == "request_approval":
            engine.request_approval(out.args)
            status = "waiting_for_approval"; break
        if errors_in_row >= 2:
            status = "error"; break
        engine.advance(out.args.get("minutes", min(cfg["wait_minutes"])) if out.status == "wait"
                       else min(cfg["wait_minutes"]))
    engine.refresh()
    return {"status": status, "rounds": rounds, **engine.summary()}


def run_script_batch(engine, backend="lab_server", poll_minutes=30, round_limit=None):
    """Baseline: split every root in manifest order, submit in that order, poll every 30 min,
    retry a failed job once, collect, stop when nothing is left. Same engine and limits."""
    cfg = engine.cfg
    roots = list(engine.rows)
    engine.split_root({"root_ids": roots})
    r = engine.submit({"root_ids": roots, "backend": backend})
    status, rounds = "round_limit", 0
    for n in range(1, (round_limit or cfg["round_limit"]) + 1):
        rounds = n
        engine.refresh()
        engine.collect({"root_ids": roots})
        for t in [t for t in engine.tasks.values() if t.state == "failed"]:
            if t.retries >= 1:
                t.state = "gave_up"
            else:
                engine.retry({"root_ids": [t.root_id]})
        if not engine.live() and not any(t.state in ("pending", "done", "failed") for t in engine.tasks.values()):
            status = "finish"; break
        engine.advance(poll_minutes)
    engine.refresh()
    return {"status": status, "rounds": rounds, "first_submit": r, **engine.summary()}
