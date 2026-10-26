# diag-analysis
Updated: 2026-10-26 13:39 (local)
Lane: course
Branch: wip/diag-analysis (status, task c021, log entry); code and results on wip/v4-candidate
Last inbox item done: 5
State: ready to merge
Now: freeze v4 done; `wip/v4-candidate` not merged to main until Andrew approves (item 3 (4))
Done since last update:
- scored v4 run complete, `results/2026-10-25_freeze_v4/README.md`, bdc1f94 on wip/v4-candidate
- balanced accuracy: script 0.67, remedy tree 0.93, diagnostician 0.93 (0.92-0.94), single agent 0.63 (0.58-0.69), all-decline 0.33; false accepts per repeat: 18, 2, 0, 0.3
- agreement: diagnostician 46 of 51 rods unanimous (kappa 0.887); single agent 34 of 51 (0.626)
- 95 usage-limit runs rerun as Andrew approved; 0 such runs in the final set; 0 harness errors
- tracker runs 404 of 420, 0 failed; LLM runs 418 of 420
- log entry `docs/running_log_pending/diag-analysis.md`; task c021 done
Needs Andrew:
- merge of `wip/v4-candidate` (code switch, v4 driver, labels, results, proposal); `wip/diag-analysis` (status, task, log) can merge any time
