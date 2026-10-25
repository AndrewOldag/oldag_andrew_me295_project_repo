# dispatcher
Updated: 2026-10-24 19:40 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 34
State: working
Now: items 31-34 (task c019): 1000 px tracking of the 48 subset windows on the lab server; checks and the agent run held until real-calib's new threshold (40+ windows) is merged (item 34)
Done since last update:
- Item 33 (1): tip rule v2 (polyline end within 50 px of the mask apex) applied to every probed root; refilled by the proposal's slot order: 0714_m10, 0708_m8, 0727_mc3 return as picks; 0711_m4 still fails (618 px). Subset back to 16 roots, 48 windows; all 48 have ft2 midlines. Decisions entry and proposal section added
- Item 33 (2): noted, c019 lab-server folder up to 100 GB
- Item 33 (3): 0714_c13 midlines built for real-calib (GPU job 5432396, 2 min, $0.006), in c019/midline
- Spend since 2026-10-23: $0.93 of $15. Cluster folder about 37.2 GB of 40
Needs Andrew:
- Cluster folder about 37.2 GB of the 40 GB cap: room for about 6 more midline windows. real-calib's 40-window calibration needs about 24 more (about 10 GB). Options: raise the cap to about 50 GB, or delete used frames there (Andrew only)
