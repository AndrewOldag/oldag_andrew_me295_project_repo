# diag-analysis
Updated: 2026-10-25 21:58 (local)
Lane: course
Branch: wip/diag-analysis (status, task c021); code on wip/v4-candidate
Last inbox item done: 3
State: working
Now: item 4 (3): LLM runs on seeds 26-28 (306: diagnostician and single agent, 3 repeats), batches of 17, pushed after each batch
Done since last update:
- item 3 (3): development check, not a score, d75717b: diagnostician, switch on, v3 seed 20, 17 runs, 14 correct (v3 on the same seed and labels: 33 of 51 over 3 repeats); rigid_drift and bad_stage_correction now repaired and accepted; misses bend30 (v3 checker false alarm), second_root (accept_on_decline), partial_occlusion (step limit)
- item 3 (4): `docs/proposals/2026-10-25_freeze-v4-candidate.md`, b86abef
- item 4: tag `freeze-v4` (e9f19f2) pushed, after labels, dev check and proposal were committed
- free-memory floor 3.85 GB (Andrew, in session 15:58; decisions, c48cb98); dev check started at 4.19 GB free
- method states: 118 tracker runs in 5 rounds, 0 failed; 346 of 420 used
- rule methods: script and remedy tree, 102 runs, second run identical 102 (ed41bc0)
- LLM runs started 18:19 at 4.13 GB free. At 21:55: diagnostician r0, r1 and single_agent r0 51 of 51 each; single_agent r1 34 of 51; 0 harness errors. Batch loop stopped on a free-memory reading at the floor (3.85 GB by the loop, just under by the driver); resumed with a 3.9 GB wait
Needs Andrew:
- none
