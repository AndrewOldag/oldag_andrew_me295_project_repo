# Remedy fixes, shared-compute limits, coupled mode (no agent), 2026-10-11

Spec: `docs/specs/2026-10-11_remedy-fixes-coupled-mode-shared-compute.md`. Approved thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h. Approved tolerance: centre REGR RMS error <= 2.5 % of the rod's true peak REGR, flank-difference RMS error <= 0.5 %/h (`config/scoring_tolerance.yaml`). Nothing proposed here is adopted.

Status: items 1-5, 7 (uncoupled) and 8 (code) done. Item 6 stopped at the clean basis: coupled growing rods fail closure. Two questions for Andrew at the end.

## Files
- `item3_band.md`: registration band, every variant tried, clean and rigid_drift rods
- `item4_clean.md`: clean rods through the fixed remedies, uncoupled
- `item4_faults.md`: rigid_drift, midline_jitter and low_texture sizes with the fixed remedies, uncoupled; summary, labels, every run
- `item5_labels.md`: part C labels of 2026-10-10 under the proposed and the approved tolerance
- `item6_clean_basis.md`: the 15 clean rods behind the thresholds, uncoupled and coupled
- `item7_bent.md`: bent rods, uncoupled
- Commands: `python scripts/synth/fix_sweep.py start|status|stop|fetch --part P`, then `python scripts/synth/eval_fix.py --out results/2026-10-11_remedy_fixes`

## 1. Shared-compute limits
- Built into `scripts/synth/sweep.py` (`run`, `status`, `stop`) and `measure/runner.py` (starters, single runs). Limits as in the spec; detail in `docs/decisions.md`
- Machine: 32 cores, so at most 4 workers. Available memory 181 GB. Disk free 21.6 TB
- Check, 8 clean runs (growth_zone and bending, seeds 0-1): 0 failed; 8.7-10.5 s per run with 4 at once; CPU share of one worker 0.83-0.92 of a core; peak memory 504-507 MB per run; load 1.92 before, 3.07 during, 3.07 after; 20 s wall
- One-thread outputs equal the earlier runs to 1e-13 px (all 8)
- Lock refusal and `stop` tested: a second `run` printed `refused`; `stop` ended the sweep and its workers: 0 processes left, no partial output

| Sweep | Runs | Failed | Wall (s) | Load 1 min before / max during / after | Peak workers | Projected after 10 runs (h) |
| :-- | --: | --: | --: | :-- | --: | --: |
| check | 8 | 0 | 20 | 1.92 / 3.07 / 3.07 | 4 | - |
| band (item 3) | 6 | 0 | 34 | 2.18 / 3.25 / 3.25 | 4 | - |
| band2 (item 3) | 36 | 0 | 155 | 2.31 / 5.85 / 5.24 | 4 | 0.04 |
| band3 (item 3) | 18 | 0 | 76 | 2.54 / 5.00 / 4.92 | 4 | 0.02 |
| u_clean (item 4) | 48 | 12 | 109 | 2.25 / 5.30 / 5.09 | 4 | 0.03 |
| u_clean, re-run of the 12 | 12 | 0 | 59 | 3.51 / 4.79 / 4.77 | 4 | 0.02 |
| u_faults (item 4) | 156 | 0 | 394 | 3.05 / 6.03 / 5.78 | 4 | 0.13 |
| c_time (item 6) | 4 | 0 | 11 | 1.84 / 2.47 / 2.47 | 4 | - |
| c_basis (item 6) | 56 | 0 | 172 | 2.37 / 5.14 / 4.87 | 4 | 0.05 |
| bent_u (item 7) | 12 | 0 | 84 | 2.36 / 5.25 / 5.23 | 4 | 0.03 |

- 356 tracker runs in total, 12 failed (a bug in the run-report line for the new band end, fixed and re-run). Total wall time 19 min
- Work space 4.46 GB before the first sweep, 5.5 GB after the last. No sweep process left after any sweep; no load wait was needed (1 min load never above 16)

## 2. smooth_midline
- Ends padded by linear extrapolation (odd reflection about the end value), over time and along s. A straight midline moving at 1.5 px/frame comes out unchanged to < 0.01 px at both levels (old code: 3.7 px light, 9.8 px strong)
- Clean rods: closure 0.07-0.11 px/h after light or strong (was 0.97-1.04 light, 2.91-3.03 strong). 12 of 12 pass

## 3. register_frames
- Cause confirmed on growth_zone seed 0: closure 1.16 / 0.21 / 0.08 px/h with the band from 0.6 / 0.8 / 0.9 of the tracked length (unregistered 0.10)
- Shorter bands failed other checks: fixed 0.8 rigid_invariance 2.38; fixed 0.9 plane_sections 3.73; profile to 400 px rigid_invariance 3.09 and 2.37 on two clean rods
- Profile to the end of the midline reached the moving frame border (ECC 0.75; the midline leaves the frame) and gave clean closure 0.75-0.96 px/h
- Chosen: from where the record's window-mean centre REGR falls under 5 % of its peak (305-315 px here) to the basal end of the midline, keeping pixels at least 25 px inside both frames. 6 of 6 clean rods pass (closure 0.09-0.16 px/h); 3 of 3 rigid_drift size-1 rods pass all checks

