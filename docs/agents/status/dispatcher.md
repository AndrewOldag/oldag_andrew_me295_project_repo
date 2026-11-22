# dispatcher
Updated: 2026-11-22 14:50 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 54 (item 46, task c027, still working)
State: waiting on Andrew
Now: c027 retracks wait for the cluster master (down since about 01:00); run pass done with failing windows held (item 54)
Done since last update:
- Auto 11-22 14:50 (from logs): run 1189 records, accept by rule 1034, decline by diagnostician 23, decline by rule 58, paused 74; LLM calls 491; run ended: done; windows this start 74; LLM calls 491. Queue 421 tasks: done 3, failed 12, fetched 402, submitted 4; cycle last:  
- Item 52 (1), cycle log, last lines: `2026-11-21 00:41 fetch: fetched 21 ... groups cleared g015`; `00:50 submit: g016, array 7425391, 24 tasks; 77 jobs wait`; `10:18 fetch: connection down (cluster master down)`; `10:18 exit: connection down`. Earlier stop: one fetch hung on the link 17:06-22:56. Reasons: link hang, then master down. Not the cap: groups of 3-4 roots kept fitting after each clear
- Status gap 00:35-10:00: the detached 2-hourly status pusher hung in `sleep 7200` and never pushed; stopped. The cycle now pushes a status line after every cleared group and every submit (52 (4))
- Item 52 (2): c026 leftover root cleared 2026-11-20 23:05 (item 51). 0727_cc7 leftover in c019: clear script ready (md5 check of its batch-2 outputs first, c019/DELETED.log); runs first thing when the cycle starts, needs the master
- Item 52 (3): a task live 2 h after its group's submit is cancelled and failed; a failed task is requeued once (tests 15 passed)
- Item 53: main merged (c031). register_v2 job lists: wave1_v2 122 jobs (86 register_v2, $0.891), wave1b_v2 76 jobs (11 register_v2, $0.297); v1 never submitted or used. Not submitted yet: master down
- Item 54: remedy hold until the integrity gate is on main: every failing window pauses before any LLM call. 12 final records that used a remedied track and their 8 roots' auditor runs set aside (staging/c027/run/held_remedy/)
- Run, all 1,189 windows have a record: 1,034 accepted by rule, 58 declined by rule, 23 declined by the diagnostician with no remedy tried, 74 paused (remedy hold or track not cached). 55 roots audited. LLM calls 491 of 900
- Queue: 16 groups; 378 tracks fetched md5 checked, 12 failed (rerun, fetched), g016 24 tasks submitted, state unknown since the master went down
- Cluster folder 24.1 GB of 30 GB at 23:05 (not readable now). Ledger spent $7.463 at 23:05
Needs Andrew:
- Open the cluster master and start me (`check github`): I start the cycle (cc7 clear, fetch g016, submit register_v2 and the rest)
- Integrity gate (option A, real-calib) on main: until then the 74 paused windows and the 12 held records wait
