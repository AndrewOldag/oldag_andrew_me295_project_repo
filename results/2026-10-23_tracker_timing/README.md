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
