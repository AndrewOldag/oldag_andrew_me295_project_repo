# compound
Updated: 2026-11-22 20:17 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 9
State: working
Now: item 10 step 3: rendering the 48 c029b candidates on the VM, then cluster label arrays (detached, c029b_labels.ps1). c029 LLM methods still running (single agent repeat 1, then repeat 2)
Done since last update:
- Item 10 (1): flicker 0.1 declines because the tracker matches raw intensity (no gain term); the generator applies the fault as defined. Not a generator bug; nothing re-rendered. Note `results/2026-11-18_heldout_compound/flicker.md`
- Item 10 (2): proposal `docs/proposals/2026-11-22_heldout-supplement.md` committed before any render (bd3c2ce); seeds 60-67; selection rule fixed
- c029b code: MILD entries in render_compound (c029 entries unchanged, tests 18 passed), heldout_supplement.py driver, compound_queue --set c029b (tests 19 passed with retrack_queue)
- New task file tasks/c029b-heldout-supplement.md
Needs Andrew:
- none
