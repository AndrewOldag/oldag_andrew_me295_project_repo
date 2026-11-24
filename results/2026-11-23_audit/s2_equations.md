# Section 2: equations (c033)

Scope: `checker/checks.py` (HEAD e0d067d), `measure/score.py` (6a19514), `measure/metrics.py`, with `measure/record.py` (`derive`, `rigid_moved`), against `docs/decisions.md` (2026-10-10 checker definitions and later entries), `docs/context/measurement_record.md`, `docs/context/research_background.md`, specs, proposals (freeze v3 section 3, registration fix R3/R4), lab reports 1-3 and `config/`.

Numeric tests: `results/2026-11-23_audit/scripts/s2_equations_check.py` (synthetic rods with known answers; under 10 s) and `scripts/s2_integrity_recompute.py` (thresholds and k from committed rows). Existing tests: `pytest tests/test_checker.py tests/test_score.py tests/test_integrity.py tests/test_freeze_v3.py tests/test_check_profiles.py`: 79 passed, 9 s.

Counts: blocker 0, major 2, minor 4.

## Findings

### S2-1 (major): the integrity gate passes tracks whose centre points are lost
- Where: `checker/checks.py:196-197`, `:206-208`, `:191`, `:210`, `:247-250`, `:271` (e0d067d)
- Evidence:
  - A frame with fewer than 3 tracked centre points is skipped (`continue`); it adds no inversion, gap or lateral value
  - The gap ratio uses only neighbour pairs with both points tracked (`pair_ok`), so a gap across lost (NaN) points is never measured
  - With no usable frame, `ratio` keeps its start value 0.0 and inversions 0, lateral is NaN (`passed` None)
  - Test D (`s2_equations_check.py`): a track with 2 of 81 centre points tracked in every frame gives inversions 0 (pass), gap ratio 0 (pass), lateral NaN (not run); `integrity_gate` returns True
  - Same track as the remedied track against a good base under option A (`relative_integrity`, k from `config/integrity_relative_k.yaml`): ratios inversions 1.0, gap 0.0, lateral NaN; `integrity_gate` True
  - Spec 2026-11-20 R item 3 and proposal R3 (a) ask for point order "in every frame"; the gate exists to catch a remedy that lost the tissue (spec 2026-11-20 "Why")
- Not checked: whether any committed remedied track has frames with fewer than 3 tracked points or long NaN runs (tracks are not on this machine)
- Fix: count skipped frames and lost points as integrity values; treat a not-computable value on a remedied track as failing (as `checks_pass(not_computable_fails=True)` does for checks); measure gaps between tracked neighbours across lost points

### S2-2 (minor): inversion count includes ties from points clamped at a midline end
- Where: `checker/checks.py:174` (projection clamped to `u` in [0, 1]), `:202` (`~(np.diff(s_full) > 0)` counts equal arc length); `results/2026-11-20_registration_fix/README.md:51` (858ed31)
- Evidence:
  - Every centre point beyond the basal end of the frame's midline projects to the same arc length; each neighbour pair among them counts as an inversion. Lateral is then the distance to the midline end point, not a perpendicular distance as proposal R3 (c) states
  - Test D: a straight track in perfect order with the midline 20 points shorter than the chain gives 260 inversions (20 per frame, 13 frames) and fails the gate
  - The README reads "40 of 115 base tracks have inversions; some have hundreds (point order already lost without any remedy)". The count does not separate true order reversals from end-clamp ties. Not verified on the real tracks (not on this machine)
- Fix: exclude or report separately points whose projection is clamped at a midline end; recount the 40 batch-1 base tracks before the README states that point order was lost

### S2-3 (major): lab report 2 states plane sections on real windows is "about 10 times" its threshold; its own numbers give a far larger ratio
- Where: `docs/reports/2026-10-30_lab-report-2.md:55` (0060c20); source `docs/decisions.md:159`
- Evidence:
  - The median plane-sections value given on the same line, and in `results/2026-10-25_real_calibration/README.md:16` (41 windows), divided by the 3.25 %/h threshold is more than 70, not about 10
  - The single-window source (`docs/proposals/2026-10-23_real-midline-smoothing.md:7`) gives a range whose ratio to 3.25 is 40-76
  - No committed file gives a ratio of about 10
  - Graded major, not blocker: a descriptive ratio supporting a non-gating decision, not a scored result
