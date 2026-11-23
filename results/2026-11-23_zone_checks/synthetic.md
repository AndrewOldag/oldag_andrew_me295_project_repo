# Synthetic detection, freeze v4 rods (seeds 26-28)

Thresholds (`config/zone_thresholds.yaml`): plateau_regr 8.5, plateau_speed 0.018, pp_rms_rel 0.0044, pp_max_rel 0.0063

| Set | Shift px | Records | plateau flags | particle_path flags | either |
| :-- | --: | --: | --: | --: | --: |
| accept_clean (threshold set) | 0 | 18 | 0 of 18 | 0 of 15 | 0 of 18 |
| shifted | -60 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| shifted | -30 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| shifted | -15 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| shifted | +15 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| shifted | +30 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| shifted | +60 | 15 | 0 of 15 | 15 of 15 | 15 of 15 |
| accept_repaired (not in the threshold set) | 0 | 9 | 0 of 9 | 0 of 9 | 0 of 9 |

- Counts read `flagged of computable`. `plateau_speed` and the relative particle-path values are not computable on `v3_still` (no growth); its `plateau_regr` is
