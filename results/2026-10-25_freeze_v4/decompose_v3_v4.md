# Freeze v3 to v4: relabelling against agent change

v4 changes the agents (C1 prompt map, C2 stage-log spread) and the label rule (C3 option a: a check that cannot be computed after a remedy fails). C3 (a) moves the stage_log_missing rows from accept_repaired to decline (3 v3 rods: v3_growth_zone_stage_log_missing_z1_s20, v3_growth_zone_stage_log_missing_z1_s21, v3_growth_zone_stage_log_missing_z1_s22). Every method declined those rods in v3, so part of the v3 to v4 difference is relabelling, with no change in agent behaviour.

- Relabelling alone: v3 runs, v3 labels -> v3 runs, C3 (a) labels (same runs, same seeds)
- Agent change and new seeds: v3 runs, C3 (a) labels -> v4 runs, v4 labels (same label rule)
- Unchanged rows: every row except stage_log_missing; the label rule is the same there in v3 and v4
- v3 seeds 20-22, v4 seeds 26-28: the agent-change columns compare different rod draws, not paired runs
- LLM methods: mean over 3 repeats. `python scripts/synth/scored_v4.py decompose`

| Column | Rods |
| :-- | :-- |
| v3 runs, v3 labels | 51 (accept_clean 18, accept_repaired 12, decline 21) |
| v3 runs, C3 (a) labels | 51 (accept_clean 18, accept_repaired 9, decline 24) |
| v4 runs, v4 labels | 51 (accept_clean 18, accept_repaired 9, decline 24) |
| v3 runs, unchanged rows | 48 (accept_clean 18, accept_repaired 9, decline 21) |
| v4 runs, unchanged rows | 48 (accept_clean 18, accept_repaired 9, decline 21) |

## Balanced accuracy

| Method | v3 runs, v3 labels | v3 runs, C3 (a) labels | v4 runs, v4 labels | v3 runs, unchanged rows | v4 runs, unchanged rows |
| :-- | --: | --: | --: | --: | --: |
| script | 0.67 | 0.67 | 0.67 | 0.67 | 0.67 |
| remedy_tree | 0.81 | 0.90 | 0.93 | 0.89 | 0.92 |
| diagnostician | 0.69 (0.69-0.69) | 0.75 (0.75-0.75) | 0.93 (0.92-0.94) | 0.74 (0.74-0.74) | 0.92 (0.90-0.94) |
| single_agent | 0.60 (0.57-0.64) | 0.65 (0.60-0.69) | 0.63 (0.58-0.69) | 0.67 (0.62-0.71) | 0.64 (0.59-0.69) |
| all_decline | 0.33 | 0.33 | 0.33 | 0.33 | 0.33 |

## Overall accuracy

| Method | v3 runs, v3 labels | v3 runs, C3 (a) labels | v4 runs, v4 labels | v3 runs, unchanged rows | v4 runs, unchanged rows |
| :-- | --: | --: | --: | --: | --: |
| script | 0.59 | 0.53 | 0.53 | 0.56 | 0.56 |
| remedy_tree | 0.80 | 0.86 | 0.90 | 0.85 | 0.90 |
| diagnostician | 0.72 (0.71-0.73) | 0.78 (0.76-0.78) | 0.90 (0.88-0.92) | 0.76 (0.75-0.77) | 0.90 (0.88-0.92) |
| single_agent | 0.59 (0.57-0.63) | 0.59 (0.57-0.63) | 0.51 (0.47-0.57) | 0.62 (0.60-0.67) | 0.54 (0.50-0.60) |
| all_decline | 0.41 | 0.47 | 0.47 | 0.44 | 0.44 |

## Accuracy, accept_repaired

| Method | v3 runs, v3 labels | v3 runs, C3 (a) labels | v4 runs, v4 labels | v3 runs, unchanged rows | v4 runs, unchanged rows |
| :-- | --: | --: | --: | --: | --: |
| script | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| remedy_tree | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 |
| diagnostician | 0.44 (0.42-0.50) | 0.59 (0.56-0.67) | 1.00 | 0.59 (0.56-0.67) | 1.00 |
| single_agent | 0.61 (0.50-0.67) | 0.81 (0.67-0.89) | 0.96 (0.89-1.00) | 0.81 (0.67-0.89) | 0.96 (0.89-1.00) |
| all_decline | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Accuracy, decline

| Method | v3 runs, v3 labels | v3 runs, C3 (a) labels | v4 runs, v4 labels | v3 runs, unchanged rows | v4 runs, unchanged rows |
| :-- | --: | --: | --: | --: | --: |
| script | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| remedy_tree | 0.67 | 0.71 | 0.79 | 0.67 | 0.76 |
| diagnostician | 0.71 (0.67-0.76) | 0.75 (0.71-0.79) | 0.79 (0.75-0.83) | 0.71 (0.67-0.76) | 0.76 (0.71-0.81) |
| single_agent | 0.43 (0.33-0.48) | 0.38 (0.29-0.42) | 0.10 (0.04-0.17) | 0.43 (0.33-0.48) | 0.11 (0.05-0.19) |
| all_decline | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## False accepts per repeat

| Method | v3 runs, v3 labels | v3 runs, C3 (a) labels | v4 runs, v4 labels | v3 runs, unchanged rows | v4 runs, unchanged rows |
| :-- | --: | --: | --: | --: | --: |
| script | 18.0 | 18.0 | 18.0 | 18.0 | 18.0 |
| remedy_tree | 4.0 | 4.0 | 2.0 | 4.0 | 2.0 |
| diagnostician | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| single_agent | 0.0 | 0.0 | 0.3 (0.0-1.0) | 0.0 | 0.3 (0.0-1.0) |
