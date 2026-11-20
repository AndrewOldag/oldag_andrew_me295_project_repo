# Novel-fault sizes

Sizing seeds 50, 51, unremedied, v3_growth_zone. Rule: the smallest candidate at which the checker fails on both seeds; else the largest candidate.

| Fault | Size | Seed | rigid_invariance | closure | plane_sections | REGR err (limit) | All pass | Good |
| :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |
| focus_drift | 3 | 50 | 2.00 | 1.23 F | 8.22 F | 2.03 (1.35) | no | no |
| focus_drift | 3 | 51 | 2.61 F | 0.38 | 6.36 F | 1.21 (1.35) | no | no |
| focus_drift | 6 | 50 | 23.42 F | 2.33 F | 44.48 F | 11.59 (1.35) | no | no |
| focus_drift | 6 | 51 | 9.55 F | 2.08 F | 48.32 F | 5.14 (1.35) | no | no |
| illumination_flicker | 0.1 | 50 | 7.00 F | 2.44 F | 22.02 F | 3.57 (1.35) | no | no |
| illumination_flicker | 0.1 | 51 | 11.86 F | 2.69 F | 41.74 F | 4.12 (1.35) | no | no |
| illumination_flicker | 0.3 | 50 | 365.28 F | 3.26 F | 278.01 F | 51.06 (1.35) | no | no |
| illumination_flicker | 0.3 | 51 | 249.96 F | 4.29 F | 323.46 F | 59.78 (1.35) | no | no |

- Sizes: {'focus_drift': '3', 'illumination_flicker': '0.1'}
