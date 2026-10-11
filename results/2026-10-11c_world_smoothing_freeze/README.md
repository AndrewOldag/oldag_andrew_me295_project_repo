# World-coordinate smoothing, flank tolerance, diagnostician runs, freeze list, 2026-10-11

Specs: `docs/specs/2026-10-11c_world-coordinate-smoothing-uncoupled.md`, with items 2 and 3 of `2026-10-11b_padding-flank-tolerance-coupling-weight.md`. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h.

Status: item 1 done; item 2 run, flank tolerance stopped (rule gives 1.00, not 0.75); diagnostician runs made (5); items 3 and 4 done. Freeze list in `docs/proposals/2026-10-11_freeze-v1.md`.

## Files
- `c1_smoothing.md`: clean rods and `midline_jitter` with world-coordinate smoothing
- `c2_flank_tolerance.md`: basis rule with the bent rods, per setting, and the clean-rod table
- `diagnostician/`: trace and summary per run
- Commands: `python scripts/synth/fix_sweep.py start|status|fetch --part c_smooth|c_bent`, then `python scripts/synth/eval_fix.py --out results/2026-10-11c_world_smoothing_freeze --parts c_smooth c_tolerance`

## Sweeps (shared-machine limits as before)
| Sweep | Runs | Failed | Wall (s) | Load 1 min before / max during / after | Peak workers | Projected after 10 runs (h) |
| :-- | --: | --: | --: | :-- | --: | --: |
| c_smooth (item 1) | 72 | 0 | 153 | 2.12 / 5.87 / 5.72 | 4 | 0.05 |
| c_bent (item 2) | 84 | 0 | 252 | 3.72 / 6.32 / 6.12 | 4 | 0.07 |

- Diagnostician runs: tracker runs as single jobs through `RemoteRunner` (load-checked, lowest priority; cached runs reused). 156 sweep runs, 6.8 min sweep wall time; work space 5.62 -> 5.67 GB

## 1. smooth_midline in world coordinates
- Stage log added before the time smoothing and subtracted after. Padding, sigmas and levels unchanged. Tag `mslight4`, `msstrong4`
- Tests: the two existing ones pass; steady world motion with stage steps every 7 frames is unchanged to < 0.01 px at both levels
- Clean growth_zone and bending, 3 seeds: 12 of 12 pass after light and after strong (strong closure 0.07-0.10 px/h; was 1.55-1.60)
- `midline_jitter`: 0.5 px meets the criteria on 3 of 3 seeds (seeds 0 and 1 by `strong`, seed 2 by `light`); 1, 2 and 3 px meet them on none

## 2. Flank tolerance (stopped) and the withdrawal of `strong`
- Bent rods run through the 7 remedy settings (84 runs). After `strong`, all 6 bent clean rods fail plane_sections (3.43-4.69 %/h); after `light` they pass
- By the rule of 11c item 1 (a clean rod fails after `strong`): `strong` withdrawn from the remedy list, `light` stays. With `light` alone, `midline_jitter` 0.5 px meets the criteria on 1 of 3 seeds, so no size qualifies: `midline_jitter` is not repairable at 3 px, decline is its correct outcome
- Basis rule (settings that keep all 12 clean runs passing: none, register_frames, smooth light, enlarge 1.5x and 2x, crop, mask): largest flank-difference error 0.797 %/h (bend_reverse seed 0, enlarge_patch 2x). Rounded up: 1.00 %/h, not 0.75. Stop: not put in the config; labels not recomputed
- Without `enlarge_patch` 2x the largest is 0.66 %/h (register_frames), which gives 0.75
- Largest clean centre error: 2.45 % of the true peak (bend_continue seed 2, enlarge_patch 2x); limit 2.5 %
- `low_texture` repairable size: not re-examined, as the tolerance is not set

## Diagnostician runs (seed 0, uncoupled; good = approved tolerance, flank 0.5 %/h)
| Fault | Size | Label | Outcome | Category | Named fault | Correct | Steps | Remedies | Roll backs | Tokens in / out | Call time (s) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | --: | :-- | --: | :-- | --: |
| displacement_exceeds_patch | 2x6 | repairable | step_limit | not_reported | - | no | 8 | frame stride 6 -> 3; frames registered (from 305 px) | 0 | 35349 / 3989 | 46.0 |
| width_change | 1/400 | repairable | decline | unnecessary_decline | unknown | no | 7 | none | 0 | 29301 / 3098 | 36.9 |
| rigid_drift | 0.5 | repairable | decline | unnecessary_decline | unknown | no | 7 | none | 0 | 29778 / 3444 | 39.2 |
| low_texture | 0.03 | not repairable | decline | correct_decline | midline_jitter | no | 7 | frames registered (from 425 px); midline smoothed (light) | 0 | 29110 / 3580 | 39.6 |
| midline_jitter | 3 | not repairable | step_limit | not_reported | - | no | 8 | midline smoothed (light); frame stride 1 -> 2 | 0 | 35910 / 4000 | 45.5 |

- 1 of 5 correct outcomes; 0 of 5 faults named correctly. Totals: 37 steps, 159k input and 18k output tokens, 207 s call time
- width_change: the agent named no fault and declined with plane sections failing alone; the prompt line on width change was not used
- rigid_drift: the agent read closure failing alone with a clean stage log and declined; it did not try `register_frames`
- Two scripting faults were found after the runs and fixed; no agent call was repeated:
  - `demo_slice.py` crashed after the outcome with a relative `--out` path, so no summaries were written. `--replay` added: it re-applies the remedies in a trace (tracker outputs from the cache) and writes the summary
  - `truth_error` crashed when no grid point was covered (low_texture final run); it now returns no error and zero coverage, which scores as not good
- Roll-back fault found in the low_texture run: registration made the failing checks worse, and plane sections became uncomputable; the rule counted the uncomputable check as resolved, so nothing was rolled back. Fixed: only a check skipped on purpose (width-free) counts as resolved. The summary keeps the run as it happened. The run needs one re-run (Andrew: the 5-run limit is used)

## 3. Uncoupled system
- `couple` false everywhere; `--couple-lambda` and `--couple-mu` stay in `qb_track.py` with no caller. README line added

## 4. Freeze list
- `docs/proposals/2026-10-11_freeze-v1.md`: faults, sizes and labels; remedies; info kinds; prompt commit; thresholds; tolerance; run settings; four open items

## Questions for Andrew
1. Flank tolerance: 1.00 %/h by the rule, or 0.75 with `enlarge_patch` 2x left out of the basis, or other?
2. Confirm the withdrawal of `strong`: it makes `midline_jitter` not repairable (0.5 px met the criteria only with `strong`)
3. Re-run the low_texture diagnostician run after the roll-back fix (one run over the limit of 5)?
