# compound
Updated: 2026-11-21 10:55 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 6
State: waiting on Andrew
Now: c029 label runs on the cluster: 331 of 854 fetched (incl. the 2 equivalence runs), 523 queued in array 7418923; register_v2 states (about 300 runs) to submit. Fetch and submit stopped: cluster master down (10:20). c030 done
Done since last update:
- Item 5: rod job kind with tests; 2-rod cluster vs VM equivalence 3.5e-7 and 1.5e-12 px (limit 1e-6); 852 non-register label runs submitted 23:20
- Item 6: merged main (cbdb7f4, register_v2); register label states now register_v2 (`compound_queue.py jobs`: 825 runs not cached, 48 tasks, worst case $0.58); generic job kind `scripts/rod_jobs.py` (e213ddb) and branch `wip/rod-jobs` from origin/main, ready to merge
- c030 done: `results/2026-11-18_auditor_check/README.md` (LLM auditor 9, 8, 9 of 15 caught; wrong_unit 0 of 12; rule 15 of 15 with 55 of 225 false alarms)
- Fetch log: storage link reset (10054, 3 failed reconnects) overnight, then cluster master down at 10:20
Needs Andrew:
- Open the cluster connection master on the lab server, then start me: I fetch the 523 queued runs and submit the register_v2 states
- Track integrity is reported, not used in the c029 labels (labels stay on the freeze v4 rule; the gate is not wired into the agents on main yet). Say if remedied label states should also pass the integrity gate
