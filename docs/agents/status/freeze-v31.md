# freeze-v31
Updated: 2026-10-24 11:55 (local)
Lane: course
Branch: wip/freeze-v31
Last inbox item done: 1
State: waiting on Andrew
Now: item 2 blocked: sizing sweep 1 stopped by the sweep's 10 GB work-space limit after 13 of 114 runs, 0 failed
Done since last update:
- Sizing sweep 1 (log sweep_freeze_v31_20261024-114448): status `projected_space`, 13 runs done, 0 failed, 67 s; work space 8.06 -> 8.32 GB; projection for the full plan 10.25 GB, over the 10 GB limit. 13 outputs fetched
- Partial sizing (`results/2026-10-24_freeze_v3.1/sizing.md`): rigid_drift 0.5 and 1.5, bad_stage_correction 3, stage_log_missing 1: check fails 3 of 3, unremedied measurement good 3 of 3 (rule part 2 fails). 51 rod states (102 runs) still needed
- Driver `scripts/synth/scored_v31.py`, `tests/test_freeze_v31.py` 3 passed (1c1a548); second_root note (`second_root.md`)
Needs Andrew:
- Lab-server work space: 8.32 of 10 GB. About 0.02 GB per tracker run (mostly renders); the rest of v3.1 needs about 290 runs, about 6 GB. Sessions cannot delete there. Options: (a) Andrew frees space in the work folder (e.g. v3 renders no longer needed); (b) Andrew raises the sweep's `--max-gb` limit for this freeze (a limit change, docs/decisions.md). I start the next sweep on your word
- Size steps I chose (spec says "the fault's own unit"): rigid_drift factor steps of 1 (0.5-5.5), bad_stage_correction 1 px (3-8 px). If you want steps of the v3 size instead (bad_stage 3, 6, ..., 18 px), say so before the next sweep
