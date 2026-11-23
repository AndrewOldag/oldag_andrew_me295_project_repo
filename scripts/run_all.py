"""Task c027 (spec 2026-11-18 B): the integrated run over every include-yes root and its usable windows.

  python scripts/run_all.py windows                         # the 1,189 windows in dispatcher order, with batch
  python scripts/run_all.py fetch                           # base tracks storage -> VM cache (md5 checked)
  python scripts/run_all.py run --out staging/c027/run [--stop-at 2026-11-21T18:00]
  python scripts/run_all.py tree --run staging/c027/run --out staging/c027/tree [--stop-at ...]
  python scripts/run_all.py audit --out staging/c027/run [--final-now]
  python scripts/run_all.py report --run staging/c027/run --tree staging/c027/tree --out results/2026-11-18_integrated_run

run     Fixed-script dispatcher (agents/dispatcher.py run_script_batch) over the manifest's include-yes roots; it
        splits each root into its usable windows and hands each to the collector: track (cache by settings tag) ->
        checker (real profile, closure gate 19 px/h) -> decline by rule if a gating check is not computable ->
        diagnostician on a failing window. A root's accepted windows go to the auditor once all its windows are
        final. One record per window in OUT/windows/; a restarted run skips them.
        A track not in the cache pauses the window (`paused: needs <tag>`); the paused trace is set aside, the
        settings go to OUT/paused.jsonl for `retrack_queue.py jobs --paused`, and the window reruns from step 0 on
        the next start. No step waits on the cluster.
tree    The remedy tree (agents/baselines.py run_tree, step limit 8) on every window whose first check fails,
        through the same cache; the c026 tree records stand for the windows it reached.
audit   Auditor runs for roots whose windows are all final; --final-now also takes roots with paused windows,
        over their final windows (the cut-off pass).
report  scripts/run_all_report.py.

Caps: 900 LLM calls for the diagnostician and the auditor together (`--llm-cap`; c027 restarted with 1,300 at 782
calls, inbox item 59). A diagnostician window starts only if the calls
so far plus its step limit (8) plus 5 per root still to audit stay within the cap. Free VM memory at least 3 GB
before each window. A trace with the seat's session-limit message is set aside, not recorded, and the run stops.
"""
import argparse
import csv
import datetime
import json
import shutil
import sys
import time
from collections import Counter, OrderedDict
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from agents import dispatcher as D  # noqa: E402
from measure.real_runner import RealRunner, RealWindow, vm_free_gb  # noqa: E402

CONFIG = ROOT / "private" / "real_runner_c027.yaml"
BATCHES = {1: ROOT / "results" / "2026-10-25_full_batch_1" / "windows.csv",
           2: ROOT / "results" / "2026-10-25_full_batch_2" / "windows.csv"}
C026_TREE = ROOT / "staging" / "c026" / "tree" / "windows"
LLM_CAP, STEP_LIMIT, AUDIT_RESERVE, VM_MIN_GB = 900, 8, 5, 3.0
LIMIT_TEXT = "hit your session limit"
# Inbox items 49 and 53: register_frames v1 tracks can pass closure with points out of order. They count as not
# cached, so they are never used; register_v2 tracks are used like any other
REGISTER_HOLD = True
# Inbox items 53-55: decisions on a remedied track waited for the integrity gate (option A). It is on main and wired
# into every remedy step (agents/executors.py), so the hold is lifted (2026-11-22). True pauses every failing window
REMEDY_HOLD = False


class Paused(BaseException):
    """A track the window needs is not cached. BaseException: it passes the orchestrator's executor guard, so the
    window stops at once instead of the agent seeing an error (spec A4)."""

    def __init__(self, window, settings, kinds, reason=None):
        super().__init__(reason or f"paused: needs {settings.tag()} ({', '.join(kinds)})")
        self.window, self.settings, self.kinds = window, settings, kinds


class StopRun(Exception):
    pass


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


# ---- windows
def batch_rows():
    """window id -> row of the batch windows.csv (batch 1 or 2), with `batch`."""
    out = {}
    for b, p in BATCHES.items():
        with open(p, newline="") as f:
            for r in csv.DictReader(f):
                out[r["window"]] = dict(r, batch=b)
    return out


