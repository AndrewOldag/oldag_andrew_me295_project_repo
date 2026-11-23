---
id: c029b
title: held-out supplement: milder compound and novel faults, 48 candidates, 20 selected, same methods as c029
lane: course
owner: compound
state: done
branch: wip/compound
host: VM (renders and LLM runs), cluster (tracker runs)
created: 2026-11-22 20:20
last_update: 2026-11-23 11:05
blocker: none
done_marker: results/2026-11-18_heldout_compound/supplement/README.md
---

Inbox compound item 10 (Andrew, 2026-11-22). Reported beside c029, never merged into its numbers.

## Parts
- [x] Flicker diagnosis, one paragraph for the c029 README: `results/2026-11-18_heldout_compound/flicker.md` (not a generator bug)
- [x] Proposal committed before any render: `docs/proposals/2026-11-22_heldout-supplement.md` (bd3c2ce)
- [x] Renderer entries and driver: `measure/render_compound.py` MILD, `scripts/synth/heldout_supplement.py`, `compound_queue.py --set c029b`
- [x] Render 48 candidates on the VM (96 renders); label runs on the cluster (unremedied 96, remedied array 7874239, 0 failed); labels and selected 20 committed before any method run (701442d): all 48 clean 7, repaired 19, decline 22; selected 4/10/6, no shortfall
- [x] Methods: script 20, remedy tree 20 (last run after arrays 7919315 and 7925321, 09:53), diagnostician 60, single agent 60; 4 runs set aside and redone (missing-state 2, usage-limit 2); 124 of 150 agent runs
- [x] Metrics and all-decline baseline; `supplement/README.md` written 2026-11-23 (remedy tree 0.75 overall, diagnostician 0.48, single agent 0.35, all-decline 0.30)
