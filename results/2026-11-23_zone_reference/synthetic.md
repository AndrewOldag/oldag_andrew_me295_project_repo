# Synthetic re-run with the residual split (freeze v4, seeds 26-28)

Synthetic shape threshold (R4 rule on the 18 clean tracks, this test only): `pp_shape_rel` 0.0019

| Set | Shift px | Records | shape flags | `pp_shape_rel` range | common share of squared residual (median) |
| :-- | --: | --: | --: | :-- | --: |
| accept_clean (threshold set) | 0 | 18 | 0 of 15 | 0.00113-0.00124 | 0.60 |
| shifted | -60 | 15 | 15 of 15 | 0.176-0.176 | 0.43 |
| shifted | -30 | 15 | 15 of 15 | 0.0902-0.0904 | 0.41 |
| shifted | -15 | 15 | 15 of 15 | 0.0454-0.0456 | 0.40 |
| shifted | +15 | 15 | 15 of 15 | 0.0451-0.0453 | 0.44 |
| shifted | +30 | 15 | 15 of 15 | 0.0897-0.09 | 0.44 |
| shifted | +60 | 15 | 15 of 15 | 0.174-0.175 | 0.45 |
| accept_repaired (not in the threshold set) | 0 | 9 | 0 of 9 | 0.00114-0.00129 | 0.55 |

Stop rule (proposal): shape flags 15 of 15 at every shift: met
