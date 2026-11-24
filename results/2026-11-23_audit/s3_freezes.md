# Section 3: freezes and held-out sets (c033)

Scope: freeze v3 (spec 2026-10-23b, `results/2026-10-23_freeze_v3/`), freeze v3.1 (spec 2026-10-24, `results/2026-10-24_freeze_v3.1/`), freeze v4 (`results/2026-10-25_freeze_v4/`), c029, c029b, c030 (spec 2026-11-18 D, E; `results/2026-11-18_heldout_compound/` with `supplement/`, `results/2026-11-18_auditor_check/`), `docs/decisions.md`, lab reports 2-3. Usable-window rule over every tracked file, the private fq-real frame list and the staged fq-real labels (read only).

Method: `git log --all --date=iso` (author and commit dates, offsets kept), `git tag`, `git diff --stat` between the tag and the last scored run on agents/, checker/, config/, measure/, prompts and drivers; `commit` field of every run summary. Scripts: `scripts/s3_windows_check.py` (tracked files and fq-real frames against the manifest; 10 s), `scripts/s3_windows_history.py` (same over older trees), `scripts/s3_fq_reference.py` (real frame_quality reference with and without out-of-rule windows).

Counts: blocker 0, major 1, minor 5.

## Commit order

Times as committed (PDT -0700 to 1 Nov, PST -0800 after; UTC rows marked +0000).

### Freeze v3 (tag `freeze-v3` -> e1e672a)

| Commit | Time | What |
| :-- | :-- | :-- |
| cd11da9 | 2026-10-23 13:34 -0700 | proposal |
| d9d5318 | 2026-10-23 13:47 -0700 | approval recorded (Andrew 13:41) |
| 1a16f11 | 2026-10-23 13:56 -0700 | v3 rods, curvature-corrected width-free ratio, scoring tolerance, metrics |
| 47a3c47 | 2026-10-23 14:07 -0700 | driver `scored_v3.py`, seeds 20-22 |
| f599564 | 2026-10-23 14:53 -0700 | held-out sizes (36 runs; no size change) |
| 6ebc9db | 2026-10-23 22:12 +0000 (15:12 -0700) | labels of 51 rods |
| e1e672a | 2026-10-23 18:33 -0700 | CLI pin 2.1.310, v3_bend30 kept accept_clean; tag `freeze-v3` (tag object 18:33:57 -0700) |
| 869f130 | 2026-10-23 22:34 -0700 | first scored runs: script and remedy tree (run summaries record 231d418, 21:51) |
| f8b6729 .. b6bbf2c | 2026-10-23 22:35 to 2026-10-24 04:03 -0700 | 306 LLM runs |
| 8e1888a | 2026-10-24 04:16 -0700 | metrics, README |

- `git diff e1e672a 8e1888a` on agents/, checker/, config/, measure/score.py, metrics.py, remedies.py, record.py: none. Only `scripts/synth/scored_v3.py` (b3829b3, `--max-runs` block option)
- Run summaries: 408 of 408 `freeze_tag` freeze-v3; commits 231d418 .. d04cf92, all after the tag

### Freeze v3.1 (no tag; ended at its stop rule)

| Commit | Time | What |
| :-- | :-- | :-- |
| (spec) | 2026-10-24 | spec 2026-10-24_freeze-v3.1 |
| 66a94a3, dd9fcf7 | 2026-10-24 19:17 +0000, 12:18 -0700 | sizing sweeps; stop rule reached |
| 9b7ea8c | 2026-10-24 12:44 -0700 | ended by Andrew (option a); v3 stays the scored set |
| a46d837 | 2026-10-24 12:50 -0700 | sizing README |

- No label sweep, no tag, no method run. Sizing on seeds 10-12; scoring seeds 23-25 not used

### Freeze v4 (tag `freeze-v4` -> b86abef)

