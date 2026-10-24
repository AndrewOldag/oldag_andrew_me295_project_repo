# Spec audit 2026-10-23: summary

Spec: `docs/specs/2026-10-23_spec-audit.md`. Lead session: spec-audit. Branch: `wip/spec-audit`. Read-only audit; no code, config, threshold, prompt or result changed.

## Counts
| Reviewer | File | Findings | Reported number | Design choice | Record only | Frozen item touched |
| :-- | :-- | --: | --: | --: | --: | --: |
| specs | `specs.md` | 21 | 0 | 2 | 19 | 2 |
| rules | `rules.md` | 11 | 0 | 4 | 7 | 1 |
| numbers | `numbers.md` | 13 | 0 | 1 | 12 | 0 |
| kinematics | `kinematics.md` | 6 | 0 | 1 | 5 | 2 |
| bending-and-tracking | `bending-and-tracking.md` | 9 | 0 | 3 | 6 | 3 |
| evaluation | `evaluation.md` | 11 | 0 | 6 | 5 | 4 |
| Total | | 71 | 0 | 17 | 54 | 12 |

- No finding is rated "would change a reported number"
- One STOP item (rules-1), below
- Reviewers kinematics and bending-and-tracking used the literature network copy on the VM (location in the private paths file). `abstract_only` depth was treated as a lead, like `metadata_only`
- Start nodes ChavarriaKrauser2008 and Krupar2026 are not in the network (bending-and-tracking, section 5)

## STOP: Andrew
- rules-1: pre-push scan over all 36 refs (18 local, 18 `origin/`): one hit, the same on every ref. Rule "absolute path", commit 304a3cb, `scripts/manifest/open_review.bat` line 5. In pushed history. Logged on 2026-10-12 and left as is by Andrew (`docs/running_log.md:215`). Listed because the spec makes any history hit a stop item
- Related, not hook hits: rules-3 and specs-20 (home-relative paths and a personal author identity on `origin/status/gate2` and in tracked inbox files; the hook does not cover these)

## Findings ranked
Severity, then reviewer order (specs, rules, numbers, kinematics, bending-and-tracking, evaluation). Full text in each reviewer file.

### Would change a reported number
- none

### Would change a design choice
| Id | Finding | Frozen item |
| :-- | :-- | :-- |
| specs-1 | Claude Code re-pin 2.1.293 -> 2.1.302 changes a freeze v2 item without a new freeze version | yes: freeze v2 section 4 |
| specs-2 | Literature-reviewer stages of the 2026-10-16 VM-setup spec (items 4-8) not done; no task file | no |
| rules-2 | Code run on the lab server renames and overwrites files there (`.part.npz` rename, `tar xf`, plan file); only `sweep.py` lock files are excepted | no |
| rules-3 | Paths outside the repo in 8 tracked lines (home-relative), not caught by the hook | no |
| rules-4 | Research-lane (other lab) work described in tracked files on the public remote; published status unknown | no |
| rules-7 | Agent single jobs on the lab server check load but not the sweep lock | no |
| numbers-1 | 118 roots in the summary, Lab report 1 and the dispatcher cost estimate match no manifest count (102 include yes); estimate +16 % | no |
| kinematics-1 | The width-free ratio keeps the width-change term on a curved rod (recomputed -0.035 to -0.435 on `width_change` at 1/400 px) | yes: `use_width_free_ratio` remedy, `width_change` label |
| bending-and-tracking-1 | Synthetic rods at 2.105 um/px; real movies 0.84 um/px. At 0.84 the rods fall below reported Arabidopsis ranges; real roots move 2.4-9.5 px/frame against 1.5 px/frame for the threshold basis rods | yes: checker thresholds, rod geometry |
| bending-and-tracking-2 | Development `low_texture` texture and focus values lie inside the real clean range (provisional reference) | yes: `low_texture` size, frame_quality reference |
| bending-and-tracking-3 | Clean bent rods bend 30 and 45 deg/h; reported Arabidopsis 16-24 deg/h; flank tolerance basis is the 45 deg/h rod | yes: scoring tolerance |
| evaluation-1 | All-decline policy scores 12 of 15 on held-out, above every method (diagnostician 11) | yes: held-out sizes and labels, scoring seeds |
| evaluation-2 | Abstention precision and recall listed as metrics; not defined or computed in code | no |
| evaluation-3 | No scored rod has accept-without-remedy as correct outcome (all 40 have a fault) | yes: scoring set, freeze v2 section 7 |
| evaluation-7 | Single-agent prompt keeps rules that need checker results it never gets; step limit in 18 of 40 runs | no |
| evaluation-8 | Single-agent baseline measures the checker, not one agent against several | no |
| evaluation-9 | Repeated-run agreement not measured; no statistic or repeat count defined | no |

