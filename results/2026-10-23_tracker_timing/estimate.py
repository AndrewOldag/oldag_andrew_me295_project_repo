"""Cost estimate for tracking the real movies, from the one-window timing in this folder.

  python results/2026-10-23_tracker_timing/estimate.py

Reads timing.json and manifest/root_manifest.csv; prints estimate.md to stdout.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RATE = 0.012            # $ per core-hour, lowest tier (spec B3, Andrew, 2026-10-23)
WORKERS = 4             # lab server limit, decisions 2026-10-11
WINDOW_H = 2.0
MOVED = 2               # each window tracked again on a rigidly moved copy (rigid-invariance check)
SETTINGS = {"low": 1, "mid": 3, "high": 10}   # tracker settings per window: first run; + 2 remedies; every setting
SUBSET_ROOTS = 16
REPEATS = 3

t = json.loads((HERE / "timing.json").read_text())
runs = t["runs"]
per_frame = max((r["midline_cpu_s"] + r["track_wall_s"]) / r["frames"] for r in runs)   # slower run
peak_gb = max(r["track_peak_rss_kb"] for r in runs) / 1e6
out_mb = max(r["track_out_bytes"] + r["midline_out_bytes"] for r in runs) / 1e6

rows = list(csv.DictReader(open(REPO / "manifest" / "root_manifest.csv", newline="")))
inc = [r for r in rows if r["include"] == "yes"]
frames_inc = sum((float(r["usable_to_h"]) - float(r["usable_from_h"])) * 3600 / float(r["step_s"]) for r in inc)
hours_inc = sum(float(r["usable_to_h"]) - float(r["usable_from_h"]) for r in inc)
frames_per_root_24h = 24 * 3600 / 90.0
windows_inc = sum(-(-(float(r["usable_to_h"]) - float(r["usable_from_h"])) // WINDOW_H) for r in inc)


def line(name, frames, factor):
    out = []
    for k, s in SETTINGS.items():
        ch = frames * per_frame * MOVED * s * factor / 3600
        out.append(f"| {name} | {k} ({s}) | {ch:,.0f} | {ch / WORKERS:,.0f} | ${ch * RATE:,.2f} |")
    return out


print("| Set | Settings per window | Core-hours | Lab-server wall h (4 workers) | Cluster $ |")
print("| :-- | :-- | --: | --: | --: |")
for l in (line(f"(a) subset {SUBSET_ROOTS} roots x 24 h, tracker outputs cached across repeats",
               SUBSET_ROOTS * frames_per_root_24h, 1)
          + line(f"(a') subset, no cache, {REPEATS} repeats", SUBSET_ROOTS * frames_per_root_24h, REPEATS)
          + line(f"(b) all {len(inc)} include-yes roots once, usable hours ({hours_inc:,.0f} h)", frames_inc, 1)
          + line("(b') 118 roots x 24 h once", 118 * frames_per_root_24h, 1)):
    print(l)
print()
print(f"- Core-seconds per frame (midline + tracker, slower of {len(runs)} runs): {per_frame:.2f}")
print(f"- Include-yes roots {len(inc)}, usable hours {hours_inc:,.1f}, frames {frames_inc:,.0f}, "
      f"{WINDOW_H:.0f} h windows {windows_inc:,.0f}")
print(f"- Peak memory per job {peak_gb:.1f} GB; output per window {out_mb:.2f} MB; "
      f"output for (b) at 1 setting x 2 {out_mb * windows_inc * MOVED / 1e3:.1f} GB")
print(f"- Cluster rate ${RATE} per core-hour")

runs_c = t.get("cluster_runs", [])
if runs_c:
    print()
    print("Cluster runner (midline nets + QC + kinematics), one 2 h window per job:")
    print()
    print("| Job | Elapsed min | $ per 2 h window | $ per 24 h root (12 windows) | $ include-yes windows | $ 118 roots x 24 h |")
    print("| :-- | --: | --: | --: | --: | --: |")
    for c in runs_c:
        usd = c["units_per_h"] * c["elapsed_s"] / 3600 * RATE
        print(f"| {c['job']} ({c['hardware']}) | {c['elapsed_s'] / 60:.1f} | {usd:.3f} | {12 * usd:.2f} | "
              f"{windows_inc * usd:,.0f} | {118 * 12 * usd:,.0f} |")
    print()
    print("- Units: cpus + 10 per P100 or V100, per hour, at the rate above. No moved copy")
