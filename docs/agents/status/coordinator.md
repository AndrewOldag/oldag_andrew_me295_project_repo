# coordinator
Updated: 2026-10-23 00:50 (local)
Lane: course
Branch: main
Last inbox item done: 7
State: waiting on spec-audit
Now: sessions spec-audit, spec-audit-r, lab-report-2, dispatcher running; spec-audit-check starts when wip/spec-audit says ready to merge
Done since last update:
- Item 1: no unmerged course-lane branch says ready to merge; no merge, no test run
- Item 6: first start of the four new sessions did the coordinator inbox instead of their own (not told their names); no output beyond 2170ca5. Restarted at 00:40 with names; each now reads its own inbox
Branches (last commit, state):
- wip/spec-audit: 2026-10-23 00:49, working
- status/spec-audit-r: 2026-10-23 00:43, working (research lane, not merged)
- wip/lab-report-2: 2026-10-23 00:42, waiting on spec-audit
- wip/dispatcher: 2026-10-23 00:41, working
- wip/spec-audit-check: not started (waits for wip/spec-audit)
- wip/readme-check: 2026-10-17 15:26, merged
- wip/vm-setup: 2026-10-16 18:24, done, merged
- status/gate2: 2026-10-16 12:27, waiting on Andrew (research lane, not merged)
- wip/auditor-v1b, wip/fq-real, wip/auditor-v1, wip/scored-v1, wip/freeze-v2, heldout/faults, wip/baselines, wip/diag-review, wip/lab-report-1, wip/gatekeeper: merged
Needs Andrew:
- Local branch worktree-coordinator-c007 (b563b33, not pushed) duplicates 2170ca5 from the first start; keep or drop
- Board test test_board.py::test_research_rows_never_in_tracked_files fails at 2170ca5 (reported by lab-report-2): a research-lane task state 'waiting on Andrew' is not in the board's state list
