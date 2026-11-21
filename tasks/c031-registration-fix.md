---
id: c031
title: register_frames fix (direct to reference, plausibility bound), track-integrity check, synthetic regression
lane: course
owner: real-calib
state: review
branch: wip/real-calib
host: VM (code and checker), cluster (all tracker runs)
created: 2026-11-20 14:50
last_update: 2026-11-20 23:05
blocker: R1 per-pair job and R5 need register_v2 on main and a retrack_queue job kind (diag, synthetic rods)
done_marker: results/2026-11-20_registration_fix/README.md
---

Spec `docs/specs/2026-11-20_registration-fix.md`, section R.

## Parts
- [x] Proposal committed before any run
- [ ] Diagnosis on the flagged window (R1): integrity values done (798 inversions vs 3); register_diag.py written and tested, cluster run open
- [x] register_v2 with tests (R2)
- [x] Integrity check and thresholds by rule (R3, R4): 0 of 115 batch-1 base tracks pass (lateral), for Andrew
- [ ] Synthetic regression on the cluster (R5)
- [x] Decisions, log, ready to merge (code parts)
