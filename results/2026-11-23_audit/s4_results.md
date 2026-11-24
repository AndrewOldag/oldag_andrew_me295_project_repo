# Section 4: results tables recomputed from committed files (task c033)

Scope: `results/2026-11-18_integrated_run/`, `results/2026-11-18_heldout_compound/` and `supplement/`, `results/2026-11-18_auditor_check/`, `results/2026-11-20_registration_fix/`, `results/2026-10-25_freeze_v4/`. Date of the check: 2026-11-23. Read-only. Scripts in `results/2026-11-23_audit/scripts/`, each under 1 min, none writes a file:
- `s4_integrated.py`: integrated-run tables from `windows.csv` and the disagreement rows of `tables.md`; window list from `scripts/run_all.py` `window_list()` in memory
- `s4_scored.py <folder>`: independent recompute of a scored synthetic set (summaries vs `scores.json`, classes vs `labels.json`, categories, metrics per repeat, Fleiss kappa, per row, cost, deterministic reruns, set-aside runs); run on freeze v4, c029 and c029b
- `s4_metrics_code.py`: the repo's `measure/metrics.py` (`over_repeats`, `agreement`) on each `scores.json`, compared field by field with `metrics.json`
- `s4_synth_extra.py`: freeze v4 v3-alongside and decomposition tables, known limits (a)-(d), tracker counts; c029 table without the 3 missing-state runs, expected vs label, selection rule, equivalence, flicker checks
- `s4_auditor.py`: auditor check from `batches.json`, `run_map.json`, `rule/*.json`, `llm/*_result.json` (not from `scores.json`)
- `s4_registration.py`: every table and number of the registration-fix README from its JSON files

Counts: blocker 0, major 0, minor 9. Every table in the five folders that can be recomputed from committed files matches to the printed precision. The findings are wording and missing provenance.

## Findings

### Integrated run (`results/2026-11-18_integrated_run/`)

### S4-1 (minor): README says "the 16 disagreements" are in tables.md; the table has 27 rows
- Where: `results/2026-11-18_integrated_run/README.md:34`; `tables.md:38-66`
- Evidence: `s4_integrated.py`: 90 windows with both final; outcome differs on 16 (same set as `windows.csv`), kept settings differ on 21; the table lists the union, 27 rows (16 outcome disagreements, 11 with the same outcome and different kept settings). The 10 / 6 split of the 16 is correct
- Fix: say "the 27 windows where outcome or kept settings differ (16 outcome disagreements)"

### S4-2 (minor): `windows.csv` auditor column is empty on all 1,189 rows; auditor counts cannot be traced
- Where: `results/2026-11-18_integrated_run/windows.csv` (column `auditor`); `scripts/run_all_report.py:197-198`; README lines 36, 42; `tables.md:78,80`; `failure_modes.md:14`
- Evidence: 0 of 1,189 rows have a value. The report looks up auditor decisions by window id (`rid == w`), but auditor decisions are keyed by run id (`r01`...; e.g. `0708_c10: r02` in `example_traces.md`). Auditor runs 99, calls 439 and flags 240 have no committed per-root source. 99 = 102 roots - 3 roots with paused windows is consistent
- Fix: map run ids to windows in the report (or commit the per-root auditor decisions) and regenerate `windows.csv`

### S4-3 (minor): LLM, tree-remedy, cluster, spend and 5 failure-mode counts have no committed source
- Where: `results/2026-11-18_integrated_run/README.md:35-37`; `tables.md:73,79,84`; `failure_modes.md:5,12,13,15,16`
- Evidence: the run records, tree records, traces, queue and ledger are in the git-ignored `staging/c027/`. Not recomputable: all-trace calls 1,007; auditor calls 439; tree remedies 352 / 27 / 325; retrack tasks 616 in 47 arrays (576 / 28 / 12); spend $8.248 (only in `docs/agents/status/dispatcher.md:15`); failure-mode counts tracker error 4, worse remedy diagnostician 33 and tree 76, retrack failed 28, link down 1. Their examples: `0711_m1__w0-2` exists (declined by rule, closure nan); `0708_c10__w0-2` diagnostician worse remedy is shown in `example_traces.md` (76.11 -> 80.88 px/h, rolled back); the tree example, the retrack error and the link-down entry cannot be checked. Recomputed from `windows.csv`: diagnostician calls 358, remedies 73 / 4 / 69, both match
- Fix: commit a small summary of the queue (state counts per array), the ledger total for c027 and the per-window tree remedy list (settings, closure before/after, kept), or state in the README that these numbers come from `staging/c027/` and are not committed

