# Scored runs v1, 2026-10-12

Spec `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md`, items 5-7. Freeze tag `freeze-v2` (5b64897). Every run records the freeze tag and commit c9d5a0c (harness; no prompt, threshold or tool change after it). Claude Code 2.1.293, model and step limit as in freeze v2.

## Files
- `table_dev.md`, `table_heldout.md`: method x fault table, totals per method, one row per run
- `scores.json`: one record per run (method, fault, seed, label, status, category, fault named, steps, remedies, roll backs, tokens in and out, call time, freeze tag, commit)
- `dev/`, `heldout/`: trace and summary per run, `<method>_<fault>[_z<size>]_s<seed>`
- Commands: `python scripts/synth/scored_v1.py next --set dev|heldout`, `status`, `fetch` (repeat until nothing is needed), `rules --set S`, `agents --set S --method diagnostician|single_agent`, `eval`

## Runs
- Development: five faults at their frozen sizes, seeds 1-5. Held-out: five faults at the approved sizes, seeds 0-2
- Four methods: fixed script, remedy tree, diagnostician, single agent (`docs/proposals/2026-10-12_single-agent-baseline.md`). 160 runs; 80 agent runs (50 development, 30 held-out)
- Harness errors: 0 of 80. Orchestrator `error` outcomes: 0
- Labels: development from freeze v2 (seeds 0-5); held-out from `results/2026-10-12b_heldout_labels/` (committed before any agent run)
- Correct: good_report on a repairable rod, correct_decline on a not-repairable rod. Held-out fault names counted correct: own name; flank_swap `unknown`; partial_occlusion `low_texture` or `unknown`
- Terminal fault: the fault in the last `apply_remedy` or `decline`. The script names none

## Tracker runs
- Cache: this spec's `staging/tracks_scored_v1` plus the 2026-10-12 caches (baselines, seeds 3-5, held-out sizes and labels). No run from before 2026-10-12 is reused
- Rule methods: 9 sweep rounds, 96 tracker runs, 0 failed, 445 s sweep wall time; load (1 min) at most 4.73 on 32 cores; work space 7.30 -> 7.52 GB
- Agent runs: 22 further tracker runs as single load-checked jobs at lowest priority
- Spec total with the label sweep: 202 tracker runs, 657 s sweep wall time

## Development faults, seeds 1-5
Cells: correct outcomes / false accepts / unnecessary declines / terminal fault correct, each of 5.

| Fault | Label | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch | repairable | 0 / 5 / 0 / 0 | 4 / 0 / 1 / 5 | 5 / 0 / 0 / 5 | 0 / 0 / 1 / 3 |
| width_change | repairable | 5 / 0 / 0 / 0 | 5 / 0 / 0 / 5 | 5 / 0 / 0 / 5 | 5 / 0 / 0 / 5 |
| rigid_drift | repairable | 5 / 0 / 0 / 0 | 5 / 0 / 0 / 5 | 5 / 0 / 0 / 5 | 1 / 0 / 0 / 0 |
| low_texture | not repairable | 0 / 5 / 0 / 0 | 5 / 0 / 0 / 5 | 5 / 0 / 0 / 5 | 5 / 0 / 0 / 5 |
| midline_jitter | not repairable | 0 / 0 / 0 / 0 | 5 / 0 / 0 / 3 | 4 / 0 / 0 / 4 | 0 / 0 / 0 / 5 |

| Method | Runs | Correct | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | Terminal fault correct |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| script | 25 | 10 | 15 | 10 | 0 | 0 | 0 | 0 |
| remedy_tree | 25 | 24 | 14 | 0 | 10 | 1 | 0 | 23 |
| diagnostician | 25 | 24 | 15 | 0 | 9 | 0 | 1 | 24 |
| single_agent | 25 | 11 | 6 | 0 | 5 | 1 | 13 | 18 |

- not_reported: diagnostician 1 step_limit (midline_jitter s3; two remedies, both rolled back); single agent 13 step_limit
- script on midline_jitter: 5 accepts with a good measurement (good_report on a not-repairable rod; the known limit in freeze v2). Counted neither correct nor false accept

## Held-out faults, seeds 0-2
Cells as above, each of 3.

| Fault | Label | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| second_root | not repairable | 0 / 3 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| fast_rotation | not repairable | 0 / 3 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 1 / 0 / 0 / 0 |
| bad_stage_correction | repairable | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 2 / 0 / 1 / 3 | 3 / 0 / 0 / 1 |
| flank_swap | not repairable | 0 / 3 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 | 3 / 0 / 0 / 0 |
| partial_occlusion | not repairable | 0 / 3 / 0 / 0 | 0 / 3 / 0 / 1 | 3 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |

| Method | Runs | Correct | good_report | false_accept | correct_decline | unnecessary_decline | not_reported | Terminal fault correct |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| script | 15 | 3 | 3 | 12 | 0 | 0 | 0 | 0 |
| remedy_tree | 15 | 9 | 6 | 3 | 6 | 0 | 0 | 1 |
| diagnostician | 15 | 11 | 5 | 0 | 9 | 1 | 0 | 3 |
| single_agent | 15 | 7 | 6 | 0 | 4 | 0 | 5 | 1 |

- second_root: remedy tree, diagnostician and single agent each applied `use_width_free_ratio`, named `width_change` and accepted on 3 of 3; centre error 0.48-0.83 %/h against a limit of 1.08 (good_report). The label is not repairable (fitting states only; `results/2026-10-12b_heldout_labels/README.md`), so these 9 runs count neither correct nor false accept. If the width-free ratio were a label state, second_root would be repairable and these 9 runs correct. For Andrew
- Terminal fault names on fast_rotation, flank_swap and partial_occlusion: per run in `table_heldout.md`
- diagnostician bad_stage_correction s2: declined at step 2, naming bad_stage_correction, without a remedy (unnecessary_decline)

## Steps, tokens and call time per method (both sets, 40 runs each)

| Method | Correct | Steps (mean) | Tokens in (mean) | Tokens out (mean) | Call time, s (mean) |
| :-- | --: | :-- | :-- | :-- | :-- |
| script | 13 | 40 (1.0) | - | - | - |
| remedy_tree | 33 | 155 (3.9) | - | - | - |
| diagnostician | 35 | 210 (5.2) | 921244 (23031) | 109786 (2745) | 1263.5 (31.6) |
| single_agent | 18 | 272 (6.8) | 1136585 (28415) | 131137 (3278) | 1552.6 (38.8) |

- Remedies kept and roll backs per set: in the totals of `table_dev.md` and `table_heldout.md`. The single agent has no roll back by definition
