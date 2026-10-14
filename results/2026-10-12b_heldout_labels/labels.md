# Held-out faults: labels, seeds 0-2, approved sizes (tracker only, no agent)

Spec 2026-10-12b item 3. Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and the fitting remedy gives three passes and a good measurement on at least 2 of 3 seeds; a rod is repairable if a state of at most two steps gives three passes and a good measurement. Good: approved tolerance (REGR limit in brackets, 2.5 % of the true peak; flank 1.00 %/h). Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. States: the fitting remedies of `docs/proposals/2026-10-12_heldout-faults.md`, open item 3. Unremedied runs from the held-out size sweep (`staging/tracks_heldout`).

Expected outcome (proposal section 2) against the labels. Where they differ the label wins (spec 2026-10-12b):

| Fault | Size | Expected outcome (proposal) | Labels, seeds 0-2 | Correct outcome by label | Differs |
| :-- | :-- | :-- | :-- | :-- | :-- |
| second_root | 30 | decline | 3 not repairable | decline (not repairable) |  |
| fast_rotation | 2 | accept after register_frames | 3 not repairable | decline (not repairable) | yes |
| bad_stage_correction | 3 | accept after register_frames | 3 repairable | accept (repairable) |  |
| flank_swap | 0.5 | decline | 3 not repairable | decline (not repairable) |  |
| partial_occlusion | 20 | decline | 3 not repairable | decline (not repairable) |  |

Faults whose labels differ from the expected outcome: fast_rotation.

| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | Remedied: three passes and good | Meets criteria |
| :-- | :-- | :-- | :-- | :-- | :-- |
| second_root | 30 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| fast_rotation | 2 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| bad_stage_correction | 3 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| flank_swap | 0.5 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| partial_occlusion | 20 | 3 of 3 | 1 of 3 | 0 of 3 | no |

Labels (from these states only):

| Rod | Label | Repairing remedy |
| :-- | :-- | :-- |
| growth_zone_second_root_z30_s0 | not repairable | - |
| growth_zone_second_root_z30_s1 | not repairable | - |
| growth_zone_second_root_z30_s2 | not repairable | - |
| growth_zone_fast_rotation_z2_s0 | not repairable | - |
| growth_zone_fast_rotation_z2_s1 | not repairable | - |
| growth_zone_fast_rotation_z2_s2 | not repairable | - |
| growth_zone_bad_stage_correction_z3_s0 | repairable | register_frames |
| growth_zone_bad_stage_correction_z3_s1 | repairable | register_frames |
| growth_zone_bad_stage_correction_z3_s2 | repairable | register_frames |
| growth_zone_flank_swap_z0.5_s0 | not repairable | - |
| growth_zone_flank_swap_z0.5_s1 | not repairable | - |
| growth_zone_flank_swap_z0.5_s2 | not repairable | - |
| growth_zone_partial_occlusion_z20_s0 | not repairable | - |
| growth_zone_partial_occlusion_z20_s1 | not repairable | - |
| growth_zone_partial_occlusion_z20_s2 | not repairable | - |

Per run (F = fails the approved threshold):

| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| growth_zone_second_root_z30_s0 | none | 0.70 | 0.10 | 10.97 F | 0.48 (1.08) | 3.38 | no | no |
| growth_zone_second_root_z30_s0 | crop_or_mask/crop_to_main_root | 0.70 | 0.10 | 10.97 F | 0.48 (1.08) | 3.38 | no | no |
| growth_zone_second_root_z30_s0 | crop_or_mask/mask_second_root | 0.70 | 0.10 | 10.97 F | 0.48 (1.08) | 3.38 | no | no |
| growth_zone_second_root_z30_s1 | none | 0.58 | 0.08 | 9.03 F | 0.72 (1.08) | 2.59 | no | no |
| growth_zone_second_root_z30_s1 | crop_or_mask/crop_to_main_root | 0.58 | 0.08 | 9.03 F | 0.72 (1.08) | 2.59 | no | no |
| growth_zone_second_root_z30_s1 | crop_or_mask/mask_second_root | 0.58 | 0.08 | 9.03 F | 0.72 (1.08) | 2.59 | no | no |
| growth_zone_second_root_z30_s2 | none | 0.70 | 0.09 | 11.33 F | 0.83 (1.08) | 3.00 | no | no |
| growth_zone_second_root_z30_s2 | crop_or_mask/crop_to_main_root | 0.70 | 0.09 | 11.33 F | 0.83 (1.08) | 3.00 | no | no |
| growth_zone_second_root_z30_s2 | crop_or_mask/mask_second_root | 0.70 | 0.09 | 11.33 F | 0.83 (1.08) | 3.00 | no | no |
| growth_zone_fast_rotation_z2_s0 | none | 58.59 F | 4.76 F | 91.84 F | 11.35 (1.08) | 16.21 | no | no |
| growth_zone_fast_rotation_z2_s0 | register_frames | 705.98 F | 393.86 F | 322.02 F | 148.80 (1.08) | 151.63 | no | no |
| growth_zone_fast_rotation_z2_s1 | none | 72.56 F | 29.63 F | 58.20 F | 13.26 (1.08) | 16.68 | no | no |
| growth_zone_fast_rotation_z2_s1 | register_frames | 123.96 F | 29.71 F | 55.10 F | 13.15 (1.08) | 15.83 | no | no |
| growth_zone_fast_rotation_z2_s2 | none | 124.79 F | 17.95 F | 31.70 F | 23.16 (1.08) | 9.28 | no | no |
| growth_zone_fast_rotation_z2_s2 | register_frames | 131.04 F | 18.12 F | 38.04 F | 10.55 (1.08) | 10.47 | no | no |
| growth_zone_bad_stage_correction_z3_s0 | none | 0.70 | 2.93 F | 1.38 | 0.41 (1.08) | 0.29 | no | yes |
| growth_zone_bad_stage_correction_z3_s0 | register_frames | 1.87 | 0.10 | 1.68 | 0.41 (1.08) | 0.34 | yes | yes |
| growth_zone_bad_stage_correction_z3_s1 | none | 0.58 | 2.92 F | 0.57 | 0.44 (1.08) | 0.18 | no | yes |
| growth_zone_bad_stage_correction_z3_s1 | register_frames | 1.27 | 0.09 | 0.48 | 0.45 (1.08) | 0.18 | yes | yes |
| growth_zone_bad_stage_correction_z3_s2 | none | 0.70 | 2.93 F | 0.37 | 0.44 (1.08) | 0.15 | no | yes |
| growth_zone_bad_stage_correction_z3_s2 | register_frames | 0.93 | 0.11 | 0.43 | 0.44 (1.08) | 0.17 | yes | yes |
| growth_zone_flank_swap_z0.5_s0 | none | 39.85 F | 1.42 F | 84.90 F | 6.63 (1.08) | 26.48 | no | no |
| growth_zone_flank_swap_z0.5_s0 | enlarge_patch/1.5x | 21.36 F | 1.14 F | 62.68 F | 6.65 (1.08) | 23.90 | no | no |
| growth_zone_flank_swap_z0.5_s0 | enlarge_patch/2x | 17.78 F | 1.05 F | 65.35 F | 6.29 (1.08) | 26.40 | no | no |
| growth_zone_flank_swap_z0.5_s0 | change_frame_stride/double | 16.92 F | 1.43 F | 77.02 F | 6.76 (1.08) | 25.63 | no | no |
| growth_zone_flank_swap_z0.5_s0 | change_frame_stride/double + enlarge_patch/1.5x | 25.58 F | 1.18 F | 60.79 F | 6.76 (1.08) | 25.10 | no | no |
| growth_zone_flank_swap_z0.5_s0 | change_frame_stride/double + enlarge_patch/2x | 18.47 F | 1.06 F | 67.36 F | 6.42 (1.08) | 26.55 | no | no |
| growth_zone_flank_swap_z0.5_s1 | none | 43.06 F | 2.12 F | 82.97 F | 6.49 (1.08) | 36.47 | no | no |
| growth_zone_flank_swap_z0.5_s1 | enlarge_patch/1.5x | 41.67 F | 2.49 F | 203.00 F | 9.18 (1.08) | 38.59 | no | no |
| growth_zone_flank_swap_z0.5_s1 | enlarge_patch/2x | 29.39 F | 0.73 | 199.70 F | 6.43 (1.08) | 35.96 | no | no |
| growth_zone_flank_swap_z0.5_s1 | change_frame_stride/double | 48.57 F | 2.12 F | 85.54 F | 6.46 (1.08) | 33.25 | no | no |
| growth_zone_flank_swap_z0.5_s1 | change_frame_stride/double + enlarge_patch/1.5x | 35.48 F | 2.51 F | 195.42 F | 8.54 (1.08) | 37.26 | no | no |
| growth_zone_flank_swap_z0.5_s1 | change_frame_stride/double + enlarge_patch/2x | 57.97 F | 0.61 | 193.82 F | 6.45 (1.08) | 35.73 | no | no |
| growth_zone_flank_swap_z0.5_s2 | none | 51.77 F | 2.49 F | 172.60 F | 4.36 (1.08) | 40.93 | no | no |
| growth_zone_flank_swap_z0.5_s2 | enlarge_patch/1.5x | 47.56 F | 0.19 | 67.84 F | 4.22 (1.08) | 23.52 | no | no |
| growth_zone_flank_swap_z0.5_s2 | enlarge_patch/2x | 14.51 F | 3.03 F | 125.08 F | 5.34 (1.08) | 32.22 | no | no |
| growth_zone_flank_swap_z0.5_s2 | change_frame_stride/double | 41.43 F | 2.52 F | 172.87 F | 4.19 (1.08) | 41.38 | no | no |
| growth_zone_flank_swap_z0.5_s2 | change_frame_stride/double + enlarge_patch/1.5x | 47.47 F | 0.22 | 67.45 F | 4.19 (1.08) | 23.02 | no | no |
| growth_zone_flank_swap_z0.5_s2 | change_frame_stride/double + enlarge_patch/2x | 123.86 F | 2.95 F | 145.25 F | 4.94 (1.08) | 40.69 | no | no |
| growth_zone_partial_occlusion_z20_s0 | none | 44.48 F | 0.10 | 34.47 F | 24.55 (1.08) | 7.51 | no | no |
| growth_zone_partial_occlusion_z20_s0 | enlarge_patch/1.5x | 172.12 F | 0.12 | 27.18 F | 15.51 (1.08) | 7.15 | no | no |
| growth_zone_partial_occlusion_z20_s0 | enlarge_patch/2x | 1.93 | 0.19 | 23.90 F | 2.52 (1.08) | 6.00 | no | no |
| growth_zone_partial_occlusion_z20_s0 | change_frame_stride/double | 73.27 F | 0.10 | 35.46 F | 6.70 (1.08) | 6.83 | no | no |
| growth_zone_partial_occlusion_z20_s0 | change_frame_stride/double + enlarge_patch/1.5x | 164.72 F | 0.14 | 31.15 F | 17.23 (1.08) | 7.73 | no | no |
| growth_zone_partial_occlusion_z20_s0 | change_frame_stride/double + enlarge_patch/2x | 0.66 | 0.21 | 7.13 F | 2.35 (1.08) | 1.56 | no | no |
| growth_zone_partial_occlusion_z20_s1 | none | 42.64 F | 0.08 | 15.31 F | 22.58 (1.08) | 3.55 | no | no |
| growth_zone_partial_occlusion_z20_s1 | enlarge_patch/1.5x | 8.32 F | 0.11 | 34.20 F | 8.14 (1.08) | 6.88 | no | no |
| growth_zone_partial_occlusion_z20_s1 | enlarge_patch/2x | 0.75 | 0.17 | 2.52 | 2.11 (1.08) | 0.64 | yes | no |
| growth_zone_partial_occlusion_z20_s1 | change_frame_stride/double | 103.78 F | 0.09 | 14.33 F | 20.60 (1.08) | 3.53 | no | no |
| growth_zone_partial_occlusion_z20_s1 | change_frame_stride/double + enlarge_patch/1.5x | 35.49 F | 0.12 | 36.26 F | 8.74 (1.08) | 6.93 | no | no |
| growth_zone_partial_occlusion_z20_s1 | change_frame_stride/double + enlarge_patch/2x | 0.74 | 0.19 | 2.48 | 1.67 (1.08) | 0.64 | yes | no |
| growth_zone_partial_occlusion_z20_s2 | none | 99.18 F | 0.09 | 5.71 F | 32.82 (1.08) | 1.75 | no | no |
| growth_zone_partial_occlusion_z20_s2 | enlarge_patch/1.5x | 1.30 | 0.09 | 13.73 F | 15.82 (1.08) | 3.17 | no | no |
| growth_zone_partial_occlusion_z20_s2 | enlarge_patch/2x | 2.26 F | 0.14 | 18.62 F | 13.42 (1.08) | 3.74 | no | no |
| growth_zone_partial_occlusion_z20_s2 | change_frame_stride/double | 122.93 F | 0.08 | 6.24 F | 28.94 (1.08) | 1.89 | no | no |
| growth_zone_partial_occlusion_z20_s2 | change_frame_stride/double + enlarge_patch/1.5x | 39.20 F | 0.10 | 42.28 F | 16.93 (1.08) | 7.97 | no | no |
| growth_zone_partial_occlusion_z20_s2 | change_frame_stride/double + enlarge_patch/2x | 4.00 F | 0.15 | 22.63 F | 14.99 (1.08) | 4.89 | no | no |

