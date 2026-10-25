---
id: c021
title: Freeze v4 candidate (C1, C2, C3 a), seeds 26-28 labels, scored v4 run
lane: course
owner: diag-analysis
state: waiting on Andrew
branch: wip/v4-candidate
created: 2026-10-25 15:00
last_update: 2026-10-25 15:11
blocker: label sweep host (workstation at 20 GB cap) and run cap (228 needed, 150 allowed)
done_marker: results/2026-10-25_freeze_v4/table_metrics.md
host: VM (code, LLM runs), lab server (tracker sweeps)
---

Inbox diag-analysis items 3 and 4. Proposal `docs/proposals/2026-10-25_diagnostician-repair-misses.md`.

## Parts
- 3(1). C1, C2, C3 (a) behind `candidate: v4` (off by default); switch check equal to v3: done (6a19514, wip/v4-candidate)
- 3(2). Labels of seeds 26-28 (tracker only, at most 150 runs), committed before any agent run: driver ready (8185bcb); waiting on Andrew
- 3(3). Development check, switch on, one run per fault class: not started
- 3(4). `docs/proposals/2026-10-25_freeze-v4-candidate.md`: not started
- 4(3). Tag `freeze-v4`; all methods on seeds 26-28, LLM 3 repeats; `results/2026-10-25_freeze_v4/`: not started
