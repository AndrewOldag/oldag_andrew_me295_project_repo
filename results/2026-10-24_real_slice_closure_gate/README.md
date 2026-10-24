# Real slice with the resulting real-movie profile (closure gates): 0708_m12, 4-6 h

Command: `python scripts/real_slice.py --out results/2026-10-24_real_slice_closure_gate`. Claude Code 2.1.310, model claude-opus-5-5. 2026-10-24. PROVISIONAL: current fine-tuned midline net; whole-pixel moved copy.

## Real-movie profile (decisions 2026-10-24)
- Gates: closure only
- Reported, not gating: rigid invariance (full range; profile-window value beside it) and plane sections
- Known limits on real windows: plane sections about 10x its threshold from per-frame midline curvature noise; rigid invariance 5.8-7.3 %/h against 2.0, with the excess in well-covered basal chain points (`results/2026-10-24_rigid_cause_test/`). Synthetic rods and freeze v3 keep all three checks as gates

## Chain
| Stage | Result |
| :-- | :-- |
| Dispatcher (agent) | 2 rounds: split, submit, wait; collect, finish. 1 window |
| Checker | closure 0.945 px/h pass (gating); rigid_invariance 7.29 %/h full range, 5.76 %/h on the profile window (s <= 398 px), reported; plane_sections 133.6 %/h, reported |
| Diagnostician | not called: no gating check failed, so the measurement is accepted without an agent call (slice rule) |
| Auditor | accepted run r01 flagged, reason other: rigid invariance 7.29 against 2.0 (about 13 % of the 55.5 %/h centre peak) and plane sections 133.6 against 3.25, both computed but not gating; closure passed. Report notes the flag rests only on non-gating checks |

## Reading
- With closure as the only gate, the diagnostician has nothing to act on and the window is accepted; the auditor flags it from the reported, non-gating values. The non-gating checks still reach the auditor's view
