# auditor-v1
Updated: 2026-10-13 22:30 (local)
Lane: course
Branch: wip/auditor-v1
Last inbox item done: 0
State: working
Now: item 1, A4: LLM auditor prompt development on the 4 dev batches (round 1 running)
Done since last update:
- A1-A3 code and definition committed before any auditor run (99d70bd): `audit/view.py`, `audit/rule.py`, `audit/llm.py`, `agents/prompts/auditor.md`, `scripts/synth/auditor_v1.py`, `docs/proposals/2026-10-13_auditor-v1.md`; 187 tests passed
- All 160 final records found in the cache; no tracker runs
- Rule auditor on 8 batches (d15db20): every false accept flagged (dev 10/10, held-out 15/15); good reports flagged: dev tree 6/14, diagnostician 7/15
Needs Andrew:
- Cached final records read in place from the scored-v1 worktree staging (local links, read only). Keep that worktree until auditor-v1 is merged
- z cutoff 3 (provisional); MAD-0 fallback; `flag`/`clear` take run id lists (25 accepted runs, step limit 20). In the proposal