## 4. Uncoupled re-run
- Clean rods (`item4_clean.md`): 24 of 24 runs pass after no remedy, register_frames, smooth_midline light and strong. Stop condition not met
- Faults (`item4_faults.md`):

| Fault | Sizes | Meets the criteria | Note |
| :-- | :-- | :-- | :-- |
| rigid_drift | 0.25, 0.5, 0.75, 1 | all four | 0.25 and 0.5: three passes and good on 3 of 3. 0.75 and 1: 2 of 3 (seed 0 flank error 0.54 and 0.58 %/h after registration). Unremedied closure 4.1 / 8.2 / 12.2 / 16.3 px/h, after 0.11-0.45 |
| midline_jitter | 0.5, 1, 2, 3 px | none | strong smoothing brings plane_sections under 3.25 at 0.5 px (3 of 3) but not closure: closure is unchanged by smoothing (0.5 px: 0.37, 1.05, 1.16 px/h on seeds 0-2). See question 1 |
| low_texture | contrast 0.2, 0.25 | none | enlarge_patch gives three passes on 1 of 3 (0.2) and 2 of 3 (0.25), but the flank-difference error stays 0.52-1.02 %/h, above 0.5. Never good |

- Proposed sizes (not adopted):
  - `rigid_drift` 0.5: the largest size with three passes and a good measurement on 3 of 3 seeds after register_frames; unremedied closure 8.1-8.2 px/h, 8 times the threshold
  - `midline_jitter`: none meets the criteria with the remedy as fixed
  - repairable `low_texture`: none at 0.2 or 0.25

## 5. Tolerance
- In `config/scoring_tolerance.yaml`, status approved, with date and basis. `measure.score.rod_tolerance`: centre limit 1.085 %/h on the standard rods (peak 43.4 %/h), 2.17 %/h on the 2x6 rods (peak 86.9 %/h)
- Tests: the 2x6 rod and a clean rod, each 0.01 %/h inside and outside each limit (`tests/test_score.py`)
- Part C labels recomputed on the same runs: no label changes (`item5_labels.md`)

## 6. Coupled mode (stopped)
- `couple` is a field of the run settings, passed as `--couple`, recorded in the record's settings, and the run tag gets `_cpl`. Not a remedy, not on any agent list
- Timing, growth_zone seed 0, the rod and its moved copy: uncoupled 9.3 s, coupled 9.4-9.6 s per run; peak memory 504-505 MB and 505-507 MB. Under the 5x limit
- Clean basis (`item6_clean_basis.md`): coupled, all 10 growing rods (growth_zone and bending, seeds 0-4) fail closure, 1.46-1.99 px/h. rigid_translation passes 5 of 5. Coupled centre REGR error 4.4-5.3 %/h against 0.41-0.44 uncoupled
- Not a reading error here: the tracker's own REGR output on growth_zone seed 0 peaks at 31.9 %/h coupled and 43.3 %/h uncoupled (truth 43.4)
- Stopped per the spec. Not run: remedies on clean rods, faults, rotation, coupled (about 420 runs)

## 7. Bent rods
- `bend_continue` and `bend_reverse` added (field level: derived fields match the truth; integrated strain rate equals tip velocity). Image level: frame 640 px wide, base at column 400, tracked length 400 px
- Uncoupled, 3 seeds each: 6 of 6 pass all three checks. plane_sections 0.62-1.75 %/h (continue), 0.93-2.24 (reverse). Centre REGR error 0.49-0.58 %/h; plus flank 0.46-0.71, minus flank 0.36-0.66 %/h
- Coupled not run (item 6 stop)

## 8. Diagnostician, part D (code only)
- Prompt: the two rules of the spec replace "Do not repeat a remedy that has already failed for the same fault"
- `apply_remedy` results show each check's value before and after; roll back when a remedy makes no failing check pass and lowers none by a quarter. Tests in `tests/test_executors.py`
- No diagnostician runs: they wait for Andrew's approval of the sizes

## Questions for Andrew
1. `smooth_midline` with odd-reflection padding keeps the first and last midline of the window as they are, jitter included. Closure depends on the net tip displacement, so smoothing cannot lower it. Fitting the padding line to the last few frames (a least-squares line, not the end value) also passes the translating-midline test and would smooth the end frames too. Changing it now would be changing a remedy after seeing the fault results. Change it, or keep it and record `midline_jitter` as not repairable?
2. Coupled tracking flattens the growth zone (peak 31.9 against 43.4 %/h) and fails closure on all 10 growing clean rods. Continue the coupled sweeps as data, stop coupled runs, or other?
