# Spec: smoothing padding, flank tolerance, first diagnostician runs, coupling weight

From: planning account. Date: 2026-10-11. Status: open. Decisions by Andrew on 2026-10-11, on the two questions and the proposals of build session 8.

## Review of build session 8
- Read: running log, decisions, `results/2026-10-11_remedy_fixes/` (README, items 4, 6, 7), `measure/preprocess.py`, `config/scoring_tolerance.yaml`
- Items 1-5, 7 (uncoupled) and 8 are done. The item 6 stop was correct
- Shared-machine limits held: 356 runs, 19 min, 4 workers, 1 min load at most 6.03
- Coupled clean rods: peak REGR 31.9 against 43.4 %/h, yet closure is short by only 1.5-2.0 px/h of a 60 px/h tip path. So the integrated growth is nearly kept and the profile is spread along the root. That reads as smoothing along s, not as lost growth
- The bent clean rods pass every check but have flank-difference error up to 0.59 %/h, above the 0.5 tolerance. The tolerance basis did not include them

## Decisions
- `rigid_drift` size 0.5 approved
- `smooth_midline` padding is changed to a fitted line (question 1)
- The remaining coupled sweeps at the default setting are not run. A sweep of the coupling weight on clean rods replaces them (question 2)
- Flank-difference tolerance: the basis rule of 2026-10-10 is applied again with the bent rods in the clean set
- The system runs uncoupled until Andrew says otherwise. The approved thresholds and the clean basis are uncoupled

## Limits
- Every tracker run follows the shared-machine limits already in `scripts/synth/sweep.py`. Report the same numbers per sweep
- About 370 tracker runs in this spec. More than 1 h of wall time in total: stop and ask

## Work, in order

### 1. `smooth_midline` padding
- Now: both ends are padded by odd reflection about the end value. The first and last midline of the window keep their jitter, and closure depends only on those two
- Change: pad each end with a least-squares straight line fitted to the first or last few frames. State the number of frames and log it. Along s the padding stays as it is
- Sigmas and levels unchanged. New run tag, so older smoothed runs are not reused
- Tests:
  - the existing one: a jitter-free translating midline is unchanged to 0.01 px at both levels
  - new: a translating midline with independent sideways jitter in every frame. After smoothing, the jitter in the first and the last frame is lower than before. Report the ratio for both levels
- Re-run: clean `growth_zone` and `bending`, 3 seeds, light and strong. Stop if a clean rod fails an approved threshold
- Re-run: `midline_jitter` at 0.5, 1, 2 and 3 px, light and strong
- About 72 tracker runs
- Report as in `item4_clean.md` and `item4_faults.md`. Propose one `midline_jitter` size under the criteria of the 2026-10-10 spec, or state that none meets them. Do not adopt it
- This is the last change to this remedy. If no size meets the criteria after it, `midline_jitter` is recorded as not repairable and decline is its correct outcome

### 2. Flank-difference tolerance
- Rule, as on 2026-10-10: the largest clean value under any setting that keeps every clean run passing, rounded up to the next 0.25 %/h
- Clean set: `growth_zone`, `bending`, `bend_continue`, `bend_reverse`, 3 seeds each
- Settings: none, `enlarge_patch` 1.5x and 2x, `crop_or_mask` both modes, `register_frames`, `smooth_midline` light and strong (after item 1). The bent rods have only been run with no remedy: run them through the others. About 84 tracker runs
- Stop if a clean bent rod fails an approved threshold after a remedy
- If the rule gives 0.75 %/h, put it in `config/scoring_tolerance.yaml` as approved, with the date and basis. If it gives anything else, stop and ask Andrew
- Check the centre tolerance on the same runs: report the largest clean centre error as a fraction of the true peak. If it is above 2.5 %, stop and ask
- Recompute every label in `results/2026-10-10_repair_criteria/` and `results/2026-10-11_remedy_fixes/` under the new tolerance. Report each label that changes
- If `low_texture` at 0.2 or 0.25 now meets the criteria, propose it as the repairable size. Do not adopt it

### 3. Diagnostician runs, part D
- For the faults with an approved size: `displacement_exceeds_patch` 2x6, `width_change` 1/400, `rigid_drift` 0.5, `low_texture` 0.03. Seed 0, one run each, uncoupled
- `midline_jitter` waits for its size
- Report per run: outcome category, named fault, steps, roll backs, tokens, call time. Traces in `results/`
- At most 4 runs here. The limit of 8 in the 2026-10-10 spec still covers all of part D

### 4. Coupling weight
- First, find which arguments of the tracker set the strength of the coupling (the length penalty and the weighting by match quality). List them with their defaults in the results README
- If the strength cannot be set from `qb_track.py` without changing the tracker's own code, stop and tell Andrew. Do not edit the tracker repository
- Sweep the strength over six values: 0, then the default times 0.01, 0.03, 0.1, 0.3 and 1. If 0 is not allowed, use the uncoupled run in its place and say so
- Rods, 3 seeds each, each tracked twice as before: `growth_zone`, `bending`, `rigid_translation`, `bend_continue`, `bend_reverse`, and `growth_zone` at twice the tip speed (stride 1). About 216 tracker runs
- Report per value and rod group, coupled next to uncoupled:
  - peak REGR from the record and from the tracker's own output, against the truth; position of the peak; length of the zone above half the peak
  - centre REGR RMS error and flank-difference RMS error
  - the three check values and the number of runs failing an approved threshold
  - on `rigid_translation`: the apparent strain rate (the noise the coupling removes)
  - integrated strain rate against tip velocity
- State the range of values, if any, where every growing clean rod passes the approved thresholds and is within the tolerance
- State whether the loss at the peak is the same fraction at once and twice the tip speed
- Do not adopt a value. Do not change or propose thresholds. No claim about which mode is better
- Results go in `results/` as usual

## Not in this spec
- The freeze. It waits for the sizes of `midline_jitter` and a repairable `low_texture`, and for Andrew
- Coupled runs of the fault and remedy tables

## Stop and ask Andrew
- A clean rod fails an approved threshold after a remedy
- The basis rule gives a flank tolerance other than 0.75 %/h, or a centre error above 2.5 % of the peak
- The coupling strength cannot be set without editing the tracker
- Fault sizes, before use
- Any change to the fault, remedy or info lists

## Report back
- One new folder under `results/`, with a README and a table per item
- Log entry per the routine in `CLAUDE.md`, with a `Demo:` line for each item
- Note in the running log when this spec and `2026-10-11_remedy-fixes-coupled-mode-shared-compute.md` are done
