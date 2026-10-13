"""Labels of the five development faults at their frozen sizes, for spec 2026-10-12 (freeze decisions).

  python scripts/synth/eval_freeze.py --out results/2026-10-12_freeze_v2 [--parts relabel seeds35]

relabel: seeds 0-2 from the existing runs, under flank tolerance 0.5 and 1.00 %/h (item 1).
seeds35: seeds 3-5 from staging/tracks_2026-10-12/tracks_freeze (freeze_sweep.py fetch), against seeds 0-2 (item 3).
Each fault is run through the fitting remedy's states only, as when seeds 0-2 were labelled. `strong` is
withdrawn and not a state. Checks use the approved thresholds; centre limit 2.5 % of the rod's true peak.
"""
import argparse
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_fix import CHECKS, THRESHOLD_NOTE, cell, evaluate  # noqa: E402
from measure.render import rod_id  # noqa: E402
from measure.score import label_rod, load_tolerance, measurement_good, rod_tolerance  # noqa: E402

warnings.simplefilter("ignore", RuntimeWarning)
STAGING = ROOT / "staging"
OLD = STAGING / "tracks"                                     # 2026-10-10 runs (repair_sweep.py)
U = STAGING / "tracks_2026-10-11" / "tracks_uncoupled"       # 2026-10-11 item 4 (fixed register_frames)
C = STAGING / "tracks_2026-10-11" / "tracks_c"               # 2026-10-11c (world-coordinate smoothing)
NEW = STAGING / "tracks_2026-10-12" / "tracks_freeze"        # seeds 3-5 (this spec)

# fault -> frozen size (docs/proposals/2026-10-11_freeze-v1.md, section 1)
FROZEN = {"displacement_exceeds_patch": "2x6", "width_change": None, "rigid_drift": "0.5",
          "low_texture": "0.03", "midline_jitter": "3"}


def states(fault):
    """[(remedy sequence, tag or tag glob, width_free)]: the fitting remedy's states, unremedied first."""
    if fault == "displacement_exceeds_patch":
        h = "change_frame_stride/half"
        return [([], "st6", False), ([h], "st3", False), ([h, h], "st1", False)]
    if fault == "width_change":
        return [([], "st1", False), (["use_width_free_ratio"], "st1", True)]
    if fault == "rigid_drift":
        return [([], "st1", False), (["register_frames"], "st1_reg2p*", False)]
    if fault == "low_texture":
        return [([], "st1", False), (["enlarge_patch/1.5x"], "st1_r22", False), (["enlarge_patch/2x"], "st1_r30", False)]
    if fault == "midline_jitter":
        return [([], "st1", False), (["smooth_midline/light"], "st1_mslight4", False)]
    raise ValueError(fault)


def dev_dirs(fault):
    """Where the seeds 0-2 runs of each fault are (the runs behind the freeze v1 labels)."""
    return {"displacement_exceeds_patch": [OLD], "width_change": [OLD], "low_texture": [OLD],
            "rigid_drift": [U, OLD], "midline_jitter": [U, C, OLD]}[fault]


def resolve(rid, tag, dirs):
    if "*" not in tag:
        return tag
    for d in dirs:
        hit = sorted(f.name[:-4].split("__")[1] for f in d.glob(f"{rid}__{tag}.npz") if ".part" not in f.name)
        if hit:
            return hit[0]
    return None


def rod_rows(fault, seed, dirs, flank_tols):
    """Evaluated states of one rod; 'good' and the label under each flank tolerance."""
    rid = rod_id("growth_zone", fault, seed, size=FROZEN[fault])
    cfg = load_tolerance()
    rows = []
    for seq, tag, wf in states(fault):
        t = resolve(rid, tag, dirs)
        r = evaluate(rid, t, dirs, wf) if t else None
        if r is None:
            continue
        r.update(sequence=seq, state=" + ".join(seq) or "none", width_free=wf)
        for ft in flank_tols:
            tol = rod_tolerance(r["truth"], 2.105, dict(cfg, flank_difference_rms_pct_per_h=ft))
            r[f"good_{ft}"] = measurement_good(r, tol, wf)
            r["limit"] = tol["regr_rms_pct_per_h"]
        rows.append(r)
    labels = {}
    for ft in flank_tols:
        lab, seq = label_rod([{"sequence": r["sequence"], "checks_pass": r["all_pass"], "good": r[f"good_{ft}"]}
                              for r in rows]) if rows else ("not run", None)
        labels[ft] = lab + (f" ({' + '.join(seq) or 'none needed'})" if seq is not None else "")
    return rid, rows, labels


