---
id: c002
title: Recompute the real-movie frame_quality reference with the real-tracking midline source
lane: course
owner: Andrew
state: blocked
branch: none
created: 2026-10-16 17:45
last_update: 2026-10-16 17:45
blocker: real-tracking midline source does not exist yet
done_marker: config/frame_quality_reference.yaml real section no longer marked provisional
---

From spec 2026-10-12 (freeze v2 open item), carried by spec 2026-10-13 Task B and inbox fq-real item 5.

- The `real:` reference in `config/frame_quality_reference.yaml` is provisional: band from a dark-root segmentation
- Recompute on the same 24 clean windows (72 frames) once the real-tracking midline source exists
- The 90 staged labeling frames stay on the VM until then (decisions, 2026-10-14)
- Owner to be assigned by the planning account
