"""Tables for docs/specs/2026-10-11_remedy-fixes-coupled-mode-shared-compute.md, from the fetched sweeps.

  python scripts/synth/eval_fix.py --out results/2026-10-11_remedy_fixes [--parts band ...]

Reads staging/tracks_2026-10-11/<tracks dir>/ (fix_sweep.py fetch) and, for
unremedied uncoupled runs made before this spec, staging/tracks (identical
output: checked to 1e-13 px in item 1). Checks use the approved thresholds.
"""
import argparse
import sys
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import load_thresholds, run_checks  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.score import checks_pass, truth_error  # noqa: E402

warnings.simplefilter("ignore", RuntimeWarning)
CACHE = ROOT / "staging" / "tracks_2026-10-11"
OLD = ROOT / "staging" / "tracks"
CHECKS = ("rigid_invariance", "closure", "plane_sections")
TH = load_thresholds()


def find(name, dirs):
    for d in dirs:
        if (d / name).exists():
            return d / name
    return None


def evaluate(rid, tag, dirs, width_free=False):
    """Check values, truth error and run time of one setting on a rod and its moved copy. None if not run."""
    a, b = find(f"{rid}__{tag}.npz", dirs), find(f"{rid}_moved__{tag}.npz", dirs)
    t = find(f"{rid}_truth.npz", list(dirs) + [OLD])
    if a is None or b is None or t is None:
        return None
    rec, moved = from_tracker_npz(a), from_tracker_npz(b)
    checks = run_checks(rec, moved, TH, ("plane_sections",) if width_free else ())
    with np.load(t) as z:
        truth = {k: z[k] for k in z.files}
    return {"id": rid, "tag": tag, **{c.check: c.value for c in checks},
            **{f"{c.check}_pass": c.passed for c in checks}, "all_pass": checks_pass(checks),
            "run_s": rec.settings.get("run_s"), "truth": truth, **truth_error(rec, truth),
            "preprocess": rec.settings.get("preprocess", {})}


def cell(r, c):
    v = r[c]
    flag = {False: " F", None: " skip", True: ""}[r[f"{c}_pass"]]
    return f"{v:.2f}{flag}"


def band_table():
    """Item 3: registration band, closure and the other checks on clean and rigid_drift rods."""
    dirs = [CACHE / "tracks_band", OLD]
    lines = ["| Rod | Band | Band start (px) | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | All pass |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- |"]
    rids = [f"{c}_clean_s{s}" for c in ("growth_zone", "bending") for s in (0, 1, 2)] + \
           [f"growth_zone_rigid_drift_z1_s{s}" for s in (0, 1, 2)]
    for rid in rids:
        tags = [("none", "st1"), ("0.6-1.0 (retired)", "st1_reg")]
        tags += [(f"fixed {f}-1.0", f"st1_regb{int(100 * f)}") for f in (0.6, 0.8, 0.9)]
        for f in sorted((CACHE / "tracks_band").glob(f"{rid}__st1_regp*.npz")):
            tag = f.name.split("__")[1][:-4]
            kind = {"400": "profile to 400 px", "end": "profile to midline end", "in": "profile to midline end, in frame"}
            tags.append((kind[tag.rsplit("_", 1)[1]], tag))
        for label, tag in tags:
            r = evaluate(rid, tag, dirs)
            if r is None:
                continue
            start = r["preprocess"].get("register", {}).get("band_px", [None])[0]
            start = {"st1_reg": 240, "st1_regb60": 240, "st1_regb80": 320, "st1_regb90": 360}.get(tag, start)
            lines.append(f"| {rid} | {label} | {start if start is not None else '-'} | "
                         + " | ".join(cell(r, c) for c in CHECKS)
                         + f" | {r['regr_rms_pct_per_h']:.2f} | {r['flank_difference_rms_pct_per_h']:.2f} | "
                         f"{'yes' if r['all_pass'] else 'no'} |")
    return "\n".join(lines) + "\n\nF = fails the approved threshold. Tracked length 400 px. Band start from the profile: where the window-mean centre REGR of the unremedied record falls under 5 % of its peak.\n"


def fmt(vals):
    vals = [v for v in vals if v is not None and np.isfinite(v)]
    return f"{np.median(vals):.2f} [{min(vals):.2f}, {max(vals):.2f}]" if vals else "-"


def state_label(tag):
    if "_reg2p" in tag:
        return "register_frames"
    if "_ms" in tag:
        return "smooth_midline " + tag.split("_ms")[1].rstrip("2").split("_")[0]
    if "_r22" in tag or "_r30" in tag:
        return "enlarge_patch " + ("1.5x" if "_r22" in tag else "2x")
    return "none"


def clean_rows(tracks_dir):
    """Every clean rod and setting run in a tracks directory: evaluated rows."""
    rows = []
    for f in sorted(tracks_dir.glob("*_clean_s*__*.npz")):
        if "_moved__" in f.name:
            continue
        rid, tag = f.name[:-4].split("__")
        r = evaluate(rid, tag, [tracks_dir])
        if r:
            r["case"], r["seed"], r["state"] = rid.split("_clean_")[0], int(rid[-1]), state_label(tag)
            rows.append(r)
    return rows


