---
id: c018
title: Real-image noise floor and real-movie thresholds
lane: course
owner: real-calib
state: working
branch: wip/real-calib
host: cluster, lab server (light)
created: 2026-10-24 16:45
last_update: 2026-10-25 17:25
blocker: none
done_marker: proposal committed first; thresholds in decisions
---

Spec: `docs/specs/2026-10-24b_real-movie-push.md`, section B.

## Parts
- [done] Calibration set and rule committed before compute
- [done] ft2 midlines (section C chain, cluster GPU)
- [done] 1000 px measurements, 12 windows (results/2026-10-25_real_calibration/windows/)
- [done] Thresholds in decisions
- [done] Item 5: 41 windows measured; closure threshold 19 px/h in decisions
- [done] Item 7 (1): full-batch proposal (935cfe7)
- [working] Item 7 (2), 8-10: first batch: segmentation done (126); staging, GPU midlines, tracking
- [todo] Item 7 (3): `results/2026-10-25_full_batch_1/`
