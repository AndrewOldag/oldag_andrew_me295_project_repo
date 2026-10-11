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
        return "smooth_midline " + tag.split("_ms")[1].split("_")[0].rstrip("23")
    if "_r22" in tag or "_r30" in tag:
        return "enlarge_patch " + ("1.5x" if "_r22" in tag else "2x")
    if tag.endswith("_mask") or tag.endswith("_crop"):
        return "crop_or_mask " + ("mask_second_root" if tag.endswith("_mask") else "crop_to_main_root")
    if tag.startswith("st2"):
        return "change_frame_stride double"
    return "none"


def clean_rows(tracks_dir, keep=lambda tag: True):
    """Every clean rod and setting run in a tracks directory (tags passing `keep`): evaluated rows."""
    rows = []
    for f in sorted(tracks_dir.glob("*_clean_s*__*.npz")):
        if "_moved__" in f.name or ".part." in f.name:
            continue
        rid, tag = f.name[:-4].split("__")
        if not keep(tag):
            continue
        r = evaluate(rid, tag, [tracks_dir])
        if r:
            r["case"], r["seed"], r["state"] = rid.split("_clean_")[0], int(rid[-1]), state_label(tag)
            rows.append(r)
    return rows


STATE_ORDER = ["none", "register_frames", "smooth_midline light", "smooth_midline strong",
               "enlarge_patch 1.5x", "enlarge_patch 2x", "crop_or_mask mask_second_root",
               "crop_or_mask crop_to_main_root", "change_frame_stride double"]


def clean_table(rows, mode=""):
    lines = ["| Case | Remedy | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | All pass | Run time (s) |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- | --: |"]
    for case in ("growth_zone", "bending", "bend_continue", "bend_reverse"):
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


def steps(tag):
    """Remedy steps from the unremedied state: one per fixed remedy here (stride halvings count each)."""
    return 0 if state_label(tag) == "none" else 1


def fault_rows(tracks_dir, fault_ids, keep=lambda tag: True, cfg=None):
    """Evaluated rows for fault rods, with the rod's tolerance (approved unless cfg is given) and 'good'."""
    from measure.score import load_tolerance, measurement_good, rod_tolerance
    cfg = cfg or load_tolerance()
    rows = []
    for rid in fault_ids:
        for f in sorted(tracks_dir.glob(f"{rid}__*.npz")):
            tag = f.name[:-4].split("__")[1]
            if ".part" in tag or not keep(tag):
                continue
            r = evaluate(rid, tag, [tracks_dir])
            if r is None:
                continue
            tol = rod_tolerance(r["truth"], 2.105, cfg)
            r.update(state=state_label(tag), steps=steps(tag), good=measurement_good(r, tol),
                     limit=tol["regr_rms_pct_per_h"])
            rows.append(r)
    return rows


def fault_tables(rows, groups):
    """Part-B form: summary per fault and size, then every run. groups: [(fault, size, [rod ids])]."""
    from measure.score import label_rod
    summary = ["| Fault | Size | Unremedied: seeds failing a check | Remedied (1 step): seeds with three passes | Remedied: three passes and good | Meets criteria |",
               "| :-- | :-- | :-- | :-- | :-- | :-- |"]
    per = ["| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |",
           "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"]
    labels = ["| Rod | Label | Repairing remedy |", "| :-- | :-- | :-- |"]
    for fault, size, rids in groups:
        fail0 = passed = good_pass = done = 0
        for rid in rids:
            rs = sorted([r for r in rows if r["id"] == rid], key=lambda r: STATE_ORDER.index(r["state"]))
            if not rs or rs[0]["steps"] != 0:
                continue
            done += 1
            fail0 += not rs[0]["all_pass"]
            rem = [r for r in rs if r["steps"] >= 1]
            passed += any(r["all_pass"] for r in rem)
            good_pass += any(r["all_pass"] and r["good"] for r in rem)
            for r in rs:
                per.append(f"| {rid} | {r['state']} | " + " | ".join(cell(r, c) for c in CHECKS)
                           + f" | {r['regr_rms_pct_per_h']:.2f} ({r['limit']:.2f}) | {r['flank_difference_rms_pct_per_h']:.2f} | "
                           f"{'yes' if r['all_pass'] else 'no'} | {'yes' if r['good'] else 'no'} |")
            lab, seq = label_rod([{"sequence": [] if r["steps"] == 0 else [r["state"]], "checks_pass": r["all_pass"],
                                   "good": r["good"]} for r in rs])
            labels.append(f"| {rid} | {lab} | {' + '.join(seq) if seq else ('none needed' if lab == 'repairable' else '-')} |")
        if done:
            meets = fail0 == done and good_pass >= 2
            summary.append(f"| {fault} | {size} | {fail0} of {done} | {passed} of {done} | {good_pass} of {done} | "
                           f"{'yes' if meets else 'no'} |")
    return "\n".join(summary), "\n".join(per), "\n".join(labels)