class _Q:
    """Dispatcher queue for the run: a submitted task is the window's cached base track, so it is done at once.
    Nothing is tracked here; the collector reads the cache and pauses a window whose track is missing."""
    cluster_cpus = 8

    def __init__(self):
        self.now, self.jobs = 0.0, {}

    def load(self):
        return 1.0, 32

    def start(self, task, backend):
        jid = f"j{len(self.jobs) + 1}"
        self.jobs[jid] = ("done", "", task.core_h)
        return jid

    def advance(self, minutes):
        self.now += minutes

    def poll(self):
        return dict(self.jobs)


def dispatch(collector, roots=None):
    """Fixed-script dispatcher over the include-yes roots (only `roots` if given; B5 demo); returns its summary."""
    rows = [r for r in D.manifest_rows() if roots is None or r["id"] in roots]
    engine = D.Engine(_Q(), D.load_config(), rows=rows,
                      budget={"core_hours": 0.0, "usd": 0.0, "approved": False}, collector=collector)
    return D.run_script_batch(engine, poll_minutes=15, round_limit=400)


def window_list(roots=None):
    seen = []
    dispatch(lambda t: (seen.append(RealWindow(t.root_id, t.from_h, t.to_h)), {"listed": True})[1], roots)
    return seen


# ---- runner
class RunRunner(RealRunner):
    """Cached tracks only. A window has the moved copy (rigid invariance) where its batch run had one."""

    def __init__(self, cfg, moved_windows, **kw):
        super().__init__(cfg, **kw)
        self.moved_windows = set(moved_windows)
        self.cached_only = True

    def kinds(self, window):
        return ["ref", "moved"] if window.id() in self.moved_windows else ["window"]

    def missing(self, window, settings):
        if REGISTER_HOLD and settings.register and settings.register_version != 2:
            return self.kinds(window)
        return [k for k in self.kinds(window) if not self.cache_path(window, settings, k).exists()]

    def measure(self, window, settings):
        miss = self.missing(window, settings)
        if miss:
            raise Paused(window, replace(settings, width_free=False), miss)
        self.with_moved = window.id() in self.moved_windows
        self.moved_span = None
        return super().measure(window, settings)


def make_runner(config=CONFIG, rows=None):
    import yaml
    from measure.remote_link import Link
    cfg = yaml.safe_load(Path(config).read_text())
    rows = rows if rows is not None else batch_rows()
    moved = [w for w, r in rows.items() if r.get("moved_copy") == "True"]
    runner = RunRunner(cfg, moved, link=Link(cfg["storage_host"], sleep=lambda s: None))
    runner.cfg_dict = cfg
    return runner


# ---- fetch
def fetch(runner, rows, log=print):
    """Base tracks of every measured window from the batch outputs on storage to the VM cache, md5 checked.
    Batch 1: <batch1_dir>/tracks. Batch 2: <batch2_dir>/<root>/tracks, then <batch2_dir>/tracks (moved copies)."""
    import hashlib
    from measure import remote_link
    from measure.remedies import TrackSettings
    remote_link.CHANNEL_TIMEOUT_S = 120      # a track is under 1 MB: a silent channel this long is a dead connection
    cfg = runner.cfg_dict
    need = OrderedDict()
    for wid, r in rows.items():
        if r["status"] != "measured":
            continue
        w = _window(wid)
        for k in runner.kinds(w):
            p = runner.cache_path(w, TrackSettings(stride=1), k)
            if not p.exists():
                dirs = ([f"{cfg['batch1_dir']}/tracks"] if r["batch"] == 1 else
                        [f"{cfg['batch2_dir']}/{w.root_id}/tracks", f"{cfg['batch2_dir']}/tracks"])
                need[p] = dirs
    log(f"{len(need)} base tracks to fetch")
    by_dir = OrderedDict()
    for p, dirs in need.items():
        by_dir.setdefault(tuple(dirs), []).append(p)
    n = bad = 0
    for dirs, paths in by_dir.items():
        md5 = {}
        for d in dirs:
            names = " ".join(f"'{p.name}'" for p in paths if p.name not in md5)
            if not names:
                break
            out = runner.link.run(f"cd '{d}' 2>/dev/null && md5sum {names} 2>/dev/null", check=False).decode()
            for line in out.splitlines():
                if line.strip():
                    md5[line.split(None, 1)[1].strip()] = (line.split()[0], d)
        for p in paths:
            if p.name not in md5:
                log(f"not on storage: {p.name}")
                bad += 1
                continue
            m, d = md5[p.name]
            data = runner.link.run(f"cat '{d}/{p.name}'")
            if hashlib.md5(data).hexdigest() != m:
                log(f"md5 mismatch: {p.name}; not cached")
                bad += 1
                continue
            tmp = p.with_suffix(".part")
            tmp.write_bytes(data)
            tmp.replace(p)
            n += 1
            if n % 100 == 0:
                log(f"fetched {n}")
    log(f"fetched {n}; missing or mismatched {bad}")
    return n, bad


