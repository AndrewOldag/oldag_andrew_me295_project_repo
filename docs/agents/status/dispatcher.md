# dispatcher
Updated: 2026-10-23 19:40 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 15
State: waiting on Andrew
Now: items 14-15 done; closure passes on the net midline (400 px); plane sections fails from midline curvature noise; B5 part 2 waits
Done since last update:
- Item 11: replaced by item 14 before it ran (lab-server load 26 of 32 from another user; no job started)
- Item 14, midline: tracker tile mode + fine-tuned net2 on 5 frames (workstation): midline end to tip median 2.0 / 2.2 / 3.2 px at low percentile 1 / 0.3 / 0.1 %; tip confidence 0.67 / 0.75 / 0.76. Kept 0.1 %, in decisions
- Item 14, whole t3 window with the net midline: 80 frames, 1411 s on 8 threads, tip confidence 0.74. Closure 0.95 (400 px, pass), 1.48 (700), 2.26 (950) px/h. Plane sections 134 / 216 / 247 %/h (fail)
- Item 14, plane-sections cause: curvature of the per-frame midline (skeleton polyline) changes 0.01-0.04 /px frame to frame against a mean of about 0.002 /px at curvature_smooth_px 0 (frozen); flank spacing 28-29 px and flank difference within +-34 %/h look normal. Checker not changed
- Item 14, tracing pack: lab-server folder `me295/tracing_pack_20261023/`, 140 frames (35 per experiment, 84 roots), 769 MB, worklist in trace_midlines.py format; held-out roots (16): 0711_c5, 0711_c7, 0711_c8, 0714_c10, 0714_c5, 0714_m1, 0714_m11, 0721_c4, 0721_c6, 0721_c9, 0721_m8, 0727_cc2, 0727_mc2, 0727_mc7, 0727_mc8, 0727_mc9
- Item 15: workstation used for the sweep and the closure runs; 0708_m12 copy reused (frames linked, nothing pulled); disk 36 GB free before and after every step; work folder 9.9 GB
- No cluster job needed (CPU fast enough for 80 frames)
Needs Andrew:
- Plane sections on real movies: the curvature term needs a smooth midline. Options: curvature from a time-smoothed or spline-fitted midline, or from the tracked centre chain. Each changes a frozen setting or the checker input (freeze item)
- Fine-tuned net was trained on 0708 hand traces (includes 0708_m12); tip reach on other experiments not yet measured. The tracing pack's held-out roots can measure it after you trace
- Tracing pack ready for tracing: `python midline_ml/finetune/trace_midlines.py <pack>/frames --out <pack>/traces.json`
