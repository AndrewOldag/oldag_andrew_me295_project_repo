---
id: c032
title: VM supervisor (no LLM): start sessions with pending work, detached registry, heartbeat
lane: course
owner: real-calib
state: done
branch: wip/supervisor
host: VM
created: 2026-11-22 22:30
last_update: 2026-11-24 09:30
blocker: none
done_marker: tests/test_supervisor.py passes
---

Spec `docs/specs/2026-11-22_vm-supervisor.md`.

## Parts
- [x] supervisor.ps1: tick (running, pending, start rule, memory gate), single-instance lock
- [x] register_detached.ps1 and dead-entry report
- [x] Heartbeat on `ops/heartbeat`, last 48 lines
- [x] install_supervisor.ps1 (and -Uninstall); written, not run
- [x] Tests with fake clock, git and process table
- [x] README, decisions, log, ready to merge
