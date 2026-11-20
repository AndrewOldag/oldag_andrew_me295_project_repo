# dispatcher
Updated: 2026-11-20 14:11 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 45
State: waiting on Andrew
Now: item 46 (c027): integrated run started on cached windows (staging/c027/run); wave 1 ready to submit
Done since last update:
- Run at 100 window records: 87 accepted (no failing check), 1 declined by rule, 5 declined by the diagnostician, 7 paused (track not cached); 4 roots audited; 36 LLM calls
- B1 proposal docs/proposals/2026-11-18_integrated-run.md committed before any run
- B2 scripts/run_all.py (windows, fetch, run, tree, audit, report) with tests; 1,189 windows in dispatcher order (126 batch 1, 1,061 batch 2, 2 of 0727_cc7)
- Base tracks: 1,159 fetched from storage to the VM cache, md5 checked, 0 missing. One fetch stopped on a paramiko rekey timeout; Link.run now treats it as a lost channel (decisions)
- Run started 14:01 with a 17:00 Sat cut-off for new windows. A failing window with no remedy track cached pauses before any LLM call (decisions)
- Wave 1b: batch-1 failing windows, 69 jobs, worst case $0.234 (c022 retracks seeded: 11)
- Correction: the times 14:45 and 15:30 in my previous status and task file were wrong; the VM clock read 13:2x then
Needs Andrew:
- Open the cluster master to submit wave 1 (461 jobs, $1.674) and 1b (69 jobs, $0.234). Projected spend $7.42 + $1.91 = $9.33 of the $12 stop. Several submit/fetch rounds while the master is up (groups of whole roots under 30 GB)
