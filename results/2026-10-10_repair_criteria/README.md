# Repair criteria: clean rods under each remedy, fault sizes, labels (no agent), 2026-10-10

Spec: `docs/specs/2026-10-10_repair-criteria.md`, parts A-C. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Nothing here is adopted: sizes and tolerance are proposals.

## Files
- `part_a.md`: clean growth_zone and bending, 3 seeds, each remedy setting alone
- `part_b.md`: fault sizes, summary then every run
- `part_c.md`: proposed tolerance and the labels from the part B states
- `runs.csv`: every evaluated run

## Runs
- 354 tracker runs, 0 failed, 1 h windows; 4 parallel workers, 52 min wall time (each run about 35 s with four running at once)
- Commands: `python scripts/synth/repair_sweep.py start|status|fetch`, then `python scripts/synth/eval_repair.py --out results/2026-10-10_repair_criteria`

## A. Clean rods under each remedy (stop condition met)
Clean runs that fail an approved threshold after a remedy applied alone:
- register_frames: closure 1.05-1.22 px/h, 0 of 6 pass. The remedy adds about 1.1 px/h of closure residual on a clean rod. Cause not yet found
- smooth_midline strong: closure 2.91-3.03 px/h, 0 of 6. light: closure 0.97-1.04 px/h, 3 of 6 pass. Likely cause: the smoothing over time pads the ends of the window with the end value, which shortens the net tip displacement by about the tip speed times the time sigma (3 frames x 1.5 px/frame at each end for strong). The closure check sees that shortfall
- change_frame_stride double (stride 2): growth_zone seed 2 rigid_invariance 23.2 %/h; the other 5 runs pass (0.78-1.02)
- enlarge_patch 1.5x and 2x, crop_or_mask both modes: all clean runs pass. enlarge_patch raises the REGR error (0.44 -> 0.55 -> 0.74 %/h). crop_or_mask leaves the run unchanged (no second object)

## B. Fault sizes
| Fault | Sizes tried | Meets the criteria | Note |
| :-- | :-- | :-- | :-- |
| displacement_exceeds_patch | tip speed x stride: 2x6, 3x4, 4x3 | 2x6 | 2x6: stride 6 -> 3 -> 1 (two halvings), three passes and good on 3 of 3; REGR error 0.95-0.99 %/h. 3x4 and 4x3 fail at stride 1 (rigid_invariance 30-125 %/h): growth 3-4 times faster than the clean basis is not tracked cleanly even every frame |
| rigid_drift | factor 0.25, 0.5, 0.75, 1 | none | after register_frames, closure 1.25-1.37 px/h at every size: above the 1.0 threshold by about what registration adds to a clean rod (part A) |
| midline_jitter | 0.5, 1, 2, 3 px | none | 0.5 px: 1 of 3 repaired by light smoothing. Strong smoothing fixes plane_sections at 0.5-1 px but fails closure (about 3 px/h, part A) |
| low_texture | contrast 0.03, 0.06, 0.1, 0.15 | none | 0.15 with patch 2x: rigid_invariance 2.37-3.19 %/h, still above 2.0. Milder sizes (contrast 0.2-0.25; clean is 0.30) not tried |
| width_change | 1/400 (unchanged) | yes | use_width_free_ratio: rigid_invariance and closure pass, plane_sections skipped, REGR error 0.40-0.45 %/h, 3 of 3 |

## C. Tolerance and labels
- Proposed tolerance: centre REGR RMS error <= 1.0 %/h, flank-difference RMS error <= 0.5 %/h. Basis: largest clean values 0.77 and 0.37 %/h under the settings that keep every clean run passing (unchanged, enlarge_patch 1.5x and 2x, crop_or_mask both), rounded up to the next 0.25 %/h
- The repaired 2x6 rods are within it by 0.01-0.05 %/h; their tip speed is twice the clean basis
- Labels at the sizes tried: `repairable` for displacement_exceeds_patch 2x6 (all seeds; two halvings), width_change (all seeds; use_width_free_ratio), midline_jitter 0.5 seed 1 (light smoothing). All other rods `not repairable`. Labels use the fitting remedy's states only
- Outcome categories, labels and diagnosis scoring: `measure/score.py`, `tests/test_score.py` (one test per table row)