| Commit | Time | What |
| :-- | :-- | :-- |
| 72173be | 2026-10-24 16:50 -0700 | C1-C3 proposal from v3 traces (nothing applied) |
| 0a7aadc | 2026-10-25 00:25 -0700 | Andrew approves C1, C2, C3 (a) and the scored v4 run |
| 6a19514 | 2026-10-25 22:08 +0000 (15:08 -0700) | candidate code, prompts `*_v4.md`, `score.py` C3 (a) |
| 8185bcb | 2026-10-25 22:10 +0000 | driver `scored_v4.py` |
| 6b72d6a | 2026-10-25 17:38 -0700 | labels seeds 26-28 |
| d75717b | 2026-10-25 18:03 -0700 | development check on v3 seed 20 (not a score) |
| b86abef | 2026-10-26 01:04 +0000 (18:04 -0700) | proposal file; tag `freeze-v4` (tag object 01:04:30 +0000) |
| ed41bc0 | 2026-10-26 01:18 +0000 | first scored runs: script and remedy tree |
| 8ca122c .. 0044354 | 2026-10-25 18:25 -0700 to 2026-10-26 13:37 -0700 | 306 LLM runs (+95 usage-limit runs set aside) |
| bdc1f94 | 2026-10-26 13:39 -0700 | metrics, README |

- `git diff 6a19514 b86abef` and `d75717b b86abef` on agents/, checker/, config/, measure/: none. `b86abef 0044354`: only `scripts/synth/scored_v4.py` (853da3b, usage-limit set-aside, cap). The README says so
- Run summaries: 408 of 408 freeze-v4; 22 recorded commits, all at or after the tag
- The v4 proposal file was committed with the tag, after the labels and the development check; the changes it records were approved (0a7aadc) and committed (6a19514) before both

### c029 (no tag)

| Commit | Time | What |
| :-- | :-- | :-- |
| 7f48c1a | 2026-11-18 14:17 -0800 | spec 2026-11-18 |
| fa459b7 | 2026-11-20 13:30 -0800 | proposal, injectors, driver |
| 510d287 | 2026-11-20 14:23 -0800 | novel-fault sizes (seeds 50-51) |
| 3142cde | 2026-11-20 23:01 -0800 | `register_frames` remedy gives register_v2 (main) |
| 47ec6e8 | 2026-11-21 10:20 -0800 | option A integrity k (config/integrity_relative_k.yaml) |
| e213ddb | 2026-11-21 10:22 -0800 | c029 register label states switched to register_v2 |
| 5a2e15e, e0d067d | 2026-11-22 14:34, 15:25 -0800 | gate in `Slice.apply_remedy`; zero-base lateral floor |
| 5cc45d5 | 2026-11-22 16:38 -0800 | label rule: a state the tracker failed on twice is no measurement |
| a9445d2 | 2026-11-22 17:07 -0800 | labels (24 rods) |
| e566854 | 2026-11-22 17:09 -0800 | merge main (gate) into wip/compound |
| 960cf04 / 38636ea | 2026-11-22 17:15 / 17:17 -0800 | first scored runs: script and remedy tree |
| bb1242c .. ad8538e | 2026-11-22 17:17 to 21:11 -0800 | 144 LLM runs (+9 usage-limit set aside) |
| 6c4eb7c | 2026-11-22 21:13 -0800 | metrics, README |
| 679a3e9 | 2026-11-23 06:54 -0800 | README: 3 missing-state runs named, metrics with and without (planning, decisions 2026-11-23 06:30) |

### c029b (no tag)

| Commit | Time | What |
| :-- | :-- | :-- |
| (inbox compound item 10) | 2026-11-22, before 20:09 -0800 | supplement decided by Andrew after the c029 labels (20 of 24 decline) and rule-method runs; decisions :270, :282 |
| bd3c2ce | 2026-11-22 20:11 -0800 | proposal, selection rule |
| cbff017, ce0a3cf | 2026-11-22 20:13, 20:14 -0800 | MILD entries; driver; proposal correction (tracker-error states fail), before any render |
| 701442d | 2026-11-23 03:46 -0800 | labels of 48, selected 20 |
| 8b4e232 | 2026-11-23 04:52 -0800 | rule methods (runs record 701442d) |
| ba032f6 | 2026-11-23 06:50 -0800 | missing-state runs set aside and redone (after 2 such runs had ended) |
| 715ec33, d1d857e | 2026-11-23 07:47, 10:47 -0800 | last LLM runs; last tree run |
| 8f40c6d | 2026-11-23 10:49 -0800 | metrics, README |

