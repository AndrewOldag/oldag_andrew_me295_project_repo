# Midline spline fit (proposal 2026-10-23, option 1): v3 synthetic validation

Command: `python scripts/synth/validate_midline_fit.py --cache <freeze-v3 tracker cache> --out results/2026-10-23_midline_fit_validation`. Rule fixed before any real result: residual = pixel quantization, 0.289 px rms (`measure/midline_fit.py`). Criterion: every checker value unchanged within 1e-3. Record-level: midlines of the tracked record and its rigidly moved twin replaced by the fit; no re-tracking.

## Result: FAIL
- 241 cached v3 runs (record + moved twin); 164 within 1e-3; 77 outside
- Largest change: closure 1.14 px/h, plane_sections 10.72 %/h, rigid_invariance 0
- 90th percentile change: closure 0.49 px/h, plane_sections 1.82 %/h
- 3 pass/fail flips: `v3_bend30_clean_s12` plane_sections 2.97 -> 3.63 (pass -> fail), and its r30 run 2.73 -> 3.38 (pass -> fail); `v3_growth_zone_midline_jitter_z3_s21` (midline_smooth light) closure 1.28 -> 0.42 (fail -> pass)

| Rod group | Runs within 1e-3 |
| :-- | --: |
| bend16, bend20, bend24, bend30 clean | 0/13, 0/13, 0/13, 0/15 |
| growth_zone width_change | 0/6 |
| growth_zone midline_jitter z3 | 0/15 |
| growth_zone fast_rotation z2 | 16/18 |
| growth_zone clean, still clean | 8/8, 8/8 |
| all other growth_zone faults (bad_stage_correction, displacement_exceeds_patch, flank_swap, low_texture, partial_occlusion, rigid_drift, second_root, stage_log_missing) | all within |

- Reading: the spline uses its whole residual budget also on a smooth curve (a noise-free 200 px arc moves up to 0.95 px at the ends, rms 0.29 px). Where curvature is the signal (bending, width change) the checker values change; on the midline-jitter fault the fit removes the injected fault. Straight growth-zone rods are unchanged
- As stated in the proposal, the option fails as written; the rule is not retuned. Not adopted

## Real window, for information only (provisional; option not adopted)
- 0708_m12, 4-6 h, net midline (fine-tuned net: provisional), same record-level fit: plane_sections 134 -> 36 (400 px), 216 -> 25 (700 px), 247 -> 31 (950 px) %/h; closure 0.945 -> 1.015, 1.476 -> 1.531, 2.261 -> 2.206 px/h
- Plane sections still about 10x its threshold with the fit
