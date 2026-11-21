## 2026-11-20 (build account, session real-calib, inbox item 19)
- Done: cause of the batch-2 `arange: cannot compute length` crash: tip point edge-frozen in every frame -> all arc lengths NaN -> `np.arange(0, NaN)` in `measure/record.py` `derive()`. Not a tracker error; tracks complete (md5 match)
- Done: fix and reproducing test (dc1cfe6); test fails before, passes after
- Done: equivalence, 5 batch-2 windows (one per condition): 5 of 5 records identical; no retrack needed
- Done: 21 of 33 arange windows checked on this machine from their batch-2 tracks: 21 not computable (decline by rule). 12 have tracks only on storage
- Tests: 399 passed, 2 skipped, 2 failed (`tests/test_board.py`: task files on main other than c028 use state `open`, not a board state), 262 s
- Demo: `python -m pytest tests/test_record_tracker.py` -> 5 passed; `results/2026-11-20_arange_fix/README.md`
- Remaining: C3 replanned (no retracks): checker on the 12 storage tracks, rows in batch 2 `windows.csv`; 0721_m5__w0-2 has no track (logistic fit error)
- Bottlenecks: planning (C3 plan); dispatcher (c027 board state)

## 2026-11-20 (build account, session real-calib, inbox items 20-21)
- Done: merged origin/main (a67866f); C3 as replanned: 12 batch-2 tracks copied from storage, read only, 12 of 12 md5 equal to the audit
- Done: `scripts/check_after_fix.py`: checker on the 33 arange windows on this machine, 33 not computable; 33 rows appended to `results/2026-10-25_full_batch_2/windows.csv` with `checked_after_fix` yes, 1061 batch-2 rows unchanged; rerun writes the same file
- Done: test `tests/test_check_after_fix.py` (rows kept, appended, rerun same); c028 done; c031 host field fixed for the board
- Demo: `QB_TRACKER=<tracker> python scripts/check_after_fix.py --tracks staging/tracks_real_fb2` -> 33 checked, 33 not computable
- Remaining: item 22 (c031, register_frames fix): proposal, diagnosis on the flagged c027 window, register_v2, integrity check; cluster runs after retrack_queue.py is on main
- Bottlenecks: `tests/test_board.py` fails on c027's host field (dispatcher); retrack_queue.py on main (dispatcher)

## 2026-11-20 (build account, session real-calib, inbox items 22-23)
- Done: proposal `docs/proposals/2026-11-20_registration-fix.md` before any run; flagged window found: 0711_c5__w6-8, c027, `st1_reg2p1075`
- Done: integrity check `checker/checks.py` `track_integrity` (336be10); flagged window: registered track 798 inversions, gap ratio 6.43, lateral 15.26 px; base track 3, 1.76, 1.03 px
- Done: thresholds by rule from 27 freeze v4 tracks: inversions 0, gap ratio 2.4, lateral 0.081 px (4ec36af); batch-1 base tracks: 0 of 115 pass all (lateral 0 of 115)
- Done: `register_frames_v2` and wiring (ea255ed and next); synthetic test: direct 0.03 deg error vs chained 1.2 deg; `scripts/remote/register_diag.py` written and tested, not run
- Tests: agents env 421 passed, 3 skipped after merging main (08de5b4); register tests 5 passed in the tracker env
- Demo: `python scripts/integrity_thresholds.py report --tracks staging/tracks_real_fb1 --out x.json` -> 115 tracks, 0 pass all
- Remaining: register_v2 and integrity check merged to main; R1 per-pair cluster job; R5 synthetic regression on the cluster
- Bottlenecks: Andrew (lateral threshold); planning (merge; job kind for register_diag); compound (synthetic-rod job kind)
