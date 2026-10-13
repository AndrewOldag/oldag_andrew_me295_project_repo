# Baselines on the development faults, scored against freeze v1

Scoring: `measure/score.py` unchanged; tolerance from `config/scoring_tolerance.yaml` (centre 0.025 x true peak, flank 0.5 %/h). Correct: good_report on a repairable rod, correct_decline on a not-repairable rod.

## Outcome per fault and method (seeds 0, 1, 2)
| Fault | Size | Label | Correct outcome | script | remedy_tree | diagnostician |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch | 2x6 | repairable | accept after the remedy | s0 false_accept; s1 false_accept; s2 false_accept | s0 good_report; s1 good_report; s2 good_report | s0 not_reported |
| width_change | 1/400 | repairable | accept with the width-free ratio | s0 good_report; s1 good_report; s2 good_report | s0 good_report; s1 good_report; s2 good_report | s0 unnecessary_decline |
| rigid_drift | 0.5 | repairable | accept after the remedy | s0 good_report; s1 good_report; s2 good_report | s0 good_report; s1 good_report; s2 good_report | s0 unnecessary_decline |
| low_texture | 0.03 | not repairable | decline | s0 false_accept; s1 false_accept; s2 false_accept | s0 correct_decline; s1 correct_decline; s2 correct_decline | s0 correct_decline |
| midline_jitter | 3 | not repairable | decline | s0 false_accept; s1 good_report; s2 false_accept | s0 correct_decline; s1 correct_decline; s2 correct_decline | s0 not_reported |

## Totals
| Method | Tasks | Correct | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | Fault named correctly | Steps | Remedies applied | Roll backs |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| script | 15 | 6 | 7 | 8 | 0 | 0 | 0 | 0 | 15 | 0 | 0 |
| remedy_tree | 15 | 15 | 9 | 0 | 6 | 0 | 0 | 15 | 57 | 42 | 20 |
| diagnostician | 5 | 1 | 0 | 0 | 1 | 2 | 2 | 1 | 37 | 6 | 0 |

