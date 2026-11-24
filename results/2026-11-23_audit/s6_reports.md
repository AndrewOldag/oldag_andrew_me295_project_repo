# Section 6: lab reports 1-3 and the top-level README

Scope: `docs/reports/2026-10-16_lab-report-1.md`, `2026-10-30_lab-report-2.md`, `2026-11-01_lab-report-2.md`, `2026-11-15_lab-report-3.md`, `README.md`, on `wip/audit` (= origin/main plus audit files), 2026-11-23. Read-only. Script: `scripts/s6_paths.py` (every backticked path in the five files checked for existence; no file written). Entry points run with `--help` only (31 scripts, all exit 0, under 30 s each); `pytest --collect-only` (no cache, no bytecode written). No agent call, no tracker, no network.

Which Lab report 2 was submitted: `2026-11-01_lab-report-2.md`. Evidence: commit 71f2a3f "rewritten in the course template ... due Sun 1 Nov"; Lab report 3:172 counts commits "since Lab report 2 (`f04a286`)", which is the commit stated in the 11-01 file (:81, :166). The 10-30 file is the earlier draft (last edit 0060c20, 2026-10-25); it still holds open `[ANDREW]` marks at :57 and :90.

Counts: blocker 4, major 0, minor 8.

Cross-references, not repeated: S2-3 (LR2 draft :55 "about 10 times"); S3-5 (LR2 :96 "scored seeds never seen", :124 0.69 vs 0.93); S1-3 / S1-4 (biology values in tracked traces); S3-1 (frame-quality reference, LR1 :26); S5-2 (README :143 cap 1,300).

## Lab report 1 (2026-10-16)

No new finding. The report has a dated correction block (:187-192, spec audit 2026-10-24) that already covers the root count, the 12 Oct test count, frames pulled and mean steps.

## Lab report 2, draft (2026-10-30, not submitted)

### S6-1 (minor) Superseded draft kept without a note
- Where: `docs/reports/2026-10-30_lab-report-2.md:1`, :57, :90
- Evidence: the file has no line saying it was replaced by `2026-11-01_lab-report-2.md`. It keeps two open `[ANDREW]` marks (:57 real subset, :90 related work) and the plan dates of 25 Oct. A reader of `docs/reports/` sees two Lab report 2 files
- Fix: add one line at the top: draft, superseded by `2026-11-01_lab-report-2.md` (submitted); or move it under a drafts folder

## Lab report 2, submitted (2026-11-01)

### S6-2 (blocker) "The fixed script accepts all 18 decline rods"
- Where: `docs/reports/2026-11-01_lab-report-2.md:44`
- Evidence: freeze v4 has 24 decline rods (`results/2026-10-25_freeze_v4/README.md:18`, per-row table :60-67: script 0 of 3 on all 8 decline rows). The script accepts all 24. 18 is its false-accept count (README:26). The sentence mixes the two. Lab report 3:27 states it correctly ("18 false accepts of 51")
- Fix: "it accepts all 24 decline rods; 18 are false accepts"

### S6-3 (blocker) "Every result folder has a README with its command"
- Where: `docs/reports/2026-11-01_lab-report-2.md:169`
- Evidence: at `f04a286` 3 of the results folders had no README: `results/2026-10-09_demo_diagnostician/`, `results/2026-10-12_heldout_faults/`, `results/2026-10-25_full_batch_2/`. At 71ccf6c (Lab report 3) and on origin/main the first two still have none (`git ls-tree` per folder)
- Fix: add a README (command, date, what the files are) to the two folders, or correct the sentence

