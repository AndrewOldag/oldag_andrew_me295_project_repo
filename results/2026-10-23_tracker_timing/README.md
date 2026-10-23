# Tracker timing on one real window, and cost estimate

Spec `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md`, items B2 and B4 (cluster rules B3). Build account, dispatcher session, 2026-10-23. Lab-server timing only; cluster trials, if run, recorded below.

## Run (B2)
- Root `0708_m12` (drought experiment, mannitol, include yes, usable 0-24.01 h). Window 2-4 h of movie time: 80 frames, 2400 x 1200 px, about 90 s apart
- Uncoupled, `qb_track.py` defaults, `--movie real`, new `--from-h 2 --to-h 4` (reads only the window frames)
- Midline: `scripts/remote/real_midline.py`, provisional (dark-root segmentation, skeleton, longest path). No midline source exists yet for real movies
- Under the shared-machine limits: one single-thread job, `nice -n 19`, `ionice -c 3`, start only with 1 min load at most half the cores, no other tracker job of this account. Driver `scripts/remote/time_window.sh`
- Three runs. t1: 2-4 h, midline oriented base first (tip rule fixed after); timing sample only. t2: 2-4 h, tip first. t3: 4-6 h, tip first (the cluster trial window, for comparison)

| Run | Midline CPU s | Midline peak MB | Tracker wall s | Tracker loop s | Tracker peak GB | Output MB (track + midline) | Load 1 min before / after |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| t1 | 30.8 | 246 | 29.0 | 11.6 | 3.95 | 0.51 + 0.41 | 0.62 / 1.45 |
| t2 | 33.2 | 249 | 49.7 | 13.1 | 3.95 | 0.52 + 0.40 | 0.74 / 1.14 |
| t3 | 32.1 | 246 | 25.7 | 12.6 | 3.95 | 0.52 + 0.40 | 0.51 / 1.08 |

- Tracker wall time is mostly frame loading (system time 9-32 s); the tracking loop itself is 12-13 s for 80 frames x 27 points
- Numbers in `timing.json`

## Checker on t2 and t3 (uncoupled, no rigidly moved run)
- t2: closure failed, 68.2 px/h (threshold 1.0); plane_sections failed, 358 %/h (threshold 3.25). t3: closure failed, 76.5 px/h; plane_sections failed, 254 %/h. rigid_invariance: not run
- Cause found: the stage follows the tip during these movies. The montage folder's stage-position table is constant over the movie; the per-frame stage-tracking moves are in the folder's auxiliary data table (XYZ stage tracking, one triplet per frame; the first entries are -2.105 um in x per frame). The tracker's stage correction reads only the position table, so the correction is zero. Seen in the data: the tip stays near the same image column for 2 h while the mature tissue and background debris move away from it, about 67 px/h at 300-400 px from the tip
- Not one of the injected faults. Closest: `bad_stage_correction`, `rigid_drift`. Stopped here for Andrew (spec, "stop and ask")

## Cost estimate (B4)
`python results/2026-10-23_tracker_timing/estimate.py` prints `estimate.md`.

- 1.04 core-seconds per frame (midline + tracker, slower run t2)
- Each window tracked twice (rigidly moved copy for rigid invariance). Rendering the moved copy not timed
- Settings per window: low 1 (first run only), mid 3 (first run + 2 remedies), high 10 (every setting)
- Cluster rate $0.012 per core-hour, lowest tier (spec B3, Andrew, 2026-10-23). P100 or V100 GPU-hour $0.12
- Lab-server wall time at 4 workers. The 2 h per sweep limit splits the larger sets into several sweeps

## Reading
- Every set fits on the lab server: worst case (118 roots x 24 h, 10 settings) 652 core-hours, about 163 h at 4 workers. All include-yes roots once at 3 settings: 153 core-hours, about 38 h
- The cluster cost is small in every case (under $8). The cluster is not needed on cost or wall time for (a); for (b) it would shorten wall time only
- Not included: LLM agent calls, staging time, the stage-correction fix, a midline net in place of the provisional midline