STATE_ORDER = ["none", "register_frames", "smooth_midline light", "smooth_midline strong",
               "enlarge_patch 1.5x", "enlarge_patch 2x"]


def clean_table(rows, mode=""):
    lines = ["| Case | Remedy | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | All pass | Run time (s) |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- | --: |"]
    for case in ("growth_zone", "bending"):
        for st in STATE_ORDER:
            rs = [r for r in rows if r["case"] == case and r["state"] == st]
            if not rs:
                continue
            lines.append(f"| {case} | {st} | {len(rs)} | " + " | ".join(fmt([r[c] for r in rs]) for c in CHECKS)
                         + f" | {fmt([r['regr_rms_pct_per_h'] for r in rs])} | {fmt([r['flank_difference_rms_pct_per_h'] for r in rs])}"
                         + f" | {sum(r['all_pass'] for r in rs)} of {len(rs)} | {fmt([r['run_s'] for r in rs])} |")
    return "\n".join(lines) + "\n\nCells: median [min, max] over seeds 0-2. " + THRESHOLD_NOTE + "\n"


THRESHOLD_NOTE = (f"Approved thresholds: rigid_invariance {TH['rigid_invariance']} %/h, closure {TH['closure']} px/h, "
                  f"plane_sections {TH['plane_sections']} %/h.")


def u_clean_table():
    rows = clean_rows(CACHE / "tracks_uncoupled")
    fails = [f"{r['id']} {r['state']}: " + ", ".join(f"{c} {r[c]:.2f}" for c in CHECKS if r[f"{c}_pass"] is False)
             for r in rows if not r["all_pass"]]
    return (clean_table(rows) + "\nClean runs failing an approved threshold: "
            + ("; ".join(fails) if fails else "none") + "\n")


class OldTag:
    """Settings as run on 2026-10-10: smoothing runs were tagged mslight/msstrong (before the fix)."""
    def __init__(self, settings):
        self.settings = settings

    def tag(self):
        import re
        return re.sub(r"(ms(?:light|strong))2", r"\1", self.settings.tag())

    def __getattr__(self, name):
        return getattr(self.settings, name)


def labels_table():
    """Item 5: part C labels of 2026-10-10 (same runs) under the proposed and the approved tolerance."""
    import eval_repair as er
    from measure.remedies import TrackSettings
    from measure.render import rod_id
    from measure.score import label_rod, load_tolerance, measurement_good, rod_tolerance
    cfg = load_tolerance()
    proposed = {"regr_rms_pct_per_h": 1.0, "flank_difference_rms_pct_per_h": 0.5}
    lines = ["| Rod | Peak REGR (%/h) | Centre limit (%/h) | Label, proposed 1.0 %/h | Label, approved | Changed |",
             "| :-- | --: | --: | :-- | :-- | :-- |"]
    changed = []
    faults = dict(er.B_SIZES, width_change=[None])
    for fault, sizes in faults.items():
        for size in sizes:
            states = er.b_states(fault, size) if fault != "width_change" else [TrackSettings(), TrackSettings(width_free=True)]
            states = [OldTag(st) for st in states]
            for seed in er.SEEDS:
                rid = rod_id("growth_zone", fault, seed, size=size)
                res = [(st, er.evaluate(OLD, rid, st, TH)) for st in states]
                res = [(st, r) for st, r in res if r]
                if not res:
                    continue
                with np.load(OLD / f"{rid}_truth.npz") as z:
                    tol = rod_tolerance({k: z[k] for k in z.files}, 2.105, cfg)
                labs = []
                for t in (proposed, tol):
                    lab, seq = label_rod([{"sequence": er.sequence(fault, size, st), "checks_pass": r["all_pass"],
                                           "good": measurement_good(r, t, st.width_free)} for st, r in res])
                    labs.append(lab + (f" ({' + '.join(seq) or 'none needed'})" if seq is not None else ""))
                ch = labs[0] != labs[1]
                if ch:
                    changed.append(rid)
                lines.append(f"| {rid} | {tol['peak_regr_pct_per_h']:.1f} | {tol['regr_rms_pct_per_h']:.3f} | {labs[0]} | "
                             f"{labs[1]} | {'yes' if ch else ''} |")
    return ("Runs of 2026-10-10 (`results/2026-10-10_repair_criteria/`), unchanged; only the tolerance differs. "
            f"Approved: centre REGR RMS error <= {cfg['regr_rms_fraction_of_true_peak']} x true peak REGR, "
            f"flank-difference RMS error <= {cfg['flank_difference_rms_pct_per_h']} %/h.\n\n"
            f"Labels that change: {', '.join(changed) if changed else 'none'}.\n\n" + "\n".join(lines) + "\n")


TABLES = {"band": ("item3_band.md", band_table), "u_clean": ("item4_clean.md", u_clean_table),
          "labels": ("item5_labels.md", labels_table)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", nargs="+", default=sorted(TABLES), choices=sorted(TABLES))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for p in a.parts:
        name, make = TABLES[p]
        text = make()
        (out / name).write_text(text)
        print(f"## {name}\n{text}")


if __name__ == "__main__":
    main()