def _window(wid):
    root, span = wid.split("__w")
    a, b = span.split("-")
    return RealWindow(root, float(a), float(b))


# ---- records
def closure(checks):
    c = next((c for c in checks if c.check == "closure"), None)
    return None if c is None else {"value": c.value, "passed": c.passed}


def remedy_steps(sl):
    steps = []
    for i in range(1, len(sl.runs)):
        settings, _, checks, change = sl.runs[i]
        if change.startswith("rolled back"):
            steps[-1]["kept"] = False
            continue
        steps.append({"change": change, "settings": settings.tag(), "closure_before": closure(sl.runs[i - 1][2]),
                      "closure_after": closure(checks), "kept": True})
    return steps


def count_calls(paths):
    """LLM calls in trace files: one line with a `call` per CLI call; and whether one hit the session limit."""
    n, limit = 0, False
    for t in paths:
        for line in Path(t).read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            if "call" in d:
                n += 1
                limit = limit or LIMIT_TEXT in json.dumps(d.get("call"))
    return n, limit


def wait_memory(free_gb=vm_free_gb, sleep=time.sleep, min_gb=VM_MIN_GB):
    while (free := free_gb()) < min_gb:
        print(f"VM memory {free:.2f} GB free, below {min_gb} GB; waiting 60 s", flush=True)
        sleep(60)


