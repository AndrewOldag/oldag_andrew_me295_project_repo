"""Compare two tracker outputs of the same window from two hosts (real-calib inbox item 11 (2)).

  python scripts/track_equivalence.py A.npz B.npz [--moved-a M.npz --moved-b N.npz]

Prints the largest absolute difference over every numeric array the two files share (px for coordinates), the arrays
present in only one file, and the checker values (real profile, closure at the real threshold) from each. Equal
means: every shared array within 1e-6 and every checker value equal (the 2026-10-23 workstation test).
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from full_batch import check_window, thresholds  # noqa: E402
from measure.real_runner import from_tracker_npz  # noqa: E402
from measure.runner import Measurement  # noqa: E402

TOL = 1e-6


def arrays(path):
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files if z[k].dtype.kind in "fiub"}


def compare(a, b):
    A, B = arrays(a), arrays(b)
    diff = {}
    for k in sorted(set(A) & set(B)):
        if A[k].shape != B[k].shape:
            diff[k] = f"shape {A[k].shape} vs {B[k].shape}"
            continue
        x, y = A[k].astype(float), B[k].astype(float)
        if not np.array_equal(np.isnan(x), np.isnan(y)):
            diff[k] = "NaN pattern differs"
            continue
        m = np.isfinite(x)
        diff[k] = float(np.max(np.abs(x[m] - y[m]))) if m.any() else 0.0
    return diff, sorted(set(A) ^ set(B))


def checks(path, moved=None):
    rec = from_tracker_npz(path, root_id="w")
    mv = from_tracker_npz(moved, root_id="w_moved") if moved else None
    outcome, vals, passed, _ = check_window(Measurement(rec, mv, None, {}), thresholds())
    return {"outcome": outcome, "values": vals}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--moved-a")
    p.add_argument("--moved-b")
    a = p.parse_args()
    diff, only = compare(a.a, a.b)
    num = [v for v in diff.values() if isinstance(v, float)]
    ca, cb = checks(a.a, a.moved_a), checks(a.b, a.moved_b)
    out = {"max_abs_diff": max(num) if num else None, "per_array": diff, "only_in_one": only,
           "checks_a": ca, "checks_b": cb, "checks_equal": ca == cb}
    out["equal"] = (len(num) == len(diff) and (out["max_abs_diff"] or 0.0) <= TOL and out["checks_equal"])
    print(json.dumps(out, indent=1))
    sys.exit(0 if out["equal"] else 1)


if __name__ == "__main__":
    main()
