---
id: c016
title: Coordinator as a scheduled tick (no long-lived session)
lane: course
owner: coord-tick
state: waiting on Andrew
branch: wip/coord-tick
host: VM
created: 2026-10-24 12:25
last_update: 2026-10-24 13:05
blocker: hand test and install need Andrew (session guard blocks git on the main checkout)
done_marker: scripts/ops/coordinator_tick.ps1 and install script; tested skip and full pass; status ready to merge
---

Inbox: `docs/agents/inbox/coord-tick.md`.

## Parts
- [x] Tick script with ref-hash skip and lock
- [x] Install script (Andrew runs it elevated)
- [ ] Tests; one hand-run skip tick and one full pass (tests done; hand run waits on Andrew)
- [x] Docs, decisions, coordinator inbox note
