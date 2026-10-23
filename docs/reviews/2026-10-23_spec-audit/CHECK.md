# Spec audit 2026-10-23: independent check

Spec `docs/specs/2026-10-23_spec-audit.md`, section "spec-audit-check". Session spec-audit-check, branch `wip/spec-audit-check` from `wip/spec-audit` at 6b33b84. Read-only.

- Read: `CLAUDE.md`, the spec, the six reviewer files, `SUMMARY.md`, and the sources each checked finding cites. Not read: `.claude/agents/audit-*.md`, session traces or transcripts
- Code, config and results at `origin/main` (c730662). The worktree equals `origin/main` for every cited code, config and result file
- Literature: the VM copy of the network (location in the private paths file), `digests/` and `papers.json` only. No PDF opened. No file in `articles/` opened
- No agent call, no tracker run, no server access. Recomputations: `measure/rod.py` and `measure/info.py` (numpy, under 1 s each), `scores.json` replay, `scripts/hooks/pre_push_check.py`
- Reviewer files not edited

## Counts
| Reviewer | Design choice checked | Confirmed | Record only sampled | Confirmed | Citations sampled | Confirmed | Not reproduced | Wrong location |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| specs | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 |
| rules | 4 | 4 | 3 | 3 | 0 | 0 | 0 | 0 |
| numbers | 1 | 1 | 4 | 4 | 0 | 0 | 0 | 0 |
| kinematics | 1 | 1 | 0 | 0 | 3 | 3 | 0 | 0 |
| bending-and-tracking | 3 | 3 | 1 | 1 | 7 | 7 | 0 | 0 |
| evaluation | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Total | 17 | 17 | 10 | 10 | 10 | 10 | 0 | 0 |

- No finding is rated "would change a reported number", so none was checked under that rating
- Severity counts in `SUMMARY.md` match the reviewer files: 71 findings; 17 design choice, 54 record only, 0 reported number; 12 with a frozen item
- Minor line offsets inside otherwise confirmed findings are listed in the tables below. None moves the main evidence

## Samples (seed 0)
- Method: Python `random.Random(0).sample(population, 10)`
- Record-only population: the 54 ids in the order of the `SUMMARY.md` "Record only" table (specs-3 ... evaluation-11)
- Drawn: rules-10, bending-and-tracking-9, numbers-2, specs-5, specs-19, numbers-8, numbers-7, rules-11, rules-1, numbers-6
- Citation population: 33 (finding, paper, location) pairs from the Source lines of the kinematics and bending-and-tracking findings, in file order: k-1 BastienEtAl2014 Eq 3/5/7/8; k-2 ChavarriaKrauser2006 abstract; k-2 BastienEtAl2014 Eq 15; k-3 HenryEtAl2023 Results sec. 2; k-3 BeemsterBaskin1998 velocity method; k-3 WolvertonEtAl2002; k-3 IshikawaEvans1992; k-3 SilkErickson1978 abstract; k-4 BastienEtAl2014 Eq 3, Fig 2; k-4 Mullen1998 (`paper_digests.md`); k-5 BastienEtAl2014 Eq 3; k-5 BastienMeroz2016 Eq 13; bt-1 HenryEtAl2024 Reported numbers; bt-1 HenryEtAl2023 Abstract; bt-1 BeemsterBaskin1998 Fig 2 legend, Table I; bt-2 HenryEtAl2023 Results/Methods; bt-2 MooreEtAl2013 Methods; bt-3 MullenEtAl1998b Table I; bt-3 WolvertonEtAl2002 Fig 6; bt-3 MooreEtAl2013 Reported numbers; bt-4 BastienEtAl2014 Equations; bt-4 ChauvetEtAl2019 Eq 1; bt-4 HartmannEtAl2021 Equations; bt-5 HenryEtAl2023 Definitions; bt-5 BasuEtAl2007 Reported numbers; bt-6 MullenEtAl1998b Methods; bt-6 HenryEtAl2023 System; bt-7 BaskinEtAl2020 Results; bt-7 HenryEtAl2024 Reported numbers; bt-7 BastienEtAl2018 Reported numbers; bt-8 HenryEtAl2023 Definitions; bt-8 MooreEtAl2013 Methods; bt-9 BasuEtAl2007 Reported numbers

