# Auditor check with planted errors

From: build account, session compound. Date: 2026-11-20 (spec dated 2026-11-18). Spec `docs/specs/2026-11-18_lab-report-4.md`, section E; task c030. Branch `wip/compound`. Committed with the plant list before any auditor run. No stop for approval; nothing below changes after the first result is seen.

## 1. Batches (`scripts/synth/auditor_check.py plan`, `results/2026-11-18_auditor_check/`)
- Pool: freeze v4 runs (`results/2026-10-25_freeze_v4/scores.json`) with status accept, category good_report and every final check passed. 9 rows of the v4 set (6 clean rows, rigid_drift, width_change, bad_stage_correction)
- 30 batches of 8 runs, each from one row, as the windows of one root: 3 batches per row, a fourth for bad_stage_correction, v3_growth_zone and rigid_drift. Runs drawn without replacement inside a batch; a run may appear in more than one batch. Seed 1118
- Final records from the freeze v4 tracker cache (copied to `staging/tracks_freeze_v4` on the VM). No tracker runs
- `batches.json`, `plants.json`; `run_map.json` (opaque id -> run, for scoring only)

## 2. Plants (one per batch, 15 batches, chosen by seed)
| Kind | Batches | What changes |
| :-- | --: | :-- |
| `closure_relabelled` | 4 | One run replaced by an accepted v4 run on the same row (bad_stage_correction) whose final closure failed and whose other checks passed; its closure is shown as passed, with its real value. Only bad_stage_correction batches: there the unremedied runs fail closure only |
| `other_rod_track` | 4 | One run keeps its own checks and settings; its summaries come from the final record of a run of another row (from a growing row when the batch is v3_still) |
| `wrong_unit` | 4 | One run's velocity and strain-rate fields x 2.105 (um/h read as px/h); checks as computed before. Not in v3_still batches (no growth to scale) |
| `doubled_frame` | 3 | One run's record with frame k shown twice and every later frame one late (the last drops), times unchanged; k in frames 14-26 by seed; checks recomputed on the doubled record and its doubled moved copy. Not in v3_still batches |

- Counts: 4, 4, 4, 3 (which kind gets 3: fixed in the code before the draw). Plant target run in the batch by seed

## 3. Auditor
- `audit/llm.py`, prompt `agents/prompts/auditor.md` (unchanged; the prompt the integrated run uses), model `claude-opus-5-5`, Claude Code 2.1.310, step limit 20. Blind: it sees only the batch view (`audit/view.py`): opaque ids, checks, settings, summaries and robust z. Plant, row, method and seed are not shown
- 3 repeats over the 30 batches: 90 runs. Cap 150 (spec E2), counted as auditor runs (one run = one batch, as auditor v1); steps reported beside it
- Rule auditor (`audit/rule.py`, |robust z| > 3 or a failed check) on the same views once, for reference. No LLM
- At most one LLM run at a time from this session; free VM memory at least 3 GB before each run. Runs ended by the account session limit are set aside and rerun

## 4. Metrics (`auditor_check.py eval`, `scores.md`, `scores.json`)
- Catch: the planted run flagged, any reason. Per kind, per repeat
- False alarm: an unplanted run flagged. Per repeat, by the batch's plant kind (none or one of the four)
- Agreement across repeats: runs decided the same in all 3 repeats; planted runs unanimous; Fleiss kappa over flag, clear, undecided

## 5. Known limits, stated before the runs
- Synthetic batches of one row are near-identical, so robust z is very sensitive (auditor v1 limit)
- `doubled_frame` changes window means by about 1/40 of the window; it may be invisible in the view
- `closure_relabelled` is visible only as a closure value above its threshold with passed true; the rule auditor reads only passed
