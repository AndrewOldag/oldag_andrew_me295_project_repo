# real-calib
Updated: 2026-10-29 10:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 13
State: waiting on Andrew
Now: batch 2 stopped at 50 of 91 roots. The driver last ran 2026-10-26 16:22 (two staging rsyncs failed when the lab-server connection dropped); Claude Code then stopped the driver, the checker loop and its wait for low VM memory. Not restarted (needs Andrew)
Done since last update:
- Andrew 2026-10-26: deleting whole-root cluster copies this session made, after md5 check, approved (decisions)
- Batch 2: 50 of 91 roots collected (md5 verified, frames cleared), 0 errors, no job lost (every submitted root collected); 570 windows checked on the lab server
- 3 roots staged on the cluster, not submitted (0721_c6, 0721_m6, 0727_cc6; the last may be partial; the driver re-runs the copy and checks file counts)
Needs Andrew:
- The lab server does not answer from the VM (ssh timeout, 2026-10-29 10:17); the cluster is reached through it
- Restart of the batch-2 driver and checker loop after the memory stop (resumes from markers): 41 roots, about 8 h of cluster time, about $2.9 more (projected total about $7.6 of $15)
- Merge of main into this branch still refused by the pre-push blocklist (main's inbox file names the cluster); the coordinator merges this branch
