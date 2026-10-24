# dispatcher
Updated: 2026-10-24 17:05 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 30
State: working
Now: item 31 (task c019): seg midlines on the lab server (about 33 s per window, 1 job); frames for the 13 early windows copying to the cluster; first ft2 GPU job next
Done since last update:
- Subset proposal `docs/proposals/2026-10-24_real-subset.md` (ea853da); C5 backup changed to 0714_c12 because 0711_c7 is in the B calibration set
- Pipeline per window: seg midline (lab server, single thread) -> window frames copied to the cluster -> ft2 tile-mode GPU job -> net_to_midline and tip-apex probe (lab server, light)
- real-calib's 16 calibration windows are added after mine to the same seg/copy/GPU queue and ledger (spec B: C's runner and ledger)
- Cluster ledger cap set to $15; spent since 2026-10-23: $0.69
Needs Andrew:
- Cluster work folder cap (30 GB) is too small for C plus B: 6.5 GB already there + C 48 windows (about 20 GB) + B 16 windows (about 7 GB) = about 34 GB, more with backups. Sessions cannot delete there. Options: (a) raise the cap to 40 GB; (b) allow jobs to unpack gzip'd window frames on the node-local scratch (saves a third; not covered by the cluster rules now). Until then C goes first and B's windows wait
