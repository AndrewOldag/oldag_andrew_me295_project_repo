---
id: c022
title: agent run over real-calib first batch (126 windows, 11 roots)
lane: course
owner: dispatcher
state: waiting on real-calib
branch: wip/dispatcher
host: VM (LLM runs), cluster (remedy retracks, CPU), lab server (light)
created: 2026-10-25 19:05
last_update: 2026-10-25 19:10
blocker: real-calib first-batch tracks and checker results not yet reported
done_marker: results/2026-10-25_full_batch_1_agents/README.md
---

Inbox: dispatcher item 39.

## Parts
- [x] Merge main into wip/dispatcher
- [ ] Wait for real-calib first-batch tracks and checker results (groups of at least 20 windows may start)
- [ ] Agent run, one run: dispatcher -> checker (real profile, closure 19 px/h) -> diagnostician -> auditor; free VM memory 3 GB wait per window; status every 20 windows
- [ ] Results README: outcome counts per experiment and condition, auditor control vs stressed; no REGR or growth-zone values
