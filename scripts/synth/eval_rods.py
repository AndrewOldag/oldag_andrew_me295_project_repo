"""Check values and truth errors for field-level and tracked image-level rods.

  python scripts/synth/eval_rods.py --tracks DIR --out results/<date>_<name>

DIR holds <id>.npz from qb_track.py, <id>_truth.npz, and <id>_moved.npz for
the rigid-invariance partner. Writes field_level.md, image_level.csv,
image_level.md, per_seed.md, rotation.md (if rigid_rotation runs at several
rates are present) and clean_profiles.png (if clean growth_zone and bending
runs are present). Pass or fail uses the approved thresholds in
config/checker_thresholds.yaml; clean cases are compared with
measure.render.IMAGE_EXPECTED.
"""
import argparse
import csv
import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from checker import run_checks, load_thresholds                    # noqa: E402
from measure.render import IMAGE_EXPECTED                            # noqa: E402
from checker.checks import MIN_COVERAGE                              # noqa: E402
from measure.record import from_tracker_npz, rigid_moved, PER_S_TO_PCT_PER_H as P  # noqa: E402
from measure.rod import field_cases, make_record                    # noqa: E402

warnings.simplefilter("ignore", RuntimeWarning)
CHECKS = ("rigid_invariance", "closure", "plane_sections")


def window_mean(a):
    m = np.nanmean(a, axis=0)
    m[np.mean(np.isfinite(a), axis=0) < MIN_COVERAGE] = np.nan
    return m


def truth_error(rec, truth):
    """RMS and max error of the window-mean centre strain rate, %/h, over the covered grid."""
    s = rec.fields["s_grid"]
    t = np.interp(s, truth["s_grid"], np.nanmean(truth["regr_mid"], axis=0), right=np.nan)
    e = (window_mean(rec.fields["regr_mid"]) - t) * P
    return float(np.sqrt(np.nanmean(e ** 2))), float(np.nanmax(np.abs(e))), float(np.nanmax(t) * P)


def field_table():
    lines = ["| Case | Check | Value | Unit | Expected | Where (s, px) |", "| :-- | :-- | --: | :-- | :-- | --: |"]
    for spec in field_cases():
        rec = make_record(spec)
        moved = rigid_moved(rec, np.deg2rad(0.1) / 90.0, (0.5 / 90.0, 0.3 / 90.0))
        for r in run_checks(rec, moved):
            exp = "pass" if spec.expected[r.check] else "fail"
            lines.append(f"| {spec.name} | {r.check} | {r.value:.4f} | {r.unit} | {exp} | {r.where_s_px:.0f} |")
    return lines


def group_of(case, fault, variant):
    if fault != "None":
        return f"{fault}{variant}"
    if case == "rigid_rotation":
        return f"rigid_rotation{variant} (closure expected to fail)"
    return f"{case}{variant} clean"


def image_rows(tracks, thresholds):
    rows = []
    for path in sorted(tracks.glob("*.npz")):
        rid = path.stem
        if rid.endswith("_truth") or rid.endswith("_moved"):
            continue
        rec = from_tracker_npz(path)
        moved_path = tracks / f"{rid}_moved.npz"
        moved = from_tracker_npz(moved_path) if moved_path.exists() else None
        truth = np.load(tracks / f"{rid}_truth.npz")
        res = {r.check: r for r in run_checks(rec, moved, thresholds)}
        rms, mx, peak = truth_error(rec, truth)
        case, fault = str(truth["case"]), str(truth["fault"])
        variant = str(truth["variant"]) if "variant" in truth.files else ""
        expected = IMAGE_EXPECTED.get(case) if fault == "None" else None
        rows.append({"id": rid, "case": case, "fault": fault, "variant": variant,
                     "group": group_of(case, fault, variant),
                     "regr_rms_err": rms, "regr_max_err": mx, "regr_peak": peak,
                     **{c: res[c].value for c in CHECKS},
                     **{f"{c}_pass": res[c].passed for c in CHECKS},
                     **{f"{c}_where_s": res[c].where_s_px for c in CHECKS},
                     "as_expected": (None if expected is None else
                                     all(res[c].passed is expected[c] for c in CHECKS)),
                     "run_s": rec.settings.get("run_s")})
    return rows


def summary(rows):
    out = ["| Group | n | REGR rms err (%/h) | REGR max err (%/h) | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | Failed checks (runs) | As expected |",
           "| :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |"]
    groups = {}
    for r in rows:
        groups.setdefault(r["group"], []).append(r)
    fmt = lambda v: f"{np.median(v):.2f} [{np.min(v):.2f}, {np.max(v):.2f}]"
    for key, rs in groups.items():
        cols = [fmt([r[k] for r in rs]) for k in ("regr_rms_err", "regr_max_err") + CHECKS]
        failed = ", ".join(f"{c} {sum(r[f'{c}_pass'] is False for r in rs)}" for c in CHECKS
                           if any(r[f"{c}_pass"] is False for r in rs)) or "none"
        exp = rs[0]["as_expected"]
        exp = "" if exp is None else f"{sum(bool(r['as_expected']) for r in rs)} of {len(rs)}"
        out.append(f"| {key} | {len(rs)} | " + " | ".join(cols) + f" | {failed} | {exp} |")
    out.append("")
    out.append("Cells: median [min, max] over seeds. Pass or fail at the approved thresholds. "
               "As expected: clean cases against `IMAGE_EXPECTED`.")
    return out


