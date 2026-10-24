# dispatcher
Updated: 2026-10-24 14:58 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 28
State: waiting on server job
Now: item 29: waiting for `c2_chain.done` or `c2_chain.failed` (workstation, c010): 0711_c2 4-6 h ft2 net midline from its 80 window frames, then the file to the lab-server task folder; checked every 5 min. Then 0711_c2 tracking on the lab server and the 3-root agent run (0708_m12, 0711_c2, 0721_m10)
Done since last update:
- Item 29 (1), (2): decisions entries (closure known limit; control-root rule replaced)
- Control rule, median over 5 window frames (`scripts/remote/tip_apex_probe.py`): net tip point to mask apex 0711_c2 4.5 px, 0714_c10 4.1 px (references 0708_m12 6.4, 0721_m10 9.2). Tracking-polyline end to apex 27-43 px on every root, slice roots included. 0711_c2 passes (first in order) and runs
- Workstation: 80 window frames of 0711_c2 copied (frame subset; the net needs only these); work folder 19.27 GiB of 20, 26.2 GB free
Needs Andrew:
- Confirm the reading of "midline end" in the item 29 rule as the net's tip point (the quantity autotrace compared with the apex). On the tracking-polyline end no root passes, the two slice roots included (27-43 px)
