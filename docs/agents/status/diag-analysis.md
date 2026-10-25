# diag-analysis
Updated: 2026-10-25 15:11 (local)
Lane: course
Branch: wip/diag-analysis (status, task c021); code on wip/v4-candidate
Last inbox item done: 2
State: waiting on Andrew
Now: item 3 (1) done; item 3 (2) label sweep needs a host and a run cap (below); no tracker or LLM runs yet
Done since last update:
- item 3 (1): C1, C2, C3 (a) behind `candidate` in `config/models.yaml` (null = off), 6a19514 on `wip/v4-candidate`
- switch check from the v3 cache (`results/2026-10-25_freeze_v4/switch_check.md`): off, 51 of 51 labels, 102 of 102 rule runs, 306 LLM traces (1319 steps) equal v3; on, only the 3 stage_log_missing labels change (to decline), traces equal except the C2 fields
- tests: 315 passed, 1 skipped (`tests/test_v4_candidate.py` 9)
- Andrew's item 4 decisions recorded in `docs/decisions.md`; v3 README note on stage_log_missing under (a)
- driver `scripts/synth/scored_v4.py` (seeds 26-28, caps, dev check), 8185bcb
Needs Andrew:
- Host for the seed 26-28 label sweep: the workstation work folder is at its 20 GB cap (26 GB free on /), so it has no room for the renders (v3: about 3-4 GB for 51 rods). Options: lab server under its limits (as v3), or workstation after space is freed
- Run cap: labels need 228 tracker runs (phase 1: 144; registration and patch states: 84; same as v3), over the 150 cap of item 3 (2). v3 methods added 164 more, so the 300 total of item 4 (3) would also be passed. Raise to 228 for labels and about 420 in all, or keep the caps (labels stop after phase 1)
