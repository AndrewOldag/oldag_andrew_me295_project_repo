# Tracker timing on one real window, and cost estimate

Spec `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md`, items B2 and B4 (cluster rules B3). Build account, dispatcher session, 2026-10-23. Lab-server timing only; cluster trials, if run, recorded below.

## Run (B2)
- Root `0708_m12` (drought experiment, mannitol, include yes, usable 0-24.01 h). Window 2-4 h of movie time: 80 frames, 2400 x 1200 px, about 90 s apart
- Uncoupled, `qb_track.py` defaults, `--movie real`, new `--from-h 2 --to-h 4` (reads only the window frames)
- Midline: `scripts/remote/real_midline.py`, provisional (dark-root segmentation, skeleton, longest path). No midline source exists yet for real movies
- Under the shared-machine limits: one single-thread job, `nice -n 19`, `ionice -c 3`, start only with 1 min load at most half the cores, no other tracker job of this account. Driver `scripts/remote/time_window.sh`
- Two runs. t1: midline oriented base first (tip rule fixed after); timing sample only. t2: tip first

| Run | Midline CPU s | Midline peak MB | Tracker wall s | Tracker loop s | Tracker peak GB | Output MB (track + midline) | Load 1 min before / after |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| t1 | 30.8 | 246 | 29.0 | 11.6 | 3.95 | 0.51 + 0.41 | 0.62 / 1.45 |
| t2 | 33.2 | 249 | 49.7 | 13.1 | 3.95 | 0.52 + 0.40 | 0.74 / 1.14 |

- Tracker wall time is mostly frame loading (system time 13-32 s); the tracking loop itself is 12-13 s for 80 frames x 27 points
- Numbers in `timing.json`

## Checker on t2 (uncoupled, no rigidly moved run)
- closure: failed, 68.2 px/h (threshold 1.0). plane_sections: failed, 358 %/h (threshold 3.25). rigid_invariance: not run
- Cause found: the stage follows the tip during these movies. The montage folder's stage-position table is constant over the movie; the per-frame stage-tracking moves are in the folder's auxiliary data table (XYZ stage tracking, one triplet per frame, -2.105 um in x per frame in this window). The tracker's stage correction reads only the position table, so the correction is zero. Seen in the data: the tip stays near the same image column for 2 h while the mature tissue and background debris move away from it, about 67 px/h at 300-400 px from the tip
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
