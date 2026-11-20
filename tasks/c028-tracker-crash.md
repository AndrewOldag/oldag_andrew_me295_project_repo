---
id: c028
title: fix the batch-2 tracker crash (arange) and track the 36 untracked windows
lane: course
owner: real-calib
state: review
branch: wip/real-calib
host: VM, cluster (through retrack_queue.py), lab server (storage)
created: 2026-11-18 14:20
last_update: 2026-11-20 13:40
blocker: C3 replan (no retrack needed) waits on planning
done_marker: results/2026-10-25_full_batch_2/windows.csv rows with tracked_after_fix
---

Spec `docs/specs/2026-11-18_lab-report-4.md`, section C.

## Parts
- [x] New wip/real-calib from origin/main
- [x] Cause found; fix with a reproducing test (C1): tip edge-frozen in every frame, `measure/record.py` derive(), not the tracker (dc1cfe6)
- [x] Equivalence on 5 windows, difference 0.0 (C2): 5 of 5 identical, checker rerun on batch-2 tracks; no retrack needed
- [x] Decisions, log, status ready to merge (C5)
- [ ] (replan: 21 of 33 checked on the VM, all not computable; 12 tracks on storage to check; no retrack) After dispatcher's retrack_queue.py is on main: base tracks and checker for the 36 windows (C3)
