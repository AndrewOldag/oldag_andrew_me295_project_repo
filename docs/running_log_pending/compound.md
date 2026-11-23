## 2026-11-20 (build account, session compound)
- Done: c029 proposal `docs/proposals/2026-11-18_heldout-compound.md`, injectors `measure/render_compound.py` (4 compound, 2 novel faults), 13 tests pass, driver `scripts/synth/heldout_compound.py`, all before any run (fa459b7)
- Done: local VM tracking checked: freeze v4 rod v3_growth_zone_clean_s26 rendered and tracked on the VM against the v4 cache, tracks within 4.2e-13 px, truth within 6.9e-18 (`scripts/synth/local_equivalence.py`)
- Done: c029 novel-fault sizing, seeds 50-51, 16 tracker runs, 0 failed, 320 s: focus_drift 3 px, illumination_flicker 0.1 (510d287)
- Done: c029 label sweep on the VM: 42 of 48 unremedied runs, 0 failed, then stopped (spec 2026-11-20: no tracking on the VM). 64 rods rendered
- Done: c030 proposal `docs/proposals/2026-11-18_auditor-check.md`, 30 batches, 15 plants (seed 1118), views and rule decisions before any LLM run (6150856); repeat 0: 30 auditor runs, all ended with a report
- Demo: `python scripts/synth/auditor_check.py eval` writes `results/2026-11-18_auditor_check/scores.md` (catches and false alarms per kind and repeat)
- Remaining: c030 repeats 1-2 and scores; c029 remaining tracker runs on the cluster via `retrack_queue.py`, labels, methods, README
- Bottlenecks: c029 waits for `retrack_queue.py` on main (dispatcher) and for the register_v2 question (planning)

## 2026-11-21 (build account, session compound)
- Done: c030 complete: 90 LLM auditor runs, 382 calls, 3.09 M tokens in; LLM catches 9, 8, 9 of 15 planted errors (closure_relabelled 12/12, other_rod_track 12/12, wrong_unit 0/12, doubled_frame 2/9), false alarms 20-25 of 225; rule auditor 15/15, 55/225 false alarms; Fleiss kappa 0.836. `results/2026-11-18_auditor_check/README.md`
- Done: synthetic-rod job kind `scripts/rod_jobs.py` with 8 fake-cluster tests (e213ddb; branch `wip/rod-jobs` ready to merge); c029 cluster vs VM equivalence on 2 rods 3.5e-7 and 1.5e-12 px (limit 1e-6)
- Done: c029 label runs on the cluster: 852 non-register runs submitted (array 7418923, 48 tasks, worst case $0.58), 329 fetched before the storage link reset and the cluster master went down (10:20)
- Demo: `python scripts/synth/compound_queue.py jobs` prints the c029 runs not cached (825, incl. about 300 register_v2 states)
- Remaining: fetch the 523 queued runs; submit the register_v2 states; labels committed; rules, diagnostician and single agent (3 repeats); c029 README by Thu 26 Nov 20:00
- Bottlenecks: cluster connection master (Andrew)

## 2026-11-22 (build account, session compound)
- Done: c029 label runs on the cluster complete: 1,307 fetched over 3 arrays (7418923, 7845308, 7852409), 5 runs failed in every submit (tracker errors), cluster CPU; storage link reset and master down on 21 Nov, resumed 22 Nov
- Done: c029 labels before any method run (a9445d2): 24 rods, accept_repaired 4 (focus_drift), decline 20; all-decline 20 of 24
- Done: merged main (option A integrity gate in Slice.apply_remedy, register_v2); suite 460 passed, 3 skipped
- Done: c029 rule methods: 47 of 48 runs, 1 paused (3-step state submitted, array 7853647); deterministic 47 of 47. LLM methods started 17:15 (144 runs planned, cap 450)
- Demo: `python scripts/synth/heldout_compound.py labels` prints the label table
- Remaining: fetch paused states and rerun paused runs; LLM methods to the end; `eval` (scores), README `results/2026-11-18_heldout_compound/`, decisions
- Bottlenecks: none
