---
id: c035
title: real reference set and threshold for the particle-path zone check (report-only)
lane: course
owner: real-calib
state: working
branch: wip/zone-reference
host: VM
created: 2026-11-23 14:35
last_update: 2026-11-23 21:10
blocker: none
done_marker: results/2026-11-23_zone_reference/README.md
---

Spec `docs/specs/2026-11-23_zone-check-real-reference.md`.

## Parts
- [done] Proposal `docs/proposals/2026-11-23_zone-reference.md` (seed, strata, threshold rule), before the draw
- [done] Step 1: residual split (`pp_common_*`, `pp_shape_*`), tests 12 passed; synthetic: shape flags 15 of 15 at every shift (synthetic.md)
- [done] Step 2: sample of 24 accepted c027 windows (sample.csv)
- [done] Step 3: 24 overlays (frames first, middle, last; tip-region zoom row) and index in `staging/c035_overlays/` (not pushed); raw frames deleted after use
- [done] Step 4a: Andrew labelled the first 24
- [done] Inbox 33: extension rule (126 more, seed 20261124) in the proposal, before the draw
- [todo] Inbox 33: draw 126 more; overlays appended to index and labels.csv
- [todo] Step 4b: Andrew labels windows 25-150
- [todo] Step 5: thresholds, Andrew approves
- [todo] Step 6: apply to all c027 windows, report-only
- [todo] Step 7: README, decisions, log; ready to merge
