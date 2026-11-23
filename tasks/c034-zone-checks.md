---
id: c034
title: growth-zone placement checks (plateau, material-point prediction), report-only
lane: course
owner: real-calib
state: waiting on Andrew
branch: wip/zone-checks
host: VM
created: 2026-11-23 13:25
last_update: 2026-11-23 15:10
blocker: spec amended on main (6810f3a) after branch cut; shifted rods to be rendered and tracked on the cluster; fault model to confirm
done_marker: results/2026-11-23_zone_checks/README.md
---

Spec `docs/specs/2026-11-23_growth-zone-checks.md`.

## Parts
- [done] Proposal `docs/proposals/2026-11-23_zone-checks.md`, committed before any run
- [done] `checker/zone_checks.py`, tests (10 passed)
- [done] Synthetic: clean and shifted freeze v4 rods; thresholds committed (config/zone_thresholds.yaml)
- [done] Real: every c027 window, report-only (1,186 computed)
- [done] README, decisions, log; ready to merge
- [blocked] Spec amendment 6810f3a: shifted rods rendered on the VM and tracked on the cluster CPU via rod_jobs.py. Current synthetic result uses on-record shifts. Waiting on Andrew for the fault model
