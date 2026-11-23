# Spec: two growth-zone placement checks (report-only)

From: planning account. Date: 2026-11-23. Approved by Andrew 2026-11-23 (answer to Lab report 3 feedback: checks that catch a misplaced growth zone without ground truth). Lane: course. Task: c034. Session: real-calib.

## Why
- Closure uses only the summed tip displacement, so it cannot see where along the root growth sits. A zone shifted along $s$ can pass every current check

## Checks (new functions in `checker/zone_checks.py`, deterministic, no LLM)
1. Plateau: past the growth zone the velocity profile in the tip frame is flat at the tip speed and $\dot\varepsilon \approx 0$. Value: largest $|\bar{\dot\varepsilon}(s)|$ (%/h) over the basal part of the tracked span, where the basal part is fixed by rule before any real window is looked at (e.g. the basal third of covered $s$), plus $|v(s_{\text{base}}) - v_{\text{tip}}|$ relative to $v_{\text{tip}}$
2. Material-point prediction (Silk particle path): integrate $\frac{dX}{dt} = v(X, t)$ from the window-mean velocity profile for tracked points seeded along $s$ at frame 0; compare predicted with tracked positions at the last frame. Value: RMS and max of the difference (px), and the same normalised by the tracked displacement

## Thresholds and validation
- Synthetic first: freeze v4 clean rods (values on correct fields) and new rods with the zone shifted tipward and basally by 1, 2 and 4 patch spacings (fixed seeds, listed in the proposal). Thresholds by the R4 rule (99.5th percentile on clean rods times 1.5), committed before any real window is checked
- Report: detection rate per shift size, false alarms on clean rods
- Real: run both on every c027 window (base and accepted tracks, from the cache; no new tracking). Report-only: they do not gate, and no c027 outcome changes. Counts of flags per outcome class and per condition; example windows by id

## Limits
- No zone positions, REGR, growth-zone or flank values in the public repo: pass/fail, residuals and counts only; anything else `[masked]`
- Shifted rods: rendered on the VM, tracked on the cluster CPU through `rod_jobs.py` (no tracking on the VM; ledger check before submit, $15 stop). No other cluster jobs
- No change to prompts, thresholds, remedies, the real profile or any scored result
- Branch `wip/zone-checks` from `origin/main`; proposal committed before any run; results in `results/2026-11-23_zone_checks/`; ready to merge by Fri 27 Nov 12:00
