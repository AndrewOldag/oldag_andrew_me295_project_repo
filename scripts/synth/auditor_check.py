"""Auditor check with planted errors (spec 2026-11-18, section E; task c030). VM only, no tracker runs.

  python scripts/synth/auditor_check.py plan          # batches.json and plants.json (commit before any run)
  python scripts/synth/auditor_check.py views         # views/bNN.json: what the auditor sees
  python scripts/synth/auditor_check.py rule          # rule auditor (no LLM), for reference
  python scripts/synth/auditor_check.py llm --repeat K [--max-runs N]
  python scripts/synth/auditor_check.py eval          # scores.md, scores.json

Batches: good, accepted freeze v4 runs (results/2026-10-25_freeze_v4/scores.json: status accept, category
good_report, every final check passed), grouped by row of the v4 set (8 runs of one row, as the windows of one
root), 30 batches. One planted error in 15 batches, chosen by seed (proposal
docs/proposals/2026-11-18_auditor-check.md). Final records from the freeze v4 tracker cache
(staging/tracks_freeze_v4, VM). The auditor: audit/llm.py, prompt agents/prompts/auditor.md, pinned model,
unchanged; it sees only the batch view (audit/view.py), with opaque run ids.
"""
import argparse
import copy
import json
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import rule  # noqa: E402
from audit.view import batch_table, batch_view  # noqa: E402
from checker import load_thresholds, run_checks  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

OUT = ROOT / "results" / "2026-11-18_auditor_check"
V4 = ROOT / "results" / "2026-10-25_freeze_v4"
V4_CACHE = ROOT / "staging" / "tracks_freeze_v4"
SEED = 1118                                  # batches and plants (proposal, section 2)
BATCH = 8
EXTRA = ("bad_stage_correction", "v3_growth_zone", "rigid_drift")    # rows with a fourth batch
KINDS = ("closure_relabelled", "other_rod_track", "wrong_unit", "doubled_frame")
PLANTS = {"closure_relabelled": 4, "other_rod_track": 4, "wrong_unit": 4, "doubled_frame": 3}
UNIT_FACTOR = 2.105                          # um per px: velocities in um/h read as px/h
NO_GROWTH = ("v3_still",)                    # wrong_unit and doubled_frame change nothing on a still rod
REPEATS = (0, 1, 2)
MAX_LLM_RUNS = 150                           # spec E2, counted as auditor runs (one run = one batch)


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def summary(stem):
    return json.loads((V4 / "runs" / f"{stem}_summary.json").read_text())


def stem_of(r):
    return f"{r['method']}_{r['rod']}" + (f"_r{r['repeat']}" if r["method"] in ("diagnostician", "single_agent") else "")


def track_file(rod_id, settings, moved=False):
    st = replace(TrackSettings(**settings), width_free=False)
    return V4_CACHE / f"{rod_id}{'_moved' if moved else ''}__{st.tag()}.npz"


def record(stem, moved=False):
    s = summary(stem)
    f = track_file(s["rod"]["id"], s["final_settings"], moved)
    if not f.exists():
        sys.exit(f"stop: final record not in the v4 cache: {f.name}")
    return from_tracker_npz(f)


# ------------------------------------------------------------------ plan

def pool():
    """Good accepted v4 runs with every final check passed, by row."""
    rows = json.loads((V4 / "scores.json").read_text())
    by = defaultdict(list)
    for r in rows:
        if r.get("missing") or r["status"] != "accept" or r["category"] != "good_report":
            continue
        s = summary(stem_of(r))
        if all(c["passed"] is not False for c in s["final_checks"]):
            by[r["kind"]].append(stem_of(r))
    return {k: sorted(v) for k, v in sorted(by.items())}


def closure_sources():
    """Accepted v4 runs on bad_stage_correction whose final closure failed and every other check passed."""
    rows = json.loads((V4 / "scores.json").read_text())
    out = []
    for r in rows:
        if r.get("missing") or r["status"] != "accept" or r["kind"] != "bad_stage_correction":
            continue
        ch = {c["check"]: c["passed"] for c in summary(stem_of(r))["final_checks"]}
        if ch.get("closure") is False and all(v is not False for k, v in ch.items() if k != "closure"):
            out.append(stem_of(r))
    return sorted(out)


