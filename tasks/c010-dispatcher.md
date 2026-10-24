---
id: c010
title: Dispatcher proposal, tracker timing, cost estimate; then first real slice
lane: course
owner: dispatcher
state: needs-input
branch: wip/dispatcher
created: 2026-10-23 00:30
last_update: 2026-10-23 20:05
blocker: Claude Code re-pin (freeze-v3); smoothing proposal (Andrew)
done_marker: proposal + results/2026-10-23_tracker_timing/; after approval, slice runs from README
host: lab server, cluster
---

Spec: `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md`.

## Parts
- [x] B1 proposal written (docs/proposals/2026-10-23_dispatcher.md); waiting for Andrew
- [x] B2 tracker timing, one root, lab server (3 runs; checker fails: stage correction zero)
- [x] B4 cost estimate (results/2026-10-23_tracker_timing/)
- [x] Stage correction in tracker repo (stage-auxdata 888f972), validated; private runner copy built
- [ ] B3 cluster trials: configs and ledger ready; job script refused by permission check (Andrew)
- [x] B5 part 1: dispatcher code, fake queue, script baseline (tests/test_dispatcher.py, 19 passed)
- [x] B5 part 2: real slice code and no-agent run (results/2026-10-23_real_slice_noagent/)
- [ ] B5 part 2: agent run (after the Claude Code re-pin)
