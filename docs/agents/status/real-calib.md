# real-calib
Updated: 2026-10-24 20:00 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 3
State: ready to merge
Now: section B done: real-movie thresholds recorded in decisions (closure 18 px/h, rigid invariance 92 %/h; 12 control windows, 4 experiments, ft2, 1000 px)
Done since last update:
- Replacement root 0714_c13 (proposal rule): w15-17 measured, w7-9 screened out; 12 measured windows, minimums met
- Thresholds by the rule: closure 18 px/h (p95 17.35; 6.73 without the largest window); rigid invariance 92 %/h (p95 91.81); plane sections no threshold. `results/2026-10-25_real_calibration/README.md`; decisions entry
- `python -m pytest -q tests`: 305 passed, 1 skipped. Log entry in `docs/running_log_pending/real-calib.md`
Needs Andrew:
- Rigid invariance on real control windows at 1000 px is 6.5-98 %/h (median 36); at 92 %/h it passes nearly every window. Whether it gates on real windows stays your call (today: reported, not gating)
- Closure threshold 18 px/h is set by one window (0711_c7 w7-9, 28.9 px/h); without it the p95 is 6.73. The rule keeps it; a rule change is yours
