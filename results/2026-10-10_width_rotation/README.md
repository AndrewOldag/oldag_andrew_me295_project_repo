# Width-change size and whole-rod rotation, 2026-10-10

Spec: `docs/specs/2026-10-10_bent-rods-width-change-rotation.md`, parts A and B. Checks at the approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.

## Files
- `per_seed.md`: every run, the three check values, where each peaked, and fails
- `image_level.md`, `image_level.csv`: per group, median [min, max] over seeds
- `rotation.md`: closure against rotation rate
- `field_level.md`: field-level cases, including the new `rotation_basal_pivot`

## Runs
- 30 tracker runs, 0 failed, 0 frozen points: width_change at curvature 1/400 and 1/267 px (flank spacing +40 %/h), rigid_rotation at 0.1, 0.03 and 0.01 deg/frame; 3 seeds each, each tracked twice (as rendered and rigidly moved)
- Width-change movies 640 x 640 px (the curved rod leaves a 320 px frame); tracked length 400 px; render 21 s, track 7-8 s per run. Rotation movies 640 x 320 px as before
- Commands: `scripts/synth/run_batch.py --case growth_zone --fault width_change --width-kappa-inv K` and `--case rigid_rotation --rotation-deg R`, then `scripts/synth/eval_rods.py --tracks <dir> --out results/2026-10-10_width_rotation`

## A. Width change
| Curvature (1/px) | True residual (%/h) | plane_sections per seed (%/h) | Peak at s (px) | Above 3.25 |
| :-- | --: | :-- | :-- | :-- |
| 1/800 (session 5) | 1.5 | 2.33, 2.08, 1.93 | 55, 85, 305 | 0 of 3 |
| 1/400 | 3.0 | 4.30, 3.43, 3.55 | 55, 40, 155 | 3 of 3 |
| 1/267 | 4.5 | 6.04, 4.98, 5.15 | 55, 75, 420 | 3 of 3 |

- Other checks pass at both sizes: rigid_invariance 0.44-1.06 %/h, closure 0.06-0.10 px/h
- At 1/400 the smallest value, 3.43 %/h, is 0.18 above the threshold. Measured values sit about 0.4-1.3 %/h above the true residual, as for 1/800
- Four of six peaks are at s = 40-75 px, near the tip, where the clean maxima also sit
- Size not chosen here; Andrew picks it

## B. Whole-rod rotation
- Field level: `rotation_basal_pivot` (0.1 deg/frame about a point 200 px basal to the last chain point): closure 13.96 px/h = rate x 200 px; the other two 0.0000. `rigid_rotation` about the last chain point: closure 0.0000
- Image level, pivot 80 px basal to the basal tracked point:

| Rate (deg/frame) | Closure per seed (px/h) | Predicted, rate x 80 px (px/h) | Flagged at 1.0 px/h |
| --: | :-- | --: | :-- |
| 0.1 | 5.60, 5.55, 5.60 | 5.58 | 3 of 3 |
| 0.03 | 1.74, 1.68, 1.70 | 1.68 | 3 of 3 |
| 0.01 | 0.58, 0.54, 0.58 | 0.56 | 0 of 3 |

- Slowest rate flagged: 0.03 deg/frame (1.2 deg/h). At this geometry the threshold corresponds to 0.018 deg/frame; it scales inversely with the pivot distance
- rigid_invariance and plane_sections pass at all rates (max 1.15 and 0.96 %/h)
- `rotation.md` and `image_level.md` mark 0.01 deg/frame "0 of 3 as expected": `IMAGE_EXPECTED` says closure fails, and at this rate the motion is below the threshold. A detection limit, not a checker error
- Clean basis without rigid_rotation (15 rods, session 5 runs): rigid_invariance max 1.04 %/h, closure 0.19 px/h, plane_sections 2.36 %/h. `results/2026-10-10_checker_synthetic/` is unchanged
