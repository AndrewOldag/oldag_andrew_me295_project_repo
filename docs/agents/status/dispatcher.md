# dispatcher
Updated: 2026-10-23 01:40 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 2
State: waiting on Andrew
Now: B1, B2, B4 done; item 5 (cluster trials) stopped at the first data copy; B5 waits for approval
Done since last update:
- Item 2, B1: proposal `docs/proposals/2026-10-23_dispatcher.md` (23443d2)
- Item 2, B2: real-window timing on the lab server, 3 runs, `results/2026-10-23_tracker_timing/` (9bfb316 and this commit)
- Item 2, B4: cost estimate `results/2026-10-23_tracker_timing/estimate.md`; all sets fit on the lab server; cluster cost under $8 in every case
- Item 4: cluster rules read; rate $0.012 used in the estimate
- Item 5: private cluster file copied and read; connection check OK; one work folder found and made; no job submitted; $0.00 spent. Stopped: the data copy to the cluster was refused by this session's permission check
- Tests: 202 passed, 1 failed (test_board, research task r004 state 'waiting on Andrew' outside the repo; not this session's file)
Needs Andrew:
- Approve or change the dispatcher proposal (window 2 h and last-window rule, round limit 200, 2 retries per task)
- Timing root fails the checker in a way not in the fault list: stage-tracking moves are in the movie's auxiliary data table, not in the stage-position table the tracker reads; stage correction is zero on these montage movies. Which source to use, and in which code (course wrapper or tracker)
- No midline source for real movies on the lab server; the timing used a provisional segmentation midline. Use the cluster runner's midline nets, or another source?
- Cluster trials: the data copy (one root's movie folder, lab server to the cluster work folder) needs a permission rule for this session, or Andrew runs the copy. Also: trial plan says raw imgdir; recovery roots have only a montage folder, and raw folders alternate two tiles. Proposed: montage folder for all three
- Lab-server probe scripts and 2 preview images left in the timing work folder there (no deletes by sessions)
- test_board fails on research task r004 state 'waiting on Andrew' (research lane)
