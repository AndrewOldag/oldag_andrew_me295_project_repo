---
id: c028
title: fix the batch-2 tracker crash (arange) and track the 36 untracked windows
lane: course
owner: real-calib
state: open
branch: wip/real-calib
host: VM, cluster (through retrack_queue.py), lab server (storage)
created: 2026-11-18 14:20
last_update: 2026-11-18 14:20
blocker: none
done_marker: results/2026-10-25_full_batch_2/windows.csv rows with tracked_after_fix
---

Spec `docs/specs/2026-11-18_lab-report-4.md`, section C.

## Parts
- [ ] New wip/real-calib from origin/main
- [ ] Cause found; fix with a reproducing test (C1)
- [ ] Equivalence on 5 windows, difference 0.0 (C2)
- [ ] Decisions, log, status ready to merge (C5)
- [ ] After dispatcher's retrack_queue.py is on main: base tracks and checker for the 36 windows (C3)