### S4-4 (minor): tables.md prints "(cap 900)" beside 1,007 calls
- Where: `results/2026-11-18_integrated_run/tables.md:79`; string hard-coded in `scripts/run_all_report.py:157`
- Evidence: README line 14 says the cap was raised to 1,300 at 782 calls. `tables.md` alone reads as a cap overrun
- Fix: print the cap in force (1,300, raised from 900 on 2026-11-23) from the run log, not a literal

### Freeze v4 (`results/2026-10-25_freeze_v4/`)

### S4-5 (minor): README metrics table drops the repeat ranges of coverage and abstention columns
- Where: `results/2026-10-25_freeze_v4/README.md:28-29` (header line 22: "range in brackets")
- Evidence: recomputed and in `table_metrics.md:10-11`: diagnostician coverage 0.58 (0.57-0.59), abstention recall 0.79 (0.75-0.83); single agent coverage 0.48 (0.43-0.55), abstention precision 0.50 (0.33-0.67), abstention recall 0.10 (0.04-0.17). The README gives the means without ranges. Means are correct
- Fix: copy the ranges from `table_metrics.md`

### S4-6 (minor): tracker-run total 404 only partly traceable
- Where: `results/2026-10-25_freeze_v4/README.md:104`
- Evidence: `tracker_runs_new` summed over the 306 scored LLM summaries gives 57 (diagnostician 28, single agent 29); README says 58 single jobs. Development-check and usage-limit summaries record 0. The cut-off run (single agent, stage_log_missing s27 r2) has no summary and may account for the 58th. Labels 228 and method states 118 have no committed count
- Fix: state where 58, 228 and 118 come from (run log or cache listing), or commit the count

### Held-out compound c029 and supplement c029b (`results/2026-11-18_heldout_compound/`)

### S4-7 (minor): tracker-output totals not traceable
- Where: `results/2026-11-18_heldout_compound/README.md:23` ("1,365 outputs cached"); `supplement/README.md:22` ("2,608 tracker runs, 0 failed")
- Evidence: no committed file lists cached outputs or array task counts. `labels.json` gives label states (c029 872 over 24 rods; c029b 1,744 over 48 rods), which are not tracker outputs. The c029 "5 runs failed" is consistent with `labels.md` (6 states marked "tracker error on the cluster (twice)"; one is a width-free state that reuses a failed track)
- Fix: name the source of the counts (cache listing, queue log) in the README or commit a count file

### Registration fix (`results/2026-11-20_registration_fix/`)

### S4-8 (minor): v2 rigid-invariance column of the R5 table has no committed source
- Where: `results/2026-11-20_registration_fix/README.md:80-89`
- Evidence: `regression.json` and `regression.md` hold closure, outcome, gate, rotation and band motion, not rigid invariance. The v1 column (1.69, 0.80, 1.08, 1.67, 0.80, 1.12) matches `results/2026-10-25_freeze_v4/labels.md:88-128` (register_frames states). The v2 values and "over 2.0 %/h on 3" can only be inferred from `all_pass` false on the 3 rods with closure passing; the values themselves are not in a tracked file
- Fix: add the rigid-invariance value (v1 and v2) to `regression.json` and `regression.md`

### S4-9 (minor): direct-fit frame range off by one
- Where: `results/2026-11-20_registration_fix/README.md:14` ("ECC fails on frames 21-80 (59 of 79 fits)")
- Evidence: `register_diag_0711_c5__w6-8.json`: 80 frames (0-79), 79 fits; the first failed fit (`ecc` null) is frame 21, the last frame is 79; 59 failed fits = frames 21-79. The same line uses 0-based frames for "frames 1-20"
- Fix: "frames 21-79"

### Cross-reference
- `results/2026-11-18_integrated_run/example_traces.md:17` (unmasked strain-rate profile in a file that says it is masked) is S1-3; not repeated here

## Repo scripts that produced the tables
- `scripts/run_all_report.py` (via `run_all.py report`): reads `staging/c027/` (git-ignored, absent here). Not run. Its `window_list()` was run in memory: 1,189 windows, same order as `windows.csv`
- `scripts/synth/heldout_compound.py eval`, `heldout_supplement.py eval`, `scored_v4.py eval|decompose`, `scripts/synth/auditor_check.py score`: write into the tracked results folders. Not run. Their metric code `measure/metrics.py` was run in memory on each `scores.json` (`s4_metrics_code.py`): 0 differences from `metrics.json` for script, remedy tree, diagnostician and single agent in all three sets (all-decline and all-accept are not in `scores.json`; checked by hand below)
- `scripts/integrity_thresholds.py thresholds|relative|report|pairs`: need the track caches (not committed). Not run. Thresholds and k were recomputed from the committed JSON in section 2 (`s2_integrity_recompute.py`)

## Checked, no finding

