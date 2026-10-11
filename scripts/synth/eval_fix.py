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


TABLES = {"band": ("item3_band.md", band_table)}


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
