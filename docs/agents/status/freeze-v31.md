# freeze-v31
Updated: 2026-10-24 12:20 (local)
Lane: course
Branch: wip/freeze-v31
Last inbox item done: 7
State: working
Now: sizing round 3 on the workstation: bad_stage_correction 5 px, register_frames, 6 tracker runs
Done since last update:
- Sizing sweep 2 on the workstation: 102 of 102 runs, 0 failed. Outputs copied to the lab-server c014 folder and verified: 446 files, count and sha256 equal. Workstation after: 30 GB free, work folder 16 GB
- Sizing so far (`results/2026-10-24_freeze_v3.1/sizing.md`), seeds 10-12, unremedied:
  - rigid_drift 0.5-4.5: check fails 3 of 3, measurement good 3 of 3; 5.5: not good on 2 of 3. Does not qualify
  - width_change: good 3 of 3. stage_log_missing 1: good 3 of 3. Do not qualify
  - displacement_exceeds_patch 2x2, 2x3, 2x4: not good 3 of 3, no stride state repairs 3 of 3. Does not qualify
  - bad_stage_correction: good at 3 px; not good on 1 of 3 at 4 px, 3 of 3 at 5-8 px; register_frames at 5 px running
- At most 1 of 5 faults can qualify: the spec stop rule (fewer than 3 faults) will be met. I stop for Andrew after round 3; no label sweep
- Tracker runs new: 114 of 300 (13 lab server, 101 workstation)
Needs Andrew:
- Coming after round 3: stop rule. Options for Andrew in the next status
- Main checkout `private/workstation.md` is the old copy; refreshed copy in this worktree's `private/`
- Pre-push blocklist flags line 22 of `docs/agents/inbox/autotrace.md` (on main); not pushed again from here
