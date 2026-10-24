# Real slice with the real-movie checker profile and rigid invariance: 0708_m12, 4-6 h

Command: `python scripts/real_slice.py`, then `python scripts/real_slice.py --audit-only --out results/2026-10-24_real_slice` after the auditor-view fix below. Branch wip/dispatcher; Claude Code 2.1.310; model claude-opus-5-5. 2026-10-24.

PROVISIONAL: all numbers use the current fine-tuned midline net (decisions 2026-10-23); they stay provisional until the new net (autotrace) is adopted.

## Real-movie checker profile (Andrew, 2026-10-23, inbox item 18)
- Gates: rigid invariance and closure. Plane sections is computed and reported for every real window but does not gate
- Known limit: per-frame midline curvature noise puts plane sections at about 10x its threshold on real windows, also after smoothing (spline fit option 1 failed its v3 validation; real t3 36 %/h with the fit; `results/2026-10-23_midline_fit_validation/`)
- Synthetic rods and freeze v3 keep all three checks. The checker code and thresholds are unchanged; the profile is applied by the orchestrator side (`agents/executors.py`, `CHECK_PROFILES`)

## Rigidly moved copy of the real window
- `scripts/remote/real_moved.py`: the synthetic rods' rigid motion (0.1 deg per 90 s about the frame-0 tip; (0.5, 0.3) px per 90 s), unlogged, applied to the 80 window frames (bilinear) and to the window midline. End of window: 7.9 deg, (39.5, 23.7) px. 1.9 s on the compute host; about 0.46 GB written

## Chain
| Stage | Result |
| :-- | :-- |
| Dispatcher (agent) | 2 rounds: split, submit, wait 15; collect, finish. 1 window |
| Checker | rigid_invariance 8.83 %/h FAIL (threshold 2.0; largest in centre strain rate at s = 435 px); closure 0.945 px/h pass; plane_sections 133.6 %/h reported, not gating |
| Diagnostician | 5 steps: smooth_midline light raised rigid invariance to 16.76 %/h and was rolled back; decline, fault midline_jitter ("rigid invariance still fails ... no other fault has its own evidence") |
| Auditor | 0 accepted; report: the decline matches the failed invariance check; plane sections computed but not gating on this profile |

## Rigid invariance on the real window: where the difference is
- Window-mean strain-rate profiles, tracked window against its moved copy, 400 px track: centre 0.8-3.4 %/h along the chain interior (s 0-400 px), 8.8 %/h at s >= 400 px (beyond the frame-0 chain length, covered only by later frames); flanks up to 4-6 %/h. No frozen points; chain length equal (398 px)
- So on real texture the tracker's response to this rigid motion plus bilinear resampling is a few %/h, above the 2 %/h threshold set on synthetic rods. Not changed; for Andrew

## Auditor view fix
- First auditor call (in the full run) saw plane sections as passed null ("not run") with a value and called it inconsistent. `audit/view.py` now marks a non-gating check (`gating: false`; "not gating" in the batch table) and extends the column note only when such a check is present: synthetic batch tables are byte-identical (test). The auditor was re-run on the recorded batch (`--audit-only`); this README reports that run

## Files
- `dispatcher_trace.jsonl`, `diagnostician_trace.jsonl`, `auditor_trace.jsonl` (re-run), `summary.json`
