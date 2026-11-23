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

## 2026-11-21 (build account, session real-calib, inbox items 24-25)
- Done: option A integrity gate: `checker/checks.py` `relative_integrity`; k from 9 freeze v4 repaired/base pairs: inversions 1.5, gap ratio 1.5, lateral 3.0 (`config/integrity_relative_k.yaml`); 8 integrity tests pass; committed before any real remedied track was scored
- Done: check on 44 c027 register_frames v1 tracks vs their base: batch 1 1 of 7 pass, batch 2 16 of 37; flagged 0711_c5__w6-8 fails (inversions ratio 200)
- Failed: R1 job not submitted; cluster master check failed 10:23
- Demo: `python scripts/integrity_thresholds.py relative --cache <freeze v4 cache>` -> k 1.5, 1.5, 3.0
- Remaining: R1 sbatch when the master is open; flagged window v2 through the gate; R5 with compound's rod job kind
- Bottlenecks: Andrew (cluster master); compound (rod job kind on main)

## 2026-11-22 (build account, session real-calib, inbox item 26)
- Done: merged origin/main (f12675c); own cluster work, code and stage folders for c031 (config git-ignored)
- Done: R5 `scripts/synth/register_v2_regression.py`: 6 freeze v4 register rods and moved copies re-rendered (truth equal within 1e-12), 12 tracker runs in one cluster array (7840638) through `scripts/rod_jobs.py`, 12 fetched, 0 failed, worst case $0.144
- Result: v1 repairs 6 of 6, register_v2 3 of 6; v2 closure lower on all 6 (0.04-0.22 px/h), v2 rigid invariance higher on all 6 and over 2.0 %/h on 3 (2.72, 2.75, 3.88); all 12 good against truth; all v2 plausible; option A gate passes all 12
- Done: R1 job submitted (7841039, root 0711_c5 staged in the c031 stage folder, 10.7 GB); running at 14:45
- Demo: `python scripts/synth/register_v2_regression.py report` -> the table in `results/2026-11-20_registration_fix/regression.md`
- Remaining: fetch R1; clear the staged root after the output is md5-checked on storage; flagged window v2 through the gate; decisions; ready to merge
- Bottlenecks: Andrew (R5 result: v2 vs v1 on rigid invariance); dispatcher (flagged window v2 track)

## 2026-11-22 (build account, session real-calib, inbox item 27)
- Done: merged origin/main (49bc3c1); R1 job 7841039 COMPLETED, output fetched (md5 equal on cluster, storage, VM)
- Result R1: v1's 9.23 deg is the sum of 79 pair rotations (mean 0.117 deg, largest 1.0 deg, pair ECC min 0.967); direct-to-frame-0 fit erratic on frames 1-20 (up to 6.0 deg), ECC fails on 59 of 79 frames, plausible false
- Done: staged root 0711_c5 deleted on the cluster (5.3 GB) after the md5 check, logged in DELETED.log
- Done: R5 README states the known limit (Andrew keeps register_v2); decisions
- Tests: 35 passed (integrity, executors, check_after_fix, record tests)
- Demo: `results/2026-11-20_registration_fix/README.md` sections R1 and R5
- Remaining: flagged window register_v2 track through the option A gate when dispatcher has fetched it; then ready to merge
- Bottlenecks: dispatcher (register_v2 retracks in its c027 cycle)

## 2026-11-22 (build account, session real-calib, inbox item 27, end)
- Done: flagged window 0711_c5__w6-8 register_v2 track (dispatcher c027, job 7859132 task 4, md5 ac89fc29 at fetch and here) through the option A gate: inversions ratio 414.3, gap ratio 6.85, lateral 79.5, plausible no (6.02 deg over 2 deg): fail. v1: 199.8, 3.65, 14.9: fail. `results/2026-11-20_registration_fix/flagged_window_gate.json`
- Demo: `python scripts/integrity_thresholds.py pairs --pairs <csv> --out <json>` -> per-pair ratios and gate; README section "Integrity gate, option A"
- Remaining: none for c031; ready to merge
- Bottlenecks: none