### Integrated run
- Windows 1,189, roots 102 = include-yes roots in `manifest/root_manifest.csv` (`s4_integrated.py`)
- Outcome per method, 3 rows x 9 columns: integrated 1034/2/58/0/85/6/4, tree 1034/12/58/78/7, fixed script 1034/0/58/93/4: match README:29-31 and `tables.md:9-11`
- Per condition (6 rows) and per experiment (5 rows): all 77 cells match `tables.md:17-32`
- Diagnostician vs tree: both final 90, same outcome 74, same kept settings 69 (90 - 21 rows with different kept settings), tree accepts where diagnostician did not 10, diagnostician step limit and tree decline 6; for all 27 table rows the diagnostician outcome, tree outcome and remedy count match `windows.csv`
- Remedies tried by the diagnostician 73, kept 4, rolled back 69; diagnostician calls 358
- Paused: 4 integrated (0708_m9 10-12 needs a register_v2 track; 0721_m5 0-2, 0727_cc7 0-2 and 2-4 need the base track), tree 3 more (0708_m1, 0714_c9, 0727_cc6, 10-12 h); not measured in any batch 2 (0727_cc7 0-2, 2-4); roots with paused windows 3
- Failure modes with counts recomputable: not measured 2, declined by rule 58 (first `0708_c10__w20-22`), diagnostician step limit 6 (first `0708_c4__w0-2`), tree step limit 0, window error 0, paused 4 (first `0708_m9__w10-12`): counts and examples match `failure_modes.md`
- Example traces: `0714_m7__w18-20` accepted after repair (closure 19.75 -> 18.32, 6 calls, 1 remedy kept), `0708_c10__w0-2` declined by agent (76.11, 5 calls, 2 remedies): match `windows.csv`
- Demo, cached side: 12 windows of 0708_c4, outcomes and initial closures equal `windows.csv`; `0708_c4__w0-2` has 3 remedies in the cached run (README: 2 vs 3); 10 accepted windows = 1 flagged + 9 cleared; `--llm-cap 293` = 1,300 - 1,007. Demo side not committed

### Held-out compound c029
- `s4_scored.py`: 192 summaries = 192 `scores.json` rows; status, steps, tokens, call time, error, remedies agree on every row; classes agree with `labels.json`; categories recomputed from status, class and good on every row: 0 mismatches
- Metrics table, 6 methods x 7 columns (README:30-35), not-reported 12 / 49, per-row table 24 cells, agreement (15 of 24, kappa 0.460; 15 of 24, 0.448), cost (499 / 532 calls; 2,457,655 / 286,454 and 2,481,486 / 287,406 tokens; 3,095.3 / 3,159.6 s; tree 113 steps): all match
- Table without the 3 missing-state runs (README:48-49): runs 71 / 70 and every cell match. The 3 traces with a "Missing" tool result are exactly the 3 named
- Labels: accept_repaired 4, decline 20; all-decline 20 of 24; expected differs from label on 8 rods (focus_drift 4, illumination_flicker 4)
- Deterministic reruns 48 of 48 identical; usage-limit set-aside 9 runs (single agent); 144 scored + 9 = 153
- Cluster equivalence: largest difference 3.48e-7 px (`cluster_equivalence.json`)
- Flicker: unremedied script runs fail rigid invariance and plane sections 4 of 4, closure 3 of 4

### Supplement c029b
- `s4_scored.py`: 160 summaries = 160 rows; 0 mismatches; labels of 48: accept_clean 7, accept_repaired 19, decline 22; selection rule (first 4 / 10 / 6 in seed order) reproduces `selected.json`; 11 of 20 selected differ from the expected class, split as README:21
- Metrics table 6 x 8 cells, not-reported 1 / 20, 18 unnecessary declines (rate 0.60), 3 clean runs keeping a remedy, per-row table 10 rows x 4 methods, agreement 19 of 20 (0.955) and 14 of 20 (0.700), cost (285 / 394 calls; 1,355,004 / 162,532 and 1,818,016 / 213,601 tokens; 1,679.2 / 2,274.7 s; tree 56 steps), all-decline 6 of 20: all match
- Deterministic reruns 40 of 40; set aside: missing state 2, usage limit 2 (both diagnostician); 120 + 4 = 124

