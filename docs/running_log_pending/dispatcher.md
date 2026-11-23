## 2026-11-20 (build account, dispatcher session, task c027)
- Done: `scripts/retrack_queue.py` (seed, jobs, submit, fetch) with fake-relay tests (a6b0e13); alone on `wip/retrack-queue`, merged to main (2f7725a)
- Done: wave 1 job list, 84 batch-2 failing windows, 461 jobs, worst case $1.674; wave 1b, 10 batch-1 failing windows, 69 jobs, $0.234
- Done: proposal `docs/proposals/2026-11-18_integrated-run.md` committed before any run; `scripts/run_all.py` and tests; 1,189 windows in dispatcher order
- Done: 1,193 base tracks fetched storage -> VM cache, md5 checked, 0 missing (1,159, then 34 after the c028 fix)
- Done: integrated run started 14:01 on cached windows; at 464 records: 403 accepted by rule, 11 declined by rule, 10 declined by the diagnostician, 1 step limit, 39 paused; 175 LLM calls
- Done: wave 1 on the cluster from 14:30: 10 groups, 180 tracks fetched md5 checked, 12 failed (missing output folder; fixed, rerun); registration held (inbox 49), 51 jobs not submitted
- Done: 8 records that used a registered track and 6 roots' auditor runs set aside (`staging/c027/run/voided_register/`); c026 leftover staged root cleared after its md5 check, one missing c026 retrack copied to storage first
- Failed: one base-track fetch stopped on an SSH rekey timeout (Link.run fixed); one fetch hung after 17:06 until 22:56 (link); the run stopped once on the seat's session limit (auditor trace set aside)
- Demo: `python scripts/run_all.py windows` prints `1189 windows, 102 roots; batch {2: 1061, 1: 126, 'none': 2}`
- Remaining: wave-1 groups until nothing waits; rerun paused windows; register_v2 retracks after the fix; tree baseline (B4); fresh demo 0708_c4 (B5); report (B7-B9) by Thu 26 Nov 20:00
- Bottlenecks: cluster master up for the cycle (Andrew); register_v2 (real-calib, c031)

## 2026-11-21 (build account, dispatcher session, task c027)
- Done: run pass over all 1,189 windows: 1,034 accepted by rule, 58 declined by rule, 23 declined by the diagnostician (no remedy tried), 74 paused; 55 roots audited; 491 LLM calls
- Done: wave 1 to 16 groups, 378 tracks fetched md5 checked; cycle stopped 10:18 on master down (from about 01:00)
- Done: register_v2 job lists (97 register_v2 jobs, worst case $1.19 with the rest); v1 held; remedy hold until the integrity gate (12 records set aside); stuck-task and requeue-once rules with tests (15 passed)
- Failed: 2-hourly status pusher never pushed (`sleep 7200` hung in a hidden process); replaced by a push inside the cycle
- Demo: `python staging/c027/tools/counts.py` is local; `python scripts/run_all.py windows` prints the window count
- Remaining: master up -> cycle (cc7 clear, register_v2 and remaining retracks); integrity gate on main -> rerun paused windows with the diagnostician; tree baseline; fresh demo; report by Thu 26 Nov 20:00
- Bottlenecks: cluster master (Andrew); integrity gate option A (real-calib)

## 2026-11-23 (build account, dispatcher session, task c027)
- Done: tree rounds (B4) ended 05:48 after 8 rounds; the 2 jobs of 0708_m1__w10-12 failed twice and were not requeued
- Done: `run_all.py --roots` for the B5 demo, with a test (57044f4)
- Done: B5 demo of 0708_c4 started 06:47: root staged (5,347 MB) to a new cluster folder; GPU job 7918920 (worst case $0.252; ledger $8.50 of $15)
- Done: tree reruns the 38 c026-reached windows with register_v2 and the integrity gate (3c43f44); first pass 7 accept, 27 decline, 3 paused
- Done: report drops host folders from cluster error lines; draft tables, windows.csv, failure modes, example traces in `results/2026-11-18_integrated_run/`
- Demo: `python scripts/run_all.py report --run staging/c027/run --tree staging/c027/tree --out results/2026-11-18_integrated_run` writes tables.md: integrated 1034 accepted, 2 accepted after repair, 85 declined by agent; tree 12 accepted after repair, 78 declined
- Remaining: demo collect, agents and auditor on 0708_c4, compare with the c027 run; tree rescore rounds; results README (B9) by Thu 26 Nov 20:00
- Bottlenecks: none

## 2026-11-23 (build account, dispatcher, session 08:00)
- Done: B5 demo of 0708_c4 finished: GPU job collected 07:17 (12 tracks, md5 checked); agents and auditor 07:19-07:23, 22 LLM calls
- Done: demo vs cached run: same outcome 12 of 12 windows, closure equal, same auditor flag (r07 summary outlier); wall time staging 2.6 min, cluster job 27.8 min, fetch 0.1 min, agents 3.5 min
- Done: `run_all.py report --demo` writes demo.md, with a test (2354ee4); suite 451 passed, 3 skipped, 2 failed (test_board, old c032 file on this branch; fixed on main)
- Done: tree rescore rounds ended 07:20: 3 windows stay paused (0708_m1, 0714_c9, 0727_cc6, all 10-12 h; retracks failed twice)
- Done: results README for c027 (B7-B9)
- Demo: `python scripts/run_all.py report --run staging/c027/run --tree staging/c027/tree --out results/2026-11-18_integrated_run --demo staging/c027/demo --roots 0708_c4` prints `demo: same outcome 12 of 12 windows`
- Remaining: at Thu 26 Nov 12:00 `run_all.py audit --final-now` for 0708_m9, 0721_m5, 0727_cc7, rerun report, status ready to merge
- Bottlenecks: none; waiting for the cut-off
