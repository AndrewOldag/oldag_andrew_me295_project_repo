# Fixes for the c033 audit findings, 2026-11-23 (task c036)

Inbox dispatcher item 61 (planning, Andrew approved the fixes). Findings: `results/2026-11-23_audit/`. Report-only: no committed outcome, label, threshold or scored result is changed. No cluster jobs, no LLM runs.

## S1-3, S1-4: real-root biology values at the tip
- `python scripts/mask_bio.py --apply` masked strain-rate, REGR, growth-zone, flank and velocity-profile values as `[masked]` in 61 tracked files: the real-movie result folders (the audit's list plus the same pattern in 2026-10-23_real_slice, real_slice_noagent, tracker_timing, 2026-10-24_real_slice, rigid_window, rigid_whole_pixel, closure_definition, real_calibration windows) and `docs/proposals/2026-10-23_real-midline-smoothing.md:7`. One prose value masked by hand (`rigid_whole_pixel/README.md:22`)
- Kept: check values, the predicted plane-sections term, run ids, dates, positions given as `s = ... px`
- Cause of S1-3: the report masker (`scripts/batch2_agents_report.py` `MASK_KEYS`, used by `run_all_report.py`) had no `strain_rate` key; added
- Test: `tests/test_no_real_bio_values.py` (4 tests) fails if a value under a biology key or after a biology word comes back in a real-movie file
- `python scripts/mask_bio.py` prints `0 files with values`
- Git history still holds the values; the rewrite is planned after c036 and c037

## S2-1: integrity gate
- `checker/checks.py` `track_integrity`: a frame with fewer than 3 tracked centre points (or no midline) is counted in a new value `integrity_lost_frames`, which fails when above 0; inversions and gaps are measured between tracked neighbours across lost points; with no measurable frame, inversions and gap ratio are NaN. `integrity_gate` fails any integrity value that is NaN. `relative_integrity` carries `integrity_lost_frames` of the remedied track
- Tests (`tests/test_integrity.py`, 5 new): frame with < 3 points, gap across lost points, inversion across a lost point, empty track (audit test D), NaN lateral
- Impact: `python scripts/integrity_impact.py --old-rev 24f64ed --cache c027=staging/c027/tracks --cache c029=<compound staging>/tracks_c029 --cache c029b=<compound staging>/tracks_c029b --cache freeze_v4=<compound staging>/tracks_freeze_v4 --out staging/c036/integrity`. Every cached remedied track gated against its window's base track (`st1`; `st12` on the c029 low_texture_fast rods) with the old and the new gate. Every remedy produces a tracked record, so the caches hold every remedied track. Run detached

| Set | Remedied tracks | Pass old -> new | Fail old -> new | Changed | Base tracks | Bases with lost points |
| :-- | --: | --: | --: | --: | --: | --: |
| c027 | 706 | 578 pass | 126 fail | 2 (fail -> pass) | 94 | 24 |
| c029 | 651 | 548 pass | 103 fail | 0 | 24 | 4 |
| c029b | 1311 | 1231 pass | 80 fail | 0 | 48 | 0 |
| freeze v4 | 151 | 118 pass | 33 fail | 0 | 42 | 3 |

- The 2 changed tracks: c027 window 0721_c3__w2-4, enlarge_patch 1.5x and 2x (`st1_r26`, `st1_r34`), used by the c027 remedy-tree baseline at steps 2 and 3 and rolled back for integrity (inversions ratio 1.75 and 4.25 against 1.5). With order measured across lost points the ratios are 1.14 and 1.49 and the gate passes. Closure after either remedy is 151.1 and 150.8 px/h against 19 (before 149.4), so the no-improvement rule would roll both back; the window's tree outcome (decline) is the same. Only the recorded roll-back reason would differ. The diagnostician did not apply a remedy on this window (declined at step 2)
- No base track has a lost frame. 2 remedied tracks have lost frames (c027 register_frames v1 tracks, 64 and 50 frames); both already failed the old gate
- Files: `integrity_impact_summary.json` (counts per set), `integrity_impact_changed.csv` (the 2 rows). Per-track table in `staging/c036/integrity/` (not committed)

## S3-1: real frame_quality reference
- `config/frame_quality_reference.yaml` `real:` recomputed from the 23 clean fq-real windows inside the current usable windows (0727_cc7 8.5-9.5 h left out; outside since 2026-10-23): 69 values. texture_contrast median 0.0648 -> 0.0641, focus median 0.0286 -> 0.0285; lowest unchanged (0.0439, 0.0213). Audit script `results/2026-11-23_audit/scripts/s3_fq_reference.py` gives the same values
- Impact: `python scripts/fq_reference_impact.py --traces c022=staging/c022 --traces c027=staging/c027/run/traces --traces c027_demo=staging/c027/demo/run/traces ... --out staging/c036/fq_impact.json`. An answer can read differently only where a frame value lies between the old and new median

| Set | frame_quality answers | Frames | Frames between old and new median |
| :-- | --: | --: | --: |
| c022 run4 | 1 | 3 | 1 (0714_c5~6-8__w6) |
| c027 run | 24 | 72 | 1 (0727_cc3__w22-23.63) |
| c027 demo | 2 | 6 | 0 |
| c027 held and paused traces (not scored) | 17 | 51 | 0 |
| c019 killed and stopped runs (not scored) | 2 | 6 | 0 |
| c026 | 0 | 0 | 0 |

- No outcome is recomputed. File: `fq_reference_impact.json`

## S6-3, S7-1, S7-2: READMEs and commands
- READMEs added: `results/2026-10-09_demo_diagnostician/`, `results/2026-10-12_heldout_faults/`
- `results/2026-10-10_width_rotation/README.md`, `results/2026-10-10_checker_synthetic/README.md`: full `run_batch.py` commands (`--work`, `--seeds`, `--moved-too`, case, fault, size)
- `results/2026-10-25_real_subset/README.md`: run, report and agreement commands use `staging/c019/real_subset_runs/run1..3` (restored from 035e8fc) and `--out` (new option in `real_subset_report.py` and `real_subset_agreement.py`). The report no longer writes REGR or growth-zone columns. Rerun on 2026-11-23: `windows.csv`, `tables.md` and `agreement.json` identical to the committed files

## Tests
- `python -m pytest -q tests`: 506 passed, 3 skipped (2026-11-23)