## Design-choice findings (all 17)
| Id | Result | Reproduced |
| :-- | :-- | :-- |
| specs-1 | confirmed | `git diff freeze-v2 origin/main -- config/models.yaml`: version line 2.1.293 -> 2.1.302; `config/models.yaml:6`; `docs/decisions.md:121`; freeze v2 section 4 at `docs/proposals/2026-10-12_freeze-v2.md:54-56`; one tag (`freeze-v2`), no freeze v3 file |
| specs-2 | confirmed | `git log --all` on `docs/lit`, `tests/lit`, `.claude/agents/lit-*`: no commits; no `eval/*` branch; no commit message with "pitfall" or "Paper2Agent"; no papers folder in `private/`; no task file for items 4-9 (c001-c010 listed); items 4-8 in `docs/specs/2026-10-16_vm-setup.md` |
| rules-2 | confirmed | `scripts/remote/qb_track.py:126`, `:134` (`.part.npz`, `os.replace`); `origin/wip/dispatcher` `:154`; `measure/runner.py:166` (`tar xf -` into the code directory), `:197` (`cat >` plan file); `docs/decisions.md:54` records the rename design; `CLAUDE.md:35` excepts only the sweep lock files. Note: `origin/wip/dispatcher` (bebc1ff) now lists three timing runs (t1-t3), not two |
| rules-3 | confirmed | `git grep -n "~/"` on `origin/main`: 7 text lines at the cited file:line pairs; `origin/status/gate2:docs/agents/status/gate2.md:16`: 1; total 8. `PATH_RE` does not match a tilde path. Line offset: `PATH_RE` is at `scripts/hooks/pre_push_check.py:52`, not `:49` |
| rules-4 | confirmed | `docs/agents/inbox/gate2.md` 26 lines; `origin/status/gate2:docs/agents/status/gate2.md` 16 lines, with a pass/fail line; inbox files of data-steward, litreview, spec-audit-r exist. Published status not stated in the repo; Andrew's decision |
| rules-7 | confirmed | `measure/runner.py:176-180` `_load_ok` (load only), called at `:240` and `:258`; no lock check on that path; `scripts/synth/scored_v1.py` `agents` branch (`:388` on) has no `sweep_status` call; `next` and `fetch` check at `:355` and `:373` (finding says `:374`); log line 304: 96 sweep runs, 22 single jobs |
| numbers-1 | confirmed | manifest 123 rows: yes 102, unsure 11, no 10; yes + unsure 113; no subset 118. `CLAUDE.md:6` "each of 118 roots"; lab report 1 `:79`; dispatcher spec `:40`. 118 / 102 = 1.157. Note: `origin/wip/dispatcher` timing README now gives the 118-root figure as the worst case and a separate include-yes figure |
| kinematics-1 | confirmed | `width_free_ratio` (`measure/info.py`) on `width_change_spec` (`measure/rod.py`): 1/400 px, 12 points, -0.435 to -0.035; 1/800 px, 12 points, -0.214 to -0.017; `growth_zone` 0.0. `measure/rod.py:10-13` formula; `measure/score.py:78-84` skips the flank term when the ratio is reported; `research_background.md:16` "has no width in it" |
| bending-and-tracking-1 | confirmed | `pixel_um=2.105` at `measure/rod.py:153`, `measure/render.py:284`; no `docs/decisions.md` line for 2.105; recomputed peak REGR 43.4 %/h at 150 px, zone (> 20 % of peak) 49-251 px = 202 px; at 2.105 um/px: 126 um/h, 316 um, 425 um; at 0.84: 50 um/h, 126 um, 170 um; 0.08-0.32 mm/h at 0.84 um/px and 90 s: 2.38-9.52 px/frame. Reported ranges match the HenryEtAl2024, HenryEtAl2023 and BeemsterBaskin1998 digests (all full_text) |
| bending-and-tracking-2 | confirmed | `measure/render.py:71-72` (contrast 0.03, blur 2, noise 40); `config/frame_quality_reference.yaml:8-9`, `:22-23`; dev trace `diagnostician_low_texture_s1`: texture_contrast 0.0598-0.0599, focus 0.0351-0.0354 (above real clean lowest 0.0439; focus above real clean median 0.0286); thresholds comment `low_texture >= 152` |
| bending-and-tracking-3 | confirmed | `measure/rod.py:236-237`: `_turning(30.0, 40.0)` and `_turning(45.0, 40.0)` per hour; `config/scoring_tolerance.yaml:12-13` basis bend_reverse s0, 0.797. MullenEtAl1998b digest: 18 deg/h mean, 22 +- 8 and 16 +- 5 (Table I); WolvertonEtAl2002 digest: Fig. 6 fitted maximum about 24 deg/h |
| evaluation-1 | confirmed | replay of `scores.json` labels: dev 15 repairable / 10 not; held-out 3 / 12. All-decline: dev 10, held-out 12, total 22. Methods correct (dev, held-out): diagnostician 24, 11; remedy tree 24, 9; single agent 11, 7; script 10, 3 |
| evaluation-2 | confirmed | `git grep -i "precision|recall|abstain"` in `measure`, `agents`, `audit`, `scripts`, `checker`, `config`, `results`: 0 hits; listed at `project_summary.md:33`. Table recomputed: declines and correct declines diagnostician 19 / 18, remedy tree 17 / 16, single agent 10 / 9; accepted 20, 23, 12; single agent not_reported 18 |
| evaluation-3 | confirmed | `scripts/synth/scored_v1.py:78-80`: every scored rod is `Rod("growth_zone", f, s, size=z)` over the fault dict; no clean rod in the scored set |
| evaluation-7 | confirmed | `agents/prompts/single_agent.md:10`, `:11`, `:16`, `:18`; `agents/executors.py:143-154` returns `rerun`, `change`, `settings_left`; `docs/decisions.md:95` replaces one prompt sentence only. Step limit: single agent 13 of 25 dev, 5 of 15 held-out; diagnostician 1 of 40 |
| evaluation-8 | confirmed | `docs/proposals/2026-10-12_single-agent-baseline.md:6` "Measures what the deterministic checker adds"; no baseline file or result with one agent doing the dispatcher, diagnostician and auditor jobs |
| evaluation-9 | confirmed | `scores.json` 160 records, one per method x rod; `project_summary.md:30`, `:33`; `Project-Guideline.md:23`; auditor README has a `--repeat` option and per-repeat counts, no agreement statistic |