### Auditor check
- `s4_auditor.py` from raw decisions: 30 batches of 8, each from one row, all 240 runs good accepted freeze v4 runs; plants 4 / 4 / 4 / 3
- Catches (5 rows x 4 auditors) and false alarms (by batch plant, 6 rows x 4 auditors): every cell matches README:24-38 and `scores.md`
- Agreement: 240 runs decided in all 3 repeats, 227 unanimous, Fleiss kappa 0.836; planted 14 of 15 unanimous, split b25 (rigid_drift) flag / clear / flag
- Reasons: closure_relabelled LLM 12 of 12 `check_failed_but_accepted` with closure in the evidence; rule flags those 4 on summary outliers only; wrong_unit LLM clears 12 of 12, rule flags 4 of 4 on z; doubled_frame LLM flags 2 of 9 (b25); planted doubled runs pass all checks, robust z -46.5 to -90.4 (batch MAD as README:48); b13 planted z 3,952; the b24 r0 quote and the b13 "2.1x" wording occur in the reports
- Cost: 90 runs, all status report, 382 steps and calls, tokens 3,090,685 / 307,874, call time 3,635.5 s, 8 commits; usage-limit file b24 r1 at 15:09:21; rule false-alarm rate 55 / 225 = 0.24

### Registration fix
- `s4_registration.py`: chained pair rotations 79, sum 9.23, mean 0.117, mean absolute 0.23, largest 1.00 deg; ECC min 0.967, median 0.977; pair band motion median 0.52, largest 1.53 px; last-map band motion 21.74 px; path 2.44 / 5.13 / 6.27 / 9.23 deg at frames 10 / 20 / 50 / 70; direct fit -1.54 to 6.02 deg on frames 1-20, ECC 0.88-0.97, 59 of 79 fits failed, map held at 6.02 deg, band motion 3.89 px, bound 46 px / 2 deg, plausible false
- Flagged-window integrity table (3 tracks x 3 values) and gate table (2 tracks x 4 values): match; ratios recomputed from the absolute values ((n+1) for inversions) match the stored ratios
- Batch-1 table: 115 tracks; inversions median 0, p95 417, max 720, pass 75; gap ratio 1.94 / 3.83 / 8.68, pass 93; lateral 1.37 / 5.26 / 94.1, pass 0; pass all 0; 40 with inversions. Synthetic medians / max from `thresholds.json` (27 tracks) match
- Relative k pairs: inversions 1.0 on 9; gap ratio 0.995-1.0; lateral 1.0-1.95, register rods 1.24-1.95, 3 width-free rods 1.0 with the same track
- `relative_check_v1.json`: batch 1 7 pairs, pass 1, fail inversions 6, gap 2, lateral 3; batch 2 (36 + the flagged window) 37, 16, 20, 18, 19; each `passed` flag agrees with its ratios and k; medians over 44 pairs 4.84 / 1.45 / 2.44
- R5: outcomes v1 6 of 6, v2 3 of 6; v2 closure lower on all 6 (0.20, 0.22, 0.13, 0.07, 0.04, 0.11 px/h); good 12 of 12; gate passes 12 of 12; v2 rotation 0.002-0.413 deg, band motion 2.81-8.16 px, plausible 6 of 6; rigid-drift rotations 0.358-0.413
- Flagged window initial closure 22.83 px/h matches `windows.csv` (final c027 record: declined by agent, no remedy)

### Freeze v4
- `s4_scored.py`: 408 summaries = 408 rows, 0 mismatches; labels 18 / 9 / 24, clean_fails 0; all-decline 24 of 51
- Metrics table means (6 methods x 10 columns), false-accept rates 0.35 / 0.06 / 0 / 0.01, not-reported 7 / 66, accepted runs keeping a remedy on clean rods 2 of 2 and 14 of 23, agreement table (2 x 6), per-row table 17 rows x 4 methods, cost table (steps 152 / 655 / 1,040; tokens and call time), deterministic 102 of 102: all match
- v3 alongside (4 x 6) and decomposition (4 x 5) balanced accuracy, unchanged-row accept_repaired 0.59 -> 1.00, single-agent decline 0.43 -> 0.11, v3 labels 18 / 12 / 21, v3 behaviour on stage_log_missing (tree 3 decline, diagnostician 9 decline, script 3 accept, single agent 9 step limit): all match
- Known limits: (a) second_root diagnostician 8 accept_on_decline, 1 correct_decline; single agent 1 / 8 step limit; width-free in 9 of 9 for both; `crop_to_main_root` in 0 runs. (b) 153 of 153 single-agent runs start with `check_report`; 171 remedies; info calls after a remedy 0: 53, 1: 66, 2: 46, 3: 6 (using the rerun trace `_trace_132120` for the cut-off run; the partial trace gives 67 / 45). (c) 7 of 9 accept with only `use_width_free_ratio`. (d) 7 diagnostician runs with a remedy applied and no failing check, 0 rolled back, split 2 / 3 / 2 as stated
- Usage-limit set-aside 95 runs: diagnostician repeat 1 23, single agent repeat 0 27, repeat 2 45; 306 + 17 development + 95 = 418; development check 17 runs, 14 correct
- Every scored LLM run records Claude Code 2.1.310 and `freeze-v4` (306 v4, 144 c029, 120 c029b); tag `freeze-v4` is tag object e9f19f2 on commit b86abef
