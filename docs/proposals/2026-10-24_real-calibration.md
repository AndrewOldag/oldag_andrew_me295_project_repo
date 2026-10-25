# Real-movie calibration set and threshold rule

From: build account, real-calib session. Date: 2026-10-24. Spec 2026-10-24b, section B; task c018. Written and committed before any calibration value is computed. The threshold rule is Andrew's (2026-10-24); this file fixes the set and the details.

## Purpose
- A noise floor for the checks on real windows: the check values on control windows that the evaluation does not use
- Real-movie threshold per check = 95th percentile over the calibration windows, rounded up to 2 significant figures

## Eligible roots (rule)
- `include` yes in `manifest/root_manifest.csv`
- `condition` exactly `control`. The 0727 `control then control` roots are not used: their notes and flags name a medium exchange gap of about 40 min and lighting problems
- Montage folder present; `stage_tracking_log` yes; the stage-tracking table covers every window frame
- Empty `notes` and empty `flags` (the rule the real slice used for its roots, decisions 2026-10-24)
- Not in the section C subset; not 0708_m12, 0711_c2, 0721_m10
- Eligible by this rule: 0708_c5, c6, c8, c9; 0711_c1, c4, c5, c7; 0714_c10, c11, c12, c13, c4, c9; 0721_c1, c3, c5, c6

## Calibration set (fixed now)
- 4 experiments x 2 roots x 2 windows = 16 windows. Roots: the last 2 eligible roots of each experiment in manifest order. The section C subset picks after this list and leaves these roots out
- Windows: 2 h each, centred at 1/3 and 2/3 of the usable range: 7-9 h and 15-17 h (every eligible root is usable from 0 h to at least 23.88 h)

| Experiment | Root | Windows (h) |
| :-- | :-- | :-- |
| 20260708_drought_kinematics | 0708_c8 | 7-9, 15-17 |
| 20260708_drought_kinematics | 0708_c9 | 7-9, 15-17 |
| 20260711_drought_kinematics | 0711_c5 | 7-9, 15-17 |
| 20260711_drought_kinematics | 0711_c7 | 7-9, 15-17 |
| 20260714_drought_kinematics | 0714_c4 | 7-9, 15-17 |
| 20260714_drought_kinematics | 0714_c9 | 7-9, 15-17 |
| 20260721_recovery_kinematics | 0721_c5 | 7-9, 15-17 |
| 20260721_recovery_kinematics | 0721_c6 | 7-9, 15-17 |

- Replacement order, used only as stated below: 0714_c13, then 0711_c1 (the eligible roots not in the calibration set and not reserved for section C, picks or backups; amended 2026-10-24 before any compute, after the section C list was written)
- Fixed non-growing roots: not used. They were imaged on another microscope and camera at about 0.84 um/px, not the SlideBook montage rig at 2.105 um/px

## Screen (before any check value)
- The rule section C uses (dispatcher inbox item 29): a window is measured only if the ft2 net tip point lies within 15 px of the root-mask apex, median over 5 window frames (first, last and 3 evenly spaced between; `scripts/remote/tip_apex_probe.py`)
- A window that fails the screen, or whose midline or tracker run fails, is listed with the reason and left out of the percentile. It is not replaced, unless fewer than 12 windows or fewer than 3 experiments remain. Then the next replacement root is added, both windows, until both minimums are met

## Measurement (same as the real slice)
- Midline: ft2 net (`net2_midline_ft2.pt`), tile mode, low 0.1 %, high 99.5 %, window frames only
- Tracking: initial settings only (every frame, uncoupled, 1000 px tracked length; changed from 400 px by inbox item 3 after section A, before any value was computed). No remedy, no diagnostician. Thresholds come only from 1000 px tracks
- Per window also: tracked length reached, base arc length, world speed of the basal points, frame-0 midline length; a window whose frame-0 midline is shorter than 1000 px is flagged "base may be in growing tissue" (reported, not a gate, and not left out of the percentile)
- Rigid invariance: the whole-pixel moved copy against the cropped reference copy (decisions 2026-10-24). The threshold is set on the value the checker reports (full range). The profile-window value (s <= s_cov) is reported next to it, with its own 95th percentile, for information
- Closure: the definition section A kept (2026-10-10: midline end against the most basal centre point tracked in every frame), on the same 1000 px tracker outputs (the cropped reference copy is the measurement record)
- Rigid invariance at 1000 px is untested before this set (section A tracked no moved copy)
- Plane sections: computed and reported; no threshold (it stays reported, not gating)