class Run:
    """The collector of the integrated run and its auditor step. Folders under OUT: windows/ (one record per final
    window), traces/ (diagnostician trace per window), paused/ (set-aside traces of paused windows), set_aside/
    (session-limit traces), audit/<root>/ (auditor trace and record)."""

    def __init__(self, runner, out, rows, launcher=None, cap=LLM_CAP, stop_at=None, clock=datetime.datetime.now,
                 free_gb=vm_free_gb, sleep=time.sleep, orchestrator=None, auditor=None, log=print):
        self.runner, self.out, self.rows, self.launcher = runner, Path(out), rows, launcher
        self.cap, self.stop_at, self.clock, self.free_gb, self.sleep, self.log = cap, stop_at, clock, free_gb, sleep, log
        for d in ("windows", "traces", "paused", "set_aside", "audit"):
            (self.out / d).mkdir(parents=True, exist_ok=True)
        self.calls = count_calls(self.out.rglob("*trace*.jsonl"))[0]
        self.stopping = None
        self.windows_of = OrderedDict()               # root -> [window id], dispatcher order
        self._orch = orchestrator
        self._auditor = auditor
        self.done_count = 0

    # paths
    def rec_path(self, wid):
        return self.out / "windows" / f"{wid}.json"

    def final(self, wid):
        p = self.rec_path(wid)
        return p.exists() and json.loads(p.read_text())["status"] != "paused"

    def roots_to_audit(self):
        return sum(1 for r in self.windows_of if not (self.out / "audit" / r / "audit.json").exists())

    def collector(self, task):
        w = RealWindow(task.root_id, task.from_h, task.to_h)
        if self.stopping or self.final(w.id()):
            return {"skipped": True}
        if self.stop_at is not None and self.clock() >= self.stop_at:
            self.stopping = f"--stop-at {self.stop_at:%Y-%m-%d %H:%M} reached before {w.id()}"
            return {"skipped": True}
        try:
            rec = self.window(w)
        except StopRun as e:
            self.stopping = str(e)
            return {"skipped": True}
        self.rec_path(w.id()).write_text(json.dumps(rec, indent=1, default=str))
        self.done_count += 1
        self.log(f"window {w.id()}: {rec['status']} {rec.get('outcome', {}).get('status', '')} "
                 f"(calls {self.calls})", )
        if rec["status"] == "paused":
            with open(self.out / "paused.jsonl", "a") as f:
                f.write(json.dumps({"window": w.id(), "settings": rec["needs_settings"], "kinds": rec["needs_kinds"],
                                    "time": now()}) + "\n")
        return {"status": rec["status"]}

    def window(self, w):
        from agents.executors import Slice
        from real_slice import rule_outcome, summarize
        wid, row = w.id(), self.rows.get(w.id(), {})
        base = {"window": wid, "root": w.root_id, "condition": row.get("condition"), "batch": row.get("batch"),
                "from_h": w.from_h, "to_h": w.to_h, "time": now()}
        wait_memory(self.free_gb, self.sleep)
        trace = self.out / "traces" / f"{wid}_diagnostician_trace.jsonl"
        t0 = time.time()
        sl = None
        try:
            sl = Slice(self.runner, w, label=f"{wid} window")
            o = rule_outcome(sl.checks)
            decided = "rule"
            if o is None:
                self.pre_pause(w, sl)
                if self.calls + STEP_LIMIT + AUDIT_RESERVE * self.roots_to_audit() > self.cap:
                    raise StopRun(f"LLM calls {self.calls}: the next diagnostician window could pass the cap of "
                                  f"{self.cap}")
                trace.unlink(missing_ok=True)
                o = self.orchestrate(trace, wid, sl)
                decided = "diagnostician"
                n, limit = count_calls([trace])
                self.calls += n
                if limit:
                    shutil.move(str(trace), str(self.out / "set_aside" / f"{wid}_{int(time.time())}.jsonl"))
                    raise StopRun(f"{wid}: session limit; trace set aside, window reruns on the next start")
        except Paused as p:
            if trace.exists():
                self.calls += count_calls([trace])[0]     # spent calls count toward the cap
                shutil.move(str(trace), str(self.out / "paused" / f"{wid}_{int(time.time())}_trace.jsonl"))
            return dict(base, status="paused", reason=str(p), needs_settings=p.settings.to_dict(),
                        needs_kinds=p.kinds, step=0 if sl is None else len(sl.runs),
                        wall_s=round(time.time() - t0, 1))
        except StopRun:
            raise
        except Exception as e:                            # noqa: BLE001 - a window error is its outcome
            return dict(base, status="error", error=f"{type(e).__name__}: {str(e)[:300]}",
                        wall_s=round(time.time() - t0, 1))
        s = summarize(sl, o)
        return dict(base, status="final", decided_by=decided, outcome=s["outcome"], remedies=remedy_steps(sl),
                    roll_backs=s["roll_backs"], initial_checks=s["initial_checks"], final_checks=s["final_checks"],
                    initial_closure=closure(sl.runs[0][2]), final_closure=closure(sl.checks),
                    final_settings=s["final_settings"], final_tag=sl.runs[-1][0].tag(),
                    llm={k: getattr(o, k, 0) for k in ("calls", "input_tokens", "output_tokens", "call_ms")},
                    wall_s=round(time.time() - t0, 1))

    def pre_pause(self, w, sl):
        """A failing window with any single-remedy track not cached is paused before any LLM call (2026-11-22; was: none
        cached): a remedy it picks may pause it, and the calls spent would be spent again on the rerun. Every missing
        single remedy is queued."""
        from retrack_queue import single_remedies
        singles = [s for _, _, s in single_remedies(sl.runs[0][0], sl.base_disk_radius, sl.runs[0][1].record)]
        missing = [s for s in singles if self.runner.missing(w, s)]
        if REMEDY_HOLD:
            with open(self.out / "paused.jsonl", "a") as f:
                for s in missing:
                    f.write(json.dumps({"window": w.id(), "settings": s.to_dict(),
                                        "kinds": self.runner.missing(w, s), "time": now()}) + "\n")
            raise Paused(w, singles[0] if singles else sl.runs[0][0], [],
                         reason="paused: remedy hold (inbox item 54; integrity gate not on main)")
        if missing:
            with open(self.out / "paused.jsonl", "a") as f:
                for s in missing[1:]:
                    f.write(json.dumps({"window": w.id(), "settings": s.to_dict(),
                                        "kinds": self.runner.missing(w, s), "time": now()}) + "\n")
            raise Paused(w, missing[0], self.runner.missing(w, missing[0]))

    def orchestrate(self, trace, wid, sl):
        if self._orch:
            return self._orch(trace, wid, sl)
        from agents.orchestrator import Orchestrator
        return Orchestrator(self.launcher, trace).run("diagnostician", wid, sl.task(), sl.executors())

    # auditor
    def audit_ready(self, final_now=False):
        out = []
        for root, wids in self.windows_of.items():
            if (self.out / "audit" / root / "audit.json").exists():
                continue
            recs = [json.loads(self.rec_path(w).read_text()) for w in wids if self.rec_path(w).exists()]
            finals = [r for r in recs if r["status"] != "paused"]
            if len(finals) == len(wids) or (final_now and finals):
                out.append((root, finals))
        return out

    def audit(self, final_now=False):
        from measure.remedies import TrackSettings
        n = 0
        for root, recs in self.audit_ready(final_now):
            if self.stopping:
                break
            d = self.out / "audit" / root
            d.mkdir(parents=True, exist_ok=True)
            accepted = [r for r in recs if r["status"] == "final" and r["outcome"]["status"] == "accept"]
            if not accepted:
                res = {"status": "not_called", "note": "no accepted window", "calls": 0}
            else:
                if self.calls + 10 > self.cap:
                    self.stopping = f"LLM calls {self.calls}: auditor for {root} could pass the cap of {self.cap}"
                    break
                summaries, records = [], []
                for r in accepted:
                    w = _window(r["window"])
                    summaries.append({"outcome": r["outcome"], "remedies": [x["change"] for x in r["remedies"]],
                                      "roll_backs": r["roll_backs"], "initial_checks": r["initial_checks"],
                                      "final_settings": r["final_settings"], "final_checks": r["final_checks"],
                                      "condition": r["condition"], "root_id": root, "window_h": [r["from_h"], r["to_h"]]})
                    records.append(self.runner.measure(w, TrackSettings(**r["final_settings"])).record)
                res = (self._auditor or _run_auditor)(summaries, records, self.launcher, d)
                n_calls, limit = count_calls([d / "auditor_trace.jsonl"]) if (d / "auditor_trace.jsonl").exists() \
                    else (res.get("calls", 0), False)
                self.calls += n_calls
                if limit:
                    shutil.move(str(d / "auditor_trace.jsonl"), str(self.out / "set_aside" /
                                                                    f"audit_{root}_{int(time.time())}.jsonl"))
                    self.stopping = f"auditor {root}: session limit; set aside"
                    break
            res.update(root=root, windows=[r["window"] for r in recs], accepted=[r["window"] for r in accepted],
                       final_now=final_now and len(recs) < len(self.windows_of[root]), time=now())
            (d / "audit.json").write_text(json.dumps(res, indent=1, default=str))
            n += 1
            self.log(f"auditor {root}: {res['status']} (calls {self.calls})")
        return n


