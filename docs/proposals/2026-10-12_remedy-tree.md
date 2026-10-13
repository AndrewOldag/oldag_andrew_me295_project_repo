# Rule-based remedy tree (baseline), fixed before any run

From: build account. Date: 2026-10-12. Written and committed before the tree is run on any rod. Not changed after a run; a change is a new file with a new date.

Uses only what is in the freeze list (`docs/proposals/2026-10-11_freeze-v1.md`): the remedies and settings of `agents/actions.py`, the approved checker thresholds (through pass or fail only), the roll-back rule (3/4) and the step limit 8. No new remedy, setting or threshold.

## What the tree reads
- The checker report of the current measurement: each check passed, failed, skipped on purpose (plane sections under the width-free ratio), or not computable
- The current frame stride (shown in the task, as for the diagnostician)
- The result of each remedy: kept, rolled back (by the orchestrator's rule, `agents/executors.py`), or not available
- Nothing else: no check values, no `request_info`, no truth, no rod name

## Steps and the step limit
- One remedy applied is one step, kept or rolled back or not available. `accept` and `decline` are one step each
- At most 8 steps, as the diagnostician. If the 8th step is a remedy, the task ends as `step_limit` (not reported)

## Rule 0: accept
- No check fails and every check is either passed or skipped on purpose: `accept`

## Rule 1: pick the list from the failing checks
- A check that is not computable (and not skipped on purpose) counts as failing
- The first failing check in this order picks the list: closure, rigid_invariance, plane_sections

| First failing check | Remedies, in order | Fault named with each remedy |
| :-- | :-- | :-- |
| closure | `register_frames`; `change_frame_stride` half; `enlarge_patch` 1.5x; `enlarge_patch` 2x; `smooth_midline` light | rigid_drift; displacement_exceeds_patch; low_texture; low_texture; midline_jitter |
| rigid_invariance | `change_frame_stride` half; `enlarge_patch` 1.5x; `enlarge_patch` 2x; `crop_or_mask` mask_second_root | displacement_exceeds_patch; low_texture; low_texture; second_root |
| plane_sections | `smooth_midline` light; `use_width_free_ratio` | midline_jitter; width_change |

- Reasons, from the check definitions (`docs/decisions.md`, 2026-10-10):
  - closure compares tip displacement from the stage log with the tracked kinematics: unlogged rigid motion first, then lost tracking (displacement too large for the patch, then too little texture for the patch), then a wandering midline
  - rigid_invariance fails when an added known rigid motion changes the profiles: a tracking failure (displacement, then texture), then a second object in the frame
  - plane_sections alone: the midline first (a measurement fault, repaired by a re-run); the width-free ratio last, as it removes the check instead of passing it

## Rule 2: take the next remedy in the list
- Skip a remedy already tried in this task, with one exception: `change_frame_stride` half may be applied again if its last application was kept (freeze: a remedy that lowered a failing check may be applied again)
- Skip `change_frame_stride` half when the frame stride is 1 (no step used)
- Skip `enlarge_patch` 1.5x once `enlarge_patch` 2x has been kept
- Apply the first remedy not skipped. Then go back to Rule 0 with the new checker report (a rolled-back remedy leaves the report as before)

## Rule 3: decline
- The list picked by Rule 1 has no remedy left: `decline`
- Fault named: the fault of the last remedy kept; if none was kept, the fault of the first remedy tried; if none was tried, `unknown`

## Fixed-parameter script (the other non-LLM baseline)
- One run with the base settings: the rod's own analysis stride, tracker defaults otherwise, uncoupled
- The checks are run and recorded but not acted on. Outcome `accept` in every task, one step

## Scoring
- Both baselines write the same output record as the orchestrator (`Outcome` in `agents/orchestrator.py`; summary as `scripts/demo_slice.py`) and are scored by the same functions in `measure/score.py`, against the labels and correct outcomes of the freeze list, at the approved tolerance

## Disclosure
- The author of this tree had read the earlier no-agent sweeps (`results/2026-10-10_repair_criteria/`, `results/2026-10-11_remedy_fixes/`), which show which checks fail for each development fault. The order of each list follows the check definitions above; it was not tried on any rod before this file was committed
