# register_frames fix and track-integrity check (spec 2026-11-20 R, task c031)

2026-11-20 to 2026-11-22. Proposal `docs/proposals/2026-11-20_registration-fix.md` (committed before any run). Cluster CPU jobs: R1 (1 job), R5 (1 array, 12 tasks). No tracker run on this machine, no LLM run.

## Flagged window
- 0711_c5__w6-8 (batch 2, control), c027: closure 22.83 px/h -> `register_frames` v1 (`st1_reg2p1075`) -> 14.03 px/h, accepted by the diagnostician; record voided by dispatcher (inbox 49)
- v1 report saved with the track: final rotation 9.23 deg, shift 100.6 px, smallest pair ECC 0.967. No per-pair values were saved

## R1 diagnosis
- One cluster CPU job (7841039, 2026-11-22) of `scripts/remote/register_diag.py` on the window's 80 frames, band from 1075 px; output `register_diag_0711_c5__w6-8.json` (md5 equal on cluster, storage and here). The staged root copy was then deleted on the cluster (5.3 GB, logged in DELETED.log)
- Chained (v1): its chain equals `register_frames` exactly; final rotation 9.23 deg = the sum of the 79 pair rotations (mean 0.117 deg, mean absolute 0.23 deg, largest 1.00 deg). Every pair fit converged (ECC min 0.967, median 0.977); pair band motion median 0.52 px, largest 1.53 px. No single bad pair: a small per-pair bias of one sign adds up
- Path of the chained rotation: 2.4 deg by frame 10, 5.1 by 20, 6.3 by 50, 9.2 by 70 (9.23 at 79). Band-centre motion of the last map 21.7 px (under the v2 bound: 91 px from the remedy, `regv2p1075b91`); rotation 9.23 deg (over the 2 deg bound)
- Correction (2026-11-22): the diagnosis job was run with a shift bound of 46 px (the drift the closure miss implies) instead of the remedy's 91 px (2 x that drift). Its `plausible: false` comes from the rotation bound, which does not depend on it; the outcome is the same with 91 px
- Direct to frame 0 (v2): erratic on frames 1-20 (-1.5 to 6.0 deg, ECC 0.88-0.97), then ECC fails on frames 21-80 (59 of 79 fits); the map stays at the frame-20 fit (6.02 deg, band motion 3.9 px). Report `plausible: false` (6.02 deg over 2 deg): v2 would roll this remedy back
- Answer: chaining gives the 9.23 deg. The direct fit does not find one rigid motion of the basal band over the window either; the band does not stay rigidly like itself relative to frame 0 for more than about 20 frames
- v2 counts a failed fit only as a missing ECC value (`per_frame.ecc` null); it is not part of the plausibility bound. Here the rotation bound trips anyway. Reported, not changed
- Integrity of the window's tracks on this machine (`flagged_window_integrity.json`):

| Track | Inversions | Gap ratio | Lateral, px |
| :-- | --: | --: | --: |
| base `st1` | 3 | 1.76 | 1.03 |
| `register_frames` v1 `st1_reg2p1075` | 798 | 6.43 | 15.26 |
| `register_v2` `st1_regv2p1075b91` | 1656 | 12.08 | 81.59 |

- The registered track lost point order in most frames; closure did not see it
- Synthetic evidence for the chaining cause (`tests/test_register_v2.py`, 24 frames, rotation 0.05 deg per frame plus shift, noise): direct fit error 0.03 deg, 0.04 px; chained v1 error 1.2 deg. Per-pair errors add up along the chain