## Record-only sample (10)
| Id | Result | Reproduced |
| :-- | :-- | :-- |
| rules-10 | confirmed | commit times of the 14 listed commits match; diagnostician prompt blob sha256 prefix 83ba54768d332ae4 at `freeze-v2` and `origin/main`, in 210 `system_sha` fields; single agent c8a9d43830928498 in 272; auditor prompt at aa8483a 2541926380a9e924; `git diff freeze-v2 origin/main` on the frozen paths: `agents/actions.py` only. Note: 46a9d6f time is given in UTC (2026-10-14 04:58 +0000 = 2026-10-13 21:58 Pacific), while the list header says Pacific |
| bending-and-tracking-9 | confirmed | `measure/rod.py:54-55` `h(t)` and `dh(t)` take time only; `width_change_spec` (`:198-209`) varies h in time only. BasuEtAl2007 digest: diameter smallest near the tip, nearly constant from about 1.5 mm (bean) |
| numbers-2 | confirmed | manifest: 9 rows with `usable_to_h` below `duration_h` (9.5, 10, 12, 17.5, 18 x4, 20 h); 7 include yes; durations 23.63-24.01 h in those rows |
| specs-5 | confirmed | VM health log: 7 gap lines 2026-10-17 to 2026-10-23; first 2026-10-17 01:40 to 13:25, 705 min; two 2026-10-18 lines with the same start end 74 s apart; `FIRST_GAP` marker present; no tracked log, status or task line reports it (running_log.md:408 lists it as remaining) |
| specs-19 | confirmed | `origin/main:docs/specs/2026-10-23_next-steps-lr2-dispatcher.md:40` has a login-like name in backticks in "check for other ... jobs first". Name not repeated here |
| numbers-8 | confirmed | `scores.json`: diagnostician 128 + 82 = 210 steps over 40 runs = 5.25; shown as 5.2 |
| numbers-7 | confirmed | lab report 1 `:26` "90 frames pulled"; running_log.md:337 (90), :349 (21 more), :350 (replaced frames removed) |
| rules-11 | confirmed | `staging/fq_real_labeling/frames/` 90 files, `view/` 30 files in the main checkout; running_log.md:374 keeps them until Andrew says to delete |
| rules-1 | confirmed | `pre_push_check.py --commits origin/main`: 175 commits, 1 hit, rule "absolute path", 304a3cb, `scripts/manifest/open_review.bat:5`; `origin/wip/spec-audit`: 188 commits, the same single hit. Pattern not printed |
| numbers-6 | confirmed | lab report 1 `:22` "131 passed (12 Oct)"; running_log.md:229 (131), :310 (169, scored-v1 entry of 2026-10-12), :253 (report cites last logged count at drafting) |

