# freeze-v31
Updated: 2026-10-24 11:46 (local)
Lane: course
Branch: wip/freeze-v31
Last inbox item done: 1
State: working
Now: item 2: sizing sweep 1 running on the lab server (114 tracker runs, 45 rods, seeds 10-12; log sweep_freeze_v31_20261024-114448)
Done since last update:
- Driver `scripts/synth/scored_v31.py` on top of the v3 driver (v3 code unchanged); `tests/test_freeze_v31.py` 3 passed; 1c1a548 (sweep code is fbd65bb, same synced code)
- second_root cause from the v3 runs: only plane_sections fails; crop_or_mask leaves every value unchanged; after `use_width_free_ratio` all applied checks pass and the centre is good, so methods accept (accept_on_decline). Alternative repair: remedy tree 3 of 3, diagnostician 9 of 9, single agent 6 of 9 (`results/2026-10-24_freeze_v3.1/second_root.md`)
- Sizes tried: rigid_drift 0.5-5.5 (unit 1), bad_stage_correction 3-8 px, displacement_exceeds_patch 2x2/2x3/2x4; width_change has one size at v3 geometry; stage_log_missing 1 is the largest size (judged from the v3 cache)
- Earlier status time 12:00 was wrong (VM clock); local time from the server
Needs Andrew:
- none
