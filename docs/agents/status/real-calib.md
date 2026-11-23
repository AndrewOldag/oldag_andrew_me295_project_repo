# real-calib
Updated: 2026-11-23 08:46 (local)
Lane: course
Branch: wip/supervisor
Last inbox item done: 29
State: idle
Now: wip/supervisor merged into main at 114a3b5; no inbox item after 29 (checked 2026-11-23 08:46); waiting for a new item (c032 switch-over waits for a planning item after Thu 26 Nov 12:00)
Done since last update:
- Item 28 replaced by item 29
- Item 29 (c032): scripts/ops/supervisor.ps1, register_detached.ps1, install_supervisor.ps1 (not run); tests/test_supervisor.py 12 passed; test_ops, test_board 18 passed; README, decisions, log, task to review
- Two limits beyond the spec (decisions): the same session is not restarted within 60 min of its last supervisor start (a session that exits with an inbox item still open would else restart every tick); status read from the newest `Updated:` over all origin branches
- For planning: sessions that exit while an item is open should still keep `Last inbox item done` below the inbox (supervisor then retries hourly), or write the item number with a note as dispatcher does (then only the 2 h stale rule applies, and only for State working)
- Seen on the VM: a pid file `real-calib,compound.pid` in the agents folder: `agents.ps1 -Names a,b` under `-File` takes "a,b" as one name. supervisor.ps1 splits on commas; agents.ps1 not changed
- Dispatcher and compound: when the supervisor is installed, register long detached processes with `scripts/ops/register_detached.ps1` (README)
Needs Andrew:
- none
