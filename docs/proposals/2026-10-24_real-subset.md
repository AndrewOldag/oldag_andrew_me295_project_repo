# Proposal: 16-root real subset (task c019)

Dispatcher session, 2026-10-24. Spec `docs/specs/2026-10-24b_real-movie-push.md`, section C; dispatcher inbox item 31. Fixed before any run of this subset. Nothing here is a result.

## Rule
- Pool: `include` yes, montage imgdir, `stage_tracking_log` yes, empty `notes`, no `flags` other than the 0727 acquisition gap (every 0727 root has it; the windows end before it), usable window covering 4-19 h. The gap exception was written in on 2026-10-24 after the first probe, when the 0727 backup check showed the first version excluded every 0727 root it had picked 0711_c1 is left out (replaced in the 3-root slice; its run stays a reported failure)
- 16 slots: 5 control, 5 drought (mannitol; 0727 "mannitol then mannitol" counts as drought), 6 recovery (mannitol then control). All 5 experiments appear
- 0708_m12, 0711_c2, 0721_m10 are fixed slots (spec C)
- Each other slot has a pick and a backup from the same experiment and condition. The backup is used only if the pick fails the tip rule. If both fail: the next pool root of the same experiment and condition in manifest order, at most 3 tries per slot; then the slot is left empty and reported
- Tip rule (dispatcher inbox item 29): ft2 net tip point within 15 px of the root-mask apex, median over 5 frames (frames 0, 20, 40, 60, 79 of the 4-6 h window). Measure: `scripts/remote/tip_apex_probe.py`. 0711_c2 (4.5 px), 0708_m12 (6.4 px), 0721_m10 (9.2 px) and 0714_c10 (4.1 px) were measured on 2026-10-24 and are not probed again
- None of these roots, picks or backups, goes into the B calibration set (sent to the real-calib session on 2026-10-24)
- Held-out roots of the tracing pack are not excluded: they are held out from net fine-tuning only, and this subset trains nothing

## Slots
| Slot | Condition | Experiment | Pick | Backup |
| :-- | :-- | :-- | :-- | :-- |
| C1 | control | 0711 | 0711_c2 (fixed) | - |
| C2 | control | 0708 | 0708_c5 | 0708_c6 |
| C3 | control | 0714 | 0714_c10 | 0714_c11 |
| C4 | control | 0721 | 0721_c1 | 0721_c3 |
| C5 | control | 0711 | 0711_c4 | 0714_c12 |
| D1 | drought | 0708 | 0708_m12 (fixed) | - |
| D2 | drought | 0711 | 0711_m4 | 0711_m6 |
| D3 | drought | 0714 | 0714_m10 | 0714_m13 |
| D4 | drought | 0727 | 0727_mm6 | 0727_mm7 |
| D5 | drought | 0708 | 0708_m8 | 0714_m2 |
| R1 | recovery | 0721 | 0721_m10 (fixed) | - |
| R2 | recovery | 0721 | 0721_m4 | 0721_m5 |
| R3 | recovery | 0721 | 0721_m9 | 0721_m11 |
| R4 | recovery | 0727 | 0727_mc1 | 0727_mc10 |
| R5 | recovery | 0727 | 0727_mc3 | 0727_mc4 |
| R6 | recovery | 0727 | 0727_mc5 | 0727_mc11 |

- D5 has no second clean 0708 mannitol root; its backup is from 0714
- C5: the other clean 0711 control roots are in the B calibration set (0711_c5, 0711_c7) or left out (0711_c1); its backup is from 0714

## Windows
- 3 per root, 2 h each: early 4-6 h, middle 11-13 h, late 17-19 h. Same for every root
- All inside usable hours (every pool root is usable to at least 23.6 h)
- The 0727 movies have one acquisition gap of about 40 min at 19.4-20.1 h (checked on 0727_mc1, 0727_mm6, 0727_cc3). The late window ends before it
- The 4-6 h windows of 0708_m12, 0711_c2 and 0721_m10 already have ft2 midlines (3-root slice); they are reused, not rebuilt