## Threshold rule
- Per check: `numpy.percentile(values, 95)` (linear interpolation) over the windows that passed the screen, rounded up to 2 significant figures (for example 6.213 -> 6.3, 0.4471 -> 0.45)
- Reported with every window value, the count, minimum, median and maximum. Recorded in `docs/decisions.md` with the numbers
- Sensitivity, reported only (added 2026-10-24, before any value was computed): the two largest windows per check by name, and the 95th percentile with the largest window left out. With 16 windows the 95th percentile lies a quarter of the way from the second largest value to the largest, so one window can move it. No window is dropped after its value is seen; any change to the rule is Andrew's
- Synthetic thresholds and freeze v3 unchanged. Whether a check gates on real windows is not changed here (real-movie profile: closure gates)

## Limits
- The ft2 net was trained on traces from include-yes windows of many roots. Calibration roots may have a few traced frames in its training set; the subset roots may too
- Control roots only: the floor includes the tracker and midline noise of growing roots at control rates, not of stressed roots
- 16 windows: the 95th percentile lies between the two largest values

## Compute
- Midlines on the cluster GPU (P100 or V100), with the ledger check before every job; the spend since 2026-10-23 stays under $15 together with section C
- Copies, moved copies and tracking on the lab server: single thread, nice 19, at most 2 jobs of this account, 1-min load below half the cores. Frames stay on the lab server and the cluster work folder; nothing is deleted
- Every result is marked ft2 and with the closure definition used

## Extension to at least 40 windows (inbox item 5, Andrew 2026-10-24 19:35, option b)
Appended before any new value is computed. The first 12 measured windows stay as they are (`results/2026-10-25_real_calibration/windows/`); their values were seen (closure p95 17.35 px/h, superseded threshold 18 px/h). The rule is unchanged: 95th percentile, numpy linear, rounded up to 2 significant figures, over all measured windows. Closure only (item 4); rigid invariance and plane sections reported.

### Pool (same rules)
- `include` yes, `condition` exactly `control`, montage folder, stage-tracking table covering the window, empty `notes` and `flags`, inside usable hours, not in the final section C subset (0711_c2, 0708_c5, 0714_c10, 0721_c1, 0711_c4). Unused section C backups (0708_c6, 0714_c11, 0714_c12, 0721_c3) are no longer reserved and join the pool
- 14 roots, 4 experiments: 0708_c6, c8, c9; 0711_c1, c5, c7; 0714_c4, c9, c11, c12, c13; 0721_c3, c5, c6
- 3 windows per root, 2 h each: 7-9 h, 11-13 h, 15-17 h (every pool root is usable from 0 h to at least 23.88 h). 42 windows

### Windows
- The 12 measured windows: kept
- The 6 windows that dropped at the first screen (0708_c9 w15-17, 0714_c4 w7-9 and w15-17, 0714_c13 w7-9, 0721_c5 w7-9, 0721_c6 w7-9): screened again with the new tip rule. No check value was computed for them
- New: 11-13 h on the 9 roots already in the set (0708_c8, 0708_c9, 0711_c5, 0711_c7, 0714_c4, 0714_c9, 0714_c13, 0721_c5, 0721_c6); 7-9, 11-13 and 15-17 h on 0708_c6, 0711_c1, 0714_c11, 0714_c12, 0721_c3. 24 new windows

### Tip rule for every window screened from now on
- The tracking-polyline end within 50 px of the root-mask apex, median over the same 5 window frames (`median_end_to_apex_px` of `tip_apex_probe.py`; dispatcher inbox item 33). It replaces the net-tip-point rule, which jumps on some roots. The 12 measured windows passed the earlier rule and are not screened again
- A window that fails the screen, or whose midline, probe or tracker run fails, is listed with its reason and left out

### If fewer than 40 windows are measured
- Fixed now: add the two roots whose notes name no problem, in this order, 3 windows each at the same hours: 0708_c10 ("this root should be fine"), 0708_c11 ("should be fine"). If still fewer than 40, report the count reached and stop for Andrew; no other root is added

### Output
- New and re-screened windows go to `results/2026-10-25_real_calibration/windows_ext/` (the first files are not overwritten). The summary pools the 12 measured windows with the measured windows of `windows_ext/`
- Reported: threshold over all measured windows, the distribution (n, min, median, max, p95), and for information the two largest windows and the p95 without the largest
