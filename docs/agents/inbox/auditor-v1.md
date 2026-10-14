# Inbox: auditor-v1

1. Worktree `../wt-auditor-v1`, branch `wip/auditor-v1` from current `main`. Do Task A of `docs/specs/2026-10-13_auditor-v1-real-frame-quality-labels.md`. When done and tests pass: log in `docs/running_log_pending/auditor-v1.md`, status `ready to merge`
2. A1 cache (Andrew, 2026-10-13): read the scored-v1 records where they are, in the scored-v1 worktree's `staging/`. Do not copy. Put the path in `private/`, not in a tracked file. Read only; write nothing there. The scored-v1 worktree is kept until the end of the project
3. Andrew, 2026-10-14: z cutoff 3 and the MAD-0 fallback are fixed, no longer provisional (`docs/decisions.md`). Update the proposal to say so, commit on a new branch `wip/auditor-v1b` from current `main`, status `ready to merge`. No runs
