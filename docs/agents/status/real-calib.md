# real-calib
Updated: 2026-11-20 15:05 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 21
State: ready to merge
Now: items 19-21 ready to merge at be242a7; item 22 (c031) starting on this branch, nothing of it committed yet
Done since last update:
- Merged origin/main (a67866f)
- Item 21 (C3): 12 batch-2 tracks copied from storage, read only, 12 of 12 md5 equal to the audit; checker on all 33 arange windows on this machine: 33 not computable (decline by rule) (be242a7)
- Dispatcher: the 33 rows are on wip/real-calib in results/2026-10-25_full_batch_2/windows.csv, column checked_after_fix = yes, appended after the 1061 unchanged batch-2 rows (same window id twice; keep the last row)
- scripts/check_after_fix.py and tests/test_check_after_fix.py; c028 done; c031 host field fixed for the board
- 0721_m5__w0-2 (no track) and 0727_cc7 (2 windows) stay not measured, listed as failure modes in results/2026-11-20_arange_fix/README.md
Needs Andrew:
- none (tests/test_board.py still fails on the host field of tasks/c027-integrated-run.md: commas inside parentheses; dispatcher or planning)
