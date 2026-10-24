---
id: c013
title: Net-drafted midline traces for the tracing pack, previews and y/n review tool
lane: course
owner: autotrace
state: done
branch: wip/autotrace
host: workstation, lab server, cluster
created: 2026-10-23 20:12
last_update: 2026-10-24 11:30
blocker: none
done_marker: review/review_traces.py and 140 previews in the tracing pack folder; net2_midline_ft2.pt and held-out score in the lab-server work folder; ft2 weights beside the dispatcher's tracker weights on lab server and workstation (md5 checked); status done
---

Inbox: `docs/agents/inbox/autotrace.md`.

## Parts
- [x] Landmark rule from the July traces (35 px behind mask apex)
- [x] 140 drafts (net, tile mode): 140 of 140, 0 with no root
- [x] Previews and index.csv (140; 28 held out)
- [x] review_traces.py and apply_review.py, tested on 3 frames
- [x] Andrew reviews (y/n); held-out frames hand-traced by Andrew
- [x] Fine-tune net2_midline_ft2 on 181 compliant traces (gradient accumulation, option A)
- [x] Held-out score: base, ft, ft2
- [x] net2_midline_ft2 adopted (planning, 2026-10-24 05:05)
- [x] ft2 weights copied to the dispatcher's tracker weights folders, lab server and workstation