### S6-4 (blocker) Diagnostician stopping rule names a `finish` action it does not have
- Where: `docs/reports/2026-11-01_lab-report-2.md:64` ("stops when it emits `finish` with an outcome"); `docs/reports/2026-11-15_lab-report-3.md:39` ("`finish` with an outcome")
- Evidence: the diagnostician's actions are `request_info`, `apply_remedy`, `accept`, `decline`; `accept` and `decline` are terminal (`agents/actions.py:152-160`). The same at f04a286; `git log -S'Action("finish"' -- agents/actions.py` finds nothing. `finish` is a dispatcher action (`agents/dispatcher.py:376`). Lab report 3's own example trace (:68) ends in `accept`
- Fix: "stops on `accept` or `decline`, or at the step limit"

### S6-5 (minor) First-batch counts predate the not-computable rule the report cites
- Where: `docs/reports/2026-11-01_lab-report-2.md:78`, :84
- Evidence: :84 gives 114 accepted, 9 declined. :78 says the rule "now declines" the 4 windows with no computable closure (Andrew, 2026-10-26). The re-score was applied on 2026-11-02 (51486cf): 110 accepted, 13 declined (`results/2026-10-25_full_batch_1_agents/README.md`, Outcome). Lab report 3:75 has the re-scored counts. True at writing; the two lines of Lab report 2 disagree with each other
- Fix: none needed for a submitted report beyond a dated correction line, as in Lab report 1

### S6-6 (minor) Test counts without a log record at the stated commit
- Where: `docs/reports/2026-11-01_lab-report-2.md:81`, :185 (324 passed, 3 skipped, 50 s, at f04a286); `docs/reports/2026-11-15_lab-report-3.md:90`, :186 (382 passed, 2 skipped)
- Evidence: "324 passed" occurs in no tracked file other than the report (`git log --all -S"324 passed"`: only 71f2a3f, the report). "382 passed, 2 skipped" is the real-calib entry of 2026-11-05 (`docs/running_log.md:848`, commit ed97240 era). Lab report 3 is at 71ccf6c (2026-11-14); `def test_` count rose from 277 (2026-11-05) to 295 at 71ccf6c (c026 alone added 15 tests, log :854). No suite run at 71ccf6c is logged. Current tree: 489 tests collected, 0 collection errors
- Fix: give the date and commit of each count, or run the suite at the report commit and log it

### S6-7 (minor) "The checker is what makes the agent work"
- Where: `docs/reports/2026-11-01_lab-report-2.md:121`; same claim `docs/reports/2026-11-15_lab-report-3.md:27`, :47
- Evidence: the single-agent baseline differs from the diagnostician in more than the checker output: one prompt sentence changed, remedy results show the change only, and no roll back (`README.md:45`, `docs/proposals/2026-10-12_single-agent-baseline.md`). 66 of its 153 runs end at the step limit (not reported), which drives most of the 0.63. The comparison supports "the same model without checker output and roll back"; it does not isolate the checker
- Fix: name all differences in the sentence, or state it as "without checker output (and the roll back that depends on it)"

### S6-8 (minor) Midline-net comparison in a course report
- Where: `docs/reports/2026-11-01_lab-report-2.md:147`, :156 ("The base net was off the root on 24 of 28")
- Evidence: the numbers match `results/2026-10-23_autotrace/README.md:42-44`. CLAUDE.md: tracker comparisons belong to other lab work. The base-vs-fine-tuned net result is a comparison of tracking tools, not agent behaviour. The annotation loop itself (AI-prepared drafts, human review) is in scope
- Fix: Andrew decides whether the net comparison stays; if not, keep the held-out error of the net used and drop the base-net figure

## Lab report 3 (2026-11-15)

### S6-9 (blocker) Four counts off by one item
- Where and evidence:
  - :22 "17 of the full-text papers", :126 "17 papers": the index holds 17 files, 16 papers and one supplement (`results/2026-11-02_rag/README.md:6`)
  - :146 "34 batch-2 windows ... Tracker `arange` error": 33 are `arange`; 0721_m5 w0-2 failed on the logistic fit (`results/2026-10-25_full_batch_2/README.md:17`, same text at 71ccf6c)
  - :76 "Batch 2 ... (90 roots, 1,063 windows)": batch 2 is 91 roots and 1,063 windows; 90 finished (README:1, :31; top README:101 says 91)
  - :13 "All 102 include-yes roots through the checker except one (101 roots, 1,189 windows)": 1,189 includes the 2 windows of 0727_cc7, which were not run (:169 says so); windows checked are 1,187 (126 + 1,061), of which 37 ended in a tracker error before any check
- Fix: "17 files (16 papers, one supplement)"; "33 `arange`, 1 logistic-fit failure"; "91 roots, 90 finished"; "101 roots, 1,187 windows run (37 tracker errors)"

### S6-10 (minor) Demo commands need git-ignored caches and overwrite tracked results
- Where: `docs/reports/2026-11-15_lab-report-3.md:92`
- Evidence: `scripts/dispatcher_eval.py report` reads `staging/c023/batches/` (`cmd_report`, :220-221) and writes `results/2026-11-02_dispatcher_eval/`; `scripts/rag.py report` reads `staging/rag/runs/` and `staging/rag/retrieval.json` (`cmd_report`, :169-177) and writes `results/2026-11-02_rag/`. From a clean clone both fail; with the caches they rewrite tracked files rather than print. The report says "print the D2 tables from cached runs"
- Fix: say they need the run caches (not in the repo) and regenerate the results folder; for a clean clone point to the committed `tables.md` / `metrics.json`

## README.md

### S6-11 (minor) Sections describe compute locations that later rules replaced, without a date
- Where: `README.md:29-34` (sweeps on "the shared tracker machine", `sweep.py` run on it directly); :83 ("task c029, VM only", tracker on this machine); :94-95 (`demo_dispatcher.py`: "4 lab-server workers", "lab-server worker limit and load rule"; `config/dispatcher.yaml:9-10`)
- Evidence: since 2026-11-04 the lab server is storage only (CLAUDE.md; spec `2026-11-04_storage-only-server.md`); `RemoteRunner.sweep_start` refuses a storage-only host (236711b). Since spec 2026-11-20 no tracker run on the VM (README:86 says so, but :83 still heads the section "VM only"). The sections read as current run steps. The fake-queue lab-server limits are simulation settings, which the README does not say
- Fix: mark each section with the date and the rule that replaced it ("historical: lab server storage only since 2026-11-04"; "superseded by cluster CPU, spec 2026-11-20"); say the dispatcher's lab-server worker limit is a fake-queue setting

### S6-12 (minor) Stale or missing run instructions
- Where and evidence:
  - :160 "Run instructions for the full system will be added as it is built": the integrated run is documented at :131-143
  - :128 "`submit` sends no register_frames job until `register_v2` is on main": `register_v2` is on main; the code holds only v1 registration jobs, permanently (`scripts/retrack_queue.py:54-55`, `is_register_v1` :91-93)
  - :37 "branch `heldout/faults` until the freeze": the branch was deleted from GitHub on 2026-10-30 (`docs/decisions.md:198`); it is merged into main
  - Scripts that produce tracked results but have no README run step: `scripts/batch2_agents.py` (c026, Lab report 3 :77), `scripts/synth/heldout_supplement.py` (c029b), `scripts/synth/register_v2_regression.py` and `scripts/integrity_thresholds.py` (registration fix), `scripts/check_after_fix.py` (arange fix). Their commands are in the results READMEs only
- Fix: delete :160; reword :128 ("v1 registration jobs are never submitted; register_v2 replaces them"); drop the branch note at :37; add one line per missing driver pointing to its results README

## Checked, no finding

### Paths, commands, entry points
- Backticked repo paths in the five files (`s6_paths.py`): all exist, except `config/compute_budget.yaml` (README:95 says "absent = 0"; `config/dispatcher.yaml:20` agrees), `docs/agents/status/supervisor.md` (on branch `ops/heartbeat`, as README:154 says) and branch names
- Figures `docs/reports/figures/lr2_design.png`, `lr3_design.png`: exist
- Every script and test file named in README: exists (54 script paths, 19 test files)
- `--help` on 31 argparse entry points: exit 0. Every subcommand and flag named in README exists: run_batch (`--seeds --moved-too --fault --width-kappa-inv --rotation-deg`), make_rod (all 10 held-out and development faults, `--size`), demo_slice (`--size --out --replay --no-agent --runner field`), fix_sweep, heldout_sweep, baselines, eval_baselines, scored_v1, heldout_labels, scored_v3, scored_v31 (`second-root`), v4_replay_check, scored_v4 (`dev-check dev-report decompose`), auditor_v1 (`--repeat`), heldout_compound (`render`), compound_queue (`--equivalence`), auditor_check, demo_dispatcher, dispatcher_eval (`run --methods script`), real_slice (`--windows --config` multiple, `--moved-span --min-free-gb --cached-only --dispatcher --no-agent --audit-only`), real_track, real_subset_report, full_batch (`summary --batch 2`), full_batch_agents_report, rag (`build gold retrieval run report`), retrack_queue (`seed jobs submit fetch`, `--wave --jobs --paused`), run_all (`windows fetch run tree report`, `--llm-cap --demo --roots`), board (`--html`). `real_subset_agreement.py` takes run folders from `sys.argv`
- Defaults: real_slice root 0708_m12, 4-6 h, dispatcher agent (README:98, :110); run_all `--llm-cap` 900 (README:143; `scripts/run_all.py:49`)
- Setup: `environment.yml` name `me295`, Python 3.12, `pypdf`, `fastembed`, `paramiko` listed (README:106 needs the first two); `config/models.yaml` pins `claude-opus-5-5` and 2.1.310 (LR2:67, LR3:41); launcher refuses another version (`agents/launcher.py:85-86`); `check_cli.py` prints version, login, model and `OK`, exits with `FAIL:` as README:16 says; `tests/test_ops.py` skips without bash (README:17); `scripts/hooks/install.sh` exists
- `pytest --collect-only`: 489 tests, 0 collection errors

### Commits and counts
- All 7-hex commit hashes in the five files resolve and are ancestors of origin/main
- LR1: 142 commits to 4ab1c32; per day 23 / 26 / 15 / 37 / 29 / 12
- LR2 draft: 502 at 8de4d77, 360 since 4ab1c32, 330 since 2170ca5. LR2: 699 at f04a286, 557 since 4ab1c32. LR3: 828 at 71ccf6c, 129 since f04a286

### Numbers against results folders
- LR1: schema test (`results/2026-10-09_action_schema/`); checker 70 runs, 0.40-0.44 %/h RMS vs 43 %/h (`2026-10-10_checker_synthetic/`); 354 runs (`2026-10-10_repair_criteria/`); first diagnostician runs 1 of 5, 37 steps, 159k / 18k, 207 s (`2026-10-11c_world_smoothing_freeze/`); 66 runs (`2026-10-12_freeze_v2/`); 84 held-out label runs (`2026-10-12b_heldout_labels/`); scored v1 dev table 4 x 4 (`2026-10-12b_scored_v1/table_dev.md`); auditor v1 7, 5, 5 of 11 and 24 runs (`2026-10-13_auditor_v1/`); thresholds 2.0 / 1.0 / 3.25 (`config/checker_thresholds.yaml`); manifest 123 rows, 102 include yes
- LR2: freeze v4 table, decline accuracy, false accepts 18 / 2 / 0 / 0.3, unanimity 46 and 34 of 51, kappa 0.887 and 0.626, 66 of 153 at the step limit (`results/2026-10-25_freeze_v4/README.md`; recomputed in S4); v3 306 LLM runs, 0 harness errors, 102 of 102 (`2026-10-23_freeze_v3/README.md:44, :82`); real closure 19 px/h, 41 windows, median 3.60 (`2026-10-25_real_calibration/README.md:8, :13`); 2.105 um/px (decisions:170); autotrace 140 frames, 84 folders, 28 held out from 16 roots, 112 reviewed, 72 / 40, 181 = 72 + 109, 1 h 23 min, $0.234, 2.4 / 6.4 px, 24 of 28 (`2026-10-23_autotrace/README.md`); subset 43 / 5, 2 flagged, 3 of 5 (`2026-10-25_real_subset/README.md:22-23, :67-69`); batch-2 interim 437 / 371 / 49 / 17 (status commit fed24e3); cluster tracks 2.6e-7 px under the 1e-6 limit (decisions:193); spec audit 71 findings, 13 / 17 / 2 / 39, check 17 + 10 findings + 10 citations = 37, 0 not reproduced (`docs/reviews/2026-10-23_spec-audit/`); step limits 4 / 8 / 8 / 20 (`config/models.yaml:20-32`)
- LR3: trace example (closure 8.23 -> 0.31, 4 calls, 18,053 / 2,520 tokens, 28.0 s, confidence 0.85; `diagnostician_v3_growth_zone_rigid_drift_z0.5_s26_r0`); low-texture rods: 9 of 9 decline after disk radius 14 -> 21 -> 28 px; batch 1 110 / 13 / 3, 9 + 4, 8 + 1, registration 5 / 1 / 4, 34 calls; batch 2 925 / 84 / 18 / 34 / 2, $7.24; batch-2 tree 38 / 9 / 28 / 1 / 46, kept 5 / 2 / 2, 142 / 14 / 127, 148 retracks, 21 min, $7.37, 19.4 -> 20,125 px/h (`2026-11-12_batch2_agents/README.md`); dispatcher table 5 scenarios x 4 columns, S4 36 vs 24 jobs (`2026-11-02_dispatcher_eval/tables.md`, README:35); RAG 693 chunks, 11 / 19 and 8 / 14, 11 / 12 / 11, 0.85-0.90, 5 of 5, post hoc 17-18 of 20 (`2026-11-02_rag/README.md`); D3 rows second_root 8 of 9, fast_rotation 6, midline_jitter 7, displacement 7 of 9, tree second_root 0 and partial_occlusion 1 of 3 (freeze v4 per-row table); Argon recompute 0 disagreements (`docs/reviews/2026-11-03_argon-v4-recompute/review.md:23`); proposals committed before first results (dispatcher eval 10d74c1 before 855a697; RAG b69a95a before d324f76; batch-2 f2ec5be before fae4d18)

### Scope (CLAUDE.md)
- Stress, stiffness, constitutive law, turgor, modulus: not claimed in any of the five files (only "no stress, stiffness or constitutive law" scope lines)
- Biology values: none in the reports or README. Real-window numbers are outcomes, counts and check values (closure, rigid invariance, plane sections), which LR2:163 declares as the published set. The condition comparison of the auditor is described as behaviour, values withheld
- Tracker modes: LR1:35 reports coupled vs uncoupled on synthetic rods as data, with "no claim about tracker modes is made" (allowed, Andrew 2026-10-11). Related-work notes state no tool ranking (LR1:115)
