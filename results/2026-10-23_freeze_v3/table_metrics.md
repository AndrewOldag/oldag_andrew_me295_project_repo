# Freeze v3 scored runs: metrics

51 rods: accept_clean 18, accept_repaired 12, decline 21. LLM methods 3 repeats; values are the mean over repeats, (min-max) where they differ. Definitions: `docs/proposals/2026-10-23_freeze-v3.md`, section 3; code `measure/metrics.py`.

| Method | Runs | Balanced accuracy | Acc. accept_clean | Acc. accept_repaired | Acc. decline | Overall | False accepts | False-accept rate | Coverage | Abst. precision | Abst. recall | not_reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| script | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 0.59 | 18.0 | 0.35 | 1.00 | - | 0.00 | 0 |
| remedy_tree | 51 | 0.81 | 1.00 | 0.75 | 0.67 | 0.80 | 4.0 | 0.12 | 0.67 | 0.82 | 0.67 | 0 |
| diagnostician | 153 | 0.69 (0.69-0.69) | 0.91 (0.89-0.94) | 0.44 (0.42-0.50) | 0.71 (0.67-0.76) | 0.72 (0.71-0.73) | 0.0 | 0.00 | 0.48 (0.47-0.49) | 0.64 (0.64-0.65) | 0.71 (0.67-0.76) | 9 |
| single_agent | 153 | 0.60 (0.57-0.64) | 0.76 (0.72-0.78) | 0.61 (0.50-0.67) | 0.43 (0.33-0.48) | 0.59 (0.57-0.63) | 0.0 | 0.00 | 0.45 (0.43-0.47) | 0.65 (0.58-0.71) | 0.43 (0.33-0.48) | 43 |
| all_decline | 51 | 0.33 | 0.00 | 0.00 | 1.00 | 0.41 | 0.0 | - | 0.00 | 0.41 | 1.00 | 0 |
| all_accept | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 0.59 | 18.0 | 0.35 | 1.00 | - | 0.00 | 0 |

## Agreement across repeats (LLM methods)

| Method | Rods | Unanimous | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |
| :-- | --: | --: | :-- | :-- | :-- | :-- | :-- |
| diagnostician | 51 | 39 | 0.76 | 0.94 | 0.67 | 0.67 | 0.776 |
| single_agent | 51 | 24 | 0.47 | 0.44 | 0.67 | 0.38 | 0.503 |

## Categories, remedies kept, unnecessary declines (summed over repeats)

| Method | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | accept_on_decline | Runs keeping a remedy, accept_clean | Unnecessary-decline rate accept_clean / accept_repaired | Fault named correct |
| :-- | --: | --: | --: | --: | --: | --: | --: | :-- | :-- |
| script | 30 | 18 | 0 | 0 | 0 | 3 | 0 | 0.00 / 0.00 | 0 of 33 |
| remedy_tree | 27 | 4 | 14 | 3 | 0 | 3 | 1 | 0.00 / 0.25 | 14 of 33 |
| diagnostician | 65 | 0 | 45 | 25 | 9 | 9 | 0 | 0.09 (0.06-0.11) / 0.56 (0.50-0.58) | 54 of 99 |
| single_agent | 63 | 0 | 27 | 14 | 43 | 6 | 21 | 0.20 (0.17-0.22) / 0.08 (0.00-0.17) | 31 of 99 |
| all_decline | 0 | 0 | 21 | 30 | 0 | 0 | 0 | 1.00 / 1.00 | 0 of 0 |
| all_accept | 30 | 18 | 0 | 0 | 0 | 3 | 0 | 0.00 / 0.00 | 0 of 0 |

## Per row of the set (correct runs / runs)

| Row | Class | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| v3_bend16 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_bend20 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 5 / 9 |
| v3_bend24 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 7 / 9 |
| v3_bend30 | accept_clean | 3 / 3 | 3 / 3 | 6 / 9 | 5 / 9 |
| v3_still | accept_clean | 3 / 3 | 3 / 3 | 7 / 9 | 9 / 9 |
| rigid_drift | accept_repaired | 3 / 3 | 3 / 3 | 3 / 9 | 6 / 9 |
| displacement_exceeds_patch | decline | 0 / 3 | 2 / 3 | 6 / 9 | 3 / 9 |
| width_change | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| low_texture | decline | 0 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| midline_jitter | decline | 0 / 3 | 3 / 3 | 9 / 9 | 4 / 9 |
| bad_stage_correction | accept_repaired | 3 / 3 | 3 / 3 | 4 / 9 | 7 / 9 |
| stage_log_missing | accept_repaired | 3 / 3 | 0 / 3 | 0 / 9 | 0 / 9 |
| second_root | decline | 0 / 3 | 0 / 3 | 0 / 9 | 0 / 9 |
| fast_rotation | decline | 0 / 3 | 3 / 3 | 7 / 9 | 5 / 9 |
| flank_swap | decline | 0 / 3 | 3 / 3 | 7 / 9 | 4 / 9 |
| partial_occlusion | decline | 0 / 3 | 0 / 3 | 7 / 9 | 2 / 9 |

## Cost (LLM methods, all repeats)

| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: |
| script | 51 | 51 | 0 | 0 | 0.0 |
| remedy_tree | 51 | 156 | 0 | 0 | 0.0 |
| diagnostician | 153 | 593 | 2611986 | 353434 | 4076.9 |
| single_agent | 153 | 980 | 4160002 | 570456 | 6750.5 |

