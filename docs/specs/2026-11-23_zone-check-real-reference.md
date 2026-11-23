# Spec: real reference set and threshold for the growth-zone particle-path check

From: planning account. Date: 2026-11-23. Approved by Andrew 2026-11-23. Lane: course. Task: c035. Session: real-calib. Follows c034.

## Why
- c034: synthetic thresholds flag every accepted real window. In the worst real windows almost all of the particle-path residual is common to every point and follows the drift of the first tracked point's distance from the midline tip (an anchoring drift, not a misplaced zone)
- A real threshold needs a real reference set and Andrew's approval (c034 README)

## Steps
1. Decompose the particle-path residual: common mode (mean over points, along $s$) and shape (residual minus common mode). Report both. Re-run the c034 synthetic set: the shape part must still catch the shifted profiles (report detection per shift); if it does not, stop and say so in status
2. Reference sample, rule committed before drawing: 24 accepted c027 windows, seed fixed in the proposal, stratified 4 or 5 per condition, include-yes roots and usable windows only
3. For each sampled window, one overlay image set for Andrew: first, middle and last frame with midline, midline tip, tracked chain (first point marked) and predicted particle positions. Images stay on the VM in `staging/c035_overlays/` (not pushed: raw root images). A one-page index `staging/c035_overlays/index.html`
4. Andrew labels each window `clean` or `not clean` (tip or first point visibly wrong, profile visibly misplaced) in `staging/c035_overlays/labels.csv`; the session waits for it (status `waiting on Andrew`)
5. Threshold rule, committed in the proposal before Andrew labels: on the `clean` windows, 99.5th percentile of the shape residual (relative) times 1.5; the same for the common mode as an anchoring-drift flag. Andrew approves the two values before they are used
6. Apply to all 1,189 c027 windows, report-only: counts flagged by shape and by common mode, per outcome class and condition, example ids. No c027 outcome changes; gating is future work
7. Results `results/2026-11-23_zone_reference/` (counts, residuals, thresholds; no zone positions or biology values); ready to merge by Fri 27 Nov 12:00

## Limits
- No cluster jobs, no tracking, no LLM runs. Branch `wip/zone-reference` from `origin/main`