## Compute
- Midlines: ft2 net (`net2_midline_ft2.pt`), `batch_midlines.py --mode tile`, low 0.1 %, high 99.5 %; on the cluster GPU (P100 or V100 by availability), from the private runner environment. Window frames only, one root at a time, into the cluster work folder (at most 30 GB in total). Ledger check before every job; total since 2026-10-23 under $15
- Probe first: 5 frames per candidate, one GPU job for all picks. Full windows only for roots that pass
- Tracking: light single-thread jobs on the lab server (data stays there), or cluster CPU if the lab-server load is above half the cores
- Checks and agents wait for sections A (closure definition) and B (real thresholds) to merge

## Report per window
- Pass or fail per check, diagnostician decision, peak REGR, growth-zone length; auditor's batch report (control against drought against recovery)
- Every result names the midline (ft2) and the closure definition used

## Outcome of the tip rule (2026-10-24, added after the probes; the rule above is unchanged)
- Medians of net tip to mask apex over the 5 frames (px). Pass: 0708_c5 5.0, 0711_c4 3.2, 0714_c10 5.7, 0721_c1 7.8, 0721_m4 11.4, 0721_m9 6.4, 0727_mc1 8.2, 0727_mc5 7.2, 0727_mm6 5.4, 0714_m2 2.2, 0711_m6 5.1, 0714_m13 7.6
- Fail: 0708_m8 695, 0711_m4 693, 0714_m10 797, 0727_mc3 582, 0727_mc4 1139, 0727_mc13 381
- Slots: C1-C5 0711_c2, 0708_c5, 0714_c10, 0721_c1, 0711_c4; D1-D5 0708_m12, 0711_m6 (backup), 0714_m13 (backup), 0727_mm6, 0714_m2 (backup); R1-R4 0721_m10, 0721_m4, 0721_m9, 0727_mc1; R6 0727_mc5
- R5 is empty: pick 0727_mc3, backup 0727_mc4 and third try 0727_mc13 (first unreserved pool root of 0727 recovery in manifest order) all fail. The subset has 15 roots, 45 windows
- On every failing frame the tracking polyline end lies 19-30 px behind the apex, as on passing roots; the net's separate tip point jumps toward the far end of the root. Reported to Andrew; the rule is not changed here

## Tip rule v2 (inbox item 33, 2026-10-24 19:00; set after the first screen, before any check)
- Rule: tracking-polyline end within 50 px of the mask apex, median over the same 5 frames (decisions 2026-10-24)
- Medians (px): 0708_c5 30.4, 0708_m8 23.1, 0711_c4 25.6, 0711_m4 617.8, 0711_m6 44.0, 0714_c10 33.4, 0714_m10 31.8, 0714_m13 40.0, 0714_m2 32.0, 0721_c1 40.4, 0721_m4 38.0, 0721_m9 27.1, 0727_mc1 35.1, 0727_mc3 41.0, 0727_mc4 47.8, 0727_mc5 40.8, 0727_mc13 356.8, 0727_mm6 47.4. Fixed slots (item 29 probe): 0708_m12 27.2, 0711_c2 32.1, 0721_m10 43.0
- Slots refilled in proposal order: D2 0711_m6 (pick 0711_m4 fails), D3 0714_m10, D5 0708_m8, R5 0727_mc3; all other slots unchanged
- Final subset, 16 roots: control 0711_c2, 0708_c5, 0714_c10, 0721_c1, 0711_c4; drought 0708_m12, 0711_m6, 0714_m10, 0727_mm6, 0708_m8; recovery 0721_m10, 0721_m4, 0721_m9, 0727_mc1, 0727_mc3, 0727_mc5
- 0714_m13 and 0714_m2 are tracked but not in the subset