## Per run

| Method | Rod | Repeat | Class | Status | Category | Named fault | Steps | Remedies | Centre RMS (tol) | Flank RMS |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: |
| script | v3_growth_zone_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| remedy_tree | v3_growth_zone_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_clean_s20 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_clean_s20 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| single_agent | v3_growth_zone_clean_s20 | 0 | accept_clean | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.34 (1.35) | 0.158 |
| single_agent | v3_growth_zone_clean_s20 | 1 | accept_clean | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.34 (1.35) | 0.158 |
| single_agent | v3_growth_zone_clean_s20 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.34 (1.35) | 0.158 |
| script | v3_growth_zone_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.188 |
| remedy_tree | v3_growth_zone_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.188 |
| diagnostician | v3_growth_zone_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.188 |
| diagnostician | v3_growth_zone_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.188 |
| diagnostician | v3_growth_zone_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.188 |
| single_agent | v3_growth_zone_clean_s21 | 0 | accept_clean | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.359 (1.35) | 0.188 |
| single_agent | v3_growth_zone_clean_s21 | 1 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.359 (1.35) | 0.188 |
| single_agent | v3_growth_zone_clean_s21 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.359 (1.35) | 0.188 |
| script | v3_growth_zone_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.347 (1.35) | 0.17 |
| remedy_tree | v3_growth_zone_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.347 (1.35) | 0.17 |
| diagnostician | v3_growth_zone_clean_s22 | 0 | accept_clean | accept | good_report | - | 2 | none | 0.347 (1.35) | 0.17 |
| diagnostician | v3_growth_zone_clean_s22 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.347 (1.35) | 0.17 |
| diagnostician | v3_growth_zone_clean_s22 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_clean_s22 | 0 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_clean_s22 | 1 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_clean_s22 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.17 |
| script | v3_bend16_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.388 (1.35) | 0.22 |
| remedy_tree | v3_bend16_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.388 (1.35) | 0.22 |
| diagnostician | v3_bend16_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.388 (1.35) | 0.22 |
| diagnostician | v3_bend16_clean_s20 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.388 (1.35) | 0.22 |
| diagnostician | v3_bend16_clean_s20 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.388 (1.35) | 0.22 |
| single_agent | v3_bend16_clean_s20 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.388 (1.35) | 0.22 |
| single_agent | v3_bend16_clean_s20 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.388 (1.35) | 0.22 |
| single_agent | v3_bend16_clean_s20 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.388 (1.35) | 0.22 |
| script | v3_bend16_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.428 (1.35) | 0.361 |
| remedy_tree | v3_bend16_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.428 (1.35) | 0.361 |
| diagnostician | v3_bend16_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.428 (1.35) | 0.361 |
| diagnostician | v3_bend16_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.428 (1.35) | 0.361 |
| diagnostician | v3_bend16_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.428 (1.35) | 0.361 |
| single_agent | v3_bend16_clean_s21 | 0 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.434 (1.35) | 0.316 |
| single_agent | v3_bend16_clean_s21 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.428 (1.35) | 0.361 |
| single_agent | v3_bend16_clean_s21 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.428 (1.35) | 0.361 |
| script | v3_bend16_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.429 (1.35) | 0.279 |
| remedy_tree | v3_bend16_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.429 (1.35) | 0.279 |
| diagnostician | v3_bend16_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.429 (1.35) | 0.279 |
| diagnostician | v3_bend16_clean_s22 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.429 (1.35) | 0.279 |
| diagnostician | v3_bend16_clean_s22 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.429 (1.35) | 0.279 |
| single_agent | v3_bend16_clean_s22 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.429 (1.35) | 0.279 |
| single_agent | v3_bend16_clean_s22 | 1 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.423 (1.35) | 0.283 |
| single_agent | v3_bend16_clean_s22 | 2 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.423 (1.35) | 0.283 |
| script | v3_bend20_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.38 (1.35) | 0.362 |
| remedy_tree | v3_bend20_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.38 (1.35) | 0.362 |
| diagnostician | v3_bend20_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.38 (1.35) | 0.362 |
| diagnostician | v3_bend20_clean_s20 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.38 (1.35) | 0.362 |
| diagnostician | v3_bend20_clean_s20 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.38 (1.35) | 0.362 |
| single_agent | v3_bend20_clean_s20 | 0 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.382 (1.35) | 0.293 |
| single_agent | v3_bend20_clean_s20 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.38 (1.35) | 0.362 |
| single_agent | v3_bend20_clean_s20 | 2 | accept_clean | accept | good_report | - | 7 | none | 0.38 (1.35) | 0.362 |
| script | v3_bend20_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.417 (1.35) | 0.39 |
| remedy_tree | v3_bend20_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.417 (1.35) | 0.39 |
| diagnostician | v3_bend20_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.417 (1.35) | 0.39 |
| diagnostician | v3_bend20_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.417 (1.35) | 0.39 |
| diagnostician | v3_bend20_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.417 (1.35) | 0.39 |
| single_agent | v3_bend20_clean_s21 | 0 | accept_clean | decline | unnecessary_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.427 (1.35) | 0.391 |
| single_agent | v3_bend20_clean_s21 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.417 (1.35) | 0.39 |
| single_agent | v3_bend20_clean_s21 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.417 (1.35) | 0.39 |
| script | v3_bend20_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.438 (1.35) | 0.305 |
| remedy_tree | v3_bend20_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.438 (1.35) | 0.305 |
| diagnostician | v3_bend20_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.438 (1.35) | 0.305 |
| diagnostician | v3_bend20_clean_s22 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.438 (1.35) | 0.305 |
| diagnostician | v3_bend20_clean_s22 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.438 (1.35) | 0.305 |
| single_agent | v3_bend20_clean_s22 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.438 (1.35) | 0.305 |
| single_agent | v3_bend20_clean_s22 | 1 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.461 (1.35) | 0.295 |
| single_agent | v3_bend20_clean_s22 | 2 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.461 (1.35) | 0.295 |
| script | v3_bend24_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.366 |
| remedy_tree | v3_bend24_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.366 |
| diagnostician | v3_bend24_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.366 |
| diagnostician | v3_bend24_clean_s20 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.366 |
| diagnostician | v3_bend24_clean_s20 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.366 |
| single_agent | v3_bend24_clean_s20 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.401 (1.35) | 0.366 |
| single_agent | v3_bend24_clean_s20 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.401 (1.35) | 0.366 |
| single_agent | v3_bend24_clean_s20 | 2 | accept_clean | accept | good_report | - | 7 | none | 0.401 (1.35) | 0.366 |
| script | v3_bend24_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.463 (1.35) | 0.506 |
| remedy_tree | v3_bend24_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.463 (1.35) | 0.506 |
| diagnostician | v3_bend24_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.463 (1.35) | 0.506 |
| diagnostician | v3_bend24_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.463 (1.35) | 0.506 |
| diagnostician | v3_bend24_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.463 (1.35) | 0.506 |
| single_agent | v3_bend24_clean_s21 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.463 (1.35) | 0.506 |
| single_agent | v3_bend24_clean_s21 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.463 (1.35) | 0.506 |
| single_agent | v3_bend24_clean_s21 | 2 | accept_clean | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.46 (1.35) | 0.492 |
| script | v3_bend24_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.459 (1.35) | 0.326 |
| remedy_tree | v3_bend24_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.459 (1.35) | 0.326 |
| diagnostician | v3_bend24_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.459 (1.35) | 0.326 |
| diagnostician | v3_bend24_clean_s22 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.459 (1.35) | 0.326 |
| diagnostician | v3_bend24_clean_s22 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.459 (1.35) | 0.326 |
| single_agent | v3_bend24_clean_s22 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.459 (1.35) | 0.326 |
| single_agent | v3_bend24_clean_s22 | 1 | accept_clean | decline | unnecessary_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.455 (1.35) | 0.311 |
| single_agent | v3_bend24_clean_s22 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.459 (1.35) | 0.326 |
| script | v3_bend30_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.439 (1.35) | 0.347 |
| remedy_tree | v3_bend30_clean_s20 | 0 | accept_clean | accept | good_report | low_texture | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px | 0.562 (1.35) | 0.312 |
| diagnostician | v3_bend30_clean_s20 | 0 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.439 (1.35) | 0.347 |
| diagnostician | v3_bend30_clean_s20 | 1 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.439 (1.35) | 0.347 |
| diagnostician | v3_bend30_clean_s20 | 2 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.439 (1.35) | 0.347 |
| single_agent | v3_bend30_clean_s20 | 0 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 4 | none | 0.439 (1.35) | 0.347 |
| single_agent | v3_bend30_clean_s20 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.439 (1.35) | 0.347 |
| single_agent | v3_bend30_clean_s20 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.439 (1.35) | 0.347 |
| script | v3_bend30_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.485 (1.35) | 0.473 |
| remedy_tree | v3_bend30_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.485 (1.35) | 0.473 |
| diagnostician | v3_bend30_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.485 (1.35) | 0.473 |
| diagnostician | v3_bend30_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.485 (1.35) | 0.473 |
| diagnostician | v3_bend30_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.485 (1.35) | 0.473 |
| single_agent | v3_bend30_clean_s21 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.485 (1.35) | 0.473 |
| single_agent | v3_bend30_clean_s21 | 1 | accept_clean | decline | unnecessary_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.493 (1.35) | 0.535 |
| single_agent | v3_bend30_clean_s21 | 2 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.493 (1.35) | 0.535 |
| script | v3_bend30_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.482 (1.35) | 0.282 |
| remedy_tree | v3_bend30_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.482 (1.35) | 0.282 |
| diagnostician | v3_bend30_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.482 (1.35) | 0.282 |
| diagnostician | v3_bend30_clean_s22 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.482 (1.35) | 0.282 |
| diagnostician | v3_bend30_clean_s22 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.482 (1.35) | 0.282 |
| single_agent | v3_bend30_clean_s22 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.482 (1.35) | 0.282 |
| single_agent | v3_bend30_clean_s22 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.482 (1.35) | 0.282 |
| single_agent | v3_bend30_clean_s22 | 2 | accept_clean | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.48 (1.35) | 0.265 |
| script | v3_still_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.151 (0.5) | 0.165 |
| remedy_tree | v3_still_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.151 (0.5) | 0.165 |
| diagnostician | v3_still_clean_s20 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.151 (0.5) | 0.165 |
| diagnostician | v3_still_clean_s20 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.151 (0.5) | 0.165 |
| diagnostician | v3_still_clean_s20 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.151 (0.5) | 0.165 |
| single_agent | v3_still_clean_s20 | 0 | accept_clean | accept | good_report | - | 4 | none | 0.151 (0.5) | 0.165 |
| single_agent | v3_still_clean_s20 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.151 (0.5) | 0.165 |
| single_agent | v3_still_clean_s20 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.151 (0.5) | 0.165 |
| script | v3_still_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.199 (0.5) | 0.2 |
| remedy_tree | v3_still_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.199 (0.5) | 0.2 |
| diagnostician | v3_still_clean_s21 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.199 (0.5) | 0.2 |
| diagnostician | v3_still_clean_s21 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.199 (0.5) | 0.2 |
| diagnostician | v3_still_clean_s21 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.199 (0.5) | 0.2 |
| single_agent | v3_still_clean_s21 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.199 (0.5) | 0.2 |
| single_agent | v3_still_clean_s21 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.199 (0.5) | 0.2 |
| single_agent | v3_still_clean_s21 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.199 (0.5) | 0.2 |
| script | v3_still_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.152 (0.5) | 0.227 |
| remedy_tree | v3_still_clean_s22 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.152 (0.5) | 0.227 |
| diagnostician | v3_still_clean_s22 | 0 | accept_clean | decline | unnecessary_decline | unknown | 4 | none | 0.152 (0.5) | 0.227 |
| diagnostician | v3_still_clean_s22 | 1 | accept_clean | decline | unnecessary_decline | unknown | 3 | none | 0.152 (0.5) | 0.227 |
| diagnostician | v3_still_clean_s22 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.152 (0.5) | 0.227 |
| single_agent | v3_still_clean_s22 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.152 (0.5) | 0.227 |
| single_agent | v3_still_clean_s22 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.152 (0.5) | 0.227 |
| single_agent | v3_still_clean_s22 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.152 (0.5) | 0.227 |
| script | v3_growth_zone_rigid_drift_z0.5_s20 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.356 (1.35) | 0.203 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s20 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.349 (1.35) | 0.23 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s20 | 0 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.356 (1.35) | 0.203 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s20 | 1 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.356 (1.35) | 0.203 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s20 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.356 (1.35) | 0.203 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s20 | 0 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.349 (1.35) | 0.23 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s20 | 1 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.349 (1.35) | 0.23 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s20 | 2 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.349 (1.35) | 0.23 |
| script | v3_growth_zone_rigid_drift_z0.5_s21 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.395 (1.35) | 0.261 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s21 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.403 (1.35) | 0.307 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s21 | 0 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.395 (1.35) | 0.261 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s21 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.403 (1.35) | 0.307 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s21 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.403 (1.35) | 0.307 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s21 | 0 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.403 (1.35) | 0.307 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s21 | 1 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.403 (1.35) | 0.307 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s21 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 4 | none | 0.395 (1.35) | 0.261 |
| script | v3_growth_zone_rigid_drift_z0.5_s22 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.361 (1.35) | 0.285 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s22 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.371 (1.35) | 0.226 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s22 | 0 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.361 (1.35) | 0.285 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s22 | 1 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.361 (1.35) | 0.285 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s22 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.371 (1.35) | 0.226 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s22 | 0 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.371 (1.35) | 0.226 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s22 | 1 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 5 | none | 0.361 (1.35) | 0.285 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s22 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 4 | none | 0.361 (1.35) | 0.285 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 0 | decline | accept | false_accept | - | 1 | none | 74.455 (2.698) | 82.509 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 0 | decline | decline | correct_decline | low_texture | 7 | frames registered on the non-growing tissue (from 370 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 370 px from the tip) before tracking; frame stride 6 -> 3; frame stride 3 -> 1; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 3.846 (2.698) | 0.177 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 0 | decline | decline | correct_decline | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 22.111 (2.698) | 3.99 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 22.111 (2.698) | 3.99 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 2 | decline | decline | correct_decline | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 22.111 (2.698) | 3.99 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 0 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 370 px from the tip) before tracking | 83.206 (2.698) | 78.352 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3 | 42.341 (2.698) | 79.734 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | 2 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3 | 42.341 (2.698) | 79.734 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 0 | decline | accept | false_accept | - | 1 | none | 66.084 (2.698) | 46.695 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 0 | decline | accept | false_accept | displacement_exceeds_patch | 4 | frames registered on the non-growing tissue (from 350 px from the tip) before tracking; frame stride 6 -> 3; frame stride 3 -> 1 | 10.401 (2.698) | 0.262 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 0 | decline | step_limit | not_reported | low_texture | 8 | frame stride 6 -> 3; frame stride 3 -> 1; tracker disk radius 14 -> 21 px | 4.868 (2.698) | 0.264 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 1 | decline | decline | correct_decline | displacement_exceeds_patch | 7 | frame stride 6 -> 3; frame stride 3 -> 1 | 10.425 (2.698) | 0.241 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 2 | decline | decline | correct_decline | low_texture | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 10.425 (2.698) | 0.241 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 0 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 350 px from the tip) before tracking | 47.153 (2.698) | 56.839 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; tracker disk radius 14 -> 21 px | 29.828 (2.698) | 93.428 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | 2 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 350 px from the tip) before tracking | 47.153 (2.698) | 56.839 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 0 | decline | accept | false_accept | - | 1 | none | 62.448 (2.698) | 67.685 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 0 | decline | decline | correct_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 335 px from the tip) before tracking; frame stride 6 -> 3; rolled back: frame stride 6 -> 3; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 66.804 (2.698) | 61.789 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 0 | decline | decline | correct_decline | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 5.602 (2.698) | 4.735 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 1 | decline | decline | correct_decline | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 5.602 (2.698) | 4.735 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 2 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 5.602 (2.698) | 4.735 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 0 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 335 px from the tip) before tracking; frame stride 6 -> 3 | 57.792 (2.698) | 62.118 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 335 px from the tip) before tracking; frame stride 6 -> 3 | 57.792 (2.698) | 62.118 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | 2 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 5.602 (2.698) | 4.735 |
| script | v3_growth_zone_width_change_s20 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.357 (1.35) | 0.229 |
| remedy_tree | v3_growth_zone_width_change_s20 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| diagnostician | v3_growth_zone_width_change_s20 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| diagnostician | v3_growth_zone_width_change_s20 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| diagnostician | v3_growth_zone_width_change_s20 | 2 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| single_agent | v3_growth_zone_width_change_s20 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| single_agent | v3_growth_zone_width_change_s20 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| single_agent | v3_growth_zone_width_change_s20 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.229 |
| script | v3_growth_zone_width_change_s21 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.356 (1.35) | 0.288 |
| remedy_tree | v3_growth_zone_width_change_s21 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_width_change_s21 | 0 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_width_change_s21 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| diagnostician | v3_growth_zone_width_change_s21 | 2 | accept_repaired | accept | good_report | width_change | 8 | tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| single_agent | v3_growth_zone_width_change_s21 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| single_agent | v3_growth_zone_width_change_s21 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| single_agent | v3_growth_zone_width_change_s21 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.356 (1.35) | 0.288 |
| script | v3_growth_zone_width_change_s22 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.366 (1.35) | 0.308 |
| remedy_tree | v3_growth_zone_width_change_s22 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| diagnostician | v3_growth_zone_width_change_s22 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| diagnostician | v3_growth_zone_width_change_s22 | 1 | accept_repaired | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| diagnostician | v3_growth_zone_width_change_s22 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| single_agent | v3_growth_zone_width_change_s22 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| single_agent | v3_growth_zone_width_change_s22 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| single_agent | v3_growth_zone_width_change_s22 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.366 (1.35) | 0.308 |
| script | v3_growth_zone_low_texture_z0.03_s20 | 0 | decline | accept | false_accept | - | 1 | none | 20.884 (1.35) | 32.232 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s20 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 545 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 10.836 (1.35) | 18.337 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s20 | 0 | decline | decline | correct_decline | low_texture | 3 | none | 20.884 (1.35) | 32.232 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s20 | 1 | decline | decline | correct_decline | low_texture | 3 | none | 20.884 (1.35) | 32.232 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s20 | 2 | decline | decline | correct_decline | low_texture | 3 | none | 20.884 (1.35) | 32.232 |
| single_agent | v3_growth_zone_low_texture_z0.03_s20 | 0 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking | 106.015 (1.35) | 171.979 |
| single_agent | v3_growth_zone_low_texture_z0.03_s20 | 1 | decline | decline | correct_decline | low_texture | 5 | none | 20.884 (1.35) | 32.232 |
| single_agent | v3_growth_zone_low_texture_z0.03_s20 | 2 | decline | decline | correct_decline | low_texture | 4 | none | 20.884 (1.35) | 32.232 |
| script | v3_growth_zone_low_texture_z0.03_s21 | 0 | decline | accept | false_accept | - | 1 | none | 24.959 (1.35) | 56.232 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s21 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 12.892 (1.35) | 18.865 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s21 | 0 | decline | decline | correct_decline | low_texture | 3 | none | 24.959 (1.35) | 56.232 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s21 | 1 | decline | decline | correct_decline | low_texture | 3 | none | 24.959 (1.35) | 56.232 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s21 | 2 | decline | decline | correct_decline | low_texture | 3 | none | 24.959 (1.35) | 56.232 |
| single_agent | v3_growth_zone_low_texture_z0.03_s21 | 0 | decline | decline | correct_decline | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 98.699 (1.35) | 107.555 |
| single_agent | v3_growth_zone_low_texture_z0.03_s21 | 1 | decline | decline | correct_decline | low_texture | 5 | none | 24.959 (1.35) | 56.232 |
| single_agent | v3_growth_zone_low_texture_z0.03_s21 | 2 | decline | decline | correct_decline | low_texture | 5 | none | 24.959 (1.35) | 56.232 |
| script | v3_growth_zone_low_texture_z0.03_s22 | 0 | decline | accept | false_accept | - | 1 | none | 20.197 (1.35) | 36.026 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s22 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 15.099 (1.35) | 21.18 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s22 | 0 | decline | decline | correct_decline | low_texture | 3 | none | 20.197 (1.35) | 36.026 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s22 | 1 | decline | decline | correct_decline | low_texture | 3 | none | 20.197 (1.35) | 36.026 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s22 | 2 | decline | decline | correct_decline | low_texture | 3 | none | 20.197 (1.35) | 36.026 |
| single_agent | v3_growth_zone_low_texture_z0.03_s22 | 0 | decline | decline | correct_decline | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 70.66 (1.35) | nan |
| single_agent | v3_growth_zone_low_texture_z0.03_s22 | 1 | decline | decline | correct_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 70.66 (1.35) | nan |
| single_agent | v3_growth_zone_low_texture_z0.03_s22 | 2 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 70.66 (1.35) | nan |
| script | v3_growth_zone_midline_jitter_z3_s20 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.676 (1.35) | 0.375 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s20 | 0 | decline | decline | correct_decline | midline_jitter | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 0.942 (1.35) | 0.393 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s20 | 0 | decline | decline | correct_decline | midline_jitter | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.942 (1.35) | 0.393 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s20 | 1 | decline | decline | correct_decline | midline_jitter | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.942 (1.35) | 0.393 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s20 | 2 | decline | decline | correct_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.676 (1.35) | 0.375 |
| single_agent | v3_growth_zone_midline_jitter_z3_s20 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.942 (1.35) | 0.393 |
| single_agent | v3_growth_zone_midline_jitter_z3_s20 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.942 (1.35) | 0.393 |
| single_agent | v3_growth_zone_midline_jitter_z3_s20 | 2 | decline | decline | correct_decline | bad_stage_correction | 4 | none | 0.676 (1.35) | 0.375 |
| script | v3_growth_zone_midline_jitter_z3_s21 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.447 (1.35) | 0.502 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s21 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 405 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.447 (1.35) | 0.502 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s21 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 0.447 (1.35) | 0.502 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s21 | 1 | decline | decline | correct_decline | midline_jitter | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 405 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.447 (1.35) | 0.502 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s21 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 0.447 (1.35) | 0.502 |
| single_agent | v3_growth_zone_midline_jitter_z3_s21 | 0 | decline | decline | correct_decline | bad_stage_correction | 4 | none | 0.447 (1.35) | 0.502 |
| single_agent | v3_growth_zone_midline_jitter_z3_s21 | 1 | decline | step_limit | not_reported | width_change | 8 | midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.454 (1.35) | 0.572 |
| single_agent | v3_growth_zone_midline_jitter_z3_s21 | 2 | decline | decline | correct_decline | bad_stage_correction | 3 | none | 0.447 (1.35) | 0.502 |
| script | v3_growth_zone_midline_jitter_z3_s22 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.557 (1.35) | 0.361 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s22 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.557 (1.35) | 0.361 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s22 | 0 | decline | decline | correct_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.557 (1.35) | 0.361 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s22 | 1 | decline | decline | correct_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.557 (1.35) | 0.361 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s22 | 2 | decline | decline | correct_decline | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.557 (1.35) | 0.361 |
| single_agent | v3_growth_zone_midline_jitter_z3_s22 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.556 (1.35) | 0.363 |
| single_agent | v3_growth_zone_midline_jitter_z3_s22 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.744 (1.35) | 0.44 |
| single_agent | v3_growth_zone_midline_jitter_z3_s22 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.744 (1.35) | 0.44 |
| script | v3_growth_zone_bad_stage_correction_z3_s20 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.34 (1.35) | 0.158 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s20 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.337 (1.35) | 0.143 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s20 | 0 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.34 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s20 | 1 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.34 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s20 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.34 (1.35) | 0.158 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s20 | 0 | accept_repaired | step_limit | not_reported | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.337 (1.35) | 0.143 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s20 | 1 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.34 (1.35) | 0.158 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s20 | 2 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.34 (1.35) | 0.158 |
| script | v3_growth_zone_bad_stage_correction_z3_s21 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.36 (1.35) | 0.188 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s21 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.366 (1.35) | 0.23 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s21 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.366 (1.35) | 0.23 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s21 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.366 (1.35) | 0.23 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s21 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 2 | none | 0.36 (1.35) | 0.188 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s21 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.36 (1.35) | 0.188 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s21 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.36 (1.35) | 0.188 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s21 | 2 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.36 (1.35) | 0.188 |
| script | v3_growth_zone_bad_stage_correction_z3_s22 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.347 (1.35) | 0.17 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s22 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.353 (1.35) | 0.177 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s22 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.353 (1.35) | 0.177 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s22 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.353 (1.35) | 0.177 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s22 | 2 | accept_repaired | decline | unnecessary_decline | bad_stage_correction | 4 | none | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s22 | 0 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s22 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.17 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s22 | 2 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.353 (1.35) | 0.177 |
| script | v3_growth_zone_stage_log_missing_z1_s20 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.343 (1.35) | 0.158 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s20 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.343 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s20 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s20 | 1 | accept_repaired | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.158 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s20 | 2 | accept_repaired | decline | unnecessary_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.158 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s20 | 0 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.339 (1.35) | 0.145 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s20 | 1 | accept_repaired | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.339 (1.35) | 0.145 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s20 | 2 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.339 (1.35) | 0.145 |
| script | v3_growth_zone_stage_log_missing_z1_s21 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.359 (1.35) | 0.187 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s21 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.359 (1.35) | 0.187 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s21 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.187 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s21 | 1 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.187 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s21 | 2 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.187 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s21 | 0 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.374 (1.35) | 0.289 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s21 | 1 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.374 (1.35) | 0.289 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s21 | 2 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.374 (1.35) | 0.289 |
| script | v3_growth_zone_stage_log_missing_z1_s22 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.348 (1.35) | 0.171 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s22 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.348 (1.35) | 0.171 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s22 | 0 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.348 (1.35) | 0.171 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s22 | 1 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.348 (1.35) | 0.171 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s22 | 2 | accept_repaired | decline | unnecessary_decline | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.348 (1.35) | 0.171 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s22 | 0 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.345 (1.35) | 0.226 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s22 | 1 | accept_repaired | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.345 (1.35) | 0.226 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s22 | 2 | accept_repaired | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.345 (1.35) | 0.226 |
| script | v3_growth_zone_second_root_z30_s20 | 0 | decline | accept | false_accept | - | 1 | none | 1.094 (1.35) | 1.187 |
| remedy_tree | v3_growth_zone_second_root_z30_s20 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| diagnostician | v3_growth_zone_second_root_z30_s20 | 0 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| diagnostician | v3_growth_zone_second_root_z30_s20 | 1 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| diagnostician | v3_growth_zone_second_root_z30_s20 | 2 | decline | accept | accept_on_decline | second_root | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames limited to the main root (mask_second_root) | 1.094 (1.35) | 1.187 |
| single_agent | v3_growth_zone_second_root_z30_s20 | 0 | decline | accept | accept_on_decline | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| single_agent | v3_growth_zone_second_root_z30_s20 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| single_agent | v3_growth_zone_second_root_z30_s20 | 2 | decline | accept | accept_on_decline | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1.094 (1.35) | 1.187 |
| script | v3_growth_zone_second_root_z30_s21 | 0 | decline | accept | false_accept | - | 1 | none | 0.432 (1.35) | 2.052 |
| remedy_tree | v3_growth_zone_second_root_z30_s21 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| diagnostician | v3_growth_zone_second_root_z30_s21 | 0 | decline | accept | accept_on_decline | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| diagnostician | v3_growth_zone_second_root_z30_s21 | 1 | decline | accept | accept_on_decline | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| diagnostician | v3_growth_zone_second_root_z30_s21 | 2 | decline | accept | accept_on_decline | width_change | 6 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| single_agent | v3_growth_zone_second_root_z30_s21 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| single_agent | v3_growth_zone_second_root_z30_s21 | 1 | decline | accept | accept_on_decline | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| single_agent | v3_growth_zone_second_root_z30_s21 | 2 | decline | accept | accept_on_decline | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.432 (1.35) | 2.052 |
| script | v3_growth_zone_second_root_z30_s22 | 0 | decline | accept | false_accept | - | 1 | none | 0.599 (1.35) | 2.204 |
| remedy_tree | v3_growth_zone_second_root_z30_s22 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| diagnostician | v3_growth_zone_second_root_z30_s22 | 0 | decline | accept | accept_on_decline | width_change | 6 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| diagnostician | v3_growth_zone_second_root_z30_s22 | 1 | decline | accept | accept_on_decline | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| diagnostician | v3_growth_zone_second_root_z30_s22 | 2 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| single_agent | v3_growth_zone_second_root_z30_s22 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| single_agent | v3_growth_zone_second_root_z30_s22 | 1 | decline | accept | accept_on_decline | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| single_agent | v3_growth_zone_second_root_z30_s22 | 2 | decline | accept | accept_on_decline | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.599 (1.35) | 2.204 |
| script | v3_growth_zone_fast_rotation_z2_s20 | 0 | decline | accept | false_accept | - | 1 | none | 20.157 (1.35) | 35.8 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s20 | 0 | decline | decline | correct_decline | midline_jitter | 5 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light) | 16.096 (1.35) | 13.3 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s20 | 0 | decline | step_limit | not_reported | bad_stage_correction | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 20.157 (1.35) | 35.8 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s20 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 20.157 (1.35) | 35.8 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s20 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 20.157 (1.35) | 35.8 |
| single_agent | v3_growth_zone_fast_rotation_z2_s20 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 29.98 (1.35) | 67.129 |
| single_agent | v3_growth_zone_fast_rotation_z2_s20 | 1 | decline | decline | correct_decline | bad_stage_correction | 4 | none | 20.157 (1.35) | 35.8 |
| single_agent | v3_growth_zone_fast_rotation_z2_s20 | 2 | decline | decline | correct_decline | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 19.772 (1.35) | 32.32 |
| script | v3_growth_zone_fast_rotation_z2_s21 | 0 | decline | accept | false_accept | - | 1 | none | 28.582 (1.35) | 33.882 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s21 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 555 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 13.344 (1.35) | 10.978 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s21 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 24.466 (1.35) | 22.926 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s21 | 1 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 24.466 (1.35) | 22.926 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s21 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 24.466 (1.35) | 22.926 |
| single_agent | v3_growth_zone_fast_rotation_z2_s21 | 0 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 555 px from the tip) before tracking | 12.625 (1.35) | 15.382 |
| single_agent | v3_growth_zone_fast_rotation_z2_s21 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 555 px from the tip) before tracking | 12.625 (1.35) | 15.382 |
| single_agent | v3_growth_zone_fast_rotation_z2_s21 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 555 px from the tip) before tracking | 12.625 (1.35) | 15.382 |
| script | v3_growth_zone_fast_rotation_z2_s22 | 0 | decline | accept | false_accept | - | 1 | none | 49.646 (1.35) | 34.475 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s22 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 27.63 (1.35) | 18.033 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s22 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 43.937 (1.35) | 31.929 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s22 | 1 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 43.937 (1.35) | 31.929 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s22 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 43.937 (1.35) | 31.929 |
| single_agent | v3_growth_zone_fast_rotation_z2_s22 | 0 | decline | decline | correct_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 158.364 (1.35) | 149.329 |
| single_agent | v3_growth_zone_fast_rotation_z2_s22 | 1 | decline | decline | correct_decline | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 158.364 (1.35) | 149.329 |
| single_agent | v3_growth_zone_fast_rotation_z2_s22 | 2 | decline | decline | correct_decline | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 158.364 (1.35) | 149.329 |
| script | v3_growth_zone_flank_swap_z0.5_s20 | 0 | decline | accept | false_accept | - | 1 | none | 5.162 (1.35) | 32.819 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s20 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 545 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 5.162 (1.35) | 32.819 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s20 | 0 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light); rolled back: midline source smoothed (light) | 5.162 (1.35) | 32.819 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s20 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 545 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 545 px from the tip) before tracking | 5.162 (1.35) | 32.819 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s20 | 2 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light); rolled back: midline source smoothed (light) | 5.162 (1.35) | 32.819 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s20 | 0 | decline | decline | correct_decline | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking | 23.097 (1.35) | 79.52 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s20 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 3.895 (1.35) | 38.64 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s20 | 2 | decline | decline | correct_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking | 23.097 (1.35) | 79.52 |
| script | v3_growth_zone_flank_swap_z0.5_s21 | 0 | decline | accept | false_accept | - | 1 | none | 6.483 (1.35) | 31.554 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s21 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 4.772 (1.35) | 30.086 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s21 | 0 | decline | decline | correct_decline | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 6.483 (1.35) | 31.554 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s21 | 1 | decline | decline | correct_decline | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 6.483 (1.35) | 31.554 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s21 | 2 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px | 4.772 (1.35) | 30.086 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s21 | 0 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 17.349 (1.35) | 65.682 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s21 | 1 | decline | decline | correct_decline | bad_stage_correction | 3 | none | 6.483 (1.35) | 31.554 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s21 | 2 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 6.483 (1.35) | 31.554 |
| script | v3_growth_zone_flank_swap_z0.5_s22 | 0 | decline | accept | false_accept | - | 1 | none | 4.479 (1.35) | 29.929 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s22 | 0 | decline | decline | correct_decline | low_texture | 5 | tracker disk radius 14 -> 21 px; frames registered on the non-growing tissue (from 540 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 540 px from the tip) before tracking; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 5.873 (1.35) | 22.348 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s22 | 0 | decline | decline | correct_decline | unknown | 7 | none | 4.479 (1.35) | 29.929 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s22 | 1 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 4.479 (1.35) | 29.929 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s22 | 2 | decline | decline | correct_decline | midline_jitter | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; midline source smoothed (light); rolled back: midline source smoothed (light) | 4.479 (1.35) | 29.929 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s22 | 0 | decline | decline | correct_decline | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 16.42 (1.35) | 58.692 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s22 | 1 | decline | step_limit | not_reported | fast_rotation | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 16.42 (1.35) | 58.692 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s22 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 16.42 (1.35) | 58.692 |
| script | v3_growth_zone_partial_occlusion_z20_s20 | 0 | decline | accept | false_accept | - | 1 | none | 32.045 (1.35) | 6.191 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s20 | 0 | decline | accept | false_accept | width_change | 5 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 4.028 (1.35) | 2.672 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s20 | 0 | decline | decline | correct_decline | unknown | 8 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s20 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s20 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s20 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s20 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s20 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 32.045 (1.35) | 6.191 |
| script | v3_growth_zone_partial_occlusion_z20_s21 | 0 | decline | accept | false_accept | - | 1 | none | 17.569 (1.35) | 4.532 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s21 | 0 | decline | accept | false_accept | width_change | 5 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 5.05 (1.35) | 3.265 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s21 | 0 | decline | decline | correct_decline | unknown | 6 | none | 17.569 (1.35) | 4.532 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s21 | 1 | decline | decline | correct_decline | unknown | 6 | none | 17.569 (1.35) | 4.532 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s21 | 2 | decline | decline | correct_decline | unknown | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 17.569 (1.35) | 4.532 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s21 | 0 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 17.569 (1.35) | 4.532 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s21 | 1 | decline | decline | correct_decline | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 17.569 (1.35) | 4.532 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s21 | 2 | decline | decline | correct_decline | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 17.569 (1.35) | 4.532 |
| script | v3_growth_zone_partial_occlusion_z20_s22 | 0 | decline | accept | false_accept | - | 1 | none | 14.931 (1.35) | 9.388 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s22 | 0 | decline | accept | false_accept | width_change | 4 | tracker disk radius 14 -> 21 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 7.685 (1.35) | 8.595 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s22 | 0 | decline | decline | correct_decline | midline_jitter | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.931 (1.35) | 9.388 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s22 | 1 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 14.931 (1.35) | 9.388 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s22 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 14.931 (1.35) | 9.388 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s22 | 0 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.931 (1.35) | 9.388 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s22 | 1 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.931 (1.35) | 9.388 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s22 | 2 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.931 (1.35) | 9.388 |
