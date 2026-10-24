# dispatcher
Updated: 2026-10-24 14:05 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 27
State: waiting on Andrew
Now: items 22-27 done: 3-root agent run with ft2 finished; closure fails on all 3 windows, all declined
Done since last update:
- 3-root agent run, wall 1459 s, `results/2026-10-24_real_slice_3roots/`: closure 0708_m12 4.52, 0711_c1 64.2, 0721_m10 4.66 px/h (threshold 1.0), all FAIL; rigid invariance 7.13, 63.4, 7.26; plane sections 214, 234, 168 (reported)
- Diagnostician: bad_stage_correction on all 3, residual at the logged stage moves; registration tried on 0708_m12 (3.61) and 0721_m10 (9.03), rolled back; decline x3. Auditor: 0 accepted; condition comparison given as context only
- Dispatcher agent: finish in 2 rounds, 3 windows collected. Log entry in `docs/running_log_pending/dispatcher.md`
Needs Andrew:
- ft2 closure regression: 0708_m12 4-6 h closure was 0.945 px/h (pass) with `net2_midline_ft.pt`, 4.52 with ft2; tracker, settings and window the same. Keep ft2 for real movies, or look into why first?
- 0711_c1 (the control root): closure 64.2 and rigid invariance 63.4, about 10x the others; ft2 tip confidence median 0.176. Replace it with another control root, or look into it?
