"""Task c026 (spec 2026-11-12): the remedy tree and the diagnostician over the batch-2 windows that fail closure.

  python scripts/batch2_agents.py windows [--args]                      # the 84 windows (proposal table)
  python scripts/batch2_agents.py fetch --config private/real_runner_c026.yaml
  python scripts/batch2_agents.py tree --config private/real_runner_c026.yaml --out staging/c026/tree
  python scripts/batch2_agents.py agents --config private/real_runner_c026.yaml --out staging/c026/agents
  python scripts/batch2_agents.py report --tree staging/c026/tree --agents staging/c026/agents \
      --out results/2026-11-12_batch2_agents

windows  The windows of results/2026-10-25_full_batch_2/windows.csv with outcome fail (closure above 19 px/h).
fetch    Copies each window's batch-2 tracks (1000 px, stride 1; the w10-12 reference and moved copy) from storage into
         the runner's local cache, md5 checked, so the first measurement of every window is the batch-2 track.
tree     The remedy tree (agents/baselines.py run_tree, step limit 8) on each window, root by root, through the same
         Slice, runner, remedies and checker the diagnostician uses (agents/executors.py). Remedy retracks are Slurm CPU
         jobs on cluster nodes (RealRunner `compute: cluster`), cached by window and settings tag. One record per window
         in OUT/windows/ (a restarted run skips them); a budget stop or a lost connection stops the run (Needs Andrew);
         any other error is the window's outcome. After the last window of a root its staged copy is cleared
         (ClusterCompute.clear_root: tracks md5-equal on storage first, DELETED.log).
agents   scripts/real_slice.py (dispatcher agent -> checker -> diagnostician) over the windows in groups of 21, in root
         order, without the auditor; a group whose traces hold the seat's session-limit message is set aside and run
         again (c023); no group starts once the LLM calls reach the cap. Then real_slice.py --audit-only over all
         windows (one auditor run).
report   Tables per method, agreement, disagreement list, windows.csv and the example traces. Writes outcome and check
         values only; REGR, growth-zone and flank values are masked.
"""
import argparse
import csv
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, OrderedDict
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.baselines import run_tree  # noqa: E402
from agents.executors import Slice  # noqa: E402
from measure.real_runner import RealWindow, vm_free_gb  # noqa: E402

BATCH2 = ROOT / "results" / "2026-10-25_full_batch_2" / "windows.csv"
STEP_LIMIT, GROUP, LLM_CAP, VM_MIN_GB = 8, 21, 700, 3.0
LIMIT_TEXT = "hit your session limit"                   # the seat's session-limit message (scripts/dispatcher_eval.py)
STOPS = ("BudgetStop", "MasterDown", "LinkDown")       # stop the run and ask Andrew; never a window outcome


def failing_windows(path=BATCH2):
    """[(RealWindow, batch-2 closure px/h)] with outcome fail, in the file's (root, window) order."""
    with open(path, newline="") as f:
        return [(RealWindow(r["root"], float(r["from_h"]), float(r["to_h"])), float(r["closure_px_per_h"]))
                for r in csv.DictReader(f) if r["outcome"] == "fail"]


def by_root(windows):
    out = OrderedDict()
    for w in windows:
        out.setdefault(w.root_id, []).append(w)
    return out


def wait_memory(free_gb=vm_free_gb, sleep=time.sleep, min_gb=VM_MIN_GB):
    while (free := free_gb()) < min_gb:
        print(f"VM memory {free:.2f} GB free, below {min_gb} GB; waiting 60 s", flush=True)
        sleep(60)


def closure(checks):
    c = next((c for c in checks if c.check == "closure"), None)
    return None if c is None else {"value": c.value, "passed": c.passed}


def tree_record(sl, out, batch2_closure, wall_s):
    """Outcome, remedies (kept or rolled back) with closure before and after each, final settings."""
    steps = []
    for i in range(1, len(sl.runs)):                 # a roll back appends the restored run (agents/executors.py)
        settings, _, checks, change = sl.runs[i]
        if change.startswith("rolled back"):
            steps[-1]["kept"] = False
            continue
        steps.append({"change": change, "settings": settings.tag(), "closure_before": closure(sl.runs[i - 1][2]),
                      "closure_after": closure(checks), "kept": True})
    return {"window": sl.rod.id(), "method": "remedy_tree", "outcome": asdict(out),
            "batch2_closure": batch2_closure, "initial_closure": closure(sl.runs[0][2]),
            "final_closure": closure(sl.checks), "final_settings": sl.runs[-1][0].tag(), "remedies": steps,
            "wall_s": round(wall_s, 1)}


