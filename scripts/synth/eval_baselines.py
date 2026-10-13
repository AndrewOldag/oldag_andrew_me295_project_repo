"""Score task summaries (baselines or the diagnostician) against the freeze labels; write the table.

  python scripts/synth/eval_baselines.py --runs results/<date>_baselines [--agent-runs DIR ...] --out DIR

Reads <name>_summary.json and <name>_trace.jsonl as written by
scripts/synth/baselines.py and scripts/demo_slice.py. Scoring is
measure/score.py as it stands: approved tolerance (config/scoring_tolerance.yaml),
measurement_good, outcome_category, diagnosis_correct. Labels and correct
outcomes: docs/proposals/2026-10-11_freeze-v1.md, section 1. Truth from
staging/tracks_baselines/.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from measure.runner import Rod  # noqa: E402
from measure.score import diagnosis_correct, load_tolerance, measurement_good, outcome_category, rod_tolerance  # noqa: E402

TRUTH = ROOT / "staging" / "tracks_baselines"
PIXEL_UM = 2.105
# freeze v1, section 1: fault -> (size, label, correct outcome)
FREEZE = {"displacement_exceeds_patch": ("2x6", "repairable", "accept after the remedy"),
          "width_change": ("1/400", "repairable", "accept with the width-free ratio"),
          "rigid_drift": ("0.5", "repairable", "accept after the remedy"),
          "low_texture": ("0.03", "not repairable", "decline"),
          "midline_jitter": ("3", "not repairable", "decline")}
CORRECT = {"repairable": "good_report", "not repairable": "correct_decline"}


def named_fault(trace):
    """Fault named in the last apply_remedy or decline of the trace."""
    name = None
    for line in trace.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        act = d.get("action") or {}
        if act.get("name") in ("apply_remedy", "decline") and d.get("status") in ("executed", "terminal"):
            name = act["args"].get("fault")
    return name


def score(summary_path, method, cfg):
    s = json.loads(summary_path.read_text())
    r = s["rod"]
    rod = Rod(r["case"], r["fault"], r["seed"], size=r["size"])
    with np.load(TRUTH / f"{rod.id()}_truth.npz") as z:
        tol = rod_tolerance({k: z[k] for k in z.files}, PIXEL_UM, cfg)
    label = FREEZE[rod.fault][1]
    o = s["outcome"]
    width_free = bool(s["final_settings"].get("width_free"))
    good = measurement_good(s["error_after"], tol, width_free)
    cat = outcome_category(o["status"], label, good)
    trace = summary_path.with_name(summary_path.name.replace("_summary.json", "_trace.jsonl"))
    fault = named_fault(trace) if trace.exists() else None
    return {"method": method, "fault": rod.fault, "seed": rod.seed, "label": label, "status": o["status"],
            "steps": o["steps"], "remedies": [x for x in s["remedies"]], "roll_backs": s["roll_backs"],
            "good": good, "category": cat, "correct": cat == CORRECT[label], "named_fault": fault,
            "diagnosis_correct": diagnosis_correct(fault, rod.fault),
            "regr_rms": s["error_after"].get("regr_rms_pct_per_h"),
            "flank_rms": s["error_after"].get("flank_difference_rms_pct_per_h"),
            "regr_tol": round(tol["regr_rms_pct_per_h"], 3), "calls": o.get("calls", 0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True, help="folder of baseline summaries")
    ap.add_argument("--agent-runs", nargs="*", default=[], help="folders of diagnostician summaries (demo_slice)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = load_tolerance()
    rows = []
    for f in sorted(Path(a.runs).glob("*_summary.json")):
        rows.append(score(f, json.loads(f.read_text())["baseline"], cfg))
    for d in a.agent_runs:
        for f in sorted(Path(d).glob("*_summary.json")):
            if "outcome" in json.loads(f.read_text()):
                rows.append(score(f, "diagnostician", cfg))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "scores.json").write_text(json.dumps(rows, indent=1))

    methods = [m for m in ("script", "remedy_tree", "diagnostician") if any(r["method"] == m for r in rows)]
    lines = [f"# Baselines on the development faults, scored against freeze v1",
             "",
             f"Scoring: `measure/score.py` unchanged; tolerance from `config/scoring_tolerance.yaml` "
             f"(centre {cfg['regr_rms_fraction_of_true_peak']} x true peak, flank {cfg['flank_difference_rms_pct_per_h']} %/h). "
             "Correct: good_report on a repairable rod, correct_decline on a not-repairable rod.",
             "",
             "## Outcome per fault and method (seeds 0, 1, 2)",
             "| Fault | Size | Label | Correct outcome | " + " | ".join(methods) + " |",
             "| :-- | :-- | :-- | :-- | " + " | ".join(":--" for _ in methods) + " |"]
    for fault, (size, label, correct) in FREEZE.items():
        cells = []
        for m in methods:
            rs = sorted((r for r in rows if r["method"] == m and r["fault"] == fault), key=lambda r: r["seed"])
            cells.append("; ".join(f"s{r['seed']} {r['category']}" for r in rs) or "-")
        lines.append(f"| {fault} | {size} | {label} | {correct} | " + " | ".join(cells) + " |")
    lines += ["", "## Totals",
              "| Method | Tasks | Correct | good_report | false_accept | correct_decline | unnecessary_decline | "
              "not_reported | Fault named correctly | Steps | Remedies applied | Roll backs |",
              "| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |"]
    for m in methods:
        rs = [r for r in rows if r["method"] == m]
        c = {k: sum(r["category"] == k for r in rs) for k in ("good_report", "false_accept", "correct_decline",
                                                                "unnecessary_decline", "not_reported")}
        lines.append(f"| {m} | {len(rs)} | {sum(r['correct'] for r in rs)} | " + " | ".join(str(v) for v in c.values())
                     + f" | {sum(r['diagnosis_correct'] for r in rs)} | {sum(r['steps'] for r in rs)} | "
                     f"{sum(len(r['remedies']) - r['roll_backs'] for r in rs)} | {sum(r['roll_backs'] for r in rs)} |")
    lines += ["", "## Per task",
              "| Method | Fault | Seed | Status | Category | Steps | Named fault | Remedies | Roll backs | "
              "Centre RMS (%/h) | Centre tol | Flank RMS (%/h) |",
              "| :-- | :-- | --: | :-- | :-- | --: | :-- | :-- | --: | --: | --: | --: |"]
    for r in sorted(rows, key=lambda r: (methods.index(r["method"]), list(FREEZE).index(r["fault"]), r["seed"])):
        lines.append(f"| {r['method']} | {r['fault']} | {r['seed']} | {r['status']} | {r['category']} | {r['steps']} | "
                     f"{r['named_fault'] or '-'} | {'; '.join(r['remedies']) or 'none'} | {r['roll_backs']} | "
                     f"{r['regr_rms']} | {r['regr_tol']} | {r['flank_rms']} |")
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:4 + 3 + len(FREEZE) + 4 + len(methods)]))


if __name__ == "__main__":
    main()
