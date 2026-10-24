# dispatcher
Updated: 2026-10-23 18:50 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 10
State: waiting on Andrew
Now: item 11 (contrast-stretch sweep, factor 2.506, low percentiles 0.3, 0.1, 0.01, min-max) waiting for the lab-server load: 1 min load 26 of 32 (another user); retry every 15 min, 3 tries
Done since last update:
- Item 9: net-scale sweep, 5 frames, CPU, lab server: midline end to true tip median 617 (1.0), 543 (1.5), 282 (2.0), 299 (2.506) px; tip net within 19-30 px at all factors; tip confidence 0.16-0.38
- Item 9: preview shows the tip zone (last 250-300 px) clipped to black by the 1-99.5 % contrast stretch; the midline stops there. No factor recorded, no GPU rerun
- Item 9: closure worst pairs: whole-pixel jumps of the provisional midline tip (0-6 px per pair) against a smooth tracked tip; residual is midline-source jitter
- Item 8 follow-up: cluster CPU job timed out at 2 h (midline 85 s per frame on 8 cpus), $0.193; ledger actuals written; spent today $0.45
- Item 10: noted; job scripts here start only when no other job of this account runs
- Item 12: noted; no workstation work assigned yet; will use only the approved ssh form when host-setup assigns it
- Item 13: private workstation file copied and read (20 GB cap on the work folder, at least 20 GB free, df before and after every step, frame subsets only); no workstation work assigned yet
Needs Andrew:
- Net midline: the contrast stretch, not the scale, seems to stop it short of the tip. Try a lower low percentile for the stretch (now 1 %; the darkest 1 % of a frame is about 29k px, close to the size of the tip zone, about 300 x 70 px) on the same 5 frames? Net and contrast settings not changed by this session
- Until a midline reaches the tip, closure and plane sections on real windows cannot be judged; the provisional midline is pixel-quantized (tip jitter 0-6 px per pair, curvature noise 0.04-0.09 /px)
- Lab-server work folders left as they are
