# Checker on synthetic rods, 2026-10-10

Spec: `docs/specs/2026-10-09_checker-and-synthetic-rods.md`, items 3 and 4. Thresholds are proposed, not approved; no result here is scored.

## Files
- `field_level.md`: the three checks on the six field-level rods, with the expected outcome
- `image_level.csv`: one row per tracked image-level rod: truth error of the centre strain rate, the three check values and where each peaked
- `image_level.md`: the same, median [min, max] over seeds
- `clean_profiles.png`: tracked against true strain rate and flank difference, clean growth-zone and bending rods, 5 seeds each

## Runs
- 70 tracker runs, all completed: 4 clean cases x 5 seeds and 5 development faults x 3 seeds, each run twice (as rendered, and with a rigid motion of 0.1 deg/frame and (0.5, 0.3) px/frame added and not logged)
- Movie: 640 x 320 px, 41 frames at 90 s, rod radius 30 px, tip speed 60 px/h, peak REGR 43 %/h. Tracker: two-side, `track_centre=True`, disk radius 15 px, spacing 15 px, uncoupled. 6-7 s per tracker run; render 5-7 s (27-39 s for the 241-frame stride movie)
- Commands: `scripts/synth/run_batch.py` on the tracker machine, `scripts/synth/eval_rods.py --tracks <dir> --out results/2026-10-10_checker_synthetic` here

## Results
- Field level: all 18 check outcomes as expected. Clean values at most 0.002 %/h or 0.0000 px/h; width_change gives a 1.50 %/h plane-sections residual
- Clean image-level error (growth_zone and bending, 10 rods): RMS error of the window-mean REGR 0.40-0.44 %/h, max 1.00-1.42 %/h, against a 43 %/h peak
- Clean check values over 20 rods: rigid_invariance max 1.08 %/h; closure max 0.19 px/h (anchored cases); plane_sections max 2.36 %/h
- Faults (3 seeds each, min value):
  - rigid_drift: closure 16.3 px/h; the other two checks are at clean levels
  - displacement_exceeds_patch: all three checks fail (48 %/h, 19.8 px/h, 30.6 %/h)
  - midline_jitter: plane_sections 25.9 %/h, closure 2.2 px/h; strain rate itself unaffected
  - low_texture: all three fail (152 %/h, 4.5 px/h, 121 %/h)
  - width_change: plane_sections 1.93-2.33 %/h, inside the clean range (up to 2.36). Not detected

## Open points for Andrew
- `width_change` is not separable from clean noise at the injected size (curvature 1/800 px, flank spacing +40 %/h; true residual 1.5 %/h). Options: a larger injected change, or a plane-sections value averaged over a band of s instead of the pointwise maximum
- `rigid_rotation` (whole rod turning about a base outside the tracked length) fails closure at 5.6 px/h by construction: the basal tracked point moves. Closure assumes the basal tissue is fixed in the world
