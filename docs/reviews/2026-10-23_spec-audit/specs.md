# Spec audit, reviewer `specs`: spec and proposal conformance

Spec: `docs/specs/2026-10-23_spec-audit.md`, Reviewers item 1. Read-only. Worked from `origin/main` at c730662 (this worktree is an earlier `main` plus audit files; the two later `main` commits change only the dispatcher spec, its inbox, the coordinator status and task c010).

Method:
- Each spec in `docs/specs/` and each proposal in `docs/proposals/` read in full; items checked against `docs/running_log.md`, `docs/decisions.md`, `git log --all`, tags, `tasks/`, `docs/agents/`, `results/` and the code
- Tests re-run (agents env, under 1 min per batch): 174 of the 203 collected tests, all files except `tests/test_pre_push_check.py`. 173 passed, 1 failed (`tests/test_board.py::test_research_rows_never_in_tracked_files`, see specs-3)
- `scripts/hooks/pre_push_check.py --commits origin/main..origin/status/gate2`: 11 commits, 0 hits
- No server access, no tracker runs, no agent calls, no PDF opened

No stop condition of the spec was hit by this reviewer.

## 1. Table

States: met, partial, not met, changed by decision, not shown, in progress.

| Spec or proposal | Item | State | Evidence |
| :-- | :-- | :-- | :-- |
| spec 2026-10-09 checker and synthetic rods | 1 Housekeeping (`wip/orchestrator` gone) | met | running_log.md:76 |
| spec 2026-10-09 | 2 Measurement record, doc and two load tests | met | `docs/context/measurement_record.md`; `tests/test_record_tracker.py:51`, `tests/test_synth_field.py:56`; 6547010, 7e339e3 |
| spec 2026-10-09 | 3 Field-level cases (six) | met | `measure/rod.py:253-280`; `tests/test_synth_field.py:36` (integrated strain rate = tip velocity; re-run, pass) |
| spec 2026-10-09 | 3 Image level, five dev injectors only | met | `measure/render.py:22`; 4337285 |
| spec 2026-10-09 | 3 Clean image-level error reported | met | `results/2026-10-10_checker_synthetic/README.md:18` |
| spec 2026-10-09 | 4 Three checks, output per check | met | `checker/checks.py`; `tests/test_checker.py:42` |
| spec 2026-10-09 | 4 Definitions in decisions before coding | partial | decisions.md:14-19; running_log.md:81 "worked out alongside the code" (specs-21) |
| spec 2026-10-09 | 4 Thresholds proposed, then approved | met | running_log.md:83; decisions.md:20 |
| spec 2026-10-09 | 4 No-LLM import test; field cases give expected outcome | met | `tests/test_checker.py:19`, `:34` (re-run, pass) |
| spec 2026-10-09 | 5 `request_info`, `apply_remedy`, remedy table, runner in two forms | met | `measure/info.py`, `agents/executors.py`, decisions.md:26-41; c77ff40 |
| spec 2026-10-09 | 5 `scripts/demo_slice.py` end to end, trace in results | met | `results/2026-10-10_demo_slice/`; e62b17b |
| spec 2026-10-09 | 6 Held-out list: three named plus one chosen later by planning | changed by decision | decisions.md:93 (2026-10-12, held-out sizes approved): two added faults (`flank_swap`, `partial_occlusion`), proposed by the build account |
| spec 2026-10-09 | 6 Freeze under tag `freeze-v1` | changed by decision | decisions.md:86, :90 (2026-10-12, freeze approved from v2); tag `freeze-v2` on 5b64897 |
| spec 2026-10-09 | 6 Held-out injectors written only after the tag | not met | 8109764 (2026-10-12 20:07) before the tag commit 5b64897 (22:10) (specs-4) |
| spec 2026-10-09 | 6 `step_limit` and `error` scored as not reported | met | `measure/score.py:57`, `:99` |
| spec 2026-10-09 | Report back: results files | met | `results/2026-10-10_checker_synthetic/field_level.md`, `image_level.md`; `results/2026-10-10_demo_slice/trace.jsonl` |
| spec 2026-10-09 | Report back: spec-done note in the log | not shown | no line in running_log.md (specs-9) |
| spec 2026-10-10 bent rods | A Width change at two sizes | met | `results/2026-10-10_width_rotation/per_seed.md`; running_log.md:100; decisions.md:25 |
| spec 2026-10-10 bent rods | B Field case `rotation_basal_pivot`; image expectation and test | met | `measure/rod.py:269`; `tests/test_image_expected.py:23`; 4188ad8 |
| spec 2026-10-10 bent rods | B Closure against rotation rate | met | `results/2026-10-10_width_rotation/rotation.md`; running_log.md:101 |
| spec 2026-10-10 bent rods | B `rigid_rotation` out of the clean group | partial | thresholds comment updated (`config/checker_thresholds.yaml:5,9`; d1b6100); results tables not (specs-7) |
| spec 2026-10-10 bent rods | C1 Both cases in `field_cases()` | met | `measure/rod.py:231`, `:280`; decisions.md:59 |
| spec 2026-10-10 bent rods | C2 Image level, 5 seeds each, tracked twice | partial | 3 seeds (decisions.md:59; `results/2026-10-11_remedy_fixes/item7_bent.md`) (specs-6) |
| spec 2026-10-10 bent rods | C3 Errors, check values and peaks, profile plot, frame images | partial | `item7_bent.md`: one peak column; no plot or image committed (specs-6) |
| spec 2026-10-10 bent rods | Report back: spec-done note | not shown | specs-9 |
| spec 2026-10-10 repair criteria | A Clean rods through each remedy (stop) | met | `results/2026-10-10_repair_criteria/part_a.md`; running_log.md:131 |
| spec 2026-10-10 repair criteria | B Fault sizes, approved by Andrew | met | `part_b.md`; decisions.md:51, :61 |
| spec 2026-10-10 repair criteria | C Tolerance, labels, outcome table, test per row | met | decisions.md:50; `part_c.md`; `measure/score.py:57`; `tests/test_score.py:21` |
| spec 2026-10-10 repair criteria | D Prompt rules, before/after values, roll back in decisions | met | 9d27233; decisions.md:60; `tests/test_executors.py:133-158` |
| spec 2026-10-10 repair criteria | D Diagnostician runs, at most 8 | met | 5 runs, running_log.md:199; `results/2026-10-11c_world_smoothing_freeze/README.md:36` |
| spec 2026-10-10 repair criteria | Report back: spec-done note | not shown | specs-9 |
| spec 2026-10-11 remedy fixes | 1 Shared-compute limits in code, 8-run check | met | b04ca85; decisions.md:53-54; `tests/test_sweep.py:10`; running_log.md:151 |
| spec 2026-10-11 | 2 `smooth_midline` padding fix | met (superseded) | 6064dd0; decisions.md:55; replaced by decisions.md:66, :68 |
| spec 2026-10-11 | 3 `register_frames` cause confirmed, band redefined | met | 346388c; decisions.md:56; `results/2026-10-11_remedy_fixes/item3_band.md` |
| spec 2026-10-11 | 4 Uncoupled re-run | met | `item4_clean.md`, `item4_faults.md`; running_log.md:154 |
| spec 2026-10-11 | 5 Tolerance in config, labels, test | met | 9f73915; `config/scoring_tolerance.yaml`; `tests/test_score.py:62`; `item5_labels.md` |
| spec 2026-10-11 | 6 `couple` run setting, timing | met | decisions.md:58; `tests/test_executors.py:120`; `results/2026-10-11_remedy_fixes/README.md:71` |
| spec 2026-10-11 | 6 Coupled sweeps (about 440 runs) | changed by decision | decisions.md:63 (2026-10-11, remaining coupled sweeps not run), :69 |
| spec 2026-10-11 | 7 Bent rods, both modes | uncoupled met; coupled changed by decision | `item7_bent.md`; decisions.md:69 (2026-10-11, no further coupled runs) |
| spec 2026-10-11 | 8 Part D code | met | 9d27233 |
| spec 2026-10-11 | Report back: spec-done note | met | closed by 11b, running_log.md:173, :178 |
| spec 2026-10-11b | 1 Fitted-line padding, tests, re-run | met (stopped) | 4db4b0c; decisions.md:66; `results/2026-10-11b_padding_tolerance_coupling/b1_smoothing.md` |
| spec 2026-10-11b | 2 Flank tolerance by the basis rule | met (stop, then approved) | `results/2026-10-11c_world_smoothing_freeze/c2_flank_tolerance.md`; decisions.md:74, :78 |
| spec 2026-10-11b | 2 Recompute every label in the two results folders | partial | `results/2026-10-12_freeze_v2/item1_labels.md` covers the 15 frozen rods only (specs-8) |
| spec 2026-10-11b | 2 Repairable `low_texture` at 0.2 or 0.25 | met | none found; decisions.md:81 |
| spec 2026-10-11b | 3 Diagnostician runs, approved sizes | met | running_log.md:199 |
| spec 2026-10-11b | 4 Coupling weight: arguments listed, sweep, report | met | `results/2026-10-11b_padding_tolerance_coupling/README.md:30-35`, `b4_coupling_weight.md`; decisions.md:67 |
| spec 2026-10-11b | Report back: spec-done note | not shown | specs-9 |
| spec 2026-10-11c | 1 World-coordinate smoothing; `strong` rule | met | 8891942; decisions.md:71-72; `c1_smoothing.md` |
| spec 2026-10-11c | 2 Items 2-3 of 11b | met | running_log.md:198-199 |
| spec 2026-10-11c | 3 Uncoupled system, README line | met | `README.md:35` |
| spec 2026-10-11c | 4 Freeze list for approval | met | `docs/proposals/2026-10-11_freeze-v1.md` |
| spec 2026-10-11c | Report back: spec-done note | not shown | running_log.md:196 says not done; no later note (specs-9) |
| spec 2026-10-12 freeze decisions | 1 Decision lines, config, `strong` rejected, relabel | met | decisions.md:78-86; `config/scoring_tolerance.yaml:12`; `tests/test_executors.py:97`; `item1_labels.md`; 9ef68f1 |
| spec 2026-10-12 | 2 Scoring seeds committed before item 3 | met | f4f9a74 (20:24) before 2a5baa5 (20:31); `config/scoring_seeds.yaml` |
| spec 2026-10-12 | 3 Seeds 3-5 labelled before prompt change | met | 2a5baa5 (20:31) before 5b896cb (20:32); `item3_seeds35.md` |
| spec 2026-10-12 | 4 P1-P5 applied, tests | met | 5b896cb; `tests/test_info_p1_p5.py` (re-run, pass) |
| spec 2026-10-12 | 5 Freeze v2 file, not tagged | met | a3a0dbf |
| spec 2026-10-12 | 6 Development check, seed 0 | met | da93690; `results/2026-10-12_freeze_v2/README.md:40`, `:50` |
| spec 2026-10-12b | 1 Per-branch remote code directory, tests | met | 625b461; decisions.md:94; `tests/test_runner_code_dir.py` (re-run, pass); running_log.md:294-296 |
| spec 2026-10-12b | 2 Tag `freeze-v2`, pushed | met | `freeze-v2^{commit}` = 5b64897; tag on origin |
| spec 2026-10-12b | 3 Held-out labels before any held-out agent run | met | 1e5e2c2 (22:38) before c9d5a0c (22:43); `results/2026-10-12b_heldout_labels/` |
| spec 2026-10-12b | 4 Single-agent definition before runs, tests | met | 51f1598 (22:37) before 4192747, c9d5a0c; `tests/test_single_agent.py` (re-run, pass) |
| spec 2026-10-12b | 5-6 Scored runs, record fields | met | 160 summaries, all `freeze-v2` and c9d5a0c; `results/2026-10-12b_scored_v1/scores.json` has every listed field |
| spec 2026-10-12b | 7 Results tables; Lab report 1 root count | met | `results/2026-10-12b_scored_v1/README.md`; 30b78e1; `docs/reports/2026-10-16_lab-report-1.md:79` |
| spec 2026-10-13 auditor v1 | A1 View, withheld-key test | met | `audit/view.py`; `tests/test_auditor.py:64` (re-run, pass) |
| spec 2026-10-13 | A2 Rule written before running | met | 99d70bd (21:30:37) before d15db20 (21:31:04) |
| spec 2026-10-13 | A3 LLM auditor definition before held-out runs | met | `docs/proposals/2026-10-13_auditor-v1.md`; aa8483a before 46a9d6f |
| spec 2026-10-13 | A4 Call limits, runs, scoring, known limit | met; call unit set by build | `results/2026-10-13_auditor_v1/README.md:17-18`, `:57-58` (specs-15) |
| spec 2026-10-13 | A5 Out of scope | met | no control-vs-stressed code |
| spec 2026-10-13 | B1 30 windows from the manifest | changed by decision | decisions.md:101 (2026-10-13, usable windows only); running_log.md:348-352 |
| spec 2026-10-13 | B2 Frames pulled read-only, staged set | met | running_log.md:337-339; staged set has 90 frames, 30 views, `labels.csv` 30 rows, `HOW_TO_LABEL.txt` |
| spec 2026-10-13 | B3 Values hidden from labeling | met | running_log.md:340-341 |
| spec 2026-10-13 | B4 Real reference, separation stop, tests | met after decision | decisions.md:102, :104, :105; `config/frame_quality_reference.yaml`; `tests/test_frame_quality_reference.py` |
| spec 2026-10-16 vm-setup | 1 Restore check | met | running_log.md:393-396 |
| spec 2026-10-16 | 2 Task board, `scripts/board.py`, tests | met at build; fails now | 00da4f4; `python scripts/board.py` exits on a research-lane state (specs-3) |
| spec 2026-10-16 | 2 Open items of the 2026-10-12 specs as task files | met | `tasks/c002`, `c003`, `c004` |
| spec 2026-10-16 | 3 Heartbeat | met | decisions.md:114-115; running_log.md:202 |
| spec 2026-10-16 | 3 Report the first gap to Andrew | not shown | specs-5 |
| spec 2026-10-16 | 3 Resume rules in CLAUDE.md | met | `CLAUDE.md:52-59`; 129b1a5 |
| spec 2026-10-16 | 3 Nightly backup, keep last 7 | changed by decision | decisions.md:117, :118 (2026-10-16, no server deletes; no scheduled backup) |
| spec 2026-10-16 | 3 Backup tested by hand, checksums | met | running_log.md:400 |
| spec 2026-10-16 | 4 Stage A pitfall lists | not met | no `docs/lit/pitfalls/` on any branch; no papers folder in `private/` (specs-2) |
| spec 2026-10-16 | 5 Stage B tests | not met | no `tests/lit/` (specs-2) |
| spec 2026-10-16 | 6 Stage C reviewer agents | not met | no `.claude/agents/lit-*.md`, no `docs/reviews/<date>_<paper>.md` (specs-2) |
| spec 2026-10-16 | 7 Stage D Paper2Agent | not met | no commit or decision (specs-2) |
| spec 2026-10-16 | 8 Reviewer evaluation | not met | no `eval/planted-pitfalls` branch (specs-2) |
| spec 2026-10-16 | 9 Decision lines | partial | decisions.md:110-113 (board, Agent View, resume); none for the literature-reviewer decisions (specs-2) |
| spec 2026-10-16 | 9 Log entry at merge | met | running_log.md:391-409 |
| spec 2026-10-16 | 9 Lab report 2 names the reviewers, [ANDREW] on scope | in progress | `origin/wip/lab-report-2:docs/reports/2026-10-30_lab-report-2.md:17` |
| spec 2026-10-23 next steps | A1-A4 Lab report 2 draft | in progress (on branch) | 277d9de on `wip/lab-report-2` |
| spec 2026-10-23 next steps | A5 Accepted audit findings | not started | waits for SUMMARY.md marks |
| spec 2026-10-23 next steps | A6 Ready by Wed 28 Oct | not yet due | c009 `needs-input` on its branch |
| spec 2026-10-23 next steps | B1 Dispatcher proposal | in progress (on branch, awaiting approval) | 23443d2 on `wip/dispatcher` |
| spec 2026-10-23 next steps | B2 Tracker timing; B3 cluster rules; B4 cost estimate | not shown yet | no `results/2026-10-23_tracker_timing/` on any branch (specs-17, -18, -19) |
| spec 2026-10-23 next steps | B5 Dispatcher and real slice | not started | waits for approval |
| spec 2026-10-23 next steps | Done means: c009 | in progress | draft on branch; `[ANDREW]` items in `origin/wip/lab-report-2:docs/agents/status/lab-report-2.md` |
| spec 2026-10-23 next steps | Done means: c010 | not shown yet | |
| spec 2026-10-23 spec audit | Done means: six reviewer files and SUMMARY.md | in progress | `origin/wip/spec-audit`: evaluation f847be5, numbers c123706 |
| spec 2026-10-23 spec audit | Done means: CHECK.md | not started | spec-audit-check waits |
| spec 2026-10-23 spec audit | Done means: c008 done, log pending | not yet | c008 `working` on `origin/wip/spec-audit` |
| proposal 2026-10-09 structured actions | Conditions 1-7 | met | running_log.md:56-61; 5639f1c, 867278b, 60627bd, 1e0e2ac, 1f14abc, 25b2d35 |
| proposal 2026-10-09 structured actions | Changes if approved | met | no `scripts/check_api.py`, no `.env.example`, no `anthropic` in `environment.yml`; `config/models.yaml` has step limit and max turns |
| proposal 2026-10-09 structured actions | Open question: course staff accept typed actions as tool use | not shown | specs-16 |
| proposal 2026-10-11 freeze v1 | Whole list | changed by decision | decisions.md:86 (2026-10-12, freeze approved from v2, not v1) |
| proposal 2026-10-12 freeze v2 | 1-3, 5-8 Faults, remedies, info kinds, thresholds, tolerance, seeds, run settings | met | `git diff freeze-v2 origin/main` shows no change to `checker/`, `agents/prompts/diagnostician.md`, `measure/remedies.py`, thresholds, tolerance or seeds |
| proposal 2026-10-12 freeze v2 | 4 Claude Code 2.1.293 | changed by decision, no new freeze version | decisions.md:121; `config/models.yaml:6`; 519a3b1 (specs-1) |
| proposal 2026-10-12 freeze v2 | Open item: real `frame_quality` reference | partial | provisional real section (decisions.md:104); task c002 blocked |
| proposal 2026-10-12 freeze v2 | Header "Not tagged" | stale | `docs/proposals/2026-10-12_freeze-v2.md:3`; tag exists (specs-11) |
| proposal 2026-10-12 diagnostician misses | P1-P5 | met | 5b896cb; decisions.md:84, :87 |
| proposal 2026-10-12 diagnostician misses | Open items 1-4 | met | decisions.md:83-85, :104 (item 3 provisional) |
| proposal 2026-10-12 held-out faults | Open 1 sizes; 2 names and outcomes | met | decisions.md:93 |
| proposal 2026-10-12 held-out faults | Open 3 label sweep | met; one expected outcome replaced by label | 1e5e2c2; decisions.md:96 (`fast_rotation` decline) |
| proposal 2026-10-12 held-out faults | Open 4 branch readable on GitHub before the freeze | not shown (no decision) | specs-4 |
| proposal 2026-10-12 held-out faults | Open 5 `second_root` outcome | met | decisions.md:99 |
| proposal 2026-10-12 remedy tree | Committed before any run; unchanged after | met | ea95149 (19:59) before 720f7da, 9a2cc03; no later commit to `agents/baselines.py` |
| proposal 2026-10-12 single-agent baseline | Definition before run; four tests | met | 51f1598; `tests/test_single_agent.py:66-124` |
| proposal 2026-10-13 auditor v1 | A1-A4 | met | as spec 2026-10-13 Task A rows |
| proposal 2026-10-13 auditor v1 | For Andrew: z cutoff, MAD-0 fallback | met | decisions.md:106 |
| proposal 2026-10-13 auditor v1 | For Andrew: statistics over all runs; run id lists | not shown | specs-14 |
| proposal 2026-10-23 dispatcher | Not yet approved | out of scope | on `wip/dispatcher` only |

