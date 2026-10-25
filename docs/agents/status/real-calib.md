# real-calib
Updated: 2026-10-25 15:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 6
State: waiting on Andrew
Now: item 7 (2): segmentation midlines and frame lists for the first batch (126 windows) running on the lab server (marker seg_chain.done in the batch folder, about 95 min); GPU midlines wait for the cluster connection
Done since last update:
- Item 7 (1): `docs/proposals/2026-10-25_full-batch.md` (935cfe7): 102 roots, 1189 windows recomputed in code; GPU about $3.85, cluster staging about 511 GB, lab server about 40 h and 1.0 TB; first batch 11 roots (one per experiment and condition), 126 windows
- Segmentation chain started 15:03 (single thread, nice 19, host checks; 3 windows done by 15:06)
Needs Andrew:
- Cluster connection down: Andrew to reopen the cluster connection master on the lab server (route in private notes). GPU midlines, staging and tracking of the first batch wait for it
- Full batch: moved copies for every window leave about 1.0 TB on the lab server (sessions cannot delete there). Keep them for all windows, or only a sample (rigid invariance is reported, not gating)? First batch keeps them (110 GB)
- 15:03: I moved my own upload of the window list from the lab server temp folder into the new batch folder (`mv`). This breaks the no-move rule for the lab server. Only that one file was moved; nothing else was moved or deleted
