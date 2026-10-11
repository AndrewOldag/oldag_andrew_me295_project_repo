Criteria (spec 2026-10-10): the unremedied rod fails a check on every seed, and the fitting remedy gives three passes and a good measurement on at least 2 of 3 seeds. Good: approved tolerance (REGR limit in brackets, 2.5 % of the true peak; flank 0.5 %/h). Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.

| Fault | Size | Unremedied: seeds failing a check | Remedied (1 step): seeds with three passes | Remedied: three passes and good | Meets criteria |
| :-- | :-- | :-- | :-- | :-- | :-- |
| rigid_drift | 0.25 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| rigid_drift | 0.5 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| rigid_drift | 0.75 | 3 of 3 | 3 of 3 | 2 of 3 | yes |
| rigid_drift | 1 | 3 of 3 | 3 of 3 | 2 of 3 | yes |
| midline_jitter | 0.5 | 3 of 3 | 1 of 3 | 1 of 3 | no |
| midline_jitter | 1 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 2 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| low_texture | 0.2 | 3 of 3 | 1 of 3 | 0 of 3 | no |
| low_texture | 0.25 | 3 of 3 | 2 of 3 | 0 of 3 | no |

Labels (from these states only):

| Rod | Label | Repairing remedy |
| :-- | :-- | :-- |
| growth_zone_rigid_drift_z0.25_s0 | repairable | register_frames |
| growth_zone_rigid_drift_z0.25_s1 | repairable | register_frames |
| growth_zone_rigid_drift_z0.25_s2 | repairable | register_frames |
| growth_zone_rigid_drift_z0.5_s0 | repairable | register_frames |
| growth_zone_rigid_drift_z0.5_s1 | repairable | register_frames |
| growth_zone_rigid_drift_z0.5_s2 | repairable | register_frames |
| growth_zone_rigid_drift_z0.75_s0 | not repairable | - |
| growth_zone_rigid_drift_z0.75_s1 | repairable | register_frames |
| growth_zone_rigid_drift_z0.75_s2 | repairable | register_frames |
| growth_zone_rigid_drift_z1_s0 | not repairable | - |
| growth_zone_rigid_drift_z1_s1 | repairable | register_frames |
| growth_zone_rigid_drift_z1_s2 | repairable | register_frames |
| growth_zone_midline_jitter_z0.5_s0 | repairable | smooth_midline strong |
| growth_zone_midline_jitter_z0.5_s1 | not repairable | - |
| growth_zone_midline_jitter_z0.5_s2 | not repairable | - |
| growth_zone_midline_jitter_z1_s0 | not repairable | - |
| growth_zone_midline_jitter_z1_s1 | not repairable | - |
| growth_zone_midline_jitter_z1_s2 | not repairable | - |
| growth_zone_midline_jitter_z2_s0 | not repairable | - |
| growth_zone_midline_jitter_z2_s1 | not repairable | - |
| growth_zone_midline_jitter_z2_s2 | not repairable | - |
| growth_zone_midline_jitter_z3_s0 | not repairable | - |
| growth_zone_midline_jitter_z3_s1 | not repairable | - |
| growth_zone_midline_jitter_z3_s2 | not repairable | - |
| growth_zone_low_texture_z0.2_s0 | not repairable | - |
| growth_zone_low_texture_z0.2_s1 | not repairable | - |
| growth_zone_low_texture_z0.2_s2 | not repairable | - |
| growth_zone_low_texture_z0.25_s0 | not repairable | - |
| growth_zone_low_texture_z0.25_s1 | not repairable | - |
| growth_zone_low_texture_z0.25_s2 | not repairable | - |

Per run (F = fails the approved threshold):