## Cluster trials (B3)
- Connection to the cluster up; work folder made (empty folders for data, configs, runs, logs). No job submitted. Spend $0.00 by this session
- Stopped at the first data copy (one root's movie folder from the lab server to the cluster work folder): the copy command was refused by the build session's permission check. Not retried, not worked around. Needs Andrew
- No `cluster_spend.csv` entries yet

## Stage correction probe (inbox item 6, 2026-10-23)
- Cluster data copy for 0708_m12 (by the planning account) checked: 1931 files, names and sizes identical to the lab-server copy, 5,599,241,881 bytes
- The cluster runner reads stage motion from the same stage-position table as the lab tracker; neither reads the stage-tracking table. Both would run these montage movies with zero stage correction
- Stage-tracking table of 0708_m12: 961 rows (x, y, z), per-frame moves in whole pixels (0 to -8.42 um in x, 0 or -2.105 um in y). Sum over 4-6 h: -345 um in x (-164 px); basal tracked points move -149 px in the image over the same window
- Probe (lab server, outside the repo): t3 re-tracked with stage positions = table value + cumulative moves

| Run | Stage moves | closure px/h (threshold 1.0) | plane_sections %/h (threshold 3.25) | Tip, net px | Most basal point, net px |
| :-- | :-- | --: | --: | --: | --: |
| t3 | none | 76.5 | 254 | 7 | -149 |
| t3ap | + cumulative | 5.5 | 256 | 193 | 9 |
| t3am | - cumulative | 158.6 | 251 | -131 | -315 |

- With + sign the base is nearly still in the world frame and the tip advances about 96 px/h. Sign + is the correction
- Closure still above its threshold (provisional segmentation midline likely; not checked). plane_sections does not change with stage correction: predicted term -248 %/h from flank spacing x curvature rate; cause not checked
- Decision (Andrew, 2026-10-23): the correction goes into the tracker repo's loader, then the cluster runner install is updated. No cluster job is submitted until then. Nothing submitted; spent today $0.23 (the earlier runner test only)

## Stage correction in the tracker repo (inbox item 7, 2026-10-23)
- Tracker repo branch `stage-auxdata`, commit 888f972 (pushed, not merged). Tracker tests 46 passed, 9 skipped (9 new)
- Rule kept: stage positions = stage-position table + summed stage-tracking steps, sign +, step i = the move after frame i
- Background debris drift (world frame), no correction -> kept rule: t3 84.6 -> 2.6 px/h, t2 80.1 -> 1.1 px/h (spec limit 5 px/h): pass. Wrong sign: 159-167 px/h
- Course checker on the re-tracked windows (checker unchanged):

| Window | closure px/h (threshold 1.0) before -> after | plane_sections %/h (threshold 3.25) before -> after |
| :-- | :-- | :-- |
| t3 (4-6 h) | 76.5 -> 5.53 (fail) | 254 -> 257 (fail) |
| t2 (2-4 h) | 68.2 -> 11.20 (fail) | 358 -> 366 (fail) |

- Closure residual matches the remaining motion of the most basal tracked point (6.5 and 12.3 px/h): the 400 px tracked length ends inside the growth zone. plane_sections unchanged by the correction; cause not checked
- Scan of all 122 montage folders: 121 have a step count equal to the frame count. `0727_cc7` (include yes, usable 0-9.5 h): 155 steps for 857 frames; the loader raises on it. Flagged for Andrew (continue, Andrew, 2026-10-23)
- Private runner copy on the cluster with this branch: built; root listing works; loader confirmed on 0708_m12. The cluster jobs were not submitted: writing the job script was refused by this session's permission check. Not retried. Spent today $0.23 (earlier runner test only); no compute node used by this session

## Inbox item 8 (2026-10-23 afternoon)

### Closure against tracked length (lab server, stage-corrected loader, provisional midline)
| Window | 400 px | 700 px | 950 px |
| :-- | --: | --: | --: |
| t3 (4-6 h) | 5.53 | 0.65 (pass) | 4.71 |
| t2 (2-4 h) | 11.20 | 7.22 | 5.08 |
- Threshold 1.0 px/h. Not monotonic in length: tracked length alone does not explain the residual. Largest single-pair residual at the same frame pair in every run of a window (pair 7 in t3, pair 16 in t2). Checker and freeze unchanged
- Tracked chain (950 px) grows from about 939 to 1127 px over 2 h

### Plane sections
- 700 px, t3: 558 %/h; 950 px: 465 (t3), 440 (t2) %/h; threshold 3.25. Flank difference stays within +-7 %/h; the predicted term (flank spacing x curvature rate) carries the value
- Cause found: curvature noise of the provisional midline. At `curvature_smooth_px` 0 (frozen setting), the frame-to-frame change in curvature is 0.04-0.09 /px against a mean curvature near 1e-4 /px; at 29 px flank spacing this gives the -565 %/h predicted term at s = 575 px. The provisional midline is a pixel skeleton, resampled
- Rerun with the cluster runner's net midline: not done. Its previews fail (below)

### Cluster run, 0708_m12, 4-6 h, private runner copy (stage-auxdata 888f972)
| Job | Hardware | Queue wait | Elapsed | Midline s | QC s | Kinematics s | Peak memory (batch step) | Output | Cost |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| GPU | P100 + 4 cpus | 7 min 54 s | 11 min 15 s | 580 | 3 | 66 | 1.37 GB | 12 MB | $0.032 |
| CPU | 8 cpus | 0 min 37 s | 2 h 0 min 20 s, TIMEOUT | 6805 | 3 | not finished | 4.76 GB | 1.3 MB | $0.193 |
- GPU run status ok; 80 of 80 frames with a midline; `stage_source` aux_stage_tracking, 80 steps, 341.1 um travel (matches the lab-server validation)
- Previews fail: the ML and stabilized midlines end about 280 px short of the root tip, inside the meristem, on frames 0 and 79. Tip confidence median 0.18, maximum 0.25 (runner warning: weak on every frame). Runner kinematics (peak REGR 40 %/h at 42 um from the tip) are not valid. Stopped for Andrew; net settings not changed
- Per 2 h window on the P100: $0.032, of which the midline nets are 87 % of the time. 24 h root (12 windows): about $0.38. 1189 include-yes windows: about $38. 118 roots x 24 h: about $45. The lab server is free; its timing (about 1.04 core-s per frame with the provisional midline) stays the basis of the main estimate
- Spent today, all jobs, actual: $0.226 (earlier runner test) + $0.193 (CPU) + $0.032 (GPU) = $0.45, under the $5 cap
- On CPU the runner's midline nets take 85 s per frame on 8 cpus (GPU: 7.3 s per frame)
