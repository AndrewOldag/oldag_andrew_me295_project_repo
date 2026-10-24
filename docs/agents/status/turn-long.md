# turn-long
Updated: 2026-10-24 01:50 (local)
Lane: research
Branch: status/turn-long
Last inbox item done: 9
State: working
Now: inbox item 10 part 2: one root rerun (span end moved) on the lab server, then tables recombined with summaries with and without the single-track rule (part 1)
Done since last update:
- Item 10 part 3 done: 18 Oct full-span CIs recomputed with the corrected bootstrap into this run's folder, read only on that run. Old form reproduces the 18 Oct tables byte for byte. Corrected form: tracker call unchanged (12 of 12 rows); point estimates unchanged; 3 primary-route CIs change whether they exclude 0; 19 diagnostic or check-only rows change too
- Item 10 code: tracker repo bbad8a1 (summaries both ways, combine script, bootstrap form selectable)
- One rerun folder used a wrong span start (it shifted the root's window grid, not only its end). Its outputs are marked unused in the run log; it could not be stopped from this session (process kill not permitted) and runs to its end inside new folders. Corrected rerun queued behind it with a window check
Needs Andrew:
- none