## 2. Findings

### specs-1: Claude Code re-pin changes a freeze v2 item without a new freeze version
- Ours: `config/models.yaml:6` (2.1.302); `docs/decisions.md:121`; commit 519a3b1 (2026-10-17)
- Source: `docs/proposals/2026-10-12_freeze-v2.md:56` (Claude Code 2.1.293); `docs/decisions.md:90` (model "do not change"); spec 2026-10-12b Limits ("Model, Claude Code version and step limit as in freeze v2"); spec 2026-10-23 spec audit, Goal (a change to a frozen item needs Andrew and a new freeze version)
- Evidence: `git diff freeze-v2 origin/main -- config/models.yaml` shows the version line changed. No freeze v3 file, no new tag. The 80 scored agent runs record 2.1.293. Any later diagnostician or auditor run under freeze v2 will run 2.1.302. The decision records Andrew's approval and the reason, not a freeze version
- Severity: would change a design choice
- Frozen item: yes (freeze v2 section 4, Claude Code version)
- Andrew: accepted, handled (freeze v3)

### specs-2: Literature-reviewer stages of the VM-setup spec (items 4-8) not done; no task file
- Ours: no `docs/lit/pitfalls/`, `tests/lit/`, `.claude/agents/lit-*.md`, `docs/reviews/<date>_<paper>.md`, `eval/planted-pitfalls` branch or planted-pitfalls proposal on any branch (`git log --all` on those paths and messages: none). No papers folder in `private/`. `tasks/c001-vm-setup.md` covers items 1-3 only; no task file for items 4-9. running_log.md:408 "then items 4-9 (new session)"
- Source: spec 2026-10-16 vm-setup items 4-9; `docs/reports/2026-10-16_lab-report-1.md:72`, `:92`, `:161` (reviewers listed as planned)
- Evidence: done: item 9 log entry at merge (running_log.md:391-409); item 9 decisions partial (decisions.md:110-113 cover board, Agent View and resume rules; none of the five reviewer decisions: component, five papers, Paper2Agent for two, read-only, PDFs not committed). Item 9 Lab report 2 line exists as an open `[ANDREW]` mark ("keep in the plan, or replace with the spec audit", `origin/wip/lab-report-2`, line 17). Not done: items 4, 5, 6, 7, 8
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, handled (freeze v3)

