# Particle-path zone check with the real reference thresholds, c027 windows (report-only)

Thresholds `config/zone_reference_thresholds.yaml` (Andrew, 2026-11-23): `pp_shape_rel` 0.14, `pp_common_rel` 0.5. shape: `pp_shape_rel` over its threshold (profile misplaced along s). common: `pp_common_rel` over its threshold (anchoring drift). They gate nothing; no c027 outcome changes. n/a: largest tracked displacement under 2 px (relative values not computable)

## By outcome class

| Outcome | Track | windows | not computed | shape flagged | shape n/a | common flagged | common n/a | either flagged |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: |
| accepted | base | 1034 | 0 | 3 | 0 | 5 | 0 | 8 |
| accepted after repair | accepted | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| accepted after repair | base | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| declined by agent | base | 85 | 0 | 1 | 1 | 10 | 1 | 11 |
| declined by rule | base | 58 | 0 | 0 | 58 | 0 | 58 | 0 |
| paused | base | 4 | 3 | 0 | 0 | 1 | 0 | 1 |
| step_limit | base | 6 | 0 | 0 | 0 | 1 | 0 | 1 |

## By condition

| Condition | Track | windows | not computed | shape flagged | shape n/a | common flagged | common n/a | either flagged |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: |
| (none) | base | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| control | base | 417 | 0 | 1 | 20 | 2 | 20 | 3 |
| control then control | base | 53 | 0 | 0 | 5 | 0 | 5 | 0 |
| mannitol | accepted | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| mannitol | base | 345 | 0 | 2 | 23 | 8 | 23 | 10 |
| mannitol then control | accepted | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| mannitol then control | base | 300 | 1 | 1 | 7 | 1 | 7 | 2 |
| mannitol then mannitol | base | 72 | 0 | 0 | 4 | 6 | 4 | 6 |

## Relative residuals, base tracks (median / 90th / 99th percentile)

| Value | Computed | Percentiles |
| :-- | --: | :-- |
| pp_shape_rel | 1127 | 0.016 / 0.0371 / 0.0943 |
| pp_common_rel | 1127 | 0.0138 / 0.163 / 0.705 |

## Example windows (base track; first 3 by id per group)

| Outcome | shape | common | Windows |
| :-- | :-- | :-- | :-- |
| accepted | flag | pass | 0708_c2__w0-2, 0708_m8__w8-10, 0708_m9__w22-24 (3) |
| accepted | pass | flag | 0714_m1__w22-23.89, 0727_mm6__w10-12, 0727_mm6__w14-16 (5) |
| accepted | pass | pass | 0708_c10__w10-12, 0708_c10__w12-14, 0708_c10__w14-16 (1026) |
| accepted after repair | pass | pass | 0714_m7__w18-20, 0721_m3__w4-6 (2) |
| declined by agent | flag | pass | 0721_m11__w22-24 (1) |
| declined by agent | n/a | n/a | 0721_c3__w2-4 (1) |
| declined by agent | pass | flag | 0708_m11__w2-4, 0708_m6__w14-16, 0708_m8__w18-20 (10) |
| declined by agent | pass | pass | 0708_c10__w0-2, 0708_c10__w2-4, 0708_c11__w0-2 (73) |
| declined by rule | n/a | n/a | 0708_c10__w20-22, 0708_c10__w22-24, 0708_c11__w18-20 (58) |
| paused | pass | flag | 0708_m9__w10-12 (1) |
| step_limit | pass | flag | 0721_m4__w0-2 (1) |
| step_limit | pass | pass | 0708_c4__w0-2, 0708_m11__w0-2, 0708_m8__w0-2 (5) |
