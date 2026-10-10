| Group | n | REGR rms err (%/h) | REGR max err (%/h) | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | Failed checks (runs) | As expected |
| :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |
| width_change_k267 | 3 | 0.43 [0.42, 0.45] | 1.04 [1.03, 1.35] | 0.56 [0.45, 0.66] | 0.06 [0.06, 0.06] | 5.15 [4.98, 6.04] | plane_sections 3 |  |
| width_change_k400 | 3 | 0.42 [0.40, 0.43] | 1.32 [1.20, 1.37] | 0.76 [0.44, 1.06] | 0.08 [0.07, 0.10] | 3.55 [3.43, 4.30] | plane_sections 3 |  |
| rigid_rotation_r0.01 (closure expected to fail) | 3 | 0.11 [0.10, 0.15] | 0.31 [0.29, 0.37] | 0.98 [0.87, 1.09] | 0.58 [0.54, 0.58] | 0.56 [0.50, 0.72] | none | 0 of 3 |
| rigid_rotation_r0.03 (closure expected to fail) | 3 | 0.14 [0.12, 0.18] | 0.46 [0.36, 0.55] | 0.99 [0.79, 1.15] | 1.70 [1.68, 1.74] | 0.88 [0.70, 0.92] | closure 3 | 3 of 3 |
| rigid_rotation_r0.1 (closure expected to fail) | 3 | 0.20 [0.13, 0.25] | 0.64 [0.35, 0.66] | 0.86 [0.77, 0.98] | 5.60 [5.55, 5.60] | 0.89 [0.87, 0.96] | closure 3 | 3 of 3 |

Cells: median [min, max] over seeds. Pass or fail at the approved thresholds. As expected: clean cases against `IMAGE_EXPECTED`.
