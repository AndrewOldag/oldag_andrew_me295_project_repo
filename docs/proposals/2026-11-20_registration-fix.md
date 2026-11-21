# Proposal: register_frames fix and track-integrity check (spec 2026-11-20 R, task c031)

real-calib, 2026-11-20. Committed before any run. No stop for approval; nothing below changes after the first result is seen.

## Flagged window
- 0711_c5__w6-8 (batch 2, control), c027 run, decided by the diagnostician: closure 22.83 px/h (fail, gate 19) -> `register_frames` (tag `st1_reg2p1075`, band from 1075 px) -> 14.03 px/h (pass), accepted. Record kept in dispatcher's voided-register folder
- Registration report saved with the track: final rotation 9.23 deg, final shift 100.6 px, smallest pairwise ECC 0.967. No per-pair values were saved

## R1 Diagnosis
- On this machine (checker only, no tracker): track-integrity values (R3) of the base track and the registered track of the window
- One cluster CPU job through `scripts/retrack_queue.py` once it is on main: `scripts/remote/register_diag.py` on the window's frames and base midline, no tracking. Writes per pair t-1 -> t: rotation, shift, ECC; the chained path C_t; and each frame registered directly to frame 0 (same band, same mask rule): rotation, shift, ECC
- Reported: final rotation and shift of the chained and the direct fits; the per-pair rotation sum against the chained final; the drift that the closure miss allows (22.83 px/h x 2 h = 45.7 px). Answer: which of the two gives the 9.23 deg

## R2 register_v2
- `measure/preprocess.py` `register_frames_v2`: each frame t registered directly to frame 0 on the basal band of the frame-0 midline (band and edge rules as v1), ECC initialised from the fit of frame t-1. No chaining
- Plausibility bound: the last frame's fitted motion is not plausible if its shift exceeds 2 x the drift implied by the closure miss (closure px/h x window h) or its rotation exceeds 2 deg. Then the report says `plausible: false`; the integrity gate (R3) fails the track and the remedy is rolled back
- Settings: `TrackSettings.register_version` 2 and `register_max_shift_px` (from the record's closure when the remedy is chosen). Tag part `regv2p<from>b<bound>`; v1 tags (`reg2p<from>`) unchanged and never reused for a decision. `apply_remedy("register_frames")` gives v2 from now on
- Tests: chained vs direct on a synthetic image sequence with known rigid drift (direct recovers it, chaining error grows with frames); a pure-growth sequence gives near-identity; the bound trips on an injected 9 deg rotation

## R3 Track-integrity check (`checker/checks.py`, deterministic, no LLM)
- (a) inversions: per frame, centre points projected onto that frame's midline; count of neighbour pairs whose arc length does not increase from tip to base; summed over frames
- (b) gap ratio: per frame, largest centre-neighbour distance over the median; the largest over frames
- (c) lateral scatter: RMS perpendicular distance of centre points from the frame's midline, over all points and frames, px
- (d) for a registered track: the registration report's `plausible` (v2); v1 registered tracks have none and are reported as unknown
- Reported on every track. Gates only tracks made by a remedy: any value over its threshold, or `plausible: false`, fails. A separate function, not added to `run_checks`, so existing records, prompts and the checker output for base tracks do not change; dispatcher calls it at each remedy step

## R4 Thresholds (fixed rule)
- Set: freeze v4 rods (seeds 26-28), the 18 `accept_clean` base tracks (`<rod>__st1`) and the 9 `accept_repaired` tracks at their labelled repair setting; cached tracks only, no tracker run
- Value per track as defined in R3. Threshold = 99.5th percentile over the set x 1.5, rounded up to 2 significant figures; inversions threshold 0
- Computed and committed before any real window is checked with it. Then reported, for information only, on the batch-1 base tracks on this machine

## R5 Synthetic regression
- Freeze v4 rigid-drift rods (all sizes, seeds 26-28) retracked with `register_v2` on the cluster CPU through `retrack_queue.py`; repair outcome against truth (the freeze v4 rule) next to the old remedy's cached outcome
- Cost: one CPU task per rod and setting, 15 min limit; worst case printed and checked against the ledger before submit; stop at $15 total since 2026-10-23

## Not changed
- Closure threshold, real profile, prompts, other remedies, earlier records (c022, c026, c027 kept)

## Results
- `results/2026-11-20_registration_fix/`: README, diagnosis JSON (rotation, shift, ECC, integrity values only), thresholds, regression table
