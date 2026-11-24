---
id: c034
title: growth-zone placement checks (plateau, material-point prediction), report-only
lane: course
owner: real-calib
state: done
branch: wip/zone-checks
host: VM
created: 2026-11-23 13:25
last_update: 2026-11-24 09:30
blocker: none
done_marker: results/2026-11-23_zone_checks/README.md
---

Spec `docs/specs/2026-11-23_growth-zone-checks.md`.

## Parts
- [done] Proposal `docs/proposals/2026-11-23_zone-checks.md`, committed before any run
- [done] `checker/zone_checks.py`, tests (10 passed)
- [done] Synthetic: clean and shifted freeze v4 rods; thresholds committed (config/zone_thresholds.yaml)
- [done] Real: every c027 window, report-only (1,186 computed)
- [done] README, decisions, log; ready to merge
- [done] Spec amendment 6810f3a withdrawn (inbox 31): on-record shifts stay the fault set; limit stated in the README
