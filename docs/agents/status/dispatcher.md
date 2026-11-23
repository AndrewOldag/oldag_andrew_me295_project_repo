# dispatcher
Updated: 2026-11-23 08:15 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 59 (item 46, task c027, still working)
State: working
Now: waiting for the run cut-off Thu 26 Nov 12:00; then `run_all.py audit --final-now` for 0708_m9, 0721_m5, 0727_cc7, rerun report, ready to merge. No detached process running
Done since last update:
- start check 07:45: demo driver, demo_after.sh and tree rescore all ended normally; no cycle or run_all.py running; free memory 4.3 GB
- B5 demo done: 0708_c4 GPU job 7918920 collected 07:17 (12 tracks, md5 checked); agents and auditor 07:19-07:23, 22 LLM calls (cap 293)
- B5 vs cached run: same outcome 12 of 12 windows, closure equal to 2 decimals, same auditor flag (r07 summary outlier), same 9 cleared. Wall time: staging 2.6 min, cluster job 27.8 min, fetch 0.1 min, agents and auditor 3.5 min
- 2354ee4: `run_all.py report --demo DIR --roots ROOT` writes demo.md, with a test (test_run_all 16 passed). Suite 451 passed, 3 skipped, 2 failed (test_board, old c032 file on this branch; fixed on main)
- Tree rescore rounds ended 07:20: 3 windows stay paused (0708_m1, 0714_c9, 0727_cc6, all 10-12 h; their retracks failed twice; 0714_c9: stage-position file missing in the staged window). Tables unchanged from 07:20: tree 12 accepted after repair, 78 declined, 7 paused
- afc105f: results README (B7-B9), decision on the final-now audit at the cut-off, pending log entry
- Queue final: 616 tasks, fetched 576, failed 28, done 12; nothing to submit. Ledger $8.248 + demo worst case $0.252 = $8.50 of $15
Needs Andrew: none