Not a label state: the width-free ratio on the unremedied run (plane sections skipped; good = centre error within its limit). An agent that applies `use_width_free_ratio` and accepts is scored on this measurement:

| Rod | rigid_invariance | closure | plane_sections | REGR err (limit) | Checks pass | Centre good |
| :-- | --: | --: | --: | --: | :-- | :-- |
| growth_zone_second_root_z30_s0 | 0.70 | 0.10 | 10.97 skip | 0.48 (1.08) | yes | yes |
| growth_zone_second_root_z30_s1 | 0.58 | 0.08 | 9.03 skip | 0.72 (1.08) | yes | yes |
| growth_zone_second_root_z30_s2 | 0.70 | 0.09 | 11.33 skip | 0.83 (1.08) | yes | yes |
| growth_zone_fast_rotation_z2_s0 | 58.59 F | 4.76 F | 91.84 skip | 11.35 (1.08) | no | no |
| growth_zone_fast_rotation_z2_s1 | 72.56 F | 29.63 F | 58.20 skip | 13.26 (1.08) | no | no |
| growth_zone_fast_rotation_z2_s2 | 124.79 F | 17.95 F | 31.70 skip | 23.16 (1.08) | no | no |
| growth_zone_bad_stage_correction_z3_s0 | 0.70 | 2.93 F | 1.38 skip | 0.41 (1.08) | no | yes |
| growth_zone_bad_stage_correction_z3_s1 | 0.58 | 2.92 F | 0.57 skip | 0.44 (1.08) | no | yes |
| growth_zone_bad_stage_correction_z3_s2 | 0.70 | 2.93 F | 0.37 skip | 0.44 (1.08) | no | yes |
| growth_zone_flank_swap_z0.5_s0 | 39.85 F | 1.42 F | 84.90 skip | 6.63 (1.08) | no | no |
| growth_zone_flank_swap_z0.5_s1 | 43.06 F | 2.12 F | 82.97 skip | 6.49 (1.08) | no | no |
| growth_zone_flank_swap_z0.5_s2 | 51.77 F | 2.49 F | 172.60 skip | 4.36 (1.08) | no | no |
| growth_zone_partial_occlusion_z20_s0 | 44.48 F | 0.10 | 34.47 skip | 24.55 (1.08) | no | no |
| growth_zone_partial_occlusion_z20_s1 | 42.64 F | 0.08 | 15.31 skip | 22.58 (1.08) | no | no |
| growth_zone_partial_occlusion_z20_s2 | 99.18 F | 0.09 | 5.71 skip | 32.82 (1.08) | no | no |
