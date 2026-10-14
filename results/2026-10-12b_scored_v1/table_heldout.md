## Held-out faults, seeds 0, 1, 2

Cells: correct outcomes / false accepts / unnecessary declines / terminal fault correct, each out of 3.

| Fault | Label | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| second_root | not repairable | 0 / 3 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| fast_rotation | not repairable | 0 / 3 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 1 / 0 / 0 / 0 |
| bad_stage_correction | repairable | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 2 / 0 / 1 / 3 | 3 / 0 / 0 / 1 |
| flank_swap | not repairable | 0 / 3 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 |
| partial_occlusion | not repairable | 0 / 3 / 0 / 0 | 0 / 3 / 0 / 1 | 3 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |

| Method | Runs | Correct | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | Terminal fault correct | Steps | Remedies kept | Roll backs | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| script | 15 | 3 | 3 | 12 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 | 0 | 0.0 |
| remedy_tree | 15 | 9 | 6 | 3 | 6 | 0 | 0 | 1 | 57 | 21 | 21 | 0 | 0 | 0.0 |
| diagnostician | 15 | 11 | 5 | 0 | 9 | 1 | 0 | 3 | 82 | 7 | 8 | 361591 | 48265 | 542.9 |
| single_agent | 15 | 7 | 6 | 0 | 4 | 0 | 5 | 1 | 100 | 15 | 0 | 421903 | 55231 | 632.7 |

Per run:

| Method | Fault | Seed | Label | Status | Category | Named fault | Fault correct | Steps | Remedies | Roll backs | Tokens in / out | Call (s) | Centre RMS (tol) | Flank RMS |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- | --: | :-- | --: | :-- | --: | :-- | --: |
| script | second_root | 0 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.481 (1.085) | 3.378 |
| script | second_root | 1 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.716 (1.085) | 2.59 |
| script | second_root | 2 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.83 (1.085) | 3.003 |
| script | fast_rotation | 0 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 11.353 (1.085) | 16.21 |
| script | fast_rotation | 1 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 13.26 (1.085) | 16.678 |
| script | fast_rotation | 2 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 23.158 (1.085) | 9.284 |
| script | bad_stage_correction | 0 | repairable | accept | good_report | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.405 (1.085) | 0.288 |
| script | bad_stage_correction | 1 | repairable | accept | good_report | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.44 (1.085) | 0.182 |
| script | bad_stage_correction | 2 | repairable | accept | good_report | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 0.444 (1.085) | 0.149 |
| script | flank_swap | 0 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 6.634 (1.085) | 26.48 |
| script | flank_swap | 1 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 6.486 (1.085) | 36.465 |
| script | flank_swap | 2 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 4.358 (1.085) | 40.929 |
| script | partial_occlusion | 0 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 24.551 (1.085) | 7.509 |
| script | partial_occlusion | 1 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 22.581 (1.085) | 3.554 |
| script | partial_occlusion | 2 | not repairable | accept | false_accept | - | no | 1 | none | 0 | 0 / 0 | 0.0 | 32.824 (1.085) | 1.754 |
| remedy_tree | second_root | 0 | not repairable | accept | good_report | width_change | no | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0 / 0 | 0.0 | 0.481 (1.085) | 3.378 |
| remedy_tree | second_root | 1 | not repairable | accept | good_report | width_change | no | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0 / 0 | 0.0 | 0.716 (1.085) | 2.59 |
| remedy_tree | second_root | 2 | not repairable | accept | good_report | width_change | no | 3 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0 / 0 | 0.0 | 0.83 (1.085) | 3.003 |
| remedy_tree | fast_rotation | 0 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 430 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 430 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 2 | 0 / 0 | 0.0 | 2.749 (1.085) | 3.592 |
| remedy_tree | fast_rotation | 1 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 440 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 440 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; rolled back: tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 3 | 0 / 0 | 0.0 | 13.27 (1.085) | 15.364 |
| remedy_tree | fast_rotation | 2 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 425 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 2 | 0 / 0 | 0.0 | 14.96 (1.085) | 4.586 |
| remedy_tree | bad_stage_correction | 0 | repairable | accept | good_report | rigid_drift | no | 2 | frames registered on the non-growing tissue (from 315 px from the tip) before tracking | 0 | 0 / 0 | 0.0 | 0.405 (1.085) | 0.342 |
| remedy_tree | bad_stage_correction | 1 | repairable | accept | good_report | rigid_drift | no | 2 | frames registered on the non-growing tissue (from 310 px from the tip) before tracking | 0 | 0 / 0 | 0.0 | 0.448 (1.085) | 0.184 |
| remedy_tree | bad_stage_correction | 2 | repairable | accept | good_report | rigid_drift | no | 2 | frames registered on the non-growing tissue (from 315 px from the tip) before tracking | 0 | 0 / 0 | 0.0 | 0.442 (1.085) | 0.169 |
| remedy_tree | flank_swap | 0 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 435 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 435 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; rolled back: tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 3 | 0 / 0 | 0.0 | 6.647 (1.085) | 23.903 |
| remedy_tree | flank_swap | 1 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 390 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 390 px from the tip) before tracking; tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 3 | 0 / 0 | 0.0 | 6.432 (1.085) | 35.959 |
| remedy_tree | flank_swap | 2 | not repairable | decline | correct_decline | low_texture | no | 5 | frames registered on the non-growing tissue (from 430 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 430 px from the tip) before tracking; tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light) | 2 | 0 / 0 | 0.0 | 5.337 (1.085) | 32.221 |
| remedy_tree | partial_occlusion | 0 | not repairable | accept | false_accept | width_change | no | 5 | tracker disk radius 15 -> 22 px; rolled back: tracker disk radius 15 -> 22 px; tracker disk radius 15 -> 30 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 2 | 0 / 0 | 0.0 | 2.523 (1.085) | 6.005 |
| remedy_tree | partial_occlusion | 1 | not repairable | accept | false_accept | low_texture | yes | 3 | tracker disk radius 15 -> 22 px; tracker disk radius 22 -> 30 px | 0 | 0 / 0 | 0.0 | 2.113 (1.085) | 0.636 |
| remedy_tree | partial_occlusion | 2 | not repairable | accept | false_accept | width_change | no | 4 | tracker disk radius 15 -> 22 px; midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 0 / 0 | 0.0 | 15.823 (1.085) | 3.173 |
| diagnostician | second_root | 0 | not repairable | accept | good_report | width_change | no | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 21725 / 2091 | 26.4 | 0.481 (1.085) | 3.378 |
| diagnostician | second_root | 1 | not repairable | accept | good_report | width_change | no | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 21880 / 2142 | 25.0 | 0.716 (1.085) | 2.59 |
| diagnostician | second_root | 2 | not repairable | accept | good_report | width_change | no | 5 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 21727 / 2547 | 28.4 | 0.83 (1.085) | 3.003 |
| diagnostician | fast_rotation | 0 | not repairable | decline | correct_decline | midline_jitter | no | 8 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 | 38230 / 5773 | 62.9 | 11.353 (1.085) | 16.21 |
| diagnostician | fast_rotation | 1 | not repairable | decline | correct_decline | midline_jitter | no | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 | 20590 / 2782 | 31.0 | 13.26 (1.085) | 16.678 |
| diagnostician | fast_rotation | 2 | not repairable | decline | correct_decline | midline_jitter | no | 5 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 | 20597 / 2855 | 32.4 | 23.158 (1.085) | 9.284 |
| diagnostician | bad_stage_correction | 0 | repairable | accept | good_report | bad_stage_correction | yes | 3 | frames registered on the non-growing tissue (from 315 px from the tip) before tracking | 0 | 11456 / 1388 | 16.1 | 0.405 (1.085) | 0.342 |
| diagnostician | bad_stage_correction | 1 | repairable | accept | good_report | bad_stage_correction | yes | 3 | frames registered on the non-growing tissue (from 310 px from the tip) before tracking | 0 | 11478 / 1259 | 17.5 | 0.448 (1.085) | 0.184 |
| diagnostician | bad_stage_correction | 2 | repairable | decline | unnecessary_decline | bad_stage_correction | yes | 2 | none | 0 | 7277 / 940 | 11.0 | 0.444 (1.085) | 0.149 |
| diagnostician | flank_swap | 0 | not repairable | decline | correct_decline | midline_jitter | no | 6 | midline source smoothed (light) | 0 | 26308 / 3059 | 36.2 | 6.634 (1.085) | 26.586 |
| diagnostician | flank_swap | 1 | not repairable | decline | correct_decline | midline_jitter | no | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 | 26042 / 3605 | 41.1 | 6.486 (1.085) | 36.465 |
| diagnostician | flank_swap | 2 | not repairable | decline | correct_decline | bad_stage_correction | no | 8 | frames registered on the non-growing tissue (from 430 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 430 px from the tip) before tracking | 1 | 37678 / 6605 | 69.6 | 4.358 (1.085) | 40.929 |
| diagnostician | partial_occlusion | 0 | not repairable | decline | correct_decline | second_root | no | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root) | 1 | 31990 / 4747 | 52.9 | 24.551 (1.085) | 7.509 |
| diagnostician | partial_occlusion | 1 | not repairable | decline | correct_decline | midline_jitter | no | 6 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 | 25966 / 3621 | 39.4 | 22.581 (1.085) | 3.554 |
| diagnostician | partial_occlusion | 2 | not repairable | decline | correct_decline | midline_jitter | no | 8 | midline source smoothed (light); rolled back: midline source smoothed (light); report the centre strain rate and the width-free ratio; plane-sections check skipped | 1 | 38647 / 4851 | 53.0 | 32.824 (1.085) | 1.754 |
| single_agent | second_root | 0 | not repairable | accept | good_report | width_change | no | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 23731 / 2858 | 32.3 | 0.481 (1.085) | 3.378 |
| single_agent | second_root | 1 | not repairable | accept | good_report | width_change | no | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 23719 / 2382 | 28.6 | 0.716 (1.085) | 2.59 |
| single_agent | second_root | 2 | not repairable | accept | good_report | width_change | no | 8 | frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 36025 / 4186 | 50.5 | 0.83 (1.085) | 3.003 |
| single_agent | fast_rotation | 0 | not repairable | step_limit | not_reported | midline_jitter | no | 8 | midline source smoothed (light) | 0 | 34881 / 3285 | 40.3 | 11.353 (1.085) | 16.162 |
| single_agent | fast_rotation | 1 | not repairable | step_limit | not_reported | midline_jitter | no | 8 | midline source smoothed (light) | 0 | 34863 / 4087 | 47.0 | 13.26 (1.085) | 20.291 |
| single_agent | fast_rotation | 2 | not repairable | decline | correct_decline | rigid_drift | no | 5 | frames registered on the non-growing tissue (from 425 px from the tip) before tracking | 0 | 18430 / 2174 | 25.6 | 10.546 (1.085) | 10.469 |
| single_agent | bad_stage_correction | 0 | repairable | accept | good_report | bad_stage_correction | yes | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped; frames registered on the non-growing tissue (from 315 px from the tip) before tracking | 0 | 34925 / 6068 | 66.0 | 0.405 (1.085) | 0.342 |
| single_agent | bad_stage_correction | 1 | repairable | accept | good_report | width_change | no | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 24377 / 2928 | 34.4 | 0.44 (1.085) | 0.182 |
| single_agent | bad_stage_correction | 2 | repairable | accept | good_report | width_change | no | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 24453 / 3658 | 42.4 | 0.444 (1.085) | 0.149 |
| single_agent | flank_swap | 0 | not repairable | decline | correct_decline | bad_stage_correction | no | 4 | none | 0 | 15055 / 1874 | 22.4 | 6.634 (1.085) | 26.48 |
| single_agent | flank_swap | 1 | not repairable | decline | correct_decline | bad_stage_correction | no | 3 | none | 0 | 10356 / 1651 | 18.0 | 6.486 (1.085) | 36.465 |
| single_agent | flank_swap | 2 | not repairable | decline | correct_decline | midline_jitter | no | 8 | midline source smoothed (light) | 0 | 35294 / 4994 | 54.6 | 4.358 (1.085) | 42.538 |
| single_agent | partial_occlusion | 0 | not repairable | step_limit | not_reported | second_root | no | 8 | frames limited to the main root (mask_second_root) | 0 | 35845 / 4460 | 50.8 | 24.551 (1.085) | 7.509 |
| single_agent | partial_occlusion | 1 | not repairable | step_limit | not_reported | midline_jitter | no | 8 | midline source smoothed (light) | 0 | 34767 / 3706 | 43.0 | 22.645 (1.085) | 3.551 |
| single_agent | partial_occlusion | 2 | not repairable | step_limit | not_reported | width_change | no | 8 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 35182 / 6920 | 76.8 | 32.824 (1.085) | 1.754 |