def run_tree_windows(runner, windows, out, step_limit=STEP_LIMIT, free_gb=vm_free_gb, sleep=time.sleep,
                     clear=None, tree=run_tree):
    """windows: [(RealWindow, batch-2 closure)]. Returns 'done' or 'stopped: ...'."""
    out = Path(out)
    (out / "windows").mkdir(parents=True, exist_ok=True)
    closure_b2 = {w.id(): c for w, c in windows}
    for root, ws in by_root([w for w, _ in windows]).items():
        for w in ws:
            rec_path = out / "windows" / f"{w.id()}.json"
            if rec_path.exists():
                continue
            wait_memory(free_gb, sleep)
            t0 = time.time()
            try:
                sl = Slice(runner, w, label=f"{w.id()} window")
                o = tree(sl, step_limit=step_limit, trace_path=out / "tree_trace.jsonl")
                rec = tree_record(sl, o, closure_b2[w.id()], time.time() - t0)
            except Exception as e:                                   # noqa: BLE001 - recorded, or a stop
                if type(e).__name__ in STOPS:
                    (out / "stopped").write_text(f"{datetime.datetime.now().isoformat(timespec='seconds')} "
                                                 f"{w.id()}: {type(e).__name__}: {e}")
                    return f"stopped: {type(e).__name__}: {e}"
                rec = {"window": w.id(), "method": "remedy_tree", "outcome": {"status": "error"},
                       "error": f"{type(e).__name__}: {str(e)[:300]}", "batch2_closure": closure_b2[w.id()],
                       "wall_s": round(time.time() - t0, 1)}
            rec_path.write_text(json.dumps(rec, indent=1, default=str))
            n = len(list((out / "windows").glob("*.json")))
            print(f"window {n} of {len(windows)}: {w.id()} {rec['outcome']['status']}", flush=True)
        if clear:
            for r in clear(root):
                with open(out / "deletes.jsonl", "a") as f:
                    f.write(json.dumps(r) + "\n")
    (out / "tree.done").write_text(datetime.datetime.now().isoformat(timespec="seconds"))
    return "done"


# ---- agents: real_slice.py in groups
def groups(windows, size=GROUP):
    ids = [f"{w.root_id}:{w.from_h:g}-{w.to_h:g}" for w, _ in windows]
    return [ids[i:i + size] for i in range(0, len(ids), size)]


def trace_calls(run_dir):
    """LLM calls in a run folder: one trace line with a `call` per CLI call; and whether one hit the session limit."""
    n, limit = 0, False
    for t in Path(run_dir).glob("*_trace.jsonl"):
        for line in t.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            if "call" in d:
                n += 1
                limit = limit or LIMIT_TEXT in json.dumps(d.get("call"))
    return n, limit


def run_agent_groups(config, out, windows, slice_cmd=None, cap=LLM_CAP, per_window=8):
    """One real_slice.py run per group (g01, g02, ...); done when summary.json is written and no session limit."""
    out = Path(out)
    gs = groups(windows)
    for i, ids in enumerate(gs, 1):
        g = out / f"g{i:02d}"
        if (g / "summary.json").exists() and not trace_calls(g)[1]:
            continue
        used = sum(trace_calls(d)[0] for d in out.glob("g*") if (d / "summary.json").exists())
        if used + per_window * len(ids) + 30 > cap:          # 30: auditor (20) and dispatcher calls
            return f"stopped: {used} LLM calls; group {i} could pass the cap of {cap}"
        if g.exists():                       # unfinished or session-limited: set aside, run again (c023)
            shutil.move(str(g), str(out / f"set_aside_g{i:02d}_{int(time.time())}"))
        cmd = (slice_cmd or [sys.executable, str(ROOT / "scripts" / "real_slice.py")]) + [
            "--windows", *ids, "--config", *config, "--moved-span", "10-12", "--min-free-gb", f"{VM_MIN_GB:g}",
            "--no-auditor", "--out", str(g)]
        print(f"group {i} of {len(gs)}: {len(ids)} windows", flush=True)
        p = subprocess.run(cmd)
        if p.returncode != 0 or not (g / "summary.json").exists():
            return f"stopped: group {i} exit {p.returncode}"
        if trace_calls(g)[1]:
            return f"stopped: group {i} hit the session limit (set aside on the next start)"
    merged = merge_groups(out, len(gs))
    return f"groups done: {len(merged['tasks'])} windows"