### specs-3: Task board does not print; board test fails
- Ours: `scripts/board.py:59`; `tests/test_board.py:97`
- Source: spec 2026-10-16 item 2 (board reads both folders, one table; tests include "research rows never appear in a tracked file"); CLAUDE.md Agents ("`python scripts/board.py` prints the board")
- Evidence: `python scripts/board.py` exits with an unknown-state error on one research-lane task file outside the repo (state "waiting on Andrew", not in the state list). `tests/test_board.py::test_research_rows_never_in_tracked_files` fails for the same reason. The coordinator status on `origin/main` (c730662) lists it under Needs Andrew
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (8223616)

### specs-4: Held-out injectors written and sized before the freeze tag
- Ours: 8109764 (2026-10-12 20:07, `measure/render_heldout.py`); fe7dda1 (20:19, checker-only held-out sizes); tag commit 5b64897 (22:10); `docs/decisions.md:91`
- Source: spec 2026-10-09 item 6 ("Held-out injectors are written only after the tag. Nothing frozen changes after a held-out result is seen"); held-out proposal open item 4
- Evidence: injectors and checker-only held-out results exist on `heldout/faults` before the freeze v2 approval (5593c65, 22:00) and the tag. Frozen items finished in that interval on another branch: prompt 5b896cb (20:32), freeze v2 file a3a0dbf (20:33). P1-P5 text was fixed earlier, in 55edff8 (20:02), before 8109764. The decision line keeps the branch separate "until the freeze (no development session reads it)"; no decision replaces the spec rule, and open item 4 (branch on GitHub) has no decision. No agent run on a held-out fault before 1e5e2c2 (labels) and c9d5a0c (harness)
- Severity: record only
- Frozen item: yes (freeze v2: held-out separation; prompt 5b896cb)
- Andrew: accepted, no action

