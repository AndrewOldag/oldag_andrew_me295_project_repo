# Smoothing padding, flank tolerance, diagnostician runs, coupling weight, 2026-10-11

Spec: `docs/specs/2026-10-11b_padding-flank-tolerance-coupling-weight.md`. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Nothing proposed here is adopted.

Status: item 1 run and stopped (clean rods fail closure after strong smoothing). Items 2 and 3 not started: item 2 needs item 1, and item 3 follows. Item 4 done (it does not use any remedy).

## Files
- `b1_smoothing.md`: clean rods and `midline_jitter` with the fitted-line padding
- `b4_coupling_weight.md`: coupling weight, six values, six rod groups, next to uncoupled
- Commands: `python scripts/synth/fix_sweep.py start|status|fetch --part b_smooth|b_weight`, then `python scripts/synth/eval_fix.py --out results/2026-10-11b_padding_tolerance_coupling --parts b_smooth b_weight`

## Sweeps (shared-machine limits as before)
| Sweep | Runs | Failed | Wall (s) | Load 1 min before / max during / after | Peak workers | Projected after 10 runs (h) |
| :-- | --: | --: | --: | :-- | --: | --: |
| b_smooth (item 1) | 72 | 0 | 155 | 2.62 / 5.91 / 5.91 | 4 | 0.05 |
| b_weight (item 4) | 252 | 0 | 532 | 2.59 / 6.22 / 5.89 | 4 | 0.18 |

- 324 tracker runs, 11.5 min wall in total (limit 1 h). Work space 5.42 -> 5.62 GB. No sweep process left after either sweep

## 1. smooth_midline padding (stopped)
- Time padding: least-squares line fitted to the first or last `2 ceil(sigma_t) + 1` frames: 3 (light), 7 (strong). Along s unchanged. Run tags `mslight3`, `msstrong3`
- Tests: translating midline unchanged to < 0.01 px at both levels. Translating midline with one independent sideways shift per frame, 50 seeds: end-frame error after smoothing is 0.97 (light) and 0.73 (strong) of its value under the odd-reflection padding (which keeps the end frames as they are)
- Clean rods: light 6 of 6 pass. Strong 0 of 6: closure 1.55-1.60 px/h. Stop condition met
- Cause: the midline source is smoothed in image coordinates. The stage follows the tip in steps of 10.5 px every 7 frames, so the tip path in the image is a sawtooth. On growth_zone seed 0 a step falls at frame 34, inside the last 7 frames, and the fitted line is wrong. Net tip error over the window: 1.65 px/h smoothed in image coordinates, 0.00 px/h when the same midline is smoothed in world coordinates (image + stage log). Light (3-frame fit) passes on all 6
- The same issue sits under every version of this remedy: time smoothing across a stage step blurs the midline near the step. Odd reflection hid it in closure only because it kept the end frames
- `midline_jitter` with the new padding: no size meets the criteria (0.5 px: 1 of 3; 1-3 px: 0 of 3)
- Not changed: smoothing in world coordinates would be a further change to the remedy, and the spec says item 1 is the last. Question 1 below

## 4. Coupling weight
- Arguments of `two_side_tracking.pipeline.run_two_side` (no tracker code changed; passed through `qb_track.py --couple-lambda --couple-mu`):
  - `couple_lambda`, default 2.0: inextensibility weight, penalises the tangential (length-changing) relative motion of neighbouring points
  - `couple_mu`, default 2.0: smoothness weight, second difference of the displacements along the chain
  - `couple_aniso_ratio`, default 0.0 (off): drops a point's low-texture direction from the data term when its structure-tensor eigenvalue ratio is below this value. Not swept
  - The weighting by match quality is each point's structure tensor in the data term; it has no scalar weight
- Swept lambda and mu together at 0, 0.01, 0.03, 0.1, 0.3 and 1 times the defaults. 0 is allowed; coupled at 0 gives the uncoupled result exactly on all 18 rods
- Peak REGR, growth_zone (truth 43.4 %/h; record / tracker's own): uncoupled 42.4 / 43.3; x0.01 41.8 / 43.0; x0.03 41.0 / 42.4; x0.1 39.1 / 40.8; x0.3 35.9 / 37.7; x1 30.7 / 32.1. The peak stays at s = 150 px; the zone above half the peak widens from 120 px to 180 px. Integrated REGR stays 57.6-59.5 px/h against a 60 px/h tip path
- rigid_translation, apparent strain rate RMS: 0.19 %/h uncoupled, 0.16 / 0.13 / 0.08 / 0.04 / 0.02 at x0.01 / 0.03 / 0.1 / 0.3 / 1
- Approved thresholds: every growing clean rod passes at x0.01 and x0.03. At x0.1 one bend_reverse run fails plane_sections (3.64); at x0.3 bend_continue and bend_reverse fail plane_sections (3 of 3 each); at x1 every growing group fails closure
- Within the approved tolerance (centre 2.5 % of the true peak, flank 0.5 %/h): no value, uncoupled included, because bend_reverse has flank-difference error 0.51-0.59 %/h uncoupled (the item 2 question). Leaving bend_reverse aside: x0.01 is the only coupled value with every growing rod within tolerance; at x0.03 bend_continue flank error is 0.73-0.78 and the 2x-speed centre error 2.63-2.96 (limit 2.17)
- Loss at the peak, growth_zone at once and twice the tip speed: uncoupled 2.4 % and 3.4 %; x0.01 3.7 / 6.3; x0.03 5.6 / 9.6; x0.1 10.0 / 15.6; x0.3 17.2 / 23.7; x1 29.3 / 35.2. Not the same fraction: the loss is larger at twice the speed at every weight
- Integrated strain rate against tip speed is a like-for-like comparison on the straight rods only. On the bent rods the tip chord also carries the bending turn (116 and 136 px/h)
- No value adopted. No claim about which mode is better

## Questions for Andrew
1. Smooth the midline source over time in world coordinates (add the stage log, smooth, subtract)? It keeps the fitted-line padding and the sigmas. On growth_zone seed 0 it gives 0.00 px/h net tip error at both levels. Without it, `smooth_midline` strong fails closure on clean rods and cannot be used
2. Items 2 and 3 wait for the answer to 1 (item 2 runs the bent rods through `smooth_midline`)
