# compound
Updated: 2026-11-23 06:56 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 12
State: working
Now: item 10 step 4: c029b LLM methods running (detached runner restarted 06:53, diagnostician repeat 2, then single agent repeat 2); about 24 LLM runs left of 120
Done since last update:
- Runner had stopped at 04:57 on the account usage limit (2 runs set aside in runs/usage_limit/); restarted 06:53
- Item 12: c029b missing-state runs set aside in runs/missing_state/ with pending.jsonl, redone from step 0 once the state is cached; set-aside runs count toward the cap (ba032f6, test added; 22 passed). 2 set aside (diagnostician drift_low_texture_mild s61 r0, r2); r0 redone (decline low_texture), r2 in this pass
- Item 12: c029 README names the 3 runs, metrics with and without them; no conclusion changes (679a3e9)
- Arrays 7908864 and 7908996 fetched: 4 of 4, 0 failed
- Remedy tree low_texture_fast_mild s60 paused again on a third state (st1_r28); array 7919315 submitted (2 runs, worst case $0.024; spend before it about $8.30 of $15)
- run_rules: a paused rule run leaves no partial trace (the tracked trace blocked the runner's clean-tree check)
Needs Andrew:
- Keep the cluster connection master open until array 7919315 is fetched
