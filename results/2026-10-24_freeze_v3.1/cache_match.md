# Cache-match test: workstation against the v3 lab-server outputs

Inbox freeze-v31 item 7, 2026-10-24. One bent rod and one fault rod from the v3 cache, rendered and tracked (state st1) on the workstation with the course code of this branch (95764c7; render and tracker-wrapper code unchanged since tag `freeze-v3`). Limit: render byte-identical; tracks within 1e-6 px.

| Rod | Render files (workstation, lab server) | Render identical | Max abs difference, all numeric arrays | Largest in | Other differences |
| :-- | :-- | :-- | --: | :-- | :-- |
| v3_bend20_clean_s20 | 44, 44 | yes | 3.4e-13 | midline_world | run time in metadata only |
| v3_growth_zone_rigid_drift_z0.5_s20 | 44, 44 | yes | 2.9e-13 | qb_regr_left | run time in metadata only |

- Result: pass. Tracker run 4.6 and 4.3 s on the workstation (lab server 6.4 s for the bent rod)
- The 13 sizing runs done on the lab server before the move (sweep 1) stay in the cache
