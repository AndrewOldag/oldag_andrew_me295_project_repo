---
id: c035
title: real reference set and threshold for the particle-path zone check (report-only)
lane: course
owner: real-calib
state: waiting on Andrew
branch: wip/zone-reference
host: VM
created: 2026-11-23 14:35
last_update: 2026-11-23 17:47
blocker: Andrew labels staging/c035_overlays/labels.csv
done_marker: results/2026-11-23_zone_reference/README.md
---

Spec `docs/specs/2026-11-23_zone-check-real-reference.md`.

## Parts
- [done] Proposal `docs/proposals/2026-11-23_zone-reference.md` (seed, strata, threshold rule), before the draw
- [done] Step 1: residual split (`pp_common_*`, `pp_shape_*`), tests 12 passed; synthetic: shape flags 15 of 15 at every shift (synthetic.md)
- [done] Step 2: sample of 24 accepted c027 windows (sample.csv)
- [done] Step 3: 24 overlays (frames first, middle, last; tip-region zoom row) and index in `staging/c035_overlays/` (not pushed); raw frames deleted after use
- [waiting] Step 4: Andrew's labels in `staging/c035_overlays/labels.csv`
- [todo] Step 5: thresholds, Andrew approves
- [todo] Step 6: apply to all c027 windows, report-only
- [todo] Step 7: README, decisions, log; ready to merge
