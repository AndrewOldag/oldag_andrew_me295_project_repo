# ME 295 project: agents for strain-rate measurement in growing roots

Read this file at the start of every session. Detail is in `docs/context/`. New instructions arrive as files in `docs/specs/`; read any spec you have not acted on before starting work.

## Summary (final, submitted)
A growing plant root is a slender rod whose material generates its own strain: the axial strain rate sets elongation, and its difference across the section sets the rate of bending. This project develops a multi-agent system that measures this strain-rate field by digital image correlation on time-lapse movies, in which one agent schedules tracking jobs on a computing cluster within a cost budget, a second tests each result against beam kinematics and either repairs a failed measurement or declines to report it, and a third audits the batch; the system is evaluated against scripted and single-agent baselines on synthetic rods with known fields. The scientific aim is a strain-rate map with a stated confidence level for each of 118 roots over 24 h of osmotic loading and recovery, to determine whether a self-straining material responds to a change in load by rescaling or reshaping its growth zone, and whether strain remains balanced across the section during that response.

## Roles
- Andrew Oldag: owner. Solo project for AM/ME/CE 295, Caltech, Fall 2026
- Build account: builds, runs and tests the system
- Planning account: planning, design decisions, research context. It writes specs into `docs/specs/`. It does not edit code unless a spec says so
- Both accounts are declared in the AI Use Declaration. Keep the running log accurate so the declaration can be written from it

## System
| Part | Type | Job |
| :-- | :-- | :-- |
| Dispatcher | LLM agent | Splits roots into root-by-window tasks, estimates cost, submits tracking jobs |
| Tracker and midline nets | Tools | Stage correction, midline, strain-rate field (Quantum Borland v1) |
| Checker | Deterministic code, no LLM | Rigid-body invariance, tip-displacement closure against the stage log, Euler-Bernoulli kinematics |
| Diagnostician | LLM agent | Names the fault behind a failed check, picks a remedy from a fixed list, or declines to report |
| Auditor | LLM agent | Reviews the batch, flags outlier roots, compares control with stressed, writes the report with provenance |

- Human approval: any compute budget before jobs are submitted; any threshold change; any action that deletes or overwrites data
- Build order: checker and diagnostician, then dispatcher, then auditor. Cut in reverse order
- Baselines: fixed-parameter script, rule-based remedy tree, single-agent version. A parameter search is a further baseline if time allows
- Evaluation: synthetic rods with prescribed velocity fields and injected faults (truth known); fixed non-growing roots (zero strain); a 12-16 root subset of the real movies for baselines and repeated runs; all roots once, unattended

## Rules
- This repository will be public. Nothing in a tracked file names a machine, a user account, a path outside the repo or an access method. No comments or feedback from other people. If unsure, ask Andrew
- Private context (machines, access, data layout, other people's comments) lives in `private/`, which is git-ignored. Read it. Never copy from it into a tracked file
- Nothing unpublished from other lab work appears in this repo or in anything submitted for the course. If unsure whether something is published, ask Andrew
- Raw data is not in this repo. Never copy a whole experiment folder to the build machine. Stage one root at a time and delete staged images after use
- Tracking runs on the lab compute server by default. The computing cluster is used only after Andrew approves a cost estimate
- No Claude session deletes, moves or renames any file or folder on the lab server, by any means. Andrew deletes there himself, at the end of the project. Only exception: the lock files `scripts/synth/sweep.py` creates and removes for its own sweep. If a step needs a server delete, stop and tell Andrew (Andrew, 2026-10-13)
- The lab compute server is shared. Every job there: at most 4 single-thread workers, lowest priority, load checked before and between runs, one sweep at a time. Limits in `docs/decisions.md`, 2026-10-11
- The checker contains no LLM calls
- Remedies come from a fixed list set in advance. No free parameter tuning on data that may go into paper figures
- Pin the model ID in config. Never commit API keys, tokens or SSH keys
- The course paper makes claims about agent behaviour only. Tracker comparisons and biology results belong to other lab work and are out of scope
- Coupled and uncoupled results on synthetic rods may be committed (Andrew, 2026-10-11). They are data, not a claim
- Kinematics only. Do not claim stress, stiffness or a constitutive law
- Write in a plain, flat, declarative style. Short bullets. No flourish
- Follow the logging and pushing routine below in every session

## Logging and pushing
Lab reports are due every two weeks and are written from this repo. Keep it current so that a report is a copy of the log.

- Remote: `origin` is the GitHub repository. Work on `main`
- Start of session: `git pull --rebase`. Read this file, any new spec, and the last log entry
- Commit after each piece of work that runs or passes its test. One change per commit. The message says what changed in one line
- Push after every commit. Participation is graded from commit activity on GitHub, so unpushed work does not count
- Unfinished work that breaks the README run steps goes on a branch named `wip/<name>`, pushed the same way
- Parallel sessions write their log entry to docs/running_log_pending/<name>.md on their branch; the coordinator moves it into docs/running_log.md at merge.
- Before each commit read `git diff --cached` and check it against the first three rules above
- End of session: log entry written, nothing uncommitted, nothing unpushed. `git status` is clean and `git log origin/main..main` is empty

Log entry, appended to `docs/running_log.md` at the end of every session and after any milestone inside one:

```
## YYYY-MM-DD (build account, session N)
- Done: what was built or run, with file names, commands, numbers and commit hashes
- Demo: one command that shows the current state, and what it prints or writes
- Remaining: next steps, in order
- Bottlenecks: what is blocked, and on whom
```

- State results as measured: tests passed and skipped, run times, counts. A failed run is logged as failed
- One line per item

Keep these current, in the same commit as the change they describe:
- `README.md`: install and run steps. Another student must be able to install and run the system from it
- `docs/decisions.md`: each design choice, with its date and reason
- `results/<date>_<name>/`: small outputs a report can point to (plots, tables, short traces). No raw images

Lab reports go in `docs/reports/`, one file per report, started from `docs/reports/TEMPLATE.md`. Andrew writes them from the log.

## Where things are
- Roots: `manifest/root_manifest.csv`, one row per root position, with conditions and usable windows
- Papers: `docs/context/literature/paper_digests.md`. PDFs are not committed
- Tracker code: Quantum Borland v1, a separate private repository. Its environment is `envs/qb.yml`
- Agents environment: `environment.yml`. Model settings: `config/models.yaml`

## Dates
- Lab report 1: Fri 16 Oct (related-work note, repo and environment, running log, draft proposal)
- Lab report 2: Fri 30 Oct (1-page proposal; commitment point)
- Lab report 3: Fri 13 Nov (smallest slice running end to end)
- Lab report 4: Mon 23 Nov (integrated run; failure modes)
- Presentation: Wed 2 Dec. Final report and repository: Wed 9 Dec (syllabus deliverables table)

## Context files
- `docs/context/project_summary.md`: design, evaluation, limits, open items
- `docs/context/research_background.md`: quantities, mechanics relations, the tracker and its limits
- `docs/context/course/`: course guidelines
- `docs/context/literature/paper_digests.md`: digests of 26 papers
