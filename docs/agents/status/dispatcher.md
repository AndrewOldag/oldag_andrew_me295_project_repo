# dispatcher
Updated: 2026-10-25 21:09 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 38
State: working
Now: item 39 (task c022): agent run 4 over the 126 first-batch windows started 21:09 (all tracks cached, remedy tracks included); status every 20 windows
Done since last update:
- Run 3 finished all windows (123 collected, 3 given up after retries on the tracker 'arange' error; 9 declined among the first 119) but crashed printing the auditor's report (Unicode minus on the Windows console) before summary.json was written; results lost. Fix: summary.json written first, console escapes unencodable characters; decisions (81d4053). Run 3 traces in staging/c022/run3_no_summary/
- Run 2 stopped (ssh hang on a remedy retrack); fix: keepalive and fetch of a finished host track
- Run 1 failed at collect (one window's error aborted the batch); fix: the error fails that window only
- scripts/full_batch_agents_report.py (uncommitted until the run ends): public tables with outcome counts only; auditor comparison with numbers masked; traces and summary.json stay in staging (auditor text holds REGR values)
Needs Andrew:
- none
