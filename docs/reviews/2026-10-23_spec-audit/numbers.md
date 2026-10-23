# Spec audit, reviewer `numbers`

Spec `docs/specs/2026-10-23_spec-audit.md`, Reviewers item 3. Brief `.claude/agents/audit-numbers.md`. Worktree at `origin/main` plus audit files, 2026-10-23.

Scope: `docs/reports/2026-10-16_lab-report-1.md`, `docs/context/project_summary.md`, the last 10 entries of `docs/running_log.md` (lines 281-428), and the root count in the `CLAUDE.md` summary.

Method:
- Recomputed with `python -c` (env `me295`) from `results/2026-10-12b_scored_v1/scores.json`, `results/2026-10-13_auditor_v1/llm/*_result.json` with the git-ignored `results/2026-10-13_auditor_v1/id_map.json`, `results/2026-10-09_action_schema/result.json`, `manifest/root_manifest.csv`, `measure.rod` field cases (analytic, no tracker)
- Commit counts and hashes from `git log` / `git show`. Test counts from `pytest --collect-only` (no test run)
- Staging counts from the git-ignored `staging/` (file counts and label counts only)
- No tracker run, no agent call, no PDF opened. No STOP condition met

## 1. Table

### `docs/reports/2026-10-16_lab-report-1.md`

