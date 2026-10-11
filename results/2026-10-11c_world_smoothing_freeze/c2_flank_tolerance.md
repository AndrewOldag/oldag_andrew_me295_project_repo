Clean set: growth_zone, bending, bend_continue, bend_reverse, seeds 0-2 (12 rods). Runs: unremedied, enlarge_patch and crop_or_mask of growth_zone and bending from 2026-10-10 (same code); register_frames from 2026-10-11 item 4; smoothing (world coordinates) and every bent-rod remedy from this spec.

| Setting | Runs | All pass | Largest flank err (%/h) | Largest centre err / true peak |
| :-- | --: | :-- | --: | --: |
| none | 12 | 12 of 12 | 0.59 | 1.33 % |
| register_frames | 12 | 12 of 12 | 0.66 | 1.38 % |
| smooth_midline light | 12 | 12 of 12 | 0.59 | 1.46 % |
| smooth_midline strong | 12 | 6 of 12 | 0.62 | 1.96 % |
| enlarge_patch 1.5x | 12 | 12 of 12 | 0.63 | 1.79 % |
| enlarge_patch 2x | 12 | 12 of 12 | 0.80 | 2.45 % |
| crop_or_mask mask_second_root | 12 | 12 of 12 | 0.59 | 1.33 % |
| crop_or_mask crop_to_main_root | 12 | 12 of 12 | 0.59 | 1.33 % |

Settings that keep every clean run passing: crop_or_mask crop_to_main_root, crop_or_mask mask_second_root, enlarge_patch 1.5x, enlarge_patch 2x, none, register_frames, smooth_midline light.

Largest clean flank-difference RMS error under them: 0.797 %/h (bend_reverse_clean_s0, enlarge_patch 2x). Rounded up to the next 0.25 %/h: 1.00 %/h.

Largest clean centre REGR RMS error as a fraction of the true peak: 2.45 % (bend_continue_clean_s2, enlarge_patch 2x); approved limit 2.5 %.

Clean runs failing an approved threshold: bend_continue_clean_s0 smooth_midline strong: plane_sections 3.53; bend_continue_clean_s1 smooth_midline strong: plane_sections 3.86; bend_continue_clean_s2 smooth_midline strong: plane_sections 3.43; bend_reverse_clean_s0 smooth_midline strong: plane_sections 4.69; bend_reverse_clean_s1 smooth_midline strong: plane_sections 4.38; bend_reverse_clean_s2 smooth_midline strong: plane_sections 4.58

