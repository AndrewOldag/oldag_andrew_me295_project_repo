# Freeze decisions, scoring seeds, diagnostician fixes P1-P5, freeze v2, 2026-10-12

Spec: `docs/specs/2026-10-12_freeze-decisions-diagnostician-fixes.md`. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Scoring tolerance: centre 2.5 % of the rod's true peak, flank difference 1.00 %/h.

## Files
- `item1_labels.md`: seeds 0-2 labels of the five development faults under flank 0.5 and 1.00 %/h, existing runs
- Command: `python scripts/synth/eval_freeze.py --out results/2026-10-12_freeze_v2 --parts relabel`

## 1. Decisions recorded
- `docs/decisions.md`: one line per decision of the spec
- `config/scoring_tolerance.yaml`: flank difference 1.00 %/h
- `strong`: already absent from `REMEDIES` and `describe()`. `measure/remedies.py` accepted any `smooth_midline` setting; it now rejects all but `light`. Test `test_smooth_midline_strong_rejected`
- Labels, seeds 0-2, recomputed from the existing runs (no tracker runs): none change. 15 rods, 36 runs
