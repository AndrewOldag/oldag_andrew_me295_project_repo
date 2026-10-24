# dispatcher
Updated: 2026-10-24 00:40 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 18
State: waiting on Andrew
Now: item 18 done; real slice runs with the real-movie profile and rigid invariance; rigid invariance fails on the real window
Done since last update:
- Item 18 (1, 4): real-movie checker profile: rigid invariance and closure gate; plane sections computed and reported, not gating. Applied by `agents/executors.py` (CHECK_PROFILES, from the record's movie setting); checker code and thresholds unchanged; tests for both profiles (6 passed)
- Item 18 (2): decisions entry; known limit in `results/2026-10-24_real_slice/README.md`
- Item 18 (3): synthetic rods and freeze v3 keep all three checks; synthetic auditor tables byte-identical (test)
- Item 18 (5): rigidly moved copy of the real window (`scripts/remote/real_moved.py`; synthetic rods' rigid motion, unlogged; 7.9 deg and (39.5, 23.7) px at the window end). Real slice with agents: rigid_invariance 8.83 %/h FAIL (threshold 2.0), closure 0.945 pass, plane_sections 133.6 reported; diagnostician declined (smooth_midline light rolled back: rigid 16.76); auditor report. Provisional (current net)
- Auditor view: non-gating checks marked (`gating: false`; "not gating" in the table) after the auditor called the first view inconsistent; auditor re-run on the recorded batch
- Suite 240 passed, 1 skipped
Needs Andrew:
- Rigid invariance on real windows: 0.8-3.4 %/h along the centre profile, 8.8 at the chain end (s >= 400 px), flanks up to 4-6 %/h, against 2.0 set on synthetic rods. Possible parts: tracker response on real texture, bilinear resampling of the moved copy, chain-end coverage. Not changed; options for you: a moved copy without resampling (translation by whole pixels only), a profile window that excludes the chain end, or a real-movie threshold (a threshold change: your approval)
