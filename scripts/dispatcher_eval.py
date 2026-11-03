"""Dispatcher agent vs fixed script on the fake queue (task c023; proposal docs/proposals/2026-11-02_dispatcher-eval.md).

  python scripts/dispatcher_eval.py run [--scenarios S0 S1 ...] [--seeds 0 1 ...] [--methods script agent]
  python scripts/dispatcher_eval.py report

`run`: one batch per scenario, seed and method over the 102 include-yes roots on `FakeQueue`. Each batch writes
staging/c023/batches/<scenario>_s<seed>_<method>.json when it ends; a restarted run skips finished batches. Agent
traces in staging/c023/traces/. Waits before each agent batch while free VM memory is below 3 GB. At most 60 agent
batches in total (files in staging/c023/agent_batches.log). No real job.
`report`: results/2026-11-02_dispatcher_eval/batches.csv and README tables (median and range over seeds).
"""
import argparse
import csv
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents import dispatcher as D  # noqa: E402
from measure.real_runner import vm_free_gb  # noqa: E402

STAGE = ROOT / "staging" / "c023"
OUT = ROOT / "results" / "2026-11-02_dispatcher_eval"
SCENARIOS = ("S0", "S1", "S2", "S3", "S4")
SEEDS = (0, 1, 2, 3, 4)
ATTEMPTS = 10                   # fault draws per window (the engine allows at most 3 starts)
ROUND_LIMIT = 200
AGENT_BATCH_CAP = 60
MIN_FREE_GB = 3.0
BUDGET_SHARE = 0.70


class ScenarioQueue(D.FakeQueue):
    """FakeQueue with one preemption burst: every job running at `burst_minute` fails then (cause preempt)."""

    def __init__(self, burst_minute=None, **kw):
        super().__init__(**kw)
        self.burst_minute, self.preempted = burst_minute, 0

    def advance(self, minutes):
        t = self.burst_minute
        if t is not None and self.now < t <= self.now + minutes:
            for j in self.jobs.values():
                if j["start"] <= t < j["end"]:
                    j["end"], j["outcome"] = t, "preempt"
                    self.preempted += 1
        super().advance(minutes)


def scenario(name, seed, rows, cfg):
    """Fault draws per window and attempt, burst minute, budget, persistent root. Same for both methods."""
    rng = random.Random(f"{name}-{seed}")
    tasks = [t for r in rows for t in D.make_tasks(r, cfg)]
    total = sum(t.core_h for t in tasks)
    p = {"S1": 0.10, "S2": 0.25, "S3": 0.10}.get(name, 0.0)
    faults = {t.id: ["crash" if rng.random() < p else "ok" for _ in range(ATTEMPTS)] for t in tasks}
    burst = rng.uniform(60, 300) if name == "S2" else None
    budget = {"core_hours": 0.0, "usd": 0.0, "approved": False}
    if name == "S3":
        ch = round(BUDGET_SHARE * total, 2)
        budget = {"core_hours": ch, "usd": round(ch * cfg["timing"]["cluster_usd_per_core_h"], 2), "approved": True}
    bad_root = None
    if name == "S4":
        bad_root = rng.choice([r["id"] for r in rows])
        for t in tasks:
            if t.root_id == bad_root:
                faults[t.id] = ["crash"] * ATTEMPTS
    faults = {k: v for k, v in faults.items() if "crash" in v}
    return {"faults": faults, "burst_minute": burst, "budget": budget, "bad_root": bad_root,
            "windows": len(tasks), "core_h": total}


