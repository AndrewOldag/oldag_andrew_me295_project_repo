# Held-out supplement c029b: milder compound and novel faults, 2026-11-22 to 2026-11-23

Inbox compound item 10 (Andrew, 2026-11-22). Reported beside c029 (`../README.md`), never merged into its numbers. Proposal `docs/proposals/2026-11-22_heldout-supplement.md` (bd3c2ce), committed before any render. Labels and the selected 20 committed before any method run (701442d).

## Files
- `labels.md`, `labels.json`: labels of the 48 candidates, every state of the tracker-only sweep
- `selected.json`: the 20 rods kept by the selection rule (proposal, section 5)
- `table_metrics.md`, `metrics.json`, `scores.json`: metrics, per repeat, per run
- `runs/`: one summary and one trace per scored run; `runs/deterministic.jsonl`: second runs of the rule methods
- `runs/missing_state/`: 2 runs that hit a state not cached (kept, not scored; inbox item 12); `runs/usage_limit/`: 2 runs ended by the account session limit (kept, not scored). All 4 redone from step 0

## Commands
- `python scripts/synth/heldout_supplement.py render`; `compound_queue.py --set c029b submit|fetch`; `heldout_supplement.py labels`
- `python scripts/synth/heldout_supplement.py rules`; `agents --method diagnostician|single_agent --repeat 0|1|2`
- `python scripts/synth/heldout_supplement.py eval` writes the tables

## Set
- 48 candidates: 6 kinds x seeds 60-67, v3_growth_zone, each with its rigidly moved copy. The 4 c029 compound faults at milder severity (`measure/render_compound.py` MILD) and the 2 novel faults at smaller size (focus_drift 1.5 px, illumination_flicker 0.03)
- Labels of all 48 (freeze v4 truth rule, tracker-only sweep, as c029): accept_clean 7, accept_repaired 19, decline 22
- Selection in seed order: first 4 accept_clean, first 10 accept_repaired, first 6 decline. 20 rods, no shortfall
- Expected classes (proposal) differ from the label on most selected rods: illumination_flicker 0.03 (expected accept_clean) labels accept_repaired on seeds 60-63; focus_drift s60 labels accept_repaired; the 6 selected decline rods were expected accept_repaired
- Label tracker runs on the cluster (CPU arrays through `rod_jobs.py`): unremedied 96, remedied array 7874239 (2,608 tracker runs, 0 failed); paused remedy-tree states: arrays 7902231, 7919315, 7925321
- All-decline scores 6 of 20 (c029: 20 of 24)

## Metrics (mean over 3 repeats for the LLM methods; range in brackets)

| Method | Runs | Balanced accuracy | Acc. accept_clean | Acc. accept_repaired | Acc. decline | Overall | False accepts per repeat | Not reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | --: |
| script | 20 | 0.40 | 1.00 | 0.20 | 0.00 | 0.30 | 12.0 | 0 |
| remedy_tree | 20 | 0.77 | 1.00 | 0.80 | 0.50 | 0.75 | 4.0 | 0 |
| diagnostician | 60 | 0.60 (0.57-0.62) | 1.00 | 0.20 | 0.61 (0.50-0.67) | 0.48 (0.45-0.50) | 4.0 | 1 |
| single_agent | 60 | 0.43 (0.40-0.47) | 1.00 | 0.30 (0.20-0.40) | 0.00 | 0.35 (0.30-0.40) | 6.3 (6.0-7.0) | 20 |
| all_decline | 20 | 0.33 | 0.00 | 0.00 | 1.00 | 0.30 | 0.0 | 0 |
| all_accept | 20 | 0.40 | 1.00 | 0.20 | 0.00 | 0.30 | 12.0 | 0 |

- Not reported: the run ended at the step limit (diagnostician 1, single agent 20)
- The set separates the methods: all-decline scores 0.30 overall, the remedy tree 0.75, the diagnostician 0.48
- The script equals all-accept on every row
- Diagnostician: 18 unnecessary declines on accept_repaired rods (rate 0.60); it keeps a remedy on 3 runs of accept_clean rods
- Set-aside runs (not in the table): missing state 2, usage limit 2

## Per row (correct runs / runs)

| Kind | Label | Seeds | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| focus_drift 1.5 | accept_clean | 61-64 | 4 / 4 | 4 / 4 | 12 / 12 | 12 / 12 |
| focus_drift 1.5 | accept_repaired | 60 | 1 / 1 | 1 / 1 | 3 / 3 | 2 / 3 |
| illumination_flicker 0.03 | accept_repaired | 60-63 | 0 / 4 | 4 / 4 | 3 / 12 | 4 / 12 |
| drift_low_texture_mild | accept_repaired | 61, 64 | 0 / 2 | 2 / 2 | 0 / 6 | 3 / 6 |
| second_root_occlusion_mild | accept_repaired | 62, 64 | 0 / 2 | 0 / 2 | 0 / 6 | 0 / 6 |
| drift_jitter_mild | accept_repaired | 64 | 1 / 1 | 1 / 1 | 0 / 3 | 0 / 3 |
| drift_low_texture_mild | decline | 60 | 0 / 1 | 1 / 1 | 3 / 3 | 0 / 3 |
| second_root_occlusion_mild | decline | 60, 61 | 0 / 2 | 0 / 2 | 0 / 6 | 0 / 6 |
| drift_jitter_mild | decline | 60, 61 | 0 / 2 | 1 / 2 | 5 / 6 | 0 / 6 |
| low_texture_fast_mild | decline | 60 | 0 / 1 | 1 / 1 | 3 / 3 | 0 / 3 |

- second_root_occlusion_mild: no method is correct on any of its 4 rods

## Agreement across repeats

| Method | Unanimous rods | Fleiss kappa |
| :-- | :-- | :-- |
| diagnostician | 19 of 20 | 0.955 |
| single_agent | 14 of 20 | 0.700 |

- Rule methods: second runs from the cache identical on 40 of 40

## Cost (all repeats)
- Agent runs: 120 scored (60 per LLM method) plus 4 set aside; 124 of the cap of 150
- `claude -p` calls (agent steps), scored runs: diagnostician 285, single agent 394. Tokens in / out: diagnostician 1.36 M / 0.16 M; single agent 1.82 M / 0.21 M. Call time 1,679 s and 2,275 s. The 4 set-aside runs record no token counts
- Remedy tree: 56 steps, no LLM

## Run record
- Rule methods 2026-11-23 03:50-04:52 (script 20; remedy tree 19 of 20). The 20th (low_texture_fast_mild s60) paused on states not cached three times, each fetched from the cluster and redone from step 0; last state from array 7925321, run written 09:53
- LLM methods 03:50-07:47, one run at a time on the VM. Stopped by the account session limit (2 runs set aside) and restarted; 2 runs hit a state not cached, set aside and redone once it was fetched
- Runs record commits 701442d to 0c71f4b. Across them only `scripts/synth/heldout_compound.py` and `scripts/synth/heldout_supplement.py` changed (set-aside and pause handling); agents, checker, prompts, config and renderer unchanged
- Option A integrity gate at every remedy step (`Slice.apply_remedy`) for the tree and the diagnostician; not applied to labels (inbox item 7)

## Known limits
- Labels come from a tracker-only sweep of states of one or two steps, as c029
- Milder severities did not make every compound rod repairable: 22 of 48 candidates label decline
- 11 of 20 selected rods label differently from the proposal's expected class; the labels are scored
- One synthetic set of 20 rods and 3 repeats; differences of one or two rods are within run-to-run spread of the LLM methods
