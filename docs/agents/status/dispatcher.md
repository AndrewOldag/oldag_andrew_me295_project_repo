# dispatcher
Updated: 2026-10-24 18:15 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 30
State: working
Now: items 31-32 (task c019): ft2 midlines done for all C windows (net_to_midline running); B's 16 windows on the cluster GPU (job 5431374); next: 1000 px tracking of the 48 subset windows on the lab server (main with closure-fix merged into wip/dispatcher)
Done since last update:
- GPU jobs: 5429172 (13 windows, $0.045), 5429963 (32, $0.100), 5430544 (4 backups, $0.014), 5431144 (7, $0.022); all rc 0, 60-100 s per window. Actual spend since 2026-10-23: $0.87; with job 5431374's worst case: $1.55 of $15
- Tip rule: picks 9 pass, 4 fail (0708_m8, 0711_m4, 0714_m10, 0727_mc3); backups 0714_m2, 0711_m6, 0714_m13 pass, 0727_mc4 fails (1139 px); slot R5 third try 0727_mc13 (probe pending)
- Subset so far: control 0711_c2, 0708_c5, 0714_c10, 0721_c1, 0711_c4; drought 0708_m12, 0711_m6, 0714_m13, 0727_mm6, 0714_m2; recovery 0721_m10, 0721_m4, 0721_m9, 0727_mc1, 0727_mc5, R5 pending
- Cluster cap 40 GB (Andrew, via real-calib; decisions on wip/real-calib). Folder at 36.0 GB after B's copy. B and C root sets checked: disjoint
- Item 32: main (closure-fix, TRACK_LENGTH 1000) merged into wip/dispatcher
Needs Andrew:
- Tip rule (FYI, no change made): on every failing frame the tracking polyline end is 19-30 px behind the apex, as on passing roots; only the net's separate tip point (`tip_xy`) jumps to the far end of the root. 5 of 18 probed roots were rejected for this, all drought or recovery. Keep the rule, or test the polyline end instead?
- Lab-server storage: rigid-invariance copies are about 0.86 GB per window, about 41 GB for the 48 C windows (task folder; no deletes). Disk has 17 TB free. Say if this needs a cap
