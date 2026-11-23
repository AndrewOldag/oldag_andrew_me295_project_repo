# Labels of the held-out compound and novel set

Seeds 40, 41, 42, 43. Tracker only, no agent. States: unremedied, every single remedy step of the action schema and every pair of steps of two different remedies (schema order). Candidate v4 on: a check that cannot be computed after a remedy fails (C3 option a). A state is good when its centre REGR error and flank-difference error are within the scoring tolerance.

| Rod | Expected (proposal) | Label | Repairing states (first named) | Unremedied: checks pass, good |
| :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone_drift_low_texture_s40 | decline | decline | 0 | no, no |
| v3_growth_zone_drift_low_texture_s41 | decline | decline | 0 | no, no |
| v3_growth_zone_drift_low_texture_s42 | decline | decline | 0 | no, no |
| v3_growth_zone_drift_low_texture_s43 | decline | decline | 0 | no, no |
| v3_growth_zone_second_root_occlusion_s40 | decline | decline | 0 | no, no |
| v3_growth_zone_second_root_occlusion_s41 | decline | decline | 0 | no, no |
| v3_growth_zone_second_root_occlusion_s42 | decline | decline | 0 | no, no |
| v3_growth_zone_second_root_occlusion_s43 | decline | decline | 0 | no, no |
| v3_growth_zone_drift_jitter_s40 | decline | decline | 0 | no, yes |
| v3_growth_zone_drift_jitter_s41 | decline | decline | 0 | no, yes |
| v3_growth_zone_drift_jitter_s42 | decline | decline | 0 | no, yes |
| v3_growth_zone_drift_jitter_s43 | decline | decline | 0 | no, yes |
| v3_growth_zone_low_texture_fast_s40 | decline | decline | 0 | no, no |
| v3_growth_zone_low_texture_fast_s41 | decline | decline | 0 | no, no |
| v3_growth_zone_low_texture_fast_s42 | decline | decline | 0 | no, no |
| v3_growth_zone_low_texture_fast_s43 | decline | decline | 0 | no, no |
| v3_growth_zone_focus_drift_z3_s40 | decline | accept_repaired | 12 (enlarge_patch/1.5x) | yes, no |
| v3_growth_zone_focus_drift_z3_s41 | decline | accept_repaired | 2 (enlarge_patch/1.5x + use_width_free_ratio) | no, no |
| v3_growth_zone_focus_drift_z3_s42 | decline | accept_repaired | 2 (enlarge_patch/1.5x + use_width_free_ratio) | no, no |
| v3_growth_zone_focus_drift_z3_s43 | decline | accept_repaired | 7 (use_width_free_ratio) | no, no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | accept_clean | decline | 0 | no, no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | accept_clean | decline | 0 | no, no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | accept_clean | decline | 0 | no, no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | accept_clean | decline | 0 | no, no |

- Rods labelled 24 of 24; states not yet evaluated 0
- Classes: {'accept_clean': 0, 'accept_repaired': 4, 'decline': 20}
- All-decline would score 20 of 24
- Label differs from the expected class: 8: v3_growth_zone_focus_drift_z3_s40, v3_growth_zone_focus_drift_z3_s41, v3_growth_zone_focus_drift_z3_s42, v3_growth_zone_focus_drift_z3_s43, v3_growth_zone_illumination_flicker_z0.1_s40, v3_growth_zone_illumination_flicker_z0.1_s41, v3_growth_zone_illumination_flicker_z0.1_s42, v3_growth_zone_illumination_flicker_z0.1_s43
- Result: complete

## Per state

| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| v3_growth_zone_drift_low_texture_s40 | none | 275.33 F | 9.21 F | 286.52 F | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames | 628.04 F | 204.65 F | nan skip | 302.60 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double | 72.25 F | 16.22 F | 51.44 F | 17.95 (1.35) | 23.29 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light | 150.78 F | 2.86 F | 112.63 F | 26.84 (1.35) | 36.15 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/crop_to_main_root | 275.33 F | 9.21 F | 286.52 F | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/mask_second_root | 275.33 F | 9.21 F | 286.52 F | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | enlarge_patch/1.5x | 60.16 F | 10.25 F | 76.78 F | 11.57 (1.35) | 25.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | enlarge_patch/2x | 47.97 F | 8.13 F | 41.39 F | 9.14 (1.35) | 15.18 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | use_width_free_ratio | 275.33 F | 9.21 F | 286.52 skip | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + change_frame_stride/double | nan skip | nan skip | nan skip | nan (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + smooth_midline/light | 685.43 F | 96.97 F | 563.46 F | 189.97 (1.35) | 193.82 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + crop_or_mask/crop_to_main_root | 631.07 F | nan skip | nan skip | 279.60 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + crop_or_mask/mask_second_root | nan skip | 282.83 F | nan skip | nan (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + enlarge_patch/1.5x | 541.54 F | nan skip | nan skip | 359.58 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + enlarge_patch/2x | 632.93 F | nan skip | 443.13 F | 264.72 (1.35) | 163.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | register_frames + use_width_free_ratio | 628.04 F | 204.65 F | nan skip | 302.60 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + smooth_midline/light | 77.24 F | 15.55 F | 52.35 F | 12.90 (1.35) | 19.66 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 72.25 F | 16.22 F | 51.44 F | 17.95 (1.35) | 23.29 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | 72.25 F | 16.22 F | 51.44 F | 17.95 (1.35) | 23.29 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + enlarge_patch/1.5x | 46.40 F | 16.75 F | 39.93 F | 10.73 (1.35) | 15.52 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + enlarge_patch/2x | 33.96 F | 8.90 F | 36.00 F | 6.83 (1.35) | 13.28 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | change_frame_stride/double + use_width_free_ratio | 72.25 F | 16.22 F | 51.44 skip | 17.95 (1.35) | 23.29 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 150.78 F | 2.86 F | 112.63 F | 26.84 (1.35) | 36.15 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 150.78 F | 2.86 F | 112.63 F | 26.84 (1.35) | 36.15 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light + enlarge_patch/1.5x | 77.37 F | 10.76 F | 91.02 F | 11.01 (1.35) | 26.89 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light + enlarge_patch/2x | 69.94 F | 8.13 F | 42.72 F | 9.12 (1.35) | 15.18 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | smooth_midline/light + use_width_free_ratio | 150.78 F | 2.86 F | 112.63 skip | 26.84 (1.35) | 36.15 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 60.16 F | 10.25 F | 76.78 F | 11.57 (1.35) | 25.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 47.97 F | 8.13 F | 41.39 F | 9.14 (1.35) | 15.18 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 275.33 F | 9.21 F | 286.52 skip | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 60.16 F | 10.25 F | 76.78 F | 11.57 (1.35) | 25.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 47.97 F | 8.13 F | 41.48 F | 9.14 (1.35) | 15.34 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 275.33 F | 9.21 F | 286.52 skip | 22.29 (1.35) | 55.49 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | enlarge_patch/1.5x + use_width_free_ratio | 60.16 F | 10.25 F | 76.78 skip | 11.57 (1.35) | 25.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s40 | enlarge_patch/2x + use_width_free_ratio | 47.97 F | 8.13 F | 41.39 skip | 9.14 (1.35) | 15.18 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | none | 107.17 F | 15.49 F | 145.05 F | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames | 563.44 F | nan skip | 900.14 F | 279.38 (1.35) | 324.14 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double | 102.45 F | 10.06 F | 79.05 F | 13.40 (1.35) | 24.45 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light | 127.79 F | 13.39 F | 88.96 F | 15.88 (1.35) | 35.82 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/crop_to_main_root | 107.17 F | 15.49 F | 145.05 F | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/mask_second_root | 107.17 F | 15.49 F | 145.05 F | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | enlarge_patch/1.5x | 64.16 F | 12.28 F | 51.69 F | 13.66 (1.35) | 23.97 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | enlarge_patch/2x | 50.71 F | 11.88 F | 43.25 F | 9.96 (1.35) | 16.36 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | use_width_free_ratio | 107.17 F | 15.49 F | 145.05 skip | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + change_frame_stride/double | 573.19 F | 215.44 F | nan skip | 279.62 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + smooth_midline/light | 574.66 F | nan skip | 1000.37 F | 218.07 (1.35) | 313.83 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + crop_or_mask/crop_to_main_root | 605.64 F | nan skip | 383.49 F | 256.55 (1.35) | 300.90 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + crop_or_mask/mask_second_root | 411.46 F | 113.76 F | nan skip | 201.14 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + enlarge_patch/1.5x | 502.19 F | nan skip | 378.86 F | 270.72 (1.35) | 201.86 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + enlarge_patch/2x | 548.18 F | nan skip | 531.87 F | 208.55 (1.35) | 200.39 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | register_frames + use_width_free_ratio | 563.44 F | nan skip | 900.14 skip | 279.38 (1.35) | 324.14 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + smooth_midline/light | 62.43 F | 9.32 F | 69.45 F | 10.79 (1.35) | 23.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 102.45 F | 10.06 F | 79.05 F | 13.40 (1.35) | 24.45 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 102.45 F | 10.06 F | 79.05 F | 13.40 (1.35) | 24.45 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + enlarge_patch/1.5x | 49.18 F | 9.86 F | 34.70 F | 9.14 (1.35) | 13.81 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + enlarge_patch/2x | 36.34 F | 7.77 F | 34.57 F | 8.27 (1.35) | 11.55 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | change_frame_stride/double + use_width_free_ratio | 102.45 F | 10.06 F | 79.05 skip | 13.40 (1.35) | 24.45 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 127.79 F | 13.39 F | 88.96 F | 15.88 (1.35) | 35.82 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 127.79 F | 13.39 F | 88.96 F | 15.88 (1.35) | 35.82 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light + enlarge_patch/1.5x | 81.52 F | 12.28 F | 63.72 F | 13.00 (1.35) | 23.55 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light + enlarge_patch/2x | 53.73 F | 11.88 F | 38.46 F | 9.96 (1.35) | 15.02 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | smooth_midline/light + use_width_free_ratio | 127.79 F | 13.39 F | 88.96 skip | 15.88 (1.35) | 35.82 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 64.16 F | 12.28 F | 51.69 F | 13.66 (1.35) | 23.97 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 50.71 F | 11.88 F | 43.25 F | 9.96 (1.35) | 16.36 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 107.17 F | 15.49 F | 145.05 skip | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 64.16 F | 12.28 F | 51.69 F | 13.66 (1.35) | 23.97 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 50.71 F | 11.88 F | 43.25 F | 9.96 (1.35) | 16.29 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 107.17 F | 15.49 F | 145.05 skip | 20.88 (1.35) | 37.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | enlarge_patch/1.5x + use_width_free_ratio | 64.16 F | 12.28 F | 51.69 skip | 13.66 (1.35) | 23.97 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s41 | enlarge_patch/2x + use_width_free_ratio | 50.71 F | 11.88 F | 43.25 skip | 9.96 (1.35) | 16.36 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | none | 123.33 F | 10.46 F | 92.10 F | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames | 490.91 F | nan skip | nan skip | 123.28 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double | 83.52 F | 15.86 F | 78.92 F | 15.19 (1.35) | 22.94 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light | 192.31 F | 12.42 F | 141.68 F | 24.94 (1.35) | 34.26 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/crop_to_main_root | 123.33 F | 10.46 F | 92.10 F | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/mask_second_root | 123.33 F | 10.46 F | 92.10 F | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | enlarge_patch/1.5x | 70.21 F | 15.19 F | 42.31 F | 15.66 (1.35) | 18.84 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | enlarge_patch/2x | 48.95 F | 10.91 F | 62.08 F | 10.17 (1.35) | 19.92 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | use_width_free_ratio | 123.33 F | 10.46 F | 92.10 skip | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + change_frame_stride/double | 442.48 F | 60.08 F | 465.83 F | 92.92 (1.35) | 164.42 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + smooth_midline/light | 495.63 F | 163.95 F | 392.21 F | 228.27 (1.35) | 154.98 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + crop_or_mask/crop_to_main_root | 663.54 F | 168.21 F | nan skip | 201.64 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + crop_or_mask/mask_second_root | 554.62 F | nan skip | nan skip | 143.66 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + enlarge_patch/1.5x | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + enlarge_patch/2x | 508.70 F | 143.52 F | 266.62 F | 133.46 (1.35) | 94.98 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | register_frames + use_width_free_ratio | 490.91 F | nan skip | nan skip | 123.28 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + smooth_midline/light | 81.71 F | 12.60 F | 53.96 F | 11.67 (1.35) | 21.46 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 83.52 F | 15.86 F | 78.92 F | 15.19 (1.35) | 22.94 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 83.52 F | 15.86 F | 78.92 F | 15.19 (1.35) | 22.94 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + enlarge_patch/1.5x | 51.18 F | 12.28 F | 33.91 F | 11.51 (1.35) | 14.45 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + enlarge_patch/2x | 53.07 F | 10.40 F | 25.88 F | 6.21 (1.35) | 10.48 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | change_frame_stride/double + use_width_free_ratio | 83.52 F | 15.86 F | 78.92 skip | 15.19 (1.35) | 22.94 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 192.31 F | 12.42 F | 141.68 F | 24.94 (1.35) | 34.26 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 192.31 F | 12.42 F | 141.68 F | 24.94 (1.35) | 34.26 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light + enlarge_patch/1.5x | 91.52 F | 15.20 F | 53.77 F | 15.61 (1.35) | 20.43 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light + enlarge_patch/2x | 76.83 F | 10.91 F | 66.95 F | 10.18 (1.35) | 20.44 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | smooth_midline/light + use_width_free_ratio | 192.31 F | 12.42 F | 141.68 skip | 24.94 (1.35) | 34.26 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 70.21 F | 15.19 F | 42.31 F | 15.66 (1.35) | 18.84 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 48.95 F | 10.91 F | 62.08 F | 10.17 (1.35) | 19.92 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 123.33 F | 10.46 F | 92.10 skip | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 70.21 F | 15.19 F | 42.31 F | 15.66 (1.35) | 18.84 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 48.95 F | 10.91 F | 62.08 F | 10.17 (1.35) | 20.15 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 123.33 F | 10.46 F | 92.10 skip | 21.21 (1.35) | 31.38 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | enlarge_patch/1.5x + use_width_free_ratio | 70.21 F | 15.19 F | 42.31 skip | 15.66 (1.35) | 18.84 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s42 | enlarge_patch/2x + use_width_free_ratio | 48.95 F | 10.91 F | 62.08 skip | 10.17 (1.35) | 19.92 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | none | 177.20 F | 14.04 F | 125.12 F | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames | 554.71 F | nan skip | nan skip | 230.36 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double | 358.88 F | 20.16 F | 72.14 F | 15.70 (1.35) | 28.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light | 109.94 F | 13.45 F | 133.35 F | 23.27 (1.35) | 34.47 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/crop_to_main_root | 177.20 F | 14.04 F | 125.12 F | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/mask_second_root | 177.20 F | 14.04 F | 125.12 F | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | enlarge_patch/1.5x | 58.39 F | 13.06 F | 77.02 F | 15.82 (1.35) | 26.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | enlarge_patch/2x | 73.77 F | 5.51 F | 61.68 F | 10.26 (1.35) | 20.44 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | use_width_free_ratio | 177.20 F | 14.04 F | 125.12 skip | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + change_frame_stride/double | 350.00 F | nan skip | 149.84 F | 139.69 (1.35) | 52.34 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + smooth_midline/light | 1058.24 F | nan skip | 1365.93 F | 201.66 (1.35) | 318.14 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + crop_or_mask/crop_to_main_root | 576.08 F | 53.86 F | nan skip | 203.35 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + crop_or_mask/mask_second_root | nan skip | 106.14 F | nan skip | nan (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + enlarge_patch/1.5x | 625.62 F | nan skip | 731.99 F | 176.07 (1.35) | 248.65 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + enlarge_patch/2x | 297.57 F | 114.44 F | 196.56 F | 87.38 (1.35) | 70.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | register_frames + use_width_free_ratio | 554.71 F | nan skip | nan skip | 230.36 (1.35) | nan (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + smooth_midline/light | 75.57 F | 16.89 F | 74.03 F | 13.94 (1.35) | 24.34 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 358.88 F | 20.16 F | 72.14 F | 15.70 (1.35) | 28.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 358.88 F | 20.16 F | 72.14 F | 15.70 (1.35) | 28.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + enlarge_patch/1.5x | 91.34 F | 14.32 F | 44.95 F | 12.95 (1.35) | 17.62 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + enlarge_patch/2x | 83.01 F | 9.33 F | 49.65 F | 8.26 (1.35) | 15.59 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | change_frame_stride/double + use_width_free_ratio | 358.88 F | 20.16 F | 72.14 skip | 15.70 (1.35) | 28.31 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 109.94 F | 13.45 F | 133.35 F | 23.27 (1.35) | 34.47 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 109.94 F | 13.45 F | 133.35 F | 23.27 (1.35) | 34.47 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light + enlarge_patch/1.5x | 78.02 F | 12.73 F | 57.13 F | 15.89 (1.35) | 24.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light + enlarge_patch/2x | 67.13 F | 5.55 F | 53.79 F | 10.28 (1.35) | 18.85 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | smooth_midline/light + use_width_free_ratio | 109.94 F | 13.45 F | 133.35 skip | 23.27 (1.35) | 34.47 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 58.39 F | 13.06 F | 77.02 F | 15.82 (1.35) | 26.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 73.77 F | 5.51 F | 61.68 F | 10.26 (1.35) | 20.44 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 177.20 F | 14.04 F | 125.12 skip | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 58.39 F | 13.06 F | 77.02 F | 15.82 (1.35) | 26.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 74.18 F | 5.51 F | 61.68 F | 10.26 (1.35) | 19.95 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 177.20 F | 14.04 F | 125.12 skip | 28.44 (1.35) | 48.11 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | enlarge_patch/1.5x + use_width_free_ratio | 58.39 F | 13.06 F | 77.02 skip | 15.82 (1.35) | 26.88 (1.00) | no | no |
| v3_growth_zone_drift_low_texture_s43 | enlarge_patch/2x + use_width_free_ratio | 73.77 F | 5.51 F | 61.68 skip | 10.26 (1.35) | 20.44 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | none | 87.05 F | 0.16 | 56.66 F | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames | 57.26 F | 0.03 | 58.14 F | 14.91 (1.35) | 12.33 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double | 70.84 F | 0.10 | 100.66 F | 16.58 (1.35) | 19.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light | 171.34 F | 0.16 | 55.36 F | 33.60 (1.35) | 10.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/crop_to_main_root | 87.05 F | 0.16 | 56.66 F | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/mask_second_root | 87.05 F | 0.16 | 56.66 F | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | enlarge_patch/1.5x | 4.07 F | 0.20 | 22.67 F | 7.96 (1.35) | 5.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | enlarge_patch/2x | 2.47 F | 0.24 | 18.53 F | 4.00 (1.35) | 4.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | use_width_free_ratio | 87.05 F | 0.16 | 56.66 skip | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + change_frame_stride/double | 118.52 F | 0.10 | 56.11 F | 30.24 (1.35) | 13.93 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + smooth_midline/light | 71.91 F | 0.04 | 56.79 F | 11.62 (1.35) | 11.28 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + crop_or_mask/crop_to_main_root | 57.26 F | 0.03 | 58.14 F | 14.91 (1.35) | 12.33 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + crop_or_mask/mask_second_root | 57.26 F | 0.03 | 58.14 F | 14.91 (1.35) | 12.33 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + enlarge_patch/1.5x | 2.42 F | 0.02 | 22.82 F | 8.51 (1.35) | 5.59 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + enlarge_patch/2x | 2.88 F | 0.03 | 18.45 F | 4.06 (1.35) | 4.73 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | register_frames + use_width_free_ratio | 57.26 F | 0.03 | 58.14 skip | 14.91 (1.35) | 12.33 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + smooth_midline/light | 148.93 F | 0.10 | 47.65 F | 20.95 (1.35) | 10.80 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 70.84 F | 0.10 | 100.66 F | 16.58 (1.35) | 19.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | 70.84 F | 0.10 | 100.66 F | 16.58 (1.35) | 19.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + enlarge_patch/1.5x | 141.25 F | 0.14 | 22.32 F | 10.29 (1.35) | 5.31 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + enlarge_patch/2x | 127.41 F | 0.20 | 20.13 F | 4.26 (1.35) | 4.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | change_frame_stride/double + use_width_free_ratio | 70.84 F | 0.10 | 100.66 skip | 16.58 (1.35) | 19.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 171.34 F | 0.16 | 55.36 F | 33.60 (1.35) | 10.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 171.34 F | 0.16 | 55.36 F | 33.60 (1.35) | 10.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light + enlarge_patch/1.5x | 17.05 F | 0.20 | 22.43 F | 7.96 (1.35) | 5.59 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light + enlarge_patch/2x | 6.06 F | 0.24 | 18.32 F | 4.00 (1.35) | 4.75 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | smooth_midline/light + use_width_free_ratio | 171.34 F | 0.16 | 55.36 skip | 33.60 (1.35) | 10.27 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 4.07 F | 0.20 | 22.67 F | 7.96 (1.35) | 5.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.47 F | 0.24 | 18.53 F | 4.00 (1.35) | 4.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 87.05 F | 0.16 | 56.66 skip | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 4.07 F | 0.20 | 22.67 F | 7.96 (1.35) | 5.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.47 F | 0.24 | 18.53 F | 4.00 (1.35) | 4.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 87.05 F | 0.16 | 56.66 skip | 27.77 (1.35) | 11.71 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | enlarge_patch/1.5x + use_width_free_ratio | 4.07 F | 0.20 | 22.67 skip | 7.96 (1.35) | 5.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s40 | enlarge_patch/2x + use_width_free_ratio | 2.47 F | 0.24 | 18.53 skip | 4.00 (1.35) | 4.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | none | 43.31 F | 0.19 | 38.76 F | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames | 73.66 F | 0.21 | 39.60 F | 25.92 (1.35) | 8.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double | 130.56 F | 0.08 | 84.22 F | 24.99 (1.35) | 15.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light | 40.33 F | 0.19 | 31.82 F | 18.63 (1.35) | 7.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/crop_to_main_root | 43.31 F | 0.19 | 38.76 F | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/mask_second_root | 43.31 F | 0.19 | 38.76 F | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | enlarge_patch/1.5x | 2.08 F | 0.21 | 16.56 F | 19.66 (1.35) | 3.52 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | enlarge_patch/2x | 0.89 | 0.23 | 15.50 F | 4.62 (1.35) | 3.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | use_width_free_ratio | 43.31 F | 0.19 | 38.76 skip | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + change_frame_stride/double | 32.27 F | 0.27 | 84.02 F | 22.33 (1.35) | 15.91 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + smooth_midline/light | 18.19 F | 0.20 | 33.03 F | 20.08 (1.35) | 7.97 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + crop_or_mask/crop_to_main_root | 73.66 F | 0.21 | 39.60 F | 25.92 (1.35) | 8.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + crop_or_mask/mask_second_root | 73.66 F | 0.21 | 39.60 F | 25.92 (1.35) | 8.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + enlarge_patch/1.5x | 1.91 | 0.19 | 16.05 F | 19.70 (1.35) | 3.47 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + enlarge_patch/2x | 1.74 | 0.16 | 15.52 F | 4.66 (1.35) | 3.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | register_frames + use_width_free_ratio | 73.66 F | 0.21 | 39.60 skip | 25.92 (1.35) | 8.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + smooth_midline/light | 69.39 F | 0.09 | 82.88 F | 20.90 (1.35) | 15.01 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 130.56 F | 0.08 | 84.22 F | 24.99 (1.35) | 15.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 130.56 F | 0.08 | 84.22 F | 24.99 (1.35) | 15.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + enlarge_patch/1.5x | 106.23 F | 0.12 | 16.30 F | 12.36 (1.35) | 3.34 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + enlarge_patch/2x | 139.13 F | 0.16 | 11.85 F | 4.41 (1.35) | 2.59 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | change_frame_stride/double + use_width_free_ratio | 130.56 F | 0.08 | 84.22 skip | 24.99 (1.35) | 15.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 40.33 F | 0.19 | 31.82 F | 18.63 (1.35) | 7.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 40.33 F | 0.19 | 31.82 F | 18.63 (1.35) | 7.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light + enlarge_patch/1.5x | 52.97 F | 0.21 | 16.42 F | 19.66 (1.35) | 3.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light + enlarge_patch/2x | 3.09 F | 0.23 | 15.42 F | 4.62 (1.35) | 3.17 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | smooth_midline/light + use_width_free_ratio | 40.33 F | 0.19 | 31.82 skip | 18.63 (1.35) | 7.77 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 2.08 F | 0.21 | 16.56 F | 19.66 (1.35) | 3.52 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.89 | 0.23 | 15.50 F | 4.62 (1.35) | 3.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 43.31 F | 0.19 | 38.76 skip | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 2.08 F | 0.21 | 16.56 F | 19.66 (1.35) | 3.52 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.89 | 0.23 | 15.60 F | 4.62 (1.35) | 3.21 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 43.31 F | 0.19 | 38.76 skip | 23.25 (1.35) | 8.87 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | enlarge_patch/1.5x + use_width_free_ratio | 2.08 F | 0.21 | 16.56 skip | 19.66 (1.35) | 3.52 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s41 | enlarge_patch/2x + use_width_free_ratio | 0.89 | 0.23 | 15.50 skip | 4.62 (1.35) | 3.18 (1.00) | yes | no |
| v3_growth_zone_second_root_occlusion_s42 | none | 157.92 F | 0.10 | 39.04 F | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames | 254.53 F | 0.25 | 38.57 F | 47.29 (1.35) | 9.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double | 264.35 F | 0.10 | 55.28 F | 36.51 (1.35) | 16.38 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light | 135.42 F | 0.11 | 42.82 F | 33.38 (1.35) | 14.07 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/crop_to_main_root | 157.92 F | 0.10 | 39.04 F | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/mask_second_root | 216.01 F | 0.10 | 39.04 F | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | enlarge_patch/1.5x | 9.89 F | 0.15 | 46.05 F | 9.58 (1.35) | 9.02 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | enlarge_patch/2x | 0.59 | 0.19 | 17.95 F | 4.41 (1.35) | 4.80 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | use_width_free_ratio | 157.92 F | 0.10 | 39.04 skip | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + change_frame_stride/double | 287.88 F | 0.24 | 54.68 F | 65.50 (1.35) | 15.82 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + smooth_midline/light | 70.86 F | 0.22 | 44.00 F | 34.24 (1.35) | 14.69 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + crop_or_mask/crop_to_main_root | 254.52 F | 0.25 | 38.57 F | 47.29 (1.35) | 9.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + crop_or_mask/mask_second_root | 254.52 F | 0.25 | 38.57 F | 47.29 (1.35) | 9.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + enlarge_patch/1.5x | 102.18 F | 0.19 | 45.57 F | 9.39 (1.35) | 8.89 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + enlarge_patch/2x | 1.41 | 0.14 | 17.96 F | 4.47 (1.35) | 4.80 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | register_frames + use_width_free_ratio | 254.53 F | 0.25 | 38.57 skip | 47.29 (1.35) | 9.50 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + smooth_midline/light | 219.10 F | 0.11 | 69.78 F | 22.27 (1.35) | 16.74 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 260.83 F | 0.10 | 55.40 F | 35.62 (1.35) | 16.40 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 259.75 F | 0.10 | 55.49 F | 35.49 (1.35) | 16.41 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + enlarge_patch/1.5x | 42.33 F | 0.15 | 65.05 F | 8.40 (1.35) | 13.63 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + enlarge_patch/2x | 4.16 F | 0.18 | 61.91 F | 4.22 (1.35) | 12.48 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | change_frame_stride/double + use_width_free_ratio | 264.35 F | 0.10 | 55.28 skip | 36.51 (1.35) | 16.38 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 135.42 F | 0.11 | 42.82 F | 33.38 (1.35) | 14.07 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 135.42 F | 0.11 | 42.82 F | 33.38 (1.35) | 14.07 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light + enlarge_patch/1.5x | 11.19 F | 0.15 | 46.40 F | 9.58 (1.35) | 9.06 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light + enlarge_patch/2x | 27.65 F | 0.19 | 17.94 F | 4.41 (1.35) | 4.80 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | smooth_midline/light + use_width_free_ratio | 135.42 F | 0.11 | 42.82 skip | 33.38 (1.35) | 14.07 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 9.89 F | 0.15 | 46.05 F | 9.58 (1.35) | 9.02 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.59 | 0.19 | 17.95 F | 4.41 (1.35) | 4.80 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 157.92 F | 0.10 | 39.04 skip | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 9.89 F | 0.15 | 46.05 F | 9.58 (1.35) | 9.02 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.64 | 0.19 | 17.95 F | 4.41 (1.35) | 4.81 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 216.01 F | 0.10 | 39.04 skip | 17.10 (1.35) | 10.70 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | enlarge_patch/1.5x + use_width_free_ratio | 9.89 F | 0.15 | 46.05 skip | 9.58 (1.35) | 9.02 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s42 | enlarge_patch/2x + use_width_free_ratio | 0.59 | 0.19 | 17.95 skip | 4.41 (1.35) | 4.80 (1.00) | yes | no |
| v3_growth_zone_second_root_occlusion_s43 | none | 174.55 F | 0.14 | 50.76 F | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames | 222.67 F | 0.18 | 41.64 F | 66.70 (1.35) | 12.54 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double | 113.22 F | 0.10 | 61.39 F | 21.00 (1.35) | 16.05 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light | 150.69 F | 0.15 | 40.06 F | 10.00 (1.35) | 9.47 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/crop_to_main_root | 174.55 F | 0.14 | 50.76 F | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/mask_second_root | 174.55 F | 0.14 | 50.76 F | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | enlarge_patch/1.5x | 8.12 F | 0.18 | 37.30 F | 8.85 (1.35) | 7.66 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | enlarge_patch/2x | 2.81 F | 0.23 | 21.38 F | 7.05 (1.35) | 5.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | use_width_free_ratio | 174.55 F | 0.14 | 50.76 skip | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + change_frame_stride/double | 244.12 F | 0.20 | 57.75 F | 74.88 (1.35) | 18.61 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + smooth_midline/light | 75.00 F | 0.17 | 41.05 F | 9.50 (1.35) | 9.03 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + crop_or_mask/crop_to_main_root | 230.03 F | 0.18 | 41.97 F | 69.59 (1.35) | 12.90 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + crop_or_mask/mask_second_root | 276.19 F | 0.18 | 45.36 F | 127.96 (1.35) | 17.06 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + enlarge_patch/1.5x | 8.29 F | 0.14 | 36.71 F | 9.08 (1.35) | 7.52 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + enlarge_patch/2x | 1.22 | 0.10 | 21.24 F | 7.11 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | register_frames + use_width_free_ratio | 222.67 F | 0.18 | 41.64 skip | 66.70 (1.35) | 12.54 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + smooth_midline/light | 152.74 F | 0.11 | 57.84 F | 21.35 (1.35) | 13.10 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 113.22 F | 0.10 | 61.39 F | 21.00 (1.35) | 16.05 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 113.22 F | 0.10 | 61.39 F | 21.00 (1.35) | 16.05 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + enlarge_patch/1.5x | 74.14 F | 0.14 | 36.60 F | 8.63 (1.35) | 9.26 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + enlarge_patch/2x | 70.63 F | 0.19 | 33.95 F | 7.00 (1.35) | 7.48 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | change_frame_stride/double + use_width_free_ratio | 113.22 F | 0.10 | 61.39 skip | 21.00 (1.35) | 16.05 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 150.69 F | 0.15 | 40.06 F | 10.00 (1.35) | 9.47 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 150.69 F | 0.15 | 40.06 F | 10.00 (1.35) | 9.47 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light + enlarge_patch/1.5x | 9.76 F | 0.18 | 37.19 F | 8.85 (1.35) | 7.64 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light + enlarge_patch/2x | 37.93 F | 0.23 | 21.31 F | 7.05 (1.35) | 5.17 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | smooth_midline/light + use_width_free_ratio | 150.69 F | 0.15 | 40.06 skip | 10.00 (1.35) | 9.47 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 8.12 F | 0.18 | 37.30 F | 8.85 (1.35) | 7.66 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.81 F | 0.23 | 21.38 F | 7.05 (1.35) | 5.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 174.55 F | 0.14 | 50.76 skip | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 8.12 F | 0.18 | 37.30 F | 8.85 (1.35) | 7.66 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.81 F | 0.23 | 21.38 F | 7.05 (1.35) | 5.18 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 174.55 F | 0.14 | 50.76 skip | 12.58 (1.35) | 10.29 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | enlarge_patch/1.5x + use_width_free_ratio | 8.12 F | 0.18 | 37.30 skip | 8.85 (1.35) | 7.66 (1.00) | no | no |
| v3_growth_zone_second_root_occlusion_s43 | enlarge_patch/2x + use_width_free_ratio | 2.81 F | 0.23 | 21.38 skip | 7.05 (1.35) | 5.18 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s40 | none | 0.67 | 21.16 F | 44.22 F | 0.57 (1.35) | 0.53 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames | 2.41 F | 19.03 F | 44.26 F | 0.60 (1.35) | 0.63 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double | 216.42 F | 21.19 F | 44.10 F | 0.57 (1.35) | 3.93 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light | 0.53 | 13.15 F | 17.92 F | 0.44 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/crop_to_main_root | 0.67 | 21.16 F | 44.22 F | 0.57 (1.35) | 0.53 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/mask_second_root | 0.67 | 21.16 F | 44.22 F | 0.57 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | enlarge_patch/1.5x | 0.56 | 21.19 F | 44.19 F | 0.64 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | enlarge_patch/2x | 0.51 | 21.21 F | 44.11 F | 0.77 (1.35) | 0.48 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | use_width_free_ratio | 0.67 | 21.16 F | 44.22 skip | 0.57 (1.35) | 0.53 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + change_frame_stride/double | 1.24 | 19.04 F | 44.23 F | 0.61 (1.35) | 0.56 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + smooth_midline/light | 2.80 F | 9.92 F | 17.43 F | 0.48 (1.35) | 0.57 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + crop_or_mask/crop_to_main_root | 2.41 F | 19.03 F | 44.26 F | 0.60 (1.35) | 0.63 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + crop_or_mask/mask_second_root | 2.41 F | 19.03 F | 44.26 F | 0.60 (1.35) | 0.65 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + enlarge_patch/1.5x | 1.67 | 19.04 F | 44.15 F | 0.65 (1.35) | 0.57 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + enlarge_patch/2x | 1.42 | 19.04 F | 44.06 F | 0.78 (1.35) | 0.53 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | register_frames + use_width_free_ratio | 2.41 F | 19.03 F | 44.26 skip | 0.60 (1.35) | 0.63 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + smooth_midline/light | 101.33 F | 19.45 F | 58.64 F | 2.95 (1.35) | 6.93 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 216.42 F | 21.19 F | 44.10 F | 0.57 (1.35) | 3.93 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | 216.42 F | 21.19 F | 44.10 F | 0.57 (1.35) | 3.95 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + enlarge_patch/1.5x | 244.29 F | 21.22 F | 44.04 F | 0.63 (1.35) | 0.46 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + enlarge_patch/2x | 274.89 F | 21.23 F | 43.95 F | 0.77 (1.35) | 0.47 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | change_frame_stride/double + use_width_free_ratio | 216.42 F | 21.19 F | 44.10 skip | 0.57 (1.35) | 3.93 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 0.53 | 13.15 F | 17.92 F | 0.44 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 0.53 | 13.15 F | 17.92 F | 0.44 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light + enlarge_patch/1.5x | 0.40 | 13.15 F | 17.95 F | 0.51 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light + enlarge_patch/2x | 0.33 | 13.17 F | 17.94 F | 0.66 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | smooth_midline/light + use_width_free_ratio | 0.53 | 13.15 F | 17.92 skip | 0.44 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.56 | 21.19 F | 44.19 F | 0.64 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.51 | 21.21 F | 44.11 F | 0.77 (1.35) | 0.48 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 0.67 | 21.16 F | 44.22 skip | 0.57 (1.35) | 0.53 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.56 | 21.19 F | 44.24 F | 0.64 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.51 | 21.21 F | 44.15 F | 0.77 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 0.67 | 21.16 F | 44.22 skip | 0.57 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | enlarge_patch/1.5x + use_width_free_ratio | 0.56 | 21.19 F | 44.19 skip | 0.64 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s40 | enlarge_patch/2x + use_width_free_ratio | 0.51 | 21.21 F | 44.11 skip | 0.77 (1.35) | 0.48 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | none | 0.58 | 11.57 F | 37.14 F | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames | 2.24 F | 7.94 F | 37.69 F | 0.69 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double | 78.19 F | 11.65 F | 41.21 F | 11.90 (1.35) | 4.46 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light | 0.64 | 8.25 F | 19.73 F | 0.56 (1.35) | 0.52 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/crop_to_main_root | 0.58 | 11.57 F | 37.14 F | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/mask_second_root | 0.58 | 11.57 F | 37.11 F | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | enlarge_patch/1.5x | 0.55 | 11.62 F | 37.06 F | 0.77 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | enlarge_patch/2x | 0.53 | 11.66 F | 37.11 F | 0.87 (1.35) | 0.65 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | use_width_free_ratio | 0.58 | 11.57 F | 37.14 skip | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + change_frame_stride/double | 1.10 | 7.90 F | 41.34 F | 0.69 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + smooth_midline/light | 2.13 F | 1.82 F | 19.54 F | 0.65 (1.35) | 0.71 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + crop_or_mask/crop_to_main_root | 2.24 F | 7.94 F | 37.69 F | 0.69 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + crop_or_mask/mask_second_root | 2.24 F | 7.94 F | 37.66 F | 0.69 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + enlarge_patch/1.5x | 1.53 | 7.93 F | 37.45 F | 0.74 (1.35) | 0.68 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + enlarge_patch/2x | 1.24 | 7.90 F | 37.38 F | 0.85 (1.35) | 0.71 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | register_frames + use_width_free_ratio | 2.24 F | 7.94 F | 37.69 skip | 0.69 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + smooth_midline/light | 76.41 F | 18.61 F | 42.21 F | 3.21 (1.35) | 0.50 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 78.19 F | 11.65 F | 41.21 F | 11.90 (1.35) | 4.46 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 78.19 F | 11.65 F | 41.21 F | 11.90 (1.35) | 4.46 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + enlarge_patch/1.5x | 63.95 F | 11.68 F | 41.21 F | 0.76 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + enlarge_patch/2x | 48.28 F | 11.71 F | 41.25 F | 0.87 (1.35) | 0.64 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | change_frame_stride/double + use_width_free_ratio | 78.19 F | 11.65 F | 41.21 skip | 11.90 (1.35) | 4.46 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 0.64 | 8.25 F | 19.73 F | 0.56 (1.35) | 0.52 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 0.64 | 8.25 F | 19.73 F | 0.56 (1.35) | 0.52 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light + enlarge_patch/1.5x | 0.58 | 8.26 F | 19.92 F | 0.62 (1.35) | 0.52 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light + enlarge_patch/2x | 0.56 | 8.32 F | 20.09 F | 0.73 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | smooth_midline/light + use_width_free_ratio | 0.64 | 8.25 F | 19.73 skip | 0.56 (1.35) | 0.52 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.55 | 11.62 F | 37.06 F | 0.77 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.53 | 11.66 F | 37.11 F | 0.87 (1.35) | 0.65 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 0.58 | 11.57 F | 37.14 skip | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.55 | 11.62 F | 37.05 F | 0.77 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.53 | 11.69 F | 37.05 F | 0.87 (1.35) | 0.65 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 0.58 | 11.57 F | 37.11 skip | 0.71 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | enlarge_patch/1.5x + use_width_free_ratio | 0.55 | 11.62 F | 37.06 skip | 0.77 (1.35) | 0.61 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s41 | enlarge_patch/2x + use_width_free_ratio | 0.53 | 11.66 F | 37.11 skip | 0.87 (1.35) | 0.65 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | none | 0.63 | 8.27 F | 53.78 F | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames | 1.73 | 1.84 F | 54.19 F | 0.47 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double | 71.41 F | 16.08 F | 58.99 F | 4.50 (1.35) | 11.14 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light | 0.55 | 8.36 F | 30.53 F | 0.41 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/crop_to_main_root | 0.63 | 8.27 F | 53.78 F | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/mask_second_root | 0.63 | 8.27 F | 53.78 F | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | enlarge_patch/1.5x | 0.55 | 8.28 F | 53.80 F | 0.49 (1.35) | 0.33 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | enlarge_patch/2x | 0.54 | 8.33 F | 53.78 F | 0.65 (1.35) | 0.31 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | use_width_free_ratio | 0.63 | 8.27 F | 53.78 skip | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + change_frame_stride/double | 0.73 | 1.81 F | 61.73 F | 0.42 (1.35) | 10.53 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | register_frames + smooth_midline/light | 1.31 | 2.61 F | 30.61 F | 0.45 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + crop_or_mask/crop_to_main_root | 1.73 | 1.84 F | 54.19 F | 0.47 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + crop_or_mask/mask_second_root | 1.73 | 1.84 F | 54.19 F | 0.47 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + enlarge_patch/1.5x | 1.22 | 1.82 F | 54.14 F | 0.52 (1.35) | 0.55 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + enlarge_patch/2x | 1.04 | 1.79 F | 54.12 F | 0.67 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | register_frames + use_width_free_ratio | 1.73 | 1.84 F | 54.19 skip | 0.47 (1.35) | 0.62 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + smooth_midline/light | 94.73 F | 16.00 F | 30.76 F | 3.77 (1.35) | 7.94 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 71.41 F | 16.08 F | 58.99 F | 4.50 (1.35) | 11.14 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 71.41 F | 16.08 F | 58.99 F | 4.50 (1.35) | 11.14 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + enlarge_patch/1.5x | 76.21 F | 8.31 F | 56.53 F | 0.49 (1.35) | 9.78 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + enlarge_patch/2x | 75.80 F | 8.36 F | 55.16 F | 0.65 (1.35) | 9.58 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | change_frame_stride/double + use_width_free_ratio | 71.41 F | 16.08 F | 58.99 skip | 4.50 (1.35) | 11.14 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 0.55 | 8.36 F | 30.53 F | 0.41 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 0.55 | 8.36 F | 30.53 F | 0.41 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light + enlarge_patch/1.5x | 0.50 | 8.40 F | 30.50 F | 0.50 (1.35) | 0.33 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light + enlarge_patch/2x | 0.61 | 8.45 F | 30.45 F | 0.67 (1.35) | 0.32 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | smooth_midline/light + use_width_free_ratio | 0.55 | 8.36 F | 30.53 skip | 0.41 (1.35) | 0.35 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.55 | 8.28 F | 53.80 F | 0.49 (1.35) | 0.33 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.54 | 8.33 F | 53.78 F | 0.65 (1.35) | 0.31 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 0.63 | 8.27 F | 53.78 skip | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.55 | 8.28 F | 53.80 F | 0.49 (1.35) | 0.33 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.54 | 8.33 F | 53.78 F | 0.65 (1.35) | 0.31 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 0.63 | 8.27 F | 53.78 skip | 0.40 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | enlarge_patch/1.5x + use_width_free_ratio | 0.55 | 8.28 F | 53.80 skip | 0.49 (1.35) | 0.33 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s42 | enlarge_patch/2x + use_width_free_ratio | 0.54 | 8.33 F | 53.78 skip | 0.65 (1.35) | 0.31 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | none | 0.65 | 21.58 F | 51.62 F | 0.43 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames | 2.65 F | 20.37 F | 51.79 F | 0.53 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double | 195.17 F | 23.37 F | 97.72 F | 7.75 (1.35) | 14.12 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light | 0.83 | 20.21 F | 35.33 F | 0.42 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/crop_to_main_root | 0.65 | 21.58 F | 51.62 F | 0.43 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/mask_second_root | 0.65 | 21.58 F | 51.62 F | 0.43 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | enlarge_patch/1.5x | 0.56 | 21.66 F | 51.78 F | 0.48 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | enlarge_patch/2x | 0.58 | 21.70 F | 51.77 F | 0.62 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | use_width_free_ratio | 0.65 | 21.58 F | 51.62 skip | 0.43 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + change_frame_stride/double | 60.54 F | 20.42 F | 100.02 F | 3.07 (1.35) | 15.59 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | register_frames + smooth_midline/light | 3.01 F | 19.14 F | 35.13 F | 0.60 (1.35) | 0.48 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + crop_or_mask/crop_to_main_root | 2.65 F | 20.37 F | 51.79 F | 0.53 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + crop_or_mask/mask_second_root | 2.65 F | 20.37 F | 51.79 F | 0.53 (1.35) | 0.55 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + enlarge_patch/1.5x | 2.04 F | 20.52 F | 51.86 F | 0.54 (1.35) | 0.49 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + enlarge_patch/2x | 1.74 | 20.56 F | 51.84 F | 0.65 (1.35) | 0.50 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | register_frames + use_width_free_ratio | 2.65 F | 20.37 F | 51.79 skip | 0.53 (1.35) | 0.54 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + smooth_midline/light | 181.24 F | 17.65 F | 40.24 F | 6.43 (1.35) | 8.05 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 195.17 F | 23.37 F | 97.72 F | 7.75 (1.35) | 14.12 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 195.17 F | 23.37 F | 97.72 F | 7.75 (1.35) | 14.12 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + enlarge_patch/1.5x | 81.21 F | 21.72 F | 54.20 F | 0.46 (1.35) | 6.14 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + enlarge_patch/2x | 64.42 F | 21.75 F | 54.15 F | 0.61 (1.35) | 0.37 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | change_frame_stride/double + use_width_free_ratio | 195.17 F | 23.37 F | 97.72 skip | 7.75 (1.35) | 14.12 (1.00) | no | no |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 0.83 | 20.21 F | 35.33 F | 0.42 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 0.83 | 20.21 F | 35.33 F | 0.42 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light + enlarge_patch/1.5x | 0.76 | 20.17 F | 35.39 F | 0.47 (1.35) | 0.34 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light + enlarge_patch/2x | 0.74 | 20.16 F | 35.39 F | 0.62 (1.35) | 0.38 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | smooth_midline/light + use_width_free_ratio | 0.83 | 20.21 F | 35.33 skip | 0.42 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.56 | 21.66 F | 51.78 F | 0.48 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.58 | 21.70 F | 51.77 F | 0.62 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 0.65 | 21.58 F | 51.62 skip | 0.43 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.56 | 21.63 F | 51.81 F | 0.48 (1.35) | 0.37 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.58 | 21.67 F | 51.82 F | 0.62 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 0.65 | 21.58 F | 51.62 skip | 0.43 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | enlarge_patch/1.5x + use_width_free_ratio | 0.56 | 21.66 F | 51.78 skip | 0.48 (1.35) | 0.36 (1.00) | no | yes |
| v3_growth_zone_drift_jitter_s43 | enlarge_patch/2x + use_width_free_ratio | 0.58 | 21.70 F | 51.77 skip | 0.62 (1.35) | 0.39 (1.00) | no | yes |
| v3_growth_zone_low_texture_fast_s40 | none | 332.88 F | 192.68 F | 306.45 F | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames | 335.83 F | 185.22 F | 265.29 F | 63.04 (2.70) | 76.43 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half | 408.07 F | 166.25 F | 357.29 F | 57.74 (2.70) | 71.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light | 340.85 F | 192.57 F | 286.97 F | 72.92 (2.70) | 84.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/crop_to_main_root | 332.88 F | 192.68 F | 306.45 F | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/mask_second_root | 332.88 F | 192.68 F | 306.45 F | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | enlarge_patch/1.5x | 395.35 F | 218.90 F | 223.30 F | 69.09 (2.70) | 76.51 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | enlarge_patch/2x | 361.98 F | 202.96 F | 517.23 F | 64.41 (2.70) | 131.32 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | use_width_free_ratio | 332.88 F | 192.68 F | 306.45 skip | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + change_frame_stride/half | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + change_frame_stride/double | 453.63 F | 199.40 F | 630.54 F | 55.89 (2.70) | 177.83 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + smooth_midline/light | 460.25 F | 190.81 F | 494.34 F | 77.40 (2.70) | 127.92 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + crop_or_mask/crop_to_main_root | 335.81 F | 186.45 F | 265.33 F | 63.05 (2.70) | 76.44 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + crop_or_mask/mask_second_root | 335.81 F | 186.47 F | 262.33 F | 63.05 (2.70) | 77.15 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + enlarge_patch/1.5x | 372.41 F | 200.59 F | 306.01 F | 95.81 (2.70) | 86.19 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + enlarge_patch/2x | 748.39 F | 156.13 F | 386.88 F | 62.82 (2.70) | 90.40 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | register_frames + use_width_free_ratio | 335.83 F | 185.22 F | 265.29 skip | 63.04 (2.70) | 76.43 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + smooth_midline/light | 541.10 F | 182.56 F | 340.42 F | 68.97 (2.70) | 80.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + crop_or_mask/crop_to_main_root | 408.07 F | 166.25 F | 357.29 F | 57.74 (2.70) | 71.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + crop_or_mask/mask_second_root | 408.07 F | 166.25 F | 357.29 F | 57.74 (2.70) | 71.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + enlarge_patch/1.5x | 372.99 F | 111.61 F | 414.65 F | 54.41 (2.70) | 112.57 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + enlarge_patch/2x | 397.97 F | 208.49 F | 464.47 F | 57.22 (2.70) | 104.86 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/half + use_width_free_ratio | 408.07 F | 166.25 F | 357.29 skip | 57.74 (2.70) | 71.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + smooth_midline/light | 510.37 F | 196.00 F | 262.19 F | 63.42 (2.70) | 57.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + enlarge_patch/1.5x | 169.16 F | 195.57 F | 256.12 F | 66.38 (2.70) | 61.88 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + enlarge_patch/2x | 575.37 F | 194.46 F | 511.08 F | 64.49 (2.70) | 102.10 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | change_frame_stride/double + use_width_free_ratio | tracker error on the cluster (twice) | | | | | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 340.85 F | 192.57 F | 286.97 F | 72.92 (2.70) | 84.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 340.85 F | 192.57 F | 286.97 F | 72.92 (2.70) | 84.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light + enlarge_patch/1.5x | 282.94 F | 218.90 F | 250.73 F | 67.73 (2.70) | 73.70 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light + enlarge_patch/2x | 375.26 F | 202.96 F | 565.82 F | 67.86 (2.70) | 132.17 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | smooth_midline/light + use_width_free_ratio | 340.85 F | 192.57 F | 286.97 skip | 72.92 (2.70) | 84.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 395.35 F | 218.90 F | 223.30 F | 69.09 (2.70) | 76.51 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 361.98 F | 202.96 F | 517.23 F | 64.41 (2.70) | 131.32 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 332.88 F | 192.68 F | 306.45 skip | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 395.35 F | 218.90 F | 223.30 F | 69.09 (2.70) | 76.51 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 384.92 F | 202.96 F | 617.05 F | 64.41 (2.70) | 144.09 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 332.88 F | 192.68 F | 306.45 skip | 63.61 (2.70) | 80.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | enlarge_patch/1.5x + use_width_free_ratio | 395.35 F | 218.90 F | 223.30 skip | 69.09 (2.70) | 76.51 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s40 | enlarge_patch/2x + use_width_free_ratio | 361.98 F | 202.96 F | 517.23 skip | 64.41 (2.70) | 131.32 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | none | 486.06 F | 202.90 F | 386.57 F | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames | 438.21 F | 244.94 F | nan skip | 101.46 (2.70) | nan (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half | 337.05 F | 101.63 F | 356.89 F | 48.43 (2.70) | 100.53 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double | 447.58 F | 193.38 F | 489.39 F | 67.84 (2.70) | 99.92 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light | 336.01 F | 220.17 F | 298.23 F | 61.29 (2.70) | 89.55 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/crop_to_main_root | 486.06 F | 202.90 F | 386.57 F | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/mask_second_root | 486.06 F | 202.90 F | 386.57 F | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | enlarge_patch/1.5x | 338.64 F | 214.76 F | 228.79 F | 66.29 (2.70) | 74.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | enlarge_patch/2x | 327.51 F | 189.74 F | 185.44 F | 82.24 (2.70) | 56.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | use_width_free_ratio | 486.06 F | 202.90 F | 386.57 skip | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + change_frame_stride/half | 465.97 F | 246.94 F | 405.90 F | 102.40 (2.70) | 178.23 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + change_frame_stride/double | 402.06 F | 194.26 F | 440.70 F | 54.22 (2.70) | 108.27 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + smooth_midline/light | 451.27 F | 209.72 F | 695.91 F | 76.26 (2.70) | 144.73 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + crop_or_mask/crop_to_main_root | 433.79 F | 239.97 F | nan skip | 110.77 (2.70) | nan (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + crop_or_mask/mask_second_root | 667.68 F | 237.68 F | nan skip | 160.77 (2.70) | nan (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + enlarge_patch/1.5x | 445.48 F | 285.16 F | nan skip | 55.83 (2.70) | nan (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + enlarge_patch/2x | 570.50 F | 220.51 F | 668.59 F | 127.41 (2.70) | 202.20 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | register_frames + use_width_free_ratio | 438.21 F | 244.94 F | nan skip | 101.46 (2.70) | nan (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + smooth_midline/light | 335.88 F | 150.42 F | 394.90 F | 82.69 (2.70) | 94.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + crop_or_mask/crop_to_main_root | 337.05 F | 101.63 F | 356.89 F | 48.43 (2.70) | 100.53 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + crop_or_mask/mask_second_root | 337.05 F | 101.63 F | 356.89 F | 48.43 (2.70) | 100.53 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + enlarge_patch/1.5x | 528.12 F | 133.88 F | 366.85 F | 73.14 (2.70) | 88.39 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + enlarge_patch/2x | 435.20 F | 110.50 F | 243.66 F | 64.66 (2.70) | 75.75 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/half + use_width_free_ratio | 337.05 F | 101.63 F | 356.89 skip | 48.43 (2.70) | 100.53 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + smooth_midline/light | 348.42 F | 193.82 F | 206.06 F | 76.77 (2.70) | 56.44 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 447.58 F | 193.38 F | 489.39 F | 67.84 (2.70) | 99.92 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 447.58 F | 193.38 F | 489.39 F | 67.84 (2.70) | 99.92 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + enlarge_patch/1.5x | 295.53 F | 194.22 F | 324.89 F | 71.52 (2.70) | 98.04 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + enlarge_patch/2x | 373.87 F | 187.34 F | 190.07 F | 66.46 (2.70) | 52.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | change_frame_stride/double + use_width_free_ratio | 447.58 F | 193.38 F | 489.39 skip | 67.84 (2.70) | 99.92 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 336.01 F | 220.17 F | 298.23 F | 61.29 (2.70) | 89.55 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 336.01 F | 220.17 F | 298.23 F | 61.29 (2.70) | 89.55 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light + enlarge_patch/1.5x | 295.36 F | 214.47 F | 236.76 F | 65.67 (2.70) | 78.87 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light + enlarge_patch/2x | 289.17 F | 189.74 F | 248.96 F | 81.64 (2.70) | 77.74 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | smooth_midline/light + use_width_free_ratio | 336.01 F | 220.17 F | 298.23 skip | 61.29 (2.70) | 89.55 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 338.64 F | 214.76 F | 228.79 F | 66.29 (2.70) | 74.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 327.51 F | 189.74 F | 185.44 F | 82.24 (2.70) | 56.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 486.06 F | 202.90 F | 386.57 skip | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 338.64 F | 214.76 F | 228.79 F | 66.29 (2.70) | 74.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 317.46 F | 189.74 F | 150.69 F | 82.24 (2.70) | 49.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 486.06 F | 202.90 F | 386.57 skip | 100.49 (2.70) | 87.38 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | enlarge_patch/1.5x + use_width_free_ratio | 338.64 F | 214.76 F | 228.79 skip | 66.29 (2.70) | 74.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s41 | enlarge_patch/2x + use_width_free_ratio | 327.51 F | 189.74 F | 185.44 skip | 82.24 (2.70) | 56.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | none | 369.98 F | 200.96 F | 343.50 F | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames | 352.97 F | 539.60 F | 321.20 F | 112.62 (2.70) | 101.46 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half | 368.89 F | 187.04 F | 442.22 F | 63.23 (2.70) | 91.73 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double | 287.95 F | 203.84 F | 267.58 F | 68.75 (2.70) | 62.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light | 390.21 F | 186.44 F | 277.61 F | 56.33 (2.70) | 80.20 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/crop_to_main_root | 369.98 F | 200.96 F | 343.50 F | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/mask_second_root | 369.98 F | 200.96 F | 343.50 F | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | enlarge_patch/1.5x | 382.02 F | 206.43 F | 295.79 F | 86.98 (2.70) | 70.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | enlarge_patch/2x | 458.92 F | 195.96 F | 379.52 F | 82.17 (2.70) | 80.14 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | use_width_free_ratio | 369.98 F | 200.96 F | 343.50 skip | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + change_frame_stride/half | 480.20 F | 445.49 F | 604.01 F | 83.50 (2.70) | 145.47 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + change_frame_stride/double | 542.20 F | 207.58 F | 197.74 F | 58.08 (2.70) | 86.64 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + smooth_midline/light | 473.74 F | 444.95 F | 502.74 F | 133.31 (2.70) | 130.45 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + crop_or_mask/crop_to_main_root | 352.97 F | 539.60 F | 321.20 F | 112.62 (2.70) | 97.50 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + crop_or_mask/mask_second_root | 405.51 F | 482.24 F | 402.05 F | 106.43 (2.70) | 131.39 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + enlarge_patch/1.5x | 509.95 F | 556.20 F | 291.34 F | 124.23 (2.70) | 110.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + enlarge_patch/2x | 421.54 F | 494.24 F | 441.06 F | 117.50 (2.70) | 131.51 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | register_frames + use_width_free_ratio | 352.97 F | 539.60 F | 321.20 skip | 112.62 (2.70) | 101.46 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + smooth_midline/light | 415.08 F | 128.33 F | 465.58 F | 55.52 (2.70) | 98.11 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + crop_or_mask/crop_to_main_root | 368.89 F | 187.04 F | 442.22 F | 63.23 (2.70) | 91.73 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + crop_or_mask/mask_second_root | 368.89 F | 187.04 F | 442.22 F | 63.23 (2.70) | 91.73 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + enlarge_patch/1.5x | 457.02 F | 116.86 F | 383.42 F | 136.74 (2.70) | 99.28 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + enlarge_patch/2x | 433.14 F | 49.72 F | 171.31 F | 71.14 (2.70) | 59.34 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/half + use_width_free_ratio | 368.89 F | 187.04 F | 442.22 skip | 63.23 (2.70) | 91.73 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + smooth_midline/light | 397.85 F | 204.61 F | 124.99 F | 66.88 (2.70) | 39.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 287.95 F | 203.84 F | 267.58 F | 68.75 (2.70) | 62.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 287.95 F | 203.84 F | 267.58 F | 68.75 (2.70) | 62.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + enlarge_patch/1.5x | 254.06 F | 208.20 F | 256.60 F | 75.74 (2.70) | 61.52 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + enlarge_patch/2x | 345.37 F | 191.54 F | 227.10 F | 88.88 (2.70) | 63.57 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | change_frame_stride/double + use_width_free_ratio | 287.95 F | 203.84 F | 267.58 skip | 68.75 (2.70) | 62.67 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 390.21 F | 186.44 F | 277.61 F | 56.33 (2.70) | 80.20 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 390.21 F | 186.44 F | 277.61 F | 56.33 (2.70) | 80.20 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light + enlarge_patch/1.5x | 374.72 F | 206.76 F | 305.02 F | 85.57 (2.70) | 69.43 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light + enlarge_patch/2x | 470.25 F | 195.96 F | 432.69 F | 68.82 (2.70) | 86.79 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | smooth_midline/light + use_width_free_ratio | 390.21 F | 186.44 F | 277.61 skip | 56.33 (2.70) | 80.20 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 382.02 F | 206.43 F | 295.79 F | 86.98 (2.70) | 70.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 458.92 F | 195.96 F | 379.52 F | 82.17 (2.70) | 80.14 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 369.98 F | 200.96 F | 343.50 skip | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 382.02 F | 206.43 F | 295.79 F | 86.98 (2.70) | 70.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 454.13 F | 195.96 F | 379.52 F | 82.17 (2.70) | 83.28 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 369.98 F | 200.96 F | 343.50 skip | 95.29 (2.70) | 71.16 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | enlarge_patch/1.5x + use_width_free_ratio | 382.02 F | 206.43 F | 295.79 skip | 86.98 (2.70) | 70.30 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s42 | enlarge_patch/2x + use_width_free_ratio | 458.92 F | 195.96 F | 379.52 skip | 82.17 (2.70) | 80.14 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | none | 440.54 F | 176.95 F | 277.29 F | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames | 333.39 F | 179.41 F | 224.23 F | 88.09 (2.70) | 90.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half | 521.14 F | 172.32 F | 241.64 F | 54.10 (2.70) | 96.33 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double | 314.18 F | 184.89 F | 275.55 F | 67.74 (2.70) | 59.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light | 265.06 F | 192.40 F | 187.38 F | 81.10 (2.70) | 49.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/crop_to_main_root | 440.54 F | 176.95 F | 277.29 F | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/mask_second_root | 440.54 F | 176.95 F | 277.29 F | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | enlarge_patch/1.5x | 323.76 F | 151.23 F | 413.22 F | 75.11 (2.70) | 95.95 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | enlarge_patch/2x | 434.69 F | 184.39 F | 338.61 F | 74.58 (2.70) | 85.11 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | use_width_free_ratio | 440.54 F | 176.95 F | 277.29 skip | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + change_frame_stride/half | 292.56 F | 153.00 F | 288.66 F | 51.17 (2.70) | 94.36 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + change_frame_stride/double | 279.44 F | 183.50 F | 197.77 F | 80.76 (2.70) | 52.48 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + smooth_midline/light | 382.59 F | 174.19 F | 455.08 F | 58.73 (2.70) | 129.61 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + crop_or_mask/crop_to_main_root | 333.39 F | 179.41 F | 224.23 F | 88.09 (2.70) | 90.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + crop_or_mask/mask_second_root | 332.88 F | 179.41 F | 219.39 F | 87.66 (2.70) | 78.86 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + enlarge_patch/1.5x | 338.00 F | 203.59 F | 259.15 F | 56.20 (2.70) | 70.24 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + enlarge_patch/2x | 470.19 F | 164.60 F | 462.84 F | 63.45 (2.70) | 98.23 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | register_frames + use_width_free_ratio | 333.39 F | 179.41 F | 224.23 skip | 88.09 (2.70) | 90.49 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + smooth_midline/light | 236.37 F | 131.60 F | 231.74 F | 54.21 (2.70) | 69.47 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + crop_or_mask/crop_to_main_root | 521.14 F | 172.32 F | 241.64 F | 54.10 (2.70) | 96.33 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + crop_or_mask/mask_second_root | 521.14 F | 172.32 F | 241.64 F | 54.10 (2.70) | 96.33 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + enlarge_patch/1.5x | 355.97 F | 104.02 F | 389.61 F | 61.20 (2.70) | 75.80 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + enlarge_patch/2x | 355.62 F | 90.21 F | 266.57 F | 76.53 (2.70) | 63.58 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/half + use_width_free_ratio | 521.14 F | 172.32 F | 241.64 skip | 54.10 (2.70) | 96.33 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + smooth_midline/light | 248.29 F | 185.72 F | 199.32 F | 71.75 (2.70) | 49.34 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 314.18 F | 184.89 F | 275.55 F | 67.74 (2.70) | 59.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 314.18 F | 184.89 F | 275.55 F | 67.74 (2.70) | 59.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + enlarge_patch/1.5x | 311.70 F | 189.33 F | 183.67 F | 81.36 (2.70) | 57.97 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + enlarge_patch/2x | 332.06 F | 189.05 F | 143.85 F | 70.94 (2.70) | 38.96 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | change_frame_stride/double + use_width_free_ratio | 314.18 F | 184.89 F | 275.55 skip | 67.74 (2.70) | 59.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 265.06 F | 192.40 F | 187.38 F | 81.10 (2.70) | 49.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 265.06 F | 192.40 F | 187.38 F | 81.10 (2.70) | 49.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light + enlarge_patch/1.5x | 359.87 F | 151.18 F | 431.01 F | 74.85 (2.70) | 99.22 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light + enlarge_patch/2x | 326.92 F | 184.40 F | 310.62 F | 74.33 (2.70) | 75.29 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | smooth_midline/light + use_width_free_ratio | 265.06 F | 192.40 F | 187.38 skip | 81.10 (2.70) | 49.59 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 323.76 F | 151.23 F | 413.22 F | 75.11 (2.70) | 95.95 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 434.69 F | 184.39 F | 338.61 F | 74.58 (2.70) | 85.11 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 440.54 F | 176.95 F | 277.29 skip | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 323.76 F | 151.23 F | 413.22 F | 75.11 (2.70) | 95.95 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 434.57 F | 184.39 F | 265.44 F | 74.58 (2.70) | 76.26 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 440.54 F | 176.95 F | 277.29 skip | 80.81 (2.70) | 97.07 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | enlarge_patch/1.5x + use_width_free_ratio | 323.76 F | 151.23 F | 413.22 skip | 75.11 (2.70) | 95.95 (1.00) | no | no |
| v3_growth_zone_low_texture_fast_s43 | enlarge_patch/2x + use_width_free_ratio | 434.69 F | 184.39 F | 338.61 skip | 74.58 (2.70) | 85.11 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | none | 1.39 | 0.72 | 3.22 | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames | 2.68 F | 1.22 F | 3.21 | 1.66 (1.35) | 1.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double | 64.76 F | 0.70 | 106.35 F | 10.86 (1.35) | 16.45 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light | 2.24 F | 0.66 | 2.95 | 1.49 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/crop_to_main_root | 1.39 | 0.72 | 3.22 | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/mask_second_root | 1.39 | 0.72 | 3.22 | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | enlarge_patch/1.5x | 0.76 | 0.38 | 2.45 | 1.08 (1.35) | 0.86 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | enlarge_patch/2x | 0.68 | 0.41 | 2.23 | 0.96 (1.35) | 0.69 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | use_width_free_ratio | 1.39 | 0.72 | 3.22 skip | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + change_frame_stride/double | 77.84 F | 1.10 F | 22.31 F | 10.84 (1.35) | 4.06 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + smooth_midline/light | 3.21 F | 0.88 | 3.13 | 1.54 (1.35) | 1.23 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + crop_or_mask/crop_to_main_root | 2.68 F | 1.22 F | 3.21 | 1.66 (1.35) | 1.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + crop_or_mask/mask_second_root | 2.68 F | 1.22 F | 3.21 | 1.66 (1.35) | 1.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + enlarge_patch/1.5x | 1.68 | 0.83 | 2.62 | 1.14 (1.35) | 0.91 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + enlarge_patch/2x | 1.25 | 0.69 | 2.42 | 1.01 (1.35) | 0.73 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | register_frames + use_width_free_ratio | 2.68 F | 1.22 F | 3.21 skip | 1.66 (1.35) | 1.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + smooth_midline/light | 104.76 F | 0.61 | 3.03 | 8.21 (1.35) | 1.16 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 64.76 F | 0.70 | 106.35 F | 10.86 (1.35) | 16.45 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | 64.76 F | 0.70 | 106.35 F | 10.86 (1.35) | 16.45 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + enlarge_patch/1.5x | 140.79 F | 0.32 | 2.34 | 5.47 (1.35) | 0.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + enlarge_patch/2x | 130.51 F | 0.35 | 2.17 | 0.96 (1.35) | 0.70 (1.00) | no | yes |
| v3_growth_zone_focus_drift_z3_s40 | change_frame_stride/double + use_width_free_ratio | 64.76 F | 0.70 | 106.35 skip | 10.86 (1.35) | 16.45 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 2.24 F | 0.66 | 2.95 | 1.49 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 2.24 F | 0.66 | 2.95 | 1.49 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light + enlarge_patch/1.5x | 1.69 | 0.38 | 2.45 | 1.08 (1.35) | 0.87 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light + enlarge_patch/2x | 1.65 | 0.41 | 2.23 | 0.96 (1.35) | 0.69 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | smooth_midline/light + use_width_free_ratio | 2.24 F | 0.66 | 2.95 skip | 1.49 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.76 | 0.38 | 2.45 | 1.08 (1.35) | 0.86 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.68 | 0.41 | 2.23 | 0.96 (1.35) | 0.69 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 1.39 | 0.72 | 3.22 skip | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.76 | 0.38 | 2.45 | 1.08 (1.35) | 0.86 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.68 | 0.41 | 2.23 | 0.96 (1.35) | 0.69 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 1.39 | 0.72 | 3.22 skip | 1.59 (1.35) | 1.19 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s40 | enlarge_patch/1.5x + use_width_free_ratio | 0.76 | 0.38 | 2.45 skip | 1.08 (1.35) | 0.86 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s40 | enlarge_patch/2x + use_width_free_ratio | 0.68 | 0.41 | 2.23 skip | 0.96 (1.35) | 0.69 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s41 | none | 1.59 | 1.15 F | 6.49 F | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames | 2.33 F | 1.15 F | 7.43 F | 1.75 (1.35) | 1.97 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double | 64.34 F | 1.14 F | 80.48 F | 5.46 (1.35) | 12.81 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light | 2.27 F | 0.91 | 5.40 F | 1.53 (1.35) | 1.64 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/crop_to_main_root | 1.59 | 1.15 F | 6.49 F | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/mask_second_root | 1.59 | 1.15 F | 6.49 F | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | enlarge_patch/1.5x | 0.96 | 0.57 | 3.86 F | 1.18 (1.35) | 1.16 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | enlarge_patch/2x | 0.73 | 0.43 | 4.23 F | 0.99 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | use_width_free_ratio | 1.59 | 1.15 F | 6.49 skip | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + change_frame_stride/double | 1.79 | 1.17 F | 78.36 F | 5.39 (1.35) | 12.45 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + smooth_midline/light | 3.98 F | 0.95 | 6.17 F | 1.62 (1.35) | 1.81 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + crop_or_mask/crop_to_main_root | 2.33 F | 1.15 F | 7.43 F | 1.75 (1.35) | 1.97 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + crop_or_mask/mask_second_root | 2.33 F | 1.15 F | 7.43 F | 1.75 (1.35) | 1.97 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + enlarge_patch/1.5x | 1.85 | 0.52 | 4.37 F | 1.24 (1.35) | 1.28 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + enlarge_patch/2x | 1.69 | 0.31 | 4.68 F | 1.03 (1.35) | 1.25 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | register_frames + use_width_free_ratio | 2.33 F | 1.15 F | 7.43 skip | 1.75 (1.35) | 1.97 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + smooth_midline/light | 69.84 F | 0.90 | 77.61 F | 4.18 (1.35) | 11.92 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 64.34 F | 1.14 F | 80.48 F | 5.46 (1.35) | 12.81 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 64.34 F | 1.14 F | 80.48 F | 5.46 (1.35) | 12.81 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + enlarge_patch/1.5x | 103.83 F | 0.56 | 3.81 F | 1.16 (1.35) | 1.15 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + enlarge_patch/2x | 138.03 F | 0.40 | 4.19 F | 0.98 (1.35) | 1.12 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | change_frame_stride/double + use_width_free_ratio | 64.34 F | 1.14 F | 80.48 skip | 5.46 (1.35) | 12.81 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 2.27 F | 0.91 | 5.40 F | 1.53 (1.35) | 1.64 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 2.27 F | 0.91 | 5.40 F | 1.53 (1.35) | 1.64 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light + enlarge_patch/1.5x | 1.90 | 0.57 | 3.86 F | 1.18 (1.35) | 1.16 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light + enlarge_patch/2x | 1.49 | 0.43 | 4.23 F | 0.99 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | smooth_midline/light + use_width_free_ratio | 2.27 F | 0.91 | 5.40 skip | 1.53 (1.35) | 1.64 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.96 | 0.57 | 3.86 F | 1.18 (1.35) | 1.16 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.73 | 0.43 | 4.23 F | 0.99 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 1.59 | 1.15 F | 6.49 skip | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.96 | 0.57 | 3.86 F | 1.18 (1.35) | 1.16 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.73 | 0.43 | 4.23 F | 0.99 (1.35) | 1.13 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 1.59 | 1.15 F | 6.49 skip | 1.67 (1.35) | 1.82 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s41 | enlarge_patch/1.5x + use_width_free_ratio | 0.96 | 0.57 | 3.86 skip | 1.18 (1.35) | 1.16 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s41 | enlarge_patch/2x + use_width_free_ratio | 0.73 | 0.43 | 4.23 skip | 0.99 (1.35) | 1.13 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s42 | none | 1.84 | 0.56 | 9.14 F | 1.89 (1.35) | 2.38 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames | 2.10 F | 0.31 | 9.57 F | 2.02 (1.35) | 2.54 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double | 54.86 F | 0.57 | 44.77 F | 1.83 (1.35) | 9.62 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light | 1.90 | 0.53 | 8.67 F | 1.67 (1.35) | 2.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/crop_to_main_root | 1.84 | 0.56 | 9.14 F | 1.89 (1.35) | 2.38 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/mask_second_root | 1.84 | 0.56 | 9.14 F | 1.89 (1.35) | 2.38 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | enlarge_patch/1.5x | 1.17 | 0.27 | 7.81 F | 1.12 (1.35) | 1.94 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | enlarge_patch/2x | 0.96 | 0.19 | 6.16 F | 0.96 (1.35) | 1.59 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | use_width_free_ratio | 1.84 | 0.56 | 9.14 skip | 1.89 (1.35) | 2.38 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + change_frame_stride/double | 1.22 | 0.74 | 45.72 F | 1.89 (1.35) | 9.72 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + smooth_midline/light | 2.90 F | 0.80 | 9.10 F | 1.84 (1.35) | 2.46 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + crop_or_mask/crop_to_main_root | 2.10 F | 0.31 | 9.57 F | 2.02 (1.35) | 2.54 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + crop_or_mask/mask_second_root | 2.10 F | 0.31 | 9.57 F | 2.02 (1.35) | 2.54 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + enlarge_patch/1.5x | 1.47 | 0.24 | 8.04 F | 1.24 (1.35) | 2.04 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + enlarge_patch/2x | 1.16 | 0.37 | 6.35 F | 1.05 (1.35) | 1.69 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | register_frames + use_width_free_ratio | 2.10 F | 0.31 | 9.57 skip | 2.02 (1.35) | 2.54 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + smooth_midline/light | 51.56 F | 0.55 | 76.87 F | 1.64 (1.35) | 11.78 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 54.86 F | 0.57 | 44.77 F | 1.83 (1.35) | 9.62 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 54.86 F | 0.57 | 44.77 F | 1.83 (1.35) | 9.62 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + enlarge_patch/1.5x | 43.26 F | 0.29 | 69.10 F | 1.10 (1.35) | 10.62 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + enlarge_patch/2x | 0.84 | 0.20 | 65.24 F | 0.96 (1.35) | 10.04 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | change_frame_stride/double + use_width_free_ratio | 54.86 F | 0.57 | 44.77 skip | 1.83 (1.35) | 9.62 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 1.90 | 0.53 | 8.67 F | 1.67 (1.35) | 2.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 1.90 | 0.53 | 8.67 F | 1.67 (1.35) | 2.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light + enlarge_patch/1.5x | 1.39 | 0.27 | 7.81 F | 1.12 (1.35) | 1.94 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light + enlarge_patch/2x | 1.13 | 0.19 | 6.16 F | 0.96 (1.35) | 1.59 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | smooth_midline/light + use_width_free_ratio | 1.90 | 0.53 | 8.67 skip | 1.67 (1.35) | 2.30 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 1.17 | 0.27 | 7.81 F | 1.12 (1.35) | 1.94 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.96 | 0.19 | 6.16 F | 0.96 (1.35) | 1.59 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 1.84 | 0.56 | 9.14 skip | 1.89 (1.35) | 2.38 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 1.17 | 0.27 | 7.81 F | 1.12 (1.35) | 1.94 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.96 | 0.19 | 6.16 F | 0.96 (1.35) | 1.59 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 1.84 | 0.56 | 9.14 skip | 1.89 (1.35) | 2.38 (1.00) | yes | no |
| v3_growth_zone_focus_drift_z3_s42 | enlarge_patch/1.5x + use_width_free_ratio | 1.17 | 0.27 | 7.81 skip | 1.12 (1.35) | 1.94 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s42 | enlarge_patch/2x + use_width_free_ratio | 0.96 | 0.19 | 6.16 skip | 0.96 (1.35) | 1.59 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | none | 1.32 | 0.46 | 8.55 F | 1.27 (1.35) | 2.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames | 1.73 | 0.31 | 9.25 F | 1.35 (1.35) | 2.40 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double | 117.37 F | 0.45 | 51.09 F | 1.30 (1.35) | 8.21 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light | 1.53 | 0.36 | 8.16 F | 1.17 (1.35) | 2.19 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/crop_to_main_root | 1.32 | 0.46 | 8.55 F | 1.27 (1.35) | 2.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/mask_second_root | 1.32 | 0.46 | 8.55 F | 1.27 (1.35) | 2.27 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | enlarge_patch/1.5x | 0.75 | 0.38 | 4.94 F | 0.91 (1.35) | 1.53 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | enlarge_patch/2x | 0.61 | 0.52 | 5.17 F | 0.83 (1.35) | 1.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | use_width_free_ratio | 1.32 | 0.46 | 8.55 skip | 1.27 (1.35) | 2.27 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + change_frame_stride/double | 1.50 | 0.28 | 50.72 F | 1.32 (1.35) | 8.17 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + smooth_midline/light | 2.59 F | 0.39 | 8.50 F | 1.27 (1.35) | 2.28 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + crop_or_mask/crop_to_main_root | 1.73 | 0.31 | 9.25 F | 1.35 (1.35) | 2.40 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + crop_or_mask/mask_second_root | 1.73 | 0.31 | 9.25 F | 1.35 (1.35) | 2.40 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + enlarge_patch/1.5x | 1.15 | 0.25 | 5.37 F | 0.95 (1.35) | 1.60 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + enlarge_patch/2x | 1.15 | 0.45 | 5.45 F | 0.86 (1.35) | 1.39 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | register_frames + use_width_free_ratio | 1.73 | 0.31 | 9.25 skip | 1.35 (1.35) | 2.40 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + smooth_midline/light | 118.85 F | 0.35 | 50.75 F | 1.21 (1.35) | 8.14 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 117.37 F | 0.45 | 51.09 F | 1.30 (1.35) | 8.21 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 117.37 F | 0.45 | 51.09 F | 1.30 (1.35) | 8.21 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + enlarge_patch/1.5x | 75.41 F | 0.37 | 28.65 F | 0.95 (1.35) | 5.15 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + enlarge_patch/2x | 72.31 F | 0.51 | 28.09 F | 0.87 (1.35) | 5.00 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | change_frame_stride/double + use_width_free_ratio | 117.37 F | 0.45 | 51.09 skip | 1.30 (1.35) | 8.21 (1.00) | no | yes |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 1.53 | 0.36 | 8.16 F | 1.17 (1.35) | 2.19 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 1.53 | 0.36 | 8.16 F | 1.17 (1.35) | 2.19 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light + enlarge_patch/1.5x | 1.32 | 0.38 | 4.94 F | 0.91 (1.35) | 1.52 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light + enlarge_patch/2x | 1.02 | 0.52 | 5.17 F | 0.83 (1.35) | 1.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | smooth_midline/light + use_width_free_ratio | 1.53 | 0.36 | 8.16 skip | 1.17 (1.35) | 2.19 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 0.75 | 0.38 | 4.94 F | 0.91 (1.35) | 1.53 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 0.61 | 0.52 | 5.17 F | 0.83 (1.35) | 1.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 1.32 | 0.46 | 8.55 skip | 1.27 (1.35) | 2.27 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 0.75 | 0.38 | 4.94 F | 0.91 (1.35) | 1.53 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 0.61 | 0.52 | 5.17 F | 0.83 (1.35) | 1.30 (1.00) | no | no |
| v3_growth_zone_focus_drift_z3_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 1.32 | 0.46 | 8.55 skip | 1.27 (1.35) | 2.27 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | enlarge_patch/1.5x + use_width_free_ratio | 0.75 | 0.38 | 4.94 skip | 0.91 (1.35) | 1.53 (1.00) | yes | yes |
| v3_growth_zone_focus_drift_z3_s43 | enlarge_patch/2x + use_width_free_ratio | 0.61 | 0.52 | 5.17 skip | 0.83 (1.35) | 1.30 (1.00) | yes | yes |
| v3_growth_zone_illumination_flicker_z0.1_s40 | none | 66.69 F | 1.91 F | 51.40 F | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames | 71.82 F | 1.90 F | 51.84 F | 11.11 (1.35) | 15.84 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double | 119.16 F | 1.50 F | 89.51 F | 11.80 (1.35) | 26.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light | 27.78 F | 2.08 F | 39.44 F | 7.01 (1.35) | 10.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/crop_to_main_root | 66.69 F | 1.91 F | 51.40 F | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/mask_second_root | 66.69 F | 1.91 F | 51.40 F | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | enlarge_patch/1.5x | 2.74 F | 1.26 F | 11.04 F | 2.90 (1.35) | 3.76 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | enlarge_patch/2x | 2.75 F | 1.42 F | 7.61 F | 2.36 (1.35) | 3.06 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | use_width_free_ratio | 66.69 F | 1.91 F | 51.40 skip | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + change_frame_stride/double | 38.66 F | 1.51 F | 90.59 F | 15.22 (1.35) | 25.82 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + smooth_midline/light | 26.03 F | 2.07 F | 39.59 F | 7.34 (1.35) | 10.68 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + crop_or_mask/crop_to_main_root | 71.82 F | 1.90 F | 51.84 F | 11.11 (1.35) | 15.84 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + crop_or_mask/mask_second_root | 71.82 F | 1.90 F | 51.84 F | 11.11 (1.35) | 15.84 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + enlarge_patch/1.5x | 3.56 F | 1.26 F | 10.85 F | 2.88 (1.35) | 3.83 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + enlarge_patch/2x | 2.23 F | 1.36 F | 8.20 F | 2.38 (1.35) | 3.09 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | register_frames + use_width_free_ratio | 71.82 F | 1.90 F | 51.84 skip | 11.11 (1.35) | 15.84 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + smooth_midline/light | 113.71 F | 1.55 F | 64.70 F | 12.86 (1.35) | 15.53 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 119.16 F | 1.50 F | 89.51 F | 11.80 (1.35) | 26.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + crop_or_mask/mask_second_root | 119.16 F | 1.50 F | 89.51 F | 11.80 (1.35) | 26.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + enlarge_patch/1.5x | 130.64 F | 0.77 | 30.39 F | 3.44 (1.35) | 6.97 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + enlarge_patch/2x | 42.50 F | 0.89 | 22.22 F | 2.26 (1.35) | 5.58 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | change_frame_stride/double + use_width_free_ratio | 119.16 F | 1.50 F | 89.51 skip | 11.80 (1.35) | 26.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light + crop_or_mask/crop_to_main_root | 27.78 F | 2.08 F | 39.44 F | 7.01 (1.35) | 10.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light + crop_or_mask/mask_second_root | 27.78 F | 2.08 F | 39.44 F | 7.01 (1.35) | 10.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light + enlarge_patch/1.5x | 12.01 F | 1.26 F | 11.08 F | 2.90 (1.35) | 3.82 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light + enlarge_patch/2x | 8.73 F | 1.42 F | 7.62 F | 2.36 (1.35) | 3.18 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | smooth_midline/light + use_width_free_ratio | 27.78 F | 2.08 F | 39.44 skip | 7.01 (1.35) | 10.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 2.74 F | 1.26 F | 11.04 F | 2.90 (1.35) | 3.76 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.75 F | 1.42 F | 7.61 F | 2.36 (1.35) | 3.06 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 66.69 F | 1.91 F | 51.40 skip | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 2.74 F | 1.26 F | 11.04 F | 2.90 (1.35) | 3.76 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.75 F | 1.42 F | 7.61 F | 2.36 (1.35) | 3.06 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | crop_or_mask/mask_second_root + use_width_free_ratio | 66.69 F | 1.91 F | 51.40 skip | 9.90 (1.35) | 17.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | enlarge_patch/1.5x + use_width_free_ratio | 2.74 F | 1.26 F | 11.04 skip | 2.90 (1.35) | 3.76 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s40 | enlarge_patch/2x + use_width_free_ratio | 2.75 F | 1.42 F | 7.61 skip | 2.36 (1.35) | 3.06 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | none | 8.70 F | 1.87 F | 17.52 F | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames | 31.43 F | 1.72 F | 17.41 F | 7.73 (1.35) | 5.60 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double | 102.48 F | 1.42 F | 97.00 F | 9.44 (1.35) | 18.30 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light | 21.02 F | 1.59 F | 13.62 F | 5.17 (1.35) | 5.26 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/crop_to_main_root | 8.70 F | 1.87 F | 17.52 F | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/mask_second_root | 8.70 F | 1.87 F | 17.52 F | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | enlarge_patch/1.5x | 2.52 F | 1.51 F | 8.96 F | 2.84 (1.35) | 3.38 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | enlarge_patch/2x | 2.30 F | 1.19 F | 8.54 F | 2.32 (1.35) | 3.12 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | use_width_free_ratio | 8.70 F | 1.87 F | 17.52 skip | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + change_frame_stride/double | 39.49 F | 1.37 F | 97.16 F | 9.31 (1.35) | 18.23 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + smooth_midline/light | 35.78 F | 1.55 F | 24.85 F | 5.16 (1.35) | 7.31 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + crop_or_mask/crop_to_main_root | 31.43 F | 1.72 F | 17.41 F | 7.73 (1.35) | 5.60 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + crop_or_mask/mask_second_root | 31.43 F | 1.72 F | 17.41 F | 7.73 (1.35) | 5.60 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + enlarge_patch/1.5x | 9.23 F | 1.53 F | 9.00 F | 2.78 (1.35) | 3.42 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + enlarge_patch/2x | 8.12 F | 1.19 F | 8.50 F | 2.33 (1.35) | 3.09 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | register_frames + use_width_free_ratio | 31.43 F | 1.72 F | 17.41 skip | 7.73 (1.35) | 5.60 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + smooth_midline/light | 60.19 F | 1.35 F | 84.82 F | 8.20 (1.35) | 15.88 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 102.48 F | 1.42 F | 97.00 F | 9.44 (1.35) | 18.30 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + crop_or_mask/mask_second_root | 102.48 F | 1.42 F | 97.00 F | 9.44 (1.35) | 18.30 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + enlarge_patch/1.5x | 118.46 F | 1.20 F | 8.18 F | 4.04 (1.35) | 3.20 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + enlarge_patch/2x | 132.93 F | 1.07 F | 7.48 F | 2.26 (1.35) | 2.74 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | change_frame_stride/double + use_width_free_ratio | 102.48 F | 1.42 F | 97.00 skip | 9.44 (1.35) | 18.30 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light + crop_or_mask/crop_to_main_root | 21.02 F | 1.59 F | 13.62 F | 5.17 (1.35) | 5.26 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light + crop_or_mask/mask_second_root | 21.02 F | 1.59 F | 13.62 F | 5.17 (1.35) | 5.26 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light + enlarge_patch/1.5x | 8.18 F | 1.51 F | 8.96 F | 2.84 (1.35) | 3.37 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light + enlarge_patch/2x | 5.92 F | 1.19 F | 8.54 F | 2.32 (1.35) | 3.10 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | smooth_midline/light + use_width_free_ratio | 21.02 F | 1.59 F | 13.62 skip | 5.17 (1.35) | 5.26 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 2.52 F | 1.51 F | 8.96 F | 2.84 (1.35) | 3.38 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.30 F | 1.19 F | 8.54 F | 2.32 (1.35) | 3.12 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 8.70 F | 1.87 F | 17.52 skip | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 2.52 F | 1.51 F | 8.96 F | 2.84 (1.35) | 3.38 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.30 F | 1.19 F | 8.54 F | 2.32 (1.35) | 3.12 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | crop_or_mask/mask_second_root + use_width_free_ratio | 8.70 F | 1.87 F | 17.52 skip | 7.55 (1.35) | 5.43 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | enlarge_patch/1.5x + use_width_free_ratio | 2.52 F | 1.51 F | 8.96 skip | 2.84 (1.35) | 3.38 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s41 | enlarge_patch/2x + use_width_free_ratio | 2.30 F | 1.19 F | 8.54 skip | 2.32 (1.35) | 3.12 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | none | 29.19 F | 0.84 | 44.61 F | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames | 38.24 F | 0.85 | 44.72 F | 6.91 (1.35) | 14.71 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double | 100.22 F | 0.33 | 60.19 F | 9.55 (1.35) | 13.42 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light | 47.56 F | 0.62 | 32.82 F | 5.89 (1.35) | 12.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/crop_to_main_root | 29.19 F | 0.84 | 44.61 F | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/mask_second_root | 29.19 F | 0.84 | 44.61 F | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | enlarge_patch/1.5x | 6.44 F | 0.47 | 20.26 F | 3.74 (1.35) | 5.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | enlarge_patch/2x | 2.48 F | 0.64 | 17.50 F | 1.64 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | use_width_free_ratio | 29.19 F | 0.84 | 44.61 skip | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + change_frame_stride/double | 24.19 F | 0.29 | 60.44 F | 9.55 (1.35) | 13.46 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + smooth_midline/light | 108.13 F | 0.60 | 32.37 F | 5.89 (1.35) | 12.02 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + crop_or_mask/crop_to_main_root | 38.24 F | 0.85 | 44.72 F | 6.91 (1.35) | 14.71 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + crop_or_mask/mask_second_root | 38.24 F | 0.85 | 44.72 F | 6.91 (1.35) | 14.71 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + enlarge_patch/1.5x | 9.37 F | 0.44 | 20.70 F | 3.73 (1.35) | 5.97 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + enlarge_patch/2x | 2.00 F | 0.57 | 17.43 F | 1.65 (1.35) | 5.17 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | register_frames + use_width_free_ratio | 38.24 F | 0.85 | 44.72 skip | 6.91 (1.35) | 14.71 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + smooth_midline/light | 98.48 F | 0.44 | 74.03 F | 6.93 (1.35) | 12.51 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 100.22 F | 0.33 | 60.19 F | 9.55 (1.35) | 13.42 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + crop_or_mask/mask_second_root | 100.22 F | 0.33 | 60.19 F | 9.55 (1.35) | 13.42 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + enlarge_patch/1.5x | 74.22 F | 0.37 | 55.00 F | 1.91 (1.35) | 9.28 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + enlarge_patch/2x | 51.77 F | 0.47 | 9.57 F | 1.55 (1.35) | 3.09 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | change_frame_stride/double + use_width_free_ratio | 100.22 F | 0.33 | 60.19 skip | 9.55 (1.35) | 13.42 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light + crop_or_mask/crop_to_main_root | 47.56 F | 0.62 | 32.82 F | 5.89 (1.35) | 12.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light + crop_or_mask/mask_second_root | 47.56 F | 0.62 | 32.82 F | 5.89 (1.35) | 12.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light + enlarge_patch/1.5x | 12.59 F | 0.47 | 20.26 F | 3.74 (1.35) | 5.94 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light + enlarge_patch/2x | 7.60 F | 0.64 | 17.50 F | 1.64 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | smooth_midline/light + use_width_free_ratio | 47.56 F | 0.62 | 32.82 skip | 5.89 (1.35) | 12.08 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 6.44 F | 0.47 | 20.26 F | 3.74 (1.35) | 5.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.48 F | 0.64 | 17.50 F | 1.64 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 29.19 F | 0.84 | 44.61 skip | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 6.44 F | 0.47 | 20.26 F | 3.74 (1.35) | 5.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.48 F | 0.64 | 17.50 F | 1.64 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | crop_or_mask/mask_second_root + use_width_free_ratio | 29.19 F | 0.84 | 44.61 skip | 6.95 (1.35) | 14.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | enlarge_patch/1.5x + use_width_free_ratio | 6.44 F | 0.47 | 20.26 skip | 3.74 (1.35) | 5.89 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s42 | enlarge_patch/2x + use_width_free_ratio | 2.48 F | 0.64 | 17.50 skip | 1.64 (1.35) | 5.16 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | none | 55.43 F | 2.33 F | 28.02 F | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames | 56.09 F | 2.34 F | 27.52 F | 7.03 (1.35) | 10.93 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double | 114.67 F | 0.97 | 54.40 F | 2.37 (1.35) | 12.37 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light | 90.41 F | 1.43 F | 93.07 F | 5.11 (1.35) | 15.59 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/crop_to_main_root | 55.43 F | 2.33 F | 28.02 F | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/mask_second_root | 55.43 F | 2.33 F | 28.02 F | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | enlarge_patch/1.5x | 3.15 F | 1.22 F | 9.42 F | 2.42 (1.35) | 3.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | enlarge_patch/2x | 2.15 F | 1.15 F | 7.21 F | 2.00 (1.35) | 2.75 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | use_width_free_ratio | 55.43 F | 2.33 F | 28.02 skip | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + change_frame_stride/double | 2.74 F | 1.09 F | 54.23 F | 2.38 (1.35) | 12.40 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + smooth_midline/light | 86.76 F | 1.52 F | 44.75 F | 5.07 (1.35) | 9.44 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + crop_or_mask/crop_to_main_root | 56.09 F | 2.34 F | 27.52 F | 7.03 (1.35) | 10.94 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + crop_or_mask/mask_second_root | 56.09 F | 2.34 F | 27.52 F | 7.03 (1.35) | 10.94 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + enlarge_patch/1.5x | 24.67 F | 1.25 F | 9.81 F | 2.40 (1.35) | 3.90 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + enlarge_patch/2x | 37.35 F | 1.07 F | 7.43 F | 2.00 (1.35) | 2.75 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | register_frames + use_width_free_ratio | 56.09 F | 2.34 F | 27.52 skip | 7.03 (1.35) | 10.93 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + smooth_midline/light | 103.36 F | 0.79 | 60.81 F | 2.16 (1.35) | 12.50 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + crop_or_mask/crop_to_main_root | 114.67 F | 0.97 | 54.40 F | 2.37 (1.35) | 12.37 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + crop_or_mask/mask_second_root | 114.67 F | 0.97 | 54.40 F | 2.37 (1.35) | 12.37 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + enlarge_patch/1.5x | 70.53 F | 0.49 | 35.60 F | 1.55 (1.35) | 6.30 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + enlarge_patch/2x | 70.16 F | 0.54 | 34.42 F | 1.44 (1.35) | 6.01 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | change_frame_stride/double + use_width_free_ratio | 114.67 F | 0.97 | 54.40 skip | 2.37 (1.35) | 12.37 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light + crop_or_mask/crop_to_main_root | 90.41 F | 1.43 F | 93.07 F | 5.11 (1.35) | 15.54 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light + crop_or_mask/mask_second_root | 90.42 F | 1.43 F | 93.08 F | 5.11 (1.35) | 15.59 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light + enlarge_patch/1.5x | 8.58 F | 1.22 F | 9.42 F | 2.42 (1.35) | 3.86 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light + enlarge_patch/2x | 7.68 F | 1.15 F | 7.21 F | 2.00 (1.35) | 2.78 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | smooth_midline/light + use_width_free_ratio | 90.41 F | 1.43 F | 93.07 skip | 5.11 (1.35) | 15.59 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/1.5x | 3.15 F | 1.22 F | 9.42 F | 2.42 (1.35) | 3.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/crop_to_main_root + enlarge_patch/2x | 2.15 F | 1.15 F | 7.21 F | 2.00 (1.35) | 2.75 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/crop_to_main_root + use_width_free_ratio | 55.43 F | 2.33 F | 28.02 skip | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/mask_second_root + enlarge_patch/1.5x | 3.15 F | 1.22 F | 9.42 F | 2.42 (1.35) | 3.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/mask_second_root + enlarge_patch/2x | 2.15 F | 1.15 F | 7.21 F | 2.00 (1.35) | 2.75 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | crop_or_mask/mask_second_root + use_width_free_ratio | 55.43 F | 2.33 F | 28.02 skip | 6.76 (1.35) | 11.36 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | enlarge_patch/1.5x + use_width_free_ratio | 3.15 F | 1.22 F | 9.42 skip | 2.42 (1.35) | 3.85 (1.00) | no | no |
| v3_growth_zone_illumination_flicker_z0.1_s43 | enlarge_patch/2x + use_width_free_ratio | 2.15 F | 1.15 F | 7.21 skip | 2.00 (1.35) | 2.75 (1.00) | no | no |
