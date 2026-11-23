# Growth-zone placement checks on the c027 windows (report-only)

Thresholds `config/zone_thresholds.yaml`: plateau_regr 8.5, plateau_speed 0.018, pp_rms_rel 0.0044, pp_max_rel 0.0063
They gate nothing; no c027 outcome changes. `plateau_regr` values are not shown (basal strain rate)

## By outcome class

| Outcome | Track | windows | not computed | plateau flagged | plateau n/a | particle_path flagged | particle_path n/a | either flagged |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: |
| accepted | base | 1034 | 0 | 1017 | 0 | 1034 | 0 | 1034 |
| accepted after repair | accepted | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| accepted after repair | base | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| declined by agent | base | 85 | 0 | 84 | 1 | 84 | 1 | 84 |
| declined by rule | base | 58 | 0 | 3 | 55 | 0 | 58 | 3 |
| paused | base | 4 | 3 | 1 | 0 | 1 | 0 | 1 |
| step_limit | base | 6 | 0 | 6 | 0 | 6 | 0 | 6 |

## By condition

| Condition | Track | windows | not computed | plateau flagged | plateau n/a | particle_path flagged | particle_path n/a | either flagged |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: |
| (none) | base | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| control | base | 417 | 0 | 396 | 20 | 397 | 20 | 397 |
| control then control | base | 53 | 0 | 48 | 5 | 48 | 5 | 48 |
| mannitol | accepted | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| mannitol | base | 345 | 0 | 323 | 21 | 322 | 23 | 324 |
| mannitol then control | accepted | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| mannitol then control | base | 300 | 1 | 280 | 6 | 292 | 7 | 293 |
| mannitol then mannitol | base | 72 | 0 | 66 | 4 | 68 | 4 | 68 |

## Residuals, base tracks (median / 90th / 99th percentile)

| Value | Computed | Percentiles |
| :-- | --: | :-- |
| plateau_speed | 1097 | 0.0382 / 0.184 / 1.54 |
| pp_rms_px | 1127 | 3.54 / 22.3 / 131 |
| pp_max_px | 1127 | 9.76 / 38 / 176 |
| pp_rms_rel | 1127 | 0.0304 / 0.166 / 0.706 |
| pp_max_rel | 1127 | 0.0607 / 0.21 / 0.564 |
| abs pp_mean_px | 1127 | 1.83 / 20.4 / 125 |
| abs tip_offset_change_px | 1127 | 1.24 / 18.9 / 129 |

Common part: share of the squared mean residual in the squared RMS residual, median 0.27 over 1127 base tracks, 0.98 over the quarter with the largest `pp_rms_px`. Correlation of the mean residual with `tip_offset_change_px`: -1.00. Base tracks with `|tip_offset_change_px|` over 15 px (one patch spacing): 143 of 1127

## Example windows (base track; first 3 by id per group)

| Outcome | particle_path | plateau | Windows |
| :-- | :-- | :-- | :-- |
| accepted | flag | pass | 0711_m1__w14-16, 0714_c14__w10-12, 0721_m11__w14-16 (17) |
| accepted | flag | flag | 0708_c10__w10-12, 0708_c10__w12-14, 0708_c10__w14-16 (1017) |
| accepted after repair | flag | flag | 0714_m7__w18-20, 0721_m3__w4-6 (2) |
| declined by agent | n/a | n/a | 0721_c3__w2-4 (1) |
| declined by agent | flag | flag | 0708_c10__w0-2, 0708_c10__w2-4, 0708_c11__w0-2 (84) |
| declined by rule | n/a | n/a | 0708_c10__w20-22, 0708_c10__w22-24, 0708_c11__w18-20 (55) |
| declined by rule | n/a | flag | 0711_m3__w0-2, 0714_m9__w0-2, 0727_mc2__w0-2 (3) |
| paused | flag | flag | 0708_m9__w10-12 (1) |
| step_limit | flag | flag | 0708_c4__w0-2, 0708_m11__w0-2, 0708_m8__w0-2 (6) |
