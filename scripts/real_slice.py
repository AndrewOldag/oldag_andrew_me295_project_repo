"""The smallest real slice, end to end: dispatcher -> tracker -> checker -> diagnostician -> auditor.

  python scripts/real_slice.py [--root 0708_m12 --from-h 4 --to-h 6] [--dispatcher agent|script] [--no-agent] [--audit-only] [--out DIR]
  python scripts/real_slice.py --windows 0708_m12:4-6 0711_c1:4-6 0721_m10:4-6 --config private/real_runner.yaml private/real_runner_lab.yaml

With several --config files, each window runs on the host of the first config that lists it (RunnerSet).

One or more include-yes roots, one window each inside its usable hours. The dispatcher (LLM agent by default, or the
script baseline) splits the window into a task and submits it; the job tracks the window on the compute
host (measure/real_runner.py, net midline, settings from private/real_runner.yaml). Collecting a task
checks it (checker, approved thresholds) and, if a check fails, hands it to the diagnostician with the
real request_info and apply_remedy (agents/executors.py). The auditor then reviews the batch. Each run
carries its root's condition, and with more than one condition in the batch the auditor's task asks it to
compare them (inbox item 21); the auditor prompt is not changed.

A plane-sections failure on real movies is an expected result here (midline curvature noise,
docs/proposals/2026-10-23_real-midline-smoothing.md) and is reported, not fixed. Rigid invariance is
not run on real movies (no rigidly moved copy yet).

Writes to results/<date>_real_slice/ (or --out): dispatcher, diagnostician and auditor traces, and
summary.json. Tracker outputs are cached in staging/tracks_real/ (git-ignored); a rerun reuses them.
"""
import argparse
import datetime
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents import dispatcher as D  # noqa: E402
from agents.executors import Slice  # noqa: E402
from agents.actions import ACTION_SETS, ActionSet  # noqa: E402
from agents.orchestrator import Orchestrator  # noqa: E402
from audit.llm import AuditBatch  # noqa: E402
from audit.view import batch_table, batch_view  # noqa: E402
from measure.real_runner import REAL_CONFIG, RealRunner, RealWindow, RunnerSet, vm_free_gb  # noqa: E402


class InlineQueue:
    """Dispatcher queue backend for a short slice: a submitted job (the window's first tracker run) runs at
    once on the compute host; the clock only moves with the dispatcher's waits. load() reads the host."""

    cluster_cpus = 8

    def __init__(self, runner, host_load=True):
        self.runner, self.now, self.jobs = runner, 0.0, {}
        self.host_load = host_load
        self._load, self._load_at = None, -1.0

    def load(self):
        if not self.host_load:
            return 1.0, 32
        if self._load is None or time.time() - self._load_at > 60:
            s = self.runner.host_state()
            self._load, self._load_at = (s["load1"], s["cores"]), time.time()
        return self._load

    def start(self, task, backend):
        if backend != "lab_server":
            raise RuntimeError("the slice runs on the compute host only; no cluster job")
        jid = f"j{len(self.jobs) + 1}"
        w = RealWindow(task.root_id, task.from_h, task.to_h)
        try:
            self.runner.measure(w, self.runner.initial_settings(w))
            self.jobs[jid] = ("done", "", task.core_h)
        except Exception as e:              # a failed job is the dispatcher's to retry
            self.jobs[jid] = ("failed", f"crash: {type(e).__name__}: {str(e)[:120]}", 0.0)
        return jid

    def advance(self, minutes):
        self.now += minutes

    def poll(self):
        return dict(self.jobs)


def summarize(sl, outcome):
    return {"outcome": outcome.__dict__, "remedies": [ch for _, _, _, ch in sl.runs[1:]],
            "roll_backs": sum(ch.startswith("rolled back") for _, _, _, ch in sl.runs[1:]),
            "initial_checks": [c.to_dict() for c in sl.runs[0][2]],
            "final_settings": sl.runs[-1][0].to_dict(), "final_checks": [c.to_dict() for c in sl.checks]}


class Accepted:
    """Outcome stand-in when no check fails: the measurement is reported without an agent call."""
    def __init__(self):
        self.status, self.args, self.steps, self.failed_steps, self.calls = "accept", {"confidence": None}, 0, 0, 0
        self.input_tokens = self.output_tokens = self.call_ms = 0
        self.note = "no failing check; diagnostician not called"


