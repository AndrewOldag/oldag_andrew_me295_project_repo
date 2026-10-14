# gate2
Updated: 2026-10-14 01:15 (local)
Lane: research
Branch: status/gate2
Last inbox item done: 5
State: working
Now: item 3, synthetic validation running on the VM: 2 phantoms x 2 trackers, about 80 windows each; about 5 h
Done since last update:
- Code change (plan section 2) done: commit d3ff364 on the tracker remote; 4 new tests pass
- Phantoms rendered: growth-plus-bend (120 frames) and zero-growth bend (120 frames), texture from a frame of this dataset
- Smoke run on 2 windows found a curvature-rate error at the chain end; fixed, estimator checked against the exact phantom chain
- Plan section 3, drop contact in stimulated_1 interval 3: no contact found through the last frame; 0 frames excluded for it
- Full-run code for the tracker machine written (driver, runner); not started
Needs Andrew:
- Zero-growth phantom: the original source movie is not on the tracker machine; rebuild it with the same construction on a frame from this dataset, and say so in the report
- Delta-REGR definition: score the phantom against the true delta-REGR at the tracked flank lines (not at the root surface); write this into the plan as a dated clarification
- Drop contact: dataset notes say the stimulated_1 tip grows into a drop late in interval 3; frames show a gap to the drop rim at the last frame. Confirm no exclusion
- Sweep lock: the full run takes the lock only if no lock file exists, never removes it, and leaves it stale at exit (the course sweep clears stale locks). Confirm this is acceptable
