# Spec audit 2026-10-23: evaluation

Reviewer 6 of `docs/specs/2026-10-23_spec-audit.md`. Worktree `wip/spec-audit` (origin/main plus audit files). Read-only. Replay only: one recomputation from `results/2026-10-12b_scored_v1/scores.json` (160 records), no agent call, no tracker run, no server access.

No STOP item. The literature network location is now recorded in the private paths file. No real-movie frame is used in any scored result checked here.

## 1. Findings

### evaluation-1: An all-decline policy beats every method on the held-out set (12 of 15 correct)
- Ours: `scripts/synth/scored_v1.py:69` (`CORRECT = {"repairable": "good_report", "not repairable": "correct_decline"}`), `:265`; `measure/score.py:93-99`; `results/2026-10-12b_scored_v1/scores.json`; table in `docs/reports/2026-10-16_lab-report-1.md:44-49`
- Source: spec item Reviewers 6, "can an agent score well by declining everything"
- Evidence: replayed the score with every run set to `decline`, using the labels in `scores.json`. Dev, 25 rods (15 repairable, 10 not repairable): all-decline 10 correct, 0 false accepts, 15 unnecessary declines. Held-out, 15 rods (3 repairable, 12 not repairable): all-decline 12 correct, 0 false accepts, 3 unnecessary declines. Reported held-out correct: diagnostician 11, remedy tree 9, single agent 7, script 3. Both sets, 40 rods: all-decline 22; diagnostician 35, remedy tree 33, single agent 18, script 13. All-decline scores above the single agent on both sets combined
- Evidence: 4 of 5 held-out faults are labelled not repairable (`results/2026-10-12b_heldout_labels/`, commit 1e5e2c2). The held-out repairable class is one fault (bad_stage_correction, 3 rods)
- Severity: would change a design choice
- Frozen item: yes (held-out fault sizes and labels, approved 2026-10-12; scoring seeds, freeze v2 section 7)
- Andrew: accepted, handled (freeze v3)

### evaluation-2: Abstention precision and recall are listed as metrics but not defined or computed anywhere
- Ours: `docs/context/project_summary.md:33`; `docs/reports/2026-10-16_lab-report-1.md:165`; draft `docs/reports/2026-10-30_lab-report-2.md:46` on `wip/lab-report-2`; `measure/score.py:57` (five outcome categories only); `scripts/synth/scored_v1.py:69,265` (single `correct` flag)
- Source: spec item Reviewers 6, "are abstention precision and recall defined so that they penalise that"
- Evidence: grep for `precision`, `recall`, `coverage`, `abstain` over code, config and results: no definition and no computed value. The only scored aggregate is `correct` (good_report on repairable, correct_decline on not repairable)
- Evidence: computed here, with precision = correct_decline / declines and recall = correct_decline / not-repairable rods (both sets, 40 rods each):

| Method | Declines | Abstention precision | Abstention recall | Accepted (coverage) | False accepts / accepted | not_reported |
| :-- | --: | :-- | :-- | --: | :-- | --: |
| script | 0 | - | 0/22 | 40 | 22/40 | 0 |
| remedy_tree | 17 | 16/17 | 16/22 | 23 | 3/23 | 0 |
| diagnostician | 19 | 18/19 | 18/22 | 20 | 0/20 | 1 |
| single_agent | 10 | 9/10 | 9/22 | 12 | 0/12 | 18 |
| all-decline | 40 | 22/40 | 22/22 | 0 | - | 0 |

- Evidence: under these definitions precision penalises all-decline (22/40; held-out alone 12/15), recall does not (22/22). `not_reported` (step limit) is neither a decline nor an accept and falls out of both; it is 18 of 40 single-agent runs
- Evidence: 9 held-out second_root runs and 5 dev script midline_jitter runs are good reports on not-repairable rods; they count as neither correct nor false accept (`results/2026-10-12b_scored_v1/README.md`), so they lower every method's `correct` and do not lower all-decline's
- Severity: would change a design choice
- Frozen item: no (no metric section in `docs/proposals/2026-10-12_freeze-v2.md`)
- Andrew: accepted, handled (freeze v3)

