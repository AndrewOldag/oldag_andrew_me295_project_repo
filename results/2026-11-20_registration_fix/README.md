# register_frames fix and track-integrity check (spec 2026-11-20 R, task c031)

2026-11-20. Proposal `docs/proposals/2026-11-20_registration-fix.md` (committed before any run). No tracker run, no cluster job, no LLM run so far.

## Flagged window
- 0711_c5__w6-8 (batch 2, control), c027: closure 22.83 px/h -> `register_frames` v1 (`st1_reg2p1075`) -> 14.03 px/h, accepted by the diagnostician; record voided by dispatcher (inbox 49)
- v1 report saved with the track: final rotation 9.23 deg, shift 100.6 px, smallest pair ECC 0.967. No per-pair values were saved

## R1 diagnosis (part done)
- Integrity of the window's tracks on this machine (`flagged_window_integrity.json`):

| Track | Inversions | Gap ratio | Lateral, px |
| :-- | --: | --: | --: |
| base `st1` | 3 | 1.76 | 1.03 |
| `register_frames` v1 `st1_reg2p1075` | 798 | 6.43 | 15.26 |

- The registered track lost point order in most frames; closure did not see it
- Per-pair and direct fits: `scripts/remote/register_diag.py`, written and tested (its chain equals `register_frames`), not run. Needs one cluster CPU job (see Open)
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

- Flagged window, v1: inversions ratio 199.8, gap ratio 3.65, lateral 14.9: fails. Its v2 track is not back yet (dispatcher's register_v2 retracks)
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
- On real windows rigid invariance is reported, not gating (real profile), so this check does not decline real windows. No change to v2 or to any threshold here (fixed remedy list); for Andrew

## Open
- R1 per-pair run: submitted 2026-11-22 (one CPU job, 45 min limit); result to fetch
- Flagged window v2 through the gate, once dispatcher's register_v2 track of it is fetched
- R5 result above: v2 repairs 3 of 6 synthetic rods against 6 of 6 for v1

## Commands
- `python -m pytest tests/test_integrity.py tests/test_executors.py` (agents env); `tests/test_register_v2.py` in the tracker env with the tracker on PYTHONPATH
- `python scripts/integrity_thresholds.py thresholds --cache <freeze v4 track cache>` -> gap ratio 2.4, lateral 0.081, inversions 0
- `python scripts/integrity_thresholds.py report --tracks <batch-1 tracks> --out <json>` -> 115 tracks, 0 pass all
- `python scripts/integrity_thresholds.py relative --cache <freeze v4 track cache>` -> k inversions 1.5, gap ratio 1.5, lateral 3.0
- `python scripts/integrity_thresholds.py pairs --pairs <csv: window, base, remedied, label> --out <json>` -> per pair ratios and gate