def merge_groups(out, n):
    """One summary.json over every group, for real_slice.py --audit-only."""
    out = Path(out)
    tasks, disp = {}, []
    for i in range(1, n + 1):
        s = json.loads((out / f"g{i:02d}" / "summary.json").read_text())
        tasks.update(s["tasks"])
        disp.append(s["dispatcher"])
        first = s
    merged = {"windows": [[t["root_id"], *t["window_h"]] for t in tasks.values()], "dispatcher_mode": "agent",
              "dispatcher_groups": disp, "tasks": tasks, "auditor": None, "model": first.get("model"),
              "claude_code": first.get("claude_code"), "groups": n}
    (out / "summary.json").write_text(json.dumps(merged, indent=1, default=str))
    return merged


def fetch(runner, windows, storage_dir, moved_span=(10.0, 12.0)):
    """Batch-2 tracks storage -> local cache (cache names of the runner), md5 compared on both ends."""
    from measure.remedies import TrackSettings
    n = 0
    for w in windows:
        kinds = ["ref", "moved"] if (w.from_h, w.to_h) == moved_span else ["window"]
        for k in kinds:
            local = runner.cache_path(w, TrackSettings(stride=1), k)
            if local.exists():
                continue
            # per-root folder (batch-2 roots 51-90, and every window track); flat tracks/ (moved copies, roots 1-50)
            src = next(p for p in (f"{storage_dir}/{w.root_id}/tracks/{local.name}", f"{storage_dir}/tracks/{local.name}")
                       if runner.link.run(f"test -s '{p}' && echo yes || echo no").decode().strip() == "yes")
            data = runner.link.run(f"cat '{src}'")
            md5 = runner.link.run(f"md5sum < '{src}'").decode().split()[0]
            if hashlib.md5(data).hexdigest() != md5:
                raise RuntimeError(f"md5 mismatch fetching {local.name}")
            local.write_bytes(data)
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["windows", "fetch", "tree", "agents", "report"])
    ap.add_argument("--config", nargs="+", default=[str(ROOT / "private" / "real_runner_c026.yaml")])
    ap.add_argument("--out")
    ap.add_argument("--args", action="store_true", help="windows: print ROOT:A-B arguments for real_slice.py")
    ap.add_argument("--tree")
    ap.add_argument("--agents")
    ap.add_argument("--storage-dir", help="fetch: the batch-2 output folder on storage (default: config batch2_dir)")
    a = ap.parse_args()
    windows = failing_windows()
    if a.step == "windows":
        for w, c in windows:
            print(f"{w.root_id}:{w.from_h:g}-{w.to_h:g}" if a.args else f"{w.id()}\t{c:.1f}")
        return
    if a.step == "report":
        import batch2_agents_report as R
        return R.main(Path(a.tree), Path(a.agents), Path(a.out), windows)
    if a.step == "agents":
        print(run_agent_groups(a.config, Path(a.out), windows))
        return
    import yaml
    from measure.real_runner import RealRunner
    cfg = yaml.safe_load(Path(a.config[0]).read_text())
    runner = RealRunner(cfg)
    runner.moved_span = (10.0, 12.0)
    if a.step == "fetch":
        print(f"fetched {fetch(runner, [w for w, _ in windows], a.storage_dir or cfg['batch2_dir'])} tracks")
        return
    runner.relay.require_master()
    runner.relay.link.run(f"mkdir -p '{runner.work}/tracks'")
    runner.sync_code()

    def clear(root):
        return runner.cc.clear_root(root, runner.work, f"root {root}: c026 remedy-tree retracks md5-verified on "
                                    "storage; one staged root at a time (spec 2026-11-12)")
    status = run_tree_windows(runner, windows, Path(a.out), clear=clear)
    (Path(a.out) / "runner_log.json").write_text(json.dumps(runner.log + runner.cc.log, indent=1, default=str))
    print(status)


if __name__ == "__main__":
    main()
