# Freeze v4 development check, not a score

Diagnostician, candidate v4 on, v3 seed 20 (v3 scoring seed; C1 and C2 were written from its traces), one run per row of the v3 set. Labels: v3 label sweep with C3 (a) (`switch_check.md`). States from the v3 cache only.

| Row | Rod | Class | Status | Category | Named fault | Fault correct | Steps | Remedies | v3 diagnostician correct (seed 20, 3 repeats) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | --: | :-- | :-- |
| v3_growth_zone | v3_growth_zone_clean_s20 | accept_clean | accept | good_report | - | - | 1 | none | 3 / 3 |
| v3_bend16 | v3_bend16_clean_s20 | accept_clean | accept | good_report | - | - | 2 | none | 3 / 3 |
| v3_bend20 | v3_bend20_clean_s20 | accept_clean | accept | good_report | - | - | 2 | none | 3 / 3 |
| v3_bend24 | v3_bend24_clean_s20 | accept_clean | accept | good_report | - | - | 1 | none | 3 / 3 |
| v3_bend30 | v3_bend30_clean_s20 | accept_clean | decline | unnecessary_decline | bad_stage_correction | - | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0 / 3 |
| v3_still | v3_still_clean_s20 | accept_clean | accept | good_report | - | - | 1 | none | 3 / 3 |
| rigid_drift | v3_growth_zone_rigid_drift_z0.5_s20 | accept_repaired | accept | good_report | bad_stage_correction | no | 3 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0 / 3 |
| displacement_exceeds_patch | v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | decline | decline | correct_decline | displacement_exceeds_patch | yes | 7 | frame stride 6 -> 3; frame stride 3 -> 1 | 2 / 3 |
| width_change | v3_growth_zone_width_change_s20 | accept_repaired | accept | good_report | width_change | yes | 6 | report the centre strain rate and the width-free ratio; plane-sections check skipped | 3 / 3 |
| low_texture | v3_growth_zone_low_texture_z0.03_s20 | decline | decline | correct_decline | low_texture | yes | 7 | tracker disk radius 14 -> 21 px; tracker disk radius 21 -> 28 px | 3 / 3 |
| midline_jitter | v3_growth_zone_midline_jitter_z3_s20 | decline | decline | correct_decline | midline_jitter | yes | 7 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking; midline source smoothed (light) | 3 / 3 |
| bad_stage_correction | v3_growth_zone_bad_stage_correction_z3_s20 | accept_repaired | accept | good_report | bad_stage_correction | yes | 4 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 0 / 3 |
| stage_log_missing | v3_growth_zone_stage_log_missing_z1_s20 | decline | decline | correct_decline | rigid_drift | yes | 6 | frames registered on the non-growing tissue (from 400 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 400 px from the tip) before tracking | 3 / 3 |
| second_root | v3_growth_zone_second_root_z30_s20 | decline | accept | accept_on_decline | width_change | no | 7 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 / 3 |
| fast_rotation | v3_growth_zone_fast_rotation_z2_s20 | decline | decline | correct_decline | midline_jitter | no | 7 | midline source smoothed (light); rolled back: midline source smoothed (light) | 1 / 3 |
| flank_swap | v3_growth_zone_flank_swap_z0.5_s20 | decline | decline | correct_decline | bad_stage_correction | no | 8 | frames registered on the non-growing tissue (from 545 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 545 px from the tip) before tracking | 2 / 3 |
| partial_occlusion | v3_growth_zone_partial_occlusion_z20_s20 | decline | step_limit | not_reported | midline_jitter | no | 8 | frames limited to the main root (mask_second_root); rolled back: frames limited to the main root (mask_second_root); report the centre strain rate and the width-free ratio; plane-sections check skipped; midline source smoothed (light); rolled back: midline source smoothed (light) | 1 / 3 |

- Runs 17; correct 14
- Development check only: seed 20 is not unseen. Not a score