### specs-5: First heartbeat gap not shown as reported to Andrew
- Ours: VM health log (location in `private/paths.md`) and its `FIRST_GAP` marker; running_log.md:408; `tasks/c001-vm-setup.md` (state done)
- Source: spec 2026-10-16 item 3 ("Report the first gap seen to Andrew"); Stop and ask ("The first heartbeat gap")
- Evidence: the health log has 7 gap lines from 2026-10-17 to 2026-10-23; the first is 2026-10-17 01:40 to 13:25 (705 min). No log entry, status or task file reports it. Two gap lines on 2026-10-18 have the same start time and end 74 s apart
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-6: Bent rods part C delivered in part
- Ours: `results/2026-10-11_remedy_fixes/item7_bent.md`; `docs/decisions.md:59`
- Source: spec 2026-10-10 bent rods, part C work 2-3 and Results ("one new folder under `results/` for this spec")
- Evidence: 3 seeds per case, not 5 (decisions.md:59 follows spec 2026-10-11 item 7, which gives about 24 runs; no decision changes the 5). One "Peak at s" column, not the peak of each check. No profile plot and no first-frame or last-frame image in `git ls-files results` (only `results/2026-10-10_checker_synthetic/clean_profiles.png`). Parts A-B in `results/2026-10-10_width_rotation/`, part C in `results/2026-10-11_remedy_fixes/`. Coupled runs not made: changed by decision (decisions.md:69)
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-7: `rigid_rotation` still listed as clean in the 2026-10-10 results
- Ours: `results/2026-10-10_checker_synthetic/image_level.md:10` ("rigid_rotation clean"); `results/2026-10-10_checker_synthetic/README.md:19` ("Clean check values over 20 rods: rigid_invariance max 1.08")
- Source: spec 2026-10-10 bent rods part B ("Remove `rigid_rotation` from the clean group in the results tables and in the basis comment of the thresholds file")
- Evidence: the thresholds comment was changed (`config/checker_thresholds.yaml:5`, `:9`: 15 rods, max 1.04; d1b6100). The results folder was last changed in aebc749 and still counts 20 clean rods
- Severity: record only
- Frozen item: no (the approved thresholds do not change)
- Andrew: accepted, no action

