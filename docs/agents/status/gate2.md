# gate2
Updated: 2026-10-14 04:05 (local)
Lane: research
Branch: status/gate2
Last inbox item done: 5
State: working
Now: item 3, synthetic validation v2 running on the VM: growth phantom 10 of about 80 windows per tracker, bend phantom not started; about 11 h left (VM was suspended about 3 h)
Done since last update:
- Inbox checked: no new items after 5
- Validation v1 stopped after 13 windows per tracker: a pipeline defect found (curvature from tracked nodes near the tip). Fixed; dated entry in the plan file; v1 kept, not used
- Full-run code checked on the tracker machine: smoke run, 1 worker, 2 windows, completed; no lock taken, lock checked first
- Full-run scope set to the gate windows (stimulated: 1.5-3 h; controls: non-overlapping windows, interval 1 after the fix and interval 2). Every-frame windows for all 7 roots estimated over 48 h
Needs Andrew:
- Zero-growth phantom: the original source movie is not on the tracker machine; rebuild it with the same construction on a frame from this dataset, and say so in the report
- Delta-REGR definition: score the phantom against the true delta-REGR at the tracked flank lines (not at the root surface); write this into the plan as a dated clarification
- Drop contact: dataset notes say the stimulated_1 tip grows into a drop late in interval 3; frames show a gap to the drop rim at the last frame. Confirm no exclusion
- Sweep lock: the full run takes the lock only if no lock file exists, never removes it, and leaves it stale at exit (the course sweep clears stale locks). Confirm this is acceptable
- Plan section 6 comparisons (every-frame W20, other schemes, coupled): over the 48 h limit on the shared machine; not run unless approved
- Vault: not reachable from the VM. Validation and results notes are written to the gate2 folder on the VM for copying
