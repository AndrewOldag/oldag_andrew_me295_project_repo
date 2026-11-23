# Held-out compound and novel faults: metrics

20 rods: accept_clean 4, accept_repaired 10, decline 6. LLM methods 3 repeats; values are the mean over repeats, (min-max) where they differ. Seeds 40-43, candidate v4 on, freeze v4 prompts. Definitions as freeze v4 (`docs/proposals/2026-10-23_freeze-v3.md`, section 3); code `measure/metrics.py`.

| Method | Runs | Balanced accuracy | Acc. accept_clean | Acc. accept_repaired | Acc. decline | Overall | False accepts | False-accept rate | Coverage | Abst. precision | Abst. recall | not_reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| script | 20 | 0.40 | 1.00 | 0.20 | 0.00 | 0.30 | 12.0 | 0.60 | 1.00 | - | 0.00 | 0 |
| remedy_tree | 20 | 0.77 | 1.00 | 0.80 | 0.50 | 0.75 | 4.0 | 0.24 | 0.85 | 1.00 | 0.50 | 0 |
| diagnostician | 60 | 0.60 (0.57-0.62) | 1.00 | 0.20 | 0.61 (0.50-0.67) | 0.48 (0.45-0.50) | 4.0 | 0.40 | 0.50 | 0.38 (0.33-0.40) | 0.61 (0.50-0.67) | 1 |
| single_agent | 60 | 0.43 (0.40-0.47) | 1.00 | 0.30 (0.20-0.40) | 0.00 | 0.35 (0.30-0.40) | 6.3 (6.0-7.0) | 0.48 (0.43-0.50) | 0.67 (0.60-0.70) | - | 0.00 | 20 |
| all_decline | 20 | 0.33 | 0.00 | 0.00 | 1.00 | 0.30 | 0.0 | - | 0.00 | 0.30 | 1.00 | 0 |
| all_accept | 20 | 0.40 | 1.00 | 0.20 | 0.00 | 0.30 | 12.0 | 0.60 | 1.00 | - | 0.00 | 0 |

## Agreement across repeats (LLM methods)

| Method | Rods | Unanimous | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |
| :-- | --: | --: | :-- | :-- | :-- | :-- | :-- |
| diagnostician | 20 | 19 | 0.95 | 1.00 | 1.00 | 0.83 | 0.955 |
| single_agent | 20 | 14 | 0.70 | 1.00 | 0.50 | 0.83 | 0.700 |

## Categories, remedies kept, unnecessary declines (summed over repeats)

| Method | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | accept_on_decline | Runs keeping a remedy, accept_clean | Unnecessary-decline rate accept_clean / accept_repaired | Fault named correct |
| :-- | --: | --: | --: | --: | --: | --: | --: | :-- | :-- |
| script | 6 | 12 | 0 | 0 | 0 | 2 | 0 | 0.00 / 0.00 | 0 of 20 |
| remedy_tree | 12 | 4 | 3 | 0 | 0 | 1 | 0 | 0.00 / 0.00 | 5 of 20 |
| diagnostician | 18 | 12 | 11 | 18 | 1 | 0 | 3 | 0.00 / 0.60 | 34 of 60 |
| single_agent | 21 | 19 | 0 | 0 | 20 | 0 | 7 | 0.00 / 0.00 | 11 of 60 |
| all_decline | 0 | 0 | 6 | 14 | 0 | 0 | 0 | 1.00 / 1.00 | 0 of 0 |
| all_accept | 6 | 12 | 0 | 0 | 0 | 2 | 0 | 0.00 / 0.00 | 0 of 0 |

## Per row of the set (correct runs / runs)

| Row | Class | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| drift_low_texture_mild | accept_repaired, decline | 0 / 3 | 3 / 3 | 3 / 9 | 3 / 9 |
| second_root_occlusion_mild | accept_repaired, decline | 0 / 4 | 0 / 4 | 0 / 12 | 0 / 12 |
| drift_jitter_mild | accept_repaired, decline | 1 / 3 | 2 / 3 | 5 / 9 | 0 / 9 |
| low_texture_fast_mild | decline | 0 / 1 | 1 / 1 | 3 / 3 | 0 / 3 |
| focus_drift | accept_clean, accept_repaired | 5 / 5 | 5 / 5 | 15 / 15 | 14 / 15 |
| illumination_flicker | accept_repaired | 0 / 4 | 4 / 4 | 3 / 12 | 4 / 12 |

## Cost (LLM methods, all repeats)

| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: |
| script | 20 | 20 | 0 | 0 | 0.0 |
| remedy_tree | 20 | 56 | 0 | 0 | 0.0 |
| diagnostician | 60 | 285 | 1355004 | 162532 | 1679.2 |
| single_agent | 60 | 394 | 1818016 | 213601 | 2274.7 |

## Per run

| Method | Rod | Repeat | Class | Status | Category | Named fault | Steps | Remedies | Centre RMS (tol) | Flank RMS |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: |
| script | v3_growth_zone_drift_low_texture_mild_s60 | 0 | decline | accept | false_accept | - | 1 | none | 1.168 (1.35) | 1.61 |
| remedy_tree | v3_growth_zone_drift_low_texture_mild_s60 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 0.727 (1.35) | 0.991 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s60 | 0 | decline | decline | correct_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.754 (1.35) | 1.108 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s60 | 1 | decline | decline | correct_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.754 (1.35) | 1.108 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s60 | 2 | decline | decline | correct_decline | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; frames registered on the non-growing tissue (from 425 px from the tip) before tracking | 0.727 (1.35) | 0.991 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s60 | 0 | decline | accept | false_accept | rigid_drift | 6 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking | 1.096 (1.35) | 1.447 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s60 | 1 | decline | accept | false_accept | rigid_drift | 6 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking | 1.096 (1.35) | 1.447 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s60 | 2 | decline | accept | false_accept | rigid_drift | 6 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking | 1.096 (1.35) | 1.447 |
| script | v3_growth_zone_second_root_occlusion_mild_s60 | 0 | decline | accept | false_accept | - | 1 | none | 3.041 (1.35) | 0.381 |
| remedy_tree | v3_growth_zone_second_root_occlusion_mild_s60 | 0 | decline | accept | false_accept | - | 1 | none | 3.041 (1.35) | 0.381 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s60 | 0 | decline | accept | false_accept | - | 1 | none | 3.041 (1.35) | 0.381 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s60 | 1 | decline | accept | false_accept | - | 1 | none | 3.041 (1.35) | 0.381 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s60 | 2 | decline | accept | false_accept | - | 1 | none | 3.041 (1.35) | 0.381 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s60 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 3.041 (1.35) | 0.381 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s60 | 1 | decline | accept | false_accept | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 3.041 (1.35) | 0.381 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s60 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 3.041 (1.35) | 0.381 |
| script | v3_growth_zone_drift_jitter_mild_s60 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.378 (1.35) | 0.239 |
| remedy_tree | v3_growth_zone_drift_jitter_mild_s60 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 0.636 (1.35) | 0.289 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s60 | 0 | decline | decline | correct_decline | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.446 (1.35) | 0.355 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s60 | 1 | decline | step_limit | not_reported | rigid_drift | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.355 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s60 | 2 | decline | decline | correct_decline | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.446 (1.35) | 0.355 |
| single_agent | v3_growth_zone_drift_jitter_mild_s60 | 0 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.355 |
| single_agent | v3_growth_zone_drift_jitter_mild_s60 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.355 |
| single_agent | v3_growth_zone_drift_jitter_mild_s60 | 2 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.446 (1.35) | 0.355 |
| script | v3_growth_zone_low_texture_fast_mild_s60 | 0 | decline | accept | false_accept | - | 1 | none | 19.393 (1.35) | 42.347 |
| remedy_tree | v3_growth_zone_low_texture_fast_mild_s60 | 0 | decline | decline | correct_decline | low_texture | 7 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking; rolled back: integrity: frames registered on the non-growing tissue (from 435 px from the tip) before tracking; frame stride 4 -> 2; frame stride 2 -> 1; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 0.804 (1.35) | 1.079 |
| diagnostician | v3_growth_zone_low_texture_fast_mild_s60 | 0 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| diagnostician | v3_growth_zone_low_texture_fast_mild_s60 | 1 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| diagnostician | v3_growth_zone_low_texture_fast_mild_s60 | 2 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| single_agent | v3_growth_zone_low_texture_fast_mild_s60 | 0 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| single_agent | v3_growth_zone_low_texture_fast_mild_s60 | 1 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| single_agent | v3_growth_zone_low_texture_fast_mild_s60 | 2 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.762 (1.35) | 28.434 |
| script | v3_growth_zone_focus_drift_z1.5_s60 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.602 (1.35) | 0.891 |
| remedy_tree | v3_growth_zone_focus_drift_z1.5_s60 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.602 (1.35) | 0.891 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s60 | 0 | accept_repaired | accept | good_report | low_texture | 5 | tracker disk radius 14 -> 21 px | 0.538 (1.35) | 0.62 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s60 | 1 | accept_repaired | accept | good_report | low_texture | 6 | tracker disk radius 14 -> 21 px | 0.538 (1.35) | 0.62 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s60 | 2 | accept_repaired | accept | good_report | low_texture | 5 | tracker disk radius 14 -> 21 px | 0.538 (1.35) | 0.62 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s60 | 0 | accept_repaired | step_limit | not_reported | width_change | 8 | tracker disk radius 14 -> 21 px; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.538 (1.35) | 0.62 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s60 | 1 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.602 (1.35) | 0.891 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s60 | 2 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.602 (1.35) | 0.891 |
| script | v3_growth_zone_illumination_flicker_z0.03_s60 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 0.935 (1.35) | 1.453 |
| remedy_tree | v3_growth_zone_illumination_flicker_z0.03_s60 | 0 | accept_repaired | accept | good_report | low_texture | 2 | tracker disk radius 14 -> 21 px | 0.631 (1.35) | 0.834 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s60 | 0 | accept_repaired | decline | unnecessary_decline | unknown | 6 | none | 0.935 (1.35) | 1.453 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s60 | 1 | accept_repaired | decline | unnecessary_decline | unknown | 7 | none | 0.935 (1.35) | 1.453 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s60 | 2 | accept_repaired | decline | unnecessary_decline | unknown | 7 | none | 0.935 (1.35) | 1.453 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s60 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.935 (1.35) | 1.453 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s60 | 1 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.935 (1.35) | 1.453 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s60 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.935 (1.35) | 1.453 |
| script | v3_growth_zone_drift_low_texture_mild_s61 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 0.901 (1.35) | 1.39 |
| remedy_tree | v3_growth_zone_drift_low_texture_mild_s61 | 0 | accept_repaired | accept | good_report | low_texture | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px | 0.614 (1.35) | 0.927 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s61 | 0 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.601 (1.35) | 1.012 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s61 | 1 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.601 (1.35) | 1.012 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s61 | 2 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.601 (1.35) | 1.012 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s61 | 0 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.876 (1.35) | 1.356 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s61 | 1 | accept_repaired | accept | false_accept | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.876 (1.35) | 1.356 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s61 | 2 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.876 (1.35) | 1.356 |
| script | v3_growth_zone_second_root_occlusion_mild_s61 | 0 | decline | accept | false_accept | - | 1 | none | 6.447 (1.35) | 0.274 |
| remedy_tree | v3_growth_zone_second_root_occlusion_mild_s61 | 0 | decline | accept | false_accept | - | 1 | none | 6.447 (1.35) | 0.274 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s61 | 0 | decline | accept | false_accept | - | 1 | none | 6.447 (1.35) | 0.274 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s61 | 1 | decline | accept | false_accept | - | 1 | none | 6.447 (1.35) | 0.274 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s61 | 2 | decline | accept | false_accept | - | 1 | none | 6.447 (1.35) | 0.274 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s61 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 6.447 (1.35) | 0.274 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s61 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 6.447 (1.35) | 0.274 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s61 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 6.447 (1.35) | 0.274 |
| script | v3_growth_zone_drift_jitter_mild_s61 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.392 (1.35) | 0.181 |
| remedy_tree | v3_growth_zone_drift_jitter_mild_s61 | 0 | decline | accept | accept_on_decline | width_change | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.421 (1.35) | 0.265 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s61 | 0 | decline | decline | correct_decline | rigid_drift | 7 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.422 (1.35) | 0.274 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s61 | 1 | decline | decline | correct_decline | midline_jitter | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.421 (1.35) | 0.265 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s61 | 2 | decline | decline | correct_decline | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.421 (1.35) | 0.265 |
| single_agent | v3_growth_zone_drift_jitter_mild_s61 | 0 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.422 (1.35) | 0.274 |
| single_agent | v3_growth_zone_drift_jitter_mild_s61 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.421 (1.35) | 0.265 |
| single_agent | v3_growth_zone_drift_jitter_mild_s61 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.421 (1.35) | 0.265 |
| script | v3_growth_zone_focus_drift_z1.5_s61 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.528 (1.35) | 0.522 |
| remedy_tree | v3_growth_zone_focus_drift_z1.5_s61 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.528 (1.35) | 0.522 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s61 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.528 (1.35) | 0.522 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s61 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.528 (1.35) | 0.522 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s61 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.528 (1.35) | 0.522 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s61 | 0 | accept_clean | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.528 (1.35) | 0.522 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s61 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.528 (1.35) | 0.522 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s61 | 2 | accept_clean | accept | good_report | - | 4 | none | 0.528 (1.35) | 0.522 |
| script | v3_growth_zone_illumination_flicker_z0.03_s61 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 1.056 (1.35) | 1.253 |
| remedy_tree | v3_growth_zone_illumination_flicker_z0.03_s61 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.056 (1.35) | 1.253 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s61 | 0 | accept_repaired | decline | unnecessary_decline | unknown | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.056 (1.35) | 1.253 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s61 | 1 | accept_repaired | decline | unnecessary_decline | unknown | 6 | none | 1.056 (1.35) | 1.253 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s61 | 2 | accept_repaired | decline | unnecessary_decline | unknown | 6 | none | 1.056 (1.35) | 1.253 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s61 | 0 | accept_repaired | accept | false_accept | - | 7 | none | 1.056 (1.35) | 1.253 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s61 | 1 | accept_repaired | accept | false_accept | - | 4 | none | 1.056 (1.35) | 1.253 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s61 | 2 | accept_repaired | accept | false_accept | - | 4 | none | 1.056 (1.35) | 1.253 |
| script | v3_growth_zone_second_root_occlusion_mild_s62 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 1.783 (1.35) | 0.288 |
| remedy_tree | v3_growth_zone_second_root_occlusion_mild_s62 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 1.783 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s62 | 0 | accept_repaired | accept | false_accept | width_change | 3 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.783 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s62 | 1 | accept_repaired | accept | false_accept | - | 1 | none | 1.783 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s62 | 2 | accept_repaired | accept | false_accept | - | 1 | none | 1.783 (1.35) | 0.288 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s62 | 0 | accept_repaired | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.783 (1.35) | 0.288 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s62 | 1 | accept_repaired | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.783 (1.35) | 0.288 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s62 | 2 | accept_repaired | accept | false_accept | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.783 (1.35) | 0.288 |
| script | v3_growth_zone_focus_drift_z1.5_s62 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.699 (1.35) | 0.869 |
| remedy_tree | v3_growth_zone_focus_drift_z1.5_s62 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.699 (1.35) | 0.869 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s62 | 0 | accept_clean | accept | good_report | - | 2 | none | 0.699 (1.35) | 0.869 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s62 | 1 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.699 (1.35) | 0.869 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s62 | 2 | accept_clean | accept | good_report | - | 3 | none | 0.699 (1.35) | 0.869 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s62 | 0 | accept_clean | accept | good_report | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.699 (1.35) | 0.869 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s62 | 1 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.699 (1.35) | 0.869 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s62 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.699 (1.35) | 0.869 |
| script | v3_growth_zone_illumination_flicker_z0.03_s62 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 0.852 (1.35) | 1.995 |
| remedy_tree | v3_growth_zone_illumination_flicker_z0.03_s62 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.852 (1.35) | 1.995 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s62 | 0 | accept_repaired | decline | unnecessary_decline | unknown | 6 | none | 0.852 (1.35) | 1.995 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s62 | 1 | accept_repaired | decline | unnecessary_decline | unknown | 7 | none | 0.852 (1.35) | 1.995 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s62 | 2 | accept_repaired | decline | unnecessary_decline | unknown | 6 | none | 0.852 (1.35) | 1.995 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s62 | 0 | accept_repaired | accept | false_accept | - | 4 | none | 0.852 (1.35) | 1.995 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s62 | 1 | accept_repaired | accept | false_accept | - | 5 | none | 0.852 (1.35) | 1.995 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s62 | 2 | accept_repaired | accept | false_accept | - | 5 | none | 0.852 (1.35) | 1.995 |
| script | v3_growth_zone_focus_drift_z1.5_s63 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.405 (1.35) | 0.673 |
| remedy_tree | v3_growth_zone_focus_drift_z1.5_s63 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.405 (1.35) | 0.673 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s63 | 0 | accept_clean | accept | good_report | - | 2 | none | 0.405 (1.35) | 0.673 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s63 | 1 | accept_clean | accept | good_report | low_texture | 5 | tracker disk radius 14 -> 21 px | 0.431 (1.35) | 0.445 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s63 | 2 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.405 (1.35) | 0.673 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s63 | 0 | accept_clean | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.405 (1.35) | 0.673 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s63 | 1 | accept_clean | accept | good_report | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.405 (1.35) | 0.673 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s63 | 2 | accept_clean | accept | good_report | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.405 (1.35) | 0.673 |
| script | v3_growth_zone_illumination_flicker_z0.03_s63 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 1.092 (1.35) | 2.066 |
| remedy_tree | v3_growth_zone_illumination_flicker_z0.03_s63 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.092 (1.35) | 2.066 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s63 | 0 | accept_repaired | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.092 (1.35) | 2.066 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s63 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.092 (1.35) | 2.066 |
| diagnostician | v3_growth_zone_illumination_flicker_z0.03_s63 | 2 | accept_repaired | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.092 (1.35) | 2.066 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s63 | 0 | accept_repaired | accept | false_accept | - | 7 | none | 1.092 (1.35) | 2.066 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s63 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.092 (1.35) | 2.066 |
| single_agent | v3_growth_zone_illumination_flicker_z0.03_s63 | 2 | accept_repaired | accept | false_accept | - | 4 | none | 1.092 (1.35) | 2.066 |
| script | v3_growth_zone_drift_low_texture_mild_s64 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 0.843 (1.35) | 1.478 |
| remedy_tree | v3_growth_zone_drift_low_texture_mild_s64 | 0 | accept_repaired | accept | good_report | low_texture | 4 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 0.657 (1.35) | 0.844 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s64 | 0 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.614 (1.35) | 1.088 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s64 | 1 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.614 (1.35) | 1.088 |
| diagnostician | v3_growth_zone_drift_low_texture_mild_s64 | 2 | accept_repaired | decline | unnecessary_decline | low_texture | 6 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 0.614 (1.35) | 1.088 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s64 | 0 | accept_repaired | accept | false_accept | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking | 0.824 (1.35) | 1.501 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s64 | 1 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.824 (1.35) | 1.501 |
| single_agent | v3_growth_zone_drift_low_texture_mild_s64 | 2 | accept_repaired | accept | false_accept | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking | 0.824 (1.35) | 1.501 |
| script | v3_growth_zone_second_root_occlusion_mild_s64 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 2.022 (1.35) | 0.297 |
| remedy_tree | v3_growth_zone_second_root_occlusion_mild_s64 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 2.022 (1.35) | 0.297 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s64 | 0 | accept_repaired | accept | false_accept | - | 1 | none | 2.022 (1.35) | 0.297 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s64 | 1 | accept_repaired | accept | false_accept | - | 1 | none | 2.022 (1.35) | 0.297 |
| diagnostician | v3_growth_zone_second_root_occlusion_mild_s64 | 2 | accept_repaired | accept | false_accept | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 2.022 (1.35) | 0.297 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s64 | 0 | accept_repaired | accept | false_accept | width_change | 7 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 2.022 (1.35) | 0.297 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s64 | 1 | accept_repaired | accept | false_accept | second_root | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames limited to the main root (mask_second_root) | 2.022 (1.35) | 0.297 |
| single_agent | v3_growth_zone_second_root_occlusion_mild_s64 | 2 | accept_repaired | accept | false_accept | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 2.022 (1.35) | 0.297 |
| script | v3_growth_zone_drift_jitter_mild_s64 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.375 (1.35) | 0.228 |
| remedy_tree | v3_growth_zone_drift_jitter_mild_s64 | 0 | accept_repaired | accept | good_report | width_change | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.36 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s64 | 0 | accept_repaired | decline | unnecessary_decline | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.366 (1.35) | 0.36 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s64 | 1 | accept_repaired | decline | unnecessary_decline | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.366 (1.35) | 0.36 |
| diagnostician | v3_growth_zone_drift_jitter_mild_s64 | 2 | accept_repaired | decline | unnecessary_decline | midline_jitter | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.366 (1.35) | 0.36 |
| single_agent | v3_growth_zone_drift_jitter_mild_s64 | 0 | accept_repaired | step_limit | not_reported | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.376 (1.35) | 0.372 |
| single_agent | v3_growth_zone_drift_jitter_mild_s64 | 1 | accept_repaired | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.366 (1.35) | 0.36 |
| single_agent | v3_growth_zone_drift_jitter_mild_s64 | 2 | accept_repaired | step_limit | not_reported | midline_jitter | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.376 (1.35) | 0.372 |
| script | v3_growth_zone_focus_drift_z1.5_s64 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.474 (1.35) | 0.549 |
| remedy_tree | v3_growth_zone_focus_drift_z1.5_s64 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.474 (1.35) | 0.549 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s64 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.474 (1.35) | 0.549 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s64 | 1 | accept_clean | accept | good_report | - | 2 | none | 0.474 (1.35) | 0.549 |
| diagnostician | v3_growth_zone_focus_drift_z1.5_s64 | 2 | accept_clean | accept | good_report | - | 2 | none | 0.474 (1.35) | 0.549 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s64 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.474 (1.35) | 0.549 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s64 | 1 | accept_clean | accept | good_report | - | 4 | none | 0.474 (1.35) | 0.549 |
| single_agent | v3_growth_zone_focus_drift_z1.5_s64 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.474 (1.35) | 0.549 |
