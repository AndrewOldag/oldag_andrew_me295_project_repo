# dispatcher
Updated: 2026-11-03 22:07 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 43
State: ready to merge
Now: task c023 done: not-computable rule (item 40 (2)), README real-slice command (item 42), dispatcher vs fixed script on the fake queue (item 43); ready to merge
Done since last update:
- Item 43: 25 script and 25 agent batches, S0-S4 x seeds 0-4; all finished, budget overrun 0, 0 budget requests. Agent collects more in S1-S3 mainly from its 2 retries vs the script's 1 (proposal; reported as a known difference). S4: agent 36 jobs on the persistent-fault root vs script 24; it did not name a persistent fault. results/2026-11-02_dispatcher_eval/ (README, tables.md, batches.csv); decisions and log entries
- 18 agent batches lost to the Claude seat's session limit were not recorded and were rerun; harness stops on that message (98cdb03). 43 of the 60-batch cap used
- Item 42: README "Run the real slice" (7e043a9). Item 40 (2): closure not computable -> decline; first batch re-scored (51486cf)
Needs Andrew:
- none