## R2 register_v2
- `measure/preprocess.py` `register_frames_v2`: each frame fitted directly to frame 0 on the frame-0 basal band, started from the previous frame's fit. Report per frame: rotation, band motion, ECC
- Plausibility bound on the last frame: band motion over `register_max_shift_px` or rotation over 2 deg -> `plausible: false`. Band motion is the displacement of the band centre, not the translation term (a rotation about the image origin inflates that)
- `register_frames` remedy now gives v2 with bound ceil(2 x closure px/h x window h). Tag `regv2p<from>b<bound>`; v1 tags, args and settings dicts unchanged. Remedy description text unchanged
- `qb_track.py --register-version 2 --register-max-shift-px N`
- Tests: drift recovered (direct beats chained), pure growth near identity (under 0.05 deg, 0.3 px), 9 deg trips the bound, shift trips the bound. Run in the tracker env (OpenCV); 240 x 240 synthetic arrays, no tracking

## R3 integrity check
- `checker/checks.py` `track_integrity`, `integrity_gate`; no LLM. Separate from `run_checks`, so base records and prompts do not change
- inversions (neighbour pairs whose arc length along the frame's midline does not increase, summed over frames); gap ratio (largest over median neighbour distance, largest over frames); lateral (RMS distance from the midline); registration plausible (v2 report; unknown for v1)

## R4 thresholds (rule fixed in the proposal)
- Set: 27 freeze v4 tracks (18 accept_clean base, 9 accept_repaired at their repair), cached, no tracker run
- 99.5th percentile x 1.5, rounded up to 2 significant figures: gap ratio 2.4, lateral 0.081 px; inversions 0. `config/integrity_thresholds.yaml`, `thresholds.json`. Committed (4ec36af) before the batch-1 report
- Sanity check, batch-1 base tracks (115), information only (`batch1_base_integrity.json`):

| Value | Synthetic median / max | Batch-1 median | p95 | max | Batch-1 pass |
| :-- | :-- | --: | --: | --: | --: |
| inversions | 0 / 0 | 0 | 417 | 720 | 75 of 115 |
| gap ratio | 1.55 / 1.55 | 1.94 | 3.83 | 8.68 | 93 of 115 |
| lateral, px | 0.036 / 0.054 | 1.37 | 5.26 | 94.1 | 0 of 115 |

- With these thresholds 0 of 115 batch-1 base tracks pass all three. Applied as a gate, every remedied real track would be rolled back on lateral scatter alone. Synthetic midlines are the render's own; real midlines come from the net, so lateral scatter on real tracks includes midline error
- 40 of 115 base tracks have inversions; some have hundreds (point order already lost without any remedy)

## Integrity gate, option A (Andrew, 2026-11-21)
- The absolute thresholds above stay reported, not gating. The gate compares a remedied track with the window's own base track: ratios (inversions + 1), gap ratio, lateral; rolled back if any ratio exceeds its k, or the v2 registration is not plausible
- `checker/checks.py` `relative_integrity` (with `integrity_gate`); `config/integrity_relative_k.yaml`
- k by the same rule from the 9 freeze v4 accept_repaired tracks against their own base tracks (`relative_k.json`): inversions 1.5, gap ratio 1.5, lateral 3.0. Synthetic ratios: inversions 1.0 on all 9; gap ratio 0.995-1.0; lateral 1.0-1.95 (6 register_frames rods 1.24-1.95; 3 width-free rods 1.0, same track). Committed before any real remedied track was scored
- Check on register_frames v1 tracks of the c027 cache against their base tracks (`relative_check_v1.json`; no decision changed):

| Set | Pairs | Pass | Fail on inversions | on gap ratio | on lateral |
| :-- | --: | --: | --: | --: | --: |
| batch 1 | 7 | 1 | 6 | 2 | 3 |
| batch 2 | 37 | 16 | 20 | 18 | 19 |

- Flagged window under the gate (`flagged_window_gate.json`; v2 track from dispatcher's c027 cycle, cluster job 7859132 task 4, md5 checked at fetch and here):

| Track | Inversions ratio | Gap ratio | Lateral ratio | Registration plausible | Gate |
| :-- | --: | --: | --: | :-- | :-- |
| v1 `st1_reg2p1075` | 199.8 | 3.65 | 14.9 | not bounded (v1) | fail |
| v2 `st1_regv2p1075b91` | 414.3 | 6.85 | 79.5 | no (6.02 deg, bound 2 deg) | fail |

- v2 fails every ratio and the plausibility bound; both remedies are rolled back. Its 6.02 deg final rotation matches the R1 direct fit (6.02 deg). The window cannot be repaired by registration
- Over the 44 pairs: median ratio inversions 4.8, gap ratio 1.45, lateral 2.4

## R5 synthetic regression (2026-11-22)
- Rods: the 6 freeze v4 rods labelled accept_repaired with `register_frames` (rigid_drift z0.5, bad_stage_correction z3; seeds 26-28), each with its moved copy. Re-rendered on this machine; truth equal to the freeze v4 truth within 1e-12 (the re-render differs by about 1e-18)
- `register_v2` settings from `apply_remedy` on the cached unremedied run: band from 400 px; bound 17 px (rigid drift), 6 px (bad stage correction)
- 12 tracker runs on the cluster CPU, one array through `scripts/rod_jobs.py` (`scripts/synth/register_v2_regression.py`): 12 fetched, 0 failed, md5 checked; worst case $0.144
- Outcome by the freeze v4 rule; v1 tracks are the cached freeze v4 ones (`regression.md`, `regression.json`):

| Rod | v1 | v2 | v2 closure, px/h | v2 rigid invariance, %/h | v1 rigid invariance, %/h |
| :-- | :-- | :-- | --: | --: | --: |
| rigid_drift s26 | accept_repaired correct | not accepted | 0.20 | 2.75 (fail) | 1.69 |
| rigid_drift s27 | accept_repaired correct | accept_repaired correct | 0.22 | 1.53 | 0.80 |
| rigid_drift s28 | accept_repaired correct | accept_repaired correct | 0.13 | 1.98 | 1.08 |
| bad_stage s26 | accept_repaired correct | not accepted | 0.07 | 3.88 (fail) | 1.67 |
| bad_stage s27 | accept_repaired correct | accept_repaired correct | 0.04 | 1.71 | 0.80 |
| bad_stage s28 | accept_repaired correct | not accepted | 0.11 | 2.72 (fail) | 1.12 |

- v1 repairs 6 of 6; v2 repairs 3 of 6. v2 closure is lower than v1 on all 6; v2 rigid invariance (rod against its moved copy) is higher on all 6 and over the synthetic gate (2.0 %/h) on 3. All 12 measurements (v1 and v2) are good against truth; the 3 v2 rods are declined by the check, not by error
- All 6 v2 registrations plausible (rotation 0.002-0.41 deg, band motion 2.8-8.2 px, under the bounds); the option A gate passes all 12
- v2 fits a rotation of 0.36-0.41 deg on the rigid-drift rods. Not explained yet
- On real windows rigid invariance is reported, not gating (real profile), so this check does not decline real windows
- Known limit (Andrew, 2026-11-22: register_v2 kept as the registration remedy, fixed list unchanged): on the synthetic register rods v2 repairs 3 of 6 against 6 of 6 for v1, because rigid invariance against the moved copy is higher after v2. Listed as a failure mode for Lab report 4

## Commands
- `python -m pytest tests/test_integrity.py tests/test_executors.py` (agents env); `tests/test_register_v2.py` in the tracker env with the tracker on PYTHONPATH
- `python scripts/integrity_thresholds.py thresholds --cache <freeze v4 track cache>` -> gap ratio 2.4, lateral 0.081, inversions 0
- `python scripts/integrity_thresholds.py report --tracks <batch-1 tracks> --out <json>` -> 115 tracks, 0 pass all
- `python scripts/integrity_thresholds.py relative --cache <freeze v4 track cache>` -> k inversions 1.5, gap ratio 1.5, lateral 3.0
- `python scripts/integrity_thresholds.py pairs --pairs <csv: window, base, remedied, label> --out <json>` -> per pair ratios and gate
