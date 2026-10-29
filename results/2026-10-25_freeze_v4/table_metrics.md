# Freeze v4 scored runs: metrics

51 rods: accept_clean 18, accept_repaired 9, decline 24. LLM methods 3 repeats; values are the mean over repeats, (min-max) where they differ. Seeds 26-28, candidate v4 on. Definitions as freeze v3 (`docs/proposals/2026-10-23_freeze-v3.md`, section 3); code `measure/metrics.py`.

| Method | Runs | Balanced accuracy | Acc. accept_clean | Acc. accept_repaired | Acc. decline | Overall | False accepts | False-accept rate | Coverage | Abst. precision | Abst. recall | not_reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| script | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 0.53 | 18.0 | 0.35 | 1.00 | - | 0.00 | 0 |
| remedy_tree | 51 | 0.93 | 1.00 | 1.00 | 0.79 | 0.90 | 2.0 | 0.06 | 0.63 | 1.00 | 0.79 | 0 |
| diagnostician | 153 | 0.93 (0.92-0.94) | 1.00 | 1.00 | 0.79 (0.75-0.83) | 0.90 (0.88-0.92) | 0.0 | 0.00 | 0.58 (0.57-0.59) | 1.00 | 0.79 (0.75-0.83) | 7 |
| single_agent | 153 | 0.63 (0.58-0.69) | 0.83 (0.78-0.89) | 0.96 (0.89-1.00) | 0.10 (0.04-0.17) | 0.51 (0.47-0.57) | 0.3 (0.0-1.0) | 0.01 (0.00-0.04) | 0.48 (0.43-0.55) | 0.50 (0.33-0.67) | 0.10 (0.04-0.17) | 66 |
| all_decline | 51 | 0.33 | 0.00 | 0.00 | 1.00 | 0.47 | 0.0 | - | 0.00 | 0.47 | 1.00 | 0 |
| all_accept | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 0.53 | 18.0 | 0.35 | 1.00 | - | 0.00 | 0 |

## Agreement across repeats (LLM methods)

| Method | Rods | Unanimous | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |
| :-- | --: | --: | :-- | :-- | :-- | :-- | :-- |
| diagnostician | 51 | 46 | 0.90 | 1.00 | 1.00 | 0.79 | 0.887 |
| single_agent | 51 | 34 | 0.67 | 0.56 | 0.89 | 0.67 | 0.626 |

## Categories, remedies kept, unnecessary declines (summed over repeats)

| Method | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | accept_on_decline | Runs keeping a remedy, accept_clean | Unnecessary-decline rate accept_clean / accept_repaired | Fault named correct |
| :-- | --: | --: | --: | --: | --: | --: | --: | :-- | :-- |
| script | 27 | 18 | 0 | 0 | 0 | 6 | 0 | 0.00 / 0.00 | 0 of 33 |
| remedy_tree | 27 | 2 | 19 | 0 | 0 | 3 | 0 | 0.00 / 0.00 | 16 of 33 |
| diagnostician | 81 | 0 | 57 | 0 | 7 | 8 | 2 | 0.00 / 0.00 | 54 of 99 |
| single_agent | 71 | 1 | 7 | 6 | 66 | 2 | 23 | 0.11 / 0.00 | 39 of 99 |
| all_decline | 0 | 0 | 24 | 27 | 0 | 0 | 0 | 1.00 / 1.00 | 0 of 0 |
| all_accept | 27 | 18 | 0 | 0 | 0 | 6 | 0 | 0.00 / 0.00 | 0 of 0 |

## Per row of the set (correct runs / runs)

| Row | Class | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| v3_bend16 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_bend20 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 7 / 9 |
| v3_bend24 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 8 / 9 |
| v3_bend30 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_still | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| rigid_drift | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| displacement_exceeds_patch | decline | 0 / 3 | 3 / 3 | 7 / 9 | 0 / 9 |
| width_change | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| low_texture | decline | 0 / 3 | 3 / 3 | 9 / 9 | 0 / 9 |
| midline_jitter | decline | 0 / 3 | 3 / 3 | 7 / 9 | 0 / 9 |
| bad_stage_correction | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 8 / 9 |
| stage_log_missing | decline | 0 / 3 | 3 / 3 | 9 / 9 | 0 / 9 |
| second_root | decline | 0 / 3 | 0 / 3 | 1 / 9 | 0 / 9 |
| fast_rotation | decline | 0 / 3 | 3 / 3 | 6 / 9 | 2 / 9 |
| flank_swap | decline | 0 / 3 | 3 / 3 | 9 / 9 | 2 / 9 |
| partial_occlusion | decline | 0 / 3 | 1 / 3 | 9 / 9 | 3 / 9 |

## Cost (LLM methods, all repeats)

| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: |
| script | 51 | 51 | 0 | 0 | 0.0 |
| remedy_tree | 51 | 152 | 0 | 0 | 0.0 |
| diagnostician | 153 | 655 | 3061490 | 389197 | 4560.3 |
| single_agent | 153 | 1040 | 4790821 | 644251 | 7539.0 |

## Per run

