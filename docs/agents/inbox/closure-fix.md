# Inbox: closure-fix

1. Read `CLAUDE.md`, `docs/agents/README.md`, `docs/specs/2026-10-24b_real-movie-push.md` (your section A and the Limits). Branch `wip/closure-fix` in your own worktree, never main. Task `tasks/c017-*.md`. First status, push
2. Do section A. When finished: `State: ready to merge`. Detached server or cluster jobs: done markers and `State: waiting on server job` as in the dispatcher's standing item
3. Planning, 2026-10-25 00:40, under Andrew's overnight delegation (00:21; hard limits: cluster spend cap \$15 total, no delete of anything a Claude session did not write on the workstation, lab server or cluster; never delete on Andrew's Mac). Freeze v3 and v3.1 scored items unchanged. Log: `docs/agents/overnight-2026-10-25.md`:
   - `scripts/remote/real_moved.py` writes `<name>.part` and renames it on the compute host; `CLAUDE.md` forbids renames on the lab server. Make it write-once like `qb_track.py`: write the final name directly, refuse if it exists. Test for the refuse case and for unchanged output on one cached window. Decisions entry (rules-2), log entry, status `ready to merge`
