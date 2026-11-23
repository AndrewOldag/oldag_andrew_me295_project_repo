# dispatcher
Updated: 2026-11-23 13:45 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 60
State: ready to merge
Now: idle; c027 done. Check github: no inbox item after 60. No detached process running (dispatcher-c027-audit exited)
Done since last update:
- item 60: `run_all.py audit --final-now --llm-cap 1300` 13:10-13:12: 0708_m9 and 0721_m5 audited over 11 of 12 windows each (4 calls each); 0727_cc7 not audited, both its windows paused, no final window (bc36328)
- report rerun: auditor 101 runs, 447 calls; all traces 1,015 of 1,300 calls; auditor flags 245; tables line now names the cap raise; results README, task c027 and pending log updated (bc36328)
- suite 485 passed, 3 skipped, 2 failed: test_board, `tasks/c033-audit.md` on main has host `VM (read-only, no cluster jobs)`, which board.py splits at the comma (planning's file, not edited)
Needs Andrew:
- none (planning: fix the c033 task host field, then merge wip/dispatcher)