def run_script_budget_batch(engine, poll_minutes=30, round_limit=ROUND_LIMIT):
    """S3 fixed script (proposal): in manifest order a root's pending windows go to the cluster if their
    core-hours fit the budget left, else to the lab server; a retry the budget refuses goes to the lab server.
    Otherwise as run_script_batch: poll every 30 min, collect, retry a failed window once."""
    roots = list(engine.rows)
    engine.split_root({"root_ids": roots})
    for rid in roots:
        need = sum(t.core_h for t in engine.root_tasks(rid) if t.state == "pending")
        backend = "cluster" if need <= engine.cluster_left_h() + 1e-9 else "lab_server"
        engine.submit({"root_ids": [rid], "backend": backend})
    status, rounds = "round_limit", 0
    for n in range(1, round_limit + 1):
        rounds = n
        engine.refresh()
        engine.collect({"root_ids": roots})
        failed = [t for t in engine.tasks.values() if t.state == "failed"]
        for t in failed:                              # give up first: a retry by root id retries every failed
            if t.retries >= 1:                        # window of the root, so a later entry of the same root
                t.state = "gave_up"                   # would read as already retried
        again = sorted({t.root_id for t in failed if t.state == "failed"})
        if again:
            engine.retry({"root_ids": again})
        stuck = sorted({t.root_id for t in engine.tasks.values() if t.state == "pending"})
        if stuck:                                     # cluster retry refused: to the lab server
            engine.submit({"root_ids": stuck, "backend": "lab_server"})
        if not engine.live() and not any(t.state in ("pending", "done", "failed") for t in engine.tasks.values()):
            status = "finish"; break
        engine.advance(poll_minutes)
    engine.refresh()
    return {"status": status, "rounds": rounds, **engine.summary()}


def llm_calls(trace):
    if not trace or not Path(trace).exists():
        return 0
    n = 0
    for line in Path(trace).read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        n += bool(d.get("call"))
    return n


def metrics(engine, queue, out, sc, method, name, seed, trace=None, wall_s=0.0):
    tasks = list(engine.tasks.values())
    cluster_used = sum(t.used_core_h for t in tasks if t.backend == "cluster")
    bad = sc["bad_root"]
    return {
        "scenario": name, "seed": seed, "method": method, "status": out["status"],
        "sim_h": round(queue.now / 60, 2),
        "collected": sum(t.state == "collected" for t in tasks), "windows": sc["windows"],
        "gave_up": sum(t.state == "gave_up" for t in tasks),
        "left_failed_or_pending": sum(t.state in ("failed", "pending", "done") for t in tasks),
        "retries": engine.stats["retries"], "jobs_started": len(queue.jobs),
        "jobs_failed": sum(j["outcome"] != "ok" for j in queue.jobs.values()), "preempted": queue.preempted,
        "bad_root": bad or "", "jobs_on_bad_root": (sum(1 for j in queue.jobs.values()
                                                        if engine.tasks[j["task"]].root_id == bad) if bad else 0),
        "budget_core_h": sc["budget"]["core_hours"], "cluster_core_h": round(cluster_used, 2),
        "budget_overrun_core_h": round(max(0.0, cluster_used - sc["budget"]["core_hours"]), 4),
        "budget_requests": engine.stats["approvals"], "cluster_refused": engine.stats["cluster_refused"],
        "rounds": out["rounds"], "llm_calls": llm_calls(trace), "wall_s": round(wall_s, 1),
    }


def run_one(name, seed, method, rows, cfg, launcher=None):
    sc = scenario(name, seed, rows, cfg)
    q = ScenarioQueue(burst_minute=sc["burst_minute"], faults=sc["faults"])
    e = D.Engine(q, cfg, rows=rows, budget=sc["budget"])
    t0, trace = time.time(), None
    if method == "agent":
        trace = STAGE / "traces" / f"{name}_s{seed}.jsonl"
        trace.parent.mkdir(parents=True, exist_ok=True)
        trace.unlink(missing_ok=True)
        out = D.run_agent_batch(e, launcher, trace, round_limit=ROUND_LIMIT, on_approval="deny")
    elif name == "S3":
        out = run_script_budget_batch(e)
    else:
        out = D.run_script_batch(e, round_limit=ROUND_LIMIT)
    return metrics(e, q, out, sc, method, name, seed, trace, time.time() - t0)


LIMIT_TEXT = "hit your session limit"


def hit_session_limit(trace):
    """A CLI call refused for the seat's session limit: the batch measures the seat, not the agent."""
    return Path(trace).exists() and LIMIT_TEXT in Path(trace).read_text(encoding="utf-8")


def agent_batches_started():
    log = STAGE / "agent_batches.log"
    return len(log.read_text().splitlines()) if log.exists() else 0