| Number | Where stated | Source | Recomputed | Match |
| :-- | :-- | :-- | :-- | :-- |
| 142 commits, 304a3cb to 4ab1c32; 23/26/15/37/29/12 per day | :7 | git history | 142 (root + 141); 23/26/15/37/29/12 | yes |
| fresh clone efd8b22; env 42 s; Claude Code 2.1.302 | :8 | log :412-423; commits 251383d, 7d7cbbd exist | - | yes |
| 198 passed, 5 skipped, 0 failed | :8, :22, :84 | log :419, :425 | 203 collected; `test_ops.py` 5 | yes |
| model `claude-opus-5-5`; 2.1.293, re-pin 2.1.302 | :16 | `config/models.yaml` | as stated | yes |
| check_cli OK, 1.5 s | :16 | log :62 only | - | no source (log only) |
| schema test 12 calls; 4/4, 4/4, 0/4 | :18 | `results/2026-10-09_action_schema/result.json` | 12 calls; optional 4 valid, nullable 4, union 0 | yes |
| seven review conditions | :17 | `docs/proposals/2026-10-09_structured-action-agents.md` Review | 7 | yes |
| at most 4 workers | :19 | `docs/decisions.md` 2026-10-11 | as stated | yes |
| pre-push 29 tests | :20, :62 | log :213, :396 | 29 collected | yes |
| 131 passed (12 Oct) | :22 | log :213, :229 | last 12 Oct suite: 169 (log :310) | see numbers-6 |
| 187 (13 Oct); 203 (16 Oct) | :22 | log :328, :405 | 203 collected | yes |
| 123 positions, 192 folders, 102 keep, 9 windows set | :25, :79 | `manifest/root_manifest.csv`, `manifest/README.md` | 123 rows; 192 distinct imgdir (122 montage + 70 raw); include yes 102 / unsure 11 / no 10; 9 rows with `usable_to_h` below the movie end (7 yes, 2 unsure) | yes |
| 118 (submitted summary) | :79 | `CLAUDE.md`:6; log :18 (earlier inventory) | no manifest subset gives 118 | see numbers-1, numbers-3 |
| 30 windows, 90 frames; 24 clean, 5 unsure, 1 not clean | :26 | log :352, :361; `staging/fq_real_labeling/` | labels 24 / 5 / 1; frames 90; views 30 | yes (pulled count: numbers-7) |
| six field cases within 0.08 %/h | :29 | log (2026-10-10) :79; `tests/test_synth_field.py` bound 0.1 | max 0.029 %/h over the six (now 9 cases; max 0.053) | yes |
| 70 tracker runs; 18 of 18; 0.40-0.44 %/h RMS; 43 %/h peak | :30 | `results/2026-10-10_checker_synthetic/README.md`, `field_level.md`, `image_level.md` | 18 rows as expected; clean gz and bending 0.40-0.44 | yes |
| thresholds 2.0, 1.0, 3.25 | :31 | `config/checker_thresholds.yaml` | as stated | yes |
| 354 tracker runs, 0 failed | :33 | `results/2026-10-10_repair_criteria/README.md` | as stated | yes |
| register_frames 6 of 6, 0.09-0.16 px/h; smooth_midline 12 of 12; strong fails 6 of 6 bent | :34 | `results/2026-10-11_remedy_fixes/README.md` s3; `results/2026-10-11c_world_smoothing_freeze/README.md` s1-2 | as stated | yes |
| coupled 10 of 10 fail closure; 252 runs | :35 | `results/2026-10-11_remedy_fixes/README.md` s6; `results/2026-10-11b_padding_tolerance_coupling/README.md`:16 | as stated | yes |
| first diagnostician runs: 1 of 5, 0 of 5, 37 steps, 159k / 18k, 207 s, three code faults | :38 | `results/2026-10-11c_world_smoothing_freeze/README.md` table | steps 37; in 159,448; out 18,111; 207.2 s; faults 2 scripting + 1 roll-back | yes |
| flank 1.00 %/h; seeds 1-5; 66 runs; 5 of 5, 5 of 5 | :39 | `config/scoring_tolerance.yaml`; `results/2026-10-12_freeze_v2/README.md` | 60 + 6 = 66; devcheck 5 correct, 5 named | yes |
| held-out 3 of 3 seeds, 54 runs; labels 84 runs | :40 | `results/2026-10-12_heldout_faults/checker_sizes.md`; `results/2026-10-12b_heldout_labels/README.md` | 9 sizes x 3 seeds x 2 copies = 54 | yes |
| 160 runs, 80 agent, 202 tracker runs | :42 | `scores.json`; `results/2026-10-12b_scored_v1/README.md` | 160 records; 80 agent; 96 + 22 + 84 = 202; `tracker_runs_new` sums to 22 | yes |
| method table dev / held-out correct and false accepts | :44-49 | `scores.json` | script 10/10, 3/12; tree 24/0, 9/3; diagnostician 24/0, 11/0; single 11/0, 7/0 | yes |
| 5.2 steps, 23.0k, 31.6 s; 6.8, 28.4k, 38.8 s; 13 of 25 step limit | :51 | `scores.json` | 5.25, 23,031, 31.59; 6.80, 28,415, 38.81; single dev `not_reported` 13 | yes (rounding: numbers-8) |
| second_root 3 of 3 each, 9 runs | :52 | `scores.json` | 9 good_report runs named width_change | yes |
| auditor: 14 of 15 x3; rule 15/15; good 7, 5, 5 of 11; rule 5/11; 24 runs | :53 | auditor `llm/` results + `id_map.json` | per repeat FA 14/15; good 7, 5, 5 / 11; 24 result files, all `report` | yes |
| restore 11 branches; bundle 3.1 MB; 1.14 GB; 917 MB; 124 MB; 219 MB | :57-58 | log :381-383 | 11 heads listed; all hashes resolve; tag 6a68610 -> 5b64897 | no source (log only) for sizes |
| checksums 5 of 5; load 2.2 of 32; 74 MB/s above 50 MB/s cap | :60 | log :385-386 | - | no source (log only); cap: numbers-10 |
| private/ 21 of 21; 570 of 570; 203 passed | :62 | log :394, :405 | 43 + 24 + 503 = 570 | yes (sum); per-file counts log only |
| step limit of 8 | :158 | `config/models.yaml` diagnostician | 8 | yes |
| held-out 15 runs; 11 of 15, 0 FA; tree 9 of 15, 3 FA | :172 | `scores.json` | as stated | yes |
| 12 of 15 held-out (script) | :112 | `scores.json` | 12 | yes |
| 13 of 25 (single agent step limit) | :108 | `scores.json` | 13 | yes |
| PatchTrack disks every 10 px | :118 | `paper_digests.md` Henry2023 | as stated | yes |
| Platre 8 % / 60 min, 25 % / 12 h | :121 | `paper_digests.md` Platre2024 | as stated | yes |
| ReAct 47 %, 23 %, 0 %, 56 %; Geifman 2 %, 99.9 %, 60 %; Wei four levels, five capabilities | :101-111 | none in repo (not in `paper_digests.md`) | - | no source (numbers-11) |
| five papers for pitfall lists; items 1-3 done, 4-9 remaining | :71-72 | log :408; spec 2026-10-16 | 5 named | yes |

