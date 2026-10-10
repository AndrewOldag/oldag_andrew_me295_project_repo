# Spec: width-change size, whole-rod rotation, strongly bent rods

From: planning account. Date: 2026-10-10. Status: open. All three parts requested by Andrew.

## Review of build session 5
- Read: running log, decisions, results in `results/2026-10-10_checker_synthetic/`, `measure/rod.py`, `measure/render.py`, `checker/checks.py`
- Andrew approved the thresholds on 2026-10-10: rigid_invariance 2.0 %/h and closure 1.0 px/h as proposed, plane_sections 3.25 %/h (proposed 3.0; raised because the clean maximum is 2.36). `config/checker_thresholds.yaml` is marked approved
- Andrew's answers to the two open points are parts A and B below

## Order
- Parts A and B first, then item 5 of the 2026-10-09 spec
- Part C at any time before item 6 of that spec. The thresholds are frozen there, and these cases are part of the basis
- About 50 tracker runs in total

## A. Width change, larger injection
- Decision: try a slightly larger injected change and see whether the plane-sections check separates it. The check itself is not changed
- Now: curvature 1/800 per px, flank spacing growing 40 %/h, true residual 1.5 %/h, measured 1.93-2.33 %/h
- Run two sizes, 3 seeds each, each tracked twice as before. Keep the spacing rate at 40 %/h and raise the curvature:
  - curvature 1/400 per px, true residual 3.0 %/h
  - curvature 1/267 per px, true residual 4.5 %/h
- Report per size: the plane-sections value for each seed, where it peaked, and whether it is above 3.25 %/h. Report the other two checks as well
- Do not pick the size. Andrew picks it from the table. The fault list is unchanged

## B. Whole-rod rotation is flagged
- Decision: closure keeps the assumption that the basal tissue is fixed in the world. A whole rod turning about a point basal to the most basal tracked point is a failed measurement, and closure is the check that flags it
- This reverses the reading in the session 5 results, where `rigid_rotation` was listed with the clean cases. Its closure value of 5.6 px/h is a correct failure
- Work:
  - Field level: add a case in which the rod turns about a point basal to the last chain point (the existing `rigid_rotation` turns about the last chain point, so closure passes there). Expected: closure fails, the other two pass
  - Image level: `rigid_rotation` is expected to fail closure and pass the other two. Add that expectation to the evaluation script and a test
  - Report the closure value against rotation rate for three rates at the existing geometry: 0.1, 0.03 and 0.01 degrees per frame, 3 seeds each. State the slowest rate that is flagged at 1.0 px/h. The value should be near the rotation rate times the distance from the pivot to the basal tracked point
- Remove `rigid_rotation` from the clean group in the results tables and in the basis comment of the thresholds file. The clean basis is then 15 rods. The rigid_invariance clean maximum becomes 1.04 %/h (was 1.08); the closure and plane_sections maxima do not change
- This is a checker test only. No fault name, remedy or injector for rotation is added. `fast_rotation` stays held out for the diagnostician

## C. Strongly bent rods
Why:
- The existing `bending` case turns about 3 degrees in the hour. Its flank difference at the peak is 1.8 %/h, below the clean plane-sections value. It does not test a rod that is visibly bent
- Real roots in the drought and recovery movies bend. Bending is not induced there but it occurs

Both are clean cases, not faults. Both use the `growth_zone` velocity field and constant width. Both start bent. Curvature is carried by the material, so a bend that has left the growth zone stays.

- `bend_continue`: a bent rod that keeps bending the same way
  - Starting bend in `kappa0`: Gaussian in X, centred at 150 px, sigma 40 px, turning angle 30 degrees (peak curvature 5.22e-3 per px, radius 191 px)
  - Curvature rate: same sign, Gaussian in s, centred at 150 px, sigma 40 px, 30 degrees per hour. Flank difference at the peak 15.7 %/h
- `bend_reverse`: a bent rod that then bends the other way and ends S-shaped
  - Starting bend in `kappa0`: Gaussian in X, centred at 300 px, sigma 30 px, turning angle 30 degrees. This is basal to the growth zone (strain rate there is 5 % of the peak), so the bend is permanent
  - Curvature rate: opposite sign, Gaussian in s, centred at 150 px, sigma 40 px, 45 degrees per hour. Flank difference at the peak 23.5 %/h
- Expected: all three checks pass in both cases

Planning account trial, field level, existing code, not committed:

| Case | Turning angle at the start (deg) | Turning angle at the end (deg) | Largest curvature x half-spacing | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) |
| :-- | :-- | :-- | --: | --: | --: | --: |
| bend_continue | 30 | 77 | 0.15 | 0.0000 | 0.0000 | 0.22 |
| bend_reverse | 30 | 30 one way, then 53 the other | 0.12 | 0.0000 | 0.0000 | 0.12 |

- The plane-sections value is not zero at field level because the check uses the form without the curvature-squared term. That is expected
- The rod leaves a 320 px wide frame. The trial used 640 px wide with the base moved sideways
- In `bend_reverse` the old bend moves from s = 300 px to s = 360 px. Set the tracked length so the whole old bend stays inside it in every frame

Work:
1. Add both cases to `field_cases()` with the expected outcomes. Check: the field-level test passes for both, and integrated strain rate equals tip velocity to tolerance
2. Image level: 5 seeds per case, each tracked twice. Widen the frame so the whole rod is inside it in every frame; state the frame size and the tracked length
3. Report:
   - Centre strain-rate error against the truth, as for the clean cases
   - Plus and minus flank strain-rate error against the truth, separately. The flank difference is the signal here
   - The three check values, and where each peaked
   - A profile plot like `clean_profiles.png`, and one first-frame and last-frame image per case

## Results
- One new folder under `results/` for this spec. Do not overwrite `results/2026-10-10_checker_synthetic/`

## Stop and ask Andrew
- A clean bent rod exceeds an approved threshold. Report the values. Do not change a threshold or a check
- The tracker loses points or freezes them on a clean bent rod
- Any change to the fault, remedy or info lists. Nothing here adds to them

## Report back
- Log entry per the routine in `CLAUDE.md`, with a `Demo:` line for each part
- Note in the running log when this spec is done
