# Real slice, 3 roots, ft2 midline, control 0711_c2: 0708_m12, 0711_c2, 0721_m10, 4-6 h each

Command: `python scripts/real_slice.py --windows 0708_m12:4-6 0711_c2:4-6 0721_m10:4-6 --config private/real_runner.yaml private/real_runner_lab.yaml --out results/2026-10-24_real_slice_3roots_c2`. 2026-10-24, started 15:25, wall 597 s. Claude Code 2.1.310, model claude-opus-5-5.

## Setup
- Midline: `net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 %. Uncoupled, every frame, track length 400 px
- Real-movie profile: closure gates; rigid invariance (whole-pixel copy) and plane sections reported, not gating
- Control root 0711_c2 replaces 0711_c1 (inbox items 28-30). Rule: ft2 net tip point within 15 px of the root-mask apex, median over 5 window frames: 4.5 px. Its ft2 net midline: workstation, from the 80 window frames only, 1829 s, tip confidence median 0.385. The 0711_c1 run stays as a reported failure in `results/2026-10-24_real_slice_3roots/`
- Hosts: 0708_m12 and 0721_m10 tracked on the workstation (cached from the first 3-root run, same settings); 0711_c2 tracked on the lab server (single thread, nice 19). Agents on the VM. No cluster job

## Results
| Window | Condition | Rigid invariance (%/h, threshold 2.0, reported) | Closure (px/h, threshold 1.0, gates) | Plane sections (%/h, threshold 3.25, reported) | Diagnostician |
| :-- | :-- | --: | --: | --: | :-- |
| 0708_m12 | mannitol | 7.13 | 4.52 FAIL | 214 | bad_stage_correction; registration (3.61) and light midline smoothing tried, both rolled back; decline |
| 0711_c2 | control | 3.51 | 20.4 FAIL | 210 | bad_stage_correction; registration tried (16.06), rolled back; decline |
| 0721_m10 | mannitol then control | 7.26 | 4.66 FAIL | 168 | bad_stage_correction; registration tried (9.03), rolled back; decline |

- Dispatcher agent: finish in 2 rounds, 3 windows collected
- Auditor: 0 accepted, 0 flagged, 0 cleared. Condition profiles given as context only; it states that no conclusion about the conditions can be drawn (one root per condition, every run failed closure)
- The agents declining every real window is the reported result (decisions 2026-10-24)
- Traces: `dispatcher_trace.jsonl`, `diagnostician_trace.jsonl`, `auditor_trace.jsonl`; all numbers in `summary.json`

## Known limits (decisions 2026-10-24)
- Closure on real windows: with tip noise removed, closure is 3.0-5.2 px/h against the 1.0 px/h synthetic threshold (0708_m12, `results/2026-10-24_closure_ft_vs_ft2/`); the tip moves 2-9 px more than the tracked chain over 2 h, consistent with the tip-versus-tissue drift seen on the 18 Oct gravistimulation run. No threshold change, no tip stabilization; closure stays the gate. Root cause (chain base, stage correction, fixed-root calibration) is a research-lane open item after 28 Oct
- Plane sections and rigid invariance do not gate on real movies: per-frame midline curvature noise is about 10x the plane-sections threshold; rigid invariance excess lies in well-covered points (cause test, `results/2026-10-24_rigid_cause_test/`)
