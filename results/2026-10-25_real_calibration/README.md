# Real-movie calibration (spec 2026-10-24b B, task c018): INTERIM

2026-10-24. Interim: 11 windows measured, below the 12-window minimum of the proposal; replacement root 0714_c13 to be added (proposal rule). No threshold is recorded from this table.

Set and rule: `docs/proposals/2026-10-24_real-calibration.md`. Midline ft2 (`net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 %). Tracked length 1000 px (inbox item 3). Closure definition: the 2026-10-10 one, kept by section A. Uncoupled, every frame, initial settings, no remedy, no agent.

Command: `python scripts/real_calib.py run --config private/real_runner_c018.yaml` (lab server, single thread, nice 19, host checks before each run), then `python scripts/real_calib.py summary`. Per-window files in `windows/`; `summary.json`, `table.md`.

## Counts
- 16 windows, 4 experiments: 11 measured; 4 screened out (net tip 15.8, 17.8, 176.6, 878.4 px from the mask apex); 1 screen failed (probe error: segmentation midline shorter than the probe's 40 px step)
- Host log of the first pass (load, free space, run times per tracker run) was overwritten by the second pass; `runner_log.json` holds later runs only (script fixed to append). The host checks ran before every tracker run
- No window flagged 'base may be in growing tissue' (every frame-0 midline longer than 1000 px)

## Interim values (11 windows)
| Check | Min | Median | Max | p95 | p95 rounded up | Two largest | p95 without the largest |
| :-- | --: | --: | --: | --: | --: | :-- | --: |
| Rigid invariance, full range (%/h) | 6.52 | 44.7 | 97.8 | 92.4 | 93 | 0714_c9 w7-9 97.8; 0711_c7 w7-9 86.9 | 78.0 |
| Rigid invariance, profile window (%/h) | 6.52 | 44.7 | 97.8 | 92.4 | 93 | as above | 78.0 |
| Closure (px/h) | 0.698 | 3.70 | 28.9 | 18.4 | 19 | 0711_c7 w7-9 28.9; 0714_c9 w7-9 7.93 | 6.85 |
| Plane sections (%/h, reported only) | 150 | 238 | 383 | 365 | 370 | 0721_c5 w15-17 383; 0711_c7 w15-17 347 | 327 |

- Synthetic thresholds for comparison: rigid invariance 2.0 %/h, closure 1.0 px/h, plane sections 3.25 %/h
- Closure: one window (0711_c7 w7-9, tip-side term 27.0 px/h, largest single-pair residual at pair 1) carries the p95; without it the p95 is 6.85
