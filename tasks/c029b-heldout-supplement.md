---
id: c029b
title: held-out supplement: milder compound and novel faults, 48 candidates, 20 selected, same methods as c029
lane: course
owner: compound
state: working
branch: wip/compound
host: VM (renders and LLM runs), cluster (tracker runs)
created: 2026-11-22 20:20
last_update: 2026-11-23 07:51
blocker: none
done_marker: results/2026-11-18_heldout_compound/supplement/README.md
---

Inbox compound item 10 (Andrew, 2026-11-22). Reported beside c029, never merged into its numbers.

## Parts
- [x] Flicker diagnosis, one paragraph for the c029 README: `results/2026-11-18_heldout_compound/flicker.md` (not a generator bug)
- [x] Proposal committed before any render: `docs/proposals/2026-11-22_heldout-supplement.md` (bd3c2ce)
- [x] Renderer entries and driver: `measure/render_compound.py` MILD, `scripts/synth/heldout_supplement.py`, `compound_queue.py --set c029b`
- [x] Render 48 candidates on the VM (96 renders); label runs on the cluster (unremedied 96, remedied array 7874239, 0 failed); labels and selected 20 committed before any method run (701442d): all 48 clean 7, repaired 19, decline 22; selected 4/10/6, no shortfall
- [ ] Methods: fixed script, remedy tree, diagnostician, single agent; 3 repeats for LLM methods; cap 150 agent runs. Script 20, diagnostician 60, single agent 60 (runner ended 07:11; 715ec33); remedy tree 19 of 20: low_texture_fast_mild s60 fetched st1_r28 (array 7919315), then paused on a fourth state st1_r21_mask, array 7925321 submitted 07:49. Set aside and redone: missing-state 2, usage-limit 2
- [ ] Metrics and all-decline baseline on each set; `supplement/README.md` by Thu 26 Nov 20:00
