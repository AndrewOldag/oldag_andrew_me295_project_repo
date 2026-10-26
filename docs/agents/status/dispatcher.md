# dispatcher
Updated: 2026-10-25 17:15 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 38 (36 in progress)
State: working
Now: item 38: repeat run 2 of 48 windows running (cached tracks only; started at 3.8 GB free, bar 3 GB); then run 3, agreement, README
Done since last update:
- Item 37 / 36 (1): subset run 1 done, 48 windows, wall 1059 s: 43 accepted, 5 declined at closure (19 px/h); auditor 2 flagged, 41 cleared; control 14/15, drought 12/15, recovery 17/18 accepted. README, tables and traces in results/2026-10-25_real_subset/; decisions entries
- Fault found: 0708_m8 17-19 h register remedy could not run (lab-server output existed, tracker never overwrites); runner now fetches existing host outputs; suite 310 passed, 1 skipped
- Item 37 restart found a bug: real_slice.py gave the dispatcher one row per root, so only 16 of 48 windows were split; fixed (one row per window, id ROOT~A-B), test added, suite 308 passed, 1 skipped; that run was stopped by me after its dispatcher step and restarted; partial traces in staging/c019/stopped_run_2/
- real_slice.py: waits before each window while free VM memory is below 2 GB (item 37)
- scripts/real_subset_report.py: per-window and per-condition tables (item 36)
- Item 33 (1): tip rule v2 (polyline end within 50 px of the mask apex) applied to every probed root; refilled by the proposal's slot order: 0714_m10, 0708_m8, 0727_mc3 return as picks; 0711_m4 still fails (618 px). Subset back to 16 roots, 48 windows; all 48 have ft2 midlines. Decisions entry and proposal section added
- Item 33 (2): noted, c019 lab-server folder up to 100 GB
- Item 33 (3): 0714_c13 midlines built for real-calib (GPU job 5432396, 2 min, $0.006), in c019/midline
- Item 35: after the cluster frames were cleared, real-calib's last 21 calibration windows (15 planned + 6 fallback) ran: GPU job 5437471, 24 min, $0.068; all 21 netmids in the lab-server task folder. Spend since 2026-10-23: $1.03 of $15; cluster folder about 15.7 GB of 40
Needs Andrew:
- none
