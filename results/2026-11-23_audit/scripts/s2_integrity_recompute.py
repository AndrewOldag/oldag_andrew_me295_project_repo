"""Audit c033 s2: recompute integrity thresholds and relative k from the committed per-track rows."""
import json, math, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[2] / "2026-11-20_registration_fix"


def up2(x):
    if x <= 0:
        return 0.0
    e = math.floor(math.log10(x)) - 1
    return round(math.ceil(x / 10 ** e - 1e-9) * 10 ** e, max(0, -e))


t = json.loads((R / "thresholds.json").read_text())
rows = t["tracks"]
for c in ("integrity_gap_ratio", "integrity_lateral", "integrity_inversions"):
    v = np.array([r[c] for r in rows], float)
    p = np.percentile(v, 99.5)
    print(c, "n", len(v), "max", round(v.max(), 4), "p99.5", round(p, 4), "x1.5 up2sf", up2(1.5 * p))
print("stored", t["thresholds"])
k = json.loads((R / "relative_k.json").read_text())
for c in ("inversions", "gap_ratio", "lateral"):
    v = np.array([r[c] for r in k["pairs"]], float)
    p = np.percentile(v, 99.5)
    print(c, "n", len(v), "max", round(v.max(), 4), "p99.5", round(p, 4), "x1.5 up2sf", up2(1.5 * p))
print("stored", k["k"])
