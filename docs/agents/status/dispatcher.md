# dispatcher
Updated: 2026-11-23 04:15 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 59 (item 46, task c027, still working)
State: working
Now: tree baseline (B4) rounds running detached (tree_cycle.sh): round 1 group g032 submitted 03:59 (array 7903953, 5 track tasks; 3 jobs wait); after each wave the tree reruns its paused windows; at most 8 rounds
Done since last update:
- Diagnostician run finished 03:26 with --llm-cap 1300: 1,189 records; accept by rule 1034, accept by diagnostician 2, decline by rule 58, decline by diagnostician 85, step_limit 6, paused 4; LLM calls 1,007 of 1,300; auditor reports for 99 roots
- 4 windows stay paused (no track to fetch): 0708_m9__w10-12 (register_v2 ref/moved failed twice, g026 and g027), 0721_m5__w0-2, 0727_cc7__w0-2, 0727_cc7__w2-4 (st1 window track never queued; 0727_cc7 not measured, item 52)
- Tree baseline first pass 03:47-03:49 over the diagnostician windows the c026 tree did not reach: 4 accept, 43 decline, 8 paused (tracks not cached; 10 jobs, worst case $0.048). 0727_cc6__w10-12 register_v2 rows left out (failed twice, same error); that window stays paused
- start check 03:45: no run_all.py, cycle.sh or after_wave.sh running; free memory 4.2 GB
Next: tree rounds to the end -> fresh one-root demo B5 (0708_c4; after the tree rounds so cluster staging stays under 30 GB) -> `run_all.py report`, results README, windows.csv, example_traces.md (B7-B9) by Thu 26 Nov 20:00
Needs Andrew:
- Planning: `tasks/c032-vm-supervisor.md` on main has no front matter; `tests/test_board.py` fails 2 tests until it does
