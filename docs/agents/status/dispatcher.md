# dispatcher
Updated: 2026-10-24 20:15 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 34
State: working
Now: items 31-34 (task c019): 1000 px tracking of the 48 subset windows on the lab server; checks and the agent run held until real-calib's new threshold (40+ windows) is merged (item 34)
Done since last update:
- Item 33 (1): tip rule v2 (polyline end within 50 px of the mask apex) applied to every probed root; refilled by the proposal's slot order: 0714_m10, 0708_m8, 0727_mc3 return as picks; 0711_m4 still fails (618 px). Subset back to 16 roots, 48 windows; all 48 have ft2 midlines. Decisions entry and proposal section added
- Item 33 (2): noted, c019 lab-server folder up to 100 GB
- Item 33 (3): 0714_c13 midlines built for real-calib (GPU job 5432396, 2 min, $0.006), in c019/midline
- Spend since 2026-10-23: $0.93 of $15
Needs Andrew:
- My error: my tracking run started a net-midline build on the lab-server CPU (0721_m10 4-6 h, batch_midlines, 3 threads, nice 19, running about 45 min) because that window's ft2 midline exists only on the workstation. Item 25 rules this out. My kill was blocked by the permission check, so it is still running and will finish on its own. Kill pid 2139614 on the lab server if you want it stopped. Fixed for later runs: scripts/real_track.py now skips a window whose midline file is missing on the host
- Cluster folder is full: about 40,900 MiB of the 40,960 MiB cap (40 GiB, about 42.9 decimal GB; I counted the cap in binary units, say if you meant decimal GB). real-calib extension: 9 of 24 windows copied and on the GPU (job 5434764); 15 more plus 6 fallback windows (about 9 GB) need a higher cap or deletes there (Andrew only)
