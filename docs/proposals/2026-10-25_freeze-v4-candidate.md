# Freeze v4 candidate

From: build account, session diag-analysis. Date: 2026-10-25. Inbox diag-analysis items 3-5. Branch `wip/v4-candidate` (not merged to main until Andrew approves). Scored v4 run approved by Andrew 2026-10-25 00:25 (item 4 (3)).

## 1. What changed (switch `candidate: v4`, off by default)
- One switch: `candidate` in `config/models.yaml`, null by default. The v4 driver (`scripts/synth/scored_v4.py`) turns it on for its own process (`agents.candidate.use("v4")`). The config file and every v3 or v3.1 command are unchanged
- C1, prompt: `agents/prompts/diagnostician_v4.md` and `single_agent_v4.md` = v3 text plus the fault-to-remedy map after the check list and one rule ("Decline without a remedy only when no listed remedy is mapped to the fault you name"). Same section in both, so the single-agent comparison stays fair. Text as in `docs/proposals/2026-10-25_diagnostician-repair-misses.md`, C1
- C2, info: `stage_log_summary` adds `moves_every_pair` (with the note "at-moves and elsewhere cannot be compared" when true), `closure_residual_px_per_pair_median`, `closure_residual_px_per_pair_max`, `closure_residual_max_pair_index` (`measure/info.py`, `stage_log_spread`). v3 fields unchanged. No threshold
- C3 option (a), labels: a check that cannot be computed after a remedy counts as failing (`measure/score.py`, `checks_pass(..., not_computable_fails=True)`), as the roll-back rule already does (`agents/executors.py`, `no_progress`). Andrew, 2026-10-25
- Not changed: checker, thresholds, remedies and their settings, action lists, scoring tolerance, metrics, model `claude-opus-5-5`, Claude Code 2.1.310, step limits

## 2. Switch-off check (`results/2026-10-25_freeze_v4/switch_check.md`)
From the v3 tracker cache; no tracker runs, no LLM calls. `python scripts/synth/v4_replay_check.py`.

| Part | Switch off | Switch on |
| :-- | :-- | :-- |
| v3 labels (51 rods) | 51 equal | 48 equal; 3 stage_log_missing rods accept_repaired -> decline (C3 a) |
| Rule methods rerun (102 runs) | 102 same outcome | 102 same outcome |
| v3 LLM traces re-executed (306 runs, 1319 steps) | 0 differ | 0 differ, apart from the C2 fields |

- Tests: `tests/test_v4_candidate.py` (9); whole suite 315 passed, 1 skipped

## 3. Labels, unseen seeds 26-28 (`results/2026-10-25_freeze_v4/labels.md`, `labels.json`)
- Every v3 class at its v3 size: 6 clean rows; development faults at the freeze v2 sizes; held-out faults at the v3 sizes. 51 rods
- Tracker only, v3 repair criteria with C3 (a). Committed (6b72d6a) before any agent run
- Lab server under its standing limits (Andrew, item 5). 228 tracker runs (144 unremedied and stride states, then 84 registration and patch states), 0 failed. The first start stopped itself at 13 runs on the 10 GB default work-space limit (the runner config lacked the 50 GB setting of 2026-10-24); restarted, finished runs skipped

| Row | Rods | Label | Repairing remedy |
| :-- | --: | :-- | :-- |
| v3_growth_zone, v3_bend16, v3_bend20, v3_bend24, v3_bend30, v3_still | 18 | accept_clean | - |
| rigid_drift 0.5 | 3 | accept_repaired | register_frames |
| width_change | 3 | accept_repaired | use_width_free_ratio |
| bad_stage_correction 3 | 3 | accept_repaired | register_frames |
| stage_log_missing 1 | 3 | decline | - (register_frames state: closure not computable, so failing under C3 a) |
| displacement_exceeds_patch 2x6 | 3 | decline | - |
| low_texture 0.03, midline_jitter 3 | 6 | decline | - |
| second_root 30, fast_rotation 2, flank_swap 0.5, partial_occlusion 20 | 12 | decline | - |

- Classes: accept_clean 18, accept_repaired 9, decline 24. 0 labels differ from the expected class (v3 labels, with stage_log_missing under C3 a)
- Decline-all scores 24 of 51 (overall 0.47; balanced accuracy 0.33: decline 1.00, both accept classes 0.00)
- No clean rod fails a check unremedied (v3 had one checker false alarm, on seed 20)
- As in v3, all 9 accept_repaired rods have a good unremedied measurement with a failing check, so a method that accepts without a remedy scores correct on them (script, all-accept)

## 4. Development check, not a score (`results/2026-10-25_freeze_v4/dev_check.md`)
- Diagnostician, switch on, v3 seed 20 (a v3 scoring seed whose traces C1 and C2 were written from), one run per row of the v3 set: 17 runs. States from the v3 cache only; 0 runs needed a state outside it. Labels: v3 labels with C3 (a)
- Correct 14 of 17. Same seed, v3 diagnostician runs scored against the same labels: 33 of 51 over 3 repeats

| Row | Class | Dev check | v3, seed 20 (3 repeats) |
| :-- | :-- | :-- | :-- |
| 5 clean rows except bend30 | accept_clean | 5 / 5 accept | 15 / 15 |
| v3_bend30 (checker false alarm) | accept_clean | decline | 0 / 3 |
| rigid_drift | accept_repaired | register_frames, accept | 0 / 3 |
| bad_stage_correction | accept_repaired | register_frames, accept | 0 / 3 |
| width_change | accept_repaired | accept | 3 / 3 |
| stage_log_missing | decline (C3 a) | decline | 3 / 3 |
| displacement_exceeds_patch, low_texture, midline_jitter, fast_rotation, flank_swap | decline | 5 / 5 decline | 11 / 15 |
| second_root | decline | accept after use_width_free_ratio (accept_on_decline) | 0 / 3 |
| partial_occlusion | decline | step limit (not reported) | 1 / 3 |

- The group A misses of the repair-miss analysis do not recur on this seed: both rods apply `register_frames` and accept. rigid_drift is still named bad_stage_correction
- One run per row on a development seed. It shows the switch works end to end; it does not estimate accuracy

## 5. Scored run (approved, item 4 (3))
- Tag `freeze-v4` on `wip/v4-candidate` after this file is committed
- All methods on seeds 26-28 with the switch on: script, remedy tree, single agent, diagnostician (LLM methods 3 repeats), decline-all as reference. Metrics, agreement statistics and README layout as `results/2026-10-23_freeze_v3/`, in `results/2026-10-25_freeze_v4/`
- Stops: over 420 tracker runs in all (228 used by labels) or 400 LLM runs (17 used by the development check); free VM memory under 3.85 GB before a batch (Andrew, 2026-10-25, lowered from 4 GB)
- No change to prompts, thresholds or remedies after the first v4 result is seen

## Limits
- Seeds 26-28 are a new draw of the same rod kinds and sizes as v3, not new fault kinds
- C3 (a) moves stage_log_missing from accept_repaired to decline; v3 and v4 accept_repaired accuracies are over different rows (v3: 4 rows, 12 rods; v4: 3 rows, 9 rods)
- Kinematics only
