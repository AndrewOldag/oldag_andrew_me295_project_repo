# real-calib
Updated: 2026-11-02 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 13
State: waiting on Andrew
Now: paused (Andrew, 2026-11-02: lab server down; restart later). Batch 2 at 50 of 91 roots
Done since last update:
- Batch 2: 50 of 91 roots collected (md5 verified, frames cleared), 0 errors, no job lost; 570 windows checked
- 3 roots staged on the cluster, not submitted (0721_c6, 0721_m6, 0727_cc6; the last may be partial)
- Driver, state markers and restart scripts kept in this worktree's git-ignored `private/` (`fb2_driver.py`, `fb2_state/`, `fb2_scripts/`)
- Log entry in `docs/running_log_pending/real-calib.md`
Needs Andrew:
- Restart when the lab server is back: run the batch-2 driver and checker loop (resume from markers): 41 roots, about 8 h, about $2.9 more (projected total about $7.6 of $15)
- Merge of main into this branch is refused by the pre-push blocklist (main's inbox file names the cluster); the coordinator merges this branch