def plan():
    rng = random.Random(SEED)
    runs = pool()
    batches = []
    for row in runs:
        for k in range(3 + (row in EXTRA)):
            batches.append({"row": row, "runs": sorted(rng.sample(runs[row], BATCH))})
    rng.shuffle(batches)
    for i, b in enumerate(batches):
        b["batch"] = f"b{i + 1:02d}"
    kinds = [k for k, n in PLANTS.items() for _ in range(n)]
    srcs = closure_sources()
    # closure_relabelled: in the bad_stage_correction batches (their source runs fail closure only)
    bsc = [b for b in batches if b["row"] == "bad_stage_correction"]
    plants = []
    for b in bsc[:PLANTS["closure_relabelled"]]:
        plants.append({"batch": b["batch"], "kind": "closure_relabelled", "source": rng.choice(srcs)})
    rest = [k for k in kinds if k != "closure_relabelled"]
    rng.shuffle(rest)
    free = [b for b in batches if b["row"] != "bad_stage_correction"]
    rng.shuffle(free)
    used = set()
    for kind in rest:
        b = next(x for x in free if x["batch"] not in used and not (kind in ("wrong_unit", "doubled_frame")
                                                                       and x["row"] in NO_GROWTH))
        used.add(b["batch"])
        p = {"batch": b["batch"], "kind": kind}
        if kind == "other_rod_track":
            others = [s for row, ss in runs.items() if row != b["row"] and row not in (
                NO_GROWTH if b["row"] in NO_GROWTH else ()) for s in ss]
            p["source"] = rng.choice(sorted(others))
        if kind == "doubled_frame":
            p["frame"] = rng.randrange(14, 27)          # middle third of the 41 frames
        plants.append(p)
    for p in plants:
        b = next(x for x in batches if x["batch"] == p["batch"])
        p["target"] = rng.choice(b["runs"])             # the run the plant replaces or changes
    plants.sort(key=lambda p: p["batch"])
    return batches, plants, srcs


# ------------------------------------------------------------------ plants

def doubled(rec, k):
    """Frame k shown twice (frame k+1 replaced by k), later frames one late; the last frame drops. Times kept."""
    shift = lambda a: np.concatenate([a[:k + 1], a[k:-1]])
    return replace(rec, stage_px=shift(rec.stage_px), centre=shift(rec.centre), plus=shift(rec.plus),
                   minus=shift(rec.minus), midline=shift(rec.midline), _fields=None)


def wrong_unit(rec):
    f = dict(rec.fields)
    for k in ("v_mid", "regr_mid", "regr_plus", "regr_minus"):
        f[k] = f[k] * UNIT_FACTOR
    return replace(rec, _fields=f)


def planted_run(p):
    """(summary, record) the auditor sees for the planted run."""
    t = summary(p["target"])
    if p["kind"] == "closure_relabelled":
        s = copy.deepcopy(summary(p["source"]))
        for c in s["final_checks"]:
            if c["check"] == "closure":
                c["passed"] = True
        return s, record(p["source"])
    s = copy.deepcopy(t)
    if p["kind"] == "other_rod_track":
        return s, record(p["source"])
    if p["kind"] == "wrong_unit":
        return s, wrong_unit(record(p["target"]))
    rec, mov = doubled(record(p["target"]), p["frame"]), doubled(record(p["target"], True), p["frame"])
    skip = ("plane_sections",) if s["final_settings"].get("width_free") else ()
    s["final_checks"] = [c.to_dict() for c in run_checks(rec, mov, load_thresholds(), skip)]
    return s, rec


