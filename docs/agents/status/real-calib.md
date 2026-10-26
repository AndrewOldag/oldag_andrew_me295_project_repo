# real-calib
Updated: 2026-10-25 21:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 10
State: working
Now: item 11: batch 2 (91 roots, 1063 windows) running root by root on the cluster (one GPU job per root: segmentation, ft2 midline, tracking midline, tracks), 2 jobs at a time; outputs copied to the lab server with md5 checks, then the root's staged frames cleared; checker passes every 10 min. The driver stops by itself when the cluster connection closes (about 01:00)
Done since last update:
- Whole per-root cluster chain equal to the first-batch chain on 0708_c2 (12 windows): tracking midlines identical, tracks within 2.6e-7 px, checker values equal (decisions 2026-10-25)
- Batch 2 started: 0708_c4 and 0708_m2 done in 25 min each (about $0.07 per root); folder under 35 GB; spend since 2026-10-23 about $2.0 of $15
- `scripts/full_batch.py` batch 2 committed
Needs Andrew:
- Cluster connection master closes about 01:00: batch 2 stops there (about 18 roots expected done). Reopen it to continue; the driver resumes from its markers
