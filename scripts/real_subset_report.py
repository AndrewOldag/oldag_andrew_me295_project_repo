"""Tables for the 16-root real subset (task c019, dispatcher inbox item 36): one row per window, counts per root and
per condition, from a scripts/real_slice.py run and the cached tracks.

  python scripts/real_subset_report.py --run results/2026-10-25_real_subset [--config private/real_runner_c019.yaml]

Per window: outcome, fault named, remedies kept, final checks (closure gates at the real threshold; rigid invariance
and plane sections reported), tracked length reached, base arc length, basal world speed and the frame-0 flag
(inbox item 32, `base_info` of scripts/real_calib.py on the initial run), and the field summary of the final run
(centre REGR peak and growth-zone length, audit/view.py). Writes windows.csv and tables.md into the run folder.
Reads cached tracks only (staging/tracks_real/); no host step.
"""
import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from audit.view import field_summaries  # noqa: E402
from measure.real_runner import RealRunner, RealWindow  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

spec = importlib.util.spec_from_file_location("real_calib", ROOT / "scripts" / "real_calib.py")
RC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RC)

GROUP = {"control": "control", "control then control": "control", "mannitol": "drought",
         "mannitol then mannitol": "drought", "mannitol then control": "recovery"}


def check(checks, name):
    c = next(c for c in checks if c["check"] == name)
    v = c["value"]
    return (None if v is None or v != v else round(v, 2)), c["passed"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--config", default=str(ROOT / "private" / "real_runner_c019.yaml"))
    a = ap.parse_args()
    run = Path(a.run)
    s = json.loads((run / "summary.json").read_text())
    runner = RealRunner(a.config)
    rows = []
    for tid, t in sorted(s["tasks"].items(), key=lambda kv: (kv[1].get("root_id", kv[0]), kv[1]["window_h"][0])):
        root = t.get("root_id") or tid.split("__")[0]
        w = RealWindow(root, *t["window_h"])
        init = from_tracker_npz(runner.cache_path(w, runner.initial_settings(w), "ref"), root_id=w.id())
        fin_set = TrackSettings(**t["final_settings"])
        fin = from_tracker_npz(runner.cache_path(w, fin_set, "ref"), root_id=w.id())
        b = RC.base_info(init)
        f = field_summaries(fin, width_free=fin_set.width_free)
        o = t["outcome"]
        clo, clo_pass = check(t["final_checks"], "closure")
        rows.append({
            "window": w.id(), "root": root, "condition": t["condition"], "group": GROUP[t["condition"]],
            "outcome": o["status"], "fault": (o.get("args") or {}).get("fault", ""),
            "remedies_kept": "; ".join(x for x in t["remedies"] if not x.startswith("rolled back")),
            "roll_backs": t["roll_backs"],
            "closure_initial_px_h": check(t["initial_checks"], "closure")[0],
            "closure_final_px_h": clo, "closure_pass": clo_pass,
            "rigid_invariance_pct_h": check(t["final_checks"], "rigid_invariance")[0],
            "plane_sections_pct_h": check(t["final_checks"], "plane_sections")[0],
            "tracked_length_px": b["tracked_length_reached_px"], "base_s_px": b["base_s_px"],
            "basal_speed_px_h": b["basal_speed_px_per_h"][-1][1] if b["basal_speed_px_per_h"] else None,
            "frame0_midline_px": b["frame0_midline_px"], "base_flag": b["flag"] or "",
            "peak_regr_pct_h": f.get("centre_peak_regr_pct_per_h"),
            "growth_zone_um": f.get("growth_zone_length_um"),
        })
    with (run / "windows.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)

    accepted = ("accept", "accepted", "accept_repaired")
    md = ["| Window | Group | Outcome | Fault | Closure px/h (initial, final) | Rigid %/h | Plane %/h | "
          "Tracked px | Base s px | Base flag | Peak REGR %/h | Growth zone um |",
          "| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |"]
    for r in rows:
        md.append(f"| {r['window']} | {r['group']} | {r['outcome']} | {r['fault']} | {r['closure_initial_px_h']}, "
                  f"{r['closure_final_px_h']} | {r['rigid_invariance_pct_h']} | {r['plane_sections_pct_h']} | "
                  f"{r['tracked_length_px']} | {r['base_s_px']} | {'yes' if r['base_flag'] else ''} | "
                  f"{r['peak_regr_pct_h']} | {r['growth_zone_um']} |")
    per_root, per_group = defaultdict(Counter), defaultdict(Counter)
    for r in rows:
        k = "accepted" if r["outcome"] in accepted else r["outcome"]
        per_root[(r["group"], r["root"])][k] += 1
        per_group[r["group"]][k] += 1
    keys = sorted({k for c in per_group.values() for k in c})
    md += ["", "| Group | Root | " + " | ".join(keys) + " |", "| :-- | :-- | " + " | ".join(":--" for _ in keys) + " |"]
    for (g, root), c in sorted(per_root.items()):
        md.append(f"| {g} | {root} | " + " | ".join(str(c[k]) for k in keys) + " |")
    md += ["", "| Group | Windows | " + " | ".join(keys) + " |", "| :-- | :-- | " + " | ".join(":--" for _ in keys) + " |"]
    for g in ("control", "drought", "recovery"):
        c = per_group[g]
        md.append(f"| {g} | {sum(c.values())} | " + " | ".join(str(c[k]) for k in keys) + " |")
    (run / "tables.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
