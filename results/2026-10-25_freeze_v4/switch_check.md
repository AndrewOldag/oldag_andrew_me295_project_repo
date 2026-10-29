# Freeze v4 candidate: switch check against freeze v3

From the v3 tracker cache and run records; no tracker runs, no LLM calls. `python scripts/synth/v4_replay_check.py`.

## Labels (51 rods)

| Switch | Rods | Label or sequence differs from v3 |
| :-- | --: | :-- |
| off | 51 | 0 |
| v4 | 51 | 3: v3_growth_zone_stage_log_missing_z1_s20 accept_repaired -> decline; v3_growth_zone_stage_log_missing_z1_s21 accept_repaired -> decline; v3_growth_zone_stage_log_missing_z1_s22 accept_repaired -> decline |

## Rule methods rerun from the cache

| Switch | Runs | Same outcome | Differ |
| :-- | --: | --: | :-- |
| off | 102 | 102 | none |
| v4 | 102 | 102 | none |

## LLM traces re-executed (request_info and apply_remedy results)

| Switch | Runs | Steps compared | Runs with a differing step | Wall (s) |
| :-- | --: | --: | :-- | --: |
| off | 306 | 1319 | 0 | 23 |
| v4 | 306 | 1319 | 0 | 24 |

Switch on: the C2 fields of stage_log_summary are removed before the comparison; every other result, check values included, must be equal.

