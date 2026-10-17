# Inbox: readme-check

1. Andrew, 2026-10-16: check the README setup from a fresh clone, for the "README checked on" line in Lab report 1 (due Sun 18 Oct). Task file: `tasks/c006-readme-check.md`; read it first and mark parts done as you go
   - Branch `wip/readme-check`, in an Agent View worktree. Fresh clone of `origin/main` into a new folder outside the main checkout and outside `.claude/worktrees/`. Do not use the main checkout's env or `private/` in that clone. Never push from the fresh clone
   - `df` first. If the new env would take the VM near full, stop and put it under Needs Andrew
   - Follow README "Setup" steps 1-6 in order, as written, as a new user would:
     - Step 1: Miniforge is installed. Record its version; do not reinstall
     - Step 2: create the env under a new name so `me295` is untouched: `conda env create -f environment.yml -n me295-readme`. Record time taken and any solver warning
     - Step 3: Claude Code is installed and signed in. Check its version against `config/models.yaml`; do not reinstall or log in again
     - Step 4: `python scripts/check_cli.py`. One agent call; allowed. No other agent calls in this task
     - Step 5: `python -m pytest -q tests`. Record passed, failed, skipped and time
     - Step 6: run `sh scripts/hooks/install.sh` in the fresh clone, which has no `private/blocklist.txt`. Record what it does. Do not copy `private/` into the clone
   - No tracker runs. No lab server access
   - Record per step: command, result, time, and any place where the README text did not match what you had to do
   - README wrong or unclear: fix the README text only, on `wip/readme-check`. No code changes. A code fault goes under Needs Andrew, not fixed
   - Log entry in `docs/running_log_pending/readme-check.md`: date, commit checked, per-step results, test count. Status `ready to merge`
   - At the end, remove the fresh clone and the `me295-readme` env (VM only)
