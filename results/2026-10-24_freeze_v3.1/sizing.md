# Freeze v3.1 sizing: accept_repaired rods that need their repair

Sizing seeds 10, 11, 12. Rule, each part on 3 of 3 seeds: (1) a listed check fails unremedied; (2) the unremedied measurement fails the scoring tolerance; (3) a remedy state of the v3 label sweep passes every check and is good. Smallest size meeting the rule; at most 6 sizes per fault. States already in the v3 cache are reused.

| Fault | Size | Unremedied run | (1) check fails | (2) not good | (3) remedy repairs | Qualifies |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| rigid_drift | 0.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 1.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 2.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 3.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 4.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 5.5 | 3 of 3 | 3 of 3 | 2 of 3 | 0 of 3 | no |
| width_change | v3 (one size) | 3 of 3 | 3 of 3 | 0 of 3 | 3 of 3 | no |
| bad_stage_correction | 3 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| bad_stage_correction | 4 | 3 of 3 | 3 of 3 | 1 of 3 | 0 of 3 | no |
| bad_stage_correction | 5 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 6 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 7 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 8 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | not yet |
| stage_log_missing | 1 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 2x2 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 2x3 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 2x4 | 3 of 3 | 3 of 3 | 3 of 3 | 0 of 3 | no |

- Tracker states still needed: 3
- Sizes so far: {'rigid_drift': None, 'width_change': None, 'bad_stage_correction': None, 'stage_log_missing': None, 'displacement_exceeds_patch': None}

- Result: incomplete

## Per state

| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| v3_growth_zone_rigid_drift_z0.5_s10 | none | 0.91 | 8.04 F | 0.67 | 0.34 (1.35) | 0.24 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s11 | none | 0.72 | 8.17 F | 0.51 | 0.36 (1.35) | 0.19 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s12 | none | 0.77 | 8.08 F | 1.32 | 0.40 (1.35) | 0.30 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s10 | none | 1.00 | 24.24 F | 0.69 | 0.32 (1.35) | 0.24 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s11 | none | 0.80 | 24.37 F | 0.71 | 0.34 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s12 | none | 0.74 | 24.31 F | 0.91 | 0.37 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z2.5_s10 | none | 0.87 | 40.46 F | 0.66 | 0.34 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z2.5_s11 | none | 1.32 | 40.57 F | 0.77 | 0.34 (1.35) | 0.22 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z2.5_s12 | none | 0.70 | 40.51 F | 1.06 | 0.37 (1.35) | 0.29 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z3.5_s10 | none | 0.69 | 56.73 F | 0.75 | 0.37 (1.35) | 0.27 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z3.5_s11 | none | 1.06 | 56.85 F | 0.78 | 0.37 (1.35) | 0.23 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z3.5_s12 | none | 0.87 | 56.76 F | 1.55 | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z4.5_s10 | none | 0.91 | 73.23 F | 0.73 | 0.34 (1.35) | 0.28 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z4.5_s11 | none | 49.21 F | 73.30 F | 0.52 | 0.34 (1.35) | 0.15 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z4.5_s12 | none | 34.35 F | 73.26 F | 0.80 | 0.34 (1.35) | 0.23 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z5.5_s10 | none | 29.30 F | nan skip | 0.64 | 0.36 (1.35) | 0.28 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z5.5_s11 | none | 62.56 F | nan skip | 10.53 F | 0.36 (1.35) | 1.61 (1.00) | no | no |
| v3_growth_zone_rigid_drift_z5.5_s12 | none | 89.28 F | nan skip | 32.88 F | 0.40 (1.35) | 4.96 (1.00) | no | no |
| v3_growth_zone_width_change_s10 | none | 0.68 | 0.03 | 3.86 F | 0.34 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_width_change_s10 | use_width_free_ratio | 0.68 | 0.03 | 3.86 skip | 0.34 (1.35) | 0.35 (1.00) | yes | yes |
| v3_growth_zone_width_change_s11 | none | 0.85 | 0.01 | 3.74 F | 0.34 (1.35) | 0.28 (1.00) | no | yes |
| v3_growth_zone_width_change_s11 | use_width_free_ratio | 0.85 | 0.01 | 3.74 skip | 0.34 (1.35) | 0.28 (1.00) | yes | yes |
| v3_growth_zone_width_change_s12 | none | 0.58 | 0.15 | 3.84 F | 0.37 (1.35) | 0.29 (1.00) | no | yes |
| v3_growth_zone_width_change_s12 | use_width_free_ratio | 0.58 | 0.15 | 3.84 skip | 0.37 (1.35) | 0.29 (1.00) | yes | yes |
| v3_growth_zone_bad_stage_correction_z3_s10 | none | 0.92 | 2.92 F | 0.41 | 0.34 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s11 | none | 0.88 | 2.81 F | 0.39 | 0.32 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s12 | none | 0.65 | 2.87 F | 0.88 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z4_s10 | none | 0.92 | 3.92 F | 0.41 | 0.34 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z4_s11 | none | 1.07 | 3.81 F | 0.39 | 4.72 (1.35) | 0.16 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z4_s12 | none | 0.65 | 3.87 F | 0.88 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z5_s10 | none | 36.32 F | 5.03 F | 135.19 F | 22.39 (1.35) | 23.63 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z5_s11 | none | 87.68 F | 5.30 F | 75.44 F | 19.69 (1.35) | 16.99 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z5_s12 | none | 36.46 F | 12.41 F | 35.00 F | 13.37 (1.35) | 14.37 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z6_s10 | none | 126.19 F | 3.91 F | 148.97 F | 18.28 (1.35) | 39.32 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z6_s11 | none | 165.80 F | 6.11 F | 86.67 F | 41.11 (1.35) | 26.23 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z6_s12 | none | 131.25 F | 9.24 F | 89.37 F | 24.54 (1.35) | 36.86 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z7_s10 | none | 107.32 F | 11.39 F | 134.82 F | 31.47 (1.35) | 46.27 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z7_s11 | none | 139.38 F | 5.28 F | 122.57 F | 39.94 (1.35) | 38.05 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z7_s12 | none | 70.77 F | 10.24 F | 196.02 F | 24.83 (1.35) | 56.55 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z8_s10 | none | 54.78 F | 11.70 F | 161.61 F | 22.44 (1.35) | 50.07 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z8_s11 | none | 81.07 F | 4.63 F | 289.08 F | 30.07 (1.35) | 62.23 (1.00) | no | no |
| v3_growth_zone_bad_stage_correction_z8_s12 | none | 100.49 F | 11.52 F | 181.40 F | 23.11 (1.35) | 40.38 (1.00) | no | no |
| v3_growth_zone_stage_log_missing_z1_s10 | none | 0.92 | 95.92 F | 0.41 | 0.34 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s11 | none | 0.87 | 95.81 F | 0.38 | 0.32 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s12 | none | 0.64 | 95.87 F | 0.88 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s10 | none | 250.76 F | 58.10 F | 219.59 F | 29.63 (2.70) | 40.16 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s10 | change_frame_stride/half | 37.32 F | 0.22 | 0.84 | 0.94 (2.70) | 0.23 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s11 | none | 329.69 F | 60.14 F | 163.99 F | 33.97 (2.70) | 45.51 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s11 | change_frame_stride/half | 35.05 F | 0.21 | 20.79 F | 4.25 (2.70) | 4.33 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s12 | none | 212.97 F | 71.29 F | 139.94 F | 25.78 (2.70) | 42.94 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x2_s12 | change_frame_stride/half | 55.05 F | 0.23 | 1.32 | 0.90 (2.70) | 0.27 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s10 | none | 242.71 F | 126.47 F | 306.10 F | 51.18 (2.70) | 70.89 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s10 | change_frame_stride/half | 38.15 F | 0.20 | 0.70 | 0.91 (2.70) | 0.21 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s11 | none | 356.72 F | 182.39 F | 391.36 F | 61.01 (2.70) | 86.78 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s11 | change_frame_stride/half | 35.89 F | 0.21 | 21.40 F | 4.37 (2.70) | 4.46 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s12 | none | 340.14 F | 93.46 F | 229.57 F | 34.83 (2.70) | 53.86 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x3_s12 | change_frame_stride/half | 56.73 F | 0.21 | 1.37 | 0.89 (2.70) | 0.28 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s10 | none | 288.16 F | 195.82 F | 275.11 F | 46.94 (2.70) | 64.83 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s10 | change_frame_stride/half | 250.76 F | 58.10 F | 219.59 F | 29.63 (2.70) | 40.16 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s10 | change_frame_stride/half + change_frame_stride/half | 37.32 F | 0.22 | 0.84 | 0.94 (2.70) | 0.23 (1.00) | no | yes |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s11 | none | 246.02 F | 146.19 F | 343.33 F | 51.80 (2.70) | 64.49 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s11 | change_frame_stride/half | 329.69 F | 60.14 F | 163.99 F | 33.97 (2.70) | 45.51 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s11 | change_frame_stride/half + change_frame_stride/half | 35.05 F | 0.21 | 20.79 F | 4.25 (2.70) | 4.33 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s12 | none | 330.03 F | 171.87 F | 158.26 F | 80.09 (2.70) | 48.19 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s12 | change_frame_stride/half | 212.97 F | 71.29 F | 139.94 F | 25.78 (2.70) | 42.94 (1.00) | no | no |
| v3_growth_zone_displacement_exceeds_patch_z2x4_s12 | change_frame_stride/half + change_frame_stride/half | 55.05 F | 0.23 | 1.32 | 0.90 (2.70) | 0.27 (1.00) | no | yes |
