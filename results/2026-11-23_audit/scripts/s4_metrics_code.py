"""S4 audit: run the repo's measure/metrics.py (over_repeats, agreement) on each committed scores.json, in memory,
and compare with the committed metrics.json. Writes nothing."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from measure import metrics as M  # noqa: E402


def same(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) | set(b):
            out += same(a.get(k), b.get(k), f"{path}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path]
        return [x for i, (u, v) in enumerate(zip(a, b)) for x in same(u, v, f"{path}[{i}]")]
    if isinstance(a, float) and isinstance(b, (int, float)):
        return [] if math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) else [path]
    return [] if a == b else [path]


for d in ("results/2026-10-25_freeze_v4", "results/2026-11-18_heldout_compound",
          "results/2026-11-18_heldout_compound/supplement"):
    sc = json.loads((ROOT / d / "scores.json").read_text())
    mj = json.loads((ROOT / d / "metrics.json").read_text())
    for m in mj:
        rs = [r for r in sc if r["method"] == m]
        if not rs:
            print(d, m, "reference policy, not in scores.json: not compared")
            continue
        got = M.over_repeats(rs)
        if len({r["repeat"] for r in rs}) > 1:
            got["agreement"] = M.agreement(rs)
        diff = same(got, mj[m])
        print(d, m, "runs", len(rs), "differences", len(diff), diff[:5])
