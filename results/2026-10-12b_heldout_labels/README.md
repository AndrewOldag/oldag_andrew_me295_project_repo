# Held-out fault labels, seeds 0-2, approved sizes, 2026-10-12

Spec `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md`, item 3. Tracker only, no agent. Committed before any agent run on a held-out fault.

## Files
- `labels.md`: expected outcome against the labels, summary, labels, per-run checks and errors, width-free cross-check
- `labels.json`: per rod, label, repairing sequence and every state's values
- Commands: `python scripts/synth/heldout_labels.py start`, `status`, `fetch`, then `python scripts/synth/heldout_labels.py eval --out results/2026-10-12b_heldout_labels`

## Sweep
- 15 rods, 42 remedied states, 84 tracker runs (each with its moved copy), 0 failed. Unremedied runs reused from the held-out size sweep
- 212 s wall, 4 workers, 2.8 s per run. Load (1 min) 0.39 before, 5.71 max, 5.42 after, on 32 cores. Work space 7.28 -> 7.30 GB
- States: register_frames on fast_rotation and bad_stage_correction; crop_to_main_root and mask_second_root on second_root; enlarge_patch 1.5x and 2x, change_frame_stride double, and double then 1.5x or 2x on flank_swap and partial_occlusion

## Labels

| Fault | Size | Expected (proposal) | Label, seeds 0-2 | Correct outcome | Differs |
| :-- | :-- | :-- | :-- | :-- | :-- |
| second_root | 30 px | decline | 3 not repairable | decline | |
| fast_rotation | 2 deg/frame | accept after register_frames | 3 not repairable | decline | yes |
| bad_stage_correction | 3 px | accept after register_frames | 3 repairable (register_frames) | accept | |
| flank_swap | 0.5 | decline | 3 not repairable | decline | |
| partial_occlusion | 20 px | decline | 3 not repairable | decline | |

- fast_rotation: register_frames leaves all three checks failing on 3 of 3. Seed 0: rigid_invariance 58.6 -> 706.0 %/h, REGR error 11.4 -> 148.8 %/h. Seeds 1-2 change little. The label wins (spec); size unchanged
- bad_stage_correction: register_frames gives three passes and a good measurement on 3 of 3
- partial_occlusion: one seed reaches three passes after a remedy, with the centre error outside the limit; no state is good
- Not a label state: `use_width_free_ratio` on the unremedied second_root rods skips plane sections, the other two checks pass and the centre error is within its limit on 3 of 3 (0.48, 0.72, 0.83 %/h; limit 1.08). Under the repair criteria with any listed remedy, second_root would be repairable in one step. Labels here use the fitting states of the proposal, as the development labels did. For Andrew