### specs-8: Label recompute of 11b item 2 narrowed to the frozen rods
- Ours: `results/2026-10-12_freeze_v2/item1_labels.md` (15 rods, 36 runs)
- Source: spec 2026-10-11b item 2 ("Recompute every label in `results/2026-10-10_repair_criteria/` and `results/2026-10-11_remedy_fixes/` under the new tolerance"); spec 2026-10-12 item 1 (dev faults, seeds 0-2)
- Evidence: labels of other sizes in those folders (for example `rigid_drift` sizes other than 0.5) are not recomputed at 1.00 %/h. The narrower scope comes from the later spec, not from a decisions entry
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-9: Spec-done notes missing from the running log
- Ours: `docs/running_log.md` (no done note for these specs)
- Source: spec 2026-10-09 line 71; spec 2026-10-10 bent rods line 79; spec 2026-10-10 repair criteria line 86; spec 2026-10-11b line 84; spec 2026-10-11c line 65
- Evidence: running_log.md:150, :178 and :196 state "spec not done" for 11, 11b and 11c; only 11 is later closed (by 11b, :178). The freeze-v2 and scored-v1 entries (:266, :293) state their specs done. No entry closes 2026-10-09, both 2026-10-10 specs, 11b or 11c
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (3163fec; notes in the pending log entry)

