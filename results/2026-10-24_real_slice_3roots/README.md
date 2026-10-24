# Real slice, 3 roots, ft2 midline: 0708_m12, 0711_c1, 0721_m10, 4-6 h each

Command: `python scripts/real_slice.py --windows 0708_m12:4-6 0711_c1:4-6 0721_m10:4-6 --config private/real_runner.yaml private/real_runner_lab.yaml --out results/2026-10-24_real_slice_3roots`. 2026-10-24, started 13:29, wall 1459 s. Claude Code 2.1.310, model claude-opus-5-5.

## Setup
- Midline: `net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 % (decisions 2026-10-24). Not provisional (inbox item 22)
- Uncoupled, every frame, track length 400 px. Real-movie profile: closure gates; rigid invariance (whole-pixel copy) and plane sections reported, not gating
- Hosts (inbox items 25, 27): 0708_m12 and 0721_m10 net midline and tracking on the workstation; 0711_c1 net midline (started before item 25) and tracking on the lab server. Agents on the VM. No cluster job

## Net midlines
| Window | Frames | Net time | Tip confidence, median | Tip to segmentation tip, median |
| :-- | --: | --: | --: | --: |
| 0708_m12 4-6 h | 80 | 2939 s (lab server, 3 threads) | 0.572 | 5.5 px |
| 0711_c1 4-6 h | 80 | 3452 s (lab server, 3 threads) | 0.176 | 13.6 px |
| 0721_m10 4-6 h | 73 | 1663 s (workstation, 3 threads) | 0.249 | 11.2 px |

## Results
| Window | Condition | Rigid invariance (%/h, threshold 2.0, reported) | Closure (px/h, threshold 1.0, gates) | Plane sections (%/h, threshold 3.25, reported) | Diagnostician |
| :-- | :-- | --: | --: | --: | :-- |
| 0708_m12 | mannitol | 7.13 | 4.52 FAIL | 214 | bad_stage_correction; registration tried (3.61), rolled back; decline |
| 0711_c1 | control | 63.4 | 64.2 FAIL | 234 | bad_stage_correction; no remedy; decline |
| 0721_m10 | mannitol then control | 7.26 | 4.66 FAIL | 168 | bad_stage_correction; registration tried (9.03), rolled back; decline |

- Dispatcher agent: finish in 2 rounds, 3 windows collected
- Auditor: 0 accepted, 0 flagged, 0 cleared. It reports the condition comparison as context only and states that no condition difference can be reported, since no run passed closure
- Traces: `dispatcher_trace.jsonl`, `diagnostician_trace.jsonl`, `auditor_trace.jsonl`; all numbers in `summary.json`

## Notes
- 0708_m12 4-6 h with `net2_midline_ft.pt` passed closure (0.945 px/h, `results/2026-10-24_real_slice_closure_gate/`). With ft2 it fails (4.52 px/h). Tracker, settings and window are the same; only the midline net differs
- 0711_c1 has the lowest tip confidence (0.176) and closure and rigid invariance about 10x the other two windows
- In every window the diagnostician places the closure residual at the logged stage moves
- Known limit (decisions 2026-10-24): plane sections and rigid invariance do not gate on real movies
