# Freeze v3.1: sizing for accept_repaired rods that need their repair (ended at the stop rule)

Spec `docs/specs/2026-10-24_freeze-v3.1.md`. Session freeze-v31, task c014. Ended by Andrew on 2026-10-24 (option a, inbox freeze-v31 item 8): no label sweep, no tag `freeze-v3.1`, no method runs. v3 (`results/2026-10-23_freeze_v3/`) stays the scored set. Driver `scripts/synth/scored_v31.py` (the v3 driver, pointed at a new cache and rod set).

## Files
- `sizing.md`: rule parts per fault and size, and every evaluated state (checker values, errors against truth)
- `second_root.md`: cause of 0 correct on second_root in v3, and the alternative-repair counts
- `cache_match.md`: workstation against the v3 lab-server outputs

## Rule (spec)
A fault size qualifies if, on 3 of 3 sizing seeds (10, 11, 12): (1) a listed check fails on the unremedied run; (2) the unremedied measurement fails the scoring tolerance (centre RMS above 2.5 % of the true peak, or flank-difference RMS above 1.00 %/h); (3) a remedy state of the v3 label sweep passes every check and is good. Smallest qualifying size; at most 6 sizes per fault. Stop for Andrew if fewer than 3 faults qualify.

## Faults and sizes
- rigid_drift: factor 0.5-5.5 in steps of 1 (1 = the 2026-10-10 drift). Remedy register_frames
- bad_stage_correction: 3-8 px in steps of 1 px. Remedy register_frames
- stage_log_missing: 1 (the v3 size; the largest, no stage move logged). Remedy register_frames
- width_change: one size at v3 geometry. Remedy use_width_free_ratio
- displacement_exceeds_patch: 2x2, 2x3, 2x4 (speed 2, stride 2-4). Remedy change_frame_stride/half, at most two steps, from the rod's own stride
- Steps approved by Andrew (inbox item 4). Checker, thresholds, remedies, tolerance and rod geometry are the v3 ones

## Per-seed outcome
Each cell: rule part (1) check fails, (2) unremedied not good, (3) a remedy repairs (y, n; - = not run: part 1 or 2 already failed on some seed, or a smaller state decided the fault).

| Fault | Size | s10 | s11 | s12 | Qualifies |
| :-- | :-- | :-- | :-- | :-- | :-- |
| rigid_drift | 0.5 | y n - | y n - | y n - | no |
| rigid_drift | 1.5 | y n - | y n - | y n - | no |
| rigid_drift | 2.5 | y n - | y n - | y n - | no |
| rigid_drift | 3.5 | y n - | y n - | y n - | no |
| rigid_drift | 4.5 | y n - | y n - | y n - | no |
| rigid_drift | 5.5 | y n - | y y - | y y - | no |
| width_change | one size | y n y | y n y | y n y | no |
| bad_stage_correction | 3 | y n - | y n - | y n - | no |
| bad_stage_correction | 4 | y n - | y y - | y n - | no |
| bad_stage_correction | 5 | y y y | y y n | y y n | no |
| bad_stage_correction | 6 | y y - | y y - | y y - | not run (part 3) |
| bad_stage_correction | 7 | y y - | y y - | y y - | not run (part 3) |
| bad_stage_correction | 8 | y y - | y y - | y y - | not run (part 3) |
| stage_log_missing | 1 | y n - | y n - | y n - | no |
| displacement_exceeds_patch | 2x2 | y y n | y y n | y y n | no |
| displacement_exceeds_patch | 2x3 | y y n | y y n | y y n | no |
| displacement_exceeds_patch | 2x4 | y y n | y y n | y y n | no |

- bad_stage_correction 5 px after register_frames: s10 passes and is good; s11 fails all three checks and is not good; s12 is good but rigid_invariance is 3.02 %/h (threshold 2.0)
- displacement_exceeds_patch at stride 1: rigid_invariance fails on every seed (35-55 %/h at 2x2); the field is good on 2 of 3 seeds at 2x2
- Registration at 6-8 px was not run: with at most 1 of 5 faults able to qualify, the stop rule holds whatever it gives

## Finding (`docs/decisions.md`, 2026-10-24)
- As run: none of the 5 faults met the rule on 3 of 3 seeds at the sizes tested; fewer than 3 of 5 can qualify, so the stop rule holds. This is narrower than "no fault is both harmed and repaired":
  - bad_stage_correction 5 px: register_frames repaired seed 10; seed 12 was good after it but failed rigid_invariance (3.02 against 2.0 %/h); seed 11 was not repaired
  - bad_stage_correction 6-8 px: register_frames was not run, so these sizes are untested for part 3
- Small faults (rigid_drift to 4.5, bad_stage_correction to 3-4 px, stage_log_missing, width_change) fail a check but leave the field within tolerance: accepting without a remedy gives a good field. Large faults (bad_stage_correction from 5 px, displacement_exceeds_patch) degrade the field, and the listed remedy does not repair them on every seed
- The paper's claim stays on accept versus decline (v3 false accepts: script 18, remedy tree 4, LLM methods 0). Repair skill is a stated limit

## second_root (v3 traces, `second_root.md`)
- Unremedied, only plane_sections fails (4.79-9.89 %/h); the centre is good, the flank difference is not. Both crop_or_mask states give the same values as the unremedied run
- After `use_width_free_ratio` (plane_sections skipped, flank error not scored) every applied check passes and the centre is good, so methods accept: accept_on_decline, not counted correct (label kept, Andrew 2026-10-13)
- Alternative repair (accept, width-free, good): remedy tree 3 of 3, diagnostician 9 of 9, single agent 6 of 9. Script: 3 false accepts (unremedied, flank not good)

## Tracker runs and storage
- 121 tracker runs logged, 0 failed (cap 300): sweep 1 on the lab server 13 (stopped by the 10 GB work-space limit, status `projected_space`); sweep 2 on the workstation 102; sweep 3 on the workstation 6. 120 distinct outputs (sweep 2 reran the partner of one pair sweep 1 had left half done). Plus 2 cache-match runs
- States already in the v3 cache (bad_stage_correction 3, stage_log_missing 1 on seeds 10-12) were reused, not rerun
- After the move (Andrew, 2026-10-24): lab server for storage only. Cache-match test passed first: renders byte-identical (44 of 44 files), tracks within 3.4e-13 px
- Storage: the task's c014 folder on the lab server holds the tracker outputs, plans, logs and the rods' truth, midline and marker files: 464 files, count and sha256 equal to the workstation copies
- Renders: after that check, the workstation render files of the 78 sweep rods were deleted under Andrew's one exception (3,660 files, 1.74 GB), each logged with time and size; the log is also stored on the lab server. The 2 cache-match rods' renders remain. Nothing else deleted
- Workstation after: work folder 14 GB of the 20 GB cap; 32 GB free on the disk
