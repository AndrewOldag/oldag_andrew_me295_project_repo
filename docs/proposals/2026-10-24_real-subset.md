# Proposal: 16-root real subset (task c019)

Dispatcher session, 2026-10-24. Spec `docs/specs/2026-10-24b_real-movie-push.md`, section C; dispatcher inbox item 31. Fixed before any run of this subset. Nothing here is a result.

## Rule
- Pool: `include` yes, montage imgdir, `stage_tracking_log` yes, empty `notes` and `flags`, usable window covering 4-19 h. 0711_c1 is left out (replaced in the 3-root slice; its run stays a reported failure)
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
| C5 | control | 0711 | 0711_c4 | 0711_c7 |
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
