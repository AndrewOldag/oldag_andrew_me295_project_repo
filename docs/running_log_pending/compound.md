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

## 2026-11-22 (build account, session compound, evening)
- Done: c029 LLM methods complete: diagnostician and single agent, 3 repeats, 144 runs (7596bfc and later); 9 runs ended by the account session limit set aside; runner restarted twice (session limit 18:34, dirty tree 20:14)
- Done: c029 remedy tree 48 of 48 (paused drift_jitter s41 redone after its 3-step state was fetched); rule second runs identical 48 of 48
- Done: c029 eval and README `results/2026-11-18_heldout_compound/README.md`: balanced accuracy tree 0.70, diagnostician 0.47, single agent 0.06, script 0.00, all-decline 0.50; 153 of 450 agent runs; 1,031 `claude -p` calls
- Done: flicker note (inbox 10 step 1): not a generator bug; tracker matches raw intensity
- Done: c029b proposal (bd3c2ce), MILD renderer entries with tests (18 passed), `heldout_supplement.py`, `compound_queue.py --set c029b` (19 tests passed); 96 renders on the VM; unremedied array 7872119 submitted (96 runs, worst case $1.15)
- Demo: `python scripts/synth/heldout_compound.py eval` writes `table_metrics.md` for c029
- Remaining: c029b remedied array, labels and selection committed; c029b methods (cap 150); supplement README by Thu 26 Nov 20:00
- Bottlenecks: cluster connection master (Andrew) for the c029b label arrays

## 2026-11-23 (build account, session compound)
- Done: c029b labels and selected 20 committed (701442d): 48 labelled clean 7, repaired 19, decline 22; selected 4/10/6
- Done: c029b rule methods: script 20 of 20, remedy tree 19 of 20 (1 paused, third state st1_r28 in array 7919315)
- Done: c029b LLM runner stopped 04:57 on the account usage limit (2 runs set aside), restarted 06:53
- Done: inbox 12: c029b missing-state runs set aside in `runs/missing_state/`, redone once cached (ba032f6; test_heldout_supplement 22 passed with render tests); c029 README gives metrics with and without its 3 such runs (679a3e9)
- Done: arrays 7908864, 7908996 fetched (4 of 4); array 7919315 submitted (2 runs, worst case $0.024)
- Demo: `python scripts/synth/heldout_supplement.py eval` writes `supplement/table_metrics.md` once all runs exist
- Remaining: finish c029b LLM runs (about 24 left); fetch 7919315, rerun remedy tree; eval; supplement README by Thu 26 Nov 20:00
- Bottlenecks: cluster connection master (Andrew) for array 7919315

## 2026-11-23 (build account, session compound, morning)
- Done: c029b LLM runs complete: diagnostician 60 of 60, single agent 60 of 60, 0 harness errors; runner ended 07:11 (715ec33)
- Done: array 7919315 fetched (2 of 2); remedy tree low_texture_fast_mild s60 paused on a fourth state (st1_r21_mask); array 7925321 submitted 07:49 (2 runs, worst case $0.024)
- Done: detached loop `staging/c029b_tail.ps1` (git-ignored) fetches, reruns `rules`, submits a further paused state if needed (max 3)
- Demo: `python scripts/synth/heldout_supplement.py eval` writes `supplement/table_metrics.md` (19 of 20 remedy-tree runs so far; not committed)
- Remaining: fetch 7925321, last remedy-tree run, eval, supplement README by Thu 26 Nov 20:00
- Bottlenecks: cluster queue for array 7925321; connection master (Andrew)

## 2026-11-23 (build account, session compound, late morning)
- Done: array 7925321 fetched 09:53; remedy tree low_texture_fast_mild s60 written, second run identical; remedy tree 20 of 20 (rule second runs identical 40 of 40)
- Done: c029b eval, 20 rods (clean 4, repaired 10, decline 6): overall accuracy remedy tree 0.75, diagnostician 0.48 (0.45-0.50), single agent 0.35 (0.30-0.40), script 0.30, all-decline 0.30; balanced 0.77 / 0.60 / 0.43 / 0.40 / 0.33
- Done: `results/2026-11-18_heldout_compound/supplement/README.md`; 120 scored agent runs plus 4 set aside, 124 of 150; `claude -p` calls 285 and 394; task c029b done
- Demo: `python scripts/synth/heldout_supplement.py eval` prints the c029b metrics table above
- Remaining: none on c029/c029b/c030; wait for inbox
- Bottlenecks: none
