# dispatcher
Updated: 2026-11-14 14:00 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 45
State: ready to merge
Now: task c026 done with what ran: remedy tree on 38 of 84 batch-2 failing windows; diagnostician not run (Andrew, 2026-11-14). Results `results/2026-11-12_batch2_agents/`
Done since last update:
- Tree stopped at 38 when the cluster master went down about 23:10 on 2026-11-13: accepted after repair 9, declined 28, error 1; fixed script declines all 84
- README, tables.md, windows.csv (outcome and check values only), example_traces.md (plane-sections values masked); decisions; log in docs/running_log_pending/dispatcher.md
- Fixes this task: Link.run read to EOF (ca66ae6), Link.run 30 min channel timeout, clear_root .npz only, audit-only multi-window roots, tree real-profile gates (37d108b)
- Suite: 400 passed, 2 skipped
Needs Andrew:
- A staged root copy may remain on the cluster from the stop (master down); check and clear after an md5 check, or let the next c026 run clear it
