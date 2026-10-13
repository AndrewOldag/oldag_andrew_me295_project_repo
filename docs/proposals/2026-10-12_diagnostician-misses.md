# Diagnostician misses in build session 10: causes and proposed fixes

From: build account. Date: 2026-10-12. Branch `wip/diag-review`. No code changed. No diagnostician calls (0 of 0 allowed); read from the recorded traces only.

Inputs: `results/2026-10-11c_world_smoothing_freeze/diagnostician/` (5 traces, all seed 0), `agents/prompts/diagnostician.md`, `agents/actions.py`, `measure/info.py`, `checker/checks.py`, `agents/executors.py`, `docs/proposals/2026-10-11_freeze-v1.md`.

## Summary
| Run | True fault, correct outcome | Outcome | Fault named | True fault named at any step | Cause |
| :-- | :-- | :-- | :-- | :-- | :-- |
| displacement_exceeds_patch 2x6 | accept after stride 6 -> 3 -> 1 | step limit (8) | none (last remedy: rigid_drift) | yes, step 2 | b |
| width_change | accept with `use_width_free_ratio` | decline | unknown | no | a |
| rigid_drift 0.5 | accept after `register_frames` | decline | unknown | no | b |
| low_texture | decline | decline (correct outcome) | midline_jitter | no | a |
| midline_jitter 3 px | decline | step limit (8) | none (last remedy: midline_jitter) | yes, steps 3 and 8 | b |

- Terminal fault correct: 0 of 5. Correct outcome: 1 of 5 (low_texture). True fault named in a remedy at some step: 2 of 5
- Cause a (missing measurement): 2. Cause b (prompt led away): 3. Cause c (step limit): 0. Cause d (doubtful label): 0 as main cause; 1 flag below
- The two step-limit runs needed 3-5 steps on the correct path. The limit of 8 was not the cause
- One mistaken belief drives 3 of 5 misses: the agent reads "rigid-body invariance" as a test for whole-frame drift. In `checker/checks.py` the check adds a known rigid motion and compares strain rates. It tests the tracker, not the movie. Unlogged drift passes it and fails closure
  - rigid_drift, step 1: "rigid invariance ... passed", so the agent looked for a stage fault, not drift
  - width_change, step 1: "rigid invariance and closure passed, so this is not drift"
  - displacement_exceeds_patch, step 7: a large rigid-invariance value taken as rigid motion; `register_frames` applied under fault rigid_drift
- The prompt gives no fault signatures. `describe()` lists fault names only; the one-line meanings are code comments in `agents/actions.py` and do not reach the agent

## 1. Per run

### displacement_exceeds_patch 2x6, seed 0
- True fault: tip step above the patch radius. Label: repairable, stride 6 -> 3 -> 1, then accept
- Asked for: displacement_vs_patch_radius, [remedy stride half], check_report, frame_quality, stage_log_summary, midline_jitter, [remedy register_frames], velocity_profile. Step limit at 8
- Step 1 displacement_vs_patch_radius: tip 18.0 px per pair, radius 15, ratio 1.2, stride 6. Points to the true fault
- Step 2 stride 6 -> 3, named displacement_exceeds_patch: closure 132.2 -> 6.24 px/h; rigid invariance 222 -> 185 %/h; plane sections 145 -> 205 %/h. The agent expected 9 px per pair to be "well inside the patch" (ratio 0.6)
- Step 3 check_report: same values, closure worst at pair 1
- Step 4 frame_quality: contrast 0.205-0.219, focus 0.099-0.103, 1 bright object. Clean
- Step 5 stage_log_summary: residual 0.48 at moves, 0.49 elsewhere. No stage fault
- Step 6 midline_jitter: offset 1.96 px, change 0.55 px, tip second difference 0.00. Small
- Step 7 register_frames, named rigid_drift: rigid invariance 185 -> 127, closure 6.24 -> 5.81, plane sections 205 -> 207. Not rolled back (127/185 = 0.69, under 3/4)
- Step 8 velocity_profile: peak 84.1 %/h against truth 86.9; profile has a dip to 1.8 %/h at 250 um and a negative minimum -12.5
- Fault named: displacement_exceeds_patch at step 2; rigid_drift at step 7; no terminal action
- First divergence: step 3. Stride half had lowered a failing check by 95 % and stride 3 can be halved again. The agent asked for check_report and then looked for a "second fault"
- Cause b. The prompt says a remedy that lowered a failing check "may be applied again". That reads as permission, not as the next step. The remedy result does not show the new tip step, and no line says what ratio the tracker handles
- Steps needed on the labelled path: 4 (displacement_vs_patch_radius, stride half, stride half, accept); 5 with a second displacement_vs_patch_radius

