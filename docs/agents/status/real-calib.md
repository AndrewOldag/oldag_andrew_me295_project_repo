# real-calib
Updated: 2026-11-20 13:40 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 19
State: ready to merge
Now: item 19 C1, C2, C5 done; C3 needs a new plan (no retrack needed); no cluster job, no LLM run
Done since last update:
- C1: cause is not the tracker. Tip point edge-frozen in every frame (tip on the image border) -> all arc lengths NaN -> np.arange(0, NaN) in measure/record.py derive(). Fix: empty grid, closure not computable (decline by rule). Reproducing test fails before, passes after (dc1cfe6)
- C2: checker rerun with the fix on 5 batch-2 tracks (one per condition): 5 of 5 records identical, track md5s match the audit. Tracks unchanged, so no retrack
- 21 of 33 arange windows checked on this machine from their batch-2 tracks: 21 not computable. 12 have tracks only on storage. 0721_m5__w0-2 is a different tracker error (logistic fit), no track
- results/2026-11-20_arange_fix/, decisions, log entry docs/running_log_pending/real-calib.md, task c028
- Tests 399 passed, 2 skipped, 2 failed: tests/test_board.py, task files on main (c027 first) use state 'open', not a board state
Needs Andrew:
- C3 plan: the 33 arange windows need no retrack, only the checker on their existing tracks. Proposal: copy the 12 storage tracks to the VM (md5), check them here as for the 21, add the 33 rows to batch 2 windows.csv with column checked_after_fix (spec says tracked_after_fix). 0721_m5__w0-2 (no track) and 0727_cc7 stay not measured. Go ahead?
- Board: task files c027, c029, c030 on main have state 'open'; tests/test_board.py fails until they use a board state (planning to fix on main)