### c030 (no tag)

| Commit | Time | What |
| :-- | :-- | :-- |
| 6150856 | 2026-11-20 13:37 -0800 | proposal, batches, plant list (seed 1118), 30 views, rule auditor |
| 510d287 | 2026-11-20 14:23 -0800 | first LLM auditor runs (repeat 0) |
| 64c22cc | 2026-11-21 00:12 -0800 | repeat 2, scores, README |

- Prompt `agents/prompts/auditor.md` last changed aa8483a (2026-10-13). Views, plants and batches have one commit each (6150856). 90 results record 8 commits, all CLI 2.1.310, model `claude-opus-5-5`; between them only `measure/record.py` (empty-grid fix, dc1cfe6) and the `score` alias in the driver changed

## Findings

### S3-1 (major): real frame_quality reference includes a window now outside the usable-window rule
- Where: `config/frame_quality_reference.yaml` (`real:` section, comment "Windows inside usable windows of include-yes roots only"); `manifest/root_manifest.csv` change 696784d (2026-10-23 13:31 -0700); `docs/decisions.md:104`, `:153`
- Evidence:
  - The reference (2026-10-13) is the median and lowest over 24 fq-real windows labelled clean, 3 frames each. One of them is 0727_cc7, 8.5-9.5 h (frames at 8.49-9.50 h)
  - 696784d set 0727_cc7 `usable_to_h` from 9.5 to 4.05. The window was inside the rule when used; it is outside it now. The reference was not recomputed and the config comment was not changed; decisions :153 does not mention the reference
  - `s3_fq_reference.py` reproduces the config values from the 24 windows exactly. Without the out-of-rule window (69 values): texture_contrast median 0.0641 (config 0.0648), focus median 0.0285 (config 0.0286); both lowest values unchanged
  - `measure/info.py` gives this reference with every `frame_quality` answer on a real window (`movie: real`), so it is used in testing (real subset, batch runs, integrated run)
  - Effect on the values is small; the rule ("nothing outside these windows is used for ... thresholds, tests") is broken as the manifest now stands
