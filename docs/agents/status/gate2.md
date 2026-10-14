# gate2
Updated: 2026-10-14 00:55 (local)
Lane: research
Branch: status/gate2
Last inbox item done: 5
State: working
Now: item 3, synthetic validation on the VM (growth phantom rendering, then old and coupled runs)
Done since last update:
- Tracker env on the VM: made; tracker test suite 37 passed, 9 skipped
- Code change (plan section 2) done: tracker branch gate2-windowed-coupling, commit d3ff364, pushed to the tracker remote
- New tests: 4 passed, including the real-clip check (couple=False equals d5f1829 output exactly)
- Plan file: dated clarifications added for the two pending choices
- Validation: phantom generator and gate measurement code written; not yet scored. Full run: not started
Needs Andrew:
- Zero-growth phantom: the original source movie is not on the tracker machine; rebuild it with the same construction on a frame from this dataset, and say so in the report
- Delta-REGR definition: score the phantom against the true delta-REGR at the tracked flank lines (not at the root surface); write this into the plan as a dated clarification
