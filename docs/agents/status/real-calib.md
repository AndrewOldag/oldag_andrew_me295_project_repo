# real-calib
Updated: 2026-11-22 15:40 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 27
State: waiting on dispatcher
Now: c031 done except one item: the flagged window's register_v2 track through the option A gate, once dispatcher's c027 cycle has fetched it. Everything else on this branch can be merged now
Done since last update:
- Merged origin/main (49bc3c1); integrity, executor and record tests 35 passed
- R1 (job 7841039): v1's 9.23 deg is the chained sum of 79 small pair rotations (mean 0.117 deg, largest 1.0 deg, every pair ECC >= 0.967). Fitting each frame to frame 0 (v2) is erratic up to 6.0 deg and fails on 59 of 79 frames; plausible false, so v2 rolls this remedy back. results/2026-11-20_registration_fix/
- Staged root 0711_c5 deleted on the cluster (5.3 GB) after the output md5 matched on cluster, storage and here; DELETED.log
- R5 known limit written as Andrew decided (register_v2 kept; 3 of 6 vs 6 of 6); decisions, log, task c031
- Dispatcher: I need the register_v2 track of 0711_c5__w6-8 (and its base) in your c027 cache; I read it from there, nothing else
Needs Andrew:
- none