## 2026-11-22 (build account, session real-calib, inbox item 29)
- Done: c032 VM supervisor, build and test only: `scripts/ops/supervisor.ps1`, `scripts/ops/register_detached.ps1`, `scripts/ops/install_supervisor.ps1` (not run); `tests/test_supervisor.py` 12 passed in 86 s (fake clock, fake process table, fake memory, stub agents.ps1, temporary bare origin); `tests/test_ops.py`, `tests/test_board.py` 18 passed
- Demo: `powershell -File scripts/ops/supervisor.ps1 -Once` -> one heartbeat line on `ops/heartbeat`, e.g. `2026-11-22 22:00 free=8.0GB dispatcher=exited real-calib=exited,pending:inbox compound=exited start=real-calib dead=none`
- Remaining: switch-over after the c027 cut-off (Thu 26 Nov 12:00) on a planning inbox item
- Bottlenecks: none

## 2026-11-23 (build account, session real-calib, inbox item 30)
- Done: proposal `docs/proposals/2026-11-23_zone-checks.md` before any run (e385ae2); amended before any v4 or real record: plateau tip speed along the midline (f5cc997)
- Done: `checker/zone_checks.py` (plateau, particle path), `tests/test_zone_checks.py` 10 passed; `scripts/zone_checks.py`
- Done: synthetic, freeze v4 seeds 26-28: thresholds from 18 clean base tracks committed before the real run (3cf728b): plateau_regr 8.5 %/h, plateau_speed 0.018, pp_rms_rel 0.0044, pp_max_rel 0.0063
- Done: particle path flags 15 of 15 at every shift (-60 to +60 px); plateau 0 of 15 at every shift; false alarms 0 of 18 clean, 0 of 9 repaired
- Done: real, 1,189 c027 windows from the cache (1,186 computed, 3 paused without a track): either check flags 1,034 of 1,034 accepted base tracks; pp_rms_rel median 0.030 (7x the threshold). Largest residuals are a common offset: change of the first chain point's distance from the midline tip (corr -1.00); over 15 px on 143 of 1,127. No outcome changed
- Tests: 487 passed, 3 skipped without test_board.py, 198 s; test_board.py 8 passed, 2 failed on main's c033-audit.md host field (comma inside parentheses), not this branch
- Demo: `python scripts/zone_checks.py thresholds` -> same thresholds; writes `results/2026-11-23_zone_checks/synthetic.md`
- Remaining: merge; a real threshold only with a real reference set and Andrew's approval
- Bottlenecks: none
- Done (inbox 31): on-record shift confirmed as the fault set (amendment 6810f3a withdrawn); README limit added: fault model is an arc-length offset of the profile, not a zone misplaced by another tracker error. Main merged (b22e799; conflict markers removed in the next commit). No run, no cluster job

## 2026-11-23 (build account, session real-calib, inbox item 32, c035)
- Done: proposal `docs/proposals/2026-11-23_zone-reference.md` before the draw (bcf0733): seed 20261123, strata 5/4/5/5/5 by condition, one window per root, threshold rule on clean windows, step 1 stop rule
- Done: residual split in `checker/zone_checks.py` (`pp_common_*`, `pp_shape_*`); synthetic re-run (b3e4e90): shape flags 15 of 15 at every shift -60 to +60 px, 0 of 18 clean, 0 of 9 repaired (synthetic shape threshold 0.0019; shifted 0.045-0.18). c034 values reproduced 117 of 117
- Done: 24 accepted c027 windows drawn (`results/2026-11-23_zone_reference/sample.csv`)
- Done: 24 overlays in staging (not pushed), 3 frames per window plus tip-region zoom; frames read from storage read-only and deleted after use (ee01809)
- Tests: 502 passed, 3 skipped (full suite, 202 s)
- Demo: `python scripts/zone_reference.py synthetic --cache <freeze v4 track cache>` -> writes `results/2026-11-23_zone_reference/synthetic.md`, stop rule met
- Remaining: Andrew's labels; thresholds (Andrew approves); apply to all c027 windows; README, decisions; ready to merge by Fri 27 Nov 12:00
- Bottlenecks: labels, on Andrew