def per_seed(rows, thresholds):
    out = [f"Approved thresholds: rigid_invariance {thresholds['rigid_invariance']} %/h, "
           f"closure {thresholds['closure']} px/h, plane_sections {thresholds['plane_sections']} %/h.", "",
           "| Run | rigid_invariance (%/h) | at s (px) | closure (px/h) | basal point s (px) | plane_sections (%/h) | at s (px) |",
           "| :-- | --: | --: | --: | --: | --: | --: |"]
    mark = lambda r, c: f"{r[c]:.2f}" + ("" if r[f"{c}_pass"] is not False else " fail")
    for r in rows:
        out.append(f"| {r['id']} | {mark(r, 'rigid_invariance')} | {r['rigid_invariance_where_s']:.0f} | "
                   f"{mark(r, 'closure')} | {r['closure_where_s']:.0f} | "
                   f"{mark(r, 'plane_sections')} | {r['plane_sections_where_s']:.0f} |")
    return out


def rotation_table(rows, threshold, chain_end=480.0):
    """Closure against rotation rate. Predicted: rate x (pivot to basal tracked point)."""
    rot = [r for r in rows if r["case"] == "rigid_rotation" and r["fault"] == "None"]
    rates = sorted({float(r["variant"][2:]) if r["variant"] else 0.1 for r in rot}, reverse=True)
    if len(rates) < 2:
        return None
    out = ["| Rate (deg/frame) | Rate (deg/h) | n | Closure (px/h), per seed | Pivot to basal point (px) | Predicted (px/h) | Flagged at " + f"{threshold} px/h |",
           "| --: | --: | --: | :-- | --: | --: | :-- |"]
    for rate in rates:
        rs = [r for r in rot if (float(r["variant"][2:]) if r["variant"] else 0.1) == rate]
        dist = chain_end - np.mean([r["closure_where_s"] for r in rs])
        pred = np.deg2rad(rate) * 40.0 * dist
        vals = ", ".join(f"{r['closure']:.2f}" for r in rs)
        flagged = sum(r["closure_pass"] is False for r in rs)
        out.append(f"| {rate:g} | {rate * 40:g} | {len(rs)} | {vals} | {dist:.0f} | {pred:.2f} | {flagged} of {len(rs)} |")
    return out


def plot_clean(tracks, out):
    if not list(tracks.glob("growth_zone_clean_s*.npz")) or not list(tracks.glob("bending_clean_s*.npz")):
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=False)
    for ax, case in zip(axes, ("growth_zone", "bending")):
        for path in sorted(tracks.glob(f"{case}_clean_s*.npz")):
            if path.stem.endswith(("_truth", "_moved")):
                continue
            rec = from_tracker_npz(path)
            s = rec.fields["s_grid"] * rec.pixel_um
            ax.plot(s, window_mean(rec.fields["regr_mid"]) * P, color="#4c78a8", lw=1, alpha=0.6)
            ax.plot(s, window_mean(rec.fields["regr_plus"] - rec.fields["regr_minus"]) * P,
                    color="#e45756", lw=1, alpha=0.6)
            truth = np.load(tracks / f"{path.stem}_truth.npz")
        st = truth["s_grid"] * rec.pixel_um
        ax.plot(st, np.nanmean(truth["regr_mid"], 0) * P, "k--", lw=1.2, label="truth REGR")
        ax.plot(st, np.nanmean(truth["regr_plus"] - truth["regr_minus"], 0) * P, "k:", lw=1.2,
                label="truth flank difference")
        ax.plot([], [], color="#4c78a8", label="tracked REGR (5 seeds)")
        ax.plot([], [], color="#e45756", label="tracked flank difference")
        ax.set_title(f"{case}, clean")
        ax.set_xlabel("distance from tip (um)")
        ax.set_xlim(0, 1000)
    axes[0].set_ylabel("strain rate (%/h)")
    axes[1].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(out / "clean_profiles.png", dpi=150)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tracks, out = Path(a.tracks), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "field_level.md").write_text("\n".join(field_table()) + "\n")
    thresholds = load_thresholds()
    rows = image_rows(tracks, thresholds)
    with open(out / "image_level.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    (out / "image_level.md").write_text("\n".join(summary(rows)) + "\n")
    (out / "per_seed.md").write_text("\n".join(per_seed(rows, thresholds)) + "\n")
    rot = rotation_table(rows, thresholds["closure"])
    if rot:
        (out / "rotation.md").write_text("\n".join(rot) + "\n")
        print("\n".join(rot))
    plot_clean(tracks, out)
    print((out / "image_level.md").read_text())


if __name__ == "__main__":
    main()
