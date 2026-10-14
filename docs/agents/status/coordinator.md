# coordinator
Updated: 2026-10-13 21:21 (local)
Lane: course
Branch: main
Last inbox item done: 2
State: waiting on Andrew
Now: no branch ready to merge; waiting for wip/auditor-v1 and wip/fq-real
Done since last update:
- Merged wip/scored-v1 (2733c2c); 169 tests passed; decisions.md conflict kept both sides in date order
- Item 1: branches checked; none has a status file saying ready to merge
- Item 2: pre-push hook already installed in the main repo folder (ran on every push today); not reinstalled. `private/blocklist.txt` has 23 lines
Branches (last commit, state):
- heldout/faults: 2026-10-12 20:19, merged (a0cae6a)
- wip/baselines: 2026-10-12 20:18, merged (aa594c2)
- wip/diag-review: 2026-10-12 20:02, merged (781c9d0)
- wip/freeze-v2: 2026-10-12 22:00, merged (2606168)
- wip/gatekeeper: 2026-10-12 19:23, merged (main contained it at cbcb4ba)
- wip/lab-report-1: 2026-10-12 20:00, merged (f93203b)
- wip/scored-v1: 2026-10-13 00:01, merged (2733c2c)
- wip/auditor-v1, wip/fq-real: not on GitHub yet
- status/data-steward, status/gate2, status/litreview: not on GitHub yet
Needs Andrew:
- auditor-v1 A1 reads the cached final records of the scored runs. They exist only in the git-ignored staging folder of the scored-v1 worktree, not in the main repo folder. Choose: auditor-v1 reads them there, or the coordinator copies them into the main repo folder's staging (local copy, nothing on the server). Until then keep the scored-v1 worktree
