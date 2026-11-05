# real-calib
Updated: 2026-11-05 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 17
State: ready to merge
Now: spec 2026-11-04 Work 1-7 done; batch 2 finished
Done since last update:
- Work 5: batch 2 finished: 90 of 91 roots (driver end 10:52), 0 jobs lost; job cap 4 (Andrew)
- Work 6: every batch-2 window checked on the cluster: 1061 of 1063; accept 925, decline 102 (18 not computable), failed 34, not run 2 (0727_cc7). `results/2026-10-25_full_batch_2/`
- Item 17: `results/2026-10-25_full_batch_2/audit/` (deletes, outputs, ledger, connection, reverify: 1060/1060 tracks, 1063/1063 check JSONs match)
- Work 7: decisions, log entry `docs/running_log_pending/real-calib.md`; tests 376 passed, 2 skipped
- Spend since 2026-10-23: $7.24 of $15
Needs Andrew:
- 0727_cc7 (2 windows): the tracker's loader rejects its stage-tracking table (155 steps for 857 positions). Count as not measured as now, or look at the data? Its staged root copy (4.8 GB) stays on the cluster until then
