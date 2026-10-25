# Note for the planning account: a check that cannot be computed, label rule against roll-back rule

From: build account, session diag-analysis. Date: 2026-10-24. To resolve with Andrew (Andrew, 2026-10-24: "we will resolve it then"). Detail: `docs/proposals/2026-10-25_diagnostician-repair-misses.md`, section 2 and C3. Nothing changed.

## Facts
- `stage_log_missing` 1, freeze v3, 3 rods. After `register_frames`, closure cannot be computed (value NaN, passed None). Rigid invariance and plane sections pass; the measurement is good
- Label rule, `measure/score.py` `checks_pass`: a check with passed None does not count. The registered state passes, so the rods are labelled accept_repaired
- Roll-back rule, `agents/executors.py` `no_progress`: "A check that can no longer be computed (no coverage) is not resolved." The remedy is rolled back
- Both the diagnostician and the remedy tree run under the roll-back rule. Neither can reach the labelled outcome: diagnostician 0 of 9, remedy tree 0 of 3
- The diagnostician named the cause (unlogged motion) and applied the labelled remedy in 9 of 9 runs. The misses are not an agent error

## Effect on the v3 numbers
- accept_repaired, as scored: diagnostician 16 of 36 (0.44), remedy tree 9 of 12 (0.75). Balanced accuracy includes these rods
- Without the 3 rods, from the same counts (not re-scored): diagnostician 16 of 27 (0.59), remedy tree 9 of 9
- Any agent-behaviour claim from the v3 accept_repaired numbers should state this, or wait for the decision

## Options
- (a) A check that cannot be computed counts as failing, in the labels as in the roll-back rule. The 3 rods become decline; accept_repaired 12 -> 9 rods. Accept keeps "every check computed"
- (b) The roll-back rule treats a failing check that becomes not computable as resolved, and the agent is told which check did not run. The system then reports a field that closure never tested
- Build-account recommendation: (a)
- Either changes a frozen item (labels or orchestration) and needs a decisions entry
- v3.1 sizing: `stage_log_missing` 1 does not meet the v3.1 accept_repaired rule (`results/2026-10-24_freeze_v3.1/README.md`), so v3.1 is not affected unless that changes. The rule question applies to v3 scoring and to any later freeze with a remedy that leaves a check not computable
