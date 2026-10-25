# real-calib
Updated: 2026-10-24 19:30 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 1
State: waiting on dispatcher
Now: item 2 (section B): 11 of 16 calibration windows measured, below the 12 minimum; replacement root 0714_c13 (proposal order) needs ft2 midlines from the dispatcher's chain; thresholds wait for it
Done since last update:
- Calibration run on the lab server (1000 px, ft2): 11 measured, 4 screened out, 1 screen failed (probe error); interim table in `results/2026-10-25_real_calibration/README.md` (no threshold recorded)
- Interim (11 windows): rigid invariance p95 92.4 %/h (median 44.7); closure p95 18.4 px/h (median 3.70; 6.85 without the largest window); plane sections p95 365 %/h
- Script: probe errors recorded as screen failed; `--replacements`; host log appended
Needs Andrew:
- Heads-up, no action yet: on real windows at 1000 px, rigid invariance is 6.5-98 %/h (median 45) against 2.0 synthetic. A real threshold near 90 %/h would pass almost anything; whether rigid invariance should gate on real windows stays your call (it is reported, not gating, today)
