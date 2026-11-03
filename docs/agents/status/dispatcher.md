# dispatcher
Updated: 2026-11-03 15:31 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 42
State: working
Now: task c023 item 43: rerun running; S0-S2 done (agent S2: 1160-1178/1189 collected, 18.0-18.25 h, 22-25 rounds, 72-78 calls; script 1099-1117, 17.0-17.5 h; retry rule differs, 2 vs 1, as in the proposal); S3 next
Done since last update:
- 2026-11-02: 17 agent batches ended in error from the seat's session limit (CLI "hit your session limit"), not agent behaviour; set aside in staging/c023/limit_errors/; harness now stops the run on that message instead of recording a batch (98cdb03)
- Item 43: proposal docs/proposals/2026-11-02_dispatcher-eval.md committed before any run (10d74c1)
- Harness scripts/dispatcher_eval.py: seeded per-window fault draws, preemption burst, approval requests answered "no change" in evaluation (run_agent_batch on_approval="deny"; default unchanged), S3 script rule; tests; suite 333 passed, 1 skipped (2d1d37f)
- Found and fixed before the agent runs: in the S3 script loop a refused cluster retry was given up when its root had another failed window (pattern from run_script_batch; harmless on the lab server)
- Item 42: README "Run the real slice" (7e043a9). Items 40 (2), 41: real-profile not-computable rule, first batch re-scored (51486cf)
Needs Andrew:
- none
