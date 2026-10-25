"""Validation of a closure change on freeze v3 (spec 2026-10-24b A): every synthetic checker value within 1e-3 and
every pass or fail the same.

  python scripts/closure_v3_validate.py --tracks staging/tracks_freeze_v3 [--out FILE.json]

For each scored rod: the unremedied run's three checks recomputed with the current checker from the cached tracks
(record and moved twin, `<rod>__st<stride>.npz`, stride from the summary), against `initial_checks` in the freeze v3 script summaries
(results/2026-10-23_freeze_v3/runs/). Prints the largest change and the number of changed passes; the same
for closure definition (3) (base world displacement only), which was not adopted. Reads only.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker.checks import _common_base, load_thresholds, run_checks  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

RUNS = ROOT / "results" / "2026-10-23_freeze_v3" / "runs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    tracks, th = Path(a.tracks), load_thresholds()
    rows = []
    for f in sorted(RUNS.glob("script_*_summary.json")):
        s = json.loads(f.read_text())
        rid = s["rod"]["id"]
        track = tracks / f"{rid}__st{s['final_settings']['stride']}.npz"     # the script applies no remedy
        if not track.exists():
            rows.append({"rod": rid, "error": f"missing {track.name}"})
            continue
        moved = tracks / track.name.replace("__", "_moved__", 1)
        rec = from_tracker_npz(track)
        new = {c.check: c for c in run_checks(rec, from_tracker_npz(moved), th)}
        for old in s["initial_checks"]:
            n = new[old["check"]]
            row = {"rod": rid, "check": old["check"], "old": old["value"], "new": n.value,
                   "diff": abs(n.value - old["value"]), "pass_same": n.passed == old["passed"]}
            if old["check"] == "closure":                   # definition (3), not adopted: base displacement only
                b, t = _common_base(rec.centre), rec.frame_times_s
                d3 = float(np.linalg.norm(rec.centre[-1, b] - rec.centre[0, b]) / ((t[-1] - t[0]) / 3600.0))
                row.update(def3=d3, def3_diff=abs(d3 - old["value"]), def3_pass_same=(d3 <= th["closure"]) == old["passed"])
            rows.append(row)
    ok = [r for r in rows if "error" not in r]
    c3 = [r for r in ok if "def3" in r]
    res = {"rods": len({r["rod"] for r in rows}), "values": len(ok), "errors": [r for r in rows if "error" in r],
           "max_diff": max(r["diff"] for r in ok),
           "max_diff_closure": max(r["diff"] for r in ok if r["check"] == "closure"),
           "pass_changed": sum(not r["pass_same"] for r in ok),
           "def3_changed_over_1e-3": sum(r["def3_diff"] > 1e-3 for r in c3), "def3_max_diff": max(r["def3_diff"] for r in c3),
           "def3_pass_changed": sum(not r["def3_pass_same"] for r in c3)}
    print(json.dumps(res, indent=1))
    if a.out:
        Path(a.out).write_text(json.dumps({**res, "rows": rows}, indent=1))


if __name__ == "__main__":
    main()
