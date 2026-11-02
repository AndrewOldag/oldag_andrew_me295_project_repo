# dispatcher
Updated: 2026-11-02 14:18 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 42
State: working
Now: task c023 item 43: 25 fixed-script batches done; 25 agent batches started (S0-S4 x seeds 0-4), waiting for free VM memory (another session's process holds 5.3 GB; floor 3 GB)
Done since last update:
- Item 43: proposal docs/proposals/2026-11-02_dispatcher-eval.md committed before any run (10d74c1)
- Harness scripts/dispatcher_eval.py: seeded per-window fault draws, preemption burst, approval requests answered "no change" in evaluation (run_agent_batch on_approval="deny"; default unchanged), S3 script rule; tests; suite 333 passed, 1 skipped (2d1d37f)
- Found and fixed before the agent runs: in the S3 script loop a refused cluster retry was given up when its root had another failed window (pattern from run_script_batch; harmless on the lab server)
- Item 42: README "Run the real slice" (7e043a9). Items 40 (2), 41: real-profile not-computable rule, first batch re-scored (51486cf)
Needs Andrew:
- none
