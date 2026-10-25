# Labels of the freeze v3 scored set

Scoring seeds 20, 21, 22. Tracker only, no agent. Repair criteria (spec 2026-10-10, part C; measure.score.label_rod): a state of at most two remedy steps with three passes and a good measurement. Clean rods: accept_clean if the unremedied run passes and is good.

| Rod | Expected class | Label class | Repairing remedy | Unremedied: checks pass, good |
| :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone_clean_s20 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s20 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_bend16_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s20 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_bend20_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s20 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_bend24_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_bend30_clean_s20 | accept_clean | accept_clean | - | no, yes |
| v3_bend30_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_bend30_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s20 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s21 | accept_clean | accept_clean | - | yes, yes |
| v3_still_clean_s22 | accept_clean | accept_clean | - | yes, yes |
| v3_growth_zone_rigid_drift_z0.5_s20 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_rigid_drift_z0.5_s21 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_rigid_drift_z0.5_s22 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | accept_repaired | decline | - | no, no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | accept_repaired | decline | - | no, no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | accept_repaired | decline | - | no, no |
| v3_growth_zone_width_change_s20 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_width_change_s21 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_width_change_s22 | accept_repaired | accept_repaired | use_width_free_ratio | no, yes |
| v3_growth_zone_low_texture_z0.03_s20 | decline | decline | - | no, no |
| v3_growth_zone_low_texture_z0.03_s21 | decline | decline | - | no, no |
| v3_growth_zone_low_texture_z0.03_s22 | decline | decline | - | no, no |
| v3_growth_zone_midline_jitter_z3_s20 | decline | decline | - | no, yes |
| v3_growth_zone_midline_jitter_z3_s21 | decline | decline | - | no, yes |
| v3_growth_zone_midline_jitter_z3_s22 | decline | decline | - | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s20 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s21 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_bad_stage_correction_z3_s22 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_stage_log_missing_z1_s20 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_stage_log_missing_z1_s21 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_stage_log_missing_z1_s22 | accept_repaired | accept_repaired | register_frames | no, yes |
| v3_growth_zone_second_root_z30_s20 | decline | decline | - | no, no |
| v3_growth_zone_second_root_z30_s21 | decline | decline | - | no, no |
| v3_growth_zone_second_root_z30_s22 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s20 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s21 | decline | decline | - | no, no |
| v3_growth_zone_fast_rotation_z2_s22 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s20 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s21 | decline | decline | - | no, no |
| v3_growth_zone_flank_swap_z0.5_s22 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s20 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s21 | decline | decline | - | no, no |
| v3_growth_zone_partial_occlusion_z20_s22 | decline | decline | - | no, no |

- Rods labelled 51 of 51; states not yet run 0
- Classes: {'accept_clean': 18, 'accept_repaired': 12, 'decline': 21, 'clean_fails': 0}
- All-decline would score 21 of 51
- Label differs from the expected class: 3: v3_growth_zone_displacement_exceeds_patch_z2x6_s20, v3_growth_zone_displacement_exceeds_patch_z2x6_s21, v3_growth_zone_displacement_exceeds_patch_z2x6_s22
- Result: complete

## Per state

| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| v3_growth_zone_clean_s20 | none | 0.64 | 0.17 | 0.56 | 0.34 (1.35) | 0.16 (1.00) | yes | yes |
| v3_growth_zone_clean_s21 | none | 0.79 | 0.16 | 0.49 | 0.36 (1.35) | 0.19 (1.00) | yes | yes |
| v3_growth_zone_clean_s22 | none | 0.71 | 0.02 | 0.41 | 0.35 (1.35) | 0.17 (1.00) | yes | yes |
| v3_bend16_clean_s20 | none | 0.60 | 0.22 | 0.83 | 0.39 (1.35) | 0.22 (1.00) | yes | yes |
| v3_bend16_clean_s21 | none | 0.62 | 0.18 | 1.26 | 0.43 (1.35) | 0.36 (1.00) | yes | yes |
| v3_bend16_clean_s22 | none | 0.66 | 0.12 | 0.73 | 0.43 (1.35) | 0.28 (1.00) | yes | yes |
| v3_bend20_clean_s20 | none | 0.73 | 0.15 | 1.71 | 0.38 (1.35) | 0.36 (1.00) | yes | yes |
| v3_bend20_clean_s21 | none | 0.73 | 0.16 | 1.22 | 0.42 (1.35) | 0.39 (1.00) | yes | yes |
| v3_bend20_clean_s22 | none | 0.61 | 0.09 | 1.02 | 0.44 (1.35) | 0.30 (1.00) | yes | yes |
| v3_bend24_clean_s20 | none | 0.65 | 0.14 | 1.93 | 0.40 (1.35) | 0.37 (1.00) | yes | yes |
| v3_bend24_clean_s21 | none | 0.89 | 0.15 | 1.95 | 0.46 (1.35) | 0.51 (1.00) | yes | yes |
| v3_bend24_clean_s22 | none | 0.62 | 0.13 | 0.89 | 0.46 (1.35) | 0.33 (1.00) | yes | yes |
| v3_bend30_clean_s20 | none | 1.14 | 4.51 F | 1.50 | 0.44 (1.35) | 0.35 (1.00) | no | yes |
| v3_bend30_clean_s21 | none | 0.78 | 0.17 | 1.69 | 0.48 (1.35) | 0.47 (1.00) | yes | yes |
| v3_bend30_clean_s22 | none | 0.59 | 0.18 | 0.74 | 0.48 (1.35) | 0.28 (1.00) | yes | yes |
| v3_still_clean_s20 | none | 0.87 | 0.14 | 0.41 | 0.15 (0.50) | 0.17 (1.00) | yes | yes |
| v3_still_clean_s21 | none | 0.92 | 0.03 | 0.49 | 0.20 (0.50) | 0.20 (1.00) | yes | yes |
| v3_still_clean_s22 | none | 1.89 | 0.08 | 0.76 | 0.15 (0.50) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s20 | none | 0.68 | 7.99 F | 0.54 | 0.36 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s20 | register_frames | 0.66 | 0.61 | 0.66 | 0.35 (1.35) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s21 | none | 1.03 | 8.14 F | 0.81 | 0.40 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s21 | register_frames | 1.03 | 0.35 | 1.30 | 0.40 (1.35) | 0.31 (1.00) | yes | yes |
| v3_growth_zone_rigid_drift_z0.5_s22 | none | 0.65 | 7.94 F | 1.02 | 0.36 (1.35) | 0.28 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s22 | register_frames | 0.91 | 0.55 | 0.59 | 0.37 (1.35) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | none | 272.31 F | 172.86 F | 348.21 F | 74.45 (2.70) | 82.51 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | change_frame_stride/half | 236.68 F | 116.19 F | 229.88 F | 42.34 (2.70) | 79.73 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s20 | change_frame_stride/half + change_frame_stride/half | 126.71 F | 5.31 F | 24.42 F | 22.11 (2.70) | 3.99 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | none | 278.95 F | 193.36 F | 187.60 F | 66.08 (2.70) | 46.70 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | change_frame_stride/half | 361.49 F | 85.40 F | 331.76 F | 52.20 (2.70) | 102.95 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s21 | change_frame_stride/half + change_frame_stride/half | 76.31 F | 0.32 | 0.60 | 10.43 (2.70) | 0.24 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | none | 403.05 F | 202.79 F | 255.45 F | 62.45 (2.70) | 67.69 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | change_frame_stride/half | 316.50 F | 150.37 F | 460.99 F | 52.86 (2.70) | 108.32 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x6_s22 | change_frame_stride/half + change_frame_stride/half | 52.08 F | 0.14 | 12.82 F | 5.60 (2.70) | 4.74 (1.00) | no | no |
| v3_growth_zone_width_change_s20 | none | 0.85 | 0.17 | 3.70 F | 0.36 (1.35) | 0.23 (1.00) | no | yes |
| v3_growth_zone_width_change_s20 | use_width_free_ratio | 0.85 | 0.17 | 3.70 skip | 0.36 (1.35) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_width_change_s21 | none | 0.85 | 0.06 | 3.66 F | 0.36 (1.35) | 0.29 (1.00) | no | yes |
| v3_growth_zone_width_change_s21 | use_width_free_ratio | 0.85 | 0.06 | 3.66 skip | 0.36 (1.35) | 0.29 (1.00) | yes | yes |
| v3_growth_zone_width_change_s22 | none | 1.12 | 0.03 | 3.67 F | 0.37 (1.35) | 0.31 (1.00) | no | yes |
| v3_growth_zone_width_change_s22 | use_width_free_ratio | 1.12 | 0.03 | 3.67 skip | 0.37 (1.35) | 0.31 (1.00) | yes | yes |
| v3_growth_zone_low_texture_z0.03_s20 | none | 207.93 F | 3.99 F | 124.33 F | 20.88 (1.35) | 32.23 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s20 | enlarge_patch/1.5x | 69.66 F | 0.94 | 65.46 F | 12.99 (1.35) | 24.37 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s20 | enlarge_patch/2x | 49.01 F | 5.50 F | 66.54 F | 10.84 (1.35) | 18.34 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s21 | none | 251.86 F | 8.25 F | 234.02 F | 24.96 (1.35) | 56.23 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s21 | enlarge_patch/1.5x | 94.73 F | 3.11 F | 77.08 F | 12.10 (1.35) | 25.05 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s21 | enlarge_patch/2x | 55.15 F | 4.32 F | 58.37 F | 12.89 (1.35) | 18.86 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s22 | none | 155.31 F | 2.83 F | 113.45 F | 20.20 (1.35) | 36.03 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s22 | enlarge_patch/1.5x | 65.73 F | 3.65 F | 60.11 F | 13.26 (1.35) | 23.23 (1.00) | no | no |
| v3_growth_zone_low_texture_z0.03_s22 | enlarge_patch/2x | 66.61 F | 1.17 F | 66.44 F | 15.10 (1.35) | 21.18 (1.00) | no | no |
| v3_growth_zone_midline_jitter_z3_s20 | none | 0.71 | 2.40 F | 36.79 F | 0.68 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s20 | smooth_midline/light | 0.72 | 11.32 F | 19.95 F | 0.94 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s21 | none | 0.90 | 1.01 F | 28.34 F | 0.45 (1.35) | 0.50 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s21 | smooth_midline/light | 0.87 | 1.28 F | 23.92 F | 0.45 (1.35) | 0.57 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s22 | none | 0.69 | 24.58 F | 42.58 F | 0.56 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_midline_jitter_z3_s22 | smooth_midline/light | 0.89 | 27.73 F | 36.79 F | 0.74 (1.35) | 0.44 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s20 | none | 0.64 | 2.95 F | 0.56 | 0.34 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s20 | register_frames | 1.20 | 0.31 | 0.48 | 0.34 (1.35) | 0.14 (1.00) | yes | yes |
| v3_growth_zone_bad_stage_correction_z3_s21 | none | 0.78 | 2.84 F | 0.49 | 0.36 (1.35) | 0.19 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s21 | register_frames | 1.53 | 0.12 | 0.97 | 0.37 (1.35) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_bad_stage_correction_z3_s22 | none | 0.71 | 2.98 F | 0.41 | 0.35 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s22 | register_frames | 1.26 | 0.23 | 0.38 | 0.35 (1.35) | 0.18 (1.00) | yes | yes |
| v3_growth_zone_stage_log_missing_z1_s20 | none | 0.65 | 95.95 F | 0.56 | 0.34 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s20 | register_frames | 1.18 | nan skip | 0.48 | 0.34 (1.35) | 0.14 (1.00) | yes | yes |
| v3_growth_zone_stage_log_missing_z1_s21 | none | 0.79 | 95.84 F | 0.49 | 0.36 (1.35) | 0.19 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s21 | register_frames | 1.03 | nan skip | 1.05 | 0.37 (1.35) | 0.29 (1.00) | yes | yes |
| v3_growth_zone_stage_log_missing_z1_s22 | none | 0.72 | 95.99 F | 0.41 | 0.35 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s22 | register_frames | 1.40 | nan skip | 0.51 | 0.34 (1.35) | 0.23 (1.00) | yes | yes |
| v3_growth_zone_second_root_z30_s20 | none | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s20 | crop_or_mask/crop_to_main_root | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s20 | crop_or_mask/mask_second_root | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | none | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | crop_or_mask/crop_to_main_root | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | crop_or_mask/mask_second_root | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | none | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | crop_or_mask/crop_to_main_root | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | crop_or_mask/mask_second_root | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s20 | none | 299.67 F | 31.92 F | 259.93 F | 20.16 (1.35) | 35.80 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s20 | register_frames | 225.59 F | 37.65 F | 228.47 F | 19.77 (1.35) | 32.32 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s21 | none | 155.13 F | 54.73 F | 116.80 F | 28.58 (1.35) | 33.88 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s21 | register_frames | 127.17 F | 7.09 F | 52.66 F | 12.62 (1.35) | 15.38 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s22 | none | 54.22 F | 36.08 F | 224.62 F | 49.65 (1.35) | 34.48 (1.00) | no | no |
| v3_growth_zone_fast_rotation_z2_s22 | register_frames | 314.94 F | 402.78 F | 505.69 F | 158.36 (1.35) | 149.33 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | none | 15.15 F | 2.88 F | 93.74 F | 5.16 (1.35) | 32.82 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | enlarge_patch/1.5x | 60.66 F | 3.81 F | 135.18 F | 4.54 (1.35) | 35.44 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | enlarge_patch/2x | 32.97 F | 3.69 F | 143.87 F | 4.14 (1.35) | 35.15 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | change_frame_stride/double | 316.74 F | 4.61 F | 147.12 F | 17.13 (1.35) | 37.96 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | change_frame_stride/double + enlarge_patch/1.5x | 77.05 F | 4.38 F | 136.92 F | 5.19 (1.35) | 36.00 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s20 | change_frame_stride/double + enlarge_patch/2x | 65.62 F | 3.99 F | 172.92 F | 4.20 (1.35) | 37.03 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | none | 41.36 F | 2.98 F | 87.30 F | 6.48 (1.35) | 31.55 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | enlarge_patch/1.5x | 30.73 F | 4.05 F | 75.51 F | 4.77 (1.35) | 30.09 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | enlarge_patch/2x | 53.02 F | 4.13 F | 287.10 F | 7.17 (1.35) | 49.14 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | change_frame_stride/double | 92.65 F | 2.97 F | 85.09 F | 10.24 (1.35) | 30.78 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | change_frame_stride/double + enlarge_patch/1.5x | 95.26 F | 4.11 F | 82.76 F | 6.12 (1.35) | 30.00 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s21 | change_frame_stride/double + enlarge_patch/2x | 80.67 F | 4.28 F | 295.40 F | 3.72 (1.35) | 49.69 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | none | 41.37 F | 0.74 | 106.07 F | 4.48 (1.35) | 29.93 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | enlarge_patch/1.5x | 20.69 F | 1.34 F | 66.27 F | 5.87 (1.35) | 22.35 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | enlarge_patch/2x | 87.47 F | 1.16 F | 109.86 F | 2.85 (1.35) | 27.32 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | change_frame_stride/double | 167.96 F | 0.75 | 93.03 F | 7.07 (1.35) | 29.82 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | change_frame_stride/double + enlarge_patch/1.5x | 43.31 F | 1.14 F | 50.40 F | 5.72 (1.35) | 21.15 (1.00) | no | no |
| v3_growth_zone_flank_swap_z0.5_s22 | change_frame_stride/double + enlarge_patch/2x | 165.10 F | 1.19 F | 73.64 F | 2.81 (1.35) | 21.93 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | none | 89.93 F | 0.17 | 24.99 F | 32.05 (1.35) | 6.19 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | enlarge_patch/1.5x | 14.20 F | 0.16 | 17.69 F | 8.90 (1.35) | 3.36 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | enlarge_patch/2x | 0.47 | 0.19 | 13.99 F | 4.03 (1.35) | 2.67 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | change_frame_stride/double | 295.22 F | 4.65 F | 55.09 F | 29.51 (1.35) | 10.90 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | change_frame_stride/double + enlarge_patch/1.5x | 51.95 F | 4.62 F | 11.24 F | 9.47 (1.35) | 2.35 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s20 | change_frame_stride/double + enlarge_patch/2x | 50.36 F | 4.63 F | 10.61 F | 5.11 (1.35) | 1.96 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | none | 80.07 F | 0.16 | 18.83 F | 17.57 (1.35) | 4.53 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | enlarge_patch/1.5x | 3.13 F | 0.19 | 13.13 F | 8.21 (1.35) | 3.03 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | enlarge_patch/2x | 0.58 | 0.21 | 13.17 F | 5.05 (1.35) | 3.27 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | change_frame_stride/double | 90.75 F | 0.12 | 30.43 F | 20.45 (1.35) | 6.47 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | change_frame_stride/double + enlarge_patch/1.5x | 50.37 F | 0.16 | 14.21 F | 8.61 (1.35) | 3.26 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s21 | change_frame_stride/double + enlarge_patch/2x | 62.82 F | 0.19 | 13.85 F | 4.89 (1.35) | 3.41 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | none | 133.51 F | 0.02 | 54.24 F | 14.93 (1.35) | 9.39 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | enlarge_patch/1.5x | 1.89 | 0.09 | 49.62 F | 7.68 (1.35) | 8.60 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | enlarge_patch/2x | 0.57 | 0.16 | 32.01 F | 5.56 (1.35) | 5.69 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | change_frame_stride/double | 180.24 F | 0.06 | 50.63 F | 72.83 (1.35) | 13.62 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | change_frame_stride/double + enlarge_patch/1.5x | 43.88 F | 0.11 | 26.81 F | 7.16 (1.35) | 5.30 (1.00) | no | no |
| v3_growth_zone_partial_occlusion_z20_s22 | change_frame_stride/double + enlarge_patch/2x | 49.45 F | 0.17 | 17.55 F | 5.58 (1.35) | 3.48 (1.00) | no | no |
