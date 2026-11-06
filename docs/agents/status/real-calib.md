# real-calib
Updated: 2026-11-05 16:55 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 18
State: ready to merge
Now: item 18 done (Argon A5-F1 to F7); no track, check or cluster job run
Done since last update:
- A5-F2: all 170 deletes followed their lab-server md5 check (4-26 s); none before; stamp fixed (69bf6a6, 43ca938)
- A5-F1: 80 moved-copy tracks in outputs.csv and reverify (80/80 match); .npz.ok markers explained (69bf6a6)
- A5-F3: 0727_cc7 check JSONs are failure records, counted as not run (69bf6a6)
- A5-F4: ledger 98 jobs (3 added), times with offsets; spend $7.24 of $15 (69bf6a6)
- A5-F5: relay ControlMaster=no behind ssh -O check; master check before each step and submit (0e8e36e)
- A5-F6: sweep_start refuses a storage-only host before code sync (236711b)
- A5-F7: batch-2 driver and job script committed path-free, fake-ssh tests (b9976cf)
- Tests 382 passed, 2 skipped; decisions; log entry docs/running_log_pending/real-calib.md
Needs Andrew:
- 0727_cc7 (2 windows): count as not measured as now, or look at the data? Its staged root copy (4.8 GB) stays on the cluster until then
