# Held-out sizes at v3 geometry

Sizing seeds 10, 11, 12, checker only. Rule (v2): the smallest tested size at which the checker fails 3 of 3.

| Fault | v2 size | Size | Seeds failing | rigid_invariance | closure | plane_sections | REGR err |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| bad_stage_correction | 3 | 3 | 3 of 3 | 0.65-0.92 | 2.81-2.92 | 0.39-0.88 | 0.32-0.35 |
| stage_log_missing | 1 | 1 | 3 of 3 | 0.64-0.92 | 95.81-95.92 | 0.38-0.88 | 0.32-0.35 |
| second_root | 30 | 30 | 3 of 3 | 0.65-0.92 | 0.09-0.20 | 7.83-13.23 | 0.50-0.60 |
| fast_rotation | 2 | 2 | 3 of 3 | 104.14-222.51 | 7.87-44.81 | 141.67-308.54 | 30.78-34.15 |
| flank_swap | 0.5 | 0.5 | 3 of 3 | 20.84-32.03 | 1.36-4.82 | 60.96-84.01 | 5.39-5.88 |
| partial_occlusion | 20 | 20 | 3 of 3 | 86.98-136.11 | 0.09-0.20 | 12.53-65.44 | 12.60-20.69 |

- Sizes: {'bad_stage_correction': '3', 'stage_log_missing': '1', 'second_root': '30', 'fast_rotation': '2', 'flank_swap': '0.5', 'partial_occlusion': '20'}
- Differ from v2: none
- Result: complete
