---
id: c031
title: register_frames fix (direct to reference, plausibility bound), track-integrity check, synthetic regression
lane: course
owner: real-calib
state: review
branch: wip/real-calib
host: VM (code and checker), cluster (all tracker runs)
created: 2026-11-20 14:50
last_update: 2026-11-22 19:57
blocker: none
done_marker: results/2026-11-20_registration_fix/README.md
---

Spec `docs/specs/2026-11-20_registration-fix.md`, section R.

## Parts
- [x] Proposal committed before any run
- [x] Diagnosis on the flagged window (R1): chained sum of 79 pair rotations gives 9.23 deg; direct fit not plausible; staged root cleared
- [x] register_v2 with tests (R2)
- [x] Integrity check and thresholds by rule (R3, R4): 0 of 115 batch-1 base tracks pass (lateral), for Andrew
- [x] Synthetic regression on the cluster (R5): v2 repairs 3 of 6 rods vs 6 of 6 for v1 (rigid invariance), for Andrew
- [x] Decisions, log, ready to merge (code parts)
