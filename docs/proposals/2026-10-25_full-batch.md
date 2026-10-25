# Full batch of real windows: size, cost, limits, first batch

From: build account, real-calib session. Date: 2026-10-25. Inbox real-calib items 7 and 8 (planning account, under Andrew's overnight delegation of 2026-10-25 00:21). Written before any batch value is computed.

## Scope
- Every root with `include` yes in `manifest/root_manifest.csv`, usable hours only
- Windows by the dispatcher rule (`agents/dispatcher.py` `windows`, `config/dispatcher.yaml`): 2 h from `usable_from_h`; a last partial window is kept if at least 1 h long
- Per window: segmentation midline and frame list (lab server), ft2 net midline (cluster GPU), tracking midline, whole-pixel moved copy, two 1000 px tracks (lab server), checker with the real profile (closure gates at 19 px/h, decisions 2026-10-24; rigid invariance and plane sections reported). No remedy, no agent

## Size (recomputed in code from the manifest, 2026-10-25)
- 102 roots, 2368.1 usable hours, 1189 windows, 88 413 frames, 5 experiments, 11 experiment-condition groups
- Agrees with the planning account's count (inbox item 8)

| Experiment | Condition | Windows |
| :-- | :-- | --: |
| 20260708_drought_kinematics | control | 96 |
| 20260708_drought_kinematics | mannitol | 120 |
| 20260711_drought_kinematics | control | 105 |
| 20260711_drought_kinematics | mannitol | 96 |
| 20260714_drought_kinematics | control | 108 |
| 20260714_drought_kinematics | mannitol | 129 |
| 20260721_recovery_kinematics | control | 108 |
| 20260721_recovery_kinematics | mannitol then control | 144 |
| 20260727_recovery_kinematics | control then control | 55 |
| 20260727_recovery_kinematics | mannitol then control | 156 |
| 20260727_recovery_kinematics | mannitol then mannitol | 72 |

## Cost and resources (from measured runs)
- Cluster GPU midlines: the last 21-window job ran 24 min for $0.068 (P100, 4 cores), $0.0032 per window. All 1189 windows: about $3.85 and 23 GPU-hours. Worst case per job (2 h limit, 4 cores + 1 GPU): $0.336
- Cluster folder: about 0.43 GB of window frames per window (75 frames at about 6 MB). All windows: about 511 GB. The work folder cap is 40 GB
- Lab server time per window, single thread (calibration run log, 64 tracks and 32 moved copies): segmentation midline about 33 s, moved copy 6 s (4.5-9.1), two 1000 px tracks 66 s (25.7-40.9 s each). About 2 min per window. All windows: about 40 h for one job slot
- Lab server storage per window: moved and reference copies 0.86 GB, all other outputs under 0.01 GB. All windows: about 1.0 TB. The lab data disk has about 17 TB free (82 % used)

## Limits
- Sessions cannot delete on the cluster except window-frame copies a Claude session made in the c019 cluster task folder, after every midline output of those windows is on the lab server with matching md5 (inbox item 8, logged in `DELETED.log`). Without that, the 40 GB folder holds about 50 more windows before Andrew clears it
- With rolling staging: stage up to 35 GB, run, verify, clear, stage the next set
- Sessions cannot delete on the lab server. The moved copies of all 1189 windows would leave about 1.0 TB there for Andrew to remove. Open for Andrew: keep moved copies for every window, or only for a sample, since rigid invariance is reported, not gating
- Lab server: at most 2 jobs of this account (the dispatcher's runs count), single thread, nice 19, start only if the 1-min load is below half the cores
- Cluster: P100 or V100 only, ledger check before each job, total since 2026-10-23 under $15. Tonight's added worst-case cap: $3

## First batch (inbox item 7 (2))
- One root per experiment and condition, so the batch covers all 5 trials and all 11 groups
- Rule: in each group, the first include-yes root in position order (letters, then number) that is in neither the calibration set nor the section C subset (their windows are already processed)
- Every dispatcher window of each root: 11 roots, 126 windows

| Root | Condition | Usable h | Windows |
| :-- | :-- | :-- | --: |
| 0708_c2 | control | 0-24 | 12 |
| 0708_m1 | mannitol | 0-24 | 12 |
| 0711_c3 | control | 0-24.01 | 12 |
| 0711_m1 | mannitol | 0-24.01 | 12 |
| 0714_c5 | control | 0-23.88 | 12 |
| 0714_m1 | mannitol | 0-23.89 | 12 |
| 0721_c2 | control | 0-24.02 | 12 |
| 0721_m1 | mannitol then control | 0-23.99 | 12 |
| 0727_cc1 | control then control | 0-12 | 6 |
| 0727_mc2 | mannitol then control | 0-23.61 | 12 |
| 0727_mm1 | mannitol then mannitol | 0-23.64 | 12 |

- Expected: about $0.41 actual GPU spend, 4 GPU jobs (worst case $1.34), 54 GB staged in 2 fills, 4.2 h of lab-server time, 110 GB on the lab server
- Stops: cluster folder at 35 GB (then verify and clear before the next fill), or added worst-case spend at $3
- Order: by window index across the 11 roots (the first window of every root, then the second, and so on), so an early stop still covers every group
- A window whose segmentation, midline or tracking fails is listed with the step and the error, not retried with other settings
- Outputs: `results/2026-10-25_full_batch_1/`: windows done, checker outcome counts by condition, spend, folder size. No per-root strain-rate values
