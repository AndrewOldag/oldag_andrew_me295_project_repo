# Agent run over the first batch: counts

Windows collected: 123 of 126; dispatcher end states {'collected': 123, 'gave_up': 3}. Outcome counts only; no check, REGR or growth-zone values.

## By condition group

| | windows | accept | auditor clear | auditor flag | decline |
| :-- | :-- | :-- | :-- | :-- | :-- |
| control | 52 | 45 | 37 | 8 | 7 |
| drought | 47 | 43 | 32 | 11 | 4 |
| recovery | 24 | 22 | 22 | 0 | 2 |

## By experiment

| | windows | accept | auditor clear | auditor flag | decline |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 20260708 | 24 | 20 | 12 | 8 | 4 |
| 20260711 | 23 | 22 | 19 | 3 | 1 |
| 20260714 | 24 | 22 | 18 | 4 | 2 |
| 20260721 | 23 | 19 | 17 | 2 | 4 |
| 20260727 | 29 | 27 | 25 | 2 | 2 |

## By experiment type and condition

| | windows | accept | auditor clear | auditor flag | decline |
| :-- | :-- | :-- | :-- | :-- | :-- |
| drought: control | 36 | 33 | 28 | 5 | 3 |
| drought: mannitol | 35 | 31 | 21 | 10 | 4 |
| recovery: control | 11 | 7 | 5 | 2 | 4 |
| recovery: control then control | 5 | 5 | 4 | 1 | 0 |
| recovery: mannitol then control | 24 | 22 | 22 | 0 | 2 |
| recovery: mannitol then mannitol | 12 | 12 | 11 | 1 | 0 |

## Faults named on declined windows

- bad_stage_correction: 8
- not_computable: 4
- midline_jitter: 1

## Remedies (windows)

| remedy | tried | rolled back |
| :-- | :-- | :-- |
| frames registered on the non-growing tissue | 5 | 4 |
| midline source smoothed | 1 | 0 |

## Closure not computable

4 windows: 0711_c3 0-2 h, 0721_c2 4-6 h, 0727_mc2 0-2 h, 0727_mc2 2-4 h. Outcomes: decline 4; auditor: no decision 4

Re-scored under the 2026-10-26 rule: 0711_c3 0-2 h (2026-10-26 rule: was accept, auditor flag)
Re-scored under the 2026-10-26 rule: 0721_c2 4-6 h (2026-10-26 rule: was accept, auditor flag)
Re-scored under the 2026-10-26 rule: 0727_mc2 0-2 h (2026-10-26 rule: was accept, auditor flag)
Re-scored under the 2026-10-26 rule: 0727_mc2 2-4 h (2026-10-26 rule: was accept, auditor flag)

## Auditor report, agent behaviour only (numbers masked as x)

Auditor status: report; decisions on 114 accepted runs in the run; after the re-score, decisions count on the 110 windows still accepted (tables above). The report below was written before the re-score.

Batch: x runs, x accepted, x declined (all x failed closure). x accepted runs were flagged and x cleared.

Flagged:
- other (x): r56, r70, r94.
- summary_outlier, narrow-spike profile (x): r08, r09, r11, r37, r49, r50, r59, r61, r73, r75, r78, r84, r90, r96, r98, r109, r121.
- summary_outlier, flank difference (x): r35, r58, r79.

What the flagged runs share: x of the x passed closure and were still accepted. Rigid invariance was not run on most of them and does not gate a pass or fail (r61 reads x where it was computed). So closure alone does not catch a collapsed or misplaced growth zone. More mannitol runs were flagged (x of x) than control runs (x of x).

[per-condition summary of cleared runs withheld: REGR and growth-zone medians]

These differences between conditions are measurement results, not faults.
