# Labels of the freeze v4 scored set

Scoring seeds 20, 21, 22. Tracker only, no agent. Repair criteria (spec 2026-10-10, part C; measure.score.label_rod; C3 option a: a check that cannot be computed after a remedy fails): a state of at most two remedy steps with three passes and a good measurement. Clean rods: accept_clean if the unremedied run passes and is good.

| Rod | Expected class | Label class | Repairing remedy | Unremedied: checks pass, good |
| :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_bend30_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_bend30_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_bend30_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s26 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s27 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s28 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_rigid_drift_z0.5_s26 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_rigid_drift_z0.5_s27 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_rigid_drift_z0.5_s28 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | decline | decline | - | no, no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | decline | decline | - | no, no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | decline | decline | - | no, no |
| v3_growth_zone_width_change_s26 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_width_change_s27 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_width_change_s28 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_low_texture_z0.03_s26 | decline | decline | - | no, no |
| v3_growth_zone_low_texture_z0.03_s27 | decline | decline | - | no, no |
| v3_growth_zone_low_texture_z0.03_s28 | decline | decline | - | no, no |
| v3_growth_zone_midline_jitter_z3_s26 | decline | decline | - | no, yes |
| v3_growth_zone_midline_jitter_z3_s27 | decline | decline | - | no, yes |
| v3_growth_zone_midline_jitter_z3_s28 | decline | decline | - | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s26 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s27 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s28 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_stage_log_missing_z1_s26 | decline | decline | - | no, yes |
| v3_growth_zone_stage_log_missing_z1_s27 | decline | decline | - | no, yes |
| v3_growth_zone_stage_log_missing_z1_s28 | decline | decline | - | no, yes |
| v3_growth_zone_second_root_z30_s26 | decline | decline | - | no, no |
| v3_growth_zone_second_root_z30_s27 | decline | decline | - | no, no |
| v3_growth_zone_second_root_z30_s28 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s26 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s27 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s28 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s26 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s27 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s28 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s26 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s27 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s28 | decline | decline | - | no, no |

- Rods labelled 51 of 51; states not yet run 0
- Classes: {'accept_clean': 18, 'accept_repaired': 9, 'decline': 24, 'clean_fails': 0}
- All-decline would score 24 of 51
- Label differs from the expected class: 0
- Result: complete

## Per state

| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| v3_growth_zone_clean_s26 | none | 0.91 | 0.23 | 0.55 | 0.34 (1.35) | 0.18 (1.00) | yes | yes |
| v3_growth_zone_clean_s27 | none | 0.89 | 0.23 | 0.42 | 0.32 (1.35) | 0.18 (1.00) | yes | yes |
| v3_growth_zone_clean_s28 | none | 0.84 | 0.10 | 0.81 | 0.34 (1.35) | 0.25 (1.00) | yes | yes |
| v3_bend16_clean_s26 | none | 0.60 | 0.20 | 1.39 | 0.44 (1.35) | 0.34 (1.00) | yes | yes |
| v3_bend16_clean_s27 | none | 0.78 | 0.19 | 1.21 | 0.45 (1.35) | 0.32 (1.00) | yes | yes |
| v3_bend16_clean_s28 | none | 0.71 | 0.13 | 1.21 | 0.40 (1.35) | 0.35 (1.00) | yes | yes |
| v3_bend20_clean_s26 | none | 0.62 | 0.22 | 1.19 | 0.47 (1.35) | 0.33 (1.00) | yes | yes |
| v3_bend20_clean_s27 | none | 0.65 | 0.16 | 1.72 | 0.44 (1.35) | 0.37 (1.00) | yes | yes |
| v3_bend20_clean_s28 | none | 0.66 | 0.15 | 2.22 | 0.41 (1.35) | 0.48 (1.00) | yes | yes |
| v3_bend24_clean_s26 | none | 0.70 | 0.18 | 1.62 | 0.49 (1.35) | 0.41 (1.00) | yes | yes |
| v3_bend24_clean_s27 | none | 0.81 | 0.16 | 1.72 | 0.46 (1.35) | 0.41 (1.00) | yes | yes |
| v3_bend24_clean_s28 | none | 0.67 | 0.15 | 2.28 | 0.41 (1.35) | 0.53 (1.00) | yes | yes |
| v3_bend30_clean_s26 | none | 1.11 | 0.22 | 1.91 | 0.49 (1.35) | 0.47 (1.00) | yes | yes |
| v3_bend30_clean_s27 | none | 0.56 | 0.21 | 1.25 | 0.52 (1.35) | 0.44 (1.00) | yes | yes |
| v3_bend30_clean_s28 | none | 0.53 | 0.15 | 2.23 | 0.43 (1.35) | 0.53 (1.00) | yes | yes |
| v3_still_clean_s26 | none | 1.34 | 0.06 | 0.55 | 0.14 (0.50) | 0.20 (1.00) | yes | yes |
| v3_still_clean_s27 | none | 0.82 | 0.09 | 0.87 | 0.14 (0.50) | 0.27 (1.00) | yes | yes |
| v3_still_clean_s28 | none | 1.05 | 0.05 | 0.47 | 0.19 (0.50) | 0.18 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s26 | none | 0.67 | 8.23 F | 0.97 | 0.38 (1.35) | 0.23 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s26 | register_frames | 1.69 | 0.31 | 0.68 | 0.40 (1.35) | 0.19 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s27 | none | 0.85 | 8.20 F | 0.71 | 0.34 (1.35) | 0.23 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s27 | register_frames | 0.80 | 0.24 | 0.55 | 0.38 (1.35) | 0.20 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s28 | none | 0.79 | 8.08 F | 1.28 | 0.36 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s28 | register_frames | 1.08 | 0.45 | 1.64 | 0.35 (1.35) | 0.41 (1.00) | yes | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | none | 227.14 F | 170.37 F | 232.96 F | 66.59 (2.70) | 70.80 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | change_frame_stride/half | 351.65 F | 133.23 F | 341.38 F | 54.98 (2.70) | 75.13 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s26 | change_frame_stride/half + change_frame_stride/half | 115.05 F | 0.27 | 135.64 F | 3.67 (2.70) | 18.16 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | none | 319.09 F | 170.71 F | 319.09 F | 68.81 (2.70) | 89.00 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | change_frame_stride/half | 479.17 F | 266.45 F | 193.98 F | 61.21 (2.70) | 58.49 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s27 | change_frame_stride/half + change_frame_stride/half | 71.47 F | 0.24 | 0.84 | 4.79 (2.70) | 0.24 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | none | 277.63 F | 171.53 F | 243.12 F | 71.72 (2.70) | 59.96 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | change_frame_stride/half | 468.20 F | 134.16 F | 207.07 F | 46.56 (2.70) | 62.94 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s28 | change_frame_stride/half + change_frame_stride/half | 60.40 F | 0.17 | 0.84 | 7.64 (2.70) | 0.27 (1.00) | no | no |
| v3_growth_zone_width_change_s26 | none | 0.74 | 0.11 | 3.79 F | 0.36 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_width_change_s26 | use_width_free_ratio | 0.74 | 0.11 | 3.79 skip | 0.36 (1.35) | 0.26 (1.00) | yes | yes |
| v3_growth_zone_width_change_s27 | none | 1.08 | 0.13 | 3.72 F | 0.33 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_width_change_s27 | use_width_free_ratio | 1.08 | 0.13 | 3.72 skip | 0.33 (1.35) | 0.26 (1.00) | yes | yes |
| v3_growth_zone_width_change_s28 | none | 0.80 | 0.11 | 3.86 F | 0.33 (1.35) | 0.29 (1.00) | no | yes |
| v3_growth_zone_width_change_s28 | use_width_free_ratio | 0.80 | 0.11 | 3.86 skip | 0.33 (1.35) | 0.29 (1.00) | yes | yes |
| v3_growth_zone_low_texture_z0.03_s26 | none | 187.80 F | 3.27 F | 227.61 F | 26.17 (1.35) | 50.46 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s26 | enlarge_patch/1.5x | 139.96 F | 5.56 F | 87.96 F | 14.32 (1.35) | 22.85 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s26 | enlarge_patch/2x | 40.55 F | 2.22 F | 49.03 F | 12.01 (1.35) | 17.74 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s27 | none | 166.56 F | 3.67 F | 108.29 F | 20.65 (1.35) | 32.26 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s27 | enlarge_patch/1.5x | 64.97 F | 2.45 F | 75.29 F | 12.37 (1.35) | 28.88 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s27 | enlarge_patch/2x | 57.62 F | 2.15 F | 43.79 F | 12.62 (1.35) | 16.02 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s28 | none | 249.36 F | 2.86 F | 234.90 F | 21.98 (1.35) | 72.35 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s28 | enlarge_patch/1.5x | 86.99 F | 1.51 F | 69.37 F | 12.64 (1.35) | 24.61 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s28 | enlarge_patch/2x | 58.45 F | 0.84 | 68.78 F | 12.72 (1.35) | 20.19 (1.00) | no | no |
| v3_growth_zone_midline_jitter_z3_s26 | none | 0.59 | 25.74 F | 50.04 F | 1.03 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s26 | smooth_midline/light | 0.58 | 29.92 F | 50.46 F | 0.84 (1.35) | 0.50 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s27 | none | 0.51 | 13.83 F | 41.78 F | 0.44 (1.35) | 0.43 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s27 | smooth_midline/light | 0.79 | 9.79 F | 29.76 F | 0.37 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s28 | none | 0.72 | 5.69 F | 63.62 F | 0.53 (1.35) | 0.41 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s28 | smooth_midline/light | 0.71 | 1.62 F | 37.61 F | 0.38 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s26 | none | 0.92 | 2.78 F | 0.55 | 0.34 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s26 | register_frames | 1.67 | 0.12 | 0.66 | 0.36 (1.35) | 0.21 (1.00) | yes | yes |
| v3_growth_zone_bad_stage_correction_z3_s27 | none | 0.89 | 2.77 F | 0.42 | 0.32 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s27 | register_frames | 0.80 | 0.06 | 0.46 | 0.33 (1.35) | 0.19 (1.00) | yes | yes |
| v3_growth_zone_bad_stage_correction_z3_s28 | none | 0.83 | 2.90 F | 0.81 | 0.34 (1.35) | 0.25 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s28 | register_frames | 1.12 | 0.18 | 0.91 | 0.34 (1.35) | 0.24 (1.00) | yes | yes |
| v3_growth_zone_stage_log_missing_z1_s26 | none | 0.89 | 95.78 F | 0.56 | 0.34 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s26 | register_frames | 1.56 | nan skip | 0.60 | 0.36 (1.35) | 0.22 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s27 | none | 0.90 | 95.77 F | 0.41 | 0.32 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s27 | register_frames | 0.75 | nan skip | 0.50 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s28 | none | 0.88 | 95.90 F | 0.83 | 0.34 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s28 | register_frames | 1.11 | nan skip | 1.06 | 0.35 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_second_root_z30_s26 | none | 0.91 | 0.23 | 7.74 F | 0.66 (1.35) | 1.91 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s26 | crop_or_mask/crop_to_main_root | 0.91 | 0.23 | 7.74 F | 0.66 (1.35) | 1.91 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s26 | crop_or_mask/mask_second_root | 0.91 | 0.23 | 7.74 F | 0.66 (1.35) | 1.91 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s27 | none | 0.89 | 0.23 | 8.85 F | 0.51 (1.35) | 2.06 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s27 | crop_or_mask/crop_to_main_root | 0.89 | 0.23 | 8.85 F | 0.51 (1.35) | 2.06 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s27 | crop_or_mask/mask_second_root | 0.89 | 0.23 | 8.85 F | 0.51 (1.35) | 2.06 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s28 | none | 0.85 | 0.10 | 14.43 F | 0.61 (1.35) | 2.93 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s28 | crop_or_mask/crop_to_main_root | 0.85 | 0.10 | 14.43 F | 0.61 (1.35) | 2.93 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s28 | crop_or_mask/mask_second_root | 0.85 | 0.10 | 14.43 F | 0.61 (1.35) | 2.93 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s26 | none | 64.13 F | 25.89 F | 96.29 F | 35.12 (1.35) | 26.16 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s26 | register_frames | 160.40 F | 25.34 F | 103.73 F | 33.71 (1.35) | 31.72 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s27 | none | 113.00 F | 21.47 F | 109.88 F | 35.40 (1.35) | 28.73 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s27 | register_frames | 350.65 F | 29.90 F | 86.28 F | 34.64 (1.35) | 25.59 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s28 | none | 151.51 F | 10.45 F | 187.70 F | 20.79 (1.35) | 37.70 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s28 | register_frames | 207.09 F | 10.46 F | 147.08 F | 20.20 (1.35) | 36.73 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | none | 39.36 F | 0.84 | 82.46 F | 6.58 (1.35) | 28.71 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | enlarge_patch/1.5x | 12.10 F | 1.60 F | 185.98 F | 4.86 (1.35) | 35.73 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | enlarge_patch/2x | 88.93 F | 1.62 F | 138.67 F | 3.71 (1.35) | 32.49 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | change_frame_stride/double | 141.95 F | 0.75 | 82.11 F | 8.31 (1.35) | 27.93 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | change_frame_stride/double + enlarge_patch/1.5x | 66.96 F | 1.59 F | 159.12 F | 4.83 (1.35) | 35.28 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s26 | change_frame_stride/double + enlarge_patch/2x | 108.87 F | 1.63 F | 135.89 F | 3.70 (1.35) | 32.44 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | none | 30.15 F | 0.80 | 64.35 F | 8.17 (1.35) | 25.61 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | enlarge_patch/1.5x | 67.88 F | 0.23 | 113.27 F | 9.02 (1.35) | 28.57 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | enlarge_patch/2x | 14.55 F | 0.66 | 102.53 F | 2.99 (1.35) | 29.21 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | change_frame_stride/double | 90.39 F | 0.72 | 59.87 F | 7.16 (1.35) | 25.55 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | change_frame_stride/double + enlarge_patch/1.5x | 72.33 F | 0.20 | 104.04 F | 9.05 (1.35) | 28.39 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s27 | change_frame_stride/double + enlarge_patch/2x | 18.27 F | 0.67 | 118.92 F | 3.04 (1.35) | 30.11 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | none | 175.26 F | 0.05 | 205.31 F | 4.53 (1.35) | 38.26 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | enlarge_patch/1.5x | 13.02 F | 1.37 F | 102.00 F | 5.59 (1.35) | 31.18 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | enlarge_patch/2x | 72.19 F | 1.89 F | 109.76 F | 5.37 (1.35) | 30.48 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | change_frame_stride/double | 136.16 F | 0.06 | 181.03 F | 7.55 (1.35) | 35.27 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | change_frame_stride/double + enlarge_patch/1.5x | 57.13 F | 1.37 F | 106.61 F | 5.02 (1.35) | 31.18 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s28 | change_frame_stride/double + enlarge_patch/2x | 47.95 F | 1.90 F | 89.02 F | 5.64 (1.35) | 24.79 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s26 | none | 48.18 F | 0.23 | 8.60 F | 14.93 (1.35) | 2.19 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s26 | enlarge_patch/1.5x | 32.57 F | 0.25 | 12.10 F | 10.32 (1.35) | 2.41 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s26 | enlarge_patch/2x | 1.44 | 0.27 | 2.47 | 4.96 (1.35) | 0.50 (1.00) | yes | no |
| v3_growth_zone_partial_occlusion_z20_s26 | change_frame_stride/double | 122.62 F | 0.15 | 117.77 F | 23.05 (1.35) | 17.04 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s26 | change_frame_stride/double + enlarge_patch/1.5x | 64.56 F | 0.19 | 27.87 F | 10.57 (1.35) | 4.67 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s26 | change_frame_stride/double + enlarge_patch/2x | 48.42 F | 0.21 | 2.06 | 5.36 (1.35) | 0.46 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | none | 213.70 F | 0.23 | 32.97 F | 43.72 (1.35) | 6.62 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | enlarge_patch/1.5x | 6.01 F | 0.23 | 24.41 F | 9.46 (1.35) | 4.58 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | enlarge_patch/2x | 2.14 F | 0.25 | 21.05 F | 4.59 (1.35) | 3.73 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | change_frame_stride/double | 309.90 F | 0.13 | 23.83 F | 29.68 (1.35) | 5.74 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | change_frame_stride/double + enlarge_patch/1.5x | 37.74 F | 0.16 | 15.51 F | 8.97 (1.35) | 3.37 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s27 | change_frame_stride/double + enlarge_patch/2x | 2.05 F | 0.20 | 14.93 F | 4.46 (1.35) | 2.75 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | none | 79.09 F | 0.10 | 12.31 F | 21.96 (1.35) | 3.64 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | enlarge_patch/1.5x | 60.22 F | 0.14 | 14.60 F | 16.14 (1.35) | 3.04 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | enlarge_patch/2x | 1.42 | 0.19 | 18.30 F | 8.58 (1.35) | 3.57 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | change_frame_stride/double | 117.88 F | 0.08 | 14.91 F | 37.95 (1.35) | 4.72 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | change_frame_stride/double + enlarge_patch/1.5x | 104.38 F | 0.11 | 15.62 F | 21.78 (1.35) | 3.03 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s28 | change_frame_stride/double + enlarge_patch/2x | 55.40 F | 0.16 | 18.95 F | 8.46 (1.35) | 3.63 (1.00) | no | no |
