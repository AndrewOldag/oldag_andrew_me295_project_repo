---
id: c031
title: register_frames fix (direct to reference, plausibility bound), track-integrity check, synthetic regression
lane: course
owner: real-calib
state: queued
branch: wip/real-calib
host: VM (code, checker), cluster (all tracker runs)
created: 2026-11-20 14:50
last_update: 2026-11-20 14:50
blocker: needs scripts/retrack_queue.py on main for cluster runs
done_marker: results/2026-11-20_registration_fix/README.md
---

Spec `docs/specs/2026-11-20_registration-fix.md`, section R.

## Parts
- [ ] Proposal committed before any run
- [ ] Diagnosis on the flagged window (R1)
- [ ] register_v2 with tests (R2)
- [ ] Integrity check and thresholds by rule (R3, R4)
- [ ] Synthetic regression on the cluster (R5)
- [ ] Decisions, log, ready to merge
