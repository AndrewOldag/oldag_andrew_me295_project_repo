# compound
Updated: 2026-11-22 21:28 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 9
State: waiting on cluster (c029b label array)
Now: item 10 step 3: c029b remedied label array 7874239 (96 tasks, 2,608 runs) on the cluster; a detached loop fetches every 10 min, resubmits failed runs once, then writes labels and selected.json. On restart: commit labels and selection, then start the c029b methods
Done since last update:
- c029 done: 144 LLM runs and 48 rule runs; README, metrics, decisions, log (results/2026-11-18_heldout_compound/README.md). Balanced accuracy: tree 0.70, diagnostician 0.47, single agent 0.06, script 0.00, all-decline 0.50. 153 of 450 agent runs; 1,031 claude -p calls
- c029 remedy tree: paused drift_jitter s41 redone after its 3-step state was fetched; 48 of 48
- c029b: 96 renders (48 candidates and moved copies); unremedied array 7872119 fetched 96 of 96, none failed
- Ledger: total $7.93 of $15 after the c029b arrays' worst case
Needs Andrew:
- Keep the cluster connection master open until the c029b array is fetched (about 2,600 runs)