class NotCalled(Accepted):
    """--no-agent: checks only."""
    def __init__(self):
        super().__init__()
        self.status, self.args, self.note = "not_called", {}, "--no-agent: diagnostician not called"


CONDITION_NOTE = ("Real movies. Each run is one root and carries its root's condition. In the report, compare the "
                  "runs of each condition: centre REGR peak, peak position, growth-zone length, flank difference. "
                  "A difference between conditions is a measurement result, not by itself a reason to flag.")


def run_auditor(summaries, records, launcher, out):
    """The LLM auditor on the batch. With no accepted run there is nothing to flag or clear; the auditor still
    reviews the batch and writes its report. With more than one condition, the task asks for a comparison."""
    views, stats, _ = batch_view(summaries, records, key="real_slice")
    batch = AuditBatch({"batch": "real_slice", "table": batch_table(views, stats), "runs": views})
    conditions = sorted({s["condition"] for s in summaries if s.get("condition")})
    task = batch.task()
    if len(conditions) > 1:
        task["note"] = CONDITION_NOTE
    if not batch.accepted:
        # flag and clear take accepted run ids only; with none, an empty id list is not a valid schema.
        # The auditor keeps request_info and report (audit/llm.py unchanged).
        keep = [x for x in batch.actions.actions if x.name in ("request_info", "report")]
        batch.actions = ActionSet("auditor", keep, notes="No run in this batch was accepted: nothing to flag or "
                                                         "clear. Review the batch and report.")
        ACTION_SETS["auditor"] = batch.actions
    (out / "auditor_trace.jsonl").unlink(missing_ok=True)
    o = Orchestrator(launcher, out / "auditor_trace.jsonl").run("auditor", batch.label, task, batch.executors())
    return {"status": o.status, "report": o.args.get("text"), "decisions": batch.decisions, "accepted": batch.accepted,
            "runs": {v["run_id"]: v["status"] for v in views}, "steps": o.steps, "calls": o.calls,
            "input_tokens": o.input_tokens, "output_tokens": o.output_tokens}


def audit_only(out, config):
    """Rebuild the batch from out/summary.json and the cached tracker outputs; run the auditor; update the summary."""
    from measure.remedies import TrackSettings
    from agents.launcher import Launcher
    summ = json.loads((out / "summary.json").read_text())
    runner, launcher = make_runner(config), Launcher()
    summaries, records = [], []
    for tid, s in summ["tasks"].items():
        root, frm = tid.rsplit("__w", 1)
        to_h = s["window_h"][1] if "window_h" in s else summ["window_h"][1]      # older summaries: one window
        w = RealWindow(root, float(frm), float(to_h))
        records.append(runner.measure(w, TrackSettings(**s["final_settings"])).record)
        summaries.append(s)
    summ["auditor"] = run_auditor(summaries, records, launcher, out)
    summ["auditor"]["mode"] = "--audit-only on the recorded batch"
    (out / "summary.json").write_text(json.dumps(summ, indent=1, default=str))
    a = summ["auditor"]
    print(f"auditor: {a['status']}" + (f": {a.get('report')}" if a.get("report") else ""))


def make_runner(configs):
    configs = [configs] if isinstance(configs, (str, Path)) else list(configs)
    return RealRunner(configs[0]) if len(configs) == 1 else RunnerSet(configs)


