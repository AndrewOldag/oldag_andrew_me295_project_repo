# real-calib
Updated: 2026-10-24 22:35 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 6
State: ready to merge
Now: items 5-6 done: real closure threshold 19 px/h from 41 control windows (supersedes 18 px/h); decisions entry
Done since last update:
- 48 windows, 16 control roots, 4 experiments; 41 measured (12 first, 23 planned extension, 6 fallback); 7 not measured (5 screen or probe, 2 measurement errors on 0714_c11)
- Closure: p95 18.87 -> threshold 19 px/h; median 3.60, max 28.9; without the largest window 17.47. Rigid invariance (6.4-201 %/h, median 27.5) and plane sections reported only. `results/2026-10-25_real_calibration/README.md`
- `python -m pytest -q tests`: 306 passed, 1 skipped. Log entry in `docs/running_log_pending/real-calib.md`
- Dispatcher to be told when merged (it holds its subset checks until then)
Needs Andrew:
- none
