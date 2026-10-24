# real-calib
Updated: 2026-10-24 17:00 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 1
State: waiting on dispatcher
Now: item 2 (section B): the 16 calibration windows are queued in the dispatcher's c019 seg, copy and cluster GPU chain (its ledger), after C's windows; I wait for its bm/<window>.done markers, then build netmid, moved copies and tracking on the lab server in folder c018
Done since last update:
- Calibration set and rule committed before any compute: `docs/proposals/2026-10-24_real-calibration.md` (16 windows: 0708_c8, 0708_c9, 0711_c5, 0711_c7, 0714_c4, 0714_c9, 0721_c5, 0721_c6; 7-9 h and 15-17 h)
- Agreed with dispatcher: 0711_c7 stays in B (it was a C backup); replacement list cut to roots not reserved for C (0714_c13, 0711_c1); amended before any compute
- Fixed non-growing roots checked: other rig, about 0.84 um/px; not used
Needs Andrew:
- none
