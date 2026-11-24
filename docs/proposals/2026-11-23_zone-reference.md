# Proposal: real reference set and threshold for the particle-path zone check (spec 2026-11-23_zone-check-real-reference, task c035)

real-calib, 2026-11-23. Committed before the sample is drawn and before any value below is computed. Nothing below changes after the first result is seen; a change is a new dated line in `docs/decisions.md` with the reason.

## Residual split (step 1)
- Residual per centre point `e_j = S_pred,j - S_Tj` and tracked displacement `d_j = S_Tj - S_0j`, as in `docs/proposals/2026-11-23_zone-checks.md` (unchanged)
- Common mode: `pp_common_px = mean_j e_j` (signed). Shape: `e_j - pp_common_px`; `pp_shape_rms_px` = its RMS over the points, `pp_shape_max_px` = its largest absolute value
- Relative, over the RMS of `d_j` (as `pp_rms_rel`): `pp_common_rel = |pp_common_px| / RMS(d)`, `pp_shape_rel = pp_shape_rms_px / RMS(d)`. Largest `|d_j|` under 2 px: relative values not computable
- Gating pair for this task: `pp_shape_rel` (shape) and `pp_common_rel` (anchoring-drift flag). Added to `checker/zone_checks.py` `particle_path` as values; the c034 values and thresholds stay as they are

## Synthetic re-run (step 1)
- Same set as c034: the 18 freeze v4 `accept_clean` base tracks, the 15 growing ones shifted by -60, -30, -15, +15, +30, +60 px, the 9 `accept_repaired` tracks
- Synthetic shape threshold: R4 rule on `pp_shape_rel` over the 18 clean tracks (99.5th percentile x 1.5, rounded up to 2 significant figures). For this test only; not a real threshold
- Report detection by `pp_shape_rel` per shift (flagged of 15), and the common-mode share of the squared residual per shift
- Stop rule, fixed now: if `pp_shape_rel` flags fewer than 15 of 15 at any of the six shifts, the shape part does not still catch the shifted profiles. Status says so with the table and the task stops before the sample is drawn

## Reference sample (step 2)
- Pool: `results/2026-11-18_integrated_run/windows.csv` rows with `integrated` = `accepted` (1,034; the 2 `accepted after repair` windows are left out so the overlaid track is the reported one), root `include` yes in `manifest/root_manifest.csv`, window hours inside `usable_from_h` to `usable_to_h`, base track in the c027 cache with `pp_shape_rel` and `pp_common_rel` computable
- Strata: the `condition` column. 5 windows each from control, mannitol, mannitol then control, mannitol then mannitol; 4 from control then control (fewest accepted windows, 42). Total 24
- Draw: `numpy.random.default_rng(20261123)`, one generator for the whole draw. Conditions in sorted order; in each, the pool sorted by window id is permuted with `rng.permutation`; windows are taken in that order, skipping any window whose root is already in the sample, until the stratum is full (at most one window per root)
- Code `scripts/zone_reference.py sample`; writes `results/2026-11-23_zone_reference/sample.csv` (window ids, condition, order drawn). The pool and the draw do not look at any residual value beyond computability

## Overlays (step 3)
- Per sampled window: first, middle (index `T // 2`) and last frame of the window, with the frame's midline, the midline tip, the tracked centre chain (first point marked) and the predicted particle positions (each seed moved by `dS/dt = v(S)` to that frame, placed on that frame's midline at distance `S` from its tip)
- Frames are read from storage one window at a time, read-only; raw frames are deleted from the VM after the overlays are written. Overlays and `index.html` in `staging/c035_overlays/` (git-ignored, not pushed). The index shows no residual value or flag, so labels are blind to the check
- `labels.csv`: `window,label` with `label` in `clean`, `not clean`. Andrew writes it; the session waits

## Extension to 150 windows (inbox 33, Andrew, 2026-11-23 20:52)
Committed before the extra windows are drawn and before any threshold is computed. The first 24 windows, their overlays and Andrew's labels stay as they are.
- Pool: the same pool as step 2 (accepted, include yes, usable hours, base track with `pp_shape_rel` and `pp_common_rel` computable), less the first 24 windows
- Size: 126 more windows, 150 in total
- Strata: the `condition` column, in proportion to the accepted pool (1,034 windows: control 368, control then control 42, mannitol 291, mannitol then control 272, mannitol then mannitol 61). Allocation by largest remainder of `126 x pool / 1,034`; ties go to the condition first in sorted order. Result: control 45, control then control 5, mannitol 36, mannitol then control 33, mannitol then mannitol 7
- Per root: at most 2 windows in total, counting the first 24
- Draw: `numpy.random.default_rng(20261124)`, one generator for the whole extension. Conditions in sorted order; in each, the pool sorted by window id is permuted with `rng.permutation`; windows are taken in that order, skipping any of the first 24 and any window whose root already has 2 windows in the sample, until the stratum is full
- A stratum that runs out under the per-root cap stays short; the shortfall is reported in status and README. No window moves between strata
- Code `scripts/zone_reference.py extend`; appends rows 25-150 to `sample.csv` (column `draw`: 1 for the first 24, 2 for the extension). The draw does not look at any residual value beyond computability
- Overlays as in step 3, one window at a time, raw frames deleted after use; appended to `index.html` and to `labels.csv` (blank label) in sample order after the first 24, without changing an existing label
- Threshold rule (step 5) unchanged, computed once on all 150 labels. If fewer than 30 are `clean`, status says so before anything is computed

## Threshold rule (step 5)
- Set: the windows Andrew labels `clean`
- `pp_shape_rel` threshold: 99.5th percentile over the set (numpy linear interpolation) x 1.5, rounded up to 2 significant figures. Same rule for `pp_common_rel` (anchoring-drift flag)
- Fewer than 12 `clean` windows: no threshold; report the counts and ask Andrew
- The two values go to Andrew for approval before step 6. Not written to `config/zone_thresholds.yaml` before he approves; then to a new file `config/zone_reference_thresholds.yaml`
- Also reported, not used: the `not clean` windows' values, and whether each is over the thresholds

## Apply (step 6), report-only
- All 1,189 c027 windows, base track (and the accepted track where a remedy was kept), as in c034
- Counts flagged by shape and by common mode, per outcome class and per condition; example ids. No c027 outcome, threshold or scored result changes
- Synthetic: detection per shift at the approved real shape threshold (reported)

## Public values
- Residuals (px and relative), flag counts, thresholds, labels, window ids. No zone positions, REGR or velocity values, no `v_tip`. Per-window values stay on the VM outside the repo, except the 24 sampled windows' relative residuals and labels

## Outputs
- `checker/zone_checks.py` (added values), tests, `scripts/zone_reference.py` (`synthetic`, `sample`, `overlays`, `thresholds`, `apply`; reruns skip finished parts)
- `results/2026-11-23_zone_reference/README.md` (done marker), `synthetic.md`, `sample.csv`, `reference.csv` (after labels), `real_counts.md`
