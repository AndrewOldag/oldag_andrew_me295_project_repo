## 2026-11-20 (build account, session real-calib, inbox item 19)
- Done: cause of the batch-2 `arange: cannot compute length` crash: tip point edge-frozen in every frame -> all arc lengths NaN -> `np.arange(0, NaN)` in `measure/record.py` `derive()`. Not a tracker error; tracks complete (md5 match)
- Done: fix and reproducing test (dc1cfe6); test fails before, passes after
- Done: equivalence, 5 batch-2 windows (one per condition): 5 of 5 records identical; no retrack needed
- Done: 21 of 33 arange windows checked on this machine from their batch-2 tracks: 21 not computable (decline by rule). 12 have tracks only on storage
- Tests: 399 passed, 2 skipped, 2 failed (`tests/test_board.py`: task files on main other than c028 use state `open`, not a board state), 262 s
- Demo: `python -m pytest tests/test_record_tracker.py` -> 5 passed; `results/2026-11-20_arange_fix/README.md`
- Remaining: C3 replanned (no retracks): checker on the 12 storage tracks, rows in batch 2 `windows.csv`; 0721_m5__w0-2 has no track (logistic fit error)
- Bottlenecks: planning (C3 plan); dispatcher (c027 board state)