def parse_window(text):
    """'0711_c1:4-6' -> ('0711_c1', 4.0, 6.0)"""
    root, span = text.rsplit(":", 1)
    frm, to = span.split("-")
    return root, float(frm), float(to)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="0708_m12")
    ap.add_argument("--from-h", type=float, default=4.0)
    ap.add_argument("--to-h", type=float, default=6.0)
    ap.add_argument("--windows", nargs="+", default=None, metavar="ROOT:FROM-TO",
                    help="several roots, one window each (replaces --root, --from-h, --to-h)")
    ap.add_argument("--config", nargs="+", default=[str(REAL_CONFIG)],
                    help="runner configs (host, folders, windows); a window runs on the first config that lists it")
    ap.add_argument("--dispatcher", choices=["agent", "script"], default="agent")
    ap.add_argument("--no-agent", action="store_true",
                    help="script dispatcher, tracker and checker only; no LLM call (diagnostician and auditor skipped)")
    ap.add_argument("--audit-only", action="store_true",
                    help="run only the auditor on the batch recorded in --out (cached tracker outputs; no re-run)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-free-gb", type=float, default=2.0,
                    help="wait before each window while free VM memory is below this (inbox item 37)")
    a = ap.parse_args()
    if a.audit_only:
        out = Path(a.out).resolve() if a.out else ROOT / "results" / f"{datetime.date.today().isoformat()}_real_slice"
        return audit_only(out, a.config)
    if a.no_agent:
        a.dispatcher = "script"

    out = Path(a.out).resolve() if a.out else ROOT / "results" / f"{datetime.date.today().isoformat()}_real_slice"
    out.mkdir(parents=True, exist_ok=True)
    for f in ("dispatcher_trace.jsonl", "diagnostician_trace.jsonl", "auditor_trace.jsonl"):
        (out / f).unlink(missing_ok=True)

    windows = [parse_window(w) for w in a.windows] if a.windows else [(a.root, a.from_h, a.to_h)]
    manifest = {r["id"]: r for r in D.manifest_rows()}
    rows = []
    for root, frm, to in windows:
        row = manifest.get(root)
        if row is None:
            sys.exit(f"{root} is not an include-yes root")
        if not float(row["usable_from_h"]) <= frm < to <= float(row["usable_to_h"]):
            sys.exit(f"window {frm:g}-{to:g} h is outside the usable hours of {root}")
        rows.append(dict(row, usable_from_h=str(frm), usable_to_h=str(to)))
    conditions = {r["id"]: r["condition"] for r in rows}

    runner = make_runner(a.config)
    runner.sync_code()
    launcher = None
    if not a.no_agent:
        from agents.launcher import Launcher
        launcher = Launcher()
    results = {}

    def collect(task):
        while (free := vm_free_gb()) < a.min_free_gb:          # inbox item 37: wait, do not get killed
            print(f"VM memory {free:.2f} GB free, below {a.min_free_gb} GB; waiting 60 s", flush=True)
            time.sleep(60)
        w = RealWindow(task.root_id, task.from_h, task.to_h)
        sl = Slice(runner, w, label=f"{task.root_id} window")
        if a.no_agent:
            o = NotCalled()
        elif any(c.passed is False for c in sl.checks):
            o = Orchestrator(launcher, out / "diagnostician_trace.jsonl").run(
                "diagnostician", task.id, sl.task(), sl.executors())
        else:
            o = Accepted()
        s = dict(summarize(sl, o), condition=conditions[task.root_id], window_h=[task.from_h, task.to_h])
        results[task.id] = (s, sl.current.record)
        return {"diagnostician": o.status}

    cfg = D.load_config()
    engine = D.Engine(InlineQueue(runner), cfg, rows=rows, budget={"core_hours": 0.0, "usd": 0.0, "approved": False},
                      collector=collect)
    t0 = time.time()
    if a.dispatcher == "agent":
        disp = D.run_agent_batch(engine, launcher, out / "dispatcher_trace.jsonl", round_limit=10)
    else:
        disp = D.run_script_batch(engine, poll_minutes=15, round_limit=10)
    print(f"dispatcher ({a.dispatcher}): {disp['status']}, rounds {disp['rounds']}, windows {disp['states']}")

    summaries = [s for s, _ in results.values()]
    records = [r for _, r in results.values()]
    for tid, (s, _) in results.items():
        print(f"{tid}: initial " + ", ".join(f"{c['check']} {c['value']:.3g}"
                                              f"{'' if c['passed'] is None else (' pass' if c['passed'] else ' FAIL')}"
                                              for c in s["initial_checks"]))
        print(f"  diagnostician: {s['outcome']['status']} {s['outcome']['args']}; remedies {s['remedies'] or 'none'}")

    audit = None
    if summaries:
        audit = {"status": "not_called", "note": "--no-agent"} if a.no_agent else             run_auditor(summaries, records, launcher, out)
        print(f"auditor: {audit['status']}" + (f": {audit.get('report')}" if audit.get("report") else ""))

    summary = {"windows": [[r, f, t] for r, f, t in windows], "dispatcher_mode": a.dispatcher,
               "dispatcher": disp, "tasks": {k: s for k, (s, _) in results.items()}, "auditor": audit,
               "runner_log": runner.log, "wall_s": round(time.time() - t0, 1),
               "model": launcher.cfg["model"] if launcher else None,
               "claude_code": getattr(launcher, "version", None)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