def views_cmd():
    batches = json.loads((OUT / "batches.json").read_text())["batches"]
    plants = {p["batch"]: p for p in json.loads((OUT / "plants.json").read_text())["plants"]}
    (OUT / "views").mkdir(parents=True, exist_ok=True)
    id_map = {}
    for b in batches:
        summaries, records, stems = [], [], []
        p = plants.get(b["batch"])
        for st in b["runs"]:
            if p and st == p["target"]:
                s, r = planted_run(p)
                stems.append(f"PLANT:{p['kind']}:{st}")
            else:
                s, r = summary(st), record(st)
                stems.append(st)
            summaries.append(s)
            records.append(r)
        views, stats, ids = batch_view(summaries, records, key=f"c030/{b['batch']}")
        (OUT / "views" / f"{b['batch']}.json").write_text(json.dumps(
            {"batch": b["batch"], "table": batch_table(views, stats), "runs": views}, indent=1))
        id_map[b["batch"]] = dict(zip(ids, stems))
        print(f"{b['batch']} {b['row']}: {len(views)} runs" + (f", plant {p['kind']}" if p else ""))
    (OUT / "run_map.json").write_text(json.dumps(id_map, indent=1))


def load_view(b):
    return json.loads((OUT / "views" / f"{b}.json").read_text())


def rule_cmd():
    (OUT / "rule").mkdir(parents=True, exist_ok=True)
    for f in sorted((OUT / "views").glob("b*.json")):
        d = rule.audit(load_view(f.stem)["runs"])
        (OUT / "rule" / f.name).write_text(json.dumps({"z_cutoff": rule.Z_CUTOFF, "decisions": d}, indent=1))


# ------------------------------------------------------------------ LLM auditor

def llm_results():
    return sorted((OUT / "llm").glob("*_result.json")) if (OUT / "llm").exists() else []


def llm_cmd(repeat, max_runs):
    from agents.launcher import Launcher
    from agents.orchestrator import Orchestrator
    from audit.llm import AuditBatch
    from heldout_compound import wait_memory
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files are modified; commit first (each run records the commit)")
    if git("status", "--porcelain", "--", str(OUT / "plants.json")) or not git("ls-files", "--", str(OUT / "plants.json")):
        sys.exit("plant list not committed: no auditor run before (spec E1)")
    launcher = Launcher()
    out = OUT / "llm"
    out.mkdir(parents=True, exist_ok=True)
    started = 0
    for f in sorted((OUT / "views").glob("b*.json")):
        name = f"{f.stem}_r{repeat}"
        if (out / f"{name}_result.json").exists():
            continue
        if len(llm_results()) + len(list((out / "usage_limit").glob("*_result.json"))) >= MAX_LLM_RUNS:
            sys.exit(f"stop: auditor run cap {MAX_LLM_RUNS} reached")
        if max_runs is not None and started >= max_runs:
            break
        started += 1
        wait_memory()
        trace = out / f"{name}_trace.jsonl"
        if trace.exists():
            trace = out / f"{name}_trace_{time.strftime('%H%M%S')}.jsonl"
        batch = AuditBatch(load_view(f.stem))
        t0 = time.time()
        o = Orchestrator(launcher, trace).run("auditor", batch.label, batch.task(), batch.executors())
        res = {"batch": f.stem, "repeat": repeat, "commit": git("rev-parse", "--short", "HEAD"),
               "claude_code": launcher.version, "model": launcher.cfg["model"], "wall_s": round(time.time() - t0, 1),
               "trace": trace.name, "outcome": o.__dict__, "decisions": batch.decisions,
               "undecided": batch.undecided(), "report": o.args.get("text") if o.status == "report" else None}
        dest = out / f"{name}_result.json"
        if o.status == "error" and "session limit" in o.args.get("reason", ""):
            (out / "usage_limit").mkdir(exist_ok=True)
            dest = out / "usage_limit" / f"{name}_{time.strftime('%H%M%S')}_result.json"
        dest.write_text(json.dumps(res, indent=1, default=str))
        n_flag = sum(d["decision"] == "flag" for d in batch.decisions.values())
        print(f"{name}: {o.status} steps {o.steps} flagged {n_flag} undecided {len(batch.undecided())} "
              f"tokens {o.input_tokens}/{o.output_tokens} call {o.call_ms / 1000:.1f} s", flush=True)
        if dest.parent.name == "usage_limit":
            sys.exit("usage limit: run set aside; stop")


