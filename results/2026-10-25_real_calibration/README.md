# Real-movie calibration: noise floor and real-movie thresholds (spec 2026-10-24b B, task c018)

2026-10-24. Set and rule: `docs/proposals/2026-10-24_real-calibration.md`, committed before any value was computed. Midline ft2 (`net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 %). Tracked length 1000 px (inbox item 3). Closure definition: the 2026-10-10 one, kept by section A. Uncoupled, every frame, initial settings, no remedy, no agent.

Commands: `python scripts/real_calib.py run --config private/real_runner_c018.yaml` (lab server, single thread, nice 19, host checks before each run); replacement root: `run --replacements 1 --windows 0714_c13__w7-9 0714_c13__w15-17`; then `python scripts/real_calib.py summary`. Per-window files in `windows/`; `summary.json`, `table.md`. ft2 midlines built by the section C chain on the cluster GPU (2 jobs, on its ledger).

## Counts
- 18 windows from 9 control roots, 4 experiments (16 planned; replacement root 0714_c13 added by the proposal rule after 5 windows dropped out)
- 12 measured; 5 screened out (net tip 15.8, 17.8, 176.6, 878.4, 1188.7 px from the mask apex); 1 screen failed (probe error: segmentation midline shorter than the probe's 40 px step). Minimums met (12 windows, 4 experiments)
- Four of the six drop-outs are far from the 15 px line (177-1189 px or a probe error): the net tip or the segmentation is on another object there, not a near miss
- No window flagged 'base may be in growing tissue': every frame-0 midline is longer than 1000 px
- `runner_log.json` holds the replacement root's runs only; the first pass's host log was overwritten by the second (script fixed to append). The host checks ran before every tracker run

## Thresholds (95th percentile, numpy linear, rounded up to 2 significant figures)
| Check | n | Min | Median | Max | p95 | Real threshold | Two largest | p95 without the largest | Synthetic threshold |
| :-- | --: | --: | --: | --: | --: | --: | :-- | --: | --: |
| Rigid invariance, full range (%/h) | 12 | 6.52 | 35.8 | 97.8 | 91.8 | 92 | 0714_c9 w7-9 97.8; 0711_c7 w7-9 86.9 | 77.0 | 2.0 |
| Closure (px/h) | 12 | 0.698 | 3.50 | 28.9 | 17.3 | 18 | 0711_c7 w7-9 28.9; 0714_c9 w7-9 7.93 | 6.73 | 1.0 |
| Rigid invariance, profile window (%/h, information) | 12 | 6.52 | 32.6 | 97.8 | 91.8 | (92) | as full range | 77.0 | - |
| Plane sections (%/h, reported, no threshold) | 12 | 150 | 238 | 383 | 363 | - | 0721_c5 w15-17 383; 0711_c7 w15-17 347 | 338 | 3.25 |

## Per window
See `table.md`. Every measured window also records the tracked length reached (1060-1092 px), base arc length, basal-point world speed and the closure tip-side and base terms.

## Reading
- The closure threshold is set by one window: 0711_c7 w7-9 (28.9 px/h; tip-side term 27.0 px/h, largest single-pair residual at pair 1). Without it the p95 is 6.73. The rule keeps it (no window dropped after its value is seen)
- Rigid invariance at 1000 px spans 6.5-98 %/h on control windows (median 36). In most windows the profile-window value equals the full-range value, so the difference lies where both copies are covered in every frame. A real threshold of 92 %/h passes nearly every window; it is not a sensitive check on real movies at this setting
- Whether a check gates on real windows is not changed here (real-movie profile today: closure gates; rigid invariance and plane sections reported)
