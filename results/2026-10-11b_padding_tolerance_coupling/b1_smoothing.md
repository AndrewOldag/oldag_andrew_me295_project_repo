Smoothing with the fitted-line time padding (tags `mslight3`, `msstrong3`). Unremedied runs: item 4 of the 2026-10-11 spec (same code). Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.

## Clean rods

| Case | Remedy | n | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR err (%/h) | Flank err (%/h) | All pass | Run time (s) |
| :-- | :-- | --: | --: | --: | --: | --: | --: | :-- | --: |
| growth_zone | none | 3 | 0.70 [0.58, 0.70] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 5.10 [5.00, 5.30] |
| growth_zone | smooth_midline light | 3 | 0.69 [0.65, 0.93] | 0.09 [0.08, 0.10] | 0.57 [0.37, 1.39] | 0.44 [0.41, 0.44] | 0.18 [0.15, 0.29] | 3 of 3 | 5.30 [5.10, 5.30] |
| growth_zone | smooth_midline strong | 3 | 0.87 [0.77, 1.06] | 1.57 [1.55, 1.58] | 0.36 [0.32, 1.47] | 0.45 [0.41, 0.46] | 0.14 [0.13, 0.31] | 0 of 3 | 5.20 [5.10, 5.40] |
| bending | none | 3 | 0.65 [0.62, 0.66] | 0.07 [0.06, 0.07] | 0.58 [0.31, 1.53] | 0.43 [0.41, 0.44] | 0.23 [0.16, 0.33] | 3 of 3 | 5.20 [5.20, 5.30] |
| bending | smooth_midline light | 3 | 0.75 [0.66, 1.23] | 0.08 [0.07, 0.10] | 0.81 [0.40, 1.61] | 0.41 [0.40, 0.44] | 0.29 [0.16, 0.38] | 3 of 3 | 5.30 [5.20, 5.30] |
| bending | smooth_midline strong | 3 | 0.95 [0.67, 0.95] | 1.60 [1.58, 1.60] | 0.73 [0.48, 1.55] | 0.43 [0.43, 0.46] | 0.26 [0.14, 0.35] | 0 of 3 | 5.30 [5.30, 5.30] |

Cells: median [min, max] over seeds 0-2. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.

Clean runs failing an approved threshold: bending_clean_s0 smooth_midline strong, bending_clean_s1 smooth_midline strong, bending_clean_s2 smooth_midline strong, growth_zone_clean_s0 smooth_midline strong, growth_zone_clean_s1 smooth_midline strong, growth_zone_clean_s2 smooth_midline strong

## midline_jitter

| Fault | Size | Unremedied: seeds failing a check | Remedied (1 step): seeds with three passes | Remedied: three passes and good | Meets criteria |
| :-- | :-- | :-- | :-- | :-- | :-- |
| midline_jitter | 0.5 | 3 of 3 | 1 of 3 | 1 of 3 | no |
| midline_jitter | 1 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 2 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |

| Rod | Label | Repairing remedy |
| :-- | :-- | :-- |
| growth_zone_midline_jitter_z0.5_s0 | not repairable | - |
| growth_zone_midline_jitter_z0.5_s1 | not repairable | - |
| growth_zone_midline_jitter_z0.5_s2 | repairable | smooth_midline light |
| growth_zone_midline_jitter_z1_s0 | not repairable | - |
| growth_zone_midline_jitter_z1_s1 | not repairable | - |
| growth_zone_midline_jitter_z1_s2 | not repairable | - |
| growth_zone_midline_jitter_z2_s0 | not repairable | - |
| growth_zone_midline_jitter_z2_s1 | not repairable | - |
| growth_zone_midline_jitter_z2_s2 | not repairable | - |
| growth_zone_midline_jitter_z3_s0 | not repairable | - |
| growth_zone_midline_jitter_z3_s1 | not repairable | - |
| growth_zone_midline_jitter_z3_s2 | not repairable | - |

Per run:

| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| growth_zone_midline_jitter_z0.5_s0 | none | 0.50 | 0.37 | 5.80 F | 0.42 (1.08) | 0.24 | no | yes |
| growth_zone_midline_jitter_z0.5_s0 | smooth_midline light | 0.53 | 0.59 | 4.52 F | 0.42 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z0.5_s0 | smooth_midline strong | 0.76 | 1.57 F | 2.55 | 0.43 (1.08) | 0.33 | no | yes |
| growth_zone_midline_jitter_z0.5_s1 | none | 0.60 | 1.05 F | 4.16 F | 0.41 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z0.5_s1 | smooth_midline light | 0.74 | 0.69 | 3.79 F | 0.40 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z0.5_s1 | smooth_midline strong | 0.71 | 1.66 F | 1.54 | 0.43 (1.08) | 0.21 | no | yes |
| growth_zone_midline_jitter_z0.5_s2 | none | 0.86 | 1.16 F | 4.51 F | 0.42 (1.08) | 0.19 | no | yes |
| growth_zone_midline_jitter_z0.5_s2 | smooth_midline light | 0.77 | 0.48 | 2.49 | 0.42 (1.08) | 0.18 | yes | yes |
| growth_zone_midline_jitter_z0.5_s2 | smooth_midline strong | 0.70 | 1.90 F | 1.31 | 0.42 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z1_s0 | none | 0.49 | 0.73 | 11.46 F | 0.44 (1.08) | 0.34 | no | yes |
| growth_zone_midline_jitter_z1_s0 | smooth_midline light | 0.53 | 1.17 F | 8.59 F | 0.43 (1.08) | 0.29 | no | yes |
| growth_zone_midline_jitter_z1_s0 | smooth_midline strong | 0.83 | 1.62 F | 4.12 F | 0.43 (1.08) | 0.38 | no | yes |
| growth_zone_midline_jitter_z1_s1 | none | 0.62 | 2.09 F | 8.34 F | 0.41 (1.08) | 0.28 | no | yes |
| growth_zone_midline_jitter_z1_s1 | smooth_midline light | 0.68 | 1.39 F | 7.27 F | 0.40 (1.08) | 0.27 | no | yes |
| growth_zone_midline_jitter_z1_s1 | smooth_midline strong | 0.71 | 1.94 F | 2.91 | 0.43 (1.08) | 0.27 | no | yes |
| growth_zone_midline_jitter_z1_s2 | none | 0.86 | 2.30 F | 8.60 F | 0.42 (1.08) | 0.21 | no | yes |
| growth_zone_midline_jitter_z1_s2 | smooth_midline light | 0.79 | 0.94 | 4.98 F | 0.42 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z1_s2 | smooth_midline strong | 0.71 | 2.59 F | 2.91 | 0.42 (1.08) | 0.29 | no | yes |
| growth_zone_midline_jitter_z2_s0 | none | 0.78 | 1.49 F | 23.65 F | 0.54 (1.08) | 0.50 | no | no |
| growth_zone_midline_jitter_z2_s0 | smooth_midline light | 0.63 | 2.36 F | 17.38 F | 0.44 (1.08) | 0.44 | no | yes |
| growth_zone_midline_jitter_z2_s0 | smooth_midline strong | 0.77 | 1.77 F | 7.19 F | 0.44 (1.08) | 0.44 | no | yes |
| growth_zone_midline_jitter_z2_s1 | none | 0.77 | 4.15 F | 17.10 F | 0.41 (1.08) | 0.39 | no | yes |
| growth_zone_midline_jitter_z2_s1 | smooth_midline light | 0.74 | 2.78 F | 14.14 F | 0.40 (1.08) | 0.36 | no | yes |
| growth_zone_midline_jitter_z2_s1 | smooth_midline strong | 0.89 | 2.79 F | 5.88 F | 0.43 (1.08) | 0.26 | no | yes |
| growth_zone_midline_jitter_z2_s2 | none | 0.55 | 4.45 F | 16.97 F | 0.42 (1.08) | 0.33 | no | yes |
| growth_zone_midline_jitter_z2_s2 | smooth_midline light | 0.79 | 1.86 F | 10.07 F | 0.41 (1.08) | 0.29 | no | yes |
| growth_zone_midline_jitter_z2_s2 | smooth_midline strong | 0.56 | 4.32 F | 5.34 F | 0.41 (1.08) | 0.34 | no | yes |
| growth_zone_midline_jitter_z3_s0 | none | 0.58 | 2.24 F | 35.34 F | 0.80 (1.08) | 0.76 | no | no |
| growth_zone_midline_jitter_z3_s0 | smooth_midline light | 0.51 | 3.54 F | 26.10 F | 0.54 (1.08) | 0.53 | no | no |
| growth_zone_midline_jitter_z3_s0 | smooth_midline strong | 0.73 | 2.01 F | 10.41 F | 0.45 (1.08) | 0.46 | no | yes |
| growth_zone_midline_jitter_z3_s1 | none | 0.78 | 6.18 F | 25.90 F | 0.42 (1.08) | 0.49 | no | yes |
| growth_zone_midline_jitter_z3_s1 | smooth_midline light | 0.58 | 4.17 F | 20.94 F | 0.41 (1.08) | 0.47 | no | yes |
| growth_zone_midline_jitter_z3_s1 | smooth_midline strong | 0.87 | 3.80 F | 9.04 F | 0.43 (1.08) | 0.35 | no | yes |
| growth_zone_midline_jitter_z3_s2 | none | 0.67 | 6.83 F | 26.36 F | 0.42 (1.08) | 0.50 | no | no |
| growth_zone_midline_jitter_z3_s2 | smooth_midline light | 0.89 | 2.77 F | 14.75 F | 0.42 (1.08) | 0.38 | no | yes |
| growth_zone_midline_jitter_z3_s2 | smooth_midline strong | 0.62 | 6.32 F | 7.80 F | 0.42 (1.08) | 0.37 | no | yes |
