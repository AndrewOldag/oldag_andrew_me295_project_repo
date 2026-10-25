# Spec: real-movie push to Wed 28 Oct: closure fix, real noise floor, 16-root subset

From: planning account. Date: 2026-10-24. Approved by Andrew 2026-10-24 (all three items and a $15 cluster budget). Lane: course. Goal: real windows that are good get accepted, bad ones declined, on a 16-root subset, end to end. Build stops Wed 28 Oct.

## Sessions
| Session | Task | Job | Starts |
| :-- | :-- | :-- | :-- |
| closure-fix | c017 | A. real-movie closure definition | now |
| real-calib | c018 | B. real-image noise floor and real thresholds | now (rigid invariance); closure after A |
| dispatcher | c019 | C. 16-root subset, midlines now, checks after A and B | now (midlines) |
| diag-analysis | c020 | D. why the diagnostician declines repairable rods | now |

## A. Closure on real movies (closure-fix)
- Facts: with tip noise removed, closure on real windows is 3.0-5.2 px/h against 1.0 (synthetic threshold). The tracked chain ends near the quiescent centre, about 35 px behind the apex; the tip reference is the apex; the tip moves 2-9 px more than the chain over 2 h
- Hypothesis to test: a definition mismatch (the apical segment between chain end and apex grows and the cap slides), not bad data
- Tests on 0708_m12, 0711_c2, 0721_m10 (existing outputs; no new midlines): closure computed against (1) the apex, (2) the net tip point, (3) the chain's own most apical material point, (4) the apex with the apical segment's growth added from the fitted velocity profile. Also: pixel scale against the stage-step multiples (2.105 um/px), stage-correction sign and step alignment, and the chain base
- Pick the definition that matches the physics (state the reason in kinematic terms: what moves with what). Validate: every v3 synthetic checker value changes by at most 1e-3, and the v3 scored outcomes are unchanged. If no definition meets that, stop and report
- Measurement fix only: thresholds unchanged. Decisions entry, tests, results README `results/2026-10-25_closure_definition/`

## B. Real-image noise floor (real-calib)
- Calibration set, fixed now: control-condition windows (2 h, inside usable hours, include yes, montage, stage-tracking table covering the window) from roots NOT in the C subset, at least 12 windows from at least 3 experiments. Fixed non-growing roots only if imaged on the same rig and scale (2.105 um/px montage); otherwise not used. Write the list and the rule in `docs/proposals/2026-10-24_real-calibration.md` and commit it before computing anything
- Rigid invariance: now, on the calibration set (ft2 midline, current definition). Closure: after A is merged, with the A definition
- Real-movie threshold = the 95th percentile over the calibration windows, rounded up to 2 significant figures. Reported with the distribution. Andrew approved this rule on 2026-10-24; record it in decisions with the numbers
- Plane sections stays reported, not gating
- Compute: midlines on the cluster GPU (C's runner and ledger), tracking light on the lab server (single thread, nice 19, usual checks)

## C. 16-root subset (dispatcher)
- Subset, fixed now, written to `docs/proposals/2026-10-24_real-subset.md` before any run: 16 include-yes montage roots, about a third each control, drought, recovery, from at least 4 of the 5 experiments; stage-tracking table covering the windows; ft2 tip point within 15 px of the mask apex (median of 5 frames; the rule of item 29); none in B's calibration set; 0708_m12, 0711_c2, 0721_m10 included. 3 windows per root, 2 h each, inside usable hours, spread (early, middle, late)
- Midlines now: ft2 net midlines on the cluster GPU (private runner copy; P100 or V100 by availability), window frames only, one root at a time into the cluster work folder (at most 30 GB there in total). Ledger check before every job; total spend since 2026-10-23 under $15 (Andrew, 2026-10-24); worst case per job from its time limit
- Tracking: light single-thread jobs on the lab server (data stays there), or cluster CPU if the lab-server load is above half the cores. Never more than the lab-server limits
- Checks and agents after A and B are merged: real-movie checker profile with the A closure and the B thresholds; diagnostician; auditor over the whole batch (control vs stressed). One README command. Results `results/2026-10-2x_real_subset/`
- Report per window: pass/fail per check, decision, field summary (peak REGR, growth-zone length), and the auditor's batch report

## D. Diagnostician on repairable rods (diag-analysis)
- From the v3 traces only (no new runs): for every accept_repaired rod the diagnostician declined, the step where it chose decline, the evidence it had, and whether a listed remedy was available and would have worked (from the label sweep). Group the causes. Compare with the remedy tree on the same rods
- Output `docs/proposals/2026-10-25_diagnostician-repair-misses.md`: causes, counts, and at most 3 candidate prompt or info changes for a later freeze. Change nothing now

## Limits (all sessions)
- No deletes anywhere, except the existing freeze-v31 render exception. Lab server: storage plus light jobs only. Workstation: full (19.3 of 20 GB): copy nothing more there
- Real movies: include yes and usable windows only
- Freeze v3 untouched. Synthetic thresholds untouched; real-movie thresholds only through B's rule
- Every result marked with the midline (ft2) and the closure definition used
- Nothing in tracked files names machines, accounts or paths outside the repo

## Done means
- A merged with tests; B thresholds recorded; C results for 16 roots x 3 windows with the agent run; D proposal. All by Wed 28 Oct evening
