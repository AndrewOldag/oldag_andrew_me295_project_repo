# dispatcher
Updated: 2026-10-23 14:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 8
State: waiting on Andrew
Now: item 8 done except the CPU cluster job (running) and the plane-sections rerun on the net midline (net previews fail)
Done since last update:
- Item 8, cluster: GPU job 5350185 ok, 80 frames, 11 min 15 s, $0.032, stage_source aux_stage_tracking; ledger actual written. Previews fail: midline ends about 280 px short of the tip (tip confidence 0.18). CPU job 5350184 running, in the midline stage at 31 min
- Item 8, closure vs tracked length: t3 0.65 (700 px, pass), 4.71 (950); t2 7.22 (700), 5.08 (950) px/h. Not monotonic. Checker unchanged
- Item 8, plane sections: 440-558 %/h; cause: curvature noise of the provisional pixel-skeleton midline (0.04-0.09 /px frame to frame at smoothing 0)
- Item 8, 0727_cc7: usable_to_h 9.5 -> 4.05; rule in decisions (696784d)
- Item 8, B5 part 1: dispatcher engine, typed actions, fake queue, script baseline, prompt, config, demo; 19 tests; full suite 222 passed (697321b, c42dfca, and later commits)
- Item 8, tracker: stage-auxdata merged into gate2-windowed-coupling --no-ff, 52e9bd1, pushed; tests 46 passed, 9 skipped
- Item 8: estimate.md updated with the cluster GPU numbers ($0.032 per window, about $38 for all include-yes windows)
Needs Andrew:
- Cluster runner midline on SlideBook frames: it stops about 280 px short of the tip (scale factor 2.506, tip confidence 0.18-0.25). Which net scale or setting to try? Not changed by this session
- Closure: residual not explained by tracked length alone (pass at 700 px on t3 only). Next step: run closure with a smooth midline source, or look at the frame pair with the largest residual (pair 7 in t3, 16 in t2)?
- Plane sections need a smooth midline: the net midline (once its scale works) or a smoothed provisional midline? `curvature_smooth_px` is a frozen setting
- Lab-server work folders hold probe scripts, preview images and tracker outputs (no deletes by sessions)
