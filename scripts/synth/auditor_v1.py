"""Auditor v1 (spec 2026-10-13, Task A) on the scored runs v1. No tracker runs.

  python scripts/synth/auditor_v1.py views                                   # 8 batch views from the cached final records
  python scripts/synth/auditor_v1.py rule                                    # rule auditor on all 8 batches
  python scripts/synth/auditor_v1.py llm --set dev|heldout [--method M] [--repeat K]   # LLM auditor
  python scripts/synth/auditor_v1.py eval                                    # score both auditors

A batch: the final records of one method on one set of results/2026-10-12b_scored_v1/ (dev 25 runs, held-out
15). Final records come from the staging caches the scored runs used (scripts/synth/scored_v1.py); a record not
in the cache stops the script. Outputs in results/2026-10-13_auditor_v1/:
- views/<set>_<method>.json: what the auditor sees (batch table, run records, batch statistics)
- id_map.json: opaque run id -> scored-v1 run; for scoring only, never shown to an auditor
- rule/<set>_<method>.json; llm/<set>_<method>_<n>_trace.jsonl and _result.json
LLM runs need a clean tracked tree (each records the commit).
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import rule  # noqa: E402
from audit.view import batch_table, batch_view  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from scored_v1 import METHODS, OUT as SCORED, Missing, ScoredRunner, rods, stem  # noqa: E402

OUT = ROOT / "results" / "2026-10-13_auditor_v1"
SETS = ("dev", "heldout")
MAX_DEV_RUNS = 40          # spec A4: at most 40 auditor calls on dev (one call = one auditor run on a batch)
MAX_RUNS = 52              # spec limits: at most 52 auditor calls in all


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def build(set_, method):
    rs = rods(set_)
    summaries, records = [], []
    for rod in rs:
        s = json.loads((SCORED / set_ / f"{stem(method, rod)}_summary.json").read_text())
        try:
            m = ScoredRunner().measure(rod, TrackSettings(**s["final_settings"]))
        except Missing as e:
            sys.exit(f"stop: final record not in the cache: {stem(method, rod)} ({e}); ask Andrew")
        summaries.append(s)
        records.append(m.record)
    views, stats, ids = batch_view(summaries, records, key=f"{set_}/{method}")
    return views, stats, {i: stem(method, rod) for i, rod in zip(ids, rs)}


def views_cmd():
    (OUT / "views").mkdir(parents=True, exist_ok=True)
    id_map = {}
    for set_ in SETS:
        for m in METHODS:
            views, stats, ids = build(set_, m)
            (OUT / "views" / f"{set_}_{m}.json").write_text(json.dumps(
                {"batch": f"{set_}_{m}", "table": batch_table(views, stats), "runs": views}, indent=1))
            id_map[f"{set_}_{m}"] = ids
            print(f"{set_} {m}: {len(views)} runs, {sum(v['status'] == 'accept' for v in views)} accepted")
    (OUT / "id_map.json").write_text(json.dumps(id_map, indent=1))


def load_view(set_, method):
    return json.loads((OUT / "views" / f"{set_}_{method}.json").read_text())


def rule_cmd():
    (OUT / "rule").mkdir(parents=True, exist_ok=True)
    for set_ in SETS:
        for m in METHODS:
            d = rule.audit(load_view(set_, m)["runs"])
            (OUT / "rule" / f"{set_}_{m}.json").write_text(json.dumps({"z_cutoff": rule.Z_CUTOFF, "decisions": d},
                                                                      indent=1))
            print(f"{set_} {m}: flagged {sum(x['decision'] == 'flag' for x in d.values())} of {len(d)} accepted")


def llm_runs():
    return sorted((OUT / "llm").glob("*_result.json")) if (OUT / "llm").exists() else []


def llm_cmd(set_, methods, repeat):
    from agents.launcher import Launcher
    from agents.orchestrator import Orchestrator
    from audit.llm import AuditBatch
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files are modified; commit first (each run records the commit)")
    launcher = Launcher()
    out = OUT / "llm"
    out.mkdir(parents=True, exist_ok=True)
    for m in methods:
        for _ in range(repeat):
            done = llm_runs()
            n_dev = sum(json.loads(f.read_text())["set"] == "dev" for f in done)
            if len(done) >= MAX_RUNS or (set_ == "dev" and n_dev >= MAX_DEV_RUNS):
                sys.exit(f"stop: auditor call limit reached ({len(done)} in all, {n_dev} on dev)")
            n = 1 + sum(f.name.startswith(f"{set_}_{m}_") for f in done)
            name = f"{set_}_{m}_{n}"
            trace = out / f"{name}_trace.jsonl"
            trace.unlink(missing_ok=True)
            batch = AuditBatch(load_view(set_, m))
            t0 = time.time()
            o = Orchestrator(launcher, trace).run("auditor", batch.label, batch.task(), batch.executors())
            res = {"set": set_, "method": m, "n": n, "commit": git("rev-parse", "--short", "HEAD"),
                   "claude_code": launcher.version, "model": launcher.cfg["model"], "wall_s": round(time.time() - t0, 1),
                   "outcome": o.__dict__, "decisions": batch.decisions, "undecided": batch.undecided(),
                   "report": o.args.get("text") if o.status == "report" else None}
            (out / f"{name}_result.json").write_text(json.dumps(res, indent=1))
            print(f"{name}: {o.status} steps {o.steps} flagged {sum(d['decision'] == 'flag' for d in batch.decisions.values())}"
                  f" cleared {sum(d['decision'] == 'clear' for d in batch.decisions.values())} undecided "
                  f"{len(batch.undecided())} tokens {o.input_tokens}/{o.output_tokens} call {o.call_ms / 1000:.1f} s",
                  flush=True)


# ------------------------------------------------------------------ scoring

def truth_rows():
    """scored-v1 per-run categories, keyed by run stem."""
    rows = json.loads((SCORED / "scores.json").read_text())
    out = {}
    for r in rows:
        if r.get("missing"):
            continue
        z =f"_z{r['size']}" if r.get("size") else ""
        out[(r["set"], f"{r['method']}_{r['fault']}{z}_s{r['seed']}")] = r
    return out


def group(r):
    """Scoring group of an accepted run: false_accept, alt_repair (second_root, width-free ratio, good centre;
    spec 2026-10-13 decisions), good_report."""
    if r["category"] == "false_accept":
        return "false_accept"
    if r["fault"] == "second_root" and r["category"] == "good_report":
        return "alt_repair"
    return r["category"]


def score(set_, method, decisions, id_map, truth):
    c = {g: [0, 0] for g in ("false_accept", "good_report", "alt_repair")}
    for rid, run in id_map[f"{set_}_{method}"].items():
        r = truth[(set_, run)]
        if r["status"] != "accept":
            continue
        g = group(r)
        c[g][1] += 1
        c[g][0] += decisions.get(rid, {}).get("decision") == "flag"
    return c


def cell(x):
    return f"{x[0]} / {x[1]}" if x[1] else "-"


def eval_cmd():
    id_map, truth = json.loads((OUT / "id_map.json").read_text()), truth_rows()
    L = ["# Auditor v1: scores", "",
         "Cells: flagged / runs in the group, accepted runs only. False flags = good reports flagged. "
         "alt_repair: second_root runs that applied `use_width_free_ratio` and accepted a good centre; reported apart.",
         "", "## Rule auditor (|z| > 3 or a failed final check)", "",
         "| Set | Method | Accepted | False accepts flagged | Good reports flagged | alt_repair flagged |",
         "| :-- | :-- | --: | :-- | :-- | :-- |"]
    for set_ in SETS:
        for m in METHODS:
            d = json.loads((OUT / "rule" / f"{set_}_{m}.json").read_text())["decisions"]
            c = score(set_, m, d, id_map, truth)
            L.append(f"| {set_} | {m} | {len(d)} | {cell(c['false_accept'])} | {cell(c['good_report'])} | "
                     f"{cell(c['alt_repair'])} |")
    L += ["", "## LLM auditor, per run", "",
          "| Run | Commit | Status | Steps | Undecided | False accepts flagged | Good reports flagged | "
          "alt_repair flagged | Tokens in | Tokens out | Call time (s) |",
          "| :-- | :-- | :-- | --: | --: | :-- | :-- | :-- | --: | --: | --: |"]
    for f in llm_runs():
        r = json.loads(f.read_text())
        c = score(r["set"], r["method"], r["decisions"], id_map, truth)
        o = r["outcome"]
        L.append(f"| {r['set']}_{r['method']}_{r['n']} | {r['commit']} | {o['status']} | {o['steps']} | "
                 f"{len(r['undecided'])} | {cell(c['false_accept'])} | {cell(c['good_report'])} | "
                 f"{cell(c['alt_repair'])} | {o['input_tokens']} | {o['output_tokens']} | {o['call_ms'] / 1000:.1f} |")
    text = "\n".join(L) + "\n"
    (OUT / "scores.md").write_text(text)
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["views", "rule", "llm", "eval"])
    ap.add_argument("--set", choices=SETS)
    ap.add_argument("--method", choices=METHODS)
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "views":
        views_cmd()
    elif a.cmd == "rule":
        rule_cmd()
    elif a.cmd == "llm":
        if not a.set:
            ap.error("--set is required")
        llm_cmd(a.set, [a.method] if a.method else list(METHODS), a.repeat)
    else:
        eval_cmd()


if __name__ == "__main__":
    main()
