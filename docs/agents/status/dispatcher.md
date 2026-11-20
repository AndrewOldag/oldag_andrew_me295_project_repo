# dispatcher
Updated: 2026-11-20 14:45 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 45
State: waiting on Andrew
Now: item 46 (c027): ready to submit wave 1; meanwhile proposal B1, then run_all.py on cached windows
Done since last update:
- A1 scripts/retrack_queue.py (seed, jobs, submit, fetch) with fake-relay tests, 11 passed (a6b0e13). Coordinator: merge so real-calib can use it (spec C3)
- Wave 1 (A2): 84 windows (46 not reached by the c026 tree), 461 jobs not cached: stride double, smooth light, crop, mask, patch 1.5x and 2x, register (47 long); 3 moved-copy windows. Worst case $1.674
- Ledger (A3): last c026 figure in the ledger file $7.405 (one job after it, worst case $0.012, not finalized: master was down). Projected $7.42 + $1.67 = $9.09, under the $12 stop. The live `spent` figure needs the master; submit checks it per array
- Wave 1 stages whole root imgdirs in groups under 30 GB, not window frames: the tracker loader needs every frame file (decisions 2026-10-23, 2026-10-25; new entry 2026-11-20)
- Suite: 409 passed, 2 skipped, 2 failed; both failures are `tasks/c028-tracker-crash.md` front matter `state: open` (on main, not this session's file; board accepts queued, working, ...)
Needs Andrew:
- Open the cluster master to submit wave 1. Groups of about 5 roots fit under 30 GB, so wave 1 takes several submit/fetch rounds while the master is up
