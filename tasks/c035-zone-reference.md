---
id: c035
title: real reference set and threshold for the particle-path zone check (report-only)
lane: course
owner: real-calib
state: done
branch: wip/zone-reference
host: VM
created: 2026-11-23 14:35
last_update: 2026-11-24 09:30
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
- [done] Inbox 33: 126 more drawn (b7d30ac): 45/5/36/33/7 by condition, max 2 per root, 150 in sample.csv
- [done] Inbox 33: overlays for windows 25-150, detached job: 150 of 150 made, raw frames deleted; index and labels.csv have 150 rows, first 24 labels kept
- [done] Step 4b: Andrew labelled all 150 (130 clean, 20 not clean)
- [done] Step 5: thresholds computed (83752a4), approved by Andrew 23:20; `config/zone_reference_thresholds.yaml`
- [done] Step 6: applied to 1,189 c027 windows, report-only (`real_counts.md`); accepted 8 of 1,034 flagged
- [done] Inbox 34: detection curve on 130 clean windows (`curve.md`), sizes committed before the run (1a023ff)
- [done] Step 7: README, decisions, log; ready to merge
