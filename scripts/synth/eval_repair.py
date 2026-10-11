"""Tables for the repair-criteria spec, parts A, B and C, from the no-agent sweep.

  python scripts/synth/eval_repair.py [--tracks staging/tracks] --out results/<date>_repair_criteria

Reads <id>__<tag>.npz, <id>_moved__<tag>.npz and <id>_truth.npz (fetched by
repair_sweep.py fetch). Checks use the approved thresholds. Writes part_a.md,
part_b.md, part_c.md and runs.csv. Nothing here is adopted: sizes and the
tolerance are proposals for Andrew.
"""
import argparse
import csv
import math
import sys
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import run_checks, load_thresholds  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.render import rod_id  # noqa: E402
from measure.score import checks_pass, label_rod, measurement_good, truth_error  # noqa: E402
from repair_sweep import A_SETTINGS, B_SIZES, SEEDS, b_states  # noqa: E402

warnings.simplefilter("ignore", RuntimeWarning)
CHECKS = ("rigid_invariance", "closure", "plane_sections")


def evaluate(tracks, rid, settings, thresholds):
    tag = settings.tag()
    a, b = tracks / f"{rid}__{tag}.npz", tracks / f"{rid}_moved__{tag}.npz"
    if not a.exists() or not b.exists():
        return None
    rec, moved = from_tracker_npz(a), from_tracker_npz(b)
    skip = ("plane_sections",) if settings.width_free else ()
    checks = run_checks(rec, moved, thresholds, skip)
    with np.load(tracks / f"{rid}_truth.npz") as z:
        truth = {k: z[k] for k in z.files}
    err = truth_error(rec, truth)
    return {"id": rid, "tag": tag + ("_wf" if settings.width_free else ""),
            **{c.check: c.value for c in checks}, **{f"{c.check}_pass": c.passed for c in checks},
            "all_pass": checks_pass(checks), **err}


def fmt(vals):
    vals = [v for v in vals if v is not None and np.isfinite(v)]
    return f"{np.median(vals):.2f} [{min(vals):.2f}, {max(vals):.2f}]" if vals else "-"


