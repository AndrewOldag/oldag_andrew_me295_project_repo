## 2026-10-24 (build account, session closure-fix, task c017)
- Done: spec 2026-10-24b A. Tests (1)-(4) on the cached ft2 tracks of 0708_m12, 0711_c2, 0721_m10 (4-6 h): no definition closes at 400 px (2.73-20.43 px/h); `scripts/closure_definitions.py`, `results/2026-10-25_closure_definition/definitions.json`
- Done: cause found at the chain base, not at the tip: the 400 px base lies in the growth zone (world speed about 0 only past s = 550-650 px); base moved 5.4, 38.8, 11.1 px over 2 h. The chain starts at the midline end (gap 0 px), not 35 px behind it
- Done: chain-base test on the lab server, 9 tracker runs (400, 700, 1000 px; one at a time, single thread, nice 19, own task folder c017): closure at 1000 px 2.36, 3.17, 2.19 px/h; `scripts/closure_base_test.py`, `base_test.json`
- Done: stage checks: steps whole multiples of 2.105 um; sign + and lag 0 best on 0708_m12 and 0721_m10
- Done: fix: definition (1) kept, real windows tracked to 1000 px (`measure/real_runner.py`); decisions entry; v3 validation 153 values unchanged (largest change 0.0, `scripts/closure_v3_validate.py`); pytest 303 passed, 1 skipped
- Demo: `python scripts/closure_v3_validate.py --tracks staging/tracks_freeze_v3` prints max_diff 0.0 and pass_changed 0
- Remaining: B computes real thresholds with 1000 px tracks; C reruns its windows at 1000 px (new cache names, L1000); rigid invariance at 1000 px not yet tested
- Bottlenecks: none