| Rod | Remedy | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| growth_zone_rigid_drift_z0.25_s0 | none | 0.77 | 4.09 F | 1.56 | 0.42 (1.08) | 0.32 | no | yes |
| growth_zone_rigid_drift_z0.25_s0 | register_frames | 1.63 | 0.39 | 1.88 | 0.41 (1.08) | 0.38 | yes | yes |
| growth_zone_rigid_drift_z0.25_s1 | none | 0.74 | 4.12 F | 0.53 | 0.42 (1.08) | 0.21 | no | yes |
| growth_zone_rigid_drift_z0.25_s1 | register_frames | 1.06 | 0.20 | 0.57 | 0.42 (1.08) | 0.20 | yes | yes |
| growth_zone_rigid_drift_z0.25_s2 | none | 0.67 | 4.13 F | 0.51 | 0.44 (1.08) | 0.19 | no | yes |
| growth_zone_rigid_drift_z0.25_s2 | register_frames | 0.92 | 0.33 | 0.46 | 0.46 (1.08) | 0.19 | yes | yes |
| growth_zone_rigid_drift_z0.5_s0 | none | 0.60 | 8.13 F | 1.43 | 0.43 (1.08) | 0.30 | no | yes |
| growth_zone_rigid_drift_z0.5_s0 | register_frames | 0.88 | 0.24 | 2.00 | 0.41 (1.08) | 0.40 | yes | yes |
| growth_zone_rigid_drift_z0.5_s1 | none | 0.56 | 8.18 F | 0.45 | 0.43 (1.08) | 0.20 | no | yes |
| growth_zone_rigid_drift_z0.5_s1 | register_frames | 0.86 | 0.32 | 0.66 | 0.44 (1.08) | 0.27 | yes | yes |
| growth_zone_rigid_drift_z0.5_s2 | none | 0.59 | 8.15 F | 0.56 | 0.45 (1.08) | 0.22 | no | yes |
| growth_zone_rigid_drift_z0.5_s2 | register_frames | 0.82 | 0.45 | 0.57 | 0.46 (1.08) | 0.24 | yes | yes |
| growth_zone_rigid_drift_z0.75_s0 | none | 0.51 | 12.19 F | 1.45 | 0.42 (1.08) | 0.31 | no | yes |
| growth_zone_rigid_drift_z0.75_s0 | register_frames | 0.87 | 0.33 | 2.69 | 0.44 (1.08) | 0.54 | yes | no |
| growth_zone_rigid_drift_z0.75_s1 | none | 0.53 | 12.22 F | 0.93 | 0.44 (1.08) | 0.27 | no | yes |
| growth_zone_rigid_drift_z0.75_s1 | register_frames | 1.02 | 0.24 | 1.31 | 0.47 (1.08) | 0.35 | yes | yes |
| growth_zone_rigid_drift_z0.75_s2 | none | 0.97 | 12.20 F | 0.69 | 0.43 (1.08) | 0.23 | no | yes |
| growth_zone_rigid_drift_z0.75_s2 | register_frames | 0.67 | 0.25 | 0.80 | 0.45 (1.08) | 0.30 | yes | yes |
| growth_zone_rigid_drift_z1_s0 | none | 0.49 | 16.27 F | 1.39 | 0.41 (1.08) | 0.27 | no | yes |
| growth_zone_rigid_drift_z1_s0 | register_frames | 1.08 | 0.37 | 2.88 | 0.51 (1.08) | 0.58 | yes | no |
| growth_zone_rigid_drift_z1_s1 | none | 0.69 | 16.30 F | 0.61 | 0.42 (1.08) | 0.22 | no | yes |
| growth_zone_rigid_drift_z1_s1 | register_frames | 0.78 | 0.11 | 1.35 | 0.52 (1.08) | 0.41 | yes | yes |
| growth_zone_rigid_drift_z1_s2 | none | 0.46 | 16.27 F | 0.56 | 0.44 (1.08) | 0.20 | no | yes |
| growth_zone_rigid_drift_z1_s2 | register_frames | 1.56 | 0.18 | 0.90 | 0.54 (1.08) | 0.34 | yes | yes |
| growth_zone_midline_jitter_z0.5_s0 | none | 0.50 | 0.37 | 5.80 F | 0.42 (1.08) | 0.24 | no | yes |
| growth_zone_midline_jitter_z0.5_s0 | smooth_midline light | 0.50 | 0.37 | 5.00 F | 0.42 (1.08) | 0.24 | no | yes |
| growth_zone_midline_jitter_z0.5_s0 | smooth_midline strong | 0.50 | 0.37 | 2.83 | 0.42 (1.08) | 0.22 | yes | yes |
| growth_zone_midline_jitter_z0.5_s1 | none | 0.60 | 1.05 F | 4.16 F | 0.41 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z0.5_s1 | smooth_midline light | 0.61 | 1.05 F | 3.51 F | 0.41 (1.08) | 0.22 | no | yes |
| growth_zone_midline_jitter_z0.5_s1 | smooth_midline strong | 0.56 | 1.05 F | 1.88 | 0.41 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z0.5_s2 | none | 0.86 | 1.16 F | 4.51 F | 0.42 (1.08) | 0.19 | no | yes |
| growth_zone_midline_jitter_z0.5_s2 | smooth_midline light | 0.86 | 1.16 F | 3.70 F | 0.42 (1.08) | 0.19 | no | yes |
| growth_zone_midline_jitter_z0.5_s2 | smooth_midline strong | 0.88 | 1.17 F | 2.11 | 0.42 (1.08) | 0.18 | no | yes |
| growth_zone_midline_jitter_z1_s0 | none | 0.49 | 0.73 | 11.46 F | 0.44 (1.08) | 0.34 | no | yes |
| growth_zone_midline_jitter_z1_s0 | smooth_midline light | 0.56 | 0.73 | 9.87 F | 0.44 (1.08) | 0.32 | no | yes |
| growth_zone_midline_jitter_z1_s0 | smooth_midline strong | 0.52 | 0.73 | 5.43 F | 0.43 (1.08) | 0.29 | no | yes |
| growth_zone_midline_jitter_z1_s1 | none | 0.62 | 2.09 F | 8.34 F | 0.41 (1.08) | 0.28 | no | yes |
| growth_zone_midline_jitter_z1_s1 | smooth_midline light | 0.54 | 2.09 F | 6.99 F | 0.41 (1.08) | 0.26 | no | yes |
| growth_zone_midline_jitter_z1_s1 | smooth_midline strong | 0.50 | 2.09 F | 3.55 F | 0.41 (1.08) | 0.23 | no | yes |
| growth_zone_midline_jitter_z1_s2 | none | 0.86 | 2.30 F | 8.60 F | 0.42 (1.08) | 0.21 | no | yes |
| growth_zone_midline_jitter_z1_s2 | smooth_midline light | 0.88 | 2.30 F | 7.05 F | 0.42 (1.08) | 0.21 | no | yes |
| growth_zone_midline_jitter_z1_s2 | smooth_midline strong | 0.90 | 2.30 F | 4.06 F | 0.42 (1.08) | 0.22 | no | yes |
| growth_zone_midline_jitter_z2_s0 | none | 0.78 | 1.49 F | 23.65 F | 0.54 (1.08) | 0.50 | no | no |
| growth_zone_midline_jitter_z2_s0 | smooth_midline light | 0.97 | 1.49 F | 20.15 F | 0.52 (1.08) | 0.48 | no | yes |
| growth_zone_midline_jitter_z2_s0 | smooth_midline strong | 0.68 | 1.49 F | 10.64 F | 0.46 (1.08) | 0.38 | no | yes |
| growth_zone_midline_jitter_z2_s1 | none | 0.77 | 4.15 F | 17.10 F | 0.41 (1.08) | 0.39 | no | yes |
| growth_zone_midline_jitter_z2_s1 | smooth_midline light | 0.78 | 4.15 F | 14.31 F | 0.41 (1.08) | 0.37 | no | yes |
| growth_zone_midline_jitter_z2_s1 | smooth_midline strong | 0.76 | 4.15 F | 7.16 F | 0.42 (1.08) | 0.31 | no | yes |
| growth_zone_midline_jitter_z2_s2 | none | 0.55 | 4.45 F | 16.97 F | 0.42 (1.08) | 0.33 | no | yes |
| growth_zone_midline_jitter_z2_s2 | smooth_midline light | 0.65 | 4.45 F | 13.60 F | 0.42 (1.08) | 0.32 | no | yes |
| growth_zone_midline_jitter_z2_s2 | smooth_midline strong | 0.71 | 4.45 F | 7.93 F | 0.42 (1.08) | 0.26 | no | yes |
| growth_zone_midline_jitter_z3_s0 | none | 0.58 | 2.24 F | 35.34 F | 0.80 (1.08) | 0.76 | no | no |
| growth_zone_midline_jitter_z3_s0 | smooth_midline light | 0.67 | 2.24 F | 30.08 F | 0.77 (1.08) | 0.72 | no | no |
| growth_zone_midline_jitter_z3_s0 | smooth_midline strong | 0.54 | 2.23 F | 15.47 F | 0.64 (1.08) | 0.55 | no | no |
| growth_zone_midline_jitter_z3_s1 | none | 0.78 | 6.18 F | 25.90 F | 0.42 (1.08) | 0.49 | no | yes |
| growth_zone_midline_jitter_z3_s1 | smooth_midline light | 0.83 | 6.17 F | 21.42 F | 0.42 (1.08) | 0.48 | no | yes |
| growth_zone_midline_jitter_z3_s1 | smooth_midline strong | 0.60 | 6.16 F | 10.76 F | 0.42 (1.08) | 0.38 | no | yes |
| growth_zone_midline_jitter_z3_s2 | none | 0.67 | 6.83 F | 26.36 F | 0.42 (1.08) | 0.50 | no | no |
| growth_zone_midline_jitter_z3_s2 | smooth_midline light | 0.69 | 6.83 F | 20.84 F | 0.42 (1.08) | 0.42 | no | yes |
| growth_zone_midline_jitter_z3_s2 | smooth_midline strong | 0.63 | 6.83 F | 11.77 F | 0.42 (1.08) | 0.38 | no | yes |
| growth_zone_low_texture_z0.2_s0 | none | 2.95 F | 0.35 | 3.57 F | 0.76 (1.08) | 1.40 | no | no |
| growth_zone_low_texture_z0.2_s0 | enlarge_patch 1.5x | 1.92 | 0.26 | 2.45 | 0.67 (1.08) | 1.02 | yes | no |
| growth_zone_low_texture_z0.2_s0 | enlarge_patch 2x | 1.72 | 0.29 | 2.26 | 0.84 (1.08) | 0.94 | yes | no |
| growth_zone_low_texture_z0.2_s1 | none | 5.69 F | 0.17 | 2.18 | 0.86 (1.08) | 1.01 | no | no |
| growth_zone_low_texture_z0.2_s1 | enlarge_patch 1.5x | 2.92 F | 0.13 | 1.68 | 0.67 (1.08) | 0.73 | no | no |
| growth_zone_low_texture_z0.2_s1 | enlarge_patch 2x | 2.09 F | 0.11 | 1.77 | 0.80 (1.08) | 0.74 | no | no |
| growth_zone_low_texture_z0.2_s2 | none | 4.77 F | 0.13 | 5.00 F | 1.19 (1.08) | 1.58 | no | no |
| growth_zone_low_texture_z0.2_s2 | enlarge_patch 1.5x | 3.11 F | 0.11 | 3.05 | 0.91 (1.08) | 1.01 | no | no |
| growth_zone_low_texture_z0.2_s2 | enlarge_patch 2x | 2.90 F | 0.20 | 1.91 | 0.93 (1.08) | 0.75 | no | no |
| growth_zone_low_texture_z0.25_s0 | none | 2.14 F | 0.28 | 3.10 | 0.60 (1.08) | 1.07 | no | no |
| growth_zone_low_texture_z0.25_s0 | enlarge_patch 1.5x | 1.44 | 0.23 | 2.07 | 0.61 (1.08) | 0.78 | yes | no |
| growth_zone_low_texture_z0.25_s0 | enlarge_patch 2x | 1.37 | 0.28 | 2.07 | 0.81 (1.08) | 0.76 | yes | no |
| growth_zone_low_texture_z0.25_s1 | none | 4.32 F | 0.11 | 1.64 | 0.67 (1.08) | 0.74 | no | no |
| growth_zone_low_texture_z0.25_s1 | enlarge_patch 1.5x | 2.19 F | 0.10 | 1.42 | 0.61 (1.08) | 0.54 | no | no |
| growth_zone_low_texture_z0.25_s1 | enlarge_patch 2x | 1.56 | 0.12 | 1.50 | 0.77 (1.08) | 0.57 | yes | no |
| growth_zone_low_texture_z0.25_s2 | none | 3.57 F | 0.12 | 3.53 F | 0.90 (1.08) | 1.11 | no | no |
| growth_zone_low_texture_z0.25_s2 | enlarge_patch 1.5x | 2.32 F | 0.10 | 1.93 | 0.75 (1.08) | 0.68 | no | no |
| growth_zone_low_texture_z0.25_s2 | enlarge_patch 2x | 2.25 F | 0.17 | 1.43 | 0.85 (1.08) | 0.52 | no | no |
