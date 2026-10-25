"""v3 synthetic validation of the midline spline fit (proposal 2026-10-23, option 1; inbox item 17).

  python scripts/synth/validate_midline_fit.py --cache DIR [--out results/<dir>]

For every cached v3 tracker output with its rigidly moved twin (DIR/<rod>__<tag>.npz and
DIR/<rod>_moved__<tag>.npz): the checker at the approved thresholds as tracked, then again with every
frame's midline replaced by its spline fit (measure/midline_fit.py) in both records. No re-tracking.
Pass: every checker value unchanged within 1e-3 in its unit (NaN equals NaN). Prints and writes a table.
"""
import argparse
import json
import math
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from checker import load_thresholds, run_checks  # noqa: E402
from measure.midline_fit import fit_midlines  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

TOL = 1e-3


def fitted(rec):
    return replace(rec, midline=fit_midlines(rec.midline), _fields=None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    th = load_thresholds()
    rows = []
    for f in sorted(Path(a.cache).glob("v3_*__*.npz")):
        if "_moved__" in f.name:
            continue
        rid, tag = f.stem.split("__", 1)
        mf = f.with_name(f"{rid}_moved__{tag}.npz")
        if not mf.exists():
            continue
        rec, mov = from_tracker_npz(f), from_tracker_npz(mf)
        before = {c.check: c for c in run_checks(rec, mov, th)}
        after = {c.check: c for c in run_checks(fitted(rec), fitted(mov), th)}
        row = {"run": f.stem}
        ok = True
        for k in ("rigid_invariance", "closure", "plane_sections"):
            b, x = before[k].value, after[k].value
            d = 0.0 if (math.isnan(b) and math.isnan(x)) else abs(x - b)
            row[k] = {"before": round(b, 4), "after": round(x, 4), "diff": round(d, 4),
                      "pass_before": before[k].passed, "pass_after": after[k].passed}
            ok &= d <= TOL
        row["within_tol"] = bool(ok)
        rows.append(row)
    n = len(rows)
    n_ok = sum(r["within_tol"] for r in rows)
    flips = sum(r[k]["pass_before"] != r[k]["pass_after"] for r in rows for k in ("rigid_invariance", "closure", "plane_sections"))
    worst = {k: max((r[k]["diff"] for r in rows), default=None) for k in ("rigid_invariance", "closure", "plane_sections")}
    summary = {"runs": n, "within_1e-3": n_ok, "result": "pass" if n and n_ok == n else "fail",
               "max_abs_diff": worst, "pass_fail_flips": flips}
    print(json.dumps(summary))
    if a.out:
        out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
        (out / "validation.json").write_text(json.dumps({"summary": summary, "runs": rows}, indent=1))


if __name__ == "__main__":
    main()
