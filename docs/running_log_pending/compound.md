## 2026-11-20 (build account, session compound)
- Done: c029 proposal `docs/proposals/2026-11-18_heldout-compound.md`, injectors `measure/render_compound.py` (4 compound, 2 novel faults), 13 tests pass, driver `scripts/synth/heldout_compound.py`, all before any run (fa459b7)
- Done: local VM tracking checked: freeze v4 rod v3_growth_zone_clean_s26 rendered and tracked on the VM against the v4 cache, tracks within 4.2e-13 px, truth within 6.9e-18 (`scripts/synth/local_equivalence.py`)
- Done: c029 novel-fault sizing, seeds 50-51, 16 tracker runs, 0 failed, 320 s: focus_drift 3 px, illumination_flicker 0.1 (510d287)
- Done: c029 label sweep on the VM: 42 of 48 unremedied runs, 0 failed, then stopped (spec 2026-11-20: no tracking on the VM). 64 rods rendered
- Done: c030 proposal `docs/proposals/2026-11-18_auditor-check.md`, 30 batches, 15 plants (seed 1118), views and rule decisions before any LLM run (6150856); repeat 0: 30 auditor runs, all ended with a report
- Demo: `python scripts/synth/auditor_check.py eval` writes `results/2026-11-18_auditor_check/scores.md` (catches and false alarms per kind and repeat)
- Remaining: c030 repeats 1-2 and scores; c029 remaining tracker runs on the cluster via `retrack_queue.py`, labels, methods, README
- Bottlenecks: c029 waits for `retrack_queue.py` on main (dispatcher) and for the register_v2 question (planning)
