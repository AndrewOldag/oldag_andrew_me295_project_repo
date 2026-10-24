---
id: c016
title: Coordinator as a scheduled tick (no long-lived session)
lane: course
owner: coord-tick
state: done
branch: wip/coord-tick
host: VM
created: 2026-10-24 12:25
last_update: 2026-10-24 13:10
blocker: none (install of the scheduled task is Andrew's)
done_marker: scripts/ops/coordinator_tick.ps1 and install script; tested skip and full pass; status ready to merge
---

Inbox: `docs/agents/inbox/coord-tick.md`.

## Parts
- [x] Tick script with ref-hash skip and lock
- [x] Install script (Andrew runs it elevated)
- [x] Tests; one hand-run skip tick and one full pass (Andrew ran them, 12:55 and 13:08)
- [x] Docs, decisions, coordinator inbox note
