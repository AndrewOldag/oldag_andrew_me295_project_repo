# real-calib
Updated: 2026-11-23 23:46 (local)
Lane: course
Branch: wip/zone-reference
Last inbox item done: 34
State: ready to merge
Now: c035 done; waiting for merge of wip/zone-reference and the next inbox item
Done since last update:
- Thresholds to `config/zone_reference_thresholds.yaml` (0.14, 0.5), decision dated 2026-11-23
- Step 6, 1,189 c027 windows report-only (`real_counts.md`): accepted base 8 of 1,034 flagged (shape 3, common 5); declined by agent 11 of 85; 3 tracks not cached; no outcome changes
- Detection curve (`curve.md`, sizes committed before the run in 1a023ff): false alarms shape 0 of 130, common 1 of 130. Shape: 15-30 px 2 of 130, 60 px 10, 90 px 101 (0.78). Common: 4 patch spacings toward the tip 90 of 130 (0.69), away 11 of 130
- Smallest size caught in at least 90 % of windows in both directions: none in the tested range for either check. At these thresholds the checks catch only gross misplacement on real windows; stated in the README
- Tests: `tests/test_zone_reference.py` 9 passed, `tests/test_zone_checks.py` 12 passed
Needs Andrew:
- none (for information: the curve shows low sensitivity at the approved values; values unchanged as instructed)
