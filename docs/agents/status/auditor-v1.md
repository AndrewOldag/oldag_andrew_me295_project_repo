# auditor-v1
Updated: 2026-10-13 23:55 (local)
Lane: course
Branch: wip/auditor-v1
Last inbox item done: 1
State: ready to merge
Now: item 1 done; Task A complete, tests pass (187)
Done since last update:
- Dev prompt rounds 1-3, 12 calls (b1055da, aa8483a, 23d93ef); held-out prompt fixed at aa8483a, recorded in the proposal
- Held-out: 12 runs (46a9d6f). False accepts flagged LLM 14 / 15 each run, rule 15 / 15; good reports flagged LLM 7, 5, 5 / 11, rule 5 / 11; alt_repair 0 / 9 both
- `results/2026-10-13_auditor_v1/README.md`, `scores.md`; log in `docs/running_log_pending/auditor-v1.md`
- 24 of 52 auditor calls used; 0 tracker runs
Needs Andrew:
- z cutoff 3 (provisional); MAD-0 fallback; batch statistics over all runs; `flag`/`clear` take run id lists. In the proposal
- Cached final records read in place from the scored-v1 worktree staging. Keep that worktree; the views are committed, so only rebuilding them needs it
