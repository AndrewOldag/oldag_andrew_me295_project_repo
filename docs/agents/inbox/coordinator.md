# Inbox: coordinator

1. Standing, every check: `git fetch origin`. For each course-lane branch whose `docs/agents/status/<name>.md` says `State: ready to merge`: merge it into `main` with `--no-ff`, run `python -m pytest -q tests` on the result, move `docs/running_log_pending/<name>.md` into `docs/running_log.md` in the merge commit, push. Tests fail: do not push the merge; write it under Needs Andrew. In your status, list each branch with its last commit time and state
2. Install the pre-push hook in the main repo folder if not installed: `sh scripts/hooks/install.sh` with the agents env active (Git's bash on Windows). Report whether `private/blocklist.txt` has any lines. Do not print its content
