# dispatcher
Updated: 2026-10-24 02:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 20
State: waiting on Andrew
Now: item 20 done; real-movie profile gates closure only; real slice ran end to end; numbers provisional (current net)
Done since last update:
- Item 20 step A: zero-shift control 0.000 %/h; uncropped padded whole-pixel control 7.286 %/h (equal to the cropped 7.286); basal points (s > 250 px) 520-575 px from the frame edges against a 54 px margin, 0 point-frames within it; no edge-frozen points; valid frame pairs equal in both copies (79 of 79 up to s = 375 px). `results/2026-10-24_rigid_cause_test/`, `scripts/rigid_cause_test.py`
- Item 20 step B (second branch): rigid invariance on real windows reported, not gating; closure the only gate. Full-range value reported with the profile-window value beside it. Decisions entry as planning account under delegation, with the numbers; known limit in the real-slice README
- Item 20 final run with agents: closure 0.945 pass; rigid 7.29 (window 5.76) and plane sections 133.6 reported; diagnostician not called (no gating failure); auditor flagged the accepted run from the non-gating values. `results/2026-10-24_real_slice_closure_gate/`
- Suite 242 passed, 1 skipped
Needs Andrew:
- None for this item. Note: with closure as the only gate on real windows, acceptance rests on the auditor reading the reported values (it flagged this window)
