# dispatcher
Updated: 2026-10-24 02:00 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 19
State: waiting on Andrew
Now: item 19 stopped at step 3: rigid invariance fails on the real window with both the whole-pixel copy and the profile window
Done since last update:
- Item 19 step 1: whole-pixel moved copy (translation only, round((0.5, 0.3) px per 90 s x t), max (40, 24) px; both copies cropped to the common area; exact in a test). rigid_invariance 7.29 %/h FAIL (2.0). First 250 px from the tip agree within 1.0 %/h on all three profiles; difference grows toward the chain end (centre 2.0-2.2 at 250-350 px, 5.8 at 350-400; minus flank 7.3 at 400-450). `results/2026-10-24_rigid_whole_pixel/`
- Item 19 step 2: profile-window rule committed to decisions before the rerun (compare up to the last centre point tracked in every frame, both copies; s_cov = 398 px here). rigid_invariance 5.76 %/h FAIL at s = 375 px. `results/2026-10-24_rigid_window/`. Note: the per-band differences of step 1 were seen before the rule was written; the rule follows your example wording
- Closure 0.945 px/h pass in all runs; plane sections reported, not gating
- Code: `scripts/remote/real_moved.py --mode whole_pixel`, `RealRunner(moved_mode="whole_pixel")` default, `agents/executors.py` real_rigid_invariance (checker code and thresholds unchanged); suite 242 passed, 1 skipped
Needs Andrew:
- Rigid invariance on real windows fails both ways (7.29, 5.76 %/h against 2.0). The tip-side 250 px agree within 1.0 %/h; the excess sits in the basal 100-150 px of the 400 px chain. Your call: a shorter profile range (a new rule), a different tracked length, a real-movie threshold (threshold change), or rigid invariance not gating on real windows like plane sections
