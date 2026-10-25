# Real-movie calibration: noise floor and the real closure threshold (spec 2026-10-24b B, task c018)

2026-10-24. Set and rule: `docs/proposals/2026-10-24_real-calibration.md` (first set, and the extension of inbox item 5), each committed before its values were computed. Midline ft2 (`net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 %). Tracked length 1000 px (inbox item 3). Closure definition: the 2026-10-10 one, kept by section A. Uncoupled, every frame, initial settings, no remedy, no agent.

Commands (lab server, single thread, nice 19, host checks before each run): `python scripts/real_calib.py run --config private/real_runner_c018.yaml` (first set; `--replacements 1` for 0714_c13), `python scripts/real_calib.py run --ext --fallback --config private/real_runner_c018.yaml` (extension), then `python scripts/real_calib.py summary`. Per-window files in `windows/` (first set) and `windows_ext/` (extension); `summary.json`, `table.md`. ft2 midlines built by the section C chain on the cluster GPU (4 jobs on its ledger; spend since 2026-10-23 $1.03 of $15 after the last).

## Result
- Real closure threshold: 19 px/h (95th percentile 18.87 over 41 control windows, rounded up to 2 significant figures). Supersedes 18 px/h (12 windows)
- Rigid invariance and plane sections: no real threshold; reported (inbox item 4)

| Check | n | Min | Median | Max | p95 | Real threshold | Two largest | p95 without the largest | Synthetic threshold |
| :-- | --: | --: | --: | --: | --: | --: | :-- | --: | --: |
| Closure (px/h) | 41 | 0.52 | 3.60 | 28.9 | 18.87 | 19 | 0711_c7 w7-9 28.9; 0714_c13 w11-13 27.4 | 17.47 | 1.0 |
| Rigid invariance, full range (%/h, reported) | 41 | 6.35 | 27.5 | 201 | 86.9 | - | 0714_c11 w15-17 201; 0714_c9 w7-9 97.8 | 84.1 | 2.0 |
| Rigid invariance, profile window (%/h, reported) | 41 | 6.35 | 19.6 | 201 | 86.9 | - | as full range | 84.1 | - |
| Plane sections (%/h, reported) | 41 | 150 | 248 | 519 | 390 | - | 0721_c6 w11-13 519; 0711_c1 w7-9 469 | 383 | 3.25 |

## Counts
- 48 windows from 16 control roots, 4 experiments (0708, 0711, 0714, 0721). 41 measured: 12 of the first set, 23 of the planned extension, 6 of the fallback roots 0708_c10 and 0708_c11
- First set (net-tip rule, 15 px): 18 windows, 12 measured, 6 dropped. Superseded threshold 18 px/h (p95 17.35 over 12)
- Extension (polyline-end rule, 50 px; dispatcher inbox item 33): the 6 first-set drop-outs screened again (4 measured), 24 new windows on the pool, 6 fallback windows. The fallback was added by the proposal rule once the planned set could reach at most 38 (after the 11-13 h round)
- Not measured (7): 0714_c4 w7-9 screened out (polyline end 379 px from the apex), w11-13 and w15-17 screen failed (probe error: segmentation midline shorter than the probe's 40 px step); 0714_c9 w11-13 screened out (67.5 px); 0721_c3 w7-9 screened out (50.4 px); 0714_c11 w7-9 and w11-13 failed in the measurement (`ValueError: arange: cannot compute length`, cause not traced)
- No window flagged 'base may be in growing tissue': tracked length reached 1060-1136 px; every frame-0 midline at least 1133 px
- `runner_log.json` lacks the first pass of the first set (overwritten; script fixed to append). The host checks ran before every tracker run

## Reading
- Closure: the two largest windows (28.9, 27.4 px/h) are mostly tip-side motion (0711_c7 w7-9: tip-side term 27.0 px/h). With 41 windows the 95th percentile is the third largest value (18.87), so one window no longer sets it: without the largest it is 17.47 (with 12 windows it was 6.73)
- The threshold is 19 times the synthetic one. On real windows, closure at 19 px/h separates only gross failures; median closure on control windows is 3.6 px/h
- Rigid invariance at 1000 px spans 6.4-201 %/h (median 28); it stays reported, not gating
- Gating on real windows unchanged: closure gates; rigid invariance and plane sections reported

## Per window
See `table.md`. Every measured window records the tracked length reached, base arc length, basal-point world speed and the closure tip-side and base terms.