def cmd_run(a):
    cfg, rows = D.load_config(), D.manifest_rows()
    assert len(rows) == 102, f"{len(rows)} include-yes roots, proposal expects 102"
    (STAGE / "batches").mkdir(parents=True, exist_ok=True)
    launcher = None
    for name in a.scenarios:
        for seed in a.seeds:
            for method in a.methods:
                f = STAGE / "batches" / f"{name}_s{seed}_{method}.json"
                if f.exists():
                    continue
                if method == "agent":
                    if agent_batches_started() >= AGENT_BATCH_CAP:
                        sys.exit(f"agent batch cap {AGENT_BATCH_CAP} reached")
                    while (free := vm_free_gb()) < MIN_FREE_GB:
                        print(f"VM memory {free:.2f} GB free, below {MIN_FREE_GB} GB; waiting 60 s", flush=True)
                        time.sleep(60)
                    if launcher is None:
                        from agents.launcher import Launcher
                        launcher = Launcher()
                    with open(STAGE / "agent_batches.log", "a") as log:
                        log.write(f"{time.strftime('%Y-%m-%d %H:%M')} {name} s{seed}\n")
                m = run_one(name, seed, method, rows, cfg, launcher)
                trace = STAGE / "traces" / f"{name}_s{seed}.jsonl"
                if method == "agent" and hit_session_limit(trace):      # not recorded; the run stops (c023)
                    keep = STAGE / "limit_errors" / f"{name}_s{seed}_{time.strftime('%Y%m%d%H%M')}.jsonl"
                    keep.parent.mkdir(parents=True, exist_ok=True)
                    trace.replace(keep)
                    sys.exit(f"{name} s{seed}: Claude session limit hit; batch not recorded, run stopped "
                             f"(trace {keep.relative_to(ROOT)}). Rerun after the limit resets")
                f.write_text(json.dumps(m, indent=1))
                print(f"{name} s{seed} {method}: {m['status']}, {m['collected']}/{m['windows']} collected, "
                      f"{m['sim_h']} h, retries {m['retries']}, rounds {m['rounds']}, calls {m['llm_calls']}",
                      flush=True)
        print(f"scenario {name} done", flush=True)


COLUMNS = [("sim_h", "time to finish, h"), ("collected", "collected"), ("retries", "retries"),
           ("jobs_on_bad_root", "jobs on persistent-fault root"), ("budget_overrun_core_h", "budget overrun, core-h"),
           ("budget_requests", "budget requests"), ("cluster_core_h", "cluster core-h"), ("rounds", "rounds"),
           ("llm_calls", "LLM calls")]


def cell(vals):
    med = statistics.median(vals)
    lo, hi = min(vals), max(vals)
    f = (lambda v: f"{v:g}")
    return f(round(med, 2)) if lo == hi else f"{f(round(med, 2))} ({f(round(lo, 2))}-{f(round(hi, 2))})"


def cmd_report(a):
    ms = [json.loads(p.read_text()) for p in sorted((STAGE / "batches").glob("*.json"))]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "batches.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ms[0]))
        w.writeheader()
        w.writerows(sorted(ms, key=lambda m: (m["scenario"], m["method"], m["seed"])))
    md = []
    for name in SCENARIOS:
        group = [m for m in ms if m["scenario"] == name]
        if not group:
            continue
        md += [f"### {name}", "", "| metric | " + " | ".join(mt for mt in ("script", "agent")) + " |",
               "| :-- | :-- | :-- |"]
        for key, label in COLUMNS:
            row = []
            for mt in ("script", "agent"):
                vals = [m[key] for m in group if m["method"] == mt]
                row.append(cell(vals) if vals else "-")
            md.append(f"| {label} | " + " | ".join(row) + " |")
        st = {mt: sorted({m["status"] for m in group if m["method"] == mt}) for mt in ("script", "agent")}
        n = {mt: sum(m["method"] == mt for m in group) for mt in ("script", "agent")}
        md.append(f"| end status | {', '.join(st['script']) or '-'} ({n['script']} seeds) | "
                  f"{', '.join(st['agent']) or '-'} ({n['agent']} seeds) |")
        md.append("")
    (OUT / "tables.md").write_text("\n".join(md))
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--scenarios", nargs="+", default=list(SCENARIOS), choices=SCENARIOS)
    r.add_argument("--seeds", nargs="+", type=int, default=list(SEEDS))
    r.add_argument("--methods", nargs="+", default=["script", "agent"], choices=["script", "agent"])
    sub.add_parser("report")
    a = ap.parse_args()
    {"run": cmd_run, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main()
