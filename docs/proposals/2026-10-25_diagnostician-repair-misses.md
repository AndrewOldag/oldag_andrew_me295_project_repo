# Diagnostician declines on repairable rods, freeze v3

From: build account, session diag-analysis. Date: 2026-10-24. Spec `docs/specs/2026-10-24b_real-movie-push.md`, section D. Branch `wip/diag-analysis`. No code changed except a read-only table script. No tracker runs, no LLM calls.

Inputs: `results/2026-10-23_freeze_v3/` (`labels.json`, `labels.md` per-state table, `runs/` traces and summaries), `agents/prompts/diagnostician.md`, `agents/actions.py`, `agents/executors.py` (`no_progress`), `agents/baselines.py` (`TREE`), `measure/info.py` (`stage_log_summary`), `measure/score.py` (`checks_pass`, `label_rod`), `checker/checks.py` (`closure`), `measure/render_heldout.py`. Prompt and actions are as tagged `freeze-v3` (no diff since).

Table: `python scripts/synth/repair_misses.py` prints one line per run and the counts below.

## Summary
- 12 accept_repaired rods x 3 repeats = 36 diagnostician runs. Correct 16 (0.44). Missed 20, all `decline`. None ended at the step limit
- Remedy tree on the same 12 rods: correct 9 of 12 (0.75)

| Fault (3 rods each) | Labelled remedy | Diagnostician correct | Misses | Group | Remedy tree correct |
| :-- | :-- | --: | --: | :-- | --: |
| rigid_drift 0.5 | register_frames | 3 / 9 | 6 | A | 3 / 3 |
| bad_stage_correction 3 px | register_frames | 4 / 9 | 5 | A | 3 / 3 |
| stage_log_missing 1 | register_frames | 0 / 9 | 9 | B | 0 / 3 |
| width_change | use_width_free_ratio | 9 / 9 | 0 | - | 3 / 3 |
| All | | 16 / 36 | 20 | | 9 / 12 |

- Group A (11 runs): declined with no remedy tried. The agent believed no listed remedy fixes a stage-correction error. `register_frames` fixes it (label sweep 6 of 6 rods)
- Group B (9 runs): `register_frames` applied, rolled back by the orchestrator, then declined. The roll-back rule and the label rule disagree on a check that cannot be computed. The agent followed the prompt correctly once the roll-back happened
- Group A is a prompt and information cause. Group B is a rule mismatch in the harness; no prompt change can fix it

## 1. Group A: declined with no remedy tried (11 runs)

| Rod | Repeat | Decline step | Evidence before decline | Fault named |
| :-- | :-- | --: | :-- | :-- |
| rigid_drift s20 | r0, r1, r2 | 2 | stage_log_summary | bad_stage_correction |
| rigid_drift s21 | r0 | 2 | stage_log_summary | bad_stage_correction |
| rigid_drift s22 | r0, r1 | 2 | stage_log_summary | bad_stage_correction |
| bad_stage_correction s20 | r0, r1, r2 | 2 | stage_log_summary | bad_stage_correction |
| bad_stage_correction s21 | r2 | 2 | stage_log_summary | bad_stage_correction |
| bad_stage_correction s22 | r2 | 4 | stage_log_summary, velocity_profile, check_report | bad_stage_correction |

### Evidence the agent had
- Task: closure fails (rigid_drift 7.94-8.14 px/h; bad_stage_correction 2.84-2.98 px/h; threshold 1.0). Rigid invariance and plane sections pass
- Step 1, every run of both faults: `stage_log_summary`. At v3 geometry the stage follows the tip every frame, so `stage_moves` 40 of 40 pairs. `closure_residual_px_elsewhere` is null and `closure_residual_px_per_h_elsewhere` is 0.0 by construction. The whole residual is "at moves" for both faults
  - rigid_drift: 0.2 px per pair at moves, velocity jump 1.58-1.63 px/h
  - bad_stage_correction: 0.09-0.1 px per pair at moves, velocity jump 1.59-1.63 px/h
- The split at-moves / elsewhere was added for v2 geometry (5 moves in 40 pairs; proposal 2026-10-12, P1). At v3 geometry it carries no information
- Two runs (bad_stage_correction s22 r1 and r2) stated this themselves: "every one of the 40 frame pairs has a move, so the stage log alone can't separate a bad stage correction from rigid drift". r1 then applied `register_frames` and accepted; r2 declined

