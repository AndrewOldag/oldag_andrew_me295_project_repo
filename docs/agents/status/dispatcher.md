# dispatcher
Updated: 2026-10-25 00:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 35
State: waiting on Andrew
Now: agent run over the 48 subset windows was stopped by Claude Code for low VM memory after 1 window; not restarted (needs Andrew)
Done since last update:
- Item 33 (1): tip rule v2 (polyline end within 50 px of the mask apex) applied to every probed root; refilled by the proposal's slot order: 0714_m10, 0708_m8, 0727_mc3 return as picks; 0711_m4 still fails (618 px). Subset back to 16 roots, 48 windows; all 48 have ft2 midlines. Decisions entry and proposal section added
- Item 33 (2): noted, c019 lab-server folder up to 100 GB
- Item 33 (3): 0714_c13 midlines built for real-calib (GPU job 5432396, 2 min, $0.006), in c019/midline
- Item 35: after the cluster frames were cleared, real-calib's last 21 calibration windows (15 planned + 6 fallback) ran: GPU job 5437471, 24 min, $0.068; all 21 netmids in the lab-server task folder. Spend since 2026-10-23: $1.03 of $15; cluster folder about 15.7 GB of 40
Needs Andrew:
- Restart of the subset agent run: Claude Code stopped `scripts/real_slice.py` (48 windows) because the VM was critically low on memory (7.7 GB total, several Claude sessions open; 3.4 GB free afterwards). One window had finished its diagnostician pass. Tracking is all cached, so a restart runs only agent steps and remedy retracks. Restart now, or after other sessions close? (Optional: start Claude Code with CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 to stop these kills.) Partial traces kept in staging/c019/killed_run_1/
