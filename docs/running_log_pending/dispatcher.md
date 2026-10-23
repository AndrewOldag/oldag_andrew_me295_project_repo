## 2026-10-23 (build account, session dispatcher)
- Done, B1 (23443d2): `docs/proposals/2026-10-23_dispatcher.md`. Typed actions split_root, estimate_cost, request_approval, submit, wait, collect, retry, finish; orchestrator enforces budget and shared-machine limits; fixed-script baseline; fake-queue tests. No dispatcher code until Andrew approves
- Done, B2 (9bfb316): one real window timed on the lab server, root 0708_m12 (drought, mannitol), 80 frames per 2 h window, uncoupled, one single-thread job at lowest priority. Midline 31-33 CPU s, 0.25 GB; tracker 26-50 s wall (tracking loop 12-13 s), 3.95 GB peak; output 0.92 MB per window. Load (1 min) at most 1.45 of 32 cores
- New: `qb_track.py --from-h --to-h` (window only); `scripts/remote/real_midline.py` (provisional midline); `scripts/remote/time_window.sh` (load check, nice, ionice, `/usr/bin/time -v`)
- Checker on the timing root failed, t2 (2-4 h) and t3 (4-6 h): closure 68.2 and 76.5 px/h (threshold 1.0), plane_sections 358 and 254 %/h (threshold 3.25). Cause: stage-tracking moves are in the movie's auxiliary data table, not in the stage-position table the tracker reads, so stage correction is zero. Not in the fault list. Stopped for Andrew
- Done, B4: `results/2026-10-23_tracker_timing/` (README, timing.json, estimate.py, estimate.md). 1.04 core-s per frame. All 102 include-yes roots once at 3 settings per window: 153 core-hours, about 38 h at 4 lab-server workers, $1.84 on the cluster. Worst case 118 roots x 24 h x 10 settings: 652 core-hours, $7.83
- B3 cluster trials: connection up, work folder made, no job submitted, $0.00 spent. The first data copy to the cluster was refused by the session permission check; not retried
- Tests: 202 passed, 1 failed (`tests/test_board.py::test_research_rows_never_in_tracked_files`: a research task file outside the repo has state 'waiting on Andrew', not in the board's state list; not this session's file), 130 s
- Demo: `python results/2026-10-23_tracker_timing/estimate.py` prints the cost table
- Remaining: Andrew approves or changes the proposal; stage-correction source for real movies; cluster copy permission; then B5 (dispatcher, real slice)
- Bottlenecks: proposal approval, stage-tracking table, cluster copy permission (Andrew)

## 2026-10-23 (build account, session dispatcher, inbox item 6)
- Done: cluster copy of 0708_m12 checked against the lab-server copy: 1931 files, same names and sizes, 5,599,241,881 bytes
- Done: two runner configs (CPU, P100) and a ledger check script written, both outside the repo. Spent today $0.23 (earlier runner test). P100 nodes free at check time
- Found: the cluster runner, like the lab tracker, reads no stage-tracking table; montage movies get zero stage correction
- Done: probe on the lab server, t3 re-tracked with cumulative stage-tracking moves: closure 76.5 -> 5.5 px/h (sign +), 158.6 px/h (sign -); plane_sections 254 -> 256 %/h, unchanged. `results/2026-10-23_tracker_timing/README.md`
- Decision (Andrew): stage correction goes into the tracker repo loader, then the runner install; no dispatching before that. Cluster jobs not submitted
- Demo: `python results/2026-10-23_tracker_timing/estimate.py` prints the cost table
- Remaining: stage correction in the tracker repo and runner (Andrew or research lane); then the two cluster jobs; closure residual 5.5 px/h and plane_sections on real movies; proposal approval
- Bottlenecks: tracker-repo stage correction (Andrew); proposal approval (Andrew)

## 2026-10-23 (build account, session dispatcher, inbox item 7)
- Done: tracker repo branch `stage-auxdata` 888f972: stage-tracking table reader, summed positions for constant stage tables, `stage_source`, raw two-tile folders raise; tracker tests 46 passed, 9 skipped
- Done: validation on 0708_m12 t2, t3 (lab server): background drift 80-85 -> 1-3 px/h with sign +, step after frame; pass. Course checker closure t3 76.5 -> 5.53, t2 68.2 -> 11.2 px/h (fail; tracked length inside growth zone); plane_sections unchanged
- Done: scan of 122 montage folders: 121 counts match; 0727_cc7 155 steps for 857 frames, flagged
- Done: private runner copy on the cluster with 888f972; root listing works
- Failed: cluster job script not written; permission check refused it. No job submitted; no compute node used
- Remaining: permission or Andrew to write and submit the 2 cluster jobs; 0727_cc7 decision; proposal approval
- Bottlenecks: cluster submit permission (Andrew); 0727_cc7 (Andrew)