### width_change, seed 0
- True fault: flank spacing grows 40 %/h (physical), curvature 1/400 px. Label: repairable by `use_width_free_ratio`, then accept. Measurement already within tolerance before any remedy (centre REGR RMS 0.40 %/h, flank-difference RMS 0.32 %/h)
- Asked for: midline_jitter, frame_quality, displacement_vs_patch_radius, check_report, velocity_profile, stage_log_summary, then decline
- Step 1 midline_jitter: offset 0.02 px, change 0.01 px. Clean
- Step 2 frame_quality: contrast 0.217 -> 0.192 -> 0.170 over frames 0, 20, 40; focus 0.103 -> 0.096. A fall, not named by any rule
- Step 3 displacement_vs_patch_radius: ratio 0.10, no points lost
- Step 4 check_report: plane sections 4.30 %/h at s = 116 um, flank difference -4.30, predicted -0.00; others pass
- Step 5 velocity_profile: peak 42.4 %/h at 316 um (truth 43.4); basal velocity 126.1 = tip 126.2 um/h
- Step 6 stage_log_summary: residual 0.03 / 0.02 px
- Fault named: unknown (decline)
- First divergence: none. No info kind reports width or flank spacing, so no answer showed the true fault
- The prompt rule "A width change under osmotic treatment is a physical cause" cannot fire: the task (`agents/executors.py`, `task()`) carries no condition or treatment field, and nothing measures width
- Cause a
- Steps needed with a width measurement: 3 (info with spacing rate, use_width_free_ratio, accept)

### rigid_drift 0.5, seed 0
- True fault: unlogged drift 0.2, 0.1 px/frame and 0.01 deg/frame. Label: repairable by `register_frames`, 3 of 3 seeds, then accept
- Asked for: stage_log_summary, displacement_vs_patch_radius, frame_quality, velocity_profile, check_report, midline_jitter, then decline
- Task: closure fails 8.13 px/h; rigid invariance 0.60 and plane sections 1.43 pass
- Step 1 stage_log_summary: closure residual 0.2 px per pair at moves and 0.2 elsewhere; 5 moves in 40 pairs. The clean-like width_change run gives 0.02-0.03. 0.2 px x 40 pairs = 8 px in 1 h, the closure value. Drift 0.2, 0.1 px/frame is 0.22 px per pair. This is the signature of steady unlogged motion
- Step 2 displacement_vs_patch_radius: ratio 0.11, no points lost
- Step 3 frame_quality: contrast 0.21, focus 0.10, 1 object. Clean
- Step 4 velocity_profile: basal velocity 126.1 um/h, tip net displacement 143.4 um/h. The base moves in the world frame by the difference, 17.3 um/h (8.2 px/h)
- Step 5 check_report: closure 8.13 px/h, base at s = 430 px, worst pair 38
- Step 6 midline_jitter: 0.02 / 0.01 / 0.00. Clean
- Fault named: unknown (decline). The agent stated the 8.2 px/h gap at step 5 and named no fault for it
- First divergence: step 2. The agent read "0.2 px at moves and 0.2 elsewhere" as clean, because it compared the two numbers with each other and not with zero
- Cause b. The evidence was in steps 1 and 4. The prompt names the check "rigid-body invariance" without saying what it tests, so the agent ruled out drift at step 1. No line says that steady unlogged motion fails closure with a residual spread over all pairs

### low_texture, seed 0
- True fault: contrast 0.03, blur 2 px, noise 40. Label: not repairable, decline
- Run made before the roll-back fix (freeze open item 4): registration was not rolled back although both computable checks got worse
- Asked for: displacement_vs_patch_radius, stage_log_summary, [remedy register_frames], frame_quality, midline_jitter, [remedy smooth_midline light], then decline
- Task: all three checks fail; rigid invariance 255 %/h
- Step 1 displacement_vs_patch_radius: ratio 0.10, no points lost. Rules out overrun; a tracker failure without overrun
- Step 2 stage_log_summary: residual 0.34 at moves, 0.76 elsewhere; velocity jump 8.75
- Step 3 register_frames, named rigid_drift: rigid invariance 255 -> 320, closure 5.5 -> 104.8, plane sections no longer computable
- Step 4 frame_quality: contrast 0.059, focus 0.035, 1 object, steady over frames. In the other four runs: contrast 0.17-0.22, focus 0.096-0.103. The agent wrote "no clear threshold to judge them against"
- Step 5 midline_jitter: offset 23.2 px, change 6.17 px, tip second difference 15.5 px. Low texture also degrades the midline source and the tracked points, so this is a symptom
- Step 6 smooth_midline light, named midline_jitter: rigid invariance 320 -> 467, closure 104.8 -> 30.1
- Fault named: midline_jitter (decline). Outcome correct, name wrong
- First divergence: step 5. Frame quality was low by a factor of 3-4 against every other run, but the agent had no scale inside the run
- Cause a. `frame_quality` returns raw numbers with no reference. Secondary b: no line says low texture also makes the midline jitter
- Steps needed with a reference in frame_quality: 2-3 (frame_quality, decline; or check_report first)