# ------------------------------------------------------------------ scoring

def fleiss(table):
    """Fleiss kappa for items x categories counts (equal raters per item)."""
    t = np.asarray(table, float)
    if t.size == 0:
        return None
    n = t.sum(1)[0]
    p = t.sum(0) / t.sum()
    P = ((t * t).sum(1) - n) / (n * (n - 1))
    Pe = (p * p).sum()
    return None if Pe == 1 else round(float((P.mean() - Pe) / (1 - Pe)), 3)


def decisions_of(source, b, k):
    if source == "rule":
        d = json.loads((OUT / "rule" / f"{b}.json").read_text())["decisions"]
        return {i: x["decision"] for i, x in d.items()}
    f = OUT / "llm" / f"{b}_r{k}_result.json"
    if not f.exists():
        return None
    return {i: x["decision"] for i, x in json.loads(f.read_text())["decisions"].items()}


def eval_cmd():
    id_map = json.loads((OUT / "run_map.json").read_text())
    batches = {b["batch"]: b for b in json.loads((OUT / "batches.json").read_text())["batches"]}
    plants = {p["batch"]: p for p in json.loads((OUT / "plants.json").read_text())["plants"]}
    rows, per_run = [], defaultdict(list)
    for source, reps in (("rule", (0,)), ("llm", REPEATS)):
        for k in reps:
            for b, ids in id_map.items():
                d = decisions_of(source, b, k)
                if d is None:
                    continue
                kind = plants[b]["kind"] if b in plants else "none"
                for rid, stem in ids.items():
                    planted = stem.startswith("PLANT:")
                    dec = d.get(rid, "undecided")
                    rows.append({"auditor": source, "repeat": k, "batch": b, "row": batches[b]["row"],
                                 "batch_plant": kind, "run_id": rid, "planted": planted, "decision": dec})
                    if source == "llm":
                        per_run[(b, rid)].append(dec)
    (OUT / "scores.json").write_text(json.dumps(rows, indent=1))
    L = ["# Auditor check with planted errors: scores", "",
         "Catch: the planted run flagged. False alarm: an unplanted run flagged. LLM auditor: 3 repeats, blind; "
         f"rule auditor (|robust z| > {rule.Z_CUTOFF} or a failed check) once. Batches of 8 good accepted freeze v4 runs.", "",
         "## Catches per error kind", "", "| Error kind | Batches | Rule | LLM r0 | LLM r1 | LLM r2 |", "| :-- | --: | :-- | :-- | :-- | :-- |"]
    def cell(src, k, f):
        x = [r for r in rows if r["auditor"] == src and r["repeat"] == k and f(r)]
        return f"{sum(r['decision'] == 'flag' for r in x)} / {len(x)}" if x else "-"
    for kind in KINDS:
        nb = sum(p["kind"] == kind for p in plants.values())
        L.append(f"| {kind} | {nb} | {cell('rule', 0, lambda r: r['planted'] and r['batch_plant'] == kind)} | "
                 + " | ".join(cell("llm", k, lambda r: r["planted"] and r["batch_plant"] == kind) for k in REPEATS) + " |")
    L.append(f"| all | {len(plants)} | {cell('rule', 0, lambda r: r['planted'])} | "
             + " | ".join(cell("llm", k, lambda r: r["planted"]) for k in REPEATS) + " |")
    L += ["", "## False alarms (unplanted runs flagged / unplanted runs), by the batch's plant", "",
          "| Batch plant | Batches | Rule | LLM r0 | LLM r1 | LLM r2 |", "| :-- | --: | :-- | :-- | :-- | :-- |"]
    for kind in ("none",) + KINDS:
        nb = sum(1 for b in id_map if (plants[b]["kind"] if b in plants else "none") == kind)
        L.append(f"| {kind} | {nb} | {cell('rule', 0, lambda r: not r['planted'] and r['batch_plant'] == kind)} | "
                 + " | ".join(cell("llm", k, lambda r: not r["planted"] and r["batch_plant"] == kind) for k in REPEATS) + " |")
    L.append(f"| all | {len(id_map)} | {cell('rule', 0, lambda r: not r['planted'])} | "
             + " | ".join(cell("llm", k, lambda r: not r["planted"]) for k in REPEATS) + " |")
    full = {key: v for key, v in per_run.items() if len(v) == len(REPEATS)}
    cats = ("flag", "clear", "undecided")
    table = [[v.count(c) for c in cats] for v in full.values()]
    unan = sum(len(set(v)) == 1 for v in full.values())
    planted_full = {key: v for key, v in full.items() if id_map[key[0]][key[1]].startswith("PLANT:")}
    L += ["", "## Agreement across the 3 LLM repeats", "",
          f"- Runs decided in all 3 repeats: {len(full)}; unanimous {unan}" + (f" ({unan / len(full):.2f})" if full else ""),
          f"- Planted runs unanimous: {sum(len(set(v)) == 1 for v in planted_full.values())} of {len(planted_full)}",
          f"- Fleiss kappa (flag, clear, undecided): {fleiss(table) if table else '-'}"]
    llm = [json.loads(f.read_text()) for f in llm_results()]
    if llm:
        L += ["", "## LLM auditor runs", "",
              f"- Runs {len(llm)}; status " + ", ".join(f"{k} {v}" for k, v in Counter(x['outcome']['status'] for x in llm).items())
              + f"; steps {sum(x['outcome']['steps'] for x in llm)}; tokens in {sum(x['outcome']['input_tokens'] for x in llm)}, "
              f"out {sum(x['outcome']['output_tokens'] for x in llm)}; call time {sum(x['outcome']['call_ms'] for x in llm) / 1000:.0f} s",
              f"- Commits: {sorted({x['commit'] for x in llm})}; Claude Code {sorted({x['claude_code'] for x in llm})}; "
              f"model {sorted({x['model'] for x in llm})}"]
    L += ["", "## Planted runs", "", "| Batch | Row | Kind | Rule | LLM r0 | LLM r1 | LLM r2 |", "| :-- | :-- | :-- | :-- | :-- | :-- | :-- |"]
    for b, p in sorted(plants.items()):
        rid = next(i for i, s in id_map[b].items() if s.startswith("PLANT:"))
        get = lambda src, k: (decisions_of(src, b, k) or {}).get(rid, "-") if decisions_of(src, b, k) is not None else "-"
        L.append(f"| {b} | {batches[b]['row']} | {p['kind']} | {get('rule', 0)} | " + " | ".join(get("llm", k) for k in REPEATS) + " |")
    (OUT / "scores.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "views", "rule", "llm", "eval", "score"])   # score = eval
    ap.add_argument("--repeat", type=int, choices=REPEATS)
    ap.add_argument("--max-runs", type=int, default=None)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.cmd == "plan":
        if (OUT / "plants.json").exists():
            sys.exit("plants.json exists; the plan is written once")
        batches, plants, srcs = plan()
        (OUT / "batches.json").write_text(json.dumps({"seed": SEED, "batch_size": BATCH, "batches": batches}, indent=1))
        (OUT / "plants.json").write_text(json.dumps({"seed": SEED, "unit_factor": UNIT_FACTOR,
                                                     "closure_sources": srcs, "plants": plants}, indent=1))
        print(f"{len(batches)} batches, rows {dict(Counter(b['row'] for b in batches))}")
        print(f"plants {len(plants)}: {dict(Counter(p['kind'] for p in plants))}")
    elif a.cmd == "views":
        views_cmd()
    elif a.cmd == "rule":
        rule_cmd()
    elif a.cmd == "llm":
        if a.repeat is None:
            ap.error("--repeat is required")
        llm_cmd(a.repeat, a.max_runs)
    else:
        eval_cmd()


if __name__ == "__main__":
    main()