def u_fault_groups():
    import fix_sweep as fs
    return [(f, z, [fs.Rod("growth_zone", f, s, size=z).id() for s in fs.SEEDS])
            for f, sizes in fs.U_SIZES.items() for z in sizes]


def u_faults_table():
    groups = u_fault_groups()
    rows = fault_rows(CACHE / "tracks_uncoupled", [rid for _, _, ids in groups for rid in ids])
    summary, per, labels = fault_tables(rows, groups)
    return ("Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and the fitting remedy "
            "gives three passes and a good measurement on at least 2 of 3 seeds. Good: approved tolerance "
            "(REGR limit in brackets, 2.5 % of the true peak; flank 0.5 %/h). " + THRESHOLD_NOTE + "\n\n"
            + summary + "\n\nLabels (from these states only):\n\n" + labels
            + "\n\nPer run (F = fails the approved threshold):\n\n" + per + "\n")


def side_by_side(groups, dirs_u, dirs_c, width_free=False):
    """groups: [(label, remedy, [(rid, uncoupled tag)])]. Both modes per group: checks, errors, fails, run time."""
    lines = ["| Rods | Remedy | Mode | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | Runs failing a check | Run time (s) |",
             "| :-- | :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: |"]
    allrows = {"uncoupled": [], "coupled": []}
    for label, remedy, items in groups:
        for mode, dirs, suffix in (("uncoupled", dirs_u, ""), ("coupled", dirs_c, "_cpl")):
            rs = [r for r in (evaluate(rid, tag + suffix, dirs, width_free) for rid, tag in items) if r]
            allrows[mode] += rs
            if not rs:
                continue
            lines.append(f"| {label} | {remedy} | {mode} | {len(rs)} | " + " | ".join(fmt([r[c] for r in rs]) for c in CHECKS)
                         + f" | {fmt([r['regr_rms_pct_per_h'] for r in rs])} | {fmt([r['flank_difference_rms_pct_per_h'] for r in rs])}"
                         + f" | {sum(not r['all_pass'] for r in rs)} | {fmt([r['run_s'] for r in rs])} |")
    return "\n".join(lines), allrows


def c_basis_table():
    import fix_sweep as fs
    groups = [(f"{c} s0-4", "none", [(r.id(), "st1") for r in fs.BASIS if r.case == c])
              for c in ("growth_zone", "bending", "rigid_translation")]
    d = [CACHE / "tracks_coupled"]
    table, rows = side_by_side(groups, d, d)
    per = ["| Rod | Mode | " + " | ".join(CHECKS) + " | All pass |", "| :-- | :-- | --: | --: | --: | :-- |"]
    for r in sorted(rows["uncoupled"] + rows["coupled"], key=lambda r: (r["id"], r["tag"])):
        per.append(f"| {r['id']} | {'coupled' if r['tag'].endswith('_cpl') else 'uncoupled'} | "
                   + " | ".join(cell(r, c) for c in CHECKS) + f" | {'yes' if r['all_pass'] else 'no'} |")
    fails = [r["id"] for r in rows["coupled"] if not r["all_pass"]]
    return (table + "\n\nCells: median [min, max]. " + THRESHOLD_NOTE + "\n\nClean coupled rods failing an approved threshold: "
            + (", ".join(fails) if fails else "none") + f" ({len(rows['coupled']) - len(fails)} of {len(rows['coupled'])} pass).\n\n"
            + "\n".join(per) + "\n")


def flank_errors(rid, tag, dirs):
    """RMS error (%/h) of the window-mean plus and minus flank strain rates against the truth."""
    from measure.record import PER_S_TO_PCT_PER_H
    from measure.score import _wmean
    rec = from_tracker_npz(find(f"{rid}__{tag}.npz", dirs))
    with np.load(find(f"{rid}_truth.npz", dirs)) as z:
        truth = {k: z[k] for k in z.files}
    s = rec.fields["s_grid"]
    out = {}
    for k in ("regr_plus", "regr_minus"):
        t = np.interp(s, truth["s_grid"], np.nanmean(truth[k], axis=0), right=np.nan)
        e = (_wmean(rec.fields[k]) - t) * PER_S_TO_PCT_PER_H
        out[k] = float(np.sqrt(np.nanmean(e ** 2)))
    return out


