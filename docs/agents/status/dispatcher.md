# dispatcher
Updated: 2026-11-02 22:48 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 42
State: working
Now: task c023 item 43: agent batches running; S0 done (5 of 5 seeds: 1189/1189 collected, 15.0-15.25 h, 17-19 rounds, 37-44 LLM calls; script 15.0 h); S1 next
Done since last update:
- Item 43: proposal docs/proposals/2026-11-02_dispatcher-eval.md committed before any run (10d74c1)
- Harness scripts/dispatcher_eval.py: seeded per-window fault draws, preemption burst, approval requests answered "no change" in evaluation (run_agent_batch on_approval="deny"; default unchanged), S3 script rule; tests; suite 333 passed, 1 skipped (2d1d37f)
- Found and fixed before the agent runs: in the S3 script loop a refused cluster retry was given up when its root had another failed window (pattern from run_script_batch; harmless on the lab server)
- Item 42: README "Run the real slice" (7e043a9). Items 40 (2), 41: real-profile not-computable rule, first batch re-scored (51486cf)
Needs Andrew:
- none