- Fix: state the ratio from the calibration table, or drop "about 10 times"; correct `docs/decisions.md:159` the same way

### S2-4 (minor): decisions entry on real-window gating not marked superseded
- Where: `docs/decisions.md:159`
- Evidence: says "on real windows rigid invariance and closure gate". Superseded by `docs/decisions.md:141` and `:162` (closure the only gate). Code: `agents/executors.py` `CHECK_PROFILES["real"] = ("closure",)`; `config/checker_thresholds_real.yaml` `rigid_invariance: null`. Entry `:172` is marked "SUPERSEDED"; `:159` is not
- Fix: mark `:159` superseded by `:162`

### S2-5 (minor): scoring tolerance uses the true peak rounded to 0.1 %/h, so the centre limit is discontinuous near 0
- Where: `measure/score.py:74-77`, `truth_summary` rounding
- Evidence: test E: true peak 0.04 %/h rounds to 0.0 and gets the absolute no-growth limit 0.5 %/h; true peak 0.06 %/h rounds to 0.1 and gets 0.0025 %/h (200 times stricter). For standard rods the rounding moves the limit by at most 0.00125 %/h. No scored rod has a true peak in (0, 0.05) (the non-growing rod is exactly 0), so no label changes
- Fix: compute the limit from the unrounded peak and apply the absolute limit by rule (for example peak below a stated floor); or note the behaviour in `config/scoring_tolerance.yaml`

### S2-6 (minor): plane-sections relation in the founding spec has no sign and says "width"
- Where: `docs/specs/2026-10-09_checker-and-synthetic-rods.md:39`
- Evidence: "flank difference = width x material curvature rate". Code, `docs/decisions.md:17`, `docs/context/measurement_record.md` and `research_background.md:14` use flank difference = -(flank spacing) x material curvature rate. The code is right (test B); only the spec text differs
- Fix: none needed in the spec (historical); cite `docs/decisions.md:17` as the definition in the final report

