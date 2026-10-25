# real-calib
Updated: 2026-10-24 20:10 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: ready to merge
Now: section B done: real closure threshold 18 px/h in decisions; rigid invariance reported with its distribution, no threshold (item 4)
Done since last update:
- Replacement root 0714_c13 (proposal rule): w15-17 measured, w7-9 screened out; 12 measured windows, 4 experiments, minimums met
- Item 4: closure threshold only: 18 px/h (p95 17.35; median 3.50; 6.73 without the largest window). Rigid invariance reported: 6.52-97.8 %/h, median 35.8, p95 91.81. `results/2026-10-25_real_calibration/README.md`; decisions entry
- `python -m pytest -q tests`: 305 passed, 1 skipped. Log entry in `docs/running_log_pending/real-calib.md`
Needs Andrew:
- Closure threshold 18 px/h is set by one window (0711_c7 w7-9, 28.9 px/h; tip-side term 27.0 px/h); without it the p95 is 6.73. The rule keeps it; a rule change is yours
