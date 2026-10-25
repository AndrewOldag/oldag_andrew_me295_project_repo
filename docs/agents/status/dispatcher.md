# dispatcher
Updated: 2026-10-24 17:45 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 30
State: working
Now: item 31 (task c019): ft2 GPU job 2 (32 middle and late windows) running; backup roots for 4 failed picks: seg and copy running, then a GPU job
Done since last update:
- ft2 GPU job 1 (13 early windows): 16 min, $0.045; about 75 s per 80-frame window on a P100. Spent since 2026-10-23: $0.74 actual, $1.41 with job 2's worst case
- Seg midlines for all 64 windows (C 48, B 16) on the lab server, about 31 s each
- Tip rule on the picks (net tip within 15 px of the mask apex, median of 5 frames): pass 0708_c5, 0711_c4, 0714_c10, 0721_c1, 0721_m4, 0721_m9, 0727_mc1, 0727_mc5, 0727_mm6; fail 0708_m8, 0711_m4, 0714_m10, 0727_mc3 (medians 580-800 px). Backups 0714_m2, 0711_m6, 0714_m13, 0727_mc4 in progress
- tip_apex_probe fix: a frame whose seg midline is under 40 px gets no apex (was IndexError)
- Proposal amended: the pool allows the 0727 acquisition-gap flag (every 0727 root has it; the windows end before it)
Needs Andrew:
- Cluster work folder cap 30 GB: now 25.1 GB. Backups bring C to about 30.2 GB, and B's 16 windows (about 7 GB) do not fit. Options: (a) raise the cap to 40 GB; (b) node-local unpack of gzip'd frames. B asks the same (wip/real-calib status), with (c) its midlines on the lab server CPU (about 8 h)
- Tip rule (FYI, no change made): on every failing frame the tracking polyline end is 19-30 px behind the apex, the same as on passing roots. Only the net's separate tip point (`tip_xy`) jumps to the far end of the root. The rule rejects roots whose midline is fine; all 4 rejected picks are drought or recovery roots. Keep the rule, or test the polyline end instead?
