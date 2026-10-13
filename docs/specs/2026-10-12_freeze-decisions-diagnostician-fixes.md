# Spec: freeze decisions, diagnostician fixes P1-P5, scoring seeds, freeze v2

From: planning account. Date: 2026-10-12. Status: open. Decisions by Andrew on 2026-10-12, on the open items of `docs/proposals/2026-10-11_freeze-v1.md`, the questions in `results/2026-10-11c_world_smoothing_freeze/README.md`, and `docs/proposals/2026-10-12_diagnostician-misses.md`.

## Decisions
- Flank-difference tolerance: 1.00 %/h, from the basis rule as set. `enlarge_patch` 2x stays in the basis
- `strong` smoothing withdrawn from the remedy list. Reason: the bent clean rods fail plane sections after it
- `midline_jitter` at 3 px: not repairable; correct outcome decline. Follows from the withdrawal of `strong`
- `low_texture`: no repairable size; correct outcome decline at contrast 0.03
- The low_texture diagnostician run of build session 10 is not re-run. Seed 0 is development only
- `midline_jitter` label stays decline. Known limit, recorded in the freeze: at a 1.00 %/h tolerance the field is within tolerance, but plane sections fails it, because its predicted term uses the curvature rate of the jittered midline
- P1, P2, P3 (with the "no further setting" note), P4 and P5 of `2026-10-12_diagnostician-misses.md` approved as written. P5 reference from the 15 clean basis rods, for synthetic rods only. The reference for real movies stays open
- Scoring seeds: seeds 1 and 2 of the five development faults, plus seeds 3-5 labelled by tracker-only runs before any prompt change. Seed 0 is development only
- The freeze is approved from the v2 file this spec produces, not from v1

## Limits
- Shared-machine limits as built. Sweep lock: if another session holds it, wait
- About 150 tracker runs (item 3) and 5 diagnostician runs (item 6). More than 2 h of sweep wall time in total: stop and ask
- No diagnostician run on seeds 1-5 in this spec

## Work, in order

### 1. Record the decisions
- `docs/decisions.md`: one dated line per decision above, with its reason
- `config/scoring_tolerance.yaml`: flank-difference tolerance 1.00 %/h
- Check that `strong` is gone from every remedy setting list in code (`agents/actions.py`, `measure/remedies.py`) and from `describe()`. Remove it where it is still offered. Test: requesting `smooth_midline strong` is rejected as an unknown setting
- Recompute the labels of the development faults, seeds 0-2, under the 1.00 tolerance, from the existing runs (no new tracker runs). Report any label that changes. A changed label: stop and ask

### 2. Commit the scoring split before anything else changes
- `config/scoring_seeds.yaml`: development seeds [0]; scoring seeds [1, 2, 3, 4, 5]
- Commit and push this before item 3

### 3. Label seeds 3-5 (tracker only, no agent)
- The five development faults at their frozen sizes, seeds 3, 4, 5, through the same remedy settings and repair criteria used to label seeds 0-2. About 105-150 tracker runs
- Write the labels in the same table format as `results/2026-10-11_remedy_fixes/item4_faults.md`
- A seed 3-5 label that differs from the seeds 0-2 label of the same fault: stop and ask. Do not change any size
- Commit the labels before item 4. Prompt and info changes come after the labels are in Git

### 4. Apply P1-P5
- P1: the three check descriptions in `agents/prompts/diagnostician.md` as written in the proposal. `stage_log_summary` adds `closure_residual_px_per_h_at_moves` and `closure_residual_px_per_h_elsewhere`
- P2: the two prompt lines as written
- P3: the prompt line as written. The `apply_remedy` result states "no further setting" when the remedy has none left, computed from `REMEDIES` and the current settings
- P4: `velocity_profile` adds `flank_spacing_rate_pct_per_h` and its largest absolute value, from `rec.fields["spacing"]`. Prompt rule replaced as written
- P5: `frame_quality` adds the median and the lowest `texture_contrast` and `focus` over the 15 clean basis rods, fixed in config. The low-texture prompt line as written
- Tests: one per new field (value on a clean rod and on the fault it targets); the "no further setting" note appears after `smooth_midline light`; the prompt file contains each new line
- The rule-based baseline (branch `wip/baselines`) reads no prompt. When the single-agent baseline is built, it gets the same check descriptions (P1, P5)

### 5. Freeze v2, for approval
- `docs/proposals/2026-10-12_freeze-v2.md`: v1 with every decision above applied, the prompt by its new commit, the new info fields, the P5 reference values, the scoring seeds and their labels, and the `midline_jitter` known limit
- Open items: only the real-movie `frame_quality` reference, and anything this spec stopped on
- Do not tag. Andrew approves from this file

### 6. Check run on seed 0 (not a score)
- After item 5 is committed: one diagnostician run per development fault, seed 0, with the new prompt and info fields. 5 runs
- Report as in the build session 10 table, plus the first step where each run named the true fault
- These runs are labelled "development check" in the results README. They are not scored and no further change is made from them in this spec

## Stop and ask Andrew
- A label changes under the 1.00 tolerance (item 1)
- A seed 3-5 label differs from seeds 0-2 (item 3)
- A P1-P5 change cannot be made as written
- Any change to a fault, size, remedy, threshold, model or step limit other than those above
