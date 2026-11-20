---
id: c028
title: fix the batch-2 tracker crash (arange) and track the 36 untracked windows
lane: course
owner: real-calib
state: done
branch: wip/real-calib
host: VM, cluster (through retrack_queue.py), lab server (storage)
created: 2026-11-18 14:20
last_update: 2026-11-20 14:58
blocker: none
done_marker: results/2026-10-25_full_batch_2/windows.csv rows with tracked_after_fix
---

Spec `docs/specs/2026-11-18_lab-report-4.md`, section C.

## Parts
- [x] New wip/real-calib from origin/main
- [x] Cause found; fix with a reproducing test (C1): tip edge-frozen in every frame, `measure/record.py` derive(), not the tracker (dc1cfe6)
- [x] Equivalence on 5 windows, difference 0.0 (C2): 5 of 5 identical, checker rerun on batch-2 tracks; no retrack needed
- [x] Decisions, log, status ready to merge (C5)
- [x] C3 as replanned (inbox item 21): no retrack; 12 storage tracks copied (md5), checker on all 33 on the VM, 33 not computable; rows appended with checked_after_fix
