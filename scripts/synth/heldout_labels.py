"""Labels of the five held-out faults at the approved sizes (spec 2026-10-12b, item 3). Tracker only, no agent.

  python scripts/synth/heldout_labels.py start [--dry-run]
  python scripts/synth/heldout_labels.py status
  python scripts/synth/heldout_labels.py stop
  python scripts/synth/heldout_labels.py fetch          # to staging/tracks_heldout_labels/
  python scripts/synth/heldout_labels.py eval --out results/2026-10-12b_heldout_labels

Seeds 0-2, growth_zone, uncoupled. The unremedied runs are those of the held-out size sweep
(staging/tracks_heldout, heldout_sweep.py); this sweep runs the fitting remedy's states listed in
docs/proposals/2026-10-12_heldout-faults.md, open item 3, at most two steps:
- fast_rotation, bad_stage_correction: register_frames (band start from the unremedied record)
- second_root: crop_or_mask crop_to_main_root; crop_or_mask mask_second_root
- partial_occlusion, flank_swap: enlarge_patch 1.5x and 2x; change_frame_stride double; and
  change_frame_stride double followed by enlarge_patch 1.5x or 2x
Labels by the repair criteria (spec 2026-10-10, part C; measure.score.label_rod), approved thresholds,
scoring tolerance config/scoring_tolerance.yaml (centre 2.5 % of the true peak, flank 1.00 %/h).
The width-free ratio needs no tracker run; it is evaluated on every unremedied rod and reported apart
from the labels (it is not a fitting remedy of any held-out fault in the proposal).
"""
import argparse
import json
import sys
import warnings
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_sweep import BASE_RADIUS, entry  # noqa: E402
from heldout_sweep import CACHE as BASE_CACHE, config  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

warnings.simplefilter("ignore", RuntimeWarning)
NAME, TRACKS = "heldout_labels", "tracks_heldout_labels"
CACHE = ROOT / "staging" / TRACKS
SEEDS = (0, 1, 2)
APPROVED = {"second_root": "30", "fast_rotation": "2", "bad_stage_correction": "3", "flank_swap": "0.5",
            "partial_occlusion": "20"}     # Andrew, 2026-10-12


def rods():
    return [Rod("growth_zone", f, s, size=z) for f, z in APPROVED.items() for s in SEEDS]


def band_start(rod):
    from measure.preprocess import registration_band_start
    from measure.record import from_tracker_npz
    f = BASE_CACHE / f"{rod.id()}__st1.npz"
    if not f.exists():
        raise FileNotFoundError(f"{f.name} not in {BASE_CACHE.name}; fetch the held-out size sweep first")
    return int(round(registration_band_start(from_tracker_npz(f))))


def states(rod):
    """[(remedy sequence, TrackSettings)], remedied states only (unremedied: the size sweep's st1 run)."""
    base = TrackSettings()
    r15, r2 = round(1.5 * BASE_RADIUS), 2 * BASE_RADIUS
    if rod.fault in ("fast_rotation", "bad_stage_correction"):
        return [(["register_frames"], replace(base, register=True, register_from_px=band_start(rod)))]
    if rod.fault == "second_root":
        return [([f"crop_or_mask/{m}"], replace(base, band_mask=m)) for m in ("crop_to_main_root", "mask_second_root")]
    d = "change_frame_stride/double"
    return [(["enlarge_patch/1.5x"], replace(base, disk_radius=r15)),
            (["enlarge_patch/2x"], replace(base, disk_radius=r2)),
            ([d], replace(base, stride=2)),
            ([d, "enlarge_patch/1.5x"], replace(base, stride=2, disk_radius=r15)),
            ([d, "enlarge_patch/2x"], replace(base, stride=2, disk_radius=r2))]


def plan():
    return {"rods": [entry(r, [s for _, s in states(r)]) for r in rods()]}


# ------------------------------------------------------------------ labels

def rod_rows(rod):
    from eval_fix import evaluate
    from measure.score import load_tolerance, measurement_good, rod_tolerance
    cfg = load_tolerance()
    rows = []
    for seq, st in [([], TrackSettings())] + states(rod):
        r = evaluate(rod.id(), st.tag(), [CACHE, BASE_CACHE])
        if r is None:
            rows.append({"sequence": seq, "state": " + ".join(seq) or "none", "missing": True})
            continue
        tol = rod_tolerance(r["truth"], 2.105, cfg)
        r.update(sequence=seq, state=" + ".join(seq) or "none", good=measurement_good(r, tol, False),
                 limit=tol["regr_rms_pct_per_h"], flank_limit=tol["flank_difference_rms_pct_per_h"])
        rows.append(r)
    wf = evaluate(rod.id(), "st1", [BASE_CACHE], width_free=True)
    if wf is not None:
        tol = rod_tolerance(wf["truth"], 2.105, cfg)
        wf.update(good=measurement_good(wf, tol, True), limit=tol["regr_rms_pct_per_h"])
    return rows, wf