def bent_table():
    import fix_sweep as fs
    d = [CACHE / "tracks_bent"]
    lines = ["| Rod | Mode | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | Peak at s (px) | REGR err (%/h) | Plus flank err (%/h) | Minus flank err (%/h) | Flank diff err (%/h) | All pass |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: | :-- |"]
    for rod in fs.BENT:
        for mode, tag in (("uncoupled", "st1"), ("coupled", "st1_cpl")):
            r = evaluate(rod.id(), tag, d)
            if r is None:
                continue
            fe = flank_errors(rod.id(), tag, d)
            rec = from_tracker_npz(find(f"{rod.id()}__{tag}.npz", d))
            ps = [c for c in run_checks(rec, None, TH) if c.check == "plane_sections"][0]
            lines.append(f"| {rod.id()} | {mode} | " + " | ".join(cell(r, c) for c in CHECKS)
                         + f" | {ps.where_s_px:.0f} | {r['regr_rms_pct_per_h']:.2f} | {fe['regr_plus']:.2f} | {fe['regr_minus']:.2f} | "
                         f"{r['flank_difference_rms_pct_per_h']:.2f} | {'yes' if r['all_pass'] else 'no'} |")
    return ("Frame 640 x 640 px, base at column 400, tracked length 400 px. Coupled runs not made: they wait for Andrew "
            "(coupled clean rods fail closure, item 6). " + THRESHOLD_NOTE + "\n\n" + "\n".join(lines) + "\n")


# ---- spec 2026-10-11b

B = CACHE / "tracks_b"
U = CACHE / "tracks_uncoupled"


def b_smooth_table():
    """11b item 1: clean rods and midline_jitter with the fitted-line padding; unremedied runs from item 4."""
    clean = clean_rows(U, lambda t: t == "st1") + clean_rows(B, lambda t: "_ms" in t and t.endswith("3"))
    fails = [f"{r['id']} {r['state']}" for r in clean if not r["all_pass"]]
    import fix_sweep as fs
    groups = [("midline_jitter", z, [fs.Rod("growth_zone", "midline_jitter", s, size=z).id() for s in fs.SEEDS])
              for z in fs.U_SIZES["midline_jitter"]]
    ids = [i for _, _, ii in groups for i in ii]
    rows = fault_rows(U, ids, lambda t: t == "st1") + fault_rows(B, ids, lambda t: t.endswith("3"))
    summary, per, labels = fault_tables(rows, groups)
    return ("Smoothing with the fitted-line time padding (tags `mslight3`, `msstrong3`). Unremedied runs: item 4 of the "
            "2026-10-11 spec (same code). " + THRESHOLD_NOTE + "\n\n## Clean rods\n\n" + clean_table(clean)
            + "\nClean runs failing an approved threshold: " + (", ".join(fails) if fails else "none")
            + "\n\n## midline_jitter\n\n" + summary + "\n\n" + labels + "\n\nPer run:\n\n" + per + "\n")


def profile_numbers(rid, tag, dirs):
    """Peak REGR (record and tracker's own output), peak position, zone length above half the peak,
    integrated strain rate and tip speed (px/h), apparent strain rate RMS (%/h)."""
    from measure.record import PER_S_TO_PCT_PER_H as K
    from measure.score import _wmean
    f = find(f"{rid}__{tag}.npz", dirs)
    rec = from_tracker_npz(f)
    s = rec.fields["s_grid"]
    m = _wmean(rec.fields["regr_mid"]) * K
    j = int(np.nanargmax(m))
    above = s[np.isfinite(m) & (m >= 0.5 * m[j])]
    with np.load(f) as z:
        own = 0.5 * (z["qb_regr_left"] + z["qb_regr_right"]) * K
    ok = np.isfinite(m)
    integ = float(np.trapezoid(m[ok], s[ok])) / 100.0                       # (%/h) px -> px/h
    tip = rec.midline[:, 0] + 0.0
    tw = tip                                                                 # midline is in the world frame
    speed = float(np.linalg.norm(tw[-1] - tw[0]) / ((rec.frame_times_s[-1] - rec.frame_times_s[0]) / 3600))
    return {"peak": float(m[j]), "peak_own": float(np.nanmax(own)), "peak_at": float(s[j]),
            "zone_len": float(above.max() - above.min()) if len(above) else np.nan,
            "integ": integ, "tip_speed": speed, "apparent": float(np.sqrt(np.nanmean(m ** 2)))}


