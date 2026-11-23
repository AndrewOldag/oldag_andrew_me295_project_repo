"""S4 audit: recompute the tables and numbers of results/2026-11-20_registration_fix from its JSON files. Read-only."""
import json
import math
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[3] / "results" / "2026-11-20_registration_fix"
js = lambda n: json.loads((R / n).read_text())  # noqa: E731

print("=== R1 diagnosis (register_diag)")
d = js("register_diag_0711_c5__w6-8.json")
c, di = d["chained"], d["direct"]
pr = np.array(c["pair_rotation_deg"])
print("pairs", len(pr), "sum %.2f" % pr.sum(), "mean %.3f" % pr.mean(), "mean abs %.2f" % np.abs(pr).mean(),
      "largest %.2f" % np.abs(pr).max(), "stored sum", c["sum_pair_rotation_deg"], "final", c["final_rotation_deg"])
e = np.array(c["pair_ecc"])
bm = np.array(c["pair_band_motion_px"])
print("ECC min %.3f median %.3f; band motion median %.2f max %.2f; final band motion %s; v1 report ecc_min %.3f shift %s"
      % (e.min(), np.median(e), np.median(bm), bm.max(), c["final_band_motion_px"],
         c["register_frames_report"]["ecc_min"], c["register_frames_report"]["final_shift_px"]))
path = c["path_rotation_deg"]
print("path at frames 10, 20, 50, 70, 79:", [round(path[i], 2) for i in (10, 20, 50, 70, 79)])
pf = di["per_frame"]
ecc = pf["ecc"]
rot = np.array(pf["rotation_deg"])
nfail = sum(x is None for x in ecc)
print("direct: failed fits (ecc null)", nfail, "of", len(ecc), "first null at", next((i for i, x in enumerate(ecc) if x is None), None))
ok = [i for i, x in enumerate(ecc) if x is not None]
print("direct: rotation range over frames 1-20 %.2f to %.2f" % (rot[1:21].min(), rot[1:21].max()),
      "ECC range on fitted frames %.2f-%.2f" % (min(ecc[i] for i in ok), max(ecc[i] for i in ok)),
      "final rot", di["final_rotation_deg"], "band", di["final_band_motion_px"], "bound", di["bound"], "plausible", di["plausible"])
print("rotation frames 20..79 constant:", len(set(np.round(rot[21:], 4))) == 1, "value", rot[-1])

print("\n=== flagged window integrity and gate")
fi = js("flagged_window_integrity.json")
for k, t in fi["tracks"].items():
    print(k, t["tag"], {x["check"]: (round(x["value"], 2) if isinstance(x["value"], float) and not math.isnan(x["value"]) else x["value"])
                       for x in t["checks"]})
g = js("flagged_window_gate.json")
for k, t in g["tracks"].items():
    print(k, t["tag"], t["passed"], {x["check"]: (round(x["value"], 2) if isinstance(x["value"], (int, float)) else x["value"])
                                     for x in t["checks"]})
b = g["base_absolute"]
for k, t in g["tracks"].items():
    a = t["absolute"]
    print(" recomputed ratios", k, "inv (n+1)", round((a["integrity_inversions"] + 1) / (b["integrity_inversions"] + 1), 2),
          "gap", round(a["integrity_gap_ratio"] / b["integrity_gap_ratio"], 2), "lat", round(a["integrity_lateral"] / b["integrity_lateral"], 1))

print("\n=== batch-1 base integrity")
bb = js("batch1_base_integrity.json")
tr = bb["tracks"]
th = bb["summary"]["thresholds"]
for key, lim in (("integrity_inversions", th["inversions"]), ("integrity_gap_ratio", th["gap_ratio"]),
                 ("integrity_lateral", th["lateral_px"])):
    v = np.array([t[key] for t in tr], float)
    print(key, "n", len(v), "median %.3f p95 %.3f max %.3f" % (np.median(v), np.percentile(v, 95), v.max()),
          "pass", int((v <= lim).sum()))
print("pass all", sum(t["passed"] for t in tr), "inversions > 0", sum(t["integrity_inversions"] > 0 for t in tr),
      "inversions >= 100", sum(t["integrity_inversions"] >= 100 for t in tr), "summary", bb["summary"])
ts = js("thresholds.json")
for key in ("integrity_inversions", "integrity_gap_ratio", "integrity_lateral"):
    v = np.array([t[key] for t in ts["tracks"]], float)
    print("synthetic", key, "n", len(v), "median %.3f max %.3f" % (np.median(v), v.max()))

print("\n=== relative k pairs (synthetic ratios)")
rk = js("relative_k.json")
for key in ("inversions", "gap_ratio", "lateral"):
    v = [p[key] for p in rk["pairs"]]
    print(key, "min %.3f max %.3f" % (min(v), max(v)))
reg = [p["lateral"] for p in rk["pairs"] if "reg2p" in p["repaired"]]
oth = [p["lateral"] for p in rk["pairs"] if "reg2p" not in p["repaired"]]
print("lateral register rods", len(reg), "%.2f-%.2f" % (min(reg), max(reg)), "others", len(oth), [round(x, 3) for x in oth],
      "others same track as base:", [p["repaired"] == p["base"] for p in rk["pairs"] if "reg2p" not in p["repaired"]])

print("\n=== relative_check_v1")
rc = js("relative_check_v1.json")
k = rc["k"]
by = {}
for p in rc["pairs"]:
    s = by.setdefault(p["label"].split(",")[0], {"pairs": 0, "pass": 0, "inv": 0, "gap": 0, "lat": 0})
    s["pairs"] += 1
    s["pass"] += p["passed"]
    s["inv"] += p["integrity_rel_inversions"] > k["inversions"]
    s["gap"] += p["integrity_rel_gap_ratio"] > k["gap_ratio"]
    s["lat"] += p["integrity_rel_lateral"] > k["lateral"]
    recomputed = (p["integrity_rel_inversions"] <= k["inversions"] and p["integrity_rel_gap_ratio"] <= k["gap_ratio"]
                  and p["integrity_rel_lateral"] <= k["lateral"])
    if recomputed != p["passed"]:
        print("  passed flag differs from the ratios:", p["window"], p["passed"])
print(by)
for key in ("integrity_rel_inversions", "integrity_rel_gap_ratio", "integrity_rel_lateral"):
    print("median over", len(rc["pairs"]), key, "%.2f" % np.median([p[key] for p in rc["pairs"]]))

print("\n=== R5 regression")
for r in js("regression.json")["rods"]:
    v1, v2 = r["v1"], r["v2"]
    print(r["rod"][15:], "v1", v1["outcome"], "v2", v2["outcome"], "v2 closure %.2f" % v2["closure"], "v1 closure %.2f" % v1["closure"],
          "v2 lower", v2["closure"] < v1["closure"], "gates", v1["gate"], v2["gate"], "good", v1["good"], v2["good"],
          "v2 rot", v2["final_rotation_deg"], "band", v2["final_band_motion_px"], "plausible", v2["plausible"])
