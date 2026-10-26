# diag-analysis
Updated: 2026-10-26 09:04 (local)
Lane: course
Branch: wip/diag-analysis (status, task c021); code on wip/v4-candidate
Last inbox item done: 5
State: working
Now: item 4 (3): rerun of 95 LLM runs that ended on the account usage limit; then eval, README, log
Done since last update:
- LLM runs 306 of 306 written by 23:45; 95 ended as error on the account usage limit ("session limit", no model answer): diagnostician r1 23, single_agent r0 27, r2 45
- Andrew (in session, 2026-10-26): rerun them. Records set aside in `runs/usage_limit/`; the driver sets aside further such runs and stops; LLM cap 420 counting them (853da3b, decisions)
- item 5 applied earlier (caps 228/420 tracker runs, lab server)
- tracker runs 346 of 420; LLM runs 323 so far (17 dev check, 211 valid, 95 set aside)
Needs Andrew:
- none
