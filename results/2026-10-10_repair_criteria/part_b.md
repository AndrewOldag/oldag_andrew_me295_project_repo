| Fault | Size | Unremedied: seeds failing a check | Remedied (<= 2 steps): seeds with three passes | Remedied: seeds with three passes and good | Meets criteria |
| :-- | :-- | :-- | :-- | :-- | :-- |
| rigid_drift | 0.25 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 0.5 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 0.75 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 1 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 2x6 | 3 of 3 | 3 of 3 | 3 of 3 | yes |
| displacement_exceeds_patch | 3x4 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 4x3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 0.5 | 3 of 3 | 1 of 3 | 1 of 3 | no |
| midline_jitter | 1 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 2 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| midline_jitter | 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| low_texture | 0.06 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| low_texture | 0.1 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| low_texture | 0.15 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| low_texture | 0.03 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| width_change | None | 3 of 3 | 3 of 3 | 3 of 3 | yes |

Per run (F = fails the approved threshold; skip = not applied):

| Fault | Size | Seed | State | Steps | rigid_invariance | closure | plane_sections | REGR err | Flank err | All pass | Good |
| :-- | :-- | --: | :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |
| rigid_drift | 0.25 | 0 | st1 | 0 | 0.77 | 4.09 F | 1.56 | 0.42 | 0.32 | no | yes |
| rigid_drift | 0.25 | 0 | st1_reg | 1 | 1.12 | 1.33 F | 1.83 | 0.41 | 0.36 | no | yes |
| rigid_drift | 0.25 | 1 | st1 | 0 | 0.74 | 4.12 F | 0.53 | 0.42 | 0.21 | no | yes |
| rigid_drift | 0.25 | 1 | st1_reg | 1 | 0.90 | 1.26 F | 0.67 | 0.41 | 0.21 | no | yes |
| rigid_drift | 0.25 | 2 | st1 | 0 | 0.67 | 4.13 F | 0.51 | 0.44 | 0.19 | no | yes |
| rigid_drift | 0.25 | 2 | st1_reg | 1 | 0.78 | 1.25 F | 0.43 | 0.43 | 0.17 | no | yes |
| rigid_drift | 0.5 | 0 | st1 | 0 | 0.60 | 8.13 F | 1.43 | 0.43 | 0.30 | no | yes |
| rigid_drift | 0.5 | 0 | st1_reg | 1 | 0.64 | 1.37 F | 2.16 | 0.43 | 0.43 | no | yes |
| rigid_drift | 0.5 | 1 | st1 | 0 | 0.56 | 8.18 F | 0.45 | 0.43 | 0.20 | no | yes |
| rigid_drift | 0.5 | 1 | st1_reg | 1 | 1.07 | 1.31 F | 0.95 | 0.46 | 0.33 | no | yes |
| rigid_drift | 0.5 | 2 | st1 | 0 | 0.59 | 8.15 F | 0.56 | 0.45 | 0.22 | no | yes |
| rigid_drift | 0.5 | 2 | st1_reg | 1 | 0.95 | 1.27 F | 0.64 | 0.47 | 0.25 | no | yes |
| rigid_drift | 0.75 | 0 | st1 | 0 | 0.51 | 12.19 F | 1.45 | 0.42 | 0.31 | no | yes |
| rigid_drift | 0.75 | 0 | st1_reg | 1 | 0.70 | 1.34 F | 2.36 | 0.42 | 0.47 | no | yes |
| rigid_drift | 0.75 | 1 | st1 | 0 | 0.53 | 12.22 F | 0.93 | 0.44 | 0.27 | no | yes |
| rigid_drift | 0.75 | 1 | st1_reg | 1 | 0.78 | 1.33 F | 0.94 | 0.50 | 0.36 | no | yes |
| rigid_drift | 0.75 | 2 | st1 | 0 | 0.97 | 12.20 F | 0.69 | 0.43 | 0.23 | no | yes |
| rigid_drift | 0.75 | 2 | st1_reg | 1 | 0.80 | 1.24 F | 0.81 | 0.48 | 0.30 | no | yes |
| rigid_drift | 1 | 0 | st1 | 0 | 0.49 | 16.27 F | 1.39 | 0.41 | 0.27 | no | yes |
| rigid_drift | 1 | 0 | st1_reg | 1 | 0.92 | 1.26 F | 2.91 | 0.51 | 0.61 | no | no |
| rigid_drift | 1 | 1 | st1 | 0 | 0.69 | 16.30 F | 0.61 | 0.42 | 0.22 | no | yes |
| rigid_drift | 1 | 1 | st1_reg | 1 | 1.30 | 1.26 F | 1.28 | 0.53 | 0.44 | no | yes |
| rigid_drift | 1 | 2 | st1 | 0 | 0.46 | 16.27 F | 0.56 | 0.44 | 0.20 | no | yes |
| rigid_drift | 1 | 2 | st1_reg | 1 | 0.99 | 1.13 F | 0.98 | 0.53 | 0.41 | no | yes |
| displacement_exceeds_patch | 2x6 | 0 | st6 | 0 | 222.18 F | 132.19 F | 144.82 F | 34.67 | 43.49 | no | no |
| displacement_exceeds_patch | 2x6 | 0 | st3 | 1 | 185.05 F | 6.24 F | 205.48 F | 33.14 | 45.65 | no | no |
| displacement_exceeds_patch | 2x6 | 0 | st1 | 2 | 0.89 | 0.13 | 0.94 | 0.95 | 0.22 | yes | yes |
| displacement_exceeds_patch | 2x6 | 1 | st6 | 0 | 408.05 F | 77.04 F | 166.89 F | 45.05 | 48.43 | no | no |
| displacement_exceeds_patch | 2x6 | 1 | st3 | 1 | 160.74 F | 17.67 F | 122.61 F | 16.01 | 35.18 | no | no |
| displacement_exceeds_patch | 2x6 | 1 | st1 | 2 | 0.66 | 0.18 | 0.62 | 0.95 | 0.22 | yes | yes |
| displacement_exceeds_patch | 2x6 | 2 | st6 | 0 | 394.41 F | 128.32 F | 423.87 F | 65.01 | 95.35 | no | no |
| displacement_exceeds_patch | 2x6 | 2 | st3 | 1 | 200.27 F | 60.95 F | 233.27 F | 59.23 | 49.21 | no | no |
| displacement_exceeds_patch | 2x6 | 2 | st1 | 2 | 0.59 | 0.11 | 0.51 | 0.99 | 0.19 | yes | yes |
| displacement_exceeds_patch | 3x4 | 0 | st4 | 0 | 360.10 F | 145.69 F | 124.44 F | 53.90 | 39.07 | no | no |
| displacement_exceeds_patch | 3x4 | 0 | st2 | 1 | 121.37 F | 5.49 F | 188.76 F | 17.94 | 37.38 | no | no |
| displacement_exceeds_patch | 3x4 | 0 | st1 | 2 | 90.48 F | 0.48 | 29.91 F | 2.02 | 4.71 | no | no |
| displacement_exceeds_patch | 3x4 | 1 | st4 | 0 | 275.27 F | 78.30 F | 150.35 F | 51.14 | 45.16 | no | no |
| displacement_exceeds_patch | 3x4 | 1 | st2 | 1 | 168.69 F | 16.67 F | 112.04 F | 14.06 | 28.00 | no | no |
| displacement_exceeds_patch | 3x4 | 1 | st1 | 2 | 42.41 F | 0.44 | 0.67 | 2.00 | 0.25 | no | no |
| displacement_exceeds_patch | 3x4 | 2 | st4 | 0 | 412.47 F | 125.44 F | 352.63 F | 41.93 | 110.52 | no | no |
| displacement_exceeds_patch | 3x4 | 2 | st2 | 1 | 127.72 F | 59.50 F | 155.80 F | 52.97 | 34.43 | no | no |
| displacement_exceeds_patch | 3x4 | 2 | st1 | 2 | 30.13 F | 0.37 | 0.33 | 2.06 | 0.13 | no | no |
| displacement_exceeds_patch | 4x3 | 0 | st3 | 0 | 162.45 F | 179.92 F | 155.45 F | 57.46 | 45.70 | no | no |
| displacement_exceeds_patch | 4x3 | 0 | st1 | 1 | 83.76 F | 1.33 F | 110.10 F | 7.02 | 18.61 | no | no |
| displacement_exceeds_patch | 4x3 | 1 | st3 | 0 | 354.13 F | 85.11 F | 333.46 F | 61.54 | 84.23 | no | no |
| displacement_exceeds_patch | 4x3 | 1 | st1 | 1 | 124.77 F | 1.30 F | 175.78 F | 3.40 | 39.61 | no | no |
| displacement_exceeds_patch | 4x3 | 2 | st3 | 0 | 234.39 F | 204.97 F | 402.31 F | 67.44 | 93.44 | no | no |
| displacement_exceeds_patch | 4x3 | 2 | st1 | 1 | 115.63 F | 23.79 F | 151.16 F | 15.21 | 23.55 | no | no |
| midline_jitter | 0.5 | 0 | st1 | 0 | 0.50 | 0.37 | 5.80 F | 0.42 | 0.24 | no | yes |
| midline_jitter | 0.5 | 0 | st1_mslight | 1 | 0.53 | 1.03 F | 4.10 F | 0.44 | 0.22 | no | yes |
| midline_jitter | 0.5 | 0 | st1_msstrong | 1 | 1.02 | 2.93 F | 1.70 | 0.60 | 0.32 | no | yes |
| midline_jitter | 0.5 | 1 | st1 | 0 | 0.60 | 1.05 F | 4.16 F | 0.41 | 0.23 | no | yes |
| midline_jitter | 0.5 | 1 | st1_mslight | 1 | 0.69 | 1.00 | 2.43 | 0.43 | 0.31 | yes | yes |
| midline_jitter | 0.5 | 1 | st1_msstrong | 1 | 0.90 | 2.98 F | 1.27 | 0.59 | 0.21 | no | yes |
| midline_jitter | 0.5 | 2 | st1 | 0 | 0.86 | 1.16 F | 4.51 F | 0.42 | 0.19 | no | yes |
| midline_jitter | 0.5 | 2 | st1_mslight | 1 | 0.52 | 1.06 F | 1.84 | 0.44 | 0.20 | no | yes |
| midline_jitter | 0.5 | 2 | st1_msstrong | 1 | 1.06 | 3.07 F | 1.01 | 0.59 | 0.16 | no | yes |
| midline_jitter | 1 | 0 | st1 | 0 | 0.49 | 0.73 | 11.46 F | 0.44 | 0.34 | no | yes |
| midline_jitter | 1 | 0 | st1_mslight | 1 | 0.65 | 1.16 F | 7.76 F | 0.44 | 0.26 | no | yes |
| midline_jitter | 1 | 0 | st1_msstrong | 1 | 0.96 | 2.94 F | 2.52 | 0.60 | 0.23 | no | yes |
| midline_jitter | 1 | 1 | st1 | 0 | 0.62 | 2.09 F | 8.34 F | 0.41 | 0.28 | no | yes |
| midline_jitter | 1 | 1 | st1_mslight | 1 | 0.78 | 1.00 | 4.81 F | 0.43 | 0.33 | no | yes |
| midline_jitter | 1 | 1 | st1_msstrong | 1 | 0.83 | 3.06 F | 2.26 | 0.60 | 0.26 | no | yes |
| midline_jitter | 1 | 2 | st1 | 0 | 0.86 | 2.30 F | 8.60 F | 0.42 | 0.21 | no | yes |
| midline_jitter | 1 | 2 | st1_mslight | 1 | 0.58 | 1.20 F | 3.71 F | 0.44 | 0.22 | no | yes |
| midline_jitter | 1 | 2 | st1_msstrong | 1 | 0.93 | 3.33 F | 1.98 | 0.59 | 0.20 | no | yes |
| midline_jitter | 2 | 0 | st1 | 0 | 0.78 | 1.49 F | 23.65 F | 0.54 | 0.50 | no | no |
| midline_jitter | 2 | 0 | st1_mslight | 1 | 0.53 | 1.55 F | 14.65 F | 0.48 | 0.35 | no | yes |
| midline_jitter | 2 | 0 | st1_msstrong | 1 | 1.08 | 2.95 F | 5.74 F | 0.63 | 0.23 | no | yes |
| midline_jitter | 2 | 1 | st1 | 0 | 0.77 | 4.15 F | 17.10 F | 0.41 | 0.39 | no | yes |
| midline_jitter | 2 | 1 | st1_mslight | 1 | 0.82 | 0.99 | 9.76 F | 0.43 | 0.39 | no | yes |
| midline_jitter | 2 | 1 | st1_msstrong | 1 | 0.81 | 3.36 F | 3.98 F | 0.60 | 0.27 | no | yes |
| midline_jitter | 2 | 2 | st1 | 0 | 0.55 | 4.45 F | 16.97 F | 0.42 | 0.33 | no | yes |
| midline_jitter | 2 | 2 | st1_mslight | 1 | 0.59 | 1.65 F | 7.81 F | 0.45 | 0.26 | no | yes |
| midline_jitter | 2 | 2 | st1_msstrong | 1 | 1.03 | 4.24 F | 4.03 F | 0.60 | 0.21 | no | yes |
| midline_jitter | 3 | 0 | st1 | 0 | 0.58 | 2.24 F | 35.34 F | 0.80 | 0.76 | no | no |
| midline_jitter | 3 | 0 | st1_mslight | 1 | 0.84 | 2.02 F | 21.95 F | 0.56 | 0.42 | no | yes |
| midline_jitter | 3 | 0 | st1_msstrong | 1 | 0.75 | 2.98 F | 8.79 F | 0.68 | 0.37 | no | yes |
| midline_jitter | 3 | 1 | st1 | 0 | 0.78 | 6.18 F | 25.90 F | 0.42 | 0.49 | no | yes |
| midline_jitter | 3 | 1 | st1_mslight | 1 | 0.70 | 0.96 | 14.69 F | 0.43 | 0.43 | no | yes |
| midline_jitter | 3 | 1 | st1_msstrong | 1 | 0.96 | 3.82 F | 5.59 F | 0.60 | 0.32 | no | yes |
| midline_jitter | 3 | 2 | st1 | 0 | 0.67 | 6.83 F | 26.36 F | 0.42 | 0.50 | no | no |
| midline_jitter | 3 | 2 | st1_mslight | 1 | 0.53 | 2.19 F | 11.50 F | 0.45 | 0.35 | no | yes |
| midline_jitter | 3 | 2 | st1_msstrong | 1 | 0.85 | 5.43 F | 6.00 F | 0.61 | 0.30 | no | yes |
| low_texture | 0.06 | 0 | st1 | 0 | 35.56 F | 1.10 F | 39.67 F | 3.71 | 13.21 | no | no |
| low_texture | 0.06 | 0 | st1_r22 | 1 | 19.57 F | 0.63 | 18.44 F | 2.68 | 6.51 | no | no |
| low_texture | 0.06 | 0 | st1_r30 | 1 | 18.45 F | 0.99 | 21.77 F | 2.69 | 6.64 | no | no |
| low_texture | 0.06 | 1 | st1 | 0 | 41.18 F | 1.68 F | 29.23 F | 5.38 | 11.30 | no | no |
| low_texture | 0.06 | 1 | st1_r22 | 1 | 26.01 F | 0.59 | 19.90 F | 4.08 | 7.28 | no | no |
| low_texture | 0.06 | 1 | st1_r30 | 1 | 15.29 F | 0.20 | 21.74 F | 3.19 | 5.33 | no | no |
| low_texture | 0.06 | 2 | st1 | 0 | 30.45 F | 1.20 F | 30.64 F | 4.72 | 10.61 | no | no |
| low_texture | 0.06 | 2 | st1_r22 | 1 | 22.42 F | 0.24 | 27.97 F | 4.13 | 8.90 | no | no |
| low_texture | 0.06 | 2 | st1_r30 | 1 | 16.70 F | 0.47 | 15.98 F | 4.64 | 5.63 | no | no |
| low_texture | 0.1 | 0 | st1 | 0 | 10.34 F | 0.74 | 10.13 F | 2.04 | 3.78 | no | no |
| low_texture | 0.1 | 0 | st1_r22 | 1 | 8.24 F | 0.61 | 10.41 F | 1.35 | 3.18 | no | no |
| low_texture | 0.1 | 0 | st1_r30 | 1 | 7.49 F | 0.43 | 7.96 F | 1.28 | 2.56 | no | no |
| low_texture | 0.1 | 1 | st1 | 0 | 17.87 F | 0.46 | 9.67 F | 2.54 | 2.97 | no | no |
| low_texture | 0.1 | 1 | st1_r22 | 1 | 10.18 F | 0.34 | 4.69 F | 1.44 | 2.11 | no | no |
| low_texture | 0.1 | 1 | st1_r30 | 1 | 7.51 F | 0.08 | 4.59 F | 1.30 | 1.94 | no | no |
| low_texture | 0.1 | 2 | st1 | 0 | 10.21 F | 0.32 | 12.81 F | 3.39 | 4.88 | no | no |
| low_texture | 0.1 | 2 | st1_r22 | 1 | 6.29 F | 0.11 | 9.03 F | 2.51 | 3.35 | no | no |
| low_texture | 0.1 | 2 | st1_r30 | 1 | 6.28 F | 0.39 | 7.93 F | 2.14 | 2.55 | no | no |
| low_texture | 0.15 | 0 | st1 | 0 | 4.59 F | 0.49 | 4.91 F | 1.11 | 2.06 | no | no |
| low_texture | 0.15 | 0 | st1_r22 | 1 | 3.60 F | 0.34 | 3.84 F | 0.83 | 1.51 | no | no |
| low_texture | 0.15 | 0 | st1_r30 | 1 | 2.37 F | 0.31 | 3.03 | 0.92 | 1.32 | no | no |
| low_texture | 0.15 | 1 | st1 | 0 | 8.31 F | 0.27 | 3.57 F | 1.30 | 1.47 | no | no |
| low_texture | 0.15 | 1 | st1_r22 | 1 | 4.51 F | 0.20 | 2.50 | 0.84 | 1.13 | no | no |
| low_texture | 0.15 | 1 | st1_r30 | 1 | 3.19 F | 0.08 | 2.41 | 0.90 | 1.07 | no | no |
| low_texture | 0.15 | 2 | st1 | 0 | 5.93 F | 0.14 | 7.87 F | 1.83 | 2.56 | no | no |
| low_texture | 0.15 | 2 | st1_r22 | 1 | 4.37 F | 0.11 | 5.31 F | 1.33 | 1.70 | no | no |
| low_texture | 0.15 | 2 | st1_r30 | 1 | 2.97 F | 0.26 | 3.72 F | 1.19 | 1.26 | no | no |
| low_texture | 0.03 | 0 | st1 | 0 | 255.39 F | 5.51 F | 157.29 F | 16.14 | 53.55 | no | no |
| low_texture | 0.03 | 0 | st1_r22 | 1 | 88.59 F | 0.63 | 66.46 F | 11.80 | 24.01 | no | no |
| low_texture | 0.03 | 0 | st1_r30 | 1 | 64.55 F | 2.66 F | 56.81 F | 8.06 | 22.85 | no | no |
| low_texture | 0.03 | 1 | st1 | 0 | 191.33 F | 4.92 F | 121.07 F | 21.53 | 42.57 | no | no |
| low_texture | 0.03 | 1 | st1_r22 | 1 | 85.00 F | 2.87 F | 81.46 F | 13.46 | 22.44 | no | no |
| low_texture | 0.03 | 1 | st1_r30 | 1 | 57.01 F | 1.06 F | 40.32 F | 12.66 | 18.10 | no | no |
| low_texture | 0.03 | 2 | st1 | 0 | 151.85 F | 4.50 F | 130.26 F | 22.45 | 39.01 | no | no |
| low_texture | 0.03 | 2 | st1_r22 | 1 | 131.44 F | 1.28 F | 131.50 F | 11.20 | 32.69 | no | no |
| low_texture | 0.03 | 2 | st1_r30 | 1 | 104.68 F | 0.60 | 72.21 F | 12.96 | 25.08 | no | no |
| width_change | None | 0 | st1 | 0 | 1.06 | 0.07 | 4.30 F | 0.40 | 0.32 | no | yes |
| width_change | None | 0 | st1_wf | 1 | 1.06 | 0.07 | 4.30 skip | 0.40 | 0.32 | yes | yes |
| width_change | None | 1 | st1 | 0 | 0.44 | 0.10 | 3.43 F | 0.43 | 0.25 | no | yes |
| width_change | None | 1 | st1_wf | 1 | 0.44 | 0.10 | 3.43 skip | 0.43 | 0.25 | yes | yes |
| width_change | None | 2 | st1 | 0 | 0.76 | 0.08 | 3.55 F | 0.42 | 0.26 | no | yes |
| width_change | None | 2 | st1_wf | 1 | 0.76 | 0.08 | 3.55 skip | 0.42 | 0.26 | yes | yes |
