# Closure cause ft vs ft2 on 0708_m12 4-6 h, and control-root candidates (inbox item 28)

2026-10-24. Diagnostic only: checker, thresholds and freeze v3 unchanged.

## (1) Does ft2 tip jitter explain closure 0.945 -> 4.52 px/h?
Command: `python scripts/closure_tip_compare.py --net ft <ft track> <ft net midline> --net ft2 <ft2 track> <ft2 net midline>` on the cached whole-pixel reference tracks of the 0708_m12 4-6 h window (uncoupled, every frame, L400). Output `closure_tip_compare.json`.

| | ft | ft2 |
| :-- | --: | --: |
| Closure, checker (px/h) | 0.945 | 4.521 |
| Tip jump frame to frame, median / p90 (px) | 2.00 / 4.58 | 2.00 / 4.30 |
| Pair residual \|r\|, median / p90 / max (px) | 1.67 / 4.67 / 7.07 | 1.91 / 4.34 / 7.25 |
| Closure with tip fitted in time, degree 1 / 2 / 3 (px/h) | 3.745 / 3.745 / 2.960 | 5.149 / 5.149 / 4.363 |
| Tip net change over the window (px, row, col) | -5.0, 189.0 | -5.0, 195.0 |
| Chain net change, tip relative to base (px) | -5.4, 187.2 | -5.5, 186.1 |

- The closure sum telescopes: only the first and last tip positions and the chain's net change enter it
- Tip jitter is the same for both nets. The ft2 frame-0 tip lies 5 px behind the ft tip (world col 1151 against 1156); this makes most of the difference
- With the tip noise removed by a fit, neither net closes: ft 2.96-3.75, ft2 4.36-5.15 px/h. The 0.945 with ft came from end-frame tip noise in its favour
- Jitter does not explain the change. Tip stabilization (`root_kinematics/qc_stabilize.py`) not applied; stopped as the item says
- Both nets: the tip moves 2-9 px more than the tracked chain over the window

## (2) Control-root candidates, ft2 tip confidence on 5 window frames (rule: median at least 0.5, at most 3)
Segmentation midline on the lab server (frame list); 5 frames copied to the workstation; `batch_midlines.py` tile mode, ft2, low 0.1 %, high 99.5 %.

| Root | Frames (TP) | Tip confidence | Median |
| :-- | :-- | :-- | --: |
| 0714_c10 | 144, 162, 180, 198, 215 | 0.080, 0.099, 0.313, 0.310, 0.414 | 0.310 |
| 0714_c11 | 144, 162, 180, 198, 215 | 0.070, 0.026, 0.026, 0.025, 0.028 | 0.026 |
| 0711_c2 | 160, 180, 200, 220, 239 | 0.305, 0.452, 0.457, 0.418, 0.391 | 0.418 |

- None reached 0.5. No full run; the 3-root agent run not repeated
- For reference, 4-6 h medians over the full window: 0708_m12 0.572, 0711_c1 0.176, 0721_m10 0.249
