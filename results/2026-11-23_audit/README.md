# Independent audit before Lab report 4 (c033)

Spec `docs/specs/2026-11-23_audit.md`. Session `audit`, branch `wip/audit`, 2026-11-23. Read-only audit of `origin/main` and all branches. No code, config or result outside this folder was changed. No cluster, tracker or project-agent runs.

## Summary
| Section | Blocker | Major | Minor |
| :-- | --: | --: | --: |
| 1 Rules over history | 0 | 6 | 2 |
| 2 Equations | 0 | 2 | 4 |
| 3 Freezes and held-out sets | 1 | 1 | 4 |
| 4 Results recompute | 0 | 0 | 9 |
| 5 Decisions from 2026-11-18 | 0 | 1 | 9 |
| 6 Lab reports 1-3 and README | 4 | 0 | 8 |
| 7 Reproducibility | 0 | 2 | 9 |
| Total | 5 | 12 | 45 |

- All findings: `findings.csv` (columns `id,section,severity,where,what,evidence,fix`). Built by `python scripts/merge_findings.py` from the section CSVs
- Detail, evidence and the "checked, no finding" lists: `s1_rules.md` to `s7_repro.md`
- Severity alignment: a factual error in a submitted lab report is `blocker` (spec definition). S3-5 was raised from minor to blocker for this reason. S2-3 stays major: the wrong ratio is only in the superseded LR2 draft (`2026-10-30`), not in the submitted one (`2026-11-01`, per S6 reading of commit 71f2a3f and LR3)
- Wording errors in results READMEs that change no reported number (S3-3, S4-1, S4-9) are kept minor
- No table that can be recomputed from committed files disagrees with its README (section 4). The blockers are report wording and counts, not scored results

## Blockers
- S3-5: LR2 (submitted) :96 says scored seeds were never seen by prompt or threshold work; v4 prompt fix C1 came from v3 traces on scoring seeds 20-22. :124 compares v3 0.69 with v4 0.93 without the relabelling split
- S6-2: LR2 :44 "fixed script accepts all 18 decline rods"; freeze v4 has 24 decline rods, 18 is the false-accept count
- S6-3: LR2 :169 "every result folder has a README with its command" is false
- S6-4: LR2 :64 and LR3 :39 say the diagnostician stops on `finish`; it stops on `accept` or `decline`. `finish` is a dispatcher action
- S6-9: LR3 has four counts off by one item (papers, batch-2 `arange` errors, batch-2 roots, windows through the checker)

## Major
- S1-1: 19 pushed status commits carry an author email that names a user account and a machine domain. The pre-push hook does not scan author fields
- S1-2: cluster name in pushed history of two inbox files (12 hook hits, 7 commits); clean at tip, not recorded as known hits
- S1-3: `results/2026-11-18_integrated_run/example_traces.md:17` has an unmasked real-root strain-rate profile; line 3 says values are masked
- S1-4: real-root biology values remain at the tip of main in the 10-24 real-slice traces and one proposal
- S1-5: real-subset REGR and growth-zone files remain in pushed history (disclosed in decisions; repo goes public)
- S1-6: two remote scripts renamed files on the lab server 2026-10-13 to 10-25 (disclosed and fixed)
- S2-1: integrity gate passes a track whose centre points are lost (2 of 81 points tracked passes); effect on committed remedied tracks not checkable on this VM
- S2-3: superseded LR2 draft :55 says plane sections noise is about 10 times its threshold; committed numbers give over 70
- S3-1: real frame_quality reference includes window 0727_cc7 8.5-9.5 h, outside the usable window since 696784d; not recomputed. Effect on medians is in the fourth decimal
- S5-1: c029 and c030 caps changed from LLM calls to agent runs; approved by the planning account, not Andrew; spec text unchanged. Both counts are in the READMEs
- S7-1: `run_batch.py` commands in two results READMEs omit the required `--work` flag
- S7-2: real-subset report and agreement commands read `summary.json` files that were removed from the tree

## Minor (45)
- Section 1: S1-7 ledger gaps (actual cost missing on 63 rows; no committed ledger after 2026-11-05); S1-8 backup script still runs commands on the lab server (not run since 2026-11-04)
- Section 2: S2-2 inversion count includes ties from clamped midline ends; S2-4 superseded decision not marked; S2-5 centre-tolerance jump near zero peak (no scored rod affected); S2-6 founding spec sign and wording
- Section 3: S3-2 register_v2 in c029/c029b not disclosed; S3-3 c029 run record commit range and changed files; S3-4 integrated windows overlap calibration windows, not disclosed; S3-6 no list of ft2 training traces
- Section 4: S4-1 to S4-9 (integrated-run numbers from git-ignored staging, empty auditor column, "(cap 900)" label, freeze v4 table ranges, untraceable tracker totals, registration-fix frame range 21-79 not 21-80)
- Section 5: S5-2 to S5-10 (cap 900 to 1,300 after results seen, set-aside records not disclosed, overnight build-session deviations without approval, lateral floor attribution, register_v2 limit missing from failure modes, "all windows final", 101 vs 102 roots, memory rule entry, spec 2026-11-18 not amended)
- Section 6: S6-1, S6-5 to S6-8, S6-10 to S6-12 (superseded draft not marked, pre-rescore counts, test counts, "checker is what makes the agent work", midline-net comparison scope, demo commands, stale README sections)
- Section 7: S7-3 to S7-11 (writes into non-ignored folders, date-based default outputs, unstated external inputs in 11 READMEs, private configs only in session worktrees, environment not named, no command in 4 READMEs, summary rewrite drops rows, multi-pair `--track`, step-1 commit)

## Checked, no finding (main items)
- Secrets and tokens in history: none
- Deletes on the lab server: none. Cluster deletes go through `DELETED.log`
- Cluster spend: highest running total $8.51 of $15; stated figures match the ledger
- GPU type: P100 or V100 only; no mismatch
- Lab-server jobs after 2026-11-04: none
- Checker, closure, plane-sections and rigid-invariance signs and units on synthetic inputs with known answers; all thresholds match decisions and reports; 79 checker tests pass
- Freeze v3, v4, c029, c029b, c030: labels, plants, thresholds and prompts committed before the first scored run
- Usable windows: 1,274 of 1,281 tracked root-window items in rule; the other 7 are the replaced fq-real candidates listed in a review
- All recomputable tables in the five results folders match; `measure/metrics.py` reproduces every `metrics.json`
- c029b selection rule reproduced (20 of 20, same order)
- All cited paths and commit hashes in LR1-3 and README resolve; 31 README entry points run with `--help`

## Not checked
- Committed remedied real tracks against S2-1 (tracks not on this VM)
- Cluster-side `DELETED.log` contents
- Pixel size across experiments for the single px/h closure threshold
- Lab report 4: no draft exists yet

## Scripts
- `scripts/s1_*.py` to `scripts/s7_*` and `scripts/merge_findings.py`. Private inputs are passed as arguments; no path outside the repo is stored