### evaluation-3: No scored rod has a correct outcome of accept without a remedy
- Ours: `scripts/synth/scored_v1.py:10-11,78-80` (dev: five faults x seeds 1-5; held-out: five faults x seeds 0-2); `docs/proposals/2026-10-12_heldout-faults.md:57` (held-out sizes chosen so the checker fails 3 of 3 seeds)
- Source: spec item Reviewers 6 (decline-everything check); `docs/context/project_summary.md:29` (fixed non-growing roots as truth)
- Evidence: all 40 scored rods carry an injected fault; none is a clean rod. Unnecessary declines of a clean measurement are not measured for any method. Fixed non-growing roots are listed as remaining (`docs/reports/2026-10-16_lab-report-1.md:67`) and not run
- Severity: would change a design choice
- Frozen item: yes (scoring seeds and set, freeze v2 section 7)
- Andrew: accepted, handled (freeze v3 / v3.1)

### evaluation-4: Held-out fault sizes were set on the same seeds that are scored
- Ours: `docs/proposals/2026-10-12_heldout-faults.md:32,57`; `results/2026-10-12_heldout_faults/checker_sizes.md:1`; `scripts/synth/scored_v1.py:11`
- Source: spec item Reviewers 6, "are any thresholds or prompts set on rods later scored"
- Evidence: sizes are "the smallest tested size at which the checker fails on 3 of 3 seeds", seeds 0-2 (commit fe7dda1, 2026-10-12 20:19). Held-out scoring uses seeds 0-2 at those sizes (commit f2b727e, 2026-10-13 00:00). No agent was run on them before sizing; the sizing used the checker only. Every held-out rod therefore fails the checker by construction
- Severity: record only
- Frozen item: yes (held-out sizes, approved 2026-10-12)
- Andrew: accepted, no action

### evaluation-5: Checker thresholds and the P5 frame-quality reference come from clean rods that share the random seed of scored rods
- Ours: `measure/render.py:134` (`rng = np.random.default_rng(movie.seed)`, texture and noise from it); `scripts/synth/scored_v1.py:80` (scored rods are case `growth_zone`); `docs/proposals/2026-10-12_freeze-v2.md:51,59` (basis: 15 clean rods, growth_zone, bending, rigid_translation, seeds 0-4)
- Source: spec item Reviewers 6, thresholds set on rods later scored
- Evidence: clean growth_zone seeds 1-4 (threshold basis, commit aebc749, 2026-10-10) and dev scored rods growth_zone + fault seeds 1-4 use the same seed for the texture generator; held-out scored seeds 0-2 likewise. The fault changes the rod; the base texture realisation is shared. The thresholds were set on the clean versions only, before any fault rod was scored
- Severity: record only
- Frozen item: yes (checker thresholds; P5 reference, freeze v2 sections 3 and 5)
- Andrew: accepted, no action

### evaluation-6: Auditor prompt tuned on the dev batches whose auditor results are then reported
- Ours: `results/2026-10-13_auditor_v1/README.md:17,39-44`; commits b1055da, c708fb0, aa8483a, 23d93ef (2026-10-13 21:36-21:45)
- Source: spec item Reviewers 6, prompts set on rods later scored
- Evidence: 3 prompt rounds on the 4 dev batches (dev seeds 1-5 scored records). Dev table reports all 3 rounds; diagnostician good reports flagged 7, 5, 0 of 15 over rounds 1-3. Held-out prompt fixed at aa8483a before the 12 held-out runs (46a9d6f). Lab report 1 (`:53`) reports held-out only
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### evaluation-7: Single-agent prompt keeps rules that need checker results the single agent cannot get
- Ours: `agents/prompts/single_agent.md:10` ("You will then see the re-checked result"), `:11` ("accept only when the checks pass"), `:16`, `:18`; `agents/executors.py:143-154` (BlindSlice `apply_remedy` returns `rerun`, `change`, `settings_left` only); `docs/decisions.md:95`
- Source: spec item Reviewers 6, baselines given the same information; CLAUDE.md Baselines line
- Evidence: the decision of 2026-10-12 keeps these rules on purpose. The single agent ended at the step limit in 13 of 25 dev and 5 of 15 held-out runs (`results/2026-10-12b_scored_v1/README.md`); diagnostician 1 of 40. Whether the step limits come from missing information or from rules it cannot satisfy is not separated by any run
- Severity: would change a design choice
- Frozen item: no (single-agent definition, `docs/proposals/2026-10-12_single-agent-baseline.md`, not part of freeze v2)
- Andrew: accepted, known limit (report)