| Method | Rod | Repeat | Class | Status | Category | Named fault | Steps | Remedies | Centre RMS (tol) | Flank RMS |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: |
| script | v3_growth_zone_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| remedy_tree | v3_growth_zone_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_clean_s26 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| single_agent | v3_growth_zone_clean_s26 | 0 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| single_agent | v3_growth_zone_clean_s26 | 1 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| single_agent | v3_growth_zone_clean_s26 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| script | v3_growth_zone_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| remedy_tree | v3_growth_zone_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| diagnostician | v3_growth_zone_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| diagnostician | v3_growth_zone_clean_s27 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| diagnostician | v3_growth_zone_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| single_agent | v3_growth_zone_clean_s27 | 0 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.318 (1.35) | 0.182 |
| single_agent | v3_growth_zone_clean_s27 | 1 | accept_clean | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.318 (1.35) | 0.182 |
| single_agent | v3_growth_zone_clean_s27 | 2 | accept_clean | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.318 (1.35) | 0.182 |
| script | v3_growth_zone_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| remedy_tree | v3_growth_zone_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| diagnostician | v3_growth_zone_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| diagnostician | v3_growth_zone_clean_s28 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| diagnostician | v3_growth_zone_clean_s28 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| single_agent | v3_growth_zone_clean_s28 | 0 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.336 (1.35) | 0.253 |
| single_agent | v3_growth_zone_clean_s28 | 1 | accept_clean | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.336 (1.35) | 0.253 |
| single_agent | v3_growth_zone_clean_s28 | 2 | accept_clean | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.336 (1.35) | 0.253 |
| script | v3_bend16_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.444 (1.35) | 0.341 |
| remedy_tree | v3_bend16_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.444 (1.35) | 0.341 |
| diagnostician | v3_bend16_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.444 (1.35) | 0.341 |
| diagnostician | v3_bend16_clean_s26 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.444 (1.35) | 0.341 |
| diagnostician | v3_bend16_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.444 (1.35) | 0.341 |
| single_agent | v3_bend16_clean_s26 | 0 | accept_clean | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 0.437 (1.35) | 0.279 |
| single_agent | v3_bend16_clean_s26 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.444 (1.35) | 0.341 |
| single_agent | v3_bend16_clean_s26 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.444 (1.35) | 0.341 |
| script | v3_bend16_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.446 (1.35) | 0.317 |
| remedy_tree | v3_bend16_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.446 (1.35) | 0.317 |
| diagnostician | v3_bend16_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.446 (1.35) | 0.317 |
| diagnostician | v3_bend16_clean_s27 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.446 (1.35) | 0.317 |
| diagnostician | v3_bend16_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.446 (1.35) | 0.317 |
| single_agent | v3_bend16_clean_s27 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.446 (1.35) | 0.317 |
| single_agent | v3_bend16_clean_s27 | 1 | accept_clean | accept | good_report | - | 7 | none | 0.446 (1.35) | 0.317 |
| single_agent | v3_bend16_clean_s27 | 2 | accept_clean | accept | good_report | - | 4 | none | 0.446 (1.35) | 0.317 |
| script | v3_bend16_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.353 |
| remedy_tree | v3_bend16_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.353 |
| diagnostician | v3_bend16_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.353 |
| diagnostician | v3_bend16_clean_s28 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.353 |
| diagnostician | v3_bend16_clean_s28 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.401 (1.35) | 0.353 |
| single_agent | v3_bend16_clean_s28 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.401 (1.35) | 0.353 |
| single_agent | v3_bend16_clean_s28 | 1 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.403 (1.35) | 0.364 |
| single_agent | v3_bend16_clean_s28 | 2 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.403 (1.35) | 0.364 |
| script | v3_bend20_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.47 (1.35) | 0.325 |
| remedy_tree | v3_bend20_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.47 (1.35) | 0.325 |
| diagnostician | v3_bend20_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.47 (1.35) | 0.325 |
| diagnostician | v3_bend20_clean_s26 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.47 (1.35) | 0.325 |
| diagnostician | v3_bend20_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.47 (1.35) | 0.325 |
| single_agent | v3_bend20_clean_s26 | 0 | accept_clean | accept | good_report | - | 4 | none | 0.47 (1.35) | 0.325 |
| single_agent | v3_bend20_clean_s26 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.47 (1.35) | 0.325 |
| single_agent | v3_bend20_clean_s26 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.47 (1.35) | 0.325 |
| script | v3_bend20_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.441 (1.35) | 0.373 |
| remedy_tree | v3_bend20_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.441 (1.35) | 0.373 |
| diagnostician | v3_bend20_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.441 (1.35) | 0.373 |
| diagnostician | v3_bend20_clean_s27 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.441 (1.35) | 0.373 |
| diagnostician | v3_bend20_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.441 (1.35) | 0.373 |
| single_agent | v3_bend20_clean_s27 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.441 (1.35) | 0.373 |
| single_agent | v3_bend20_clean_s27 | 1 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.461 (1.35) | 0.332 |
| single_agent | v3_bend20_clean_s27 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.441 (1.35) | 0.373 |
| script | v3_bend20_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.409 (1.35) | 0.476 |
| remedy_tree | v3_bend20_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.409 (1.35) | 0.476 |
| diagnostician | v3_bend20_clean_s28 | 0 | accept_clean | accept | good_report | bad_stage_correction | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.411 (1.35) | 0.404 |
| diagnostician | v3_bend20_clean_s28 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.409 (1.35) | 0.476 |
| diagnostician | v3_bend20_clean_s28 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.409 (1.35) | 0.476 |
| single_agent | v3_bend20_clean_s28 | 0 | accept_clean | decline | unnecessary_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.411 (1.35) | 0.404 |
| single_agent | v3_bend20_clean_s28 | 1 | accept_clean | accept | good_report | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.411 (1.35) | 0.404 |
| single_agent | v3_bend20_clean_s28 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.409 (1.35) | 0.476 |
| script | v3_bend24_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.487 (1.35) | 0.405 |
| remedy_tree | v3_bend24_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.487 (1.35) | 0.405 |
| diagnostician | v3_bend24_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.487 (1.35) | 0.405 |
| diagnostician | v3_bend24_clean_s26 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.487 (1.35) | 0.405 |
| diagnostician | v3_bend24_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.487 (1.35) | 0.405 |
| single_agent | v3_bend24_clean_s26 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.487 (1.35) | 0.405 |
| single_agent | v3_bend24_clean_s26 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.487 (1.35) | 0.405 |
| single_agent | v3_bend24_clean_s26 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.487 (1.35) | 0.405 |
| script | v3_bend24_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.464 (1.35) | 0.409 |
| remedy_tree | v3_bend24_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.464 (1.35) | 0.409 |
| diagnostician | v3_bend24_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.464 (1.35) | 0.409 |
| diagnostician | v3_bend24_clean_s27 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.464 (1.35) | 0.409 |
| diagnostician | v3_bend24_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.464 (1.35) | 0.409 |
| single_agent | v3_bend24_clean_s27 | 0 | accept_clean | decline | unnecessary_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.465 (1.35) | 0.407 |
| single_agent | v3_bend24_clean_s27 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.464 (1.35) | 0.409 |
| single_agent | v3_bend24_clean_s27 | 2 | accept_clean | accept | good_report | - | 5 | none | 0.464 (1.35) | 0.409 |
| script | v3_bend24_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.413 (1.35) | 0.534 |
| remedy_tree | v3_bend24_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.413 (1.35) | 0.534 |
| diagnostician | v3_bend24_clean_s28 | 0 | accept_clean | accept | good_report | - | 3 | none | 0.413 (1.35) | 0.534 |
| diagnostician | v3_bend24_clean_s28 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.413 (1.35) | 0.534 |
| diagnostician | v3_bend24_clean_s28 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.413 (1.35) | 0.534 |
| single_agent | v3_bend24_clean_s28 | 0 | accept_clean | accept | good_report | - | 4 | none | 0.413 (1.35) | 0.534 |
| single_agent | v3_bend24_clean_s28 | 1 | accept_clean | accept | good_report | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.403 (1.35) | 0.493 |
| single_agent | v3_bend24_clean_s28 | 2 | accept_clean | accept | good_report | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.403 (1.35) | 0.493 |
| script | v3_bend30_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.49 (1.35) | 0.466 |
| remedy_tree | v3_bend30_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.49 (1.35) | 0.466 |
| diagnostician | v3_bend30_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.49 (1.35) | 0.466 |
| diagnostician | v3_bend30_clean_s26 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.49 (1.35) | 0.466 |
| diagnostician | v3_bend30_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.49 (1.35) | 0.466 |
| single_agent | v3_bend30_clean_s26 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.49 (1.35) | 0.466 |
| single_agent | v3_bend30_clean_s26 | 1 | accept_clean | accept | good_report | - | 4 | none | 0.49 (1.35) | 0.466 |
| single_agent | v3_bend30_clean_s26 | 2 | accept_clean | decline | unnecessary_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.497 (1.35) | 0.421 |
| script | v3_bend30_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.52 (1.35) | 0.441 |
| remedy_tree | v3_bend30_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.52 (1.35) | 0.441 |
| diagnostician | v3_bend30_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.52 (1.35) | 0.441 |
| diagnostician | v3_bend30_clean_s27 | 1 | accept_clean | accept | good_report | - | 3 | none | 0.52 (1.35) | 0.441 |
| diagnostician | v3_bend30_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.52 (1.35) | 0.441 |
| single_agent | v3_bend30_clean_s27 | 0 | accept_clean | accept | good_report | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.529 (1.35) | 0.433 |
| single_agent | v3_bend30_clean_s27 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.52 (1.35) | 0.441 |
| single_agent | v3_bend30_clean_s27 | 2 | accept_clean | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.529 (1.35) | 0.433 |
| script | v3_bend30_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.431 (1.35) | 0.531 |
| remedy_tree | v3_bend30_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.431 (1.35) | 0.531 |
| diagnostician | v3_bend30_clean_s28 | 0 | accept_clean | accept | good_report | bad_stage_correction | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.565 |
| diagnostician | v3_bend30_clean_s28 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.431 (1.35) | 0.531 |
| diagnostician | v3_bend30_clean_s28 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.431 (1.35) | 0.531 |
| single_agent | v3_bend30_clean_s28 | 0 | accept_clean | accept | good_report | - | 5 | none | 0.431 (1.35) | 0.531 |
| single_agent | v3_bend30_clean_s28 | 1 | accept_clean | accept | good_report | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.565 |
| single_agent | v3_bend30_clean_s28 | 2 | accept_clean | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.446 (1.35) | 0.565 |
| script | v3_still_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.14 (0.5) | 0.202 |
| remedy_tree | v3_still_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.14 (0.5) | 0.202 |
| diagnostician | v3_still_clean_s26 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.14 (0.5) | 0.202 |
| diagnostician | v3_still_clean_s26 | 1 | accept_clean | accept | good_report | - | 4 | none | 0.14 (0.5) | 0.202 |
| diagnostician | v3_still_clean_s26 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.14 (0.5) | 0.202 |
| single_agent | v3_still_clean_s26 | 0 | accept_clean | accept | good_report | - | 4 | none | 0.14 (0.5) | 0.202 |
| single_agent | v3_still_clean_s26 | 1 | accept_clean | accept | good_report | - | 6 | none | 0.14 (0.5) | 0.202 |
| single_agent | v3_still_clean_s26 | 2 | accept_clean | accept | good_report | - | 4 | none | 0.14 (0.5) | 0.202 |
| script | v3_still_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.136 (0.5) | 0.267 |
| remedy_tree | v3_still_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.136 (0.5) | 0.267 |
| diagnostician | v3_still_clean_s27 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.136 (0.5) | 0.267 |
| diagnostician | v3_still_clean_s27 | 1 | accept_clean | accept | good_report | - | 1 | none | 0.136 (0.5) | 0.267 |
| diagnostician | v3_still_clean_s27 | 2 | accept_clean | accept | good_report | - | 1 | none | 0.136 (0.5) | 0.267 |
| single_agent | v3_still_clean_s27 | 0 | accept_clean | accept | good_report | - | 4 | none | 0.136 (0.5) | 0.267 |
| single_agent | v3_still_clean_s27 | 1 | accept_clean | accept | good_report | - | 5 | none | 0.136 (0.5) | 0.267 |
| single_agent | v3_still_clean_s27 | 2 | accept_clean | accept | good_report | - | 4 | none | 0.136 (0.5) | 0.267 |
| script | v3_still_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.192 (0.5) | 0.182 |
| remedy_tree | v3_still_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.192 (0.5) | 0.182 |
| diagnostician | v3_still_clean_s28 | 0 | accept_clean | accept | good_report | - | 1 | none | 0.192 (0.5) | 0.182 |
| diagnostician | v3_still_clean_s28 | 1 | accept_clean | accept | good_report | - | 2 | none | 0.192 (0.5) | 0.182 |
| diagnostician | v3_still_clean_s28 | 2 | accept_clean | accept | good_report | - | 4 | none | 0.192 (0.5) | 0.182 |
| single_agent | v3_still_clean_s28 | 0 | accept_clean | accept | good_report | - | 6 | none | 0.192 (0.5) | 0.182 |
| single_agent | v3_still_clean_s28 | 1 | accept_clean | accept | good_report | - | 4 | none | 0.192 (0.5) | 0.182 |
| single_agent | v3_still_clean_s28 | 2 | accept_clean | accept | good_report | - | 6 | none | 0.192 (0.5) | 0.182 |
| script | v3_growth_zone_rigid_drift_z0.5_s26 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.375 (1.35) | 0.231 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s26 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.396 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s26 | 0 | accept_repaired | accept | good_report | rigid_drift | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.396 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s26 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.396 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s26 | 2 | accept_repaired | accept | good_report | width_change | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.396 (1.35) | 0.19 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s26 | 0 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.396 (1.35) | 0.19 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s26 | 1 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.396 (1.35) | 0.19 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s26 | 2 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.396 (1.35) | 0.19 |
| script | v3_growth_zone_rigid_drift_z0.5_s27 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.344 (1.35) | 0.231 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s27 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.38 (1.35) | 0.198 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s27 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.38 (1.35) | 0.198 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s27 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.38 (1.35) | 0.198 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s27 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.38 (1.35) | 0.198 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s27 | 0 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.38 (1.35) | 0.198 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s27 | 1 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.38 (1.35) | 0.198 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s27 | 2 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.38 (1.35) | 0.198 |
| script | v3_growth_zone_rigid_drift_z0.5_s28 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.362 (1.35) | 0.335 |
| remedy_tree | v3_growth_zone_rigid_drift_z0.5_s28 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.352 (1.35) | 0.406 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s28 | 0 | accept_repaired | accept | good_report | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.352 (1.35) | 0.406 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s28 | 1 | accept_repaired | accept | good_report | width_change | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.352 (1.35) | 0.406 |
| diagnostician | v3_growth_zone_rigid_drift_z0.5_s28 | 2 | accept_repaired | accept | good_report | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.352 (1.35) | 0.406 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s28 | 0 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.352 (1.35) | 0.406 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s28 | 1 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.352 (1.35) | 0.406 |
| single_agent | v3_growth_zone_rigid_drift_z0.5_s28 | 2 | accept_repaired | accept | good_report | width_change | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.352 (1.35) | 0.406 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 0 | decline | accept | false_accept | - | 1 | none | 66.589 (2.698) | 70.801 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 0 | decline | decline | correct_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 360 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 360 px from the tip) before tracking; frame stride 6 -> 3; rolled back: frame stride 6 -> 3; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 66.589 (2.698) | 70.801 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 0 | decline | step_limit | not_reported | bad_stage_correction | 8 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 360 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 360 px from the tip) before tracking | 66.589 (2.698) | 70.801 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 1 | decline | decline | correct_decline | bad_stage_correction | 7 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; frames registered on the non-growing tissue (from 360 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 360 px from the tip) before tracking | 66.589 (2.698) | 70.801 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; midline source smoothed (light); rolled back: midline source smoothed (light) | 66.589 (2.698) | 70.801 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 0 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 3.673 (2.698) | 18.158 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 360 px from the tip) before tracking; frame stride 6 -> 3 | 57.329 (2.698) | 56.443 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | 2 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 360 px from the tip) before tracking; frame stride 6 -> 3 | 57.329 (2.698) | 56.443 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 0 | decline | accept | false_accept | - | 1 | none | 68.813 (2.698) | 88.995 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 0 | decline | decline | correct_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 325 px from the tip) before tracking; frame stride 6 -> 3; rolled back: frame stride 6 -> 3; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 60.335 (2.698) | 49.159 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 0 | decline | decline | correct_decline | displacement_exceeds_patch | 7 | frame stride 6 -> 3; frame stride 3 -> 1 | 4.795 (2.698) | 0.245 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 1 | decline | decline | correct_decline | displacement_exceeds_patch | 7 | frame stride 6 -> 3; frame stride 3 -> 1 | 4.795 (2.698) | 0.245 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 2 | decline | decline | correct_decline | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 4.795 (2.698) | 0.245 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 0 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 325 px from the tip) before tracking; frame stride 6 -> 3 | 47.124 (2.698) | 41.307 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frame stride 6 -> 3; frame stride 3 -> 1 | 4.795 (2.698) | 0.245 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | 2 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 325 px from the tip) before tracking; frame stride 6 -> 3 | 47.124 (2.698) | 41.307 |
| script | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 0 | decline | accept | false_accept | - | 1 | none | 71.718 (2.698) | 59.957 |
| remedy_tree | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 0 | decline | decline | correct_decline | low_texture | 6 | frames registered on the non-growing tissue (from 375 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 375 px from the tip) before tracking; frame stride 6 -> 3; rolled back: frame stride 6 -> 3; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 47.374 (2.698) | 49.459 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 0 | decline | decline | correct_decline | midline_jitter | 7 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; midline source smoothed (light) | 52.514 (2.698) | 68.278 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 1 | decline | decline | correct_decline | midline_jitter | 6 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; midline source smoothed (light) | 52.514 (2.698) | 68.278 |
| diagnostician | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 2 | decline | decline | correct_decline | midline_jitter | 8 | frame stride 6 -> 3; rolled back: frame stride 6 -> 3; frames registered on the non-growing tissue (from 375 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 375 px from the tip) before tracking; midline source smoothed (light) | 52.514 (2.698) | 68.278 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 0 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 375 px from the tip) before tracking; frame stride 6 -> 3 | 60.01 (2.698) | 61.144 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 1 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | frames registered on the non-growing tissue (from 375 px from the tip) before tracking; frame stride 6 -> 3 | 60.01 (2.698) | 61.144 |
| single_agent | v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | frame stride 6 -> 3; frames registered on the non-growing tissue (from 360 px from the tip) before tracking | 51.372 (2.698) | 52.298 |
| script | v3_growth_zone_width_change_s26 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.357 (1.35) | 0.255 |
| remedy_tree | v3_growth_zone_width_change_s26 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_width_change_s26 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_width_change_s26 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_width_change_s26 | 2 | accept_repaired | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| single_agent | v3_growth_zone_width_change_s26 | 0 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| single_agent | v3_growth_zone_width_change_s26 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| single_agent | v3_growth_zone_width_change_s26 | 2 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.357 (1.35) | 0.255 |
| script | v3_growth_zone_width_change_s27 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.331 (1.35) | 0.26 |
| remedy_tree | v3_growth_zone_width_change_s27 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| diagnostician | v3_growth_zone_width_change_s27 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| diagnostician | v3_growth_zone_width_change_s27 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| diagnostician | v3_growth_zone_width_change_s27 | 2 | accept_repaired | accept | good_report | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| single_agent | v3_growth_zone_width_change_s27 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| single_agent | v3_growth_zone_width_change_s27 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| single_agent | v3_growth_zone_width_change_s27 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.331 (1.35) | 0.26 |
| script | v3_growth_zone_width_change_s28 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.328 (1.35) | 0.293 |
| remedy_tree | v3_growth_zone_width_change_s28 | 0 | accept_repaired | accept | good_report | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| diagnostician | v3_growth_zone_width_change_s28 | 0 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| diagnostician | v3_growth_zone_width_change_s28 | 1 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| diagnostician | v3_growth_zone_width_change_s28 | 2 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| single_agent | v3_growth_zone_width_change_s28 | 0 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| single_agent | v3_growth_zone_width_change_s28 | 1 | accept_repaired | accept | good_report | width_change | 4 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| single_agent | v3_growth_zone_width_change_s28 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.328 (1.35) | 0.293 |
| script | v3_growth_zone_low_texture_z0.03_s26 | 0 | decline | accept | false_accept | - | 1 | none | 26.171 (1.35) | 50.456 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s26 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 540 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 540 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 12.01 (1.35) | 17.736 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s26 | 0 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s26 | 1 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s26 | 2 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| single_agent | v3_growth_zone_low_texture_z0.03_s26 | 0 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| single_agent | v3_growth_zone_low_texture_z0.03_s26 | 1 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| single_agent | v3_growth_zone_low_texture_z0.03_s26 | 2 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.01 (1.35) | 17.736 |
| script | v3_growth_zone_low_texture_z0.03_s27 | 0 | decline | accept | false_accept | - | 1 | none | 20.649 (1.35) | 32.259 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s27 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 12.625 (1.35) | 16.019 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s27 | 0 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s27 | 1 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s27 | 2 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| single_agent | v3_growth_zone_low_texture_z0.03_s27 | 0 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| single_agent | v3_growth_zone_low_texture_z0.03_s27 | 1 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| single_agent | v3_growth_zone_low_texture_z0.03_s27 | 2 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.625 (1.35) | 16.019 |
| script | v3_growth_zone_low_texture_z0.03_s28 | 0 | decline | accept | false_accept | - | 1 | none | 21.98 (1.35) | 72.35 |
| remedy_tree | v3_growth_zone_low_texture_z0.03_s28 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 550 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 12.718 (1.35) | 20.189 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s28 | 0 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s28 | 1 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| diagnostician | v3_growth_zone_low_texture_z0.03_s28 | 2 | decline | decline | correct_decline | low_texture | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| single_agent | v3_growth_zone_low_texture_z0.03_s28 | 0 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| single_agent | v3_growth_zone_low_texture_z0.03_s28 | 1 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| single_agent | v3_growth_zone_low_texture_z0.03_s28 | 2 | decline | step_limit | not_reported | low_texture | 8 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 12.718 (1.35) | 20.189 |
| script | v3_growth_zone_midline_jitter_z3_s26 | 0 | decline | accept | accept_on_decline | - | 1 | none | 1.034 (1.35) | 0.542 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s26 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 405 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 405 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 1.034 (1.35) | 0.542 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s26 | 0 | decline | step_limit | not_reported | displacement_exceeds_patch | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 405 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 1.034 (1.35) | 0.542 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s26 | 1 | decline | decline | correct_decline | midline_jitter | 8 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1.034 (1.35) | 0.542 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s26 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 405 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 405 px from the tip) before tracking | 1.034 (1.35) | 0.542 |
| single_agent | v3_growth_zone_midline_jitter_z3_s26 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.836 (1.35) | 0.501 |
| single_agent | v3_growth_zone_midline_jitter_z3_s26 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.836 (1.35) | 0.501 |
| single_agent | v3_growth_zone_midline_jitter_z3_s26 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.836 (1.35) | 0.501 |
| script | v3_growth_zone_midline_jitter_z3_s27 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.442 (1.35) | 0.431 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s27 | 0 | decline | decline | correct_decline | midline_jitter | 5 | frames registered on the non-growing tissue (from 410 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 410 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s27 | 0 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light); frames registered on the non-growing tissue (from 395 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 395 px from the tip) before tracking | 0.366 (1.35) | 0.349 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s27 | 1 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s27 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| single_agent | v3_growth_zone_midline_jitter_z3_s27 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| single_agent | v3_growth_zone_midline_jitter_z3_s27 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| single_agent | v3_growth_zone_midline_jitter_z3_s27 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.366 (1.35) | 0.349 |
| script | v3_growth_zone_midline_jitter_z3_s28 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.531 (1.35) | 0.414 |
| remedy_tree | v3_growth_zone_midline_jitter_z3_s28 | 0 | decline | decline | correct_decline | midline_jitter | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s28 | 0 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s28 | 1 | decline | decline | correct_decline | midline_jitter | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| diagnostician | v3_growth_zone_midline_jitter_z3_s28 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| single_agent | v3_growth_zone_midline_jitter_z3_s28 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| single_agent | v3_growth_zone_midline_jitter_z3_s28 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| single_agent | v3_growth_zone_midline_jitter_z3_s28 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 0.38 (1.35) | 0.358 |
| script | v3_growth_zone_bad_stage_correction_z3_s26 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.341 (1.35) | 0.181 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s26 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.209 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s26 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.209 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s26 | 1 | accept_repaired | accept | good_report | width_change | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.359 (1.35) | 0.209 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s26 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.359 (1.35) | 0.209 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s26 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s26 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s26 | 2 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.341 (1.35) | 0.181 |
| script | v3_growth_zone_bad_stage_correction_z3_s27 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.318 (1.35) | 0.182 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s27 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.333 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s27 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.333 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s27 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.333 (1.35) | 0.19 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s27 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.333 (1.35) | 0.19 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s27 | 0 | accept_repaired | accept | good_report | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.318 (1.35) | 0.182 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s27 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.318 (1.35) | 0.182 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s27 | 2 | accept_repaired | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.333 (1.35) | 0.19 |
| script | v3_growth_zone_bad_stage_correction_z3_s28 | 0 | accept_repaired | accept | good_report | - | 1 | none | 0.336 (1.35) | 0.253 |
| remedy_tree | v3_growth_zone_bad_stage_correction_z3_s28 | 0 | accept_repaired | accept | good_report | rigid_drift | 2 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.243 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s28 | 0 | accept_repaired | accept | good_report | bad_stage_correction | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.243 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s28 | 1 | accept_repaired | accept | good_report | bad_stage_correction | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.243 |
| diagnostician | v3_growth_zone_bad_stage_correction_z3_s28 | 2 | accept_repaired | accept | good_report | bad_stage_correction | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.343 (1.35) | 0.243 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s28 | 0 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.336 (1.35) | 0.253 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s28 | 1 | accept_repaired | accept | good_report | width_change | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.336 (1.35) | 0.253 |
| single_agent | v3_growth_zone_bad_stage_correction_z3_s28 | 2 | accept_repaired | accept | good_report | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.343 (1.35) | 0.243 |
| script | v3_growth_zone_stage_log_missing_z1_s26 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.341 (1.35) | 0.184 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s26 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.341 (1.35) | 0.184 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s26 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.341 (1.35) | 0.184 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s26 | 1 | decline | decline | correct_decline | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.341 (1.35) | 0.184 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s26 | 2 | decline | decline | correct_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.341 (1.35) | 0.184 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s26 | 0 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.363 (1.35) | 0.219 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s26 | 1 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.363 (1.35) | 0.219 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s26 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.363 (1.35) | 0.219 |
| script | v3_growth_zone_stage_log_missing_z1_s27 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.318 (1.35) | 0.181 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s27 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.318 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s27 | 0 | decline | decline | correct_decline | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.318 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s27 | 1 | decline | decline | correct_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.318 (1.35) | 0.181 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s27 | 2 | decline | decline | correct_decline | rigid_drift | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.318 (1.35) | 0.181 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s27 | 0 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.199 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s27 | 1 | decline | accept | accept_on_decline | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.347 (1.35) | 0.199 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s27 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.347 (1.35) | 0.199 |
| script | v3_growth_zone_stage_log_missing_z1_s28 | 0 | decline | accept | accept_on_decline | - | 1 | none | 0.337 (1.35) | 0.255 |
| remedy_tree | v3_growth_zone_stage_log_missing_z1_s28 | 0 | decline | decline | correct_decline | rigid_drift | 5 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; rolled back: tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 0.337 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s28 | 0 | decline | decline | correct_decline | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.337 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s28 | 1 | decline | decline | correct_decline | rigid_drift | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.337 (1.35) | 0.255 |
| diagnostician | v3_growth_zone_stage_log_missing_z1_s28 | 2 | decline | decline | correct_decline | rigid_drift | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.337 (1.35) | 0.255 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s28 | 0 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.351 (1.35) | 0.255 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s28 | 1 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.351 (1.35) | 0.255 |
| single_agent | v3_growth_zone_stage_log_missing_z1_s28 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0.351 (1.35) | 0.255 |
| script | v3_growth_zone_second_root_z30_s26 | 0 | decline | accept | false_accept | - | 1 | none | 0.656 (1.35) | 1.908 |
| remedy_tree | v3_growth_zone_second_root_z30_s26 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| diagnostician | v3_growth_zone_second_root_z30_s26 | 0 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| diagnostician | v3_growth_zone_second_root_z30_s26 | 1 | decline | decline | correct_decline | second_root | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames limited to the main root (mask_second_root) | 0.656 (1.35) | 1.908 |
| diagnostician | v3_growth_zone_second_root_z30_s26 | 2 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| single_agent | v3_growth_zone_second_root_z30_s26 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| single_agent | v3_growth_zone_second_root_z30_s26 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| single_agent | v3_growth_zone_second_root_z30_s26 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.656 (1.35) | 1.908 |
| script | v3_growth_zone_second_root_z30_s27 | 0 | decline | accept | false_accept | - | 1 | none | 0.506 (1.35) | 2.055 |
| remedy_tree | v3_growth_zone_second_root_z30_s27 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| diagnostician | v3_growth_zone_second_root_z30_s27 | 0 | decline | accept | accept_on_decline | second_root | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames limited to the main root (mask_second_root) | 0.506 (1.35) | 2.055 |
| diagnostician | v3_growth_zone_second_root_z30_s27 | 1 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| diagnostician | v3_growth_zone_second_root_z30_s27 | 2 | decline | accept | accept_on_decline | width_change | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| single_agent | v3_growth_zone_second_root_z30_s27 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| single_agent | v3_growth_zone_second_root_z30_s27 | 1 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| single_agent | v3_growth_zone_second_root_z30_s27 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.506 (1.35) | 2.055 |
| script | v3_growth_zone_second_root_z30_s28 | 0 | decline | accept | false_accept | - | 1 | none | 0.608 (1.35) | 2.927 |
| remedy_tree | v3_growth_zone_second_root_z30_s28 | 0 | decline | accept | accept_on_decline | width_change | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| diagnostician | v3_growth_zone_second_root_z30_s28 | 0 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| diagnostician | v3_growth_zone_second_root_z30_s28 | 1 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| diagnostician | v3_growth_zone_second_root_z30_s28 | 2 | decline | accept | accept_on_decline | width_change | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| single_agent | v3_growth_zone_second_root_z30_s28 | 0 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| single_agent | v3_growth_zone_second_root_z30_s28 | 1 | decline | accept | accept_on_decline | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| single_agent | v3_growth_zone_second_root_z30_s28 | 2 | decline | step_limit | not_reported | width_change | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0.608 (1.35) | 2.927 |
| script | v3_growth_zone_fast_rotation_z2_s26 | 0 | decline | accept | false_accept | - | 1 | none | 35.121 (1.35) | 26.163 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s26 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 565 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 565 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 32.412 (1.35) | 16.252 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s26 | 0 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 18.513 (1.35) | 28.585 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s26 | 1 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light) | 18.513 (1.35) | 28.585 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s26 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 18.513 (1.35) | 28.585 |
| single_agent | v3_growth_zone_fast_rotation_z2_s26 | 0 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 565 px from the tip) before tracking | 33.712 (1.35) | 31.718 |
| single_agent | v3_growth_zone_fast_rotation_z2_s26 | 1 | decline | decline | correct_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 565 px from the tip) before tracking | 33.712 (1.35) | 31.718 |
| single_agent | v3_growth_zone_fast_rotation_z2_s26 | 2 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 565 px from the tip) before tracking | 33.712 (1.35) | 31.718 |
| script | v3_growth_zone_fast_rotation_z2_s27 | 0 | decline | accept | false_accept | - | 1 | none | 35.399 (1.35) | 28.726 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s27 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 13.565 (1.35) | 20.605 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s27 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 27.542 (1.35) | 40.824 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s27 | 1 | decline | step_limit | not_reported | rigid_drift | 8 | midline source smoothed (light); frames registered on the non-growing tissue (from 560 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 27.542 (1.35) | 40.824 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s27 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 27.542 (1.35) | 40.824 |
| single_agent | v3_growth_zone_fast_rotation_z2_s27 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 27.542 (1.35) | 40.824 |
| single_agent | v3_growth_zone_fast_rotation_z2_s27 | 1 | decline | decline | correct_decline | rigid_drift | 8 | frames registered on the non-growing tissue (from 560 px from the tip) before tracking | 34.641 (1.35) | 25.595 |
| single_agent | v3_growth_zone_fast_rotation_z2_s27 | 2 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 27.542 (1.35) | 40.824 |
| script | v3_growth_zone_fast_rotation_z2_s28 | 0 | decline | accept | false_accept | - | 1 | none | 20.792 (1.35) | 37.696 |
| remedy_tree | v3_growth_zone_fast_rotation_z2_s28 | 0 | decline | decline | correct_decline | low_texture | 5 | frames registered on the non-growing tissue (from 570 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 570 px from the tip) before tracking; tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 23.367 (1.35) | 17.38 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s28 | 0 | decline | step_limit | not_reported | second_root | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 20.792 (1.35) | 37.696 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s28 | 1 | decline | step_limit | not_reported | rigid_drift | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); frames registered on the non-growing tissue (from 570 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 570 px from the tip) before tracking | 20.792 (1.35) | 37.696 |
| diagnostician | v3_growth_zone_fast_rotation_z2_s28 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 20.792 (1.35) | 37.696 |
| single_agent | v3_growth_zone_fast_rotation_z2_s28 | 0 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 20.777 (1.35) | 35.021 |
| single_agent | v3_growth_zone_fast_rotation_z2_s28 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 20.777 (1.35) | 35.021 |
| single_agent | v3_growth_zone_fast_rotation_z2_s28 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 570 px from the tip) before tracking | 20.198 (1.35) | 36.73 |
| script | v3_growth_zone_flank_swap_z0.5_s26 | 0 | decline | accept | false_accept | - | 1 | none | 6.582 (1.35) | 28.713 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s26 | 0 | decline | decline | correct_decline | low_texture | 5 | tracker disk radius 14 -> 21 px; frames registered on the non-growing tissue (from 530 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 530 px from the tip) before tracking; tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 3.705 (1.35) | 32.486 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s26 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 6.582 (1.35) | 28.713 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s26 | 1 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light); rolled back: midline source smoothed (light) | 6.582 (1.35) | 28.713 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s26 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 6.582 (1.35) | 28.713 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s26 | 0 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 525 px from the tip) before tracking | 88.275 (1.35) | 113.06 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s26 | 1 | decline | step_limit | not_reported | midline_jitter | 8 | midline source smoothed (light) | 5.509 (1.35) | 28.007 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s26 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 525 px from the tip) before tracking | 88.275 (1.35) | 113.06 |
| script | v3_growth_zone_flank_swap_z0.5_s27 | 0 | decline | accept | false_accept | - | 1 | none | 8.173 (1.35) | 25.607 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s27 | 0 | decline | decline | correct_decline | low_texture | 4 | tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 2.99 (1.35) | 29.208 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s27 | 0 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light); rolled back: midline source smoothed (light) | 8.173 (1.35) | 25.607 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s27 | 1 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 8.173 (1.35) | 25.607 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s27 | 2 | decline | decline | correct_decline | midline_jitter | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 8.173 (1.35) | 25.607 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s27 | 0 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 37.147 (1.35) | 54.271 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s27 | 1 | decline | decline | correct_decline | bad_stage_correction | 7 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 37.147 (1.35) | 54.271 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s27 | 2 | decline | decline | correct_decline | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 550 px from the tip) before tracking | 37.147 (1.35) | 54.271 |
| script | v3_growth_zone_flank_swap_z0.5_s28 | 0 | decline | accept | false_accept | - | 1 | none | 4.53 (1.35) | 38.256 |
| remedy_tree | v3_growth_zone_flank_swap_z0.5_s28 | 0 | decline | decline | correct_decline | low_texture | 5 | tracker disk radius 14 -> 21 px; frames registered on the non-growing tissue (from 540 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 540 px from the tip) before tracking; tracker disk radius 21 -> 28 px; rolled back: tracker disk radius 21 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 5.592 (1.35) | 31.179 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s28 | 0 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light) | 6.875 (1.35) | 21.621 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s28 | 1 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 6.875 (1.35) | 21.621 |
| diagnostician | v3_growth_zone_flank_swap_z0.5_s28 | 2 | decline | decline | correct_decline | midline_jitter | 7 | midline source smoothed (light) | 6.875 (1.35) | 21.621 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s28 | 0 | decline | step_limit | not_reported | rigid_drift | 8 | frames registered on the non-growing tissue (from 525 px from the tip) before tracking | 10.503 (1.35) | 36.99 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s28 | 1 | decline | accept | false_accept | - | 7 | none | 4.53 (1.35) | 38.256 |
| single_agent | v3_growth_zone_flank_swap_z0.5_s28 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | frames registered on the non-growing tissue (from 525 px from the tip) before tracking | 10.503 (1.35) | 36.99 |
| script | v3_growth_zone_partial_occlusion_z20_s26 | 0 | decline | accept | false_accept | - | 1 | none | 14.926 (1.35) | 2.195 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s26 | 0 | decline | accept | false_accept | low_texture | 3 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 4.961 (1.35) | 0.504 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s26 | 0 | decline | decline | correct_decline | width_change | 7 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.926 (1.35) | 2.195 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s26 | 1 | decline | decline | correct_decline | unknown | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 14.926 (1.35) | 2.195 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s26 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 14.926 (1.35) | 2.195 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s26 | 0 | decline | step_limit | not_reported | width_change | 8 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; report the centre strain rate and the width-free ratio; plane-sections check skipped | 26.822 (1.35) | 2.626 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s26 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 26.822 (1.35) | 2.626 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s26 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 26.822 (1.35) | 2.626 |
| script | v3_growth_zone_partial_occlusion_z20_s27 | 0 | decline | accept | false_accept | - | 1 | none | 43.716 (1.35) | 6.622 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s27 | 0 | decline | decline | correct_decline | low_texture | 4 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 4.594 (1.35) | 3.732 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s27 | 0 | decline | decline | correct_decline | unknown | 7 | none | 43.716 (1.35) | 6.622 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s27 | 1 | decline | decline | correct_decline | unknown | 6 | none | 43.716 (1.35) | 6.622 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s27 | 2 | decline | decline | correct_decline | unknown | 6 | none | 43.716 (1.35) | 6.622 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s27 | 0 | decline | step_limit | not_reported | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 43.716 (1.35) | 6.622 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s27 | 1 | decline | decline | correct_decline | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 43.716 (1.35) | 6.622 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s27 | 2 | decline | decline | correct_decline | width_change | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 43.716 (1.35) | 6.622 |
| script | v3_growth_zone_partial_occlusion_z20_s28 | 0 | decline | accept | false_accept | - | 1 | none | 21.964 (1.35) | 3.643 |
| remedy_tree | v3_growth_zone_partial_occlusion_z20_s28 | 0 | decline | accept | false_accept | width_change | 5 | tracker disk radius 14 -> 21 px; rolled back: tracker disk radius 14 -> 21 px; tracker disk radius 14 -> 28 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 8.58 (1.35) | 3.574 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s28 | 0 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 11.951 (1.35) | 3.252 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s28 | 1 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 11.951 (1.35) | 3.252 |
| diagnostician | v3_growth_zone_partial_occlusion_z20_s28 | 2 | decline | decline | correct_decline | midline_jitter | 5 | midline source smoothed (light) | 11.951 (1.35) | 3.252 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s28 | 0 | decline | decline | correct_decline | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 395 px from the tip) before tracking | 19.252 (1.35) | 3.577 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s28 | 1 | decline | step_limit | not_reported | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 395 px from the tip) before tracking | 19.252 (1.35) | 3.577 |
| single_agent | v3_growth_zone_partial_occlusion_z20_s28 | 2 | decline | step_limit | not_reported | bad_stage_correction | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 395 px from the tip) before tracking | 19.252 (1.35) | 3.577 |
