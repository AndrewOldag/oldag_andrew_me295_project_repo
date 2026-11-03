# dispatcher
Updated: 2026-11-03 14:38 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 42
State: working
Now: task c023 item 43: rerunning 17 agent batches (S1 s3-s4, S2-S4) that hit the Claude session limit on 2026-11-02; 8 valid agent batches kept (S0 all, S1 s0-s2). Agent batches started so far 25 of the 60 cap; rerun brings it to 42
Done since last update:
- 2026-11-02: 17 agent batches ended in error from the seat's session limit (CLI "hit your session limit"), not agent behaviour; set aside in staging/c023/limit_errors/; harness now stops the run on that message instead of recording a batch (98cdb03)
- Item 43: proposal docs/proposals/2026-11-02_dispatcher-eval.md committed before any run (10d74c1)
- Harness scripts/dispatcher_eval.py: seeded per-window fault draws, preemption burst, approval requests answered "no change" in evaluation (run_agent_batch on_approval="deny"; default unchanged), S3 script rule; tests; suite 333 passed, 1 skipped (2d1d37f)
- Found and fixed before the agent runs: in the S3 script loop a refused cluster retry was given up when its root had another failed window (pattern from run_script_batch; harmless on the lab server)
- Item 42: README "Run the real slice" (7e043a9). Items 40 (2), 41: real-profile not-computable rule, first batch re-scored (51486cf)
Needs Andrew:
- none
