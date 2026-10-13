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

## 4. P1-P5 applied (commit 5b896cb)
- Prompt lines as written in the proposal; info fields in `stage_log_summary`, `velocity_profile`, `frame_quality`; `settings_left` note in the remedy result
- Tests: `tests/test_info_p1_p5.py`, 5 tests (one per new field on a clean rod and its fault; note after `smooth_midline light`; each prompt line). Fixtures: seed 0 tracker outputs of rigid_drift 0.5, width_change, low_texture 0.03, and clean growth_zone s1 (basis run, has frame quality). Full suite: 137 passed

## 5. Freeze v2
- `docs/proposals/2026-10-12_freeze-v2.md`. Open: the real-movie `frame_quality` reference only

## 6. Development check, seed 0 (not a score)
- After the freeze v2 commit (a3a0dbf): one diagnostician run per development fault, seed 0, new prompt and info fields. 5 runs. Seed 0 is the development seed P1-P5 were written from; these runs are not scored and nothing was changed from them
- Command per run: `python scripts/demo_slice.py --fault <fault> [--size <size>] --seed 0 --out results/2026-10-12_freeze_v2/devcheck`. Trace and summary per run in `devcheck/`
- Tracker runs as single jobs through `RemoteRunner` (load-checked, lowest priority; cached runs reused)

| Fault | Size | Label | Outcome | Category | Named fault | Correct | Steps | First step naming the true fault | Remedies | Roll backs | Tokens in / out | Call time (s) | Claude Code |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: | :-- | --: | :-- |
| displacement_exceeds_patch | 2x6 | repairable | accept | good_report | displacement_exceeds_patch | yes | 7 | 2 (apply_remedy change_frame_stride) | frame stride 6 -> 3; frame stride 3 -> 1 | 0 | 31478 / 3592 | 41.6 | 2.1.293 |
| width_change | 1/400 | repairable | accept | good_report | width_change | yes | 6 | 5 (apply_remedy use_width_free_ratio) | report the centre strain rate and the width-free ratio; plane-sections check skipped | 0 | 27350 / 2380 | 27.6 | 2.1.293 |
| rigid_drift | 0.5 | repairable | accept | good_report | rigid_drift | yes | 5 | 4 (apply_remedy register_frames) | frames registered on the non-growing tissue (from 305 px from the tip) before tracking | 0 | 21852 / 2109 | 25.6 | 2.1.293 |
| low_texture | 0.03 | not repairable | decline | correct_decline | low_texture | yes | 3 | 3 (decline) | none | 0 | 11427 / 1195 | 14.9 | 2.1.293 |
| midline_jitter | 3 | not repairable | decline | correct_decline | midline_jitter | yes | 7 | 6 (apply_remedy smooth_midline) | frames registered on the non-growing tissue (from 305 px from the tip) before tracking; rolled back: frames registered on the non-growing tissue (from 305 px from the tip) before tracking; midline source smoothed (light) | 1 | 32071 / 3485 | 38.3 | 2.1.293 |

- Development check: 5 of 5 correct outcomes; terminal fault correct 5 of 5. Build session 10 (old prompt): 1 of 5 and 0 of 5. Totals: 28 steps, 124k input and 13k output tokens, 148 s call time
- Good: within the approved tolerance (centre 2.5 % of the true peak, flank 1.00 %/h). After the remedies: 2x6 REGR error 34.67 -> 0.95 %/h (limit 2.17), three passes; width_change 0.40 %/h, plane sections skipped; rigid_drift 0.42 %/h, three passes
- First step naming the true fault (session 10 in brackets): 2x6 step 2 (2); width_change step 5 (never); rigid_drift step 4 (never); low_texture step 3, the decline (never); midline_jitter step 6 (3)
- midline_jitter: `register_frames` (named rigid_drift) at step 2 was rolled back; `smooth_midline light` at step 6; decline at step 7: "the remedy cannot be applied again"
