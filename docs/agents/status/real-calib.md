# real-calib
Updated: 2026-10-24 18:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 1
State: working
Now: item 2 (section B): `scripts/real_calib.py run` on the lab server (screen, moved copies, 1000 px tracking, checks), one job at a time; per-window files in `results/2026-10-25_real_calibration/windows/`
Done since last update:
- ft2 midlines of all 16 calibration windows built by the dispatcher's chain (cluster GPU job, 18 min, $0.050 on its ledger; spend since 2026-10-23 $0.92 of $15)
- Item 3: main (section A, 1000 px real tracks) merged into wip/real-calib; calibration tracking set to 1000 px (proposal amended before any value; the script refuses another length); per window: tracked length reached, base arc length, basal-point world speed, frame-0 midline length and the 'base may be in growing tissue' flag. On the three section A 1000 px tracks it reproduces A's base arc lengths (1092, 1087, 1065 px)
Needs Andrew:
- none
