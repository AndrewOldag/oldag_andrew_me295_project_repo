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

- Replacement order, used only as stated below: 0708_c6, 0708_c5; 0711_c4, 0711_c1; 0714_c13, 0714_c12, 0714_c11, 0714_c10; 0721_c3, 0721_c1 (eligible roots, from the end of the manifest order)
- Fixed non-growing roots: not used. They were imaged on another microscope and camera at about 0.84 um/px, not the SlideBook montage rig at 2.105 um/px

## Screen (before any check value)
- The rule section C uses (dispatcher inbox item 29): a window is measured only if the ft2 net tip point lies within 15 px of the root-mask apex, median over 5 window frames (first, last and 3 evenly spaced between; `scripts/remote/tip_apex_probe.py`)
- A window that fails the screen, or whose midline or tracker run fails, is listed with the reason and left out of the percentile. It is not replaced, unless fewer than 12 windows or fewer than 3 experiments remain. Then the next replacement root of the experiment with the fewest windows is added, both windows, until both minimums are met

## Measurement (same as the real slice)
- Midline: ft2 net (`net2_midline_ft2.pt`), tile mode, low 0.1 %, high 99.5 %, window frames only
- Tracking: initial settings only (every frame, uncoupled, 400 px tracked length). No remedy, no diagnostician
- Rigid invariance: the whole-pixel moved copy against the cropped reference copy (decisions 2026-10-24). The threshold is set on the value the checker reports (full range). The profile-window value (s <= s_cov) is reported next to it, with its own 95th percentile, for information
- Closure: after section A is merged, with the A definition, on the same tracker outputs (the cropped reference copy is the measurement record)
- Plane sections: computed and reported; no threshold (it stays reported, not gating)

## Threshold rule
- Per check: `numpy.percentile(values, 95)` (linear interpolation) over the windows that passed the screen, rounded up to 2 significant figures (for example 6.213 -> 6.3, 0.4471 -> 0.45)
- Reported with every window value, the count, minimum, median and maximum. Recorded in `docs/decisions.md` with the numbers
- Synthetic thresholds and freeze v3 unchanged. Whether a check gates on real windows is not changed here (real-movie profile: closure gates)

## Limits
- The ft2 net was trained on traces from include-yes windows of many roots. Calibration roots may have a few traced frames in its training set; the subset roots may too
- Control roots only: the floor includes the tracker and midline noise of growing roots at control rates, not of stressed roots
- 16 windows: the 95th percentile lies between the two largest values

## Compute
- Midlines on the cluster GPU (P100 or V100), with the ledger check before every job; the spend since 2026-10-23 stays under $15 together with section C
- Copies, moved copies and tracking on the lab server: single thread, nice 19, at most 2 jobs of this account, 1-min load below half the cores. Frames stay on the lab server and the cluster work folder; nothing is deleted
- Every result is marked ft2 and with the closure definition used
