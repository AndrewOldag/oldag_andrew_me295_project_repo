# Growth-zone placement checks, 2026-11-23 (task c034, report-only)

Spec `docs/specs/2026-11-23_growth-zone-checks.md`. Proposal `docs/proposals/2026-11-23_zone-checks.md`, committed before any run (e385ae2; amended before any freeze v4 or real record, f5cc997). Code `checker/zone_checks.py` (deterministic, no LLM), driver `scripts/zone_checks.py`, tests `tests/test_zone_checks.py`. No tracker run, no cluster job, no LLM call.

## Files
- `synthetic.csv`: values per freeze v4 record (18 clean, 90 shifted, 9 repaired)
- `synthetic.md`: detection table with the thresholds
- `real_counts.md`: flag counts on the c027 windows by outcome and by condition, residual percentiles, example windows
- Thresholds: `config/zone_thresholds.yaml` (3cf728b, committed before any real window was checked)

## Checks
- Plateau: largest `|mean regr_mid|` over the basal third of the covered span (`plateau_regr`, %/h); `|mean v_mid there - v_tip| / v_tip` (`plateau_speed`), `v_tip` the growth speed along the midline from the midline tip to the most basal centre point tracked in every frame
- Particle path (Silk): centre points placed by their distance from the midline tip in frame 0, moved by `dS/dt = v(S)` with the window-mean `v_mid` profile (RK4), against their tracked positions in the last frame. `pp_rms_px`, `pp_max_px`; relative to the tracked displacements `pp_rms_rel`, `pp_max_rel`
- Flags: plateau on `plateau_regr` or `plateau_speed`; particle path on `pp_rms_rel` or `pp_max_rel`

## Thresholds (R4 rule: 99.5th percentile over the 18 freeze v4 accept_clean base tracks x 1.5, rounded up to 2 significant figures)
- `plateau_regr` 8.5 %/h, `plateau_speed` 0.018, `pp_rms_rel` 0.0044, `pp_max_rel` 0.0063

## Synthetic (freeze v4, seeds 26-28; profile shifted by -60 to +60 px, patch spacing 15 px)

| Set | Shift px | Records | plateau | particle path | either |
| :-- | --: | --: | --: | --: | --: |
| accept_clean (threshold set) | 0 | 18 | 0 of 18 | 0 of 15 | 0 of 18 |
| shifted | -60, -30, -15 | 15 each | 0 of 15 each | 15 of 15 each | 15 of 15 each |
| shifted | +15, +30, +60 | 15 each | 0 of 15 each | 15 of 15 each | 15 of 15 each |
| accept_repaired (not in the threshold set) | 0 | 9 | 0 of 9 | 0 of 9 | 0 of 9 |

- Particle path detects every shift down to one patch spacing. At 15 px either way, `pp_rms_rel` is 0.058-0.061 against the threshold 0.0044 (about 13x); clean growing tracks 0.0012-0.0030
- Plateau detects none. The freeze v4 zone reaches into the basal third of the 500 px tracked span (clean `plateau_regr` 5.2-5.6 %/h; +60 px gives 7.9-8.2, under 8.5). A shift of the profile does not change its plateau speed (`plateau_speed` 0.004-0.014 at every shift)
- False alarms: 0 of 18 clean (0 by construction of the rule), 0 of 9 repaired
- `v3_still`: `plateau_speed` and relative particle-path values not computable (no growth), as stated in the proposal

## Real (c027, 1,189 windows; base track each, plus the 2 accepted tracks made by a kept remedy)
- Computed on 1,186 base tracks; 3 not computed (paused windows with no cached base track)
- Base tracks flagged by either check: accepted 1,034 of 1,034; declined by agent 84 of 85; step limit 6 of 6; paused 1 of 1 computed; declined by rule 3 of 58 (55 have no profile)
- By condition: control 397 of 417, mannitol 324 of 345, mannitol then control 293 of 300, mannitol then mannitol 68 of 72, control then control 48 of 53 (the rest not computable). Tables: `real_counts.md`
- Residuals, base tracks: `pp_rms_rel` median 0.030, 90th percentile 0.17 (threshold 0.0044); `pp_rms_px` median 3.5 px, 90th percentile 22 px over a 2 h window; `plateau_speed` median 0.038 (threshold 0.018)
- What drives the large residuals: in the quarter of base tracks with the largest `pp_rms_px`, 98 % (median) of the squared residual is a part common to every point, and the mean residual equals minus the change of the first chain point's distance from the midline tip over the window (correlation -1.00). That distance changes by more than one patch spacing (15 px) on 143 of 1,127 base tracks. The checks do not tell whether the midline tip or the first tracked point moved
- Example windows by id: `real_counts.md`, last table

## Reading
- On synthetic rods with steady growth, the particle-path check finds a profile displaced by one patch spacing on every rod with no false alarm. The plateau check, with the basal-third rule fixed in advance, finds none on these rods
- Thresholds set on rendered rods do not transfer to real windows: every accepted real window is over them. The real floor of `pp_rms_rel` is about 7x the synthetic threshold at the median. The checks gate nothing and no c027 outcome changed
- A real threshold would need a real reference set (as for closure, c018) and Andrew's approval; not done here

## Limits
- The fault model is an arc-length offset of the profile (profile at the wrong s relative to the tracked tissue). It does not cover a zone misplaced by a tracker error of another kind
- The shifted rods displace the reported profile only; a displacement of the whole frame (midline tip and profile together) is not visible to either check
- The particle-path residual uses the midline tip in the first and last frame only, so midline-tip noise in those two frames enters every point
- Real growth that changes within a 2 h window adds residual that the steady synthetic rods do not have

## Commands
```
python scripts/zone_checks.py synthetic --cache <freeze v4 track cache>
python scripts/zone_checks.py thresholds
python scripts/zone_checks.py real --cache <c027 track cache>      # per-window values to staging/zone_checks/real.jsonl
python -m pytest tests/test_zone_checks.py
```
