---
id: c019
title: 16-root real subset end to end
lane: course
owner: dispatcher
state: waiting on real-calib
branch: wip/dispatcher
host: cluster, lab server (light)
created: 2026-10-24 16:45
last_update: 2026-10-24 20:45
blocker: real closure threshold from 40+ calibration windows (item 34)
done_marker: results/2026-10-2x_real_subset/README.md
---

Spec: `docs/specs/2026-10-24b_real-movie-push.md`, section C.

## Parts
- [x] Subset proposal `docs/proposals/2026-10-24_real-subset.md` (roots, slots, backups, windows)
- [x] Tip probe on the picks (9 pass, 4 fail; backups running)
- [x] ft2 midlines, 3 windows per root (cluster GPU); R5 third try pending
- [x] Tracking (lab server, light): 48 windows at 1000 px
- [ ] Checks and agent run (after A and B merge)
- [ ] Results README
