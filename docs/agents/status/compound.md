# compound
Updated: 2026-11-20 15:35 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 0
State: working
Now: item 1. c029 novel-fault sizing sweep (16 tracker runs, VM); then label sweep (about 1,350 runs). c030 auditor repeat 0 running beside it (one LLM run at a time)
Done since last update:
- Local VM tracking: tracker d5f1829 in the VM tracker env; equivalence on v4 rod s26: tracks within 4.2e-13 px, truth within 6.9e-18 (decisions)
- c029 proposal, injectors (6 faults, 13 tests pass), driver committed before any run (fa459b7); memory rule per rod batch (decisions)
- c030 proposal, 30 batches, 15 plants, views and rule decisions committed before any LLM run (6150856)
- Edge Crashpad reports folder: 0 bytes
Needs Andrew:
- Free VM memory sits at 2.9-3.2 GB with three Claude sessions; runs wait for 3 GB before each batch. I check 3 GB before each rod batch and each LLM run, 2 GB before each tracker run inside a batch (decisions 2026-11-20). Reverse if you want 3 GB per tracker run
- LLM caps of D3 and E2 counted as agent runs (one run = one rod or batch), as freeze v4 and auditor v1; steps reported beside. Say if they mean `claude -p` calls