### Where it went wrong
- Every group A decline gives the same reason: the stage correction is wrong "and no listed remedy fixes it". One rationale (rigid_drift s21 r0): "Registering frames targets unlogged drift, so no listed remedy fits"
- The prompt has no fault-to-remedy map. The fault list's one-line meanings are code comments in `agents/actions.py`; `describe()` lists names only. The prompt says rigid-body invariance passes under "drift or rotation" and closure fails under "unlogged drift or rotation". Nothing says that registration also replaces a wrong stage log
- `register_frames` registers on non-growing tissue from the images (result text "frames registered on the non-growing tissue (from 400 px from the tip) before tracking"). It does not use the stage log. It therefore removes a stage-log error as well as unlogged motion. The label sweep shows this: bad_stage_correction closure 2.84-2.98 -> 0.12-0.31 px/h, all checks pass, measurement good, 3 of 3 seeds
- First divergence: step 2, on identical evidence. The 7 correct runs on the same rods had the same step-1 answer, named the same fault (bad_stage_correction) and applied `register_frames`. Repeat-to-repeat variation decided the outcome: rigid_drift 3 of 9 applied it, bad_stage_correction 4 of 9

### Would a listed remedy have worked
- Yes on all 6 rods. Label sweep (`labels.md`, per state), `register_frames`:

| Rod | Closure before -> after (px/h) | All checks pass | Good |
| :-- | :-- | :-- | :-- |
| rigid_drift s20, s21, s22 | 7.99 -> 0.61; 8.14 -> 0.35; 7.94 -> 0.55 | yes | yes |
| bad_stage_correction s20, s21, s22 | 2.95 -> 0.31; 2.84 -> 0.12; 2.98 -> 0.23 | yes | yes |

- The 7 correct diagnostician runs reached exactly these states (same closure values after the remedy)

### Fault naming
- rigid_drift was named bad_stage_correction in 9 of 9 runs, including the 3 that accepted. The naming error follows from the uninformative split above
- The two faults differ in how the residual is spread over pairs. By the injector definitions (`measure/render_heldout.py`): bad_stage_correction under-reports one stage move by 3 px from mid-window on; rigid_drift is steady motion every frame. The closure values match this: 2.95 px/h over a 1 h window is the 3 px step; 0.2 px per pair x 40 pairs is 8 px/h of drift. `stage_log_summary` reports only the mean per pair, which hides the difference. Not measured per pair here: the records are not in the repo and the spec allows no new runs

### Remedy tree on the same rods
- 6 of 6 correct. Rule 1: closure fails first, so the tree tries `register_frames` first (named rigid_drift) and accepts after one step. The tree never reads the stage log, so the uninformative split cannot mislead it

## 2. Group B: remedy rolled back, then declined (9 runs)

| Rod | Repeats | Remedy step | Decline step | Fault named |
| :-- | :-- | :-- | :-- | :-- |
| stage_log_missing s20 | r0, r1, r2 | 3, 2, 3 | 4, 7, 6 | rigid_drift |
| stage_log_missing s21 | r0, r1, r2 | 5, 3, 3 | 6, 4, 4 | rigid_drift |
| stage_log_missing s22 | r0, r1, r2 | 3, 3, 3 | 4, 4, 4 | rigid_drift |

### Evidence the agent had
- Task: closure fails at 95.8-96.0 px/h (the full basal velocity, 202 um/h). Rigid invariance and plane sections pass
- `stage_log_summary`: 0 stage moves, residual 95.95 px/h "elsewhere". `velocity_profile` (8 runs): tip net displacement 0.0 um/h, basal velocity 202 um/h
- The agent named the cause right (unlogged whole-root motion) and applied the right remedy (`register_frames`) in 9 of 9 runs

### What happened at the remedy
- After registration closure cannot be computed: value NaN, passed None (`checker/checks.py`, `closure`). Rigid invariance 1.03-1.40 and plane sections pass. Why registration leaves closure uncomputable is not checked here (records not in the repo)
- `agents/executors.py`, `no_progress`: "A check that can no longer be computed (no coverage) is not resolved." A failing check that becomes None without a "skipped" detail counts as not resolved, so the remedy is rolled back. Result note: "the remedy made no failing check pass and lowered none by a quarter"
- `settings_left`: register_frames has no further setting. The prompt rule then says decline, naming the fault the remedy targeted. The agent did that, in 4-7 steps
- Agent behaviour after the roll-back follows the prompt. 2 runs (s20 r1, r2) looked for a second fault with its own evidence (patch, frame quality, midline) before declining, as the rule allows; 7 declined at the next step

