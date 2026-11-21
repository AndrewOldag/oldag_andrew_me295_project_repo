# dispatcher
Updated: 2026-11-20 23:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 51 (item 46, task c027, still working)
State: working
Now: c027 run (restarted 23:01) and wave-1 cycle running as detached hidden processes; register_frames held
Done since last update:
- Item 51: c026 leftover staged root 0711_m6 cleared with clear_root (5.3 GB, 3 tracks md5-checked; DELETED.log). Its one retrack that finished on the cluster after the c026 stop was copied to storage with md5 checks first
- Main merged (retrack-queue, c028). 34 base tracks of the arange windows fetched; they now decline by rule as not computable. The run's one arange error record set aside in staging/c027/run/superseded_arange/ and rerun
- Run stopped about 17:10 on the seat's session limit in the auditor of 0714_c13 (trace set aside); restarted 23:01, cut-off Thu 26 Nov 12:00
- Run at 464 records: 403 accepted by rule, 11 declined by rule, 10 declined by the diagnostician, 1 step limit, 39 paused; 175 LLM calls of 900
- Wave 1: 10 groups, 180 tracks fetched md5 checked, 12 failed and rerun; g011 submitting. 51 register_frames jobs held. A fetch hung from 17:06 to 22:56 on the link
- Cluster folder 24.1 GB of 30 GB (c027 15.1, c019 4.7, c026 0.0). Ledger spent $7.463
- Log entry docs/running_log_pending/dispatcher.md
Needs Andrew:
- Keep the cluster master up for the wave-1 cycle (about 290 short jobs left, about 10 groups)
