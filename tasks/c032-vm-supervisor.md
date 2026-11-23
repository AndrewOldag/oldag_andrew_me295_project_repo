---
id: c032
title: VM supervisor (no LLM): start sessions with pending work, detached registry, heartbeat
lane: course
owner: real-calib
state: working
branch: wip/supervisor
host: VM
created: 2026-11-22 22:30
last_update: 2026-11-22 22:47
blocker: none
done_marker: tests/test_supervisor.py passes
---

Spec `docs/specs/2026-11-22_vm-supervisor.md`.

## Parts
- [ ] supervisor.ps1: tick (running, pending, start rule, memory gate), single-instance lock
- [ ] register_detached.ps1 and dead-entry report
- [ ] Heartbeat on `ops/heartbeat`, last 48 lines
- [ ] install_supervisor.ps1 (and -Uninstall); not run
- [ ] Tests with fake clock, git and process table
- [ ] README, decisions, log, ready to merge