def b_weight_table():
    """11b item 4: coupling weight, lambda and mu scaled together, against the uncoupled run."""
    import fix_sweep as fs
    from measure.score import load_tolerance, measurement_good, rod_tolerance, truth_summary
    cfg = load_tolerance()
    d = [CACHE / "tracks_b_weight"]
    groups = {"growth_zone": "growth_zone_clean", "bending": "bending_clean", "rigid_translation": "rigid_translation_clean",
              "bend_continue": "bend_continue_clean", "bend_reverse": "bend_reverse_clean",
              "growth_zone x2 speed": "growth_zone_displacement_exceeds_patch_z2x1"}
    modes = [("uncoupled", "st1")] + [(f"coupled x{w:g}", fs.weight_tag(w)) for w in fs.WEIGHTS]
    lines = ["| Rods | Mode | Peak REGR record / tracker / truth (%/h) | Peak at s (px) | Zone above half peak (px) | REGR err (%/h) | Flank err (%/h) | rigid_invariance | closure | plane_sections | Runs failing | Within tolerance | Integrated REGR / tip speed (px/h) |",
             "| :-- | :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-- |"]
    ok_all = {m: True for m, _ in modes}
    loss = {}
    for label, prefix in groups.items():
        ids = [f"{prefix}_s{s}" for s in fs.SEEDS]
        for mode, tag in modes:
            rs, ps = [], []
            for rid in ids:
                r = evaluate(rid, tag, d)
                if r is None:
                    continue
                ts = truth_summary(r["truth"], 2.105)
                r["good"] = measurement_good(r, rod_tolerance(r["truth"], 2.105, cfg))
                r["truth_peak"] = ts["peak_regr_pct_per_h"]
                rs.append(r)
                ps.append(profile_numbers(rid, tag, d))
            if not rs:
                continue
            growing = label != "rigid_translation"
            if growing and not all(r["all_pass"] and r["good"] for r in rs):
                ok_all[mode] = False
            pk = np.median([p["peak"] for p in ps])
            tpk = rs[0]["truth_peak"]
            if label in ("growth_zone", "growth_zone x2 speed"):
                loss.setdefault(mode, {})[label] = 1 - pk / tpk
            peak_cell = (f"{pk:.1f} / {np.median([p['peak_own'] for p in ps]):.1f} / {tpk:.1f}" if growing
                         else f"apparent RMS {np.median([p['apparent'] for p in ps]):.2f}")
            lines.append(f"| {label} | {mode} | {peak_cell} | {np.median([p['peak_at'] for p in ps]):.0f} | "
                         f"{np.median([p['zone_len'] for p in ps]):.0f} | {fmt([r['regr_rms_pct_per_h'] for r in rs])} | "
                         f"{fmt([r['flank_difference_rms_pct_per_h'] for r in rs])} | "
                         + " | ".join(fmt([r[c] for r in rs]) for c in CHECKS)
                         + f" | {sum(not r['all_pass'] for r in rs)} of {len(rs)} | {sum(r['good'] for r in rs)} of {len(rs)} | "
                         f"{np.median([p['integ'] for p in ps]):.1f} / {np.median([p['tip_speed'] for p in ps]):.1f} |")
    passing = [m for m, _ in modes if ok_all[m] and m != "uncoupled"]
    loss_lines = [f"- {m}: {100 * v.get('growth_zone', np.nan):.1f} % at 1x, {100 * v.get('growth_zone x2 speed', np.nan):.1f} % at 2x"
                  for m, v in loss.items()]
    return ("Coupling weights lambda (inextensibility) and mu (smoothness), tracker defaults 2.0 each, scaled together. "
            "x0 is coupled with both set to 0. 3 seeds per group, each tracked twice. Cells: median, or median [min, max]. "
            + THRESHOLD_NOTE + " Within tolerance: approved tolerance (centre 2.5 % of the true peak, flank 0.5 %/h).\n\n"
            + "\n".join(lines)
            + "\n\nCoupled weights at which every growing clean rod passes the approved thresholds and is within tolerance: "
            + (", ".join(passing) if passing else "none") + f" (uncoupled: {'yes' if ok_all['uncoupled'] else 'no'}).\n\n"
            + "Loss at the peak (1 - record peak / true peak), growth_zone at once and twice the tip speed:\n\n"
            + "\n".join(loss_lines) + "\n")


TABLES = {"b_weight": ("b4_coupling_weight.md", b_weight_table),
          "b_smooth": ("b1_smoothing.md", b_smooth_table), "band": ("item3_band.md", band_table), "u_clean": ("item4_clean.md", u_clean_table),
          "bent": ("item7_bent.md", bent_table),
          "c_basis": ("item6_clean_basis.md", c_basis_table),
          "labels": ("item5_labels.md", labels_table), "u_faults": ("item4_faults.md", u_faults_table)}


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
