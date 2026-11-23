---
id: c029b
title: held-out supplement: milder compound and novel faults, 48 candidates, 20 selected, same methods as c029
lane: course
owner: compound
state: working
branch: wip/compound
host: VM (renders and LLM runs), cluster (tracker runs)
created: 2026-11-22 20:20
last_update: 2026-11-23 02:49
blocker: none
done_marker: results/2026-11-18_heldout_compound/supplement/README.md
---

Inbox compound item 10 (Andrew, 2026-11-22). Reported beside c029, never merged into its numbers.

## Parts
- [x] Flicker diagnosis, one paragraph for the c029 README: `results/2026-11-18_heldout_compound/flicker.md` (not a generator bug)
- [x] Proposal committed before any render: `docs/proposals/2026-11-22_heldout-supplement.md` (bd3c2ce)
- [x] Renderer entries and driver: `measure/render_compound.py` MILD, `scripts/synth/heldout_supplement.py`, `compound_queue.py --set c029b`
- [ ] Render 48 candidates on the VM (done, 96 renders); label runs on the cluster (unremedied 96 of 96 fetched; remedied array 7874239, 2,608 runs, fetch running: 2544 of about 2,704 track files at 02:48); labels and selected 20 committed before any method run
- [ ] Methods: fixed script, remedy tree, diagnostician, single agent; 3 repeats for LLM methods; cap 150 agent runs
- [ ] Metrics and all-decline baseline on each set; `supplement/README.md` by Thu 26 Nov 20:00