### `docs/context/project_summary.md`

| Number | Where stated | Source | Recomputed | Match |
| :-- | :-- | :-- | :-- | :-- |
| summary settled 7 Oct 2026 | :3 | log 2026-10-08 :5 "project summary final" | - | no (numbers-4) |
| rotation near 7 degrees per frame | :23 | `docs/context/research_background.md`:30 only | held-out: 2 deg/frame for 3 frames fails all checks on 3 of 3 | no source in results (numbers-5) |
| 12-16 root subset | :30 | plan | 102 include yes available | yes (feasible) |
| one 24 h root | :42 | plan | movie durations 23.61-24.02 h | yes |
| 118 roots over 24 h (`CLAUDE.md` summary) | `CLAUDE.md`:6 | `manifest/root_manifest.csv` | 123 / 102 / 113 (yes + unsure) | no (numbers-1, numbers-2) |

### `docs/running_log.md`, last 10 entries

| Number | Where stated | Source | Recomputed | Match |
| :-- | :-- | :-- | :-- | :-- |
| 14 tests; suite 145 | :283 | `tests/test_render_heldout.py` | 14 collected | yes |
| 54 runs, 204 s, 245 s wait, load 4.30/5.63/4.99, work space 5.83 -> 6.70 GB | :285 | none in `results/2026-10-12_heldout_faults/` | work-space chain consistent with later entries (6.7 -> 7.28 -> 7.30 -> 7.52) | no source (numbers-12) |
| checker 3 of 3 at the sizes listed; 15 px 0 of 3 | :286-287 | `checker_sizes.md` | as stated | yes |
| 6 tests (`test_runner_code_dir.py`) | :294 | tests | 6 | yes |
| 84 runs, 212 s, load 5.71; labels | :298-299 | `results/2026-10-12b_heldout_labels/README.md`, `labels.md` | as stated | yes |
| 5 tests (`test_single_agent.py`) | :302 | tests | 5 | yes |
| 160, 80, 0 errors; c9d5a0c; 2.1.293 | :303 | `scores.json` | commit c9d5a0c all; claude_code 2.1.293 on all 80 agent runs | yes |
| 96 runs, 9 rounds, 445 s, load 4.73; 22 single; 202; 657 s | :304 | results README | 96 + 22 + 84 = 202; 445 + 212 = 657 | yes |
| dev correct 10/24/24/11; FA 10; not reported 1, 13 | :305 | `scores.json` | as stated | yes |
| held-out 3/9/11/7; FA 12, 3; terminal fault 1/3/1 | :306 | `scores.json` | `fault_correct` tree 1, diagnostician 3, single 1 | yes |
| 5.2 / 23.0k / 2.7k / 31.6 s; 6.8 / 28.4k / 3.3k / 38.8 s; 0.92M, 1.14M | :308 | `scores.json` | 5.25 / 23,031 / 2,745 / 31.59; 6.80 / 28,415 / 3,278 / 38.81; 921,244; 1,136,585 | yes (numbers-8) |
| 169 passed | :310 | log only | - | no source (log only; test count at that commit not re-run) |
| 18 tests (`test_auditor.py`); 160 records; 0 tracker runs | :319-320 | tests; auditor README | 18 collected | yes |
| rule dev 10/10, held-out 15/15; good dev tree 6/14, diag 7/15, held-out 5/11 | :321 | auditor README, `rule/` | as stated | yes |
| LLM dev rounds: tree 4 -> 0 -> 0 / 14; diag 7 -> 5 -> 0 / 15; single 5 -> 0 -> 5 / 6; script 10/10, 15/15 | :322 | `llm/dev_*` + `id_map.json` | as stated | yes |
| held-out 12 calls; 74 calls; 14/15; 7, 5, 5 / 11; alt 0/9 | :323 | `llm/heldout_*` + `id_map.json` | 12 runs; 74 steps; as stated | yes (term: numbers-9) |
| REGR peak z 6.7 | :324 | auditor README | - | yes (README) |
| 24 runs; 80.2k, 48.6 s; 68.2k, 45.0 s | :325 | `llm/*_result.json` | 80,221 / 48.59 s; 68,160 / 44.99 s | yes |
| 187 passed | :328 | log only | - | no source (log only) |
| fq-real: 30 windows; 6/5/8/7/4; 4/4/5/8/9; 20 clean candidates, 10 likely poor; frame step 90-114 s, 96-111 s; load 0.3-0.7; 530 MB; 1200 x 2280 px | :335-352 | window list in `private/` (not tracked) | sums 30 and 30; 90 frames and 30 views in staging | partial; rest no tracked source (numbers-13) |
| 7 replaced, 21 frames pulled | :348-349 | log | 7 x 3 = 21 | yes (numbers-7) |
| 24 / 5 / 1 labels; 72 frames; medians and lowest 0.0648, 0.0439, 0.0286, 0.0213 | :361-362, :370 | `staging/fq_real_labeling/labels.csv`; `config/frame_quality_reference.yaml` | 24 / 5 / 1; 24 x 3 = 72; config values as stated | yes |
| fq12 values 0.070-0.073, 0.029-0.031 | :363 | `private/` only | - | no tracked source (numbers-13) |
| 3 tests; 172 passed, 87 s | :372 | tests | 3 collected; 172 log only | yes / log only |
| vm-backup: branch heads, tag, sizes, 5 of 5, 74 MB/s for 15 s, 54 MB/s, load 2.2 | :380-386 | log only; heads in git | all 11 heads and tag resolve; 1.14 GB / 74 MB/s = 15.4 s | partial (numbers-12) |
| main 41f75b3 = 8759d4f plus two log commits | :393 | git | 2 commits (d81b303, 41f75b3) | yes |
| 21/21, 43/43, 24/24, 503/503; 29 passed | :394-396 | log only; tests | 29 collected | partial (numbers-12) |
| `test_board.py` 8 | :397 | tests | 8 | yes |
| tasks c001-c005, 2 research; board 7 rows (5 course, 2 research) | :398, :406 | `tasks/` | c001-c005 exist (5 course; c006-c010 added later); research tasks outside the repo, not checked | yes |
| backup test 7 min, 1.1 GB, 328 MB, 53 s, about 28 MB/s, cap 40 | :400 | log only | (1.14 GB + 328 MB) / 53 s = 28 MB/s | yes (arithmetic); log only |
| caches 124, 81, 81, 99, 142 files | :403 | `staging/` | 124, 81 (in `tracks_2026-10-12/tracks_freeze`), 81, 99, 142 | yes |
| 8 batch views (dev 4 x 25, held-out 4 x 15) | :404 | `results/2026-10-13_auditor_v1/views/` | 8 batches; id_map 25 / 15 per batch | yes |
| 203 passed, 62 s | :405 | tests | 203 collected | yes |
| readme-check: 64 of 100 GB, 0.6 GB, conda 26.7.2, Python 3.14.7, 42 s, 0.2 s, 75 s, 70 s, 5.0 s, 2 turns | :414-425 | log only | 198 + 5 = 203 collected; `test_ops.py` 5 = skips | partial (numbers-12) |
| pin 2.1.293 -> 2.1.302 | :423 | `config/models.yaml` | 2.1.302 | yes |