### evaluation-8: The single-agent baseline measures the checker, not one agent against several
- Ours: `docs/proposals/2026-10-12_single-agent-baseline.md:6` ("Measures what the deterministic checker adds"); `CLAUDE.md:25` ("single-agent version"); `docs/context/project_summary.md:14` (why several agents)
- Source: spec item Reviewers 6, baselines; CLAUDE.md Summary ("evaluated against scripted and single-agent baselines")
- Evidence: the single agent is the diagnostician with checker output removed. No baseline has one agent doing the dispatcher, diagnostician and auditor jobs. The dispatcher is not built (`docs/reports/2026-10-16_lab-report-1.md:66`). No result compares the multi-agent split against a single agent with the same information
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, known limit (report)

### evaluation-9: Repeated-run agreement not measured; no statistic or repeat count defined
- Ours: `docs/context/project_summary.md:30,33`; `CLAUDE.md:26`; `results/2026-10-12b_scored_v1/scores.json` (160 records, one per method x rod); `results/2026-10-13_auditor_v1/README.md:18,32-34`; draft `docs/reports/2026-10-30_lab-report-2.md:46`
- Source: spec item Reviewers 6, repeated-run agreement; `docs/context/course/Project-Guideline.md:23` ("Test reliability across repeated runs")
- Evidence: summary places repeated runs on the 12-16 root real subset and names no statistic and no repeat count. Diagnostician and single agent: 1 run per rod; no repeats. LLM auditor: 3 repeats per held-out batch; counts reported per repeat (false accepts 14, 14, 14 of 15; good reports 7, 5, 5 of 11), no agreement statistic. No real-movie run exists
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, handled (freeze v3)

### evaluation-10: `paper_digests.md` has no agent-system digests; selective classification and ReAct are cited without a digest
- Ours: `docs/context/literature/paper_digests.md` (26 headings, all root kinematics, lines 10-290); `docs/reports/2026-10-16_lab-report-1.md:100-112` (Wei 2025, Yao 2023, Geifman & El-Yaniv 2017)
- Source: spec Inputs line ("26 papers, includes the agent-systems papers"); brief Sources line
- Evidence: grep for Geifman, ReAct, Yao, Wei, selective, agent in `docs/context/literature/`: 0 hits. The literature network has no key for these papers (checked by key in its paper list). No paper location exists to check the lab report 1 claims against, so no literature finding on the metric design is made
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### evaluation-11: Lab guideline names five lab reports; no date for a fifth exists in the repo
- Ours: `CLAUDE.md` Dates (lab reports 1-4 only); `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md` A2 ("Plan to Lab reports 3-5 with dates")
- Source: `docs/context/course/Lab-Guideline.md:3` ("each of the five Lab Reports"); Lab Report 2 goal ("Lab Reports 3-5 will track progress")
- Evidence: the guideline lists reports 1-4 with dates; no Lab Report 5 section and no date. Needs Andrew to check the syllabus
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action (syllabus lists reports 1-4)

## 2. Course deliverables (as of 2026-10-23)