def sequence(fault, size, s):
    if fault == "displacement_exceeds_patch":
        k, n = int(size.split("x")[1]), 0
        while k > s.stride:                     # halving is integer: 6 -> 3 -> 1
            k, n = max(1, k // 2), n + 1
        return ["change_frame_stride/half"] * n
    if s.register:
        return ["register_frames"]
    if s.midline_smooth:
        return [f"smooth_midline/{s.midline_smooth}"]
    if s.disk_radius:
        return [f"enlarge_patch/{'1.5x' if s.disk_radius == 22 else '2x'}"]
    if s.width_free:
        return ["use_width_free_ratio"]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks", default=str(ROOT / "staging" / "tracks"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tracks, out = Path(a.tracks), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    th = load_thresholds()
    rows = []

    # ---- A: clean rods under each remedy setting alone
    lines = ["| Case | Setting | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR RMS err (%/h) | Flank diff RMS err (%/h) | All pass |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- |"]
    a_ok = {}
    for case in ("growth_zone", "bending"):
        for s in A_SETTINGS:
            rs = [r for r in (evaluate(tracks, rod_id(case, None, seed), s, th) for seed in SEEDS) if r]
            for r in rs:
                r["part"] = "A"
            rows += rs
            if not rs:
                continue
            ok = all(r["all_pass"] for r in rs)
            a_ok.setdefault(s.tag(), []).append(ok)
            lines.append(f"| {case} | {s.tag()} | {len(rs)} | " + " | ".join(fmt([r[c] for r in rs]) for c in CHECKS)
                         + f" | {fmt([r['regr_rms_pct_per_h'] for r in rs])} | {fmt([r['flank_difference_rms_pct_per_h'] for r in rs])}"
                         + f" | {sum(r['all_pass'] for r in rs)} of {len(rs)} |")
    lines += ["", "Cells: median [min, max] over seeds. Approved thresholds: "
              f"rigid_invariance {th['rigid_invariance']} %/h, closure {th['closure']} px/h, plane_sections {th['plane_sections']} %/h."]
    (out / "part_a.md").write_text("\n".join(lines) + "\n")

    # ---- C (tolerance): largest clean error under settings that keep every clean run passing
    keep = {tag for tag, oks in a_ok.items() if all(oks)}
    a_rows = [r for r in rows if r["part"] == "A" and r["tag"] in keep]
    max_regr = max(r["regr_rms_pct_per_h"] for r in a_rows)
    max_flank = max(r["flank_difference_rms_pct_per_h"] for r in a_rows)
    step = 0.25
    tol = {"regr_rms_pct_per_h": math.floor(max_regr / step + 1) * step,
           "flank_difference_rms_pct_per_h": math.floor(max_flank / step + 1) * step}

    # ---- B: fault sizes and the fitting remedy's states; C: labels
    lines = ["| Fault | Size | Seed | State | Steps | rigid_invariance | closure | plane_sections | REGR err | Flank err | All pass | Good |",
             "| :-- | :-- | --: | :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |"]
    summary = ["| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | Remedied: seeds with three passes and good | Meets criteria |",
               "| :-- | :-- | :-- | :-- | :-- | :-- |"]
    labels = ["| Rod | Label | Repairing sequence |", "| :-- | :-- | :-- |"]
    faults = dict(B_SIZES, width_change=[None])
    for fault, sizes in faults.items():
        for size in sizes:
            states = b_states(fault, size) if fault != "width_change" else [TrackSettings(), TrackSettings(width_free=True)]
            fail0 = passed = good_pass = 0
            seeds_done = 0
            for seed in SEEDS:
                rid = rod_id("growth_zone", fault, seed, size=size)
                res = []
                for s in states:
                    r = evaluate(tracks, rid, s, th)
                    if r is None:
                        continue
                    seq = sequence(fault, size, s)
                    r.update(part="B", fault=fault, size=size, seed=seed, steps=len(seq),
                             sequence=" + ".join(seq) or "none",
                             good=measurement_good(r, tol, s.width_free))
                    rows.append(r)
                    res.append(r)
                    mark = lambda c: f"{r[c]:.2f}" + ("" if r[f"{c}_pass"] is not False else " F") + \
                        (" skip" if r[f"{c}_pass"] is None else "")
                    lines.append(f"| {fault} | {size} | {seed} | {r['tag']} | {r['steps']} | {mark('rigid_invariance')} | "
                                 f"{mark('closure')} | {mark('plane_sections')} | {r['regr_rms_pct_per_h']:.2f} | "
                                 f"{r['flank_difference_rms_pct_per_h']:.2f} | {'yes' if r['all_pass'] else 'no'} | "
                                 f"{'yes' if r['good'] else 'no'} |")
                if not res:
                    continue
                seeds_done += 1
                base = next(r for r in res if r["steps"] == 0)
                fail0 += not base["all_pass"]
                rem = [r for r in res if 1 <= r["steps"] <= 2]
                passed += any(r["all_pass"] for r in rem)
                good_pass += any(r["all_pass"] and r["good"] for r in rem)
                lab, seq = label_rod([{"sequence": r["sequence"].split(" + ") if r["steps"] else [],
                                       "checks_pass": r["all_pass"], "good": r["good"]} for r in res])
                labels.append(f"| {rid} | {lab} | {' + '.join(seq) if seq else ('none needed' if lab == 'repairable' else '-')} |")
            if seeds_done:
                meets = fail0 == seeds_done and good_pass >= 2
                summary.append(f"| {fault} | {size} | {fail0} of {seeds_done} | {passed} of {seeds_done} | "
                               f"{good_pass} of {seeds_done} | {'yes' if meets else 'no'} |")
    (out / "part_b.md").write_text("\n".join(summary) + "\n\nPer run (F = fails the approved threshold; skip = not applied):\n\n"
                                   + "\n".join(lines) + "\n")
    (out / "part_c.md").write_text(
        f"Proposed tolerance (not approved): centre REGR RMS error <= {tol['regr_rms_pct_per_h']} %/h, "
        f"flank-difference RMS error <= {tol['flank_difference_rms_pct_per_h']} %/h.\n"
        f"Basis: largest clean values {max_regr:.2f} and {max_flank:.2f} %/h over part A settings that keep every clean run passing "
        f"({', '.join(sorted(keep))}), rounded up to the next {step} %/h.\n\n"
        "Labels, from the part B states only (the fitting remedy's one- and two-step states). A label is final only for the approved sizes:\n\n"
        + "\n".join(labels) + "\n")
    keys = sorted({k for r in rows for k in r})
    with open(out / "runs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    print((out / "part_a.md").read_text())
    print((out / "part_b.md").read_text().split("Per run")[0])
    print((out / "part_c.md").read_text())


if __name__ == "__main__":
    main()
