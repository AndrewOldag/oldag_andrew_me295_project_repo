# gate2
Updated: 2026-10-14 00:40 (local)
Lane: research
Branch: status/gate2
Last inbox item done: 5
State: working
Now: item 3 on the VM: tracker env install, then tests, then synthetic validation
Done since last update:
- Item 5 read. Validation moves to the VM; full run stays on the tracker machine
- Tracker branch gate2-windowed-coupling from d5f1829: 6 coupling arguments added to run_windowed_kinematics and passed through; window length still from elapsed time
- New test file, 4 tests (1 needs a real clip). Gap closed in the bending-issues doc
- Not run yet: tests, commit, push. Validation: not started. Full run: not started
Needs Andrew:
- Zero-growth phantom: the original source movie is not on the tracker machine; rebuild it with the same construction on a frame from this dataset, and say so in the report
- Delta-REGR definition: score the phantom against the true delta-REGR at the tracked flank lines (not at the root surface); write this into the plan as a dated clarification
