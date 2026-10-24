# autotrace
Updated: 2026-10-23 20:35 (local)
Lane: course
Branch: wip/autotrace
Last inbox item done: 2
State: working
Now: item 3, drafting the 140 pack frames with the net (tile mode, fine-tuned net2, lo 0.1, hi 99.5)
Done since last update:
- Item 2, landmark: 10 July trace frames from include-yes 0708 roots (c10, c11, c2, c4, c5, c6, c8); trace tip end vs classical root-mask apex along the extended trace
- The July traces run tip -> base (all 115: first point at the cap, last at the frame edge), not base -> tip as in the tool docstring. Measured from the first point
- Offset trace end to mask apex: 9 valid frames, median 35.3 px = 74 um (2.105 um/px), range 23.4-63.5 px. 1 frame excluded: mask merged with a bubble at the tip (81 px, not the apex)
- Rule (20-60 px band, so near the quiescent centre): every draft ends on its midline 35 px behind the root-mask apex. Net midline cut there if longer, extended straight along its end tangent if shorter; extension length recorded per frame
- Drafts are written base -> tip as the inbox says; fine-tuning rasterizes the polyline, so order does not change it
Needs Andrew:
- none (say if drafts should instead run tip -> base like the July traces)
