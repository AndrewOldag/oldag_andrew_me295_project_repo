# dispatcher
Updated: 2026-11-23 06:55 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 59 (item 46, task c027, still working)
State: working
Now: B5 fresh demo of 0708_c4 running detached: `full_batch_2_driver.py --settings private/demo_c027.yaml` (pid 10216; stage 5.3 GB root -> one GPU job: midline net, QC, track, checker -> collect, md5) then `staging/c027/tools/demo_after.sh` (pid 7892; waits for driver.done, fetches fresh base tracks into the demo cache, copies the 2 failing windows' remedy tracks from the c027 cache, `run_all.py run --roots 0708_c4 --out staging/c027/demo/run --llm-cap 293`)
Done since last update:
- Auto 11-23 06:55 (from logs): run 1189 records, accept by diagnostician 2, accept by rule 1034, decline by diagnostician 85, decline by rule 58, paused 4, step_limit by diagnostician 6; LLM calls 1007; run ended: done; windows this start 33; LLM calls 1007. Queue 616 tasks: done 12, failed 28, fetched 576; cycle last: 2026-11-23 05:48 status pushed; for real-calib: 0711_c5__w6-8 register_v2 track and base are in the c027 cache
- start check 06:45: no cycle.sh, tree_cycle.sh or run_all.py running; free memory 4.1 GB. Tree rounds ended 05:48 after 8 rounds: rounds 2-8 each had only the 2 jobs of 0708_m1__w10-12 ref/moved, failed twice, not requeued; B4 done, 0708_m1__w10-12 and 0727_cc6__w10-12 stay paused in the tree (24 lines in tree/paused.jsonl)
- Cluster folder 8.9 GB of 30 GB; ledger spent $8.248 of $15 before the demo
- 57044f4: `run_all.py --roots` limits run, fetch and audit to given roots (B5 demo), with a test (test_run_all 13 passed); decision: demo base path fresh, remedy tracks from the c027 cache, demo LLM cap = 1,300 - 1,007 main-run calls = 293
- 06:47 demo driver started; staging 0708_c4 (5,347 MB) into a new cluster folder
Next: demo collect -> agents and auditor on 0708_c4 -> compare with the c027 run window by window, wall time per stage -> `run_all.py report`, results README, windows.csv, example_traces.md (B7-B9) by Thu 26 Nov 20:00
Needs Andrew: none
