# ME 295: agents for strain-rate measurement in growing roots

Course project for AM/ME/CE 295 (Caltech, Fall 2026). Andrew Oldag, solo project.

A growing plant root is a slender rod whose material generates its own strain: the axial strain rate sets elongation, and its difference across the section sets the rate of bending. The strain-rate field is measured by image correlation on time-lapse movies, and that measurement can fail silently (stage drift, low texture, a second root, midline errors). This repository holds an agent system that checks each measurement against beam kinematics and either repairs it with a remedy from a fixed list or declines to report it, and the experiments that compare it with scripted and single-agent baselines on synthetic rods with known fields and on 101 real roots.

## Results at a glance

| Question | Result | Folder |
| :-- | :-- | :-- |
| Known faults (51 held-out synthetic rods, 3 repeats) | Diagnostician balanced accuracy 0.93, 0 false accepts; rule tree 0.93 with 2; fixed script 0.67 with 18; same model without the checker 0.63 | `results/2026-10-25_freeze_v4/` |
| Compound and novel faults the tree was not written for (24 + 20 rods) | Rule tree beats the diagnostician: overall 0.83 vs 0.72 and 0.75 vs 0.48; the diagnostician makes fewer false accepts on the first set (0.7 vs 4.0 per repeat) | `results/2026-11-18_heldout_compound/` |
| Integrated run, every include-yes root (101 roots, 1,189 two-hour windows) | 1,034 accepted by rule, 2 accepted after repair, 58 declined by rule, 85 declined by the agent, 4 paused; auditor on 101 roots | `results/2026-11-18_integrated_run/` |
| Does the LLM auditor catch planted errors? (30 batches, 15 plants, 3 repeats) | 8-9 of 15 caught (rule auditor 15 of 15); misses every wrong-unit plant; fewer false alarms than the rule auditor | `results/2026-11-18_auditor_check/` |
| Does the dispatcher agent schedule better than a fixed script? | No: equal or 0.5 h slower; the fixed script runs the batches | `results/2026-11-02_dispatcher_eval/` |
| Can a misplaced growth zone be caught without ground truth? | Particle-path check catches shifts of about 90 px (about 76 µm) on 78 % of real windows, 0 false alarms; smaller shifts pass | `results/2026-11-23_zone_reference/` |
| Independent audit of the whole project | 62 findings, none against a results table; fixes and corrections merged | `results/2026-11-23_audit/` |

Every results folder has a README with its setup, commands, tables and limits; `results/README.md` lists them all.

## System

| Part | Type | Job |
| :-- | :-- | :-- |
| Orchestrator | Plain Python | Validates and executes typed JSON actions; budget, step and machine limits |
| Tracker and midline nets | Tools | Stage correction, midline, strain-rate field (Quantum Borland v1, private repository) |
| Checker | Deterministic code, no LLM | Tip-displacement closure against the stage log, rigid-body invariance, Euler-Bernoulli plane sections; track-integrity gate on every remedy |
| Diagnostician | LLM agent | Names the fault behind a failed check, applies a remedy from a fixed list, accepts or declines |
| Auditor | LLM agent | Reviews each root's accepted windows, flags outliers and errors |
| Dispatcher | Fixed script (an LLM version was built and evaluated) | Splits roots into windows, submits cluster jobs within a budget |

## How the agents run
- The agents' tool interface is a set of typed actions (`agents/actions.py`). The diagnostician's tools: `request_info` (evidence from the checker and tracker), `apply_remedy` (re-run the measurement with a remedy from a fixed list), `accept` and `decline`
- Each agent step is one non-interactive Claude Code call (`claude -p`) that returns one action as JSON under a fixed schema
- The orchestrator (`agents/orchestrator.py`, plain Python) checks the action against the fixed lists, carries it out, and calls the agent again with the result, until the agent accepts, declines or reaches the step limit
- The model ID and the Claude Code version are pinned in `config/models.yaml`. A call fails if any other model answers


## Repository layout

