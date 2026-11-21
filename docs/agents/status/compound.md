# compound
Updated: 2026-11-21 00:35 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 4
State: working
Now: item 5. c029: 852 non-register label runs submitted on the cluster (array 7418923, 48 tasks, worst case $0.58); fetching. Register states held for register_v2
Done since last update:
- c029 cluster vs VM equivalence on 2 rods: 3.5e-7 px and 1.5e-12 px (limit 1e-6); decisions
- c029 label runs submitted 23:20 (46 rods uploaded to storage with md5, pushed to the cluster)
- c030 done: 90 auditor runs (3 repeats), `results/2026-11-18_auditor_check/README.md`. LLM auditor catches 9, 8, 9 of 15 planted errors (closure relabel 12/12, other-rod track 12/12, wrong unit 0/12, doubled frame 2/9), false alarms 20-25 of 225; rule auditor 15/15 with 55/225 false alarms; repeats unanimous on 227 of 240 runs (kappa 0.836). The wrong-unit misses come from the auditor prompt rule "same shape, higher peak = faster root" (also auditor v1's held-out miss); reported, not changed
Needs Andrew:
- none