def evaluate_all(out):
    from eval_fix import CHECKS, THRESHOLD_NOTE, cell
    from measure.render_heldout import EXPECTED
    from measure.score import label_rod
    summary = ["| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | "
               "Remedied: three passes and good | Meets criteria |", "| :-- | :-- | :-- | :-- | :-- | :-- |"]
    labels = ["| Rod | Label | Repairing remedy |", "| :-- | :-- | :-- |"]
    per = ["| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |",
           "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"]
    wfl = ["| Rod | rigid_invariance | closure | plane_sections | REGR err (limit) | Checks pass | Centre good |",
           "| :-- | --: | --: | --: | --: | :-- | :-- |"]
    cmp = ["| Fault | Size | Expected outcome (proposal) | Labels, seeds 0-2 | Correct outcome by label | Differs |",
           "| :-- | :-- | :-- | :-- | :-- | :-- |"]
    out_json, missing, differ = [], 0, []
    for fault, size in APPROVED.items():
        fail0 = passed = good_pass = done = 0
        labs = []
        for seed in SEEDS:
            rod = Rod("growth_zone", fault, seed, size=size)
            rows, wf = rod_rows(rod)
            missing += sum(r.get("missing", False) for r in rows)
            ok = [r for r in rows if not r.get("missing")]
            if not ok or ok[0]["sequence"]:
                labels.append(f"| {rod.id()} | not run | - |")
                continue
            done += 1
            fail0 += not ok[0]["all_pass"]
            rem = ok[1:]
            passed += any(r["all_pass"] for r in rem)
            good_pass += any(r["all_pass"] and r["good"] for r in rem)
            lab, seq = label_rod([{"sequence": r["sequence"], "checks_pass": r["all_pass"], "good": r["good"]}
                                  for r in ok])
            labs.append(lab)
            labels.append(f"| {rod.id()} | {lab} | {' + '.join(seq) if seq else '-'} |")
            for r in rows:
                if r.get("missing"):
                    per.append(f"| {rod.id()} | {r['state']} | not run | | | | | | |")
                    continue
                per.append(f"| {rod.id()} | {r['state']} | " + " | ".join(cell(r, c) for c in CHECKS)
                           + f" | {r['regr_rms_pct_per_h']:.2f} ({r['limit']:.2f}) | "
                           f"{r['flank_difference_rms_pct_per_h']:.2f} | {'yes' if r['all_pass'] else 'no'} | "
                           f"{'yes' if r['good'] else 'no'} |")
            if wf is not None:
                wfl.append(f"| {rod.id()} | " + " | ".join(cell(wf, c) for c in CHECKS)
                           + f" | {wf['regr_rms_pct_per_h']:.2f} ({wf['limit']:.2f}) | "
                           f"{'yes' if wf['all_pass'] else 'no'} | {'yes' if wf['good'] else 'no'} |")
            out_json.append({"rod": rod.id(), "fault": fault, "size": size, "seed": seed, "label": lab,
                             "sequence": seq, "states": [{k: v for k, v in r.items() if k not in ("truth", "preprocess")}
                                                         for r in rows]})
        if done:
            summary.append(f"| {fault} | {size} | {fail0} of {done} | {passed} of {done} | {good_pass} of {done} | "
                           f"{'yes' if fail0 == done and good_pass >= 2 else 'no'} |")
        exp = EXPECTED[fault]
        exp_txt = exp["outcome"] + (f" after {exp['remedy']}" if exp.get("remedy") else "")
        by_label = sorted({"accept (repairable)" if x == "repairable" else "decline (not repairable)" for x in labs})
        d = sorted(set(labs)) != [("repairable" if exp["outcome"] == "accept" else "not repairable")]
        differ += [fault] if d else []
        cmp.append(f"| {fault} | {size} | {exp_txt} | {', '.join(f'{labs.count(x)} {x}' for x in sorted(set(labs)))} | "
                   f"{', '.join(by_label)} | {'yes' if d else ''} |")
    text = ("# Held-out faults: labels, seeds 0-2, approved sizes (tracker only, no agent)\n\n"
            "Spec 2026-10-12b item 3. Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and "
            "the fitting remedy gives three passes and a good measurement on at least 2 of 3 seeds; a rod is "
            "repairable if a state of at most two steps gives three passes and a good measurement. Good: approved "
            "tolerance (REGR limit in brackets, 2.5 % of the true peak; flank 1.00 %/h). " + THRESHOLD_NOTE
            + " States: the fitting remedies of `docs/proposals/2026-10-12_heldout-faults.md`, open item 3. "
            "Unremedied runs from the held-out size sweep (`staging/tracks_heldout`).\n\n"
            "Expected outcome (proposal section 2) against the labels. Where they differ the label wins (spec "
            "2026-10-12b):\n\n" + "\n".join(cmp)
            + f"\n\nFaults whose labels differ from the expected outcome: {', '.join(differ) if differ else 'none'}.\n\n"
            + "\n".join(summary) + "\n\nLabels (from these states only):\n\n" + "\n".join(labels)
            + "\n\nPer run (F = fails the approved threshold):\n\n" + "\n".join(per)
            + "\n\nNot a label state: the width-free ratio on the unremedied run (plane sections skipped; good = centre "
              "error within its limit). An agent that applies `use_width_free_ratio` and accepts is scored on this "
              "measurement:\n\n" + "\n".join(wfl) + "\n")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "labels.md").write_text(text)
    (out / "labels.json").write_text(json.dumps(out_json, indent=1, default=float))
    print(text)
    if missing:
        print(f"MISSING: {missing} state(s) not run")


def runner():
    return RemoteRunner(config(), cache=CACHE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "stop", "fetch", "eval"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.cmd == "eval":
        if not a.out:
            ap.error("eval needs --out")
        evaluate_all(a.out)
        return
    if a.cmd == "start":
        p = plan()
        n = sum(2 * len(x["runs"]) for x in p["rods"])
        if a.dry_run:
            print(f"{len(p['rods'])} rods, {n} tracker runs")
            for x in p["rods"]:
                print(x["id"], [r["tag"] for r in x["runs"]])
            return
        runner().sweep_start(p, NAME, tracks=TRACKS)
        print(f"started: {len(p['rods'])} rods, {n} tracker runs")
        return
    r = runner()
    if a.cmd == "status":
        st = r.sweep_status(NAME)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "stop":
        print(json.dumps(r.sweep_stop()))
    else:
        cache = r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched to {cache.relative_to(ROOT)}: {len(list(cache.glob('*__*.npz')))} files")


if __name__ == "__main__":
    main()
