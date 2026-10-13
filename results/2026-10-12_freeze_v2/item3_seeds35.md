Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and the fitting remedy gives three passes and a good measurement on at least 2 of 3 seeds. Good: approved tolerance (REGR limit in brackets, 2.5 % of the true peak; flank 1.00 %/h, approved 2026-10-12). Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Seeds 3-5, frozen sizes, the fitting remedy's states (`strong` withdrawn).

| Fault | Size | Label, seeds 0-2 | Label, seeds 3-5 | Differs |
| :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch | 2x6 | repairable | repairable |  |
| width_change | 1/400 | repairable | repairable |  |
| rigid_drift | 0.5 | repairable | repairable |  |
| low_texture | 0.03 | not repairable | not repairable |  |
| midline_jitter | 3 | not repairable | not repairable |  |

Seed 3-5 labels that differ from seeds 0-2: none.

| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | Remedied: three passes and good | Meets criteria |
| :-- | :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch | 2x6 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| width_change | 1/400 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| rigid_drift | 0.5 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| low_texture | 0.03 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |

Labels (from these states only):

| Rod | Label | Repairing remedy |
| :-- | :-- | :-- |
| growth_zone_displacement_exceeds_patch_z2x6_s3 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_displacement_exceeds_patch_z2x6_s4 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_displacement_exceeds_patch_z2x6_s5 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_width_change_s3 | repairable | use_width_free_ratio |
| growth_zone_width_change_s4 | repairable | use_width_free_ratio |
| growth_zone_width_change_s5 | repairable | use_width_free_ratio |
| growth_zone_rigid_drift_z0.5_s3 | repairable | register_frames |
| growth_zone_rigid_drift_z0.5_s4 | repairable | register_frames |
| growth_zone_rigid_drift_z0.5_s5 | repairable | register_frames |
| growth_zone_low_texture_z0.03_s3 | not repairable | - |
| growth_zone_low_texture_z0.03_s4 | not repairable | - |
| growth_zone_low_texture_z0.03_s5 | not repairable | - |
| growth_zone_midline_jitter_z3_s3 | not repairable | - |
| growth_zone_midline_jitter_z3_s4 | not repairable | - |
| growth_zone_midline_jitter_z3_s5 | not repairable | - |

Per run (F = fails the approved threshold):

| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| growth_zone_displacement_exceeds_patch_z2x6_s3 | none | 275.47 F | 95.37 F | 193.74 F | 34.60 (2.17) | 56.79 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s3 | change_frame_stride/half | 155.49 F | 81.57 F | 197.67 F | 31.35 (2.17) | 57.64 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s3 | change_frame_stride/half + change_frame_stride/half | 0.53 | 0.11 | 0.53 | 0.93 (2.17) | 0.17 | yes | yes |
| growth_zone_displacement_exceeds_patch_z2x6_s4 | none | 292.43 F | 126.63 F | 202.39 F | 56.12 (2.17) | 51.88 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s4 | change_frame_stride/half | 163.55 F | 23.36 F | 202.24 F | 31.08 (2.17) | 58.20 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s4 | change_frame_stride/half + change_frame_stride/half | 0.77 | 0.05 | 0.57 | 0.98 (2.17) | 0.23 | yes | yes |
| growth_zone_displacement_exceeds_patch_z2x6_s5 | none | 344.82 F | 127.38 F | 307.02 F | 63.23 (2.17) | 84.28 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s5 | change_frame_stride/half | 303.35 F | 93.81 F | 232.05 F | 47.69 (2.17) | 54.74 | no | no |
| growth_zone_displacement_exceeds_patch_z2x6_s5 | change_frame_stride/half + change_frame_stride/half | 0.84 | 0.10 | 0.92 | 0.99 (2.17) | 0.32 | yes | yes |
| growth_zone_width_change_s3 | none | 0.62 | 0.08 | 3.86 F | 0.41 (1.08) | 0.30 | no | yes |
| growth_zone_width_change_s3 | use_width_free_ratio | 0.62 | 0.08 | 3.86 skip | 0.41 (1.08) | 0.30 | yes | yes |
| growth_zone_width_change_s4 | none | 0.61 | 0.06 | 3.84 F | 0.43 (1.08) | 0.31 | no | yes |
| growth_zone_width_change_s4 | use_width_free_ratio | 0.61 | 0.06 | 3.84 skip | 0.43 (1.08) | 0.31 | yes | yes |
| growth_zone_width_change_s5 | none | 0.52 | 0.23 | 3.47 F | 0.40 (1.08) | 0.28 | no | yes |
| growth_zone_width_change_s5 | use_width_free_ratio | 0.52 | 0.23 | 3.47 skip | 0.40 (1.08) | 0.28 | yes | yes |
| growth_zone_rigid_drift_z0.5_s3 | none | 0.54 | 8.17 F | 0.59 | 0.39 (1.08) | 0.21 | no | yes |
| growth_zone_rigid_drift_z0.5_s3 | register_frames | 1.00 | 0.42 | 0.74 | 0.40 (1.08) | 0.28 | yes | yes |
| growth_zone_rigid_drift_z0.5_s4 | none | 0.62 | 8.03 F | 0.87 | 0.44 (1.08) | 0.28 | no | yes |
| growth_zone_rigid_drift_z0.5_s4 | register_frames | 1.05 | 0.50 | 0.94 | 0.43 (1.08) | 0.32 | yes | yes |
| growth_zone_rigid_drift_z0.5_s5 | none | 0.62 | 8.06 F | 0.77 | 0.45 (1.08) | 0.32 | no | yes |
| growth_zone_rigid_drift_z0.5_s5 | register_frames | 0.73 | 0.63 | 1.34 | 0.46 (1.08) | 0.41 | yes | yes |
| growth_zone_low_texture_z0.03_s3 | none | 107.13 F | 3.68 F | 133.82 F | 15.47 (1.08) | 41.03 | no | no |
| growth_zone_low_texture_z0.03_s3 | enlarge_patch/1.5x | 81.59 F | 6.84 F | 89.44 F | 12.66 (1.08) | 27.02 | no | no |
| growth_zone_low_texture_z0.03_s3 | enlarge_patch/2x | 80.55 F | 1.20 F | 42.82 F | 16.64 (1.08) | 17.40 | no | no |
| growth_zone_low_texture_z0.03_s4 | none | 139.88 F | 6.86 F | 86.56 F | 33.70 (1.08) | 35.03 | no | no |
| growth_zone_low_texture_z0.03_s4 | enlarge_patch/1.5x | 83.76 F | 0.47 | 66.45 F | 15.85 (1.08) | 24.89 | no | no |
| growth_zone_low_texture_z0.03_s4 | enlarge_patch/2x | 56.93 F | 2.17 F | 49.82 F | 13.56 (1.08) | 17.46 | no | no |
| growth_zone_low_texture_z0.03_s5 | none | 76.69 F | 1.39 F | 69.88 F | 19.62 (1.08) | 30.36 | no | no |
| growth_zone_low_texture_z0.03_s5 | enlarge_patch/1.5x | 60.29 F | 2.76 F | 65.72 F | 11.23 (1.08) | 24.12 | no | no |
| growth_zone_low_texture_z0.03_s5 | enlarge_patch/2x | 41.13 F | 0.84 | 40.27 F | 13.49 (1.08) | 17.26 | no | no |
| growth_zone_midline_jitter_z3_s3 | none | 0.67 | 2.70 F | 41.46 F | 0.46 (1.08) | 0.29 | no | yes |
| growth_zone_midline_jitter_z3_s3 | smooth_midline/light | 0.63 | 5.02 F | 41.77 F | 0.46 (1.08) | 0.32 | no | yes |
| growth_zone_midline_jitter_z3_s4 | none | 0.79 | 3.07 F | 52.55 F | 0.40 (1.08) | 0.65 | no | yes |
| growth_zone_midline_jitter_z3_s4 | smooth_midline/light | 0.87 | 2.68 F | 37.18 F | 0.44 (1.08) | 0.52 | no | yes |
| growth_zone_midline_jitter_z3_s5 | none | 0.81 | 3.79 F | 36.16 F | 0.70 (1.08) | 0.58 | no | yes |
| growth_zone_midline_jitter_z3_s5 | smooth_midline/light | 0.46 | 4.73 F | 29.41 F | 0.44 (1.08) | 0.39 | no | yes |
