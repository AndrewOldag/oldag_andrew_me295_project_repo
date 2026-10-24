# freeze-v3
Updated: 2026-10-24 05:35 (local)
Lane: course
Branch: wip/freeze-v3
Last inbox item done: 12
State: ready to merge
Now: done. Results in `results/2026-10-23_freeze_v3/README.md`; log entry in `docs/running_log_pending/freeze-v3.md`
Done since last update:
- LLM runs complete: 306 of 306 (diagnostician, single agent, 3 repeats), 0 harness errors, CLI 2.1.310 on every block; 15 blocks of 8-13 runs, free memory 1.7-2.4 GB before each (floor 1.5 GB, items 11-12)
- `eval`: balanced accuracy remedy tree 0.81, diagnostician 0.69, script 0.67, single agent 0.60, all-accept 0.67, all-decline 0.33. False accepts: script 18, remedy tree 4, LLM methods 0. Unanimity over 3 repeats: diagnostician 39 of 51 (kappa 0.776), single agent 24 of 51 (0.503)
- Tracker runs in all 528 of 600, 0 failed. Tag `freeze-v3` on e1e672a; after it only harness code changed
- Full suite 245 passed, 5 skipped
Needs Andrew:
- Review `results/2026-10-23_freeze_v3/README.md`. Two points for the evaluation: all 12 accept_repaired rods have a good unremedied measurement (so accepting without a remedy is scored correct there; script 12 of 12), and `second_root` is 0 correct for every method
