# real-calib
Updated: 2026-10-24 20:30 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: waiting on Andrew
Now: item 5: calibration extended to 42 windows (14 roots x 3), committed before computing; 24 new windows need ft2 midlines; only about 6 fit under the 40 GB cluster cap
Done since last update:
- Item 5 extension appended to `docs/proposals/2026-10-24_real-calibration.md`: pool 14 control roots (unused C backups join), windows 7-9, 11-13, 15-17 h; polyline-end tip rule (50 px) for every window screened from now on; the 6 earlier drop-outs screened again; fallback 0708_c10, 0708_c11 if fewer than 40 are measured
- 24 new windows sent to the dispatcher's chain (seg on the lab server now; GPU up to the cap)
Needs Andrew:
- Cluster work folder about 37.2 of 40 GB; the 24 new windows need about 10 GB (copied frames cannot be deleted). Options: (a) raise the cap to about 50 GB; (b) Andrew deletes cluster frames already used; (c) ft2 midlines on the lab server CPU, one at a time, 3 threads, nice 19, about 30 min per window (about 9 h for the 18 that do not fit; heavier than light jobs). The pool has 42 windows for a 40 minimum, so most of them are needed
