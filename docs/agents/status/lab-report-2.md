# lab-report-2
Updated: 2026-10-23 00:43 (local)
Lane: course
Branch: wip/lab-report-2
Last inbox item done: 2
State: waiting on spec-audit
Now: items 1-2 done (spec A1-A4); A5 waits for the audit SUMMARY.md and Andrew's marks; item 3 (ready by Wed 28 Oct) open
Done since last update:
- Draft `docs/reports/2026-10-30_lab-report-2.md` (277d9de): proposal, changes since Lab report 1, risks with actions, plan to 9 Dec, related-work note, repo and log section, progress, demo
- All commit hashes in the draft checked against git; numbers from the scored-v1 and auditor-v1 READMEs and the log
- Tests at 2170ca5: 202 passed, 1 failed, 89 s. Failure: test_board.py::test_research_rows_never_in_tracked_files; a research-lane task file outside the repo has state 'waiting on Andrew', not in the board's state list. Not changed by this session
- Log entry in docs/running_log_pending/lab-report-2.md
Needs Andrew:
- [ANDREW] line 17: literature-reviewer agents: keep in the plan or replace with the spec audit
- [ANDREW] line 61: held-out sample: add seeds under a new freeze version, or keep 15 per method
- [ANDREW] line 74: Lab report 5 date (not in Lab-Guideline.md)
- [ANDREW] line 82: related-work additions from the audit (spec A5, after marks)
- [ANDREW] line 100: recount commits on 30 Oct
- [ANDREW] line 102: log entries for spec audit, dispatcher and this report merged before submission
- [ANDREW] line 113: rerun tests after the board fix; replace the count
- [ANDREW] line 114: add the slice demo command if it runs by 30 Oct
- Proposal section is about 75 lines; trim to one printed page if needed
- Board test failure above: fix the research task state or the board's state list (coordinator or research lane)
