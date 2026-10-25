# Freeze v3 scored runs, 2026-10-23 to 2026-10-24

Spec `docs/specs/2026-10-23b_freeze-v3.md`. Proposal `docs/proposals/2026-10-23_freeze-v3.md` (approved by Andrew 2026-10-23). Tag `freeze-v3` (e1e672a). Model `claude-opus-5-5`, Claude Code 2.1.310 on every LLM run. Driver `scripts/synth/scored_v3.py`; metrics `measure/metrics.py`.

## Files
- `basis.md`: clean basis at v3 geometry (thresholds and flank tolerance check)
- `sizing.md`, `sizing.json`: held-out sizes at v3 geometry
- `labels.md`, `labels.json`: labels of the 51 scored rods
- `table_metrics.md`: metrics per method, agreement, categories, per row, cost, per run
- `metrics.json`, `scores.json`: the same, machine-readable
- `runs/`: trace and summary per run, `<method>_<rod id>[_r<repeat>]`; `deterministic.jsonl` (rule methods run twice)
- Commands: README section "Freeze v3 scored runs"

## Set
- 51 rods on scoring seeds 20-22, v3 geometry (tip 96 px/h, growth zone at 200 px, tracked length 500 px, stage follows the tip every frame)
- Classes from the labels: accept_clean 18, accept_repaired 12, decline 21. All-decline scores 21 of 51 (balanced accuracy 0.33)
- `v3_bend30_clean_s20`: checker false alarm. The unremedied run fails closure (4.51 px/h, threshold 1.0) with a good measurement (centre 0.44 against 1.35 %/h, flank 0.35 against 1.00). Kept accept_clean (Andrew, option a)
- `displacement_exceeds_patch` 2x6: not repairable at v3 speed (stride 1 still 4.8 px/frame; rigid_invariance 52-126 %/h). Labelled decline, not the expected accept_repaired
- All 12 accept_repaired rods have a good unremedied measurement with a failing check. A method that accepts without a remedy is therefore scored correct on them (script and all-accept 12 of 12)

## Metrics (mean over 3 repeats for the LLM methods; range in brackets)

| Method | Runs | Balanced accuracy | accept_clean | accept_repaired | decline | False accepts | Coverage | Abst. precision | Abst. recall | not_reported |
| :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | :-- | --: |
| script | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 18 | 1.00 | - | 0.00 | 0 |
| remedy_tree | 51 | 0.81 | 1.00 | 0.75 | 0.67 | 4 | 0.67 | 0.82 | 0.67 | 0 |
| diagnostician | 153 | 0.69 (0.69-0.69) | 0.91 (0.89-0.94) | 0.44 (0.42-0.50) | 0.71 (0.67-0.76) | 0 | 0.48 | 0.64 | 0.71 | 9 |
| single_agent | 153 | 0.60 (0.57-0.64) | 0.76 (0.72-0.78) | 0.61 (0.50-0.67) | 0.43 (0.33-0.48) | 0 | 0.45 | 0.65 | 0.43 | 43 |
| all_decline | 51 | 0.33 | 0.00 | 0.00 | 1.00 | 0 | 0.00 | 0.41 | 1.00 | 0 |
| all_accept | 51 | 0.67 | 1.00 | 1.00 | 0.00 | 18 | 1.00 | - | 0.00 | 0 |

- False accepts are counts per repeat (script, remedy tree: one run). False-accept rate: script 0.35, remedy tree 0.12, diagnostician 0, single agent 0
- Script equals all-accept: it reports the unremedied measurement on every rod

## Agreement across repeats

| Method | Unanimous rods | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |
| :-- | --: | :-- | :-- | :-- | :-- | :-- |
| diagnostician | 39 of 51 | 0.76 | 0.94 | 0.67 | 0.67 | 0.776 |
| single_agent | 24 of 51 | 0.47 | 0.44 | 0.67 | 0.38 | 0.503 |

- Rule methods: a second run from the cache gave the same outcome on 102 of 102

## Per row (correct runs / runs)

| Row | Class | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| v3_growth_zone | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| v3_bend16 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 6 / 9 |
| v3_bend20 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 5 / 9 |
| v3_bend24 | accept_clean | 3 / 3 | 3 / 3 | 9 / 9 | 7 / 9 |
| v3_bend30 | accept_clean | 3 / 3 | 3 / 3 | 6 / 9 | 5 / 9 |
| v3_still | accept_clean | 3 / 3 | 3 / 3 | 7 / 9 | 9 / 9 |
| rigid_drift | accept_repaired | 3 / 3 | 3 / 3 | 3 / 9 | 6 / 9 |
| width_change | accept_repaired | 3 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| bad_stage_correction | accept_repaired | 3 / 3 | 3 / 3 | 4 / 9 | 7 / 9 |
| stage_log_missing | accept_repaired | 3 / 3 | 0 / 3 | 0 / 9 | 0 / 9 |
| displacement_exceeds_patch | decline | 0 / 3 | 2 / 3 | 6 / 9 | 3 / 9 |
| low_texture | decline | 0 / 3 | 3 / 3 | 9 / 9 | 9 / 9 |
| midline_jitter | decline | 0 / 3 | 3 / 3 | 9 / 9 | 4 / 9 |
| second_root | decline | 0 / 3 | 0 / 3 | 0 / 9 | 0 / 9 |
| fast_rotation | decline | 0 / 3 | 3 / 3 | 7 / 9 | 5 / 9 |
| flank_swap | decline | 0 / 3 | 3 / 3 | 7 / 9 | 4 / 9 |
| partial_occlusion | decline | 0 / 3 | 0 / 3 | 7 / 9 | 2 / 9 |

## Cost (all repeats)

| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |
| :-- | --: | --: | --: | --: | --: |
| remedy_tree | 51 | 156 | - | - | - |
| diagnostician | 153 | 593 | 2,611,986 | 353,434 | 4,076.9 |
| single_agent | 153 | 980 | 4,160,002 | 570,456 | 6,750.5 |

## Tracker runs and compute
- 528 tracker runs in all (cap 600): basis 100, sizing 36, labels 228, method states 124, LLM single jobs 40. 0 failed
- Lab server only, under the shared-machine limits; at most 2 jobs of this account from 2026-10-23
- Work space on the lab server 8.05 GB after the last sweep (Andrew removed the v2 renders on 2026-10-23); the 40 single jobs are not in that figure

## Run record
- LLM runs: 306 (diagnostician and single agent, 3 repeats each), 0 harness errors, one run at a time
- Stopped twice by Claude Code on VM memory (157 of 306 after the second stop); resumed in blocks of 8-13 runs with a free-memory floor of 1.5 GB (Andrew, 2026-10-24). Free memory before each block 1.7-2.4 GB
- Status was pushed after each block, so run summaries record 17 commits. Between the tag and the last run only harness code changed (`measure/runner.py` sweep-log choice, `scripts/synth/scored_v3.py --max-runs`); no prompt, threshold, remedy, checker or config change
- v2 results stay in `results/2026-10-12b_scored_v1/`; seeds 0-5 are not used in v3