### specs-10: Task c007 state and record do not match the repo
- Ours: `tasks/c007-litnet.md` (state done, all 7 parts unchecked); 84c69c8 (2026-10-18, state working); 2170ca5 (2026-10-23, state done)
- Source: CLAUDE.md Agents (each session updates its own task file at start, each commit, stop) and Resume (done markers; working tasks with no live session set to interrupted); `tasks/README.md`
- Evidence: state `working` from 2026-10-18 22:42 to 2026-10-23 00:32 with no update and no session on the board; not set to interrupted. Set to done by the coordinator, not the owner `litnet`, with none of its parts marked. The done marker changed from a checkable file to "network on lab server; not in this repo by decision", which no file in the repo shows. No running-log entry for c007. The network is now also on the VM (`litnet:` line in `private/paths.md`, added for c008)
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-11: Status files, roster and freeze v2 header out of date
- Ours: `docs/agents/status/fq-real.md` and `docs/agents/status/auditor-v1.md` ("State: ready to merge"); `docs/agents/README.md:47-48` (auditor-v1, fq-real "to start"); `docs/proposals/2026-10-12_freeze-v2.md:3` ("Not tagged")
- Source: `docs/agents/README.md` status protocol; inbox fq-real item 6 ("status `done` after merge")
- Evidence: `wip/fq-real` merged in 742dc79, `wip/auditor-v1b` in f52dbdd (merge commits). Tag `freeze-v2` exists on 5b64897 and on origin
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (ed8279a)

