# Real-movie closure definition (spec 2026-10-24b A, task c017)

2026-10-24. Midline ft2 (`net2_midline_ft2.pt`). Windows 0708_m12, 0711_c2, 0721_m10, 4-6 h, uncoupled, every frame. Measurement fix only: checker code and thresholds unchanged.

## Result
- Closure definition kept: (1), the midline end as the tip, against the most basal centre point tracked in every frame (decisions 2026-10-10)
- Change: real windows are tracked to 1000 px (was 400; `measure/real_runner.py`, `TRACK_LENGTH`). The closure base then lies in mature tissue
- Reason, in kinematic terms: closure takes the chain base as fixed in the world. On these roots the world speed along the chain falls to about 0 only at s = 550-650 px. A 400 px chain (base at s = 458-489 px at the window end) ends inside the growth zone, and its base moves with growth: 5.4, 38.8 and 11.1 px over 2 h. That motion is most of the residual
- The hypothesis of the spec (chain ends about 35 px behind the apex) does not hold here. The chain's first point starts at the midline end (gap 0.0 px at frame 0 on all 3). The point 23-36 px ahead of the midline end is the net's own tip point, which the checker does not use
- Closure with the definition kept, 1000 px: 2.36, 3.17, 2.19 px/h (was 4.52, 20.43, 4.66). Still above the 1.0 px/h synthetic threshold. Real thresholds come from B's calibration rule, computed with this setting

## Tests (1)-(4), closure in px/h (`definitions.json`)
| Window | Tracked length | (1) midline end | (2) net tip point | (3) chain c_0 | (4) (1) with apical segment growth | Tip-side term | Base term | Base s (px) |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| 0708_m12 | 400 | 4.52 | 3.58 | 2.73 | 4.50 | 1.87 | 2.73 | 489 |
| 0711_c2 | 400 | 20.43 | 19.58 | 19.60 | 20.33 | 0.83 | 19.60 | 465 |
| 0721_m10 | 400 | 4.66 | 3.96 | 5.64 | 4.61 | 1.28 | 5.64 | 458 |
| 0708_m12 | 1000 | 2.36 | 1.49 | 0.67 | 2.32 | 1.87 | 0.67 | 1092 |
| 0711_c2 | 1000 | 3.17 | 2.98 | 2.51 | 3.09 | 0.67 | 2.51 | 1087 |
| 0721_m10 | 1000 | 2.19 | 2.58 | 0.86 | 2.22 | 1.34 | 0.86 | 1065 |

- Tip-side term: \|d(midline end) - d(c_0)\| / duration. Base term: \|d(c_b)\| / duration, world frame. Closure is the length of their vector sum
- 400 px rows: the cached whole-pixel reference tracks of the 3-root run. 1000 px rows: the movie window as is (lab server, this task). At 400 px the window as is gives the same closure as the reference copy (0708_m12 4.521 both)
- (2) net tip point: confidence median 0.57, 0.39, 0.25. It is not defined on synthetic rods
- (3) is the base term alone: it asks only whether a material point is fixed in the world. Lowest with a mature base (0.67, 2.51, 0.86). On the 51 scored v3 rods it changes 49 closure values by more than 1e-3 and 10 pass or fail outcomes (`v3_validation.json`), so it fails the validation. Not adopted
- (4) predicted apical segment growth over 2 h: 0.04-0.21 px. The fitted speed near the tip is flat, so (4) is close to (1)
- Midline end minus c_0 has a steady trend in time of 1.0-3.3 px/h (net tip minus c_0: 0.6-2.8 px/h), not end-frame noise. The tip reference is not a material point. That term stays in (1)

## Chain base (`base_test.json`)
Tracked length 400, 700, 1000 px, the same window as is. Closure, px/h:

| Window | 400 | 700 | 1000 | World speed of mature points, 1000 px run (px/h, every 4th chain point) |
| :-- | --: | --: | --: | :-- |
| 0708_m12 | 4.52 | 0.61 | 2.36 | -0.4 to 3.0 past s = 580 |
| 0711_c2 | 20.43 | 2.27 | 3.17 | 0.3 to 6.8 past s = 630, 0.3-2.0 past s = 810 |
| 0721_m10 | 4.66 | 1.62 | 2.19 | -1.2 to 0.7 past s = 610 |

- 1000 px chosen over 700: at 700 px the 0711_c2 base (s = 787 px) is at the end of its growth zone (2-6 px/h). Control and recovery roots may have longer zones. Tracking time 28-33 s per window against 12-13 s at 400 px
- Mature-tissue points scatter by about 1-3 px/h between neighbours. With one basal point that scatter enters closure directly

## Stage checks (`definitions.json`)
- Pixel scale: every stage step is a whole multiple of 2.105 um (2.11, 4.21, 6.32 um = 1, 2, 3 px). The stage moves on every frame
- Sign and alignment: jitter of the chain's per-pair world motion is smallest with sign + and lag 0 on 0708_m12 (0.23 px against 0.28-0.34) and 0721_m10 (0.20 against 0.56-0.94). 0711_c2 has equal steps on every frame, so the test does not separate there (0.20 for all)
- The ratio of base speed to stage speed differs between roots at 400 px (0.03, 0.24, 0.09), so a scale error does not explain the base motion

## Validation on freeze v3 (`v3_validation.json`)
- `python scripts/closure_v3_validate.py --tracks staging/tracks_freeze_v3 --out results/2026-10-25_closure_definition/v3_validation.json`: 51 rods, 153 check values recomputed from the cached v3 tracks against the scored summaries. Largest change 0.0, pass or fail changed 0. The same file has definition (3) on the same rods
- The checker and the synthetic runners are unchanged, so v3 scored outcomes are unchanged. No LLM run repeated
- `python -m pytest -q tests`: 303 passed, 1 skipped

## Not tested here
- Rigid invariance and plane sections at 1000 px (no moved copy tracked)
- Roots whose frame-0 midline is shorter than 1000 px: the tracker cuts the chain at the midline end, so the base can be in growing tissue

## Commands
- Net tip points (read-only, on the host with the net outputs): `python scripts/remote/net_tip_points.py NAME HTPMID.npz NETMID.npz ...` -> `net_tips.json`
- Tests (1)-(4) and stage checks: `python scripts/closure_definitions.py --tips results/2026-10-25_closure_definition/net_tips.json --track ROOT TRACK.npz ...` -> `definitions.json`
- Chain base: `python scripts/closure_base_test.py --config private/closure_runner_lab.yaml --lengths 400 700 1000 --windows 0708_m12:4-6 0711_c2:4-6 0721_m10:4-6 --out base_test.json` (one job at a time, single thread, nice 19; load 0.6-2.5 of 32 cores before each run)