## Checked, no finding
- Units: `PER_S_TO_PCT_PER_H = 3.6e5` (1/s x 3600 s/h x 100 %) correct; closure px/h from `frame_times_s` (s/3600); rigid invariance and plane sections %/h; `covered_um` and `peak_at_um` px x `pixel_um`. File `measure/record.py:16`, `checker/checks.py`, `measure/score.py`
- Uniform growth 20 %/h, straight rod, anchored base (test A): window-mean REGR 20.0000 %/h at every s; rigid invariance 5e-12 %/h after 5 deg/h rotation plus translation; closure 0; plane sections 0. 3 checks pass
- Uneven frame times (dt 150/300/600 s, test A2): REGR 20.0000 %/h at every s; closure 0. dt is per pair (`derive`), no frame-index-as-time error
- Closure sign and scale: unlogged rigid drift 5 px/h of the whole rod gives closure 5.0 px/h (test A3); midline tip drift 0.5 px per 300 s frame gives 6.0 px/h (test A4). Definition matches `docs/decisions.md:16`
- Closure is end-to-end: `|sum r|` telescopes, so alternating tip jitter with zero net gives 0 (test A5). As defined in decisions 2026-10-10; disclosed in lab report 1 (`docs/reports/2026-10-16_lab-report-1.md:176`)
- Closure on a whole-rod rotation about the frame-0 tip (5 deg/h): 69.8 px/h, fails (test C). Consistent with decisions 2026-10-10 (fixed-base assumption; rotation is a failed measurement)
- Plane sections, pure bending (test B, h 50 px, dkappa/dt 1/400 per px per h, no growth): kappa_rate measured 6.9446e-7 vs 6.9444e-7 /px/s; spacing 100.000 px; flank difference -25.13 %/h, predicted -25.00 %/h (= -2h dkappa/dt), residual 0.13 %/h (the ignored 1/(1 - kappa^2 h^2) factor, as stated in `measurement_record.md`). Reversed bend: +25.13 vs +25.00, residual 0.13. Flanks swapped: residual 50.1 %/h, fails. Sign convention (+N flank, kappa > 0 turns toward +N) consistent across `curvature_along`, `orient_flanks`, `plane_sections` and the synthetic truth (`measure/rod.py:176-177`)
- Rigid invariance: `rigid_moved` rotates about the frame-0 tip with time from frame 0 and leaves the stage log unchanged, as decisions 2026-10-10. Real-window profile window `coverage_s` per decisions 2026-10-24 (`docs/decisions.md:161`)
- `MIN_COVERAGE = 0.5` in `checker/checks.py:18` and `measure/score.py:11` default; matches `docs/decisions.md:18`
- Thresholds, code vs stated: `config/checker_thresholds.yaml` 2.0 %/h, 1.0 px/h, 3.25 %/h = decisions 2026-10-10 = lab report 1 line 31. `config/checker_thresholds_real.yaml` closure 19.0 px/h = decisions 2026-10-24 (`:173`) = lab reports 2 and 3. Pass rule `value <= threshold` everywhere
- Scoring tolerance: `config/scoring_tolerance.yaml` 0.025 x true peak, flank 1.0 %/h, no-growth 0.5 %/h = decisions 2026-10-11, 2026-10-12 (`:78`), 2026-10-23 (`:126`), freeze v3 proposal line 5. `measurement_good` uses `<=`; NaN error gives not good (test E)
- Width-free ratio: under `width_free` the flank term is skipped and the ratio is not scored; disclosed in freeze v3 proposal line 134
- Integrity thresholds and k recomputed from committed rows (`s2_integrity_recompute.py`): gap ratio 2.4, lateral 0.081 px, inversions 0 (27 tracks); k inversions 1.5, gap 1.5, lateral 3.0 (9 pairs). All match `config/integrity_thresholds.yaml`, `config/integrity_relative_k.yaml`, `docs/decisions.md:252`, `:260`
- `integrity_ratios`: (inversions + 1) ratio, gap ratio, lateral ratio, zero-base lateral floor `lateral_px` (decisions `:255`, `:263`); infinite ratio fails when k is set (`:271`). Equal tracks give 1.0, 1.0, and lateral 0/0.081 = 0 (test D)
- Metrics (`measure/metrics.py`) against freeze v3 proposal section 3, hand case of 6 runs (test F): class accuracies 0.5, 0, 0.333; balanced accuracy 0.278; overall 0.333; false-accept rate 1/3 of accepts; coverage 0.5; abstention precision 0.5, recall 0.333; unnecessary-decline rate 0.5, 0; all six categories counted once. All as defined
- Fleiss' kappa on the Fleiss (1971) worked example: 0.2099 (published 0.210)
- `agreement`: unanimity over rods with the full repeat count; rods left out counted; kappa over the six categories. As proposal section 3
- Metrics tests are in `tests/test_freeze_v3.py:176-234` (proposal named `tests/test_metrics.py`); present and passing
- Window ends: `scripts/remote/qb_track.py:109`, `real_midline.py:41`, `real_moved.py:194`, `register_diag.py:72` all select frames with `from_h <= t <= to_h` (both ends inclusive). Adjacent windows share the boundary frame; no frame pair is in two windows. Stride keeps `win[::stride]`; closure duration uses the kept frame times
- `agents/dispatcher.py:91` `frames` = (b - a) x 3600 / step_s counts frame pairs, one fewer than frames read; affects only the cost estimate (by one frame per window). Not a finding
- `checks_pass`: skipped and "reported, not gating" checks exempt; `not_computable_fails` per freeze v4 C3 (a). `label_rod`: at most two remedy steps, shortest first
- Not checked: pixel size across experiments (closure in px/h on real windows assumes one scale); real track files (not on this machine)