## 2. Findings

### numbers-1: 118 roots in the summary and the next cost estimate matches no manifest count
- Ours: `CLAUDE.md`:6 ("each of 118 roots"); `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md`:40 ("Extrapolate to 24 h and to 118 roots ... input to the cost estimate"); `docs/reports/2026-10-16_lab-report-1.md`:79
- Source: brief item "counts in the summary that refer to future work (for example 118 roots) are checked against `manifest/root_manifest.csv`"; `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md`:13 ("The 118 in the project summary is the earlier inventory")
- Evidence: manifest 123 rows; include yes 102, unsure 11, no 10; yes + unsure 113. No subset gives 118. Log (2026-10-08) :18 gives 118 as the earlier inventory, with per-folder counts that disagree with the scan
- Severity: would change a design choice (cluster cost estimate scaled to 118 instead of 102 include-yes roots: +16 %)
- Frozen item: no
- Andrew:

### numbers-2: "over 24 h" for every root; 7 include-yes roots have a shorter usable window
- Ours: `CLAUDE.md`:6 ("each of 118 roots over 24 h"); `docs/context/project_summary.md`:42
- Source: `CLAUDE.md` rule "only time inside `usable_from_h` to `usable_to_h`"
- Evidence: 9 manifest rows have `usable_to_h` below the movie end (9.5, 10, 12, 17.5, 18 x4, 20 h); 7 of them include yes. Movie durations 23.61-24.02 h
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-3: Lab report 1 states the 118 difference without the reason the spec gives
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:79 ("the submitted summary gives 118"); final text from commit b9e67ef
- Source: `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md`:57 (text to use: "the earlier inventory gave 118"); commit 30b78e1 had that wording
- Evidence: current line names the difference but not its cause (earlier inventory, log :18)
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-4: Summary date 7 Oct against the log's 8 Oct
- Ours: `docs/context/project_summary.md`:3 ("Final summary settled 7 Oct 2026")
- Source: `docs/running_log.md`:5 (entry 2026-10-08: "project summary final")
- Evidence: no tracked record dated 7 Oct; first commit 304a3cb is 2026-10-09
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-5: "Rotation near 7 degrees per frame" has no result source; results show failure at 2 deg/frame
- Ours: `docs/context/project_summary.md`:23
- Source: `docs/context/research_background.md`:30 (stated, no result); `results/2026-10-12_heldout_faults/checker_sizes.md`; `results/2026-10-12b_heldout_labels/labels.md`
- Evidence: fast_rotation at 2 deg/frame for 3 frames fails all three checks on 3 of 3 seeds and is labelled not repairable; unlogged 0.1 deg/frame fails closure (`results/2026-10-10_width_rotation/rotation.md`). No run at or near 7 deg/frame in `results/`
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-6: "131 passed (12 Oct)" is not the 12 Oct end count
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:22
- Source: `docs/running_log.md`:213, :229 (131), :244 (138), :274 (137), :283 (145), :310 (169); all 12 Oct entries
- Evidence: 131 is the gatekeeper and diag-review count; the last 12 Oct suite count is 169 (scored-v1 branch). Log :253 says the report cited the last logged count at drafting
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-7: Lab report gives 90 frames pulled; 111 were pulled
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:26 ("90 frames pulled read-only")
- Source: `docs/running_log.md`:337 (90 frames), :349 (21 more frames for 7 replaced windows), :350 (replaced frames removed from staging)
- Evidence: 90 + 21 = 111 frames pulled; the final set holds 90 (staging count 90)
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-8: Diagnostician mean steps 5.25 shown as 5.2
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:51; `docs/running_log.md`:308; `results/2026-10-12b_scored_v1/README.md` steps table
- Source: `results/2026-10-12b_scored_v1/scores.json`
- Evidence: 210 steps / 40 runs = 5.25 (half-even rounding gives 5.2; half-up gives 5.3). Other means match to the stated digit
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-9: "calls" counts two different things for the auditor
- Ours: `docs/running_log.md`:323 ("12 calls" and "one system prompt hash over 74 calls"); `results/2026-10-13_auditor_v1/README.md` Runs ("12 calls (of 40)", "all 74 held-out calls", "limit 52")
- Source: `results/2026-10-13_auditor_v1/llm/heldout_*_result.json` (`outcome.steps`, `outcome.calls`)
- Evidence: 12 held-out auditor runs; 74 steps (model calls) summed over them. "Calls" means runs in one place and model calls in the other
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-10: 50 MB/s transfer limit has no tracked source
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:60; `docs/running_log.md`:386; `docs/decisions.md`:116
- Source: `CLAUDE.md` rule "Limits in `docs/decisions.md`, 2026-10-11"; `docs/decisions.md` 2026-10-11 entry (workers, priority, load, lock; no bandwidth)
- Evidence: the 50 MB/s figure appears only as a reference to the limit the backup exceeded. Other caps in the log: 40 Mbit/s (fq-real pull, :337), 40 MB/s (backup script, :400). No tracked spec or decision sets 50 MB/s
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-11: Agent-paper numbers in the related-work note have no source in the repo
- Ours: `docs/reports/2026-10-16_lab-report-1.md`:101-111 (Wei et al. four levels, five capabilities; ReAct 47 %, 23 %, 0 %, 56 %, Table 2; Geifman & El-Yaniv 2 % top-5 error at 99.9 %, about 60 % coverage)
- Source: `docs/context/literature/paper_digests.md` (26 digests, none for Wei 2025, Yao 2023 or Geifman 2017); spec 2026-10-23 Inputs says the digests include the agent-systems papers
- Evidence: grep for the paper names and arXiv ids in `docs/` finds only the lab report. Not checked against the papers (no PDF opened)
- Severity: record only (needs Andrew to check the papers: Yao2023 Table 2; Geifman2017 ImageNet result; Wei2025 sec. 2-3)
- Frozen item: no
- Andrew:

