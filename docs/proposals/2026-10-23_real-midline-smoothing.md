# Real-movie midline smoothing for plane sections: proposal

From: build account, dispatcher session. Date: 2026-10-23. Inbox item 16. Proposal only: nothing here is implemented, and nothing in the checker, `curvature_smooth_px` or freeze v3 changes. Needs Andrew's approval.

## Problem
- Plane sections compares the flank difference with flank spacing x the material rate of curvature. The curvature comes from the per-frame midline source (`measure/record.py`, `derive`), at `curvature_smooth_px` 0 (frozen)
- On the real window (0708_m12, 4-6 h, net midline, 400-950 px tracked) plane sections is 134-247 %/h against 3.25. The flank difference is 9-34 %/h; the predicted term carries the value
- Cause: the net midline is a skeleton of a thresholded valley map, resampled. Its curvature changes 0.01-0.04 /px from frame to frame against a mean near 0.002 /px. With 28.5 px flank spacing that gives about -195 %/h at s = 575 px (`results/2026-10-23_tracker_timing/README.md`)
- Synthetic rods do not show this: their midlines are rendered without pixel quantization

## Options

### 1. Spatial spline fit per frame (midline source only)
- What changes: each frame's net polyline is replaced by a smoothing-spline fit (parametric, x(s) and y(s), cubic) before resampling, in the step that writes the midline file (`net_to_midline`, today a probe script). `measure/`, the checker and `curvature_smooth_px` are unchanged
- One parameter: the spline smoothing factor. Fixed rule, set now, before any real result is looked at: the fit residual equals the pixel quantization, rms 1/sqrt(12) = 0.289 px. In scipy terms `splprep(..., s = K x 0.289^2)` with K the number of polyline points of that frame
- Effect on the physics: removes sub-pixel staircase noise only; a real bend has curvature changes over tens of px, far above the residual budget
- Risk: end effects at the tip, where curvature is highest. Mitigation, also fixed now: no extra end conditions; the tip end keeps its fitted position (it moves at most the residual)
- Validation on v3 synthetic rods: apply the same fit (same rule) to every rendered midline of the v3 clean and fault rods, re-derive, re-run the checker. Every checker value (closure, plane_sections, rigid_invariance) must be unchanged within 1e-3 in its unit. If any value moves more, the option fails as written and is reported; the rule is not retuned

### 2. Time smoothing of the midline (midline source only)
- What changes: each midline point is smoothed over frames, in a tip-anchored frame, before the midline file is written
- One parameter: the time window. Fixed rule: the shortest window that brings the frame-to-frame curvature change below the mean curvature on the synthetic clean rods
- Effect on the physics: it averages exactly the quantity plane sections tests, the curvature rate. A real bending episode shorter than the window is blurred
- Conflict: `smooth_midline` is a remedy in the fixed list (freeze v2, v3). Always-on time smoothing removes the remedy's meaning and changes what the diagnostician sees as `midline_jitter`
- Validation on v3 synthetic rods: as for option 1, all checker values unchanged within 1e-3. Expected to fail on the `bending` and `width_change` rods, whose curvature rate is the signal

### 3. Curvature from the tracked centre chain (checker input)
- What changes: `derive` takes curvature from `rec.centre` (tracked material points) instead of `rec.midline`. This is a checker input change: a freeze item
- One parameter: none new (the chain spacing, 15 px, is a tracker setting). Curvature resolution is limited to the chain spacing
- Effect on the physics: removes the midline source from plane sections, but adds tracking noise and a 15 px resolution limit, and makes the check depend on the tracker it is meant to test
- Validation on v3 synthetic rods: all checker values unchanged within 1e-3. Expected to fail: tracking noise on the chain differs from the rendered midline, so plane-sections values change on every rod

## Recommendation
- Option 1. It changes only the midline source, not the checker or any frozen setting; its one parameter has a physical value set in advance (the pixel quantization); and on rendered synthetic midlines it should leave every checker value unchanged, which the validation tests
- Order if approved: implement the fit in the midline-file step with a test (a smooth circle arc with 0.5 px staircase noise comes back within 0.3 px rms and with curvature within 5 % of the arc); run the v3 validation; report pass or fail; only then re-run the real t3 window and report plane sections as measured
- Not proposed: any change to `curvature_smooth_px`, the plane-sections threshold, or the checker code