## Literature citations (10)
Depth for each key from `papers.json` matches the depth the reviewer states.

| Finding | Paper key (depth) | Cited location | Digest | Result |
| :-- | :-- | :-- | :-- | :-- |
| bending-and-tracking-5 | BasuEtAl2007 (full_text) | Reported numbers: correlation search had more difficulty when the root grew over a background different from the reference image | Reported numbers, same statement | confirmed |
| bending-and-tracking-6 | HenryEtAl2023 (full_text) | System: plates at 80 deg "to promote root growth along the coverslip surface" | System, same quote | confirmed |
| kinematics-2 | ChavarriaKrauser2006 (abstract_only) | abstract: DGCR is the spatial derivative of the tropic speed; dkappa/dt underestimated production | Equations and Conclusions (from the abstract), same statements; reviewer treats it as a lead | confirmed |
| kinematics-4 | BastienEtAl2014 (full_text) | Eq 3, Fig 2: sides named upper (1) and lower (2) within the bending plane | Equations, Eq 3 note, same | confirmed |
| bending-and-tracking-2 | MooreEtAl2013 (full_text) | Methods: blur from lid condensation as a failure mode | Methods, replication line, same quote | confirmed |
| bending-and-tracking-2 | HenryEtAl2023 (full_text) | Results and Methods: endogenous cell walls and air spaces, no applied markers | System (states "The Results describe" cell walls and intercellular air spaces) and Methods (no fiducial marks) | confirmed |
| bending-and-tracking-1 | HenryEtAl2024 (full_text) | Reported numbers: RIL ranges 0.08-0.32 mm/h, peak position 0.25-0.57 mm, zone 0.25-0.8 mm | Reported numbers, trait ranges, same values | confirmed |
| bending-and-tracking-6 | MullenEtAl1998b (full_text) | Methods: two cameras at right angles for circumnutation | Methods, same quote | confirmed |
| kinematics-4 | Mullen1998, repo `paper_digests.md` (read in full) | upper minus lower | `paper_digests.md:16-18`, "upper-minus-lower difference" | confirmed |
| bending-and-tracking-7 | BaskinEtAl2020 (full_text) | Results: saltation 17 um per 5 min, span about 75 um, period about 90 min | Reported numbers (paper text quoted), same values | confirmed |

## Not checked
- The other 44 record-only findings and the 23 unsampled citations
- Claims that rest on lead-level sources (abstract_only, metadata_only) beyond the one sampled: those are listed in `SUMMARY.md` "Needs Andrew to check the paper"
- Whether each finding is accepted: Andrew marks the reviewer files