### numbers-12: Operational numbers in the log with no result file
- Ours: `docs/running_log.md`:285 (held-out size sweep wall, wait, load, work space); :310, :328, :372 (suite counts at past commits); :380-386 (backup sizes, checksums, rates, load); :394 (per-file restore counts 21, 43, 24, 503); :400 (backup test times and sizes); :414-425 (disk, env, versions, timings); `docs/reports/2026-10-16_lab-report-1.md`:16 (check_cli 1.5 s, log :62), :57-62
- Source: brief "Trace each number to a result file or commit"
- Evidence: these numbers exist only in the log text (the log commit is the only record). Cross-checks that hold: work-space chain 5.83 -> 6.70 -> 7.28 -> 7.30 -> 7.52 GB across entries; 43 + 24 + 503 = 570; 1.14 GB / 74 MB/s = 15.4 s; branch heads and tag resolve in git; staging cache counts 124/81/81/99/142; 198 + 5 = 203 tests collected
- Severity: record only
- Frozen item: no
- Andrew:

### numbers-13: fq-real window composition and the not_clean values are only in `private/`
- Ours: `docs/running_log.md`:335-339, :349, :352, :363
- Source: `CLAUDE.md` rule that private context stays in `private/`; spec 2026-10-13 :78 ("Numbers may be committed. Images, root paths and the candidate list may not")
- Evidence: per-experiment window counts (6/5/8/7/4, then 4/4/5/8/9; each sums to 30), frame steps, load, 530 MB, and fq12 values have no tracked result file. Labels 24 / 5 / 1 and 90 frames confirmed from `staging/fq_real_labeling/`. Reference values confirmed in `config/frame_quality_reference.yaml`. No `results/` folder for fq-real
- Severity: record only
- Frozen item: no
- Andrew:

## 3. Checked, no finding
- Commit count and per-day counts of Lab report 1 (142; 23/26/15/37/29/12)
- All 37 commit hashes cited in Lab report 1 and the 26 cited in the last 10 log entries resolve; tag `freeze-v2` (6a68610) points to 5b64897 as log :297 states
- Scored runs v1: every count in the Lab report 1 table, log :303-308 and the results README recomputed from `scores.json`; tracker runs 96 + 22 + 84 = 202; sweep wall 445 + 212 = 657 s
- Auditor v1: false accepts and good reports flagged per run and per repeat, alt_repair 0 / 9, steps 66 and 74, tokens and call times recomputed from the 24 result files and `id_map.json`; commits recorded per round match log :322, :326
- First diagnostician runs (session 10) totals; development check after freeze v2 (5 of 5, 5 of 5); seeds 3-5 66 runs
- Held-out sizes (54 runs) and labels (84 runs, fast_rotation label change)
- Checker on synthetic rods: 70 runs, 18 of 18, clean error 0.40-0.44 %/h; field-level bound 0.08 %/h holds (max 0.029 %/h for the six original cases)
- Repair criteria 354 runs; remedy-fix numbers; coupled 10 of 10; coupling sweep 252
- Action schema 12 calls, 4 / 4 / 0
- Thresholds, tolerance, step limit 8, model and Claude Code pins against `config/`
- Manifest: 123 positions, 192 folders, 102 keep, 9 windows set
- Test counts per file in the log (14, 6, 5, 18, 3, 8, 29, 5 in `test_ops.py`) and the full suite 203 = 198 + 5 skipped
- Run counts: 25 dev = 5 faults x 5 seeds; 15 held-out = 5 x 3; 160 = 4 x 40; 80 agent runs = 2 x 40
- Fault counts: 8 classes in the summary list = 5 development + 3 held-out names (second_root, fast_rotation, bad_stage_correction); flank_swap and partial_occlusion added as held-out, the list is marked "initial"
- Paper counts: 26 digests in `paper_digests.md`; five pitfall-list papers named consistently in the report and spec 2026-10-16
- Literature numbers with a digest: PatchTrack 10 px (Henry2023), Platre 8 % and 25 % (Platre2024)
- Board at 16 Oct: c001-c005 present; 41f75b3 = 8759d4f plus 2 log commits