| Case | Remedy | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | All pass | Run time (s) |
| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- | --: |
| growth_zone | none | 3 | 0.70 [0.58, 0.70] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 27.90 [27.00, 28.40] |
| growth_zone | register_frames | 3 | 1.27 [0.80, 1.86] | 0.11 [0.09, 0.11] | 0.48 [0.43, 1.67] | 0.44 [0.41, 0.45] | 0.18 [0.17, 0.34] | 3 of 3 | 5.10 [5.00, 5.20] |
| growth_zone | smooth_midline light | 3 | 0.69 [0.65, 0.93] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 5.30 [5.10, 5.30] |
| growth_zone | smooth_midline strong | 3 | 0.74 [0.63, 0.96] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.19 [0.14, 0.29] | 3 of 3 | 5.20 [5.10, 5.30] |
| growth_zone | enlarge_patch 1.5x | 3 | 0.67 [0.63, 0.82] | 0.11 [0.09, 0.12] | 0.54 [0.34, 1.22] | 0.55 [0.53, 0.56] | 0.15 [0.13, 0.28] | 3 of 3 | 31.60 [30.90, 33.70] |
| growth_zone | enlarge_patch 2x | 3 | 0.63 [0.62, 0.75] | 0.17 [0.14, 0.19] | 0.69 [0.54, 1.47] | 0.74 [0.73, 0.76] | 0.20 [0.16, 0.36] | 3 of 3 | 37.50 [33.60, 43.60] |
| growth_zone | crop_or_mask mask_second_root | 3 | 0.70 [0.58, 0.70] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 24.60 [19.50, 25.90] |
| growth_zone | crop_or_mask crop_to_main_root | 3 | 0.70 [0.58, 0.70] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 22.20 [20.90, 29.60] |
| bending | none | 3 | 0.65 [0.62, 0.66] | 0.07 [0.06, 0.07] | 0.58 [0.31, 1.53] | 0.43 [0.41, 0.44] | 0.23 [0.16, 0.33] | 3 of 3 | 21.90 [18.00, 28.10] |
| bending | register_frames | 3 | 1.01 [0.68, 1.64] | 0.16 [0.16, 0.16] | 0.61 [0.50, 1.65] | 0.46 [0.43, 0.46] | 0.24 [0.18, 0.36] | 3 of 3 | 5.30 [5.10, 5.40] |
| bending | smooth_midline light | 3 | 0.75 [0.66, 1.23] | 0.08 [0.07, 0.10] | 0.81 [0.40, 1.61] | 0.41 [0.40, 0.44] | 0.29 [0.16, 0.38] | 3 of 3 | 5.30 [5.20, 5.30] |
| bending | smooth_midline strong | 3 | 0.73 [0.67, 1.23] | 0.08 [0.07, 0.10] | 0.81 [0.63, 1.49] | 0.41 [0.40, 0.44] | 0.29 [0.16, 0.39] | 3 of 3 | 5.20 [5.20, 5.80] |
| bending | enlarge_patch 1.5x | 3 | 0.54 [0.50, 0.55] | 0.10 [0.08, 0.10] | 0.55 [0.51, 1.38] | 0.55 [0.52, 0.55] | 0.19 [0.17, 0.31] | 3 of 3 | 31.60 [28.70, 32.40] |
| bending | enlarge_patch 2x | 3 | 0.49 [0.45, 0.51] | 0.16 [0.13, 0.18] | 0.86 [0.51, 1.61] | 0.74 [0.72, 0.77] | 0.22 [0.18, 0.37] | 3 of 3 | 33.10 [23.20, 38.70] |
| bending | crop_or_mask mask_second_root | 3 | 0.65 [0.62, 0.66] | 0.07 [0.06, 0.07] | 0.58 [0.31, 1.53] | 0.43 [0.41, 0.44] | 0.23 [0.16, 0.33] | 3 of 3 | 22.50 [15.60, 27.10] |
| bending | crop_or_mask crop_to_main_root | 3 | 0.65 [0.62, 0.66] | 0.07 [0.06, 0.07] | 0.58 [0.31, 1.53] | 0.43 [0.41, 0.44] | 0.23 [0.16, 0.33] | 3 of 3 | 21.10 [14.10, 21.10] |
| bend_continue | none | 3 | 0.71 [0.67, 0.72] | 0.12 [0.11, 0.13] | 0.89 [0.62, 1.75] | 0.57 [0.54, 0.58] | 0.33 [0.33, 0.40] | 3 of 3 | 5.20 [5.20, 5.30] |
| bend_continue | register_frames | 3 | 1.42 [1.06, 1.53] | 0.08 [0.07, 0.13] | 1.23 [0.76, 1.81] | 0.60 [0.55, 0.60] | 0.40 [0.39, 0.45] | 3 of 3 | 5.20 [5.20, 5.30] |
| bend_continue | smooth_midline light | 3 | 0.71 [0.64, 0.71] | 0.12 [0.11, 0.13] | 1.19 [1.00, 1.69] | 0.63 [0.59, 0.64] | 0.34 [0.33, 0.42] | 3 of 3 | 5.20 [5.10, 5.40] |
| bend_continue | smooth_midline strong | 3 | 0.65 [0.62, 0.82] | 0.14 [0.12, 0.17] | 3.53 [3.43, 3.86] | 0.84 [0.81, 0.85] | 0.34 [0.30, 0.46] | 0 of 3 | 5.20 [5.10, 5.20] |
| bend_continue | enlarge_patch 1.5x | 3 | 0.62 [0.55, 0.67] | 0.14 [0.13, 0.15] | 0.77 [0.76, 1.70] | 0.76 [0.75, 0.78] | 0.38 [0.32, 0.39] | 3 of 3 | 6.90 [6.80, 7.00] |
| bend_continue | enlarge_patch 2x | 3 | 0.58 [0.50, 0.65] | 0.20 [0.18, 0.22] | 0.94 [0.90, 2.00] | 1.04 [1.02, 1.06] | 0.39 [0.34, 0.43] | 3 of 3 | 9.30 [9.20, 9.60] |
| bend_continue | crop_or_mask mask_second_root | 3 | 0.71 [0.67, 0.72] | 0.12 [0.11, 0.13] | 0.89 [0.62, 1.75] | 0.57 [0.54, 0.58] | 0.33 [0.33, 0.40] | 3 of 3 | 5.30 [5.00, 5.30] |
| bend_continue | crop_or_mask crop_to_main_root | 3 | 0.71 [0.67, 0.72] | 0.12 [0.11, 0.13] | 0.89 [0.62, 1.75] | 0.57 [0.54, 0.58] | 0.33 [0.33, 0.40] | 3 of 3 | 5.10 [5.10, 5.40] |
| bend_reverse | none | 3 | 0.82 [0.62, 0.90] | 0.10 [0.09, 0.11] | 1.15 [0.93, 2.24] | 0.51 [0.49, 0.52] | 0.53 [0.51, 0.59] | 3 of 3 | 5.30 [5.20, 5.30] |
| bend_reverse | register_frames | 3 | 0.88 [0.72, 1.02] | 0.15 [0.14, 0.17] | 1.11 [1.06, 2.72] | 0.52 [0.51, 0.54] | 0.55 [0.53, 0.66] | 3 of 3 | 5.30 [5.20, 5.50] |
| bend_reverse | smooth_midline light | 3 | 0.72 [0.64, 0.73] | 0.11 [0.09, 0.12] | 1.42 [1.15, 2.54] | 0.52 [0.49, 0.53] | 0.51 [0.49, 0.59] | 3 of 3 | 5.30 [5.20, 5.30] |
| bend_reverse | smooth_midline strong | 3 | 0.72 [0.72, 0.94] | 0.20 [0.17, 0.21] | 4.58 [4.38, 4.69] | 0.49 [0.47, 0.53] | 0.50 [0.48, 0.62] | 0 of 3 | 5.20 [5.10, 5.20] |
| bend_reverse | enlarge_patch 1.5x | 3 | 0.71 [0.57, 0.83] | 0.12 [0.12, 0.12] | 1.32 [0.93, 2.04] | 0.67 [0.65, 0.70] | 0.60 [0.48, 0.63] | 3 of 3 | 6.90 [6.90, 7.10] |
| bend_reverse | enlarge_patch 2x | 3 | 0.66 [0.57, 0.78] | 0.17 [0.16, 0.20] | 1.11 [1.05, 2.04] | 0.94 [0.92, 0.96] | 0.57 [0.54, 0.80] | 3 of 3 | 9.50 [9.10, 9.80] |
| bend_reverse | crop_or_mask mask_second_root | 3 | 0.82 [0.62, 0.90] | 0.10 [0.09, 0.11] | 1.15 [0.93, 2.24] | 0.51 [0.49, 0.52] | 0.53 [0.51, 0.59] | 3 of 3 | 5.20 [5.20, 5.30] |
| bend_reverse | crop_or_mask crop_to_main_root | 3 | 0.82 [0.62, 0.90] | 0.10 [0.09, 0.11] | 1.15 [0.93, 2.24] | 0.51 [0.49, 0.52] | 0.53 [0.51, 0.59] | 3 of 3 | 5.30 [5.20, 5.30] |

Cells: median [min, max] over seeds 0-2. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.
