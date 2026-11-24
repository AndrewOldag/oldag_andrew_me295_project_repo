# Reference thresholds (proposal step 5), waiting for Andrew's approval

Labels: 150 windows, 130 clean, 20 not clean (Andrew).
Rule: 99.5th percentile over the clean windows (numpy linear) x 1.5, rounded up to 2 significant figures.

| Value | 99.5th pct (clean) | Threshold | clean over | not clean over | clean range | not clean range |
| :-- | --: | --: | --: | --: | :-- | :-- |
| `pp_shape_rel` | 0.08715 | 0.14 | 0 of 130 | 1 of 20 | 0.00801-0.115 | 0.0089-0.212 |
| `pp_common_rel` | 0.3291 | 0.5 | 1 of 130 | 0 of 20 | 2.26e-06-0.628 | 1.48e-05-0.299 |

Not clean windows over either threshold: 0708_m9__w22-24

For information, synthetic set (synthetic.csv) at the shape threshold, flagged of computable:
- accept_clean +0 px: 0 of 15
- shifted -60 px: 15 of 15
- shifted -30 px: 0 of 15
- shifted -15 px: 0 of 15
- shifted +15 px: 0 of 15
- shifted +30 px: 0 of 15
- shifted +60 px: 15 of 15
- accept_repaired +0 px: 0 of 9

Not written to config until Andrew approves (then `config/zone_reference_thresholds.yaml`).