### Record only
| Id | Finding | Frozen item |
| :-- | :-- | :-- |
| specs-3 | Task board does not print; `test_board.py` fails (research task state not in the state list) | no |
| specs-4 | Held-out injectors written and sized before the freeze-v2 tag | yes: held-out separation |
| specs-5 | First heartbeat gap (2026-10-17, 705 min) not shown as reported | no |
| specs-6 | Bent rods part C: 3 seeds of 5; no plot or frame images | no |
| specs-7 | `rigid_rotation` still listed clean in 2026-10-10 results | no |
| specs-8 | 11b label recompute narrowed to the frozen rods | no |
| specs-9 | Spec-done notes missing in the log for five specs | no |
| specs-10 | Task c007 done with all parts unchecked; done marker not checkable | no |
| specs-11 | Status files, roster and freeze v2 header ("Not tagged") out of date | no |
| specs-12 | Task c003 omits one server item left for Andrew | no |
| specs-13 | No running-log entry on main after 2026-10-17 | no |
| specs-14 | Auditor v1 open choices not shown decided | no |
| specs-15 | Auditor call limit counted per run, not per CLI call | no |
| specs-16 | Course-staff answer on typed actions as tool use not recorded | no |
| specs-17 | Dispatcher spec extrapolates to 118 roots | no |
| specs-18 | Conditional cluster approval not in decisions; disagrees with spec Limits and `CLAUDE.md` | no |
| specs-19 | Dispatcher spec names a process owner | no |
| specs-20 | `status/gate2` holds a VM path and a personal author identity | no |
| specs-21 | Checker definitions written alongside the code, not before | no |
| rules-1 | STOP item above | no |
| rules-5 | Access methods and one paraphrase of another person in tracked files | no |
| rules-6 | One transfer at 74 MB/s against the 50 MB/s cap (2026-10-16), logged as a deviation | no |
| rules-8 | 2026-10-10 sweeps ran before the shared-machine limits existed | no |
| rules-9 | 7 windows of roots not `include` yes staged, then replaced; never labelled or used | no |
| rules-10 | Commits after the first held-out result and before the freeze-v2 tag (order with times) | yes: diagnostician prompt, remedies, thresholds |
| rules-11 | Staged real frames kept on the VM after use | no |
| numbers-2 | "over 24 h": 7 include-yes roots have shorter usable windows | no |
| numbers-3 | Lab report 1 states the 118 difference without the spec's reason | no |
| numbers-4 | Summary date 7 Oct against the log's 8 Oct | no |
| numbers-5 | "Rotation near 7 deg/frame" has no result source | no |
| numbers-6 | "131 passed (12 Oct)" is not the 12 Oct end count (169) | no |
| numbers-7 | Lab report 1 gives 90 frames pulled; 111 were | no |
| numbers-8 | Diagnostician mean steps 5.25 shown as 5.2 | no |
| numbers-9 | "calls" counts runs in one place, model calls in another | no |
| numbers-10 | 50 MB/s transfer limit has no tracked source | no |
| numbers-11 | Agent-paper numbers in the related-work note have no source in the repo | no |
| numbers-12 | Operational numbers in the log have no result file | no |
| numbers-13 | fq-real window composition and not_clean values only in `private/` | no |
| kinematics-2 | DGCR required by `research_background.md:11`, computed nowhere | no |
| kinematics-3 | Arc-length origin called tip and quiescent centre; code uses tracked point 0 | no |
| kinematics-4 | Flank sign fixed by image geometry, not by a per-root record | no |
| kinematics-5 | Plane-sections relation in the docs has no sign and says "root width" | no |
| kinematics-6 | "Flank spacing grows 40 %/h" is linear growth | yes: `width_change` size, wording only |
| bending-and-tracking-4 | Plane-sections check uses flank-track separation (half the diameter); literature uses the full diameter | no |
| bending-and-tracking-5 | No injector for brightness change or different background | no |
| bending-and-tracking-6 | No injector for out-of-plane growth | no |
| bending-and-tracking-7 | No rod has a growth zone that moves within the window | no |
| bending-and-tracking-8 | Lower frame-rate bound and mid-window fault onset not injected | no |
| bending-and-tracking-9 | No rod has width varying along s | no |
| evaluation-4 | Held-out fault sizes set on the scored seeds (checker only) | yes: held-out sizes |
| evaluation-5 | Checker thresholds and P5 reference from clean rods sharing seeds with scored rods | yes: thresholds, P5 reference |
| evaluation-6 | Auditor prompt tuned on the dev batches whose results are reported | no |
| evaluation-10 | `paper_digests.md` has no agent-system digests | no |
| evaluation-11 | Lab guideline names five lab reports; no date for a fifth in the repo | no |

## Spec items by state
From `specs.md` section 1 (121 rows; full table there).

