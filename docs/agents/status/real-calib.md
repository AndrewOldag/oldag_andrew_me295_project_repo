# real-calib
Updated: 2026-11-23 23:59 (local)
Lane: course
Branch: wip/zone-reference
Last inbox item done: 33
State: waiting on Andrew
Now: c035 step 5: two thresholds computed on 150 labels; waiting for Andrew's approval before step 6 (apply)
Done since last update:
- Labels read: 150 of 150, 130 clean, 20 not clean (30 or more clean: rule applies)
- `scripts/zone_reference.py thresholds`, tests 7 passed (83752a4); `results/2026-11-23_zone_reference/thresholds.md`, `reference.csv`
- Thresholds (99.5th pct of clean x 1.5, 2 sf up): `pp_shape_rel` 0.14 (99.5th pct 0.087), `pp_common_rel` 0.5 (99.5th pct 0.33)
- On the reference set: shape flags 0 of 130 clean, 1 of 20 not clean (0708_m9__w22-24); common flags 1 of 130 clean, 0 of 20 not clean
- Synthetic at shape 0.14, for information: shifted +-60 px 15 of 15; +-15 and +-30 px 0 of 15; clean 0 of 15, repaired 0 of 9
- Not written to config
Needs Andrew:
- Approve or reject `pp_shape_rel` 0.14 and `pp_common_rel` 0.5 (`results/2026-11-23_zone_reference/thresholds.md`). Note: the values barely separate your labels (1 of 20 not clean flagged) and the shape threshold misses synthetic shifts up to 30 px. Then start me again for step 6
