# turn-long
Updated: 2026-10-24 07:22 (local)
Lane: research
Branch: status/turn-long
Last inbox item done: 8
State: working
Now: inbox item 9, cause fixed and figures rerun (rc 0); next spec step 5 FINDINGS draft, step 6 independent review, step 7 hand back
Done since last update:
- Item 9 cause: the slope CIs and the point slopes came from different estimators (bootstrap moved blocks of steps; the OLS slope of the cumulative angle weights mid-span steps more). With a rate that changes over the span, CIs were off-centre; 2 of 315 difference rows (6 predicted-slope rows) had the estimate outside its CI. Not clipped
- Fix: residual block bootstrap with the time grid fixed (same block length, reps, pairing, point estimate); tracker repo commit c2a7512, branch offshoot-turn-interval2; earlier code path kept as the default for the 18 Oct runs
- Synthetic check: point inside CI under a trend (pass); stationary coverage 0.89 vs 0.92 for the old form at equal width (1000 reps)
- Rerun compare, drift, figures: rc 0, 0 of 315 rows outside their CI, 19 of 315 agreement calls changed; first outputs kept, rerun in a new subfolder
- One code export unusable (CRLF line endings, failed at parse, nothing run); re-exported with LF
Needs Andrew:
- none yet; the 18 Oct full-span run used the same bootstrap form (open item for the hand-back)