### midline_jitter 3 px, seed 0
- True fault: midline source jitter, 3 px sideways. Label: not repairable (`light` only, `strong` withdrawn), decline
- Asked for: check_report, midline_jitter, [remedy smooth_midline light], displacement_vs_patch_radius, stage_log_summary, frame_quality, velocity_profile, [remedy stride double]. Step limit at 8
- Step 1 check_report: closure 2.24 px/h, plane sections 35.3 %/h (flank difference -0.98, predicted -36.3)
- Step 2 midline_jitter: offset 4.19 px, change 4.11 px, tip second difference 22.65 px. Points to the true fault
- Step 3 smooth_midline light, named midline_jitter: plane sections 35.3 -> 26.1 (8x threshold), closure 2.24 -> 3.54, rigid invariance passes
- Steps 4-7: displacement ratio 0.24; stage residual 3.02 / 3.36; frame quality clean; tip path 321 against net 126.5 um/h
- Step 8 stride double, named midline_jitter: closure 3.54 -> 1.25, plane sections 26.1 -> 25.8
- Fault named: midline_jitter at steps 3 and 8; no terminal action
- First divergence: step 4. `light` is the only setting and cannot be applied twice (`measure/remedies.py` raises "already smoothed"). Plane sections stayed at 8x threshold. Decline with midline_jitter was the next action
- Cause b. The prompt says decline when "a remedy has failed" and also that a remedy that lowered a failing check "may be applied again or at its next setting". 35.3 -> 26.1 is a lowering (just under 3/4), so the agent did not treat the remedy as failed, though no repeat or next setting exists
- Steps needed on the labelled path: 3-4 (midline_jitter, smooth light, decline; check_report optional)

## 2. Causes
| Cause | Runs |
| :-- | :-- |
| a. info kinds cannot tell this fault apart | width_change (no width measurement); low_texture (frame_quality has no reference) |
| b. evidence there, prompt led away | rigid_drift (check meaning); displacement_exceeds_patch (repeat rule is permissive); midline_jitter (no rule for a lowered check with no further setting) |
| c. step or turn limit | none. The two step-limit runs needed 4-5 and 3-4 steps |
| d. label doubtful | none as main cause; flag on midline_jitter below |

Flag (d), not a cause of this miss: midline_jitter 3 px, seed 0, before any remedy: centre REGR RMS 0.797 %/h (1.8 % of peak, inside 2.5 %) and flank-difference RMS 0.757 %/h (outside 0.5, inside the pending 1.00). Plane sections fails at 35 %/h because its predicted term uses the curvature rate of the jittered midline. The label decline follows the repair criteria (checks must pass). If the flank tolerance becomes 1.00, the field is within both tolerances while the checker fails it; Andrew may want to confirm the label after open item 1 of the freeze

## 3. Proposed changes
None applied. Each is the smallest change found for its run.

### P1 (b, rigid_drift; also the register_frames step in displacement_exceeds_patch). Prompt
Replace the second paragraph's list of checks with:
> - Rigid-body invariance adds a known rigid motion to the images and checks that the strain rate does not change. It tests the tracker. Drift or rotation of the whole root in the movie passes it
> - Closure compares the tip motion from the midline and stage log with the tip motion given by the tracked kinematics. Unlogged drift or rotation fails closure
> - Plane sections compares the flank difference with flank spacing times the curvature rate, for constant width
- The wording follows the check definitions in `checker/checks.py` and decisions 2026-10-10, not the traces

