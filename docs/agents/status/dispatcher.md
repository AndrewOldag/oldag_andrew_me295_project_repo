# dispatcher
Updated: 2026-10-24 14:33 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 28
State: waiting on Andrew
Now: item 28 stopped at both decision points: jitter does not explain the ft2 closure change; no control candidate reaches tip confidence 0.5
Done since last update:
- Item 28 (1), `results/2026-10-24_closure_ft_vs_ft2/`: 0708_m12 4-6 h tip jump median 2.00 px for ft and ft2 (p90 4.58 / 4.30); closure 0.945 / 4.52; with the tip path fitted in time 2.96-3.75 (ft) / 4.36-5.15 (ft2) px/h. Closure telescopes to the end-frame tips; ft2's frame-0 tip lies 5 px behind ft's. ft's pass came from end-frame noise; neither net closes with the noise removed. Tip stabilization not applied
- Item 28 (2): candidates (include-yes control, no notes, montage, not 0708/0721), ft2 tip confidence median on 5 window frames: 0714_c10 0.310, 0714_c11 0.026, 0711_c2 0.418. None >= 0.5; 3 tried; no full run
- Decisions entries for both choices with outcomes; log entry pending; workstation work folder 18.8 GiB of 20, 27 GB free; lab-server segmentation midlines for the 3 candidates (light, about 35 s each)
Needs Andrew:
- Closure on real windows: with tip noise removed, ft2 0708_m12 closure is 4.4-5.2 px/h (ft 3.0-3.7); the tip moves 2-9 px more than the tracked chain over 2 h. Look at the chain base (s = 489 px) or the stage correction next, or another step?
- Control root: no candidate reached 0.5 (best 0711_c2 0.418). Lower the bar, try more candidates, or run 0711_c2?
- ft2 tip confidence is low on every root but 0708_m12 (0.176-0.418); the confidence scale may not compare across experiments
