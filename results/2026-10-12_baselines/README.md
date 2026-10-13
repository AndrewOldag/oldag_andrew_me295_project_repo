# Non-LLM baselines on the development faults, 2026-10-12

Task: fixed-parameter script and rule-based remedy tree, scored like the agent. Tree fixed in `docs/proposals/2026-10-12_remedy-tree.md` (commit ea95149 on wip/baselines, before any run). Freeze: `docs/proposals/2026-10-11_freeze-v1.md` (proposed, not yet approved).

## Files
- `table.md`: outcome per fault and method, totals, per task
- `scores.json`: one row per task
- `runs/`: trace and summary per task (`<method>_<fault>[_z<size>]_s<seed>`)
- Commands: `python scripts/synth/baselines.py next|status|fetch` per round, `python scripts/synth/baselines.py write --out results/2026-10-12_baselines/runs`, then `python scripts/synth/eval_baselines.py --runs results/2026-10-12_baselines/runs --agent-runs results/2026-10-11c_world_smoothing_freeze/diagnostician --out results/2026-10-12_baselines`

## Sweeps (shared-machine limits; one sweep per round through the lock)
| Round | Runs | Failed | Wall (s) | Load 1 min before / max during / after | Peak workers | Work space (GB) |
| --: | --: | --: | --: | :-- | --: | :-- |
| 1 | 30 | 0 | 91 | 0.75 / 3.95 / 3.87 | 4 | 5.67 -> 5.81 |
| 2 | 30 | 0 | 136 | 2.24 / 4.55 / 4.46 | 4 | 5.81 -> 5.82 |
| 3 | 18 | 0 | 67 | 3.40 / 4.15 / 4.04 | 4 | 5.82 -> 5.82 |
| 4 | 18 | 0 | 98 | 3.25 / 4.74 / 4.47 | 4 | 5.82 -> 5.83 |
| 5 | 12 | 0 | 80 | 3.84 / 5.03 / 4.80 | 4 | 5.83 -> 5.83 |

- 108 tracker runs, 0 failed, 472 s sweep wall time, 32 cores. No other sweep held the lock at any round start

## Result (seeds 0-2; diagnostician seed 0 only, runs of 2026-10-11)
| Fault | Correct outcome | Script | Remedy tree | Diagnostician (s0) |
| :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch 2x6 | accept after the remedy | 3 false_accept | 3 good_report | not_reported |
| width_change 1/400 | accept with the width-free ratio | 3 good_report | 3 good_report | unnecessary_decline |
| rigid_drift 0.5 | accept after the remedy | 3 good_report | 3 good_report | unnecessary_decline |
| low_texture 0.03 | decline | 3 false_accept | 3 correct_decline | correct_decline |
| midline_jitter 3 | decline | 2 false_accept, 1 good_report | 3 correct_decline | not_reported |

- Correct: script 6 of 15, remedy tree 15 of 15, diagnostician 1 of 5
- Tree: 57 steps, 42 remedies applied, 20 roll backs, no step limit reached (most steps 5)
- Fault named in the last remedy or decline: tree 15 of 15, diagnostician 1 of 5 (midline_jitter, a step-limit run). The build log of 2026-10-11 gives 0 of 5 for the same runs; the 1 here is `diagnosis_correct` applied to the last `apply_remedy`, which the earlier count did not use

## Notes on the scoring (not changed)
- `outcome_category` scores an accept by the measurement only. The script accepts with checks failing; on width_change (plane_sections fails) and rigid_drift (closure fails) its base measurement is within tolerance, so these score good_report. Base centre RMS 0.40-0.45 %/h on both, under the 1.085 limit
- midline_jitter script s1 is good_report (flank RMS 0.495 against 0.5 %/h); the freeze outcome is decline, so it counts as not correct. s0 (0.757) and s2 (0.501) are false accepts at the 0.5 %/h flank tolerance; at 1.00 %/h (open item 1 of the freeze) all three would be good_report
- Tree midline_jitter: `smooth_midline` light was kept on all 3 seeds (a check lowered by a quarter) but checks still failed, so the tree declined. The measurement after smoothing is within tolerance on s1 and s2 (flank 0.469, 0.382) and not on s0 (0.531)
- The tree names faults by its own list, and the dev faults each have one remedy in the lists, so its fault-naming score follows from the list order and is not a test of diagnosis
- The diagnostician column is the 5 runs of 2026-10-11 (low_texture made before the roll-back fix), rescored here with the same code; categories match the 2026-10-11 table on 5 of 5; truth from `staging/tracks_baselines/` (same rod ids)
