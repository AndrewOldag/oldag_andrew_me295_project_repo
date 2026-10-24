# freeze-v31
Updated: 2026-10-24 12:24 (local)
Lane: course
Branch: wip/freeze-v31
Last inbox item done: 7
State: waiting on Andrew
Now: stopped at the spec stop rule: at most 1 of 5 faults can qualify (fewer than 3). No label sweep, no tag, no method runs
Done since last update:
- Sizing round 3 (workstation): bad_stage_correction 5 px, register_frames, 6 runs, 0 failed. Stored on the lab server and verified (460 files, sha256 equal)
- Sizing result, seeds 10-12 (`results/2026-10-24_freeze_v3.1/sizing.md`):
  - rigid_drift 0.5-5.5: unremedied good 3 of 3 up to 4.5; 5.5 not good 2 of 3. Out
  - width_change (one size), stage_log_missing 1: unremedied good 3 of 3. Out
  - displacement_exceeds_patch 2x2, 2x3, 2x4: unremedied not good 3 of 3; stride 1 fails rigid_invariance on every seed (35-55 %/h at 2x2). Out
  - bad_stage_correction: unremedied not good 3 of 3 from 5 px; at 5 px register_frames repairs 1 of 3 (s11 still fails; s12 good but rigid_invariance 3.02, just over). 6-8 px registration not run: the stop rule holds whatever they give
- Tracker runs new: 120 of 300 (13 lab server, 107 workstation). Renders on the workstation kept (sizing renders deletable under the exception; not deleted yet)
Needs Andrew:
- Stop rule (spec): fewer than 3 faults qualify. Options:
  - (a) End v3.1 here. v3 stays the scored set; the README states that no listed fault at these sizes needs its repair under the fixed checker and remedies (a finding about the set, not a method result)
  - (b) Finish bad_stage_correction 6-8 px (18 runs) and score a 1-fault v3.1 set (3 rods), below the spec minimum of 9
  - (c) Change the rule or sizes (e.g. 2 of 3 seeds; rigid_drift above 5.5; displacement at speed 1). A spec change; planning to write it
- Main checkout `private/workstation.md` is the old copy; refreshed copy in this worktree's `private/`
- Pre-push blocklist flags line 22 of `docs/agents/inbox/autotrace.md` (on main); not pushed again from here
