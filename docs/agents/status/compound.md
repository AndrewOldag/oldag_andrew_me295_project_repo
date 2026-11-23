# compound
Updated: 2026-11-22 17:25 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 9
State: working
Now: c029 methods running detached on the VM (started 17:15): rules done; diagnostician and single agent, repeats 0-2, one LLM run at a time, 3 GB floor. Paused-state retrack array 7853647 (2 runs) on the cluster. README by Thu 26 Nov 20:00
Done since last update:
- Items 8-9: merged main twice (000a2b6, e566854: option A gate in Slice.apply_remedy, used by the tree and the diagnostician); suite 460 passed, 3 skipped
- Label runs: second array fetched (456 of 461); 5 runs failed in every submit (tracker errors: 3 at stride 12 on low_texture_fast s40 moved copy, 2 register_v2 runs); they count as states without a measurement
- Labels committed before any method run (a9445d2): 24 rods, accept_repaired 4 (focus_drift, repaired by enlarge_patch 1.5x or the width-free ratio), decline 20. All-decline scores 20 of 24. illumination_flicker 0.1 labels decline (expected accept_clean)
- Rule methods (05c07b2 code, results committed): 47 of 48 runs; 1 remedy-tree run paused on a 3-step state (submitted); second runs identical 47 of 47
- A state a method needs that the labels did not run pauses the run; `compound_queue.py submit --paused` sends it to the cluster; the run is redone from step 0
Needs Andrew:
- none
