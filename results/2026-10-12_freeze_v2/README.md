# Freeze decisions, scoring seeds, diagnostician fixes P1-P5, freeze v2, 2026-10-12

Spec: `docs/specs/2026-10-12_freeze-decisions-diagnostician-fixes.md`. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Scoring tolerance: centre 2.5 % of the rod's true peak, flank difference 1.00 %/h.

## Files
- `item1_labels.md`: seeds 0-2 labels of the five development faults under flank 0.5 and 1.00 %/h, existing runs
- `item3_seeds35.md`: seeds 3-5 labels (tracker only), in the table form of `results/2026-10-11_remedy_fixes/item4_faults.md`
- Commands: `python scripts/synth/freeze_sweep.py start|status|fetch --part seeds35`, then the same with `--part seeds35_reg` (register_frames reads its band start from the fetched unremedied record); `python scripts/synth/eval_freeze.py --out results/2026-10-12_freeze_v2 --parts relabel seeds35`

## 1. Decisions recorded
- `docs/decisions.md`: one line per decision of the spec
- `config/scoring_tolerance.yaml`: flank difference 1.00 %/h
- `strong`: already absent from `REMEDIES` and `describe()`. `measure/remedies.py` accepted any `smooth_midline` setting; it now rejects all but `light`. Test `test_smooth_midline_strong_rejected`
- Labels, seeds 0-2, recomputed from the existing runs (no tracker runs): none change. 15 rods, 36 runs

## 3. Seeds 3-5 labelled (tracker only, no agent)
- Five development faults at their frozen sizes, seeds 3-5, through the fitting remedy's states as for seeds 0-2: 2x6 stride 6, 3, 1; width_change unremedied (the width-free ratio needs no re-run); rigid_drift unremedied and `register_frames`; low_texture unremedied, `enlarge_patch` 1.5x and 2x; midline_jitter unremedied and `light` (`strong` withdrawn, not run)
- 66 tracker runs (33 states, each with its moved copy), not the 105-150 estimated: `strong` is not a state and width_change has one run. 0 failed
- Labels: no seed 3-5 label differs from seeds 0-2. Repairable: 2x6, width_change, rigid_drift 0.5 (3 of 3 each). Not repairable: low_texture 0.03, midline_jitter 3 (0 of 3 each)

| Sweep | Runs | Failed | Wall (s) | Load 1 min before / max during / after | Peak workers | Projected after 10 runs (h) |
| :-- | --: | --: | --: | :-- | --: | --: |
| seeds35 | 60 | 0 | 289 | 1.65 / 5.44 / 4.32 | 4 | 0.05 |
| seeds35_reg | 6 | 0 | 27 | 2.61 / 2.93 / 2.70 | 4 | - |

- Work space 6.7 -> 7.28 GB. Sweep wall time so far in this spec: 316 s