### Would a listed remedy have worked
- By the label rule, yes: `register_frames` state "all pass yes, good yes" on 3 of 3 seeds (`labels.md`: closure "nan skip")
- `measure/score.py`, `checks_pass`: "a skipped check has passed None and does not count". The label rule drops a check that cannot be computed; the roll-back rule counts it as unresolved. The two rules disagree on the same state
- Under the orchestrator's rule the registered state could never be accepted. Under the label rule it is the correct outcome
- The remedy tree fails these rods the same way: register_frames rolled back, then 4 more remedies, decline "rule 3: no remedy left for closure" (0 of 3)
- This is not a diagnostician fault. It is the cause of `stage_log_missing` 0 of 9 and 0 of 3 noted in the v3 running log entry without a cause

## 3. Causes and counts

| Cause | Runs | Rods | Fix type |
| :-- | --: | :-- | :-- |
| A1. No fault-to-remedy map in the prompt: agent believes no remedy fits a stage-correction error | 11 | rigid_drift x3, bad_stage_correction x3 | prompt |
| A2. `stage_log_summary` split is uninformative when the stage moves every pair (makes A1 fire on rigid_drift; wrong fault name 9 of 9) | 6 of the 11 (and 3 correct runs misnamed) | rigid_drift x3 | info |
| B. Roll-back rule counts a not-computable check as unresolved; label rule drops it | 9 | stage_log_missing x3 | rule (Andrew) |
| Step or turn limit | 0 | - | - |

- A1 and A2 overlap on the rigid_drift runs. A1 alone explains every group A decline: on bad_stage_correction the fault was named right and the agent still declined
- Upper bound if every group A run had applied `register_frames`: 27 of 36 (0.75), from the label sweep states. Adding group B under the label rule: 36 of 36. Estimates from cached states, not runs

## 4. Candidate changes for a later freeze (at most 3; none applied)

### C1 (A1). Prompt: fault-to-remedy map
Add after the check list:
> Listed remedies by fault:
> - rigid_drift, bad_stage_correction: `register_frames`. It finds the frame motion from the images on non-growing tissue and does not use the stage log, so it removes a wrong stage correction as well as unlogged drift
> - displacement_exceeds_patch: `change_frame_stride` half
> - low_texture: `enlarge_patch`
> - midline_jitter: `smooth_midline` light
> - second_root: `crop_or_mask`
> - width_change: `use_width_free_ratio`
> - fast_rotation: `register_frames` (it may not repair a fast rotation)
> - unknown: none
- And one rule: "Decline without a remedy only when no listed remedy is mapped to the fault you name"
- Source of the map: the fixed remedy list and the label states in `scripts/synth/scored_v3.py` (`label_states`) and the remedy tree (`agents/baselines.py`, `TREE`), all set before v3. Not taken from these traces
- Risk: more remedies tried on decline-class rods. Roll-back and the checks still gate accept. The diagnostician had 0 false accepts in v3; a change must be scored for false accepts too
- The single-agent baseline gets the same map (same prompt section), so the comparison stays fair

### C2 (A2). Info: `stage_log_summary` per-pair spread
- Add `closure_residual_px_per_pair_median`, `closure_residual_px_per_pair_max` and the pair index of the max, over all pairs
- Add `moves_every_pair: true` when `stage_moves == frame_pairs`, with the note "at-moves and elsewhere cannot be compared"
- Expected signature from the injector definitions: one stage-log error gives one large pair over a small median; steady drift gives max close to median. No threshold proposed: the only values in hand are the scored seeds
- Effect is on fault naming (diagnosis score). With C1 the outcome is the same for both faults

### C3 (B). Not a prompt change: make the roll-back and label rules agree
- Needs Andrew. Two options:
  - (a) Labels count a check that cannot be computed after a remedy as failing (as `no_progress` does). stage_log_missing 1 becomes decline; accept_repaired loses 3 rods
  - (b) `no_progress` treats a failing check that becomes not computable as resolved, and the agent is told which check could not be run. The system would then accept with closure not run
- Kinematic point for the choice: with no stage log, closure has nothing to compare the tip path with after registration. (b) reports a field that one of the three checks never tested. (a) keeps "every check computed" as the accept rule
- Either option is a change to a frozen item (labels or orchestration) and needs a decisions entry

## 5. Limits
- Written from scoring-seed traces (20-22). A re-run on seeds 20-22 after C1 or C2 is a check, not a score. Score on unseen seeds (v3.1 uses 23-25 for its new rods)
- v3.1 keeps prompts unchanged (spec 2026-10-24), so none of C1-C3 can enter v3.1
- All 12 accept_repaired rods have a good unremedied measurement (v3 README). A decline there is still the wrong outcome under the v3 scoring
- No real-movie claim. The real slice (dispatcher, 2026-10-24) also declined at closure with bad_stage_correction named, but its closure definition is under review (spec section A); it is not used here

## Open, for Andrew
1. C1 and C2: approve, edit or reject for a later freeze
2. C3: option (a) or (b), or leave the mismatch and report it
