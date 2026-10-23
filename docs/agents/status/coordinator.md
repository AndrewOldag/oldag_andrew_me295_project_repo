# coordinator
Updated: 2026-10-23 12:41 (local)
Lane: course
Branch: main
Last inbox item done: 9
State: working
Now: relay loop every 10 min (item 8): merges per item 1, `check github` to live sessions whose inbox changed
Last-seen main: 43576b6 (inboxes as of 43576b6)
Done since last update:
- Item 9: board allows `waiting on Andrew` and `waiting on <agent>` (`scripts/board.py`, `tasks/README.md`), 8223616; full suite 203 passed
- Item 1: merged wip/spec-audit (2c0eb60) and then wip/spec-audit-check (f7ec454), `--no-ff`; pending log entries moved into `docs/running_log.md`; suite 203 passed on each merge
- Item 8: pinged dispatcher 01:22 (inbox changed in 588f052). Coordinator inbox also changed (own). Message tool available: SendMessage + ListAgents
- Item 8: pinged dispatcher 12:41 (inbox item 7, 43576b6)
- Checks every 10 min, 01:35-12:30: no inbox change, nothing ready to merge, no pings
- dispatcher replied 11:00: item 6 held before submit (stage correction goes into the tracker first); no cluster job submitted
- Item 2: pre-push hook installed (ran on each push, 0 hits)
Branches (last commit, state):
- wip/spec-audit: 2026-10-23 01:04, ready to merge, merged 2c0eb60
- wip/spec-audit-check: 2026-10-23 01:14, ready to merge, merged f7ec454
- wip/dispatcher: 2026-10-23 11:00, waiting on Andrew
- wip/lab-report-2: 2026-10-23 00:42, waiting on spec-audit (spec-audit merged; inbox unchanged, so not pinged; needs a manual start)
- status/spec-audit-r: 2026-10-23 00:52, waiting on Andrew (research lane, not merged)
- status/gate2: 2026-10-16 12:27, waiting on Andrew (research lane, not merged)
- wip/readme-check, wip/vm-setup, wip/auditor-v1b, wip/fq-real, wip/auditor-v1, wip/scored-v1, wip/freeze-v2, heldout/faults, wip/baselines, wip/diag-review, wip/lab-report-1, wip/gatekeeper: merged
Needs Andrew:
- Local branch worktree-coordinator-c007 (b563b33, not pushed) duplicates 2170ca5; keep or drop
- Task c008 still `review` on the board (owner spec-audit); findings need Andrew's accept/reject marks (spec-audit status)
- spec-audit Needs Andrew items: rules-1 (hook hit in 304a3cb stays?), `status/gate2` on public remote (rules-4, specs-20), paper checks, fifth lab report
