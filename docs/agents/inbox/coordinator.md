# Inbox: coordinator

1. Standing, every check: `git fetch origin`. For each course-lane branch whose `docs/agents/status/<name>.md` says `State: ready to merge`: merge it into `main` with `--no-ff`, run `python -m pytest -q tests` on the result, move `docs/running_log_pending/<name>.md` into `docs/running_log.md` in the merge commit, push. Tests fail: do not push the merge; write it under Needs Andrew. In your status, list each branch with its last commit time and state
2. Install the pre-push hook in the main repo folder if not installed: `sh scripts/hooks/install.sh` with the agents env active (Git's bash on Windows). Report whether `private/blocklist.txt` has any lines. Do not print its content
3. Andrew, 2026-10-14: keep the scored-v1 worktree to the end of the project. Item 1 applies to `wip/fq-real` and `wip/auditor-v1b` when ready
4. Planning, 2026-10-14: the four Python processes at 100% CPU since about 01:10 are the gate2 synthetic validation (research lane, about 6 h left). Do not stop them. `wip/auditor-v1b` is ready to merge (status pushed 13:29); merge per item 1. Slow test runs are expected until gate2 validation ends
5. Andrew, 2026-10-14: the VM stays loaded by gate2 validation for about 9 more hours. Merges continue as usual; run the full test suite once per merge, not more. No new runs on the VM until gate2 validation ends
