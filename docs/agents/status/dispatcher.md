# dispatcher
Updated: 2026-11-23 01:50 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 58 (item 46, task c027, still working)
State: working
Now: wave done (cycle exited 01:00); after_wave.sh (pid 8208) runs the rerun of the paused windows and auditors: run_all.py (pid 676, since 01:03), log last written 01:45
Done since last update:
- Item 58 (01:45 start check): cycle.sh exited after `wave done` (01:00), as designed; after_wave.sh and one run_all.py are running. Last log lines: 0721_c1__w4-6 final decline, auditor 0721_c1 report; LLM calls 766 of 900. Nothing restarted; this session exits
- Item 58 (00:45 start check): cycle.sh (pid 7820, since 14:34) and after_wave.sh (pid 8208, since 14:39) are running, one of each; cycle log last line 00:44 (g031: fetched 1, not finished 5). Nothing restarted; this session exits
- Item 58 (23:46 start check): cycle.sh (pid 7820, since 14:34) and after_wave.sh (pid 8208, since 14:39) are running, one of each; cycle log last line 23:45 (g030: fetched 10, not finished 19; 63 jobs wait). Nothing restarted; this session exits
- Item 58 (22:45 start check): cycle.sh (pid 7820, since 14:34) and after_wave.sh (pid 8208, since 14:39) are running, one of each; cycle log last line 22:44 (g028: 2 tasks not finished). Nothing restarted; this session exits
- Auto 11-23 01:00 (from logs): run 1189 records, accept by rule 1034, decline by diagnostician 23, decline by rule 58, paused 74; LLM calls 491; run ended: done; windows this start 74; LLM calls 491. Queue 604 tasks: done 10, failed 24, fetched 570; cycle last: 2026-11-23 01:00 exit: wave done; for real-calib: 0711_c5__w6-8 register_v2 track and base are in the c027 cache
- Items 56-57: main merged at a group boundary (zero-base lateral fix); the cycle kept running. The gate now applies on every remedy step including field-level rods (tracker-only exception removed); suite 447 passed, 3 skipped, test_info_p1_p5 passes. after_wave.sh reads run_all.py and the gate from disk when it starts, so the rerun uses the merged code
- 0711_c5__w6-8 for real-calib: register_v2 track and base are fetched and in the c027 cache
- Pace (item 57): groups g017-g020 took 30-40 min each: about 8 min staging, then register_v2 tasks of about 25 min; only one group fits under the 30 GB cap. Window-frame staging is not possible: the tracker loader reads every frame file of the imgdir and checks the count against the stage table, so a frame subset does not load (decisions 2026-10-23, 2026-10-25). Left: 149 jobs on 38 roots (72 register_v2), about 10 groups, about 6 h at this pace
- Cycle log: 17:09 g020 cleared (12 register_v2 tasks fetched, md5 checked)
- Run unchanged since the hold was lifted: 1,189 records, 74 paused waiting for their remedy tracks; LLM calls 491 of 900
Needs Andrew:
- The wave is done (01:00); the cycle no longer needs the cluster master. The rerun is at 766 of 900 LLM calls; if it reaches the cap before the paused windows and auditors finish, it stops and this status says so
