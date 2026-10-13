## 2026-10-12 (build account, held-out faults session)
- Done: `measure/render_heldout.py`: injectors for second_root, fast_rotation, bad_stage_correction (agent fault names with no injector) and flank_swap, partial_occlusion (new). Same interface as `measure/render.py`; `make_rod.py` renders them. Commit 8109764
- Done: `tests/test_render_heldout.py`: 14 passed (each injector changes the movie only where it should; size 0 equals `render.render` exactly). Full suite `python -m pytest -q tests`: 145 passed
- Done: `scripts/synth/heldout_sweep.py`, checker only, no agent, own code directory on the tracker machine, same sweep lock. Commit d9a631c
- Done: sweep, growth_zone seeds 0-2, 9 sizes, 54 tracker runs, 0 failed, 204 s wall, 4 workers; waited 245 s for the baselines sweep's lock; load 4.30 -> 5.63 max -> 4.99 on 32 cores; work space 5.83 -> 6.70 GB
- Result: checker fails 3 of 3 at second_root 30 px (15 px: 0 of 3), fast_rotation 2 and 4 deg/frame, bad_stage_correction 3 and 10 px, flank_swap 0.5, partial_occlusion 20 and 30 px. `results/2026-10-12_heldout_faults/checker_sizes.md`
- Proposed sizes (smallest failing 3 of 3): second_root 30, fast_rotation 2, bad_stage_correction 3, flank_swap 0.5, partial_occlusion 20. Not used in any scored run. `docs/proposals/2026-10-12_heldout-faults.md`
- Demo: `python scripts/synth/heldout_sweep.py eval --out results/2026-10-12_heldout_faults` (after `fetch`) prints the per-fault table of seeds failing the checker
- Remaining: Andrew approves sizes, names and outcomes; then the remedy label sweep (about 90 runs, no agent); then merge at the freeze
- Bottlenecks: size, name and outcome approval (Andrew); branch not merged until the freeze (Andrew)
