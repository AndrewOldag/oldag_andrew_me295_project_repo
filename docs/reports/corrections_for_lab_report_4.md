# Corrections for Lab report 4

Source: c033 audit (`results/2026-11-23_audit/findings.csv`), task c037. Each correction below is in a dated block at the end of the report it names (2026-11-23). The text above each block is unchanged.

## Corrections to submitted reports
| Finding | Severity | Report, line | Wrong statement | Correct statement | Evidence |
| :-- | :-- | :-- | :-- | :-- | :-- |
| S6-2 | blocker | LR2 :44 | Fixed script accepts all 18 decline rods | Accepts all 24 decline rods; 18 are false accepts | `results/2026-10-25_freeze_v4/README.md:18`, :26, :60-67 |
| S6-4 | blocker | LR2 :64; LR3 :39 | Diagnostician stops on `finish` | Stops on `accept` or `decline`, or at the step limit; `finish` is a dispatcher action | `agents/actions.py:152-160`; `agents/dispatcher.py:376` |
| S3-5 | blocker | LR2 :96 | Scored seeds never seen by any prompt or threshold work | Each set unseen when scored; v4 fix C1 written from v3 traces on seeds 20-22; v4 dev check on v3 seed 20 | 72173be; d75717b |
| S3-5 | blocker | LR2 :124 | v3 0.69 vs v4 0.93 given as the effect of C1-C3 | Relabelling +0.06 (0.69 to 0.75); agent change and new seeds +0.18 (0.75 to 0.93) | `results/2026-10-25_freeze_v4/README.md:79-90` |
| S6-3 | blocker | LR2 :169 | Every result folder has a README with its command | 3 folders had none at f04a286; `2026-10-09_demo_diagnostician`, `2026-10-12_heldout_faults` still have none | `git ls-tree` per folder |
| S6-9 | blocker | LR3 :13 | 101 roots, 1,189 windows | 101 roots, 1,187 windows run (2 of 0727_cc7 not run); 37 tracker errors | LR3 :169; `results/2026-10-25_full_batch_2/README.md` |
| S6-9 | blocker | LR3 :22, :126 | 17 papers | 17 files: 16 papers, one supplement | `results/2026-11-02_rag/README.md:6` |
| S6-9 | blocker | LR3 :76 | Batch 2: 90 roots | 91 roots, 90 finished | `results/2026-10-25_full_batch_2/README.md:1`, :31 |
| S6-9 | blocker | LR3 :146 | 34 `arange` errors | 33 `arange`, 1 logistic-fit failure (0721_m5 w0-2) | `results/2026-10-25_full_batch_2/README.md:17` |
| S2-3 | major | LR2 draft (2026-10-30) :55; noted in LR2 block | Plane sections about 10 times its threshold | 46 to 160 times 3.25 %/h, median 76 (41 windows) | `results/2026-10-25_real_calibration/README.md:16` |
| S6-1 | minor | LR2 draft (2026-10-30); noted in LR2 block | Draft kept with no note | Superseded by `2026-11-01_lab-report-2.md` (submitted); open `[ANDREW]` marks at :57, :90 | 71f2a3f; LR3 :172 |
| S6-5 | minor | LR2 :84 | Batch 1: 114 accepted, 9 declined | Re-scored 2026-11-02: 110 accepted, 13 declined, 3 tracker errors | 51486cf; `results/2026-10-25_full_batch_1_agents/README.md` |
| S6-6 | minor | LR2 :81, :185 | 324 passed, 3 skipped at f04a286 | No logged run; nearest logged 317 passed (2026-10-25), 352 passed (2026-11-02) | `docs/running_log.md:757`, :791 |
| S6-6 | minor | LR3 :90, :186 | 382 passed, 2 skipped (as at 71ccf6c) | 382 is the 2026-11-05 count; no run at 71ccf6c logged | `docs/running_log.md:848` |
| S6-7 | minor | LR2 :121; LR3 :27, :47 | The checker is what makes the agent work | Gap is checker output plus the roll back that depends on it; single agent also differs by one prompt sentence; 66 of 153 runs at the step limit | `README.md:45`; `docs/proposals/2026-10-12_single-agent-baseline.md` |
| S6-8 | minor | LR2 :147, :156 | Base net off the root on 24 of 28 (as a result) | Tracking-tool comparison, not a course claim; held-out error of the net used (2.4 px) stands | `results/2026-10-23_autotrace/README.md:42-44`; CLAUDE.md scope |
| S6-10 | minor | LR3 :92 | Report commands print the D2 tables | Need git-ignored run caches and rewrite the results folders; clean clone: read committed `tables.md`, `metrics.json` | `scripts/dispatcher_eval.py` cmd_report; `scripts/rag.py` cmd_report |

## Not in a report block
| Finding | Severity | Where | State |
| :-- | :-- | :-- | :-- |
| S2-3 | major | `docs/decisions.md:159` "about 10x its threshold" | Not changed by c037; same correction applies (median 76x) |
| S6-11 | minor | `README.md:29-34`, :83, :94-95 | README, not a report; not changed by c037 |
| S6-12 | minor | `README.md:37`, :128, :160 | README, not a report; not changed by c037 |

## Disclosure for Lab report 4
- S5-1: the c029 and c030 LLM caps (spec 2026-11-18 D3 450, E2 150) were counted in agent runs (one rod or one batch), not in `claude -p` calls. The planning account approved this unit (2026-11-20, `docs/decisions.md:235`); Andrew did not. By runs: c029 153 of 450, c030 90 of 150. By calls: c029 1,031 (499 + 532), c030 382. Both counts are in the results READMEs
