# Proposal: growth-zone placement checks (spec 2026-11-23, task c034)

real-calib, 2026-11-23. Committed before any run. Nothing below changes after the first result is seen; a change is a new dated line in `docs/decisions.md` with the reason.

## What is checked
- The reported profile: window-mean `v_mid(s)` and `regr_mid(s)` from `derive` (grid 5 px, `s` from the first tracked centre point, window mean with the checker's 50 % coverage rule)
- Against two things the profile does not set: the tip path from the midline source plus the stage log, and the tracked centre points placed by their distance from the midline tip
- Covered span: grid points where the window-mean `v_mid` is finite; `s_end` = the last of them

## Check 1: plateau (`checker/zone_checks.py`, `plateau`)
- Basal part, fixed rule: covered grid points with `s >= 2/3 s_end` (the basal third of the covered span)
- `plateau_regr`: largest `|mean regr_mid|` over the basal part, %/h
- `plateau_speed`: `|mean v_mid over the basal part - v_tip| / v_tip`. `v_tip` = growth speed: change over the window of the arc length along the midline from the midline tip to the projection of the most basal centre point tracked in every frame, divided by the window duration, px/h
- `v_tip` under 10 px/h, or no centre point tracked in every frame: `plateau_speed` not computable (fixed non-growing rods); `plateau_regr` still computed
- Amended 2026-11-23, before any freeze v4 or real record was checked: the first draft took `v_tip` from the world path of the midline tip. That path includes the turn of the tip by bending: on the field-level rod `v3_bend24` (`measure/rod.py`, correct profile) it gave `plateau_speed` 0.37. Growth speed along the midline gives 0.0006 there
- Flag: either value over its threshold

## Check 2: material-point prediction (`checker/zone_checks.py`, `particle_path`)
- Tip-frame position of centre point `j` in frame `i`: `S_ij = s_c[i, j] + o_i` (arc length along the tracked chain plus `o_i`, the arc length along the frame's midline from its tip to the projection of the first chain point; amended with `v_tip` above, was the straight distance)
- Seeds: centre points finite in frame 0 and in the last frame
- Prediction: integrate `dS/dt = v(S)` from `S_0j` over the window, RK4 with 4 substeps per frame interval; `v` = the window-mean `v_mid` profile, linear between finite grid points, held at its last finite value past `s_end`, 0 below `s = 0`
- Residual `e_j = S_pred,j - S_Tj`, px. Values: `pp_rms_px`, `pp_max_px` (max `|e_j|`); `pp_rms_rel` = `pp_rms_px` / RMS of the tracked tip-frame displacements `S_Tj - S_0j`; `pp_max_rel` = `pp_max_px` / the largest `|S_Tj - S_0j|`
- Largest tracked displacement under 2 px: the relative values are not computable (fixed rods); px values still computed
- Flag: `pp_rms_rel` or `pp_max_rel` over its threshold. Relative values gate, so that one threshold serves roots of any speed; px values are reported

## Shifted-zone rods (truth known)
- Fault: the reported profile is displaced along `s` by `d` while the tracked points and the midline are unchanged (a growth zone placed wrong in the reported field). Injected on the record: the derived fields are recomputed and `s_grid` is replaced by `s_grid + d`; grid points with `s < 0` are dropped
- Sizes: `d` = -60, -30, -15, +15, +30, +60 px (tipward and basal by 1, 2 and 4 patch spacings; the tracker's patch spacing is 15 px on every freeze v4 and c027 track)
- Rods: freeze v4 clean rows that grow (`v3_growth_zone`, `v3_bend16`, `v3_bend20`, `v3_bend24`, `v3_bend30`), seeds 26, 27, 28, base tracks `<rod>__st1` from the freeze v4 cache: 15 tracks x 6 shifts = 90 shifted records. `v3_still` has a zero profile; a shift of it is not a fault, so it is not shifted
- No new rendering, no tracker run, no cluster job

## Thresholds (R4 rule)
- Set: the 18 freeze v4 `accept_clean` base tracks (the 5 rows above plus `v3_still`, seeds 26-28), unshifted
- Per value (`plateau_regr`, `plateau_speed`, `pp_rms_rel`, `pp_max_rel`): 99.5th percentile over the set x 1.5, rounded up to 2 significant figures; not-computable values left out
- Written to `config/zone_thresholds.yaml` and committed before any real window is checked. Existing thresholds (`config/checker_thresholds.yaml`, `config/integrity_thresholds.yaml`) unchanged

## Synthetic report
- Detection rate per shift size and direction (each check, and either check), over the 15 tracks
- False alarms on the 18 clean tracks (0 by construction of the rule; stated as such) and on the freeze v4 `accept_repaired` tracks at their labelled repair setting (reported, not used for thresholds)
- Values per record in `results/2026-11-23_zone_checks/synthetic.csv`

## Real windows (report-only)
- Every window in `results/2026-11-18_integrated_run/windows.csv` (1189): the base track (`<window>_ft2__st1__L1000`) and, where the window was accepted with a remedy kept, the accepted track at its final settings; read from the c027 track cache on the VM (md5 not rechecked; read-only). No new tracking
- Missing track or no covered span: counted as not computed
- Do not gate; no c027 outcome, prompt, threshold, remedy or scored result changes
- Report: flag counts per check by outcome class (the `integrated` column) and by condition; example windows by id with pass or fail
- Public values: `plateau_speed`, `pp_*` residuals, pass/fail and counts. `plateau_regr` on real windows is a basal strain-rate value: shown as pass/fail and counts only. No `v_tip`, zone position or REGR profile values. Per-window values stay on the VM outside the repo

## Limits stated in advance
- A displacement of the whole frame of reference (midline tip and profile wrong by the same amount) is not visible to either check: both compare the profile with the midline tip
- Plateau needs the tracked span to reach past the growth zone; on a window whose zone fills the span, `plateau_regr` flags without a placement fault
- The prediction uses the window-mean profile; growth that changes within the window adds residual on real windows that the synthetic rods (steady growth) do not have

## Outputs
- `checker/zone_checks.py`, `tests/test_zone_checks.py`, `scripts/zone_checks.py` (`synthetic`, `thresholds`, `real`; reruns skip finished records)
- `results/2026-11-23_zone_checks/README.md` (done marker), `synthetic.csv`, `real_counts.md`