def _run_auditor(summaries, records, launcher, d):
    from real_slice import run_auditor
    return run_auditor(summaries, records, launcher, d)


# ---- tree baseline
def run_tree_all(runner, run_dir, out, stop_at=None, clock=datetime.datetime.now, log=print, tree=None):
    """The remedy tree on every window whose first check fails in the integrated run (run records), skipping the
    windows the c026 tree reached. Paused windows as in the run."""
    from agents.baselines import run_tree
    from agents.executors import Slice
    tree = tree or run_tree
    out = Path(out)
    (out / "windows").mkdir(parents=True, exist_ok=True)
    reached = {p.stem for p in C026_TREE.glob("*.json")}
    todo = []
    for p in sorted(Path(run_dir, "windows").glob("*.json")):
        r = json.loads(p.read_text())
        if r["status"] == "final" and r["decided_by"] == "diagnostician" and r["window"] not in reached:
            todo.append(r)
    for r in todo:
        wid = r["window"]
        rp = out / "windows" / f"{wid}.json"
        if rp.exists() and json.loads(rp.read_text())["outcome"]["status"] != "paused":
            continue
        if stop_at is not None and clock() >= stop_at:
            return f"stopped: --stop-at reached before {wid}"
        wait_memory()
        t0 = time.time()
        w = _window(wid)
        try:
            sl = Slice(runner, w, label=f"{wid} window")
            o = tree(sl, step_limit=STEP_LIMIT, trace_path=out / "tree_trace.jsonl")
            rec = {"window": wid, "method": "remedy_tree", "outcome": asdict(o), "initial_closure": closure(sl.runs[0][2]),
                   "final_closure": closure(sl.checks), "final_settings": sl.runs[-1][0].tag(),
                   "remedies": remedy_steps(sl), "wall_s": round(time.time() - t0, 1)}
        except Paused as p:
            rec = {"window": wid, "method": "remedy_tree", "outcome": {"status": "paused"}, "reason": str(p),
                   "needs_settings": p.settings.to_dict(), "needs_kinds": p.kinds}
            with open(out / "paused.jsonl", "a") as f:
                f.write(json.dumps({"window": wid, "settings": p.settings.to_dict(), "kinds": p.kinds,
                                    "time": now()}) + "\n")
        except Exception as e:                            # noqa: BLE001
            rec = {"window": wid, "method": "remedy_tree", "outcome": {"status": "error"},
                   "error": f"{type(e).__name__}: {str(e)[:300]}"}
        rp.write_text(json.dumps(rec, indent=1, default=str))
        log(f"tree {wid}: {rec['outcome']['status']}")
    return "done"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["windows", "fetch", "run", "tree", "audit", "report"])
    ap.add_argument("--config", default=str(CONFIG))
    ap.add_argument("--out")
    ap.add_argument("--run")
    ap.add_argument("--tree")
    ap.add_argument("--stop-at")
    ap.add_argument("--final-now", action="store_true")
    ap.add_argument("--llm-cap", type=int, default=LLM_CAP)
    ap.add_argument("--roots", help="comma-separated root ids: run, fetch and audit only these (B5 demo)")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(errors="backslashreplace")
    roots = set(a.roots.split(",")) if a.roots else None
    rows = batch_rows()
    if roots is not None:
        rows = {w: r for w, r in rows.items() if _window(w).root_id in roots}
    stop_at = datetime.datetime.fromisoformat(a.stop_at) if a.stop_at else None
    if a.step == "windows":
        ws = window_list()
        c = Counter(rows.get(w.id(), {}).get("batch", "none") for w in ws)
        print(f"{len(ws)} windows, {len({w.root_id for w in ws})} roots; batch {dict(c)}")
        return 0
    if a.step == "report":
        import run_all_report
        return run_all_report.main(Path(a.run), Path(a.tree), Path(a.out), rows)
    runner = make_runner(a.config, rows)
    if a.step == "fetch":
        fetch(runner, rows)
        return 0
    if a.step == "tree":
        print(run_tree_all(runner, a.run, a.out, stop_at))
        return 0
    from agents.launcher import Launcher
    run = Run(runner, a.out, rows, launcher=Launcher(), cap=a.llm_cap, stop_at=stop_at)
    window_list_into(run, roots)              # every window of each root, so a root is audited only when complete
    if a.step == "audit":
        print(f"auditor runs: {run.audit(final_now=a.final_now)}; {run.stopping or ''}")
        return 0

    def collect(task):
        res = run.collector(task)
        if not run.stopping:
            run.audit()
        return res
    t0 = time.time()
    disp = dispatch(collect, roots)
    status = run.stopping or "done"
    with open(Path(a.out) / "run_log.jsonl", "a") as f:
        f.write(json.dumps({"time": now(), "status": status, "windows_this_start": run.done_count,
                            "calls": run.calls, "dispatcher": {k: disp[k] for k in ("status", "rounds")},
                            "wall_s": round(time.time() - t0, 1)}) + "\n")
    print(f"run: {status}; windows this start {run.done_count}; LLM calls {run.calls}")
    return 0


def window_list_into(run, roots=None):
    for w in window_list(roots):
        run.windows_of.setdefault(w.root_id, []).append(w.id())


if __name__ == "__main__":
    sys.exit(main())
