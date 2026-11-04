# Agent run over real-calib's first batch (task c022)

Dispatcher inbox item 39. Batch: real-calib's first batch (`results/2026-10-25_full_batch_1/`, proposal `docs/proposals/2026-10-25_full-batch.md`).

## Setup
- 11 include-yes montage roots, one per experiment and condition: 0708_c2, 0708_m1, 0711_c3, 0711_m1, 0714_c5, 0714_m1, 0721_c2, 0721_m1, 0727_cc1, 0727_mc2, 0727_mm1
- 126 windows of 2 h over each root's usable hours (last window shorter where the hours end)
- Same system and settings as the 48-window subset (`results/2026-10-25_real_subset/`): ft2 net midline, 1000 px tracks, uncoupled; dispatcher agent -> checker (real-movie profile: closure gates at 19 px/h; rigid invariance and plane sections reported) -> diagnostician -> auditor
- Cached tracks from real-calib (lab server). Moved copy (rigid invariance) only for the 10-12 h window of each root, as real-calib made them (`--moved-span 10-12`). Remedy retracks on the lab server under its limits
- Model `claude-opus-5-5`, Claude Code 2.1.310. One run (no repeats)

## Run
```
python scripts/real_slice.py --windows <126 windows ROOT:A-B> --config private/real_runner_c022.yaml --moved-span 10-12 --min-free-gb 3 --out staging/c022/run4
python scripts/full_batch_agents_report.py --run staging/c022/run4 --out results/2026-10-25_full_batch_1_agents --rescore
```
- Run 4 is the reported run. Wall time 1892 s. Dispatcher: 4 rounds, 123 windows collected, 3 given up after retries (6 retries)
- Remedy tracks in run 4: 3 new, 20-33 s each on the lab server; the rest cached from run 3
- Diagnostician: 34 calls over the windows with a failing check. Auditor: 7 steps
- Runs 1-3 did not complete; each found a fault in the run code, fixed before the next run (`docs/decisions.md`, 2026-10-25):
  - Run 1: one window's tracker error aborted every collect call; 3 of 126 windows collected
  - Run 2: a remedy retrack's ssh call hung after the host had finished; stopped by the session after 5 windows
  - Run 3: all windows done; crashed printing the auditor's report (console encoding) before `summary.json` was written
- Traces and `summary.json` of every run are kept out of git (`staging/c022/`): the auditor's report quotes REGR and growth-zone values (Andrew, 2026-10-25: biology values out of course scope)

## Files
- `windows.csv`: one row per collected window: experiment, condition, outcome, fault named, remedies tried and rolled back, closure pass or fail, auditor run id, decision and reason, re-score note
- `tables.md`: outcome and auditor counts per condition group, experiment, and experiment type and condition; faults; remedies; windows with no computable closure; the auditor's report reduced to agent behaviour, numbers masked

## Outcome (re-scored under the 2026-10-26 rule)
- Rule (Andrew, 2026-10-26; `docs/decisions.md`): a real window whose gating check (closure) cannot be computed is declined, without an agent call; the auditor is not asked about it. Re-scored from the run 4 records (`--rescore`); the outcome follows from the rule, so no tracker or agent rerun. 4 windows change from accept to decline: 0711_c3 0-2 h, 0721_c2 4-6 h, 0727_mc2 0-2 h, 0727_mc2 2-4 h (the auditor had flagged all 4 in the run)
- 126 windows: 110 accepted, 13 declined, 3 not collected (tracker error `arange: cannot compute length` on 0711_m1 0-2 h, 0721_c2 6-8 h, 0727_cc1 0-2 h; the same 3 windows real-calib could not measure)
- Declined: 9 failed closure (fault named by the diagnostician: bad stage correction 8, midline jitter 1); 4 closure not computable (declined by rule)
- Remedies: frame registration tried on 5 windows: kept on 1 (0708_m1 18-20 h, then accepted), rolled back on 4 (declined). Midline smoothing tried on 1 (0714_c5 6-8 h, declined, fault midline jitter)
- 5 of the 9 declined windows had no remedy tried (0708_m1 10-12, 12-14, 14-16 h; 0714_c5 0-2 h; 0721_c2 8-10 h): in each, the diagnostician placed the closure residual at the logged stage moves and declined
- Auditor: 110 accepted windows, 91 cleared, 19 flagged (summary outlier 19). In the run it decided on 114 accepted windows (23 flagged: summary outlier 20, other 3); its decisions on the 4 re-scored windows are dropped

| Group | Windows | Accepted | Declined | Auditor clear | Auditor flag |
| :-- | :-- | :-- | :-- | :-- | :-- |
| control | 52 | 45 | 7 | 37 | 8 |
| drought | 47 | 43 | 4 | 32 | 11 |
| recovery | 24 | 22 | 2 | 22 | 0 |

## Agent behaviour found
- Closure was not computable on 4 windows (0711_c3 0-2 h, 0721_c2 4-6 h, 0727_mc2 0-2 h, 0727_mc2 2-4 h). No check failed, so the orchestrator accepted them without calling the diagnostician. The auditor flagged all 4 (3 as "accepted with no measurement"). Under the rule then in force the auditor was the only stage that caught them; the 2026-10-26 rule now declines such windows (`scripts/real_slice.py`, `rule_outcome`)
- The auditor flagged 20 accepted windows as summary outliers that passed closure, and named the limit itself: closure alone does not catch a misplaced or collapsed growth zone; rigid invariance does not gate on real windows
- Auditor's control vs stressed comparison (written in the run, before the re-score): it compared cleared runs per condition and stated that differences between conditions are measurement results, not faults. It flagged a larger share of mannitol runs than control runs (counts above). Its per-condition values are withheld here (biology, out of course scope)

## Known limits
- Real-movie checker profile: closure is the only gate; rigid invariance computed on 11 windows only; plane sections reported, not gating
- One run, no repeats; agreement not measured on this batch
