# dispatcher
Updated: 2026-11-22 17:19 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 57 (item 46, task c027, still working)
State: working
Now: c027 cycle running detached (status line after every group); after_wave.sh reruns the paused windows when the wave is done
Done since last update:
- Auto 11-22 17:19 (from logs): run 1189 records, accept by rule 1034, decline by diagnostician 23, decline by rule 58, paused 74; LLM calls 491; run ended: done; windows this start 74; LLM calls 491. Queue 452 tasks: done 3, failed 12, fetched 427, submitted 10; cycle last:  ; 0711_c5__w6-8 register_v2 track not fetched yet
- Items 56-57: main merged at a group boundary (zero-base lateral fix); the cycle kept running. The gate now applies on every remedy step including field-level rods (tracker-only exception removed); suite 447 passed, 3 skipped, test_info_p1_p5 passes. after_wave.sh reads run_all.py and the gate from disk when it starts, so the rerun uses the merged code
- 0711_c5__w6-8 for real-calib: base track and v1/other remedy tracks are in the c027 cache; its register_v2 track (`..._st1_regv2p1075b91__L1000.npz`) is not submitted yet: root 7 of 38 still to go, expected in the group after next (about 70 min). I will say in status when it is fetched
- Pace (item 57): groups g017-g020 took 30-40 min each: about 8 min staging, then register_v2 tasks of about 25 min; only one group fits under the 30 GB cap. Window-frame staging is not possible: the tracker loader reads every frame file of the imgdir and checks the count against the stage table, so a frame subset does not load (decisions 2026-10-23, 2026-10-25). Left: 149 jobs on 38 roots (72 register_v2), about 10 groups, about 6 h at this pace
- Cycle log: 17:09 g020 cleared (12 register_v2 tasks fetched, md5 checked)
- Run unchanged since the hold was lifted: 1,189 records, 74 paused waiting for their remedy tracks; LLM calls 491 of 900
Needs Andrew:
- Keep the cluster master up until the cycle logs `wave done` (about 6 h)