| Spec or proposal | Met | Partial | Not met | Not shown | Changed by decision | Other |
| :-- | --: | --: | --: | --: | --: | :-- |
| spec 2026-10-09 checker and synthetic rods | 12 | 1 | 1 | 1 | 2 | |
| spec 2026-10-10 bent rods; repair criteria | 9 | 3 | 0 | 2 | 0 | |
| spec 2026-10-11 remedy fixes | 9 | 0 | 0 | 0 | 1 | |
| spec 2026-10-11b | 5 | 1 | 0 | 1 | 0 | |
| spec 2026-10-11c | 4 | 0 | 0 | 1 | 0 | |
| spec 2026-10-12 freeze decisions | 6 | 0 | 0 | 0 | 0 | |
| spec 2026-10-12b held-out labels, scored runs | 6 | 0 | 0 | 0 | 0 | |
| spec 2026-10-13 auditor v1, real frame quality | 8 | 0 | 0 | 0 | 1 | |
| spec 2026-10-16 VM setup | 7 | 1 | 5 | 1 | 1 | 1 in progress; board met at build, fails now |
| spec 2026-10-23 next steps; spec audit | 0 | 0 | 0 | 2 | 0 | 4 in progress, 3 not started, 2 not yet due |
| proposal 2026-10-09 structured actions | 2 | 0 | 0 | 1 | 0 | |
| proposal 2026-10-11 freeze v1 | 0 | 0 | 0 | 0 | 1 | |
| proposals 2026-10-12 (freeze v2, misses, held-out, remedy tree, single agent) | 8 | 1 | 0 | 1 | 1 | 1 stale |
| proposal 2026-10-13 auditor v1 | 2 | 0 | 0 | 1 | 0 | |
| proposal 2026-10-23 dispatcher | | | | | | out of scope (not approved) |
| Total | 78 | 7 | 6 | 11 | 7 | 12 |

Items not met, partial or not shown:
- Not met: 2026-10-09 item 6 held-out injectors after the tag (specs-4); 2026-10-16 items 4-8 literature-reviewer stages (specs-2)
- Partial: 2026-10-09 item 4 definitions before code (specs-21); 2026-10-10 B `rigid_rotation` out of clean group (specs-7), C2 seeds, C3 plots (specs-6); 11b item 2 label recompute (specs-8); 2026-10-16 item 9 decision lines (specs-2); freeze v2 real frame_quality reference (task c002)
- Not shown: spec-done notes for 2026-10-09, 10-10 (two), 11b, 11c (specs-9); 2026-10-16 first heartbeat gap (specs-5); 2026-10-23 B2-B4 and c010 (not yet done); typed actions as tool use (specs-16); held-out branch readable before the freeze (specs-4); auditor run statistics and run id lists (specs-14)

## Needs Andrew to check the paper
No finding rated "would change a reported number" rests on a metadata-only source. These checks would raise lead-level sources to evidence:

| Paper key | Depth | What to check | Findings |
| :-- | :-- | :-- | :-- |
| ChavarriaKrauser2006 | abstract_only | DGCR definition; sign and width (2R or flank spacing) in the flank-difference relation; width-change term in curvature conservation | kinematics-1, -2, -5; bending-and-tracking-4 |
| SilkErickson1978 | abstract_only | Equation form; flank sign (outer minus inner); apex as origin | kinematics-3, -4, -5 |
| Silk1984 | metadata_only | Curvature and differential-growth formula that BastienEtAl2014 calls equivalent; material derivative | kinematics-5 |
| SilkErickson1979, EricksonSax1956 | metadata_only | Origin and velocity reference (tip or QC) | kinematics-3 |
| WolvertonEtAl2002 | full_text, values read from plots | Fig. 6 maximum curvature rate (about 24 deg/h); Fig. 2 REGR peak and position | bending-and-tracking-3; values table |
| ChauvetEtAl2016 | full_text; digest gives two forms | Which offset R refers to; digest forms imply a factor 2 | bending-and-tracking-4 |
| BastienEtAl2016 (KymoRod) | abstract_only | Width in its curvature relation; failure modes reported | bending-and-tracking-4; failure-mode table |
| ReAct (Yao et al. 2023) Table 2; Geifman and El-Yaniv 2017, ImageNet result; Wei et al. 2025 | no digest in the repo | Numbers quoted in the related-work note | numbers-11 |

Other checks for Andrew, not papers:
- Syllabus: is there a fifth lab report, and its date (evaluation-11)
- Whether the research-lane material on `origin/status/gate2` and in tracked inbox files is published (rules-4); home-relative paths and author identity there (rules-3, specs-20)

## Next
- spec-audit-check: verifies the 17 design-choice findings, 10 record-only findings (seed 0) and 10 literature citations; writes `CHECK.md`
- Andrew: marks each finding accepted or rejected in the reviewer files. A finding that changes a frozen item needs a new freeze version

## Marks
- Marked by Andrew 2026-10-24 (written by the audit-marks session at his direction): all 71 findings accepted; 13 handled (freeze v3 / v3.1), 17 fixed, 2 known limit (report), 39 no action. Marks on each `- Andrew:` line in the reviewer files
