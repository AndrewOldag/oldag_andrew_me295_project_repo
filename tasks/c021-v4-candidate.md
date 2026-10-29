---
id: c021
title: Freeze v4 candidate (C1, C2, C3 a), seeds 26-28 labels, scored v4 run
lane: course
owner: diag-analysis
state: done
branch: wip/v4-candidate
created: 2026-10-25 15:00
last_update: 2026-10-26 13:39
blocker: none
done_marker: results/2026-10-25_freeze_v4/table_metrics.md
host: VM (code and LLM runs), lab server (tracker sweeps)
---

Inbox diag-analysis items 3 and 4. Proposal `docs/proposals/2026-10-25_diagnostician-repair-misses.md`.

## Parts
- 3(1). C1, C2, C3 (a) behind `candidate: v4` (off by default); switch check equal to v3: done (6a19514, wip/v4-candidate)
- 3(2). Labels of seeds 26-28 (tracker only, at most 228 runs, item 5), committed before any agent run: done (6b72d6a; 228 runs, 0 failed)
- 3(3). Development check, switch on, one run per fault class: done (d75717b; 17 runs, 14 correct)
- 3(4). `docs/proposals/2026-10-25_freeze-v4-candidate.md`: done (b86abef)
- 4(3). Tag `freeze-v4`; all methods on seeds 26-28, LLM 3 repeats; `results/2026-10-25_freeze_v4/`: done (bdc1f94; tag e9f19f2; 404 tracker runs, 418 LLM runs)