Optional, cause a part (info): `stage_log_summary` adds `closure_residual_px_per_h_at_moves` and `closure_residual_px_per_h_elsewhere`: the net residual per hour, summed over each set of pairs. On this run it would show about 7 of the 8 px/h coming from pairs without a stage move. The current fields are per-pair mean magnitudes, which the agent compared with each other only

### P2 (b, displacement_exceeds_patch). Prompt
Replace "A remedy that lowered a failing check may be applied again or at its next setting" with:
> - If a remedy lowered a failing check and can be applied again or has a next setting, do that before testing another fault
> - After a stride or patch remedy, request `displacement_vs_patch_radius` again before choosing the next action
- No ratio threshold proposed: the only basis in hand is these runs and the 2x6 labels, which would be tuning on the scored fault

### P3 (b, midline_jitter). Prompt
Add after P2:
> - A remedy has failed when a failing check still fails and the remedy cannot be applied again or has no next setting. Then decline, naming the fault the remedy targeted, unless another fault has its own evidence
- Optional, no prompt change: the `apply_remedy` result could state "no further setting" when the remedy has none left. It is computable from `REMEDIES` and the current settings

### P4 (a, width_change). Info kind and prompt
- `velocity_profile` adds `flank_spacing_rate_pct_per_h` (window mean of d ln(spacing)/dt on the same s grid) and its largest absolute value. `rec.fields["spacing"]` is already in every record; no new measurement
- Prompt rule changes from "A width change under osmotic treatment is a physical cause" to:
> - A flank spacing that changes in time is a width change: a physical cause, not a measurement fault. Use the width-free ratio
- Reason for the rule change: the task has no treatment field, so the current rule cannot apply to a synthetic rod. Adding the root's condition to the task is the alternative; it brings the manifest into the diagnostician input and is a larger change

### P5 (a, low_texture). Info kind
- `frame_quality` adds a reference: the median and the lowest `texture_contrast` and `focus` over the 15 clean basis rods (the checker threshold basis), fixed in config. Not taken from these five runs
- For real movies the reference is an open design question (clean basis rods do not match real imaging; a per-experiment median is an alternative). Andrew decides
- Prompt, secondary b:
> - Low texture or blur also makes the midline and the tracked points jitter. Check `frame_quality` before naming `midline_jitter`

## 4. Against the freeze
The freeze is proposed, not approved. Every proposal changes an item on its list.

| Proposal | Frozen item touched | Status |
| :-- | :-- | :-- |
| P1 prompt | Section 4, prompt as of 9d27233 | needs Andrew before the freeze |
| P1 optional, stage_log_summary fields | Section 3, info kinds (answers in `measure/info.py`) | needs Andrew before the freeze |
| P2 prompt | Section 4 | needs Andrew before the freeze |
| P3 prompt | Section 4 | needs Andrew before the freeze |
| P3 optional, remedy result note | Section 2 roll-back and result format (orchestration); not a remedy or setting | needs Andrew before the freeze |
| P4 velocity_profile field | Section 3 | needs Andrew before the freeze |
| P4 prompt rule | Section 4; the rule was set with `use_width_free_ratio` (Andrew, 2026-10-10) | needs Andrew before the freeze |
| P5 frame_quality reference | Section 3; a new config value | needs Andrew before the freeze |
| P5 prompt | Section 4 | needs Andrew before the freeze |

- No proposal changes a fault, size, label, remedy, setting, threshold, tolerance, model or step limit
- Not touched: the step limit (no miss was cause c)

## 5. Seeds for scoring
- All five runs, and the earlier demo runs (2026-10-09, 2026-10-10), are seed 0. P1-P5 were written from seed 0 traces
- Seed 0 is development only. A re-run on seed 0 after a change is a check, not a score
- Score on seeds 1 and 2 of the five development faults: 10 runs, labels already in the freeze (section 1). No diagnostician has seen them
- 10 runs is a small score. To enlarge it, label seeds 3-5 by tracker-only runs (no agent) before any prompt change is applied (Andrew)
- Limit: the held-out seeds share fault sizes with seed 0, so they test the prompt across noise, not across faults. The held-out faults without injectors remain the test across faults
- P1 and P5 describe fault signatures. They may favour the five injected faults over held-out ones. The single-agent and rule-based baselines should get the same check descriptions, so the comparison stays fair

## Open, for Andrew
1. Approve, edit or reject P1-P5 before the freeze
2. Seeds 1-2 as the held-out score set; whether to label seeds 3-5 first
3. Reference for `frame_quality` on real movies (P5)
4. The midline_jitter label once the flank tolerance is set (flag in section 2)
