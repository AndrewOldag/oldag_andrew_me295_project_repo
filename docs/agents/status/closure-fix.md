# closure-fix
Updated: 2026-10-24 17:03 (local)
Lane: course
Branch: wip/closure-fix
Last inbox item done: 2
State: ready to merge
Now: section A done; definition (1) kept, real windows tracked to 1000 px so the closure base lies in mature tissue
Done since last update:
- Cause: the 400 px chain base lies in the growth zone (world speed about 0 only past s = 550-650 px); it moved 5.4, 38.8, 11.1 px over 2 h. The chain starts at the midline end (gap 0 px), so the 35 px apical-segment hypothesis does not hold
- Tests (1)-(4) at 400 px: 2.73-20.43 px/h, none closes. At 1000 px: (1) 2.36, 3.17, 2.19; (2) 1.49, 2.98, 2.58; (3) 0.67, 2.51, 0.86; (4) 2.32, 3.09, 2.22 px/h
- (3) fails v3 validation (49 of 51 closure values changed, 10 outcomes); (2) not defined on synthetic rods; (4) adds 0.04-0.21 px. Kept (1)
- Fix `measure/real_runner.py` TRACK_LENGTH 1000 (21fc8c9); v3 validation 153 values, largest change 0.0, 0 outcomes changed; pytest 303 passed, 1 skipped
- Stage: steps whole multiples of 2.105 um; sign + and lag 0 best (0711_c2 does not separate)
- Lab server: 9 tracker runs in own task folder c017 (one at a time, single thread, nice 19, load 0.6-2.5 of 32); one 0.6 MB midline file copied there; nothing deleted
- Results `results/2026-10-25_closure_definition/` (48e7fd9); log entry `docs/running_log_pending/closure-fix.md`
Needs Andrew:
- none. For B and C: real thresholds and the subset runs must use 1000 px tracks (cache names L1000); closure at 1000 px is still 2.2-3.2 px/h against the synthetic 1.0, and the midline end outruns the first tracked material point by 1.0-3.3 px/h (kept in closure). Rigid invariance at 1000 px is untested