### specs-12: Task c003 omits one server item left for Andrew
- Ours: `tasks/c003-old-remote-code-copies.md`; `docs/agents/status/vm-setup.md` (Needs Andrew)
- Source: CLAUDE.md (no Claude session deletes on the lab server; Andrew deletes at the end); vm-setup status
- Evidence: the vm-setup status asks Andrew to delete the `2026-10-16_test` backup folder and `_verify/`. c003 lists `_verify/` and the old code copies, not the test backup folder
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-13: No running-log entry after 2026-10-17 on main
- Ours: `docs/running_log.md` (last entry 2026-10-17, readme-check)
- Source: CLAUDE.md Logging ("Log entry ... at the end of every session")
- Evidence: work after 2026-10-17 with no entry on `main`: c004 marks filled 2026-10-17 by Andrew with the planning account (task c004 text); c007 2026-10-18 to 2026-10-23; coordinator items 6-7 (2170ca5, b563b33, c730662). Pending entries for 2026-10-23 sessions are on their branches
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (3163fec; gap note in the pending log entry)

### specs-14: Auditor v1 open choices not shown decided; next step has no task
- Ours: `docs/proposals/2026-10-13_auditor-v1.md:48-49`, `:54`; running_log.md:330
- Source: spec 2026-10-13 A2 (provisional items listed for Andrew); running_log.md:330 ("Remaining: Andrew: z cutoff 3, MAD-0 fallback, statistics over all runs, run id lists ... Next: flank-spacing rate in the view")
- Evidence: decisions.md:106 fixes the z cutoff and the MAD-0 fallback only. No entry for batch statistics over all runs or for run id lists in `flag` and `clear` (decisions.md:103 records them as defined). No task file for the flank-spacing rate in the view
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-15: Auditor call limit counted per run, not per CLI call
- Ours: `results/2026-10-13_auditor_v1/README.md:17-18`; `docs/proposals/2026-10-13_auditor-v1.md:40`
- Source: spec 2026-10-13 A4 ("At most 40 auditor calls on dev") and Limits ("at most 52 auditor calls")
- Evidence: from `results/2026-10-13_auditor_v1/llm/*_result.json`: 66 CLI calls in the 12 dev runs, 74 in the 12 held-out runs. The proposal defines one call as one run; the spec arithmetic (40 + 12 = 52) fits that reading. No decisions entry
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-16: Course-staff answer on typed actions as tool use not shown
- Ours: `docs/proposals/2026-10-09_structured-action-agents.md:79`; running_log.md:45 to :208 (bottleneck repeated through session 10)
- Source: proposal 2026-10-09, open question with Andrew
- Evidence: the bottleneck line stops after 2026-10-11 session 10; no log entry, decision or report line records an answer
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-17: Dispatcher spec extrapolates to 118 roots
- Ours: `origin/main:docs/specs/2026-10-23_next-steps-lr2-dispatcher.md:40`
- Source: spec 2026-10-12b Decisions ("123 root positions, 102 kept ... The 118 in the project summary is the earlier inventory"); `manifest/root_manifest.csv`
- Evidence: manifest recount: 123 rows, `include` yes 102, unsure 11, no 10
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-18: Conditional cluster approval not in decisions; spec Limits line disagrees
- Ours: `origin/main:docs/specs/2026-10-23_next-steps-lr2-dispatcher.md:46` (conditional approval under $5) and `:55` ("nothing submitted without Andrew's approval of a cost estimate"); inbox dispatcher item 5
- Source: CLAUDE.md:34 (cluster used only after Andrew approves a cost estimate); CLAUDE.md Logging (decisions kept current)
- Evidence: `docs/decisions.md` on `origin/main` has no 2026-10-23 entry for the cluster rules, the $5 cap or the conditional approval. The spec's own Limits line and CLAUDE.md:34 still state the earlier rule
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-19: Dispatcher spec names a process owner
- Ours: `origin/main:docs/specs/2026-10-23_next-steps-lr2-dispatcher.md:40` ("check for other ... jobs first", with an account name in backticks)
- Source: CLAUDE.md Rules line 1 (no tracked file names a user account)
- Evidence: the word in backticks is a login name. For the rules reviewer
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### specs-20: `status/gate2` holds a VM path and an account identity
- Ours: `origin/status/gate2:docs/agents/status/gate2.md` (Needs Andrew, second line); author fields of the 11 commits in `origin/main..origin/status/gate2`
- Source: CLAUDE.md Rules line 1; `docs/agents/README.md` research-lane status rule
- Evidence: what the branch holds that `main` lacks: one file, `docs/agents/status/gate2.md` (16 lines): state waiting on Andrew, last inbox item 7, full run 7 of 7 roots, window counts, Gate 2 pass/fail with counts, two Needs Andrew lines. One Needs Andrew line names a folder under a home directory on the VM. All 11 commits carry an author identity of the form account-at-domain (a personal address); `main` commits carry the repo identity or the noreply address. `pre_push_check.py` on the 11 commits: 0 hits (the path rule does not cover a home-relative path; author fields are not scanned)
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (branch `status/gate2` removed from the remote, inbox audit-marks item 2)

