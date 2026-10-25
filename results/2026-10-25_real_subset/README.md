# 16-root real subset, agents end to end (task c019, run 1)

Spec `docs/specs/2026-10-24b_real-movie-push.md` section C; dispatcher inbox items 31-37. Subset and rules: `docs/proposals/2026-10-24_real-subset.md`.

## Setup
- 16 include-yes montage roots: control 0711_c2, 0708_c5, 0714_c10, 0721_c1, 0711_c4; drought 0708_m12, 0711_m6, 0714_m10, 0727_mm6 (mannitol then mannitol), 0708_m8; recovery 0721_m10, 0721_m4, 0721_m9, 0727_mc1, 0727_mc3, 0727_mc5
- 3 windows per root, 2 h each: 4-6, 11-13, 17-19 h. 48 windows
- Midline: ft2 net (`net2_midline_ft2.pt`), tile mode, low 0.1 %, high 99.5 %, built on the cluster GPU (0721_m10 4-6 h on the lab-server CPU, same settings; see the log)
- Tracking: 1000 px from the tip (section A), uncoupled, whole-pixel reference copy and shifted twin, lab server
- Checks, real-movie profile: closure gates at 19 px/h (section B, `config/checker_thresholds_real.yaml`); closure definition of 2026-10-10 (kept by section A); rigid invariance and plane sections computed and reported, not gating, no real threshold
- Agents: dispatcher agent, diagnostician, auditor; model `claude-opus-5-5`, Claude Code 2.1.310

## Run
```
python scripts/real_slice.py --windows <48 windows ROOT:A-B> --config private/real_runner_c019.yaml --out results/2026-10-25_real_subset
python scripts/real_subset_report.py --run results/2026-10-25_real_subset
```
- Wall time 1059 s (tracks cached by `scripts/real_track.py`; remedy runs tracked during the run). Dispatcher: 2 rounds, 48 windows collected, 0 retries
- Files: `summary.json`, `dispatcher_trace.jsonl`, `diagnostician_trace.jsonl`, `auditor_trace.jsonl`, `windows.csv` (one row per window), `tables.md`

## Outcome
- 43 accepted, 5 declined (all at closure). No remedy was kept in any window
- Auditor: 2 flagged (r31 0714_c10 4-6 h, r34 0727_mc3 4-6 h; summary outlier, largest flank difference about -100 %/h), 41 cleared

| Group | Windows | Accepted | Declined |
| :-- | :-- | :-- | :-- |
| control | 15 | 14 | 1 |
| drought | 15 | 12 | 3 |
| recovery | 18 | 17 | 1 |

Declined windows:

| Window | Closure px/h | Fault named | Remedies (all rolled back or not run) |
| :-- | :-- | :-- | :-- |
| 0721_c1 4-6 h | 32.1 | midline_jitter | register_frames (34.7), midline smoothing light (38.2) |
| 0714_m10 17-19 h | 34.4 | midline_jitter | midline smoothing light (39.8) |
| 0708_m8 4-6 h | 48.4 | bad_stage_correction | none (no listed remedy for a wrong stage correction) |
| 0708_m8 17-19 h | 23.3 | bad_stage_correction | register_frames failed to run (see Known faults) |
| 0721_m10 17-19 h | 27.9 | bad_stage_correction | none |

Per window (all 48): `tables.md` and `windows.csv`. Columns: outcome, auditor decision, fault, closure initial and final, rigid invariance, plane sections, tracked length reached, base arc length, basal world speed, frame-0 midline length and base flag, centre REGR peak, growth-zone length.

## Base of the closure (inbox item 32)
- Tracked length reached 997-1141 px; base arc length 930-1122 px; frame-0 midline 1072 px or longer
- No window has a frame-0 midline shorter than 1000 px, so no window carries the flag 'base may be in growing tissue'
- 0727_mm6 reaches 997 px in all three windows

## Auditor's comparison (its report, condensed)
- Medians of accepted windows: control 14, REGR peak about 39 %/h at about 580 um, growth zone about 760 um; mannitol 9, about 38 %/h at about 705 um, about 650 um; mannitol then control 17, about 36 %/h at about 660 um, about 870 um
- Mannitol then mannitol (0727_mm6, 3 windows): REGR peak about 9 %/h at 1610-1894 um, growth zone 21-63 um. Cleared as a condition result; the auditor asks for a manual look before the peak position is read
- Caveat in the report: rigid invariance is high in some accepted windows (up to 119 %/h) and does not gate real movies; the clears rest on closure and the summaries
- Full text: `summary.json` (`auditor.report`)

## Known faults and limits
- 0708_m8 17-19 h: the diagnostician's register_frames remedy could not run. The lab-server output of that setting existed from the stopped earlier run, its local copy did not, and the tracker never overwrites. Fixed after this run: the runner now fetches an existing host output (`measure/real_runner.py` `fetch_host_track`). This window's decline is not a measurement result
- Rigid invariance and plane sections do not gate real movies (decisions 2026-10-23, 2026-10-24); values are reported in every row
- The tip rule for the subset was changed once before any check (proposal, decisions 2026-10-24): 6 of 18 probed roots failed the first rule, all drought or recovery; 4 of them pass the second
- Kinematics only; no claim about stress, stiffness or a constitutive law. This run is about agent behaviour; the condition comparison is the auditor's report, not a biology result