| Path | What |
| :-- | :-- |
| `agents/` | Orchestrator, typed actions, agents, prompts, baselines (fixed script, rule tree, single agent) |
| `checker/` | Checks (no LLM), integrity gate, growth-zone checks |
| `measure/` | Measurement record, synthetic rods, remedies, scoring and metrics |
| `scripts/` | Drivers for every run (`docs/RUNBOOK.md`), ops scripts for the Windows build machine |
| `config/` | Pinned model and Claude Code version, thresholds, settings |
| `results/` | One folder per run: README, tables, traces (no raw images, no biology values) |
| `docs/` | Decisions (`decisions.md`), running log, proposals and specs, lab reports, context |
| `manifest/` | One row per root: condition, include flag, usable windows |
| `tests/` | Offline tests (no agent call, no tracker) |

## Install
1. Install Miniforge (conda-forge). On Windows, create the target folder first, then run the installer. On Windows, `conda` is not on the PATH of a plain PowerShell: use the Miniforge Prompt, or run `conda init powershell` once and open a new shell
2. Create the environment: `conda env create -f environment.yml`, then `conda activate me295` (or, without conda: Python 3.12 and `pip install -r requirements.txt`)
3. Install Claude Code at the version pinned in `config/models.yaml` and sign in with your own Claude seat: `claude auth login`. No API key is used
   - Check with `claude --version`. If it differs (Claude Code updates itself), install the pinned version: `claude install <version>`. To stop updates, set `DISABLE_AUTOUPDATER=1` in the `env` block of the Claude Code user settings
4. Check agent calls: `python scripts/check_cli.py`. It prints the Claude Code version, login type, the model that answered, and `OK`. On a version mismatch it prints `FAIL: Claude Code <found> found; config pins <pinned>` and makes no agent call
5. Run the offline tests: `python -m pytest -q tests`. The tests in `tests/test_ops.py` need `bash` on the PATH and are skipped without it
6. Before the first push, with the agents env active: `sh scripts/hooks/install.sh` installs the pre-push check (`scripts/hooks/pre_push_check.py`). On Windows, run it from Git Bash; `sh` is not on the PowerShell PATH
   - The check needs `private/blocklist.txt` in the main repo folder: one regular expression per line, `#` for comments. `private/` is git-ignored. Without the file, every push is blocked


## Try it without the data

```
python -m pytest -q tests                                   # 509 passed, 17 skipped on 2026-11-24 (no agent call, no tracker)
python scripts/demo_dispatcher.py                           # fixed-script dispatcher over every root on the fake queue, no LLM call
python scripts/demo_slice.py --runner field --no-agent --out /tmp/demo   # synthetic rod in process: measurement, three checks, error against truth
python scripts/demo_slice.py --runner remote --fault rigid_drift   # rendered rod with a fault, tracked, checked, diagnostician (needs the tracker env and Claude Code)
```

## Reproduce a result

The scored runs need the tracker (private) and, for real windows, the movies (not public). Every result can be re-tabulated from its committed outputs, and every driver restarts from its cache.

| Result | Driver (full commands in `docs/RUNBOOK.md`) | Needs |
| :-- | :-- | :-- |
| Freeze v4 | `scripts/synth/scored_v4.py plan/rules/agents/eval` | Tracker env; v4 track cache |
| Held-out compound (c029, c029b) | `scripts/synth/heldout_compound.py`, `compound_queue.py` | Tracker env or cluster; label cache |
| Auditor check (c030) | `scripts/synth/auditor_check.py plan/views/rule/llm/eval` | v4 track cache |
| Integrated run (c027) | `scripts/run_all.py windows/fetch/run/tree/report`, `scripts/retrack_queue.py` | Movies, cluster, c027 cache |
| Registration fix (c031) | `scripts/remote/register_diag.py`, `scripts/rod_jobs.py` | Cluster |
| Growth-zone checks (c034, c035) | `scripts/zone_checks.py`, `scripts/zone_reference.py` | v4 and c027 track caches |
| Dispatcher eval (c023), RAG (c024) | `scripts/dispatcher_eval.py`, `scripts/rag.py` | Run caches (git-ignored); read the committed tables otherwise |

## Data, code and rules not in this repository
- Raw movies and the tracker are lab property and stay private. Paths, hosts and access live in `private/` (git-ignored)
- Real-root biology values (strain rate, REGR, growth zone, flank) are masked in every tracked file and in the history; `tests/test_no_real_bio_values.py` fails if one comes back
- Design choices with dates and reasons: `docs/decisions.md`. Session log: `docs/running_log.md`. Rules for the build sessions: `CLAUDE.md`
- AI use: the build and planning were done with Claude (Opus 5.5) under the owner's review; the declaration is in each lab report and the final paper