def relabel_table(seeds=(0, 1, 2)):
    """Item 1: seeds 0-2 under flank 0.5 (approved 2026-10-11) and 1.00 %/h (approved 2026-10-12)."""
    lines = ["| Rod | Runs | Label, flank 0.5 %/h | Label, flank 1.00 %/h | Changed |", "| :-- | --: | :-- | :-- | :-- |"]
    changed = []
    for fault in FROZEN:
        for seed in seeds:
            rid, rows, lab = rod_rows(fault, seed, dev_dirs(fault), (0.5, 1.0))
            ch = lab[0.5] != lab[1.0]
            changed += [rid] if ch else []
            lines.append(f"| {rid} | {len(rows)} | {lab[0.5]} | {lab[1.0]} | {'yes' if ch else ''} |")
    return ("Existing runs only (no new tracker runs): 2x6, width_change and low_texture from 2026-10-10 "
            "(`staging/tracks`); rigid_drift from 2026-10-11 item 4; midline_jitter unremedied from 2026-10-11 item 4 and "
            "`light` from 2026-10-11c. States: the fitting remedy only; `strong` withdrawn. " + THRESHOLD_NOTE
            + " Centre limit 2.5 % of the rod's true peak.\n\n"
            f"Labels that change: {', '.join(changed) if changed else 'none'}.\n\n" + "\n".join(lines) + "\n"), changed


def fault_tables(seeds, dirs_of, ft=1.0):
    """Item 4 table form of 2026-10-11 (summary, labels, per run), at flank tolerance ft."""
    summary = ["| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | "
               "Remedied: three passes and good | Meets criteria |", "| :-- | :-- | :-- | :-- | :-- | :-- |"]
    per = ["| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |",
           "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"]
    labels = ["| Rod | Label | Repairing remedy |", "| :-- | :-- | :-- |"]
    out = {}
    for fault, size in FROZEN.items():
        fail0 = passed = good_pass = done = 0
        for seed in seeds:
            rid, rows, lab = rod_rows(fault, seed, dirs_of(fault), (ft,))
            out[rid] = lab[ft]
            if not rows or rows[0]["sequence"]:
                labels.append(f"| {rid} | not run | - |")
                continue
            done += 1
            fail0 += not rows[0]["all_pass"]
            rem = rows[1:]
            passed += any(r["all_pass"] for r in rem)
            good_pass += any(r["all_pass"] and r[f"good_{ft}"] for r in rem)
            for r in rows:
                per.append(f"| {rid} | {r['state']} | " + " | ".join(cell(r, c) for c in CHECKS)
                           + f" | {r['regr_rms_pct_per_h']:.2f} ({r['limit']:.2f}) | {r['flank_difference_rms_pct_per_h']:.2f} | "
                           f"{'yes' if r['all_pass'] else 'no'} | {'yes' if r[f'good_{ft}'] else 'no'} |")
            name, _, seq = lab[ft].partition(" (")
            labels.append(f"| {rid} | {name} | {seq.rstrip(')') or '-'} |")
        if done:
            meets = fail0 == done and good_pass >= 2
            summary.append(f"| {fault} | {size or '1/400'} | {fail0} of {done} | {passed} of {done} | {good_pass} of {done} | "
                           f"{'yes' if meets else 'no'} |")
    return "\n".join(summary), "\n".join(labels), "\n".join(per), out


def seeds35_table():
    """Item 3: seeds 3-5 labels, and against the seeds 0-2 label of the same fault."""
    summary, labels, per, new = fault_tables((3, 4, 5), lambda f: [NEW])
    _, _, _, old = fault_tables((0, 1, 2), dev_dirs)
    cmp = ["| Fault | Size | Label, seeds 0-2 | Label, seeds 3-5 | Differs |", "| :-- | :-- | :-- | :-- | :-- |"]
    differ = []
    for fault, size in FROZEN.items():
        o = sorted({v.split(" (")[0] for k, v in old.items() if f"_{fault}_" in k})
        n = {k: v.split(" (")[0] for k, v in new.items() if f"_{fault}_" in k}
        bad = [k for k, v in n.items() if [v] != o]
        differ += bad
        cmp.append(f"| {fault} | {size or '1/400'} | {', '.join(o)} | {', '.join(sorted(set(n.values())))} | "
                   f"{', '.join(bad) if bad else ''} |")
    return ("Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and the fitting remedy "
            "gives three passes and a good measurement on at least 2 of 3 seeds. Good: approved tolerance "
            "(REGR limit in brackets, 2.5 % of the true peak; flank 1.00 %/h, approved 2026-10-12). " + THRESHOLD_NOTE
            + " Seeds 3-5, frozen sizes, the fitting remedy's states (`strong` withdrawn).\n\n"
            + "\n".join(cmp) + f"\n\nSeed 3-5 labels that differ from seeds 0-2: {', '.join(differ) if differ else 'none'}.\n\n"
            + summary + "\n\nLabels (from these states only):\n\n" + labels
            + "\n\nPer run (F = fails the approved threshold):\n\n" + per + "\n"), differ


TABLES = {"relabel": ("item1_labels.md", relabel_table), "seeds35": ("item3_seeds35.md", seeds35_table)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", nargs="+", default=["relabel"], choices=sorted(TABLES))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for p in a.parts:
        name, make = TABLES[p]
        text, flagged = make()
        (out / name).write_text(text)
        print(f"## {name}\n{text}")
        if flagged:
            print(f"STOP: {len(flagged)} label(s) flagged in {name}")


if __name__ == "__main__":
    main()
