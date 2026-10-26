# diag-analysis
Updated: 2026-10-25 15:55 (local)
Lane: course
Branch: wip/diag-analysis (status, task c021); code on wip/v4-candidate
Last inbox item done: 2
State: working
Now: item 3 (2) done; development check waits for free VM memory >= 4 GB (3.55 GB at 15:55)
Done since last update:
- item 3 (2): labels of seeds 26-28 committed before any agent run, 6b72d6a on wip/v4-candidate: 51 rods, accept_clean 18, accept_repaired 9, decline 24 (all-decline 24 of 51); 0 differ from the expected class
- label sweeps on the lab server: 228 tracker runs (144 + 84), 0 failed, standing limits; first start stopped itself at 13 runs on the 10 GB default (runner config lacked the 50 GB setting of 2026-10-24); restarted, cached runs skipped
Needs Andrew:
- none (free VM memory is under 4 GB; LLM runs wait for it)
