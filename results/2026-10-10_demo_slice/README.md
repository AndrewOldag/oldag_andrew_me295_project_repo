# Demo slice and remedy sweep, 2026-10-10

Spec: `docs/specs/2026-10-09_checker-and-synthetic-rods.md`, item 5. Thresholds approved (2.0 %/h, 1.0 px/h, 3.25 %/h).

## Files
- `trace.jsonl`, `summary.json`: `python scripts/demo_slice.py --fault displacement_exceeds_patch` (growth_zone rod, seed 0)
- `remedy_sweep.jsonl`: each development fault (seed 0) with its natural remedy applied by hand, no agent. Error = window-mean REGR RMS against the truth, %/h

## Demo slice
- Truth: growth zone, peak REGR 43.4 %/h at 316 um, no flank difference. Injected: frame stride 12 (tip moves 18 px per analysed pair; disk radius 15 px)
- Initial run: all three checks fail (47.98 %/h, 51.38 px/h, 32.79 %/h). REGR error 11.37 %/h RMS
- Diagnostician, 8 steps (the step limit), 0 failed steps, 8 calls, 35.9k input and 3.7k output tokens, 43.7 s call time:
  1. displacement_vs_patch_radius, then change_frame_stride half (12 -> 6): closure 51.4 -> 4.37 px/h
  2. check_report, frame_quality, stage_log_summary, midline_jitter, velocity_profile
  3. register_frames (named fault rigid_drift): no check passes
- Final run (stride 6, registered): REGR error 5.51 %/h RMS. Outcome `step_limit`, scored as not reported (spec item 6)

## Remedy sweep (no agent)
| Fault | Run | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR error (%/h) |
| :-- | :-- | --: | --: | --: | --: |
| displacement_exceeds_patch | stride 12 | 47.98 | 51.38 | 32.79 | 11.37 |
| | stride 6 | 51.08 | 4.37 | 33.62 | 3.87 |
| | stride 3 | 17.22 | 3.54 | 4.84 | 1.43 |
| rigid_drift | as injected | 0.49 | 16.27 | 1.39 | 0.41 |
| | register_frames | 0.92 | 1.26 | 2.91 | 0.51 |
| midline_jitter | as injected | 0.58 | 2.24 | 35.34 | 0.80 |
| | smooth_midline light | 0.84 | 2.02 | 21.95 | 0.56 |
| | smooth_midline strong | 0.75 | 2.98 | 8.79 | 0.68 |
| low_texture | as injected | 255.39 | 5.51 | 157.29 | 16.14 |
| | enlarge_patch 1.5x | 88.59 | 0.63 | 66.46 | 11.80 |
| | enlarge_patch 2x | 64.55 | 2.66 | 56.81 | 8.06 |
| width_change (1/400) | as injected | 1.06 | 0.07 | 4.30 | 0.40 |
| | use_width_free_ratio | not available | | | |

- Every remedy moves the failing check in the right direction and lowers the error, except the second enlarge_patch step on closure. None brings a fault to three passes
- The displacement_exceeds_patch movie is 241 frames (6 h); at stride 3 the window is 6 h long, against 1 h for the clean basis. Part of what remains may come from the longer window, not the stride
- No remedy setting was changed after these results