| Deliverable | Due | Required content | Exists (file) | Gap |
| :-- | :-- | :-- | :-- | :-- |
| Lab report 1 | Sun 18 Oct | Related-work note, repo and environment, running log, draft proposal | `docs/reports/2026-10-16_lab-report-1.md` (main) | None found |
| Lab report 2 | Fri 30 Oct | 1-page proposal (commitment point); updated related-work note; repo and log maintained | Draft `docs/reports/2026-10-30_lab-report-2.md` on `wip/lab-report-2` (e028880), 8 `[ANDREW]` marks; not on main | Andrew's marks; merge. Metrics in it (`:46`) include two not defined (evaluation-2, -9) |
| Lab report 3 | Fri 13 Nov | Smallest slice running end to end; progress report; next steps | None. Dispatcher proposal only, `wip/dispatcher` (23443d2), awaiting approval | Dispatcher code; tracker timing and cost estimate; no real movie through the pipeline |
| Lab report 4 | Mon 23 Nov | Integrated end-to-end run on own problem; honest failure modes | None | Integrated run (dispatcher -> tracker -> checker -> diagnostician -> auditor) on real roots; failure-mode list |
| Lab report 5 | Not in repo | Not stated in course files | None | Date and content unknown (evaluation-11) |
| Final presentation | Wed 2 Dec | PowerPoint: problem, workflow, reliability-audit evidence, results, limits, next steps; slides submitted before | None | Slides; reliability-audit evidence (repeated runs, evaluation-9) |
| Final report | Wed 9 Dec | 4-page IEEE paper: problem, context, architecture, evaluation and baseline, results, reliability, limits and safety, reproducibility, conclusions; AI Use Declaration appendix | None. `CLAUDE.md:12` says the declaration is written from the log | Paper; AI Use Declaration |
| Final repository | Wed 9 Dec | Public repo; source, README, reproducible environment (requirements.txt or Docker), pinned model ID, run steps, configuration, tests or eval scripts; audit artifacts (prompts, traces, outputs, provenance) | `README.md`, `environment.yml`, `envs/qb.yml`, `config/models.yaml` (model and Claude Code pinned), `tests/`, `scripts/synth/`, `results/`, `agents/prompts/` | Environment is conda `environment.yml`, not requirements.txt or Docker; public status not checked here; tracker code is in a separate private repository (`CLAUDE.md` Where things are), so the tracking step cannot be run from this repo |
| Course minimum: repeated-run reliability | Final | Reliability across repeated runs | Auditor 3 repeats on held-out only | Diagnostician and baselines: none (evaluation-9) |
| Course minimum: human approval before consequential action | Final | Approval points in the workflow | Budget approval in CLAUDE.md; not in code (dispatcher not built) | Approval point implemented and tested |

## 3. Checked, no finding
- Baseline step limits: remedy tree uses the diagnostician's `step_limit` from config (`scripts/synth/scored_v1.py:169`, `agents/baselines.py:87-92`); single agent has its own entry equal to the diagnostician's (`config/models.yaml`, `single_agent`: effort high, max_turns 3, step_limit 8). Script runs 1 step by definition
- Baseline information: remedy tree sees check pass or fail only, no values, no `request_info` (`agents/baselines.py:33-36`, `docs/proposals/2026-10-12_remedy-tree.md:11`), documented. All methods act on the same `Slice` code, rods and runner (`agents/executors.py`, `scripts/synth/scored_v1.py:12-13`)
- Remedy tree written before any run: proposal ea95149 (2026-10-12 19:59), code 720f7da (20:02), dev seeds 0-2 results 9a2cc03 (20:17). `agents/baselines.py` has no later commit
- Diagnostician prompt and scored seeds: P1-P5 written from seed 0 traces only (`docs/proposals/2026-10-12_diagnostician-misses.md:5,165`, commit 55edff8, 20:02), before the seeds 1-2 baseline results (9a2cc03, 20:17); applied as written at 5b896cb (20:32). No diagnostician run on seeds 1-5 before freeze-v2 tag (22:16) and the scored runs (f2b727e)
- Flank tolerance 1.00 %/h: derived from clean bent rods on 2026-10-11 (8177f96), recorded 9ef68f1 after baseline results; basis is clean rods, not scored rods (`config/scoring_tolerance.yaml`)
- Dev labels for seeds 3-5 from tracker-only runs before any prompt change (commit 2a5baa5, `config/scoring_seeds.yaml`)
- Held-out labels committed (1e5e2c2, 22:38) before any agent run on held-out (f2b727e)
- Rule auditor z cutoff: marked fixed at adbeb5f (2026-10-14 13:20 -0700), after held-out auditor runs (46a9d6f, 2026-10-13 21:58 -0700); `audit/rule.py` diff is a docstring change only, `Z_CUTOFF = 3.0` before and after
- Scoring code never shown to agents: `measure/score.py:1,64` (docstrings); not imported by `agents/`