### specs-21: Checker definitions written alongside the code
- Ours: running_log.md:81; decisions.md:14-19; commits 6547010, f606fb1
- Source: spec 2026-10-09 item 4 ("Before coding, write the exact definition of each check and its cost")
- Evidence: the log states the definitions "were worked out alongside the code, then committed before it"
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

## 3. Checked, no finding
- `wip/readme-check`: 0 commits not on `main`; merged in 7d7cbbd (2026-10-17). It holds nothing `main` lacks. Task c006 done matches
- Tasks c001, c002, c004, c005, c006: state matches the repo. c002 blocked: `config/frame_quality_reference.yaml` real section is provisional. c004: no `[ANDREW]` mark left in `docs/reports/2026-10-16_lab-report-1.md`
- Tasks c008, c009, c010 show `queued` on `main` and are updated on their own branches (`working`, `needs-input`, `working`), as `tasks/README.md` sets out. c008 on `origin/wip/spec-audit` has no blocker; the network location is in `private/paths.md`
- Frozen files unchanged since the tag: `checker/`, `agents/prompts/diagnostician.md`, `measure/remedies.py`, `config/checker_thresholds.yaml`, `config/scoring_tolerance.yaml`, `config/scoring_seeds.yaml`. Changes after the tag in `agents/actions.py` (`single_agent` alias), `config/models.yaml` (new agent entries, auditor step limit), `measure/info.py` (real reference for `movie: real` only) leave the diagnostician's lists and synthetic answers as frozen
- Scored runs v1: 160 summaries, all `freeze-v2`, commit c9d5a0c; 80 agent summaries at Claude Code 2.1.293
- Order rules held: scoring seeds before seeds 3-5 labels before P1-P5; held-out labels before held-out agent runs; single-agent and auditor definitions before their runs; remedy tree before its run
- `step_limit` and `error` scored as `not_reported` (`measure/score.py`)
- Held-out injectors are not in `measure/render.py` (only the five development faults)
- No coupled run after decisions.md:69; `couple` stays false (README.md:35)
- Spec 2026-10-13 decision on `use_width_free_ratio` as a fitting state: no labelled set made since, so not yet applicable
- Test re-runs: 173 of 174 pass (the failure is specs-3). One combined run of `tests/test_render_heldout.py` and `tests/test_ops.py` showed one F before the 58 s timeout cut it; each file alone then passed (14 and 5)
