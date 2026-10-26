# Freeze v4 scored runs, 2026-10-25 to 2026-10-26

Inbox diag-analysis items 3-5 (Andrew, 2026-10-25). Proposal `docs/proposals/2026-10-25_freeze-v4-candidate.md`. Tag `freeze-v4` (e9f19f2). Candidate `v4` on (C1, C2, C3 option a). Model `claude-opus-5-5`, Claude Code 2.1.310 on every LLM run. Driver `scripts/synth/scored_v4.py` (the v3 driver pointed at v4); metrics `measure/metrics.py`.

## Files
- `switch_check.md`: the switch against freeze v3 (labels, rule methods, every v3 LLM trace re-executed; switch off and on)
- `labels.md`, `labels.json`: labels of the 51 rods, seeds 26-28
- `dev_check.md`, `dev_check/`: development check, not a score (diagnostician, v3 seed 20, one run per row)
- `table_metrics.md`: metrics per method, agreement, categories, per row, cost, per run
- `metrics.json`, `scores.json`: the same, machine-readable
- `runs/`: trace and summary per run, `<method>_<rod id>[_r<repeat>]`; `deterministic.jsonl` (rule methods run twice)
- `runs/usage_limit/`: 95 LLM runs ended by the account usage limit, kept for the record and run again
- Commands: README section "Freeze v4 candidate"

## Set
- 51 rods on unseen seeds 26-28, v3 geometry; every v3 class at its v3 size
- Classes from the labels: accept_clean 18, accept_repaired 9, decline 24. All-decline scores 24 of 51 (balanced accuracy 0.33)
- `stage_log_missing` 1 labels decline under C3 (a) (closure not computable after `register_frames`); in v3 it was accept_repaired
- No clean rod fails a check unremedied (v3 had one checker false alarm)
- All 9 accept_repaired rods have a good unremedied measurement with a failing check. A method that accepts without a remedy is therefore scored correct on them (script and all-accept 9 of 9)

## Metrics (mean over 3 repeats for the LLM methods; range in brackets)

| Method | Runs | Balanced accuracy | accept_clean | accept_repaired | decline | False accepts | Coverage | Abst. precision | Abst. recall | not_reported |
| :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | :-- | --: |
| script | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 18 | 1.00 | - | 0.00 | 0 |
| remedy_tree | 51 | 0.93 | 1.00 | 1.00 | 0.79 | 2 | 0.63 | 1.00 | 0.79 | 0 |
| diagnostician | 153 | 0.93 (0.92-0.94) | 1.00 | 1.00 | 0.79 (0.75-0.83) | 0 | 0.58 | 1.00 | 0.79 | 7 |
| single_agent | 153 | 0.63 (0.58-0.69) | 0.83 (0.78-0.89) | 0.96 (0.89-1.00) | 0.10 (0.04-0.17) | 0.3 (0-1) | 0.48 | 0.50 | 0.10 | 66 |
| all_decline | 51 | 0.33 | 0.00 | 0.00 | 1.00 | 0 | 0.00 | 0.47 | 1.00 | 0 |
| all_accept | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 18 | 1.00 | - | 0.00 | 0 |

- False accepts are counts per repeat (script, remedy tree: one run). False-accept rate: script 0.35, remedy tree 0.06, diagnostician 0, single agent 0.01
- not_reported: diagnostician 7 runs at the step limit; single agent 66 runs at the step limit
- Script equals all-accept: it reports the unremedied measurement on every rod

## Agreement across repeats

| Method | Unanimous rods | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |
| :-- | --: | :-- | :-- | :-- | :-- | :-- |
| diagnostician | 46 of 51 | 0.90 | 1.00 | 1.00 | 0.79 | 0.887 |
| single_agent | 34 of 51 | 0.67 | 0.56 | 0.89 | 0.67 | 0.626 |

- Rule methods: a second run from the cache gave the same outcome on 102 of 102

## Per row (correct runs / runs)

| Row | Class | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| v3_bend16 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_bend20 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 7 / 9 |
| v3_bend24 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 8 / 9 |
| v3_bend30 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_still | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| rigid_drift | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| width_change | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| bad_stage_correction | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 8 / 9 |
| stage_log_missing | decline | 0 / 3 | 3 / 3 | 9 / 9 | 0 / 9 |
| displacement_exceeds_patch | decline | 0 / 3 | 3 / 3 | 7 / 9 | 0 / 9 |
| low_texture | decline | 0 / 3 | 3 / 3 | 9 / 9 | 0 / 9 |
| midline_jitter | decline | 0 / 3 | 3 / 3 | 7 / 9 | 0 / 9 |
| second_root | decline | 0 / 3 | 0 / 3 | 1 / 9 | 0 / 9 |
| fast_rotation | decline | 0 / 3 | 3 / 3 | 6 / 9 | 2 / 9 |
| flank_swap | decline | 0 / 3 | 3 / 3 | 9 / 9 | 2 / 9 |
| partial_occlusion | decline | 0 / 3 | 1 / 3 | 9 / 9 | 3 / 9 |

## Freeze v3 alongside (seeds 20-22, v3 labels, `results/2026-10-23_freeze_v3/`)
- Different seeds and, for stage_log_missing, a different label rule; not a paired comparison

| Method | v3 balanced | v4 balanced | v3 accept_repaired | v4 accept_repaired | v3 false accepts | v4 false accepts |
| :-- | :-- | :-- | :-- | :-- | --: | --: |
| script | 0.67 | 0.67 | 1.00 | 1.00 | 18 | 18 |
| remedy_tree | 0.81 | 0.93 | 0.75 | 1.00 | 4 | 2 |
| diagnostician | 0.69 | 0.93 | 0.44 | 1.00 | 0 | 0 |
| single_agent | 0.60 | 0.63 | 0.61 | 0.96 | 0 | 0.3 |

## Cost (all repeats)

| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: |
| remedy_tree | 51 | 152 | - | - | - |
| diagnostician | 153 | 655 | 3,061,490 | 389,197 | 4,560.3 |
| single_agent | 153 | 1,040 | 4,790,821 | 644,251 | 7,539.0 |

## Tracker runs and compute
- 404 tracker runs in all (cap 420, Andrew item 5): labels 228, method states 118, single jobs from LLM runs 58. 0 failed
- Lab server only, under its standing limits (at most 2 jobs, 4 single-thread workers, lowest priority, load check, one sweep at a time). The first label sweep stopped itself at 13 runs on the 10 GB default work-space limit (runner config lacked the 50 GB setting of 2026-10-24); restarted, finished runs skipped
- Work space on the lab server 10.96 GB after the last sweep

## Run record
- LLM runs: 306 scored (diagnostician and single agent, 3 repeats each) + 17 development check + 95 set aside = 418 (cap 420, Andrew 2026-10-26)
- 95 runs ended on the account usage limit (two calls in a row answered "session limit"; no model answer): diagnostician repeat 1: 23, single agent repeat 0: 27, repeat 2: 45. Set aside in `runs/usage_limit/` and run again with the same code and tag (Andrew, 2026-10-26). 0 such runs in the final set
- One run (single agent, stage_log_missing s27, repeat 2) was cut off when its batch loop stopped with the Claude Code session; its partial trace is kept under the run name and the rerun trace has a `_trace_<time>` name
- Free VM memory at least 3.85 GB before each batch (Andrew, 2026-10-25); batches of 17; status pushed after each batch, so run summaries record several commits. Between the tag and the last run only harness code changed (853da3b, `scripts/synth/scored_v4.py`: usage-limit set-aside, LLM cap); no prompt, threshold, remedy, checker or config change
- 0 harness errors
