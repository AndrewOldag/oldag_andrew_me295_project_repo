# Held-out faults: checker only, seeds 0-2, unremedied, uncoupled

Thresholds: config/checker_thresholds.yaml (approved 2026-10-10). F = fails.

| Fault | Size | Unit | Seeds failing the checker | Checks failing (seeds) |
| :-- | --: | :-- | :-- | :-- |
| second_root | 15 | px past the near edge | 0 of 3 |  |
| second_root | 30 | px past the near edge | 3 of 3 | plane_sections 3 |
| fast_rotation | 2 | deg/frame for 3 frames | 3 of 3 | rigid_invariance 3, closure 3, plane_sections 3 |
| fast_rotation | 4 | deg/frame for 3 frames | 3 of 3 | rigid_invariance 3, closure 3, plane_sections 3 |
| bad_stage_correction | 3 | px under-reported | 3 of 3 | closure 3 |
| bad_stage_correction | 10 | px under-reported | 3 of 3 | rigid_invariance 3, closure 3, plane_sections 3 |
| flank_swap | 0.5 | fraction of the window swapped | 3 of 3 | rigid_invariance 3, closure 3, plane_sections 3 |
| partial_occlusion | 20 | px drop radius | 3 of 3 | rigid_invariance 3, plane_sections 3 |
| partial_occlusion | 30 | px drop radius | 3 of 3 | rigid_invariance 3, plane_sections 3 |

| Fault | Size | Seed | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR RMS err (%/h) | Checker |
| :-- | --: | --: | --: | --: | --: | --: | :-- |
| second_root | 15 | 0 | 0.70 | 0.10 | 2.04 | 0.41 | pass |
| second_root | 15 | 1 | 0.58 | 0.08 | 2.37 | 0.44 | pass |
| second_root | 15 | 2 | 0.70 | 0.09 | 1.80 | 0.44 | pass |
| second_root | 30 | 0 | 0.70 | 0.10 | 10.97 F | 0.48 | fail |
| second_root | 30 | 1 | 0.58 | 0.08 | 9.03 F | 0.72 | fail |
| second_root | 30 | 2 | 0.70 | 0.09 | 11.33 F | 0.83 | fail |
| fast_rotation | 2 | 0 | 58.59 F | 4.76 F | 91.84 F | 11.35 | fail |
| fast_rotation | 2 | 1 | 72.56 F | 29.63 F | 58.20 F | 13.26 | fail |
| fast_rotation | 2 | 2 | 124.79 F | 17.95 F | 31.70 F | 23.16 | fail |
| fast_rotation | 4 | 0 | 352.49 F | 14.02 F | 273.53 F | 41.48 | fail |
| fast_rotation | 4 | 1 | 127.94 F | 4.40 F | 330.83 F | 32.79 | fail |
| fast_rotation | 4 | 2 | 256.57 F | 34.37 F | 191.21 F | 60.25 | fail |
| bad_stage_correction | 3 | 0 | 0.70 | 2.93 F | 1.38 | 0.41 | fail |
| bad_stage_correction | 3 | 1 | 0.58 | 2.92 F | 0.57 | 0.44 | fail |
| bad_stage_correction | 3 | 2 | 0.70 | 2.93 F | 0.37 | 0.44 | fail |
| bad_stage_correction | 10 | 0 | 65.22 F | 5.58 F | 251.36 F | 26.06 | fail |
| bad_stage_correction | 10 | 1 | 42.24 F | 12.04 F | 95.43 F | 25.22 | fail |
| bad_stage_correction | 10 | 2 | 66.12 F | 12.15 F | 121.67 F | 29.48 | fail |
| flank_swap | 0.5 | 0 | 39.85 F | 1.42 F | 84.90 F | 6.63 | fail |
| flank_swap | 0.5 | 1 | 43.06 F | 2.12 F | 82.97 F | 6.49 | fail |
| flank_swap | 0.5 | 2 | 51.77 F | 2.49 F | 172.60 F | 4.36 | fail |
| partial_occlusion | 20 | 0 | 44.48 F | 0.10 | 34.47 F | 24.55 | fail |
| partial_occlusion | 20 | 1 | 42.64 F | 0.08 | 15.31 F | 22.58 | fail |
| partial_occlusion | 20 | 2 | 99.18 F | 0.09 | 5.71 F | 32.82 | fail |
| partial_occlusion | 30 | 0 | 169.99 F | 0.10 | 255.11 F | 46.26 | fail |
| partial_occlusion | 30 | 1 | 211.22 F | 0.08 | 135.71 F | 24.79 | fail |
| partial_occlusion | 30 | 2 | 117.27 F | 0.09 | 111.81 F | 35.97 | fail |
