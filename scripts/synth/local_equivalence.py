"""Local tracking against a reference cache: largest absolute difference per array.

  python scripts/synth/local_equivalence.py <local track or truth .npz> <reference .npz> [...pairs]

Prints one JSON line per pair: arrays compared, the largest absolute difference over the numeric
arrays, and arrays present in one file only. Settings and timing entries are skipped.
"""
import json
import sys

import numpy as np

SKIP = ("settings", "run_s", "threads", "timing")


def compare(a, b):
    with np.load(a, allow_pickle=True) as x, np.load(b, allow_pickle=True) as y:
        keys = sorted(set(x.files) & set(y.files))
        worst, per = 0.0, {}
        for k in keys:
            if any(s in k for s in SKIP):
                continue
            u, v = x[k], y[k]
            if u.dtype.kind not in "fiub" or v.dtype.kind not in "fiub":
                continue
            if u.shape != v.shape:
                per[k] = "shape differs"
                worst = float("inf")
                continue
            d = float(np.nanmax(np.abs(u.astype(float) - v.astype(float)))) if u.size else 0.0
            nan_same = bool(np.array_equal(np.isnan(u.astype(float)), np.isnan(v.astype(float))))
            per[k] = d if nan_same else f"{d} (NaN pattern differs)"
            worst = max(worst, d if nan_same else float("inf"))
        return {"local": str(a).replace("\\", "/").split("/")[-1], "arrays": len(per), "max_abs_diff": worst,
                "only_local": sorted(set(x.files) - set(y.files)), "only_reference": sorted(set(y.files) - set(x.files)),
                "per_array": per}


if __name__ == "__main__":
    args = sys.argv[1:]
    for a, b in zip(args[::2], args[1::2]):
        print(json.dumps(compare(a, b), default=str))