## Per task
| Method | Fault | Seed | Status | Category | Steps | Named fault | Remedies | Roll backs | Centre RMS (%/h) | Centre tol | Flank RMS (%/h) |
| :-- | :-- | --: | :-- | :-- | --: | :-- | :-- | --: | --: | --: | --: |
| script | displacement_exceeds_patch | 0 | accept | false_accept | 1 | - | none | 0 | 34.666 | 2.173 | 43.488 |
| script | displacement_exceeds_patch | 1 | accept | false_accept | 1 | - | none | 0 | 45.05 | 2.173 | 48.434 |
| script | displacement_exceeds_patch | 2 | accept | false_accept | 1 | - | none | 0 | 65.01 | 2.173 | 95.348 |
| script | width_change | 0 | accept | good_report | 1 | - | none | 0 | 0.402 | 1.085 | 0.322 |
| script | width_change | 1 | accept | good_report | 1 | - | none | 0 | 0.427 | 1.085 | 0.246 |
| script | width_change | 2 | accept | good_report | 1 | - | none | 0 | 0.423 | 1.085 | 0.259 |
| script | rigid_drift | 0 | accept | good_report | 1 | - | none | 0 | 0.431 | 1.085 | 0.299 |
| script | rigid_drift | 1 | accept | good_report | 1 | - | none | 0 | 0.433 | 1.085 | 0.204 |
| script | rigid_drift | 2 | accept | good_report | 1 | - | none | 0 | 0.45 | 1.085 | 0.219 |
| script | low_texture | 0 | accept | false_accept | 1 | - | none | 0 | 16.137 | 1.085 | 53.553 |
| script | low_texture | 1 | accept | false_accept | 1 | - | none | 0 | 21.534 | 1.085 | 42.574 |
| script | low_texture | 2 | accept | false_accept | 1 | - | none | 0 | 22.448 | 1.085 | 39.01 |
| script | midline_jitter | 0 | accept | false_accept | 1 | - | none | 0 | 0.797 | 1.085 | 0.757 |
| script | midline_jitter | 1 | accept | good_report | 1 | - | none | 0 | 0.422 | 1.085 | 0.495 |
| script | midline_jitter | 2 | accept | false_accept | 1 | - | none | 0 | 0.422 | 1.085 | 0.501 |
| remedy_tree | displacement_exceeds_patch | 0 | accept | good_report | 4 | displacement_exceeds_patch | frames registered on the non-growing tissue (from 270 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 270 px from the tip) before tracking; frame stride 6 -> 3; frame stride 3 -> 1 | 1 | 0.948 | 2.173 | 0.22 |
| remedy_tree | displacement_exceeds_patch | 1 | accept | good_report | 4 | displacement_exceeds_patch | frames registered on the non-growing tissue (from 290 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 290 px from the tip) before tracking; frame stride 6 -> 3; frame stride 3 -> 1 | 1 | 0.952 | 2.173 | 0.216 |
| remedy_tree | displacement_exceeds_patch | 2 | accept | good_report | 4 | displacement_exceeds_patch | frames registered on the non-growing tissue (from 280 px from the tip) before tracking; frame stride 6 -> 3; frame stride 3 -> 1 | 0 | 0.999 | 2.173 | 0.176 |
| remedy_tree | width_change | 0 | accept | good_report | 3 | width_change | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0.402 | 1.085 | 0.322 |
| remedy_tree | width_change | 1 | accept | good_report | 3 | width_change | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0.427 | 1.085 | 0.246 |
| remedy_tree | width_change | 2 | accept | good_report | 3 | width_change | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0.423 | 1.085 | 0.259 |
| remedy_tree | rigid_drift | 0 | accept | good_report | 2 | rigid_drift | frames registered on the non-growing tissue (from 305 px from the tip) before tracking | 0 | 0.415 | 1.085 | 0.402 |
| remedy_tree | rigid_drift | 1 | accept | good_report | 2 | rigid_drift | frames registered on the non-growing tissue (from 305 px from the tip) before tracking | 0 | 0.438 | 1.085 | 0.268 |
| remedy_tree | rigid_drift | 2 | accept | good_report | 2 | rigid_drift | frames registered on the non-growing tissue (from 305 px from the tip) before tracking | 0 | 0.459 | 1.085 | 0.245 |
| remedy_tree | low_texture | 0 | decline | correct_decline | 5 | low_texture | frames registered on the non-growing tissue (from 425 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 425 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 2 | 8.058 | 1.085 | 22.849 |
| remedy_tree | low_texture | 1 | decline | correct_decline | 5 | low_texture | frames registered on the non-growing tissue (from 420 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 420 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 2 | 12.662 | 1.085 | 18.1 |
| remedy_tree | low_texture | 2 | decline | correct_decline | 5 | low_texture | frames registered on the non-growing tissue (from 430 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 430 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 2 | 12.961 | 1.085 | 25.083 |
| remedy_tree | midline_jitter | 0 | decline | correct_decline | 5 | midline_jitter | frames registered on the non-growing tissue (from 305 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 305 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 3 | 0.54 | 1.085 | 0.531 |
| remedy_tree | midline_jitter | 1 | decline | correct_decline | 5 | midline_jitter | frames registered on the non-growing tissue (from 305 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 305 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 3 | 0.406 | 1.085 | 0.469 |
| remedy_tree | midline_jitter | 2 | decline | correct_decline | 5 | midline_jitter | frames registered on the non-growing tissue (from 310 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 310 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; rolled back: tracker disk radius 15 -> 30 px; midline source smoothed (light) | 3 | 0.419 | 1.085 | 0.382 |
| diagnostician | displacement_exceeds_patch | 0 | step_limit | not_reported | 8 | rigid_drift | frame stride 6 -> 3; frames registered on the non-growing tissue (from 305 px from the tip) before tracking | 0 | 19.251 | 2.173 | 44.265 |
| diagnostician | width_change | 0 | decline | unnecessary_decline | 7 | unknown | none | 0 | 0.402 | 1.085 | 0.322 |
| diagnostician | rigid_drift | 0 | decline | unnecessary_decline | 7 | unknown | none | 0 | 0.431 | 1.085 | 0.299 |
| diagnostician | low_texture | 0 | decline | correct_decline | 7 | midline_jitter | frames registered on the non-growing tissue (from 425 px from the tip) before tracking; midline source smoothed (light) | 0 | 94.87 | 1.085 | nan |
| diagnostician | midline_jitter | 0 | step_limit | not_reported | 8 | midline_jitter | midline source smoothed (light); frame stride 1 -> 2 | 0 | 0.557 | 1.085 | 0.439 |
