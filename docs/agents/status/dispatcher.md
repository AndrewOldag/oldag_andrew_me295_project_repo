# dispatcher
Updated: 2026-11-20 15:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 50 (item 46, task c027, still working)
State: working
Now: c027 integrated run and wave-1 fetch/submit cycle running as detached hidden processes; registration held
Done since last update:
- Item 50: `scripts/retrack_queue.py` and tests alone on `wip/retrack-queue` from origin/main (13 passed), README section. Ready to merge
- Item 49: no register_frames retrack submitted (none ever was: arrays 7371854, 7372590, 7374329 are short tasks only; nothing to scancel). `submit` holds them (51 held); `run_all.py` counts every registered track as not cached, so such a step pauses. 8 run records whose decision used a registered track (2 accepted, 6 declined) and their 6 roots' auditor runs set aside in staging/c027/run/voided_register/, kept, not used
- Item 48: run cut-off for new windows Thu 26 Nov 12:00 (was Sat 17:00); main merged, c027 task file kept; groups staged only within 30 GB
- Item 47 and spend stop $15 in the c027 config
- Wave 1: groups g001-g003 submitted; 24 tracks fetched md5 checked (g001's 12 failed on a missing output folder and were rerun as g002; fixed with a test); 458 short jobs wait, about 3 roots per group
- Run at 450 window records: 388 accepted by rule (no failing check), 8 declined by rule, 10 declined by the diagnostician, 1 step limit, 1 error (arange: cannot compute length), 42 paused; 166 LLM calls of 900
- Cluster folder 27.6 GB of 30 GB (c027 13.6, c026 leftover staged root 5.2, c019 0727_cc7 4.7). Ledger spent $7.429
Needs Andrew:
- Keep the cluster master up for the wave-1 cycle (about 15 more groups, roughly 3 h); if it drops, the cycle exits and restarts from disk
- The c026 leftover staged root (5.2 GB) blocks one root per group; clear it after an md5 check, or say so and I will run clear_root on it
