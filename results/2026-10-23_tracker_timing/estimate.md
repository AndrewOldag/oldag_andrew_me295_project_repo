| Set | Settings per window | Core-hours | Lab-server wall h (4 workers) | Cluster $ |
| :-- | :-- | --: | --: | --: |
| (a) subset 16 roots x 24 h, tracker outputs cached across repeats | low (1) | 9 | 2 | $0.11 |
| (a) subset 16 roots x 24 h, tracker outputs cached across repeats | mid (3) | 27 | 7 | $0.32 |
| (a) subset 16 roots x 24 h, tracker outputs cached across repeats | high (10) | 88 | 22 | $1.06 |
| (a') subset, no cache, 3 repeats | low (1) | 27 | 7 | $0.32 |
| (a') subset, no cache, 3 repeats | mid (3) | 80 | 20 | $0.96 |
| (a') subset, no cache, 3 repeats | high (10) | 265 | 66 | $3.18 |
| (b) all 102 include-yes roots once, usable hours (2,374 h) | low (1) | 51 | 13 | $0.61 |
| (b) all 102 include-yes roots once, usable hours (2,374 h) | mid (3) | 153 | 38 | $1.84 |
| (b) all 102 include-yes roots once, usable hours (2,374 h) | high (10) | 510 | 127 | $6.12 |
| (b') 118 roots x 24 h once | low (1) | 65 | 16 | $0.78 |
| (b') 118 roots x 24 h once | mid (3) | 196 | 49 | $2.35 |
| (b') 118 roots x 24 h once | high (10) | 652 | 163 | $7.83 |

- Core-seconds per frame (midline + tracker, slower of 3 runs): 1.04
- Include-yes roots 102, usable hours 2,373.6, frames 88,585, 2 h windows 1,223
- Peak memory per job 4.0 GB; output per window 0.93 MB; output for (b) at 1 setting x 2 2.3 GB
- Cluster rate $0.012 per core-hour