- Fix: recompute the reference from the 23 in-rule clean windows (or record Andrew's decision to keep it), correct the config comment, and add a line to decisions :153 or a new entry

### S3-2 (minor): c029 and c029b ran with register_v2 and the integrity gate, not the freeze v4 remedies the proposal names; the READMEs do not say register_v2
- Where: `docs/proposals/2026-11-18_heldout-compound.md:39` ("Freeze v4 ... No change to prompts, thresholds, remedies or settings"); e213ddb (2026-11-21 10:22 -0800, register label states now register_v2); `results/2026-11-18_heldout_compound/README.md` (run record), `labels.md` (196 states named `register_frames`), `supplement/README.md`; run summaries `freeze_tag: freeze-v4`
- Evidence:
  - The `register_frames` remedy was replaced by register_v2 on main (3142cde, 2026-11-20 23:01 -0800), after the c029 proposal (fa459b7, 13:30 the same day). c029 label states with registration were held, then run as register_v2 (e213ddb). The gate (5a2e15e, e0d067d) was merged before the first method run (e566854)
  - Order is sound: both changes precede the labels (a9445d2) and every method run (960cf04 on). They follow the decisions of 2026-11-20, :246, :262
  - The c029 and c029b READMEs disclose the option A gate but not register_v2. `labels.md` and traces name the state `register_frames`. Every run summary carries `freeze_tag: freeze-v4`, while the remedy set differs from tag `freeze-v4` (`measure/remedies.py` changed in 3142cde, `agents/executors.py` in 5a2e15e, e0d067d)
- Fix: state in both READMEs and the proposal (dated note) that `register_frames` means register_v2 (bound 2 x closure drift) and that the remedy set is freeze v4 plus register_v2 and the gate; note that `freeze_tag` records the prompt freeze, not the remedy code

### S3-3 (minor): c029 README run record gives the wrong commit range and changed files
- Where: `results/2026-11-18_heldout_compound/README.md`, Run record ("Runs record commits 960cf04 to 043f8eb. Across them only `measure/render_compound.py` changed")
- Evidence:
  - 192 summaries record 10 commits: 960cf04, ce643eb, bb1242c, 7596bfc, be925ed, 5c1084d, bd3c2ce, cbff017, 043f8eb and ad8538e (the redone remedy-tree run on drift_jitter s41, 21:11 -0800), outside the stated range
  - `git diff --stat 960cf04 043f8eb`: `measure/render_compound.py`, `scripts/synth/compound_queue.py`, `scripts/synth/heldout_supplement.py` (new). agents/, checker/, config/ and prompts are unchanged across 960cf04 .. ad8538e, so the substance holds
- Fix: "960cf04 to ad8538e"; list the two driver files

### S3-4 (minor): integrated-run windows overlap the real calibration windows; not disclosed
- Where: `results/2026-11-18_integrated_run/README.md` (no mention of calibration); `results/2026-10-25_real_calibration/` (41 measured control windows, 16 roots); `docs/decisions.md:173`
- Evidence:
  - The 19 px/h closure gate is the 95th percentile of the 41 calibration windows. 96 of 1,189 integrated-run windows, on the 16 calibration roots, overlap a calibration window in time (same root, same frames in part).
  - The real subset (16 roots) shares no root with the calibration set (checked, 0 of 16); the integrated run and batches do not keep this separation
  - Not a usable-window breach: all calibration windows are include-yes and in window
- Fix: state in the integrated-run README (known limits) that 96 control windows overlap the calibration frames, and report their closure pass rate separately or excluded

### S3-5 (minor): Lab report 2 overstates held-out separation and does not split the v3-to-v4 gain
- Where: `docs/reports/2026-11-01_lab-report-2.md:96`, `:124` (3ba82e2); source `results/2026-10-25_freeze_v4/README.md` ("Relabelling against agent change")
- Evidence:
  - :96 "Scored seeds were never seen by any prompt or threshold work." C1 (v4 prompt map) was written from v3 traces on scoring seeds 20-22 (72173be), and the v4 development check ran on v3 seed 20 (d75717b). True for each set at its own scoring, not for seeds 20-22 overall
  - :124 gives v3 0.69 beside v4 0.93 and attributes the change to C1-C3. C3 (a) is a label-rule change: it moves the 3 stage_log_missing rods per set from accept_repaired to decline. The v4 README splits the diagnostician change into relabelling +0.06 and agent change with new seeds +0.18. The report gives neither
- Fix: ":96 Each set's seeds were unseen by prompt or threshold work when scored; v4's prompt change was written from v3 traces"; add the relabelling split to :124

### S3-6 (minor): no committed list of the ft2 training traces; its usable-window claim cannot be checked
- Where: `docs/decisions.md:137`, `:140`; `docs/proposals/2026-10-24_real-calibration.md:55`
- Evidence:
  - Decisions :140 states `net2_midline_ft2.pt` was trained on 181 include-yes, in-window traces only (72 July + 109 reviewed pack). No tracked file or result lists the traces by root id and time. The earlier net used 43 out-of-rule traces (:137)
  - The 0727_cc7 window change (696784d, 13:31 -0700) and the ft2 rule (:137, 22:15 -0700) are on the same day; whether any 0727_cc7 trace after 4.05 h was in the 72 July traces cannot be checked from the repo
- Fix: commit a list of ft2 training traces (root id, frame time only) and a check against the manifest

## Checked, no finding
- Tags: `git tag` gives freeze-v2 (5b64897), freeze-v3 (e1e672a, 2026-10-23 18:33:57 -0700), freeze-v4 (b86abef, 2026-10-26 01:04:30 +0000). No freeze-v3.1 tag, as the README states
- Freeze v3 labels (6ebc9db) and tag (e1e672a) before the first scored run (231d418 / 869f130); no agents, checker, config, prompt or scoring change between tag and last run (`git diff --stat e1e672a 8e1888a`, 1 driver file); 408 of 408 summaries freeze-v3
- Freeze v3 CLI: spec said 2.1.302, runs used 2.1.310; disclosed (decisions :132, proposal :138)
- Freeze v3 `v3_bend30_clean_s20` label decision after the label run, before any method run; disclosed (decisions :131, README)
- Freeze v3.1: no method run, no tag, scoring seeds 23-25 unused; disclosed (README, decisions :146)
- Freeze v4: code and prompts (6a19514) and labels (6b72d6a) before the tag; nothing in agents/, checker/, config/, measure/ changed between 6a19514 and the last run (0044354) except the driver; 408 of 408 summaries freeze-v4. Dev check on v3 seed 20 changed nothing (`git diff d75717b b86abef`: empty)
- Freeze v4 caps raised during the run (tracker 300 -> 420, LLM 400 -> 420): Andrew, decisions :188, :190; 95 usage-limit runs are all `error`, no outcome (`runs/usage_limit/`, 95 of 95)
- c029: proposal (fa459b7) before sizing (510d287), labels (a9445d2) before first method run (960cf04); label-rule change 5cc45d5 before labels, disclosed (README Set); sizes follow the proposal rule (`sizing.md`: focus_drift 3, flicker 0.1); 9 usage-limit runs all `error`
- c029 missing-state runs: scored as written, metrics with and without them in README; rule set by planning (decisions :277)
- c029b: proposal (bd3c2ce) before renders; labels and selection (701442d) before every method run (summaries record 701442d or later); between 701442d and 0c71f4b only the two driver files changed (agents, checker, config, measure unchanged); disclosed as designed after c029 (decisions :270, :282)
- c029b missing-state set-aside (ba032f6) came after 2 such runs had ended; both set-aside runs and both redone runs end decline: no effect on any count
- c030: plants, batches, views (6150856) before the first LLM auditor run (510d287); views, plants and batches never changed after; auditor prompt unchanged since 2026-10-13; 1 usage-limit run set aside
- Real calibration: set and rule (fce35c7, 775bc4c, 2aa1b9b) committed before computing; 18 -> 19 px/h by the same rule over more windows (Andrew, decisions :173) before any subset check; subset agent run (e15e01d, 05:44 +0000) after the 19 px/h merge (1730bf3, 05:41 +0000)
- Usable windows, tracked files (`s3_windows_check.py`): 3,964 files, 1,281 distinct root-window items; 1,274 in rule. The 7 others are all in `docs/reviews/2026-10-23_spec-audit/rules.md`, which records the fq-real candidates replaced for the rule (0708_c1, 0714_c3 include no; 0708_m5, 0711_m8, 0714_c8, 0714_m3, 0721_c12 include unsure)
- Usable windows, older trees (`s3_windows_history.py` on 7f48c1a, 62f11b4, 55cede1, 5a4767f, a70ca64^ which still held the real-subset traces): same 7 review items only
- Manifest history: 3 commits; after 2026-10-09 only 696784d (0727_cc7 9.5 -> 4.05 h). Every 0727_cc7 window in batches and the integrated run lies in 0-4.05 h
- fq-real frames (private list, 37 sets): 30 active, 7 replaced (include not yes); of the active, 29 in rule and 1 out (0727_cc7 8.49-9.50 h, S3-1)
- Real subset and calibration roots: disjoint (0 of 16 shared); all calibration roots control and include-yes
