# ME 295: agents for strain-rate measurement in growing roots

Course project for AM/ME/CE 295, Caltech, Fall 2026. Start with `CLAUDE.md` and `docs/context/project_summary.md`.

## How the agents run
- The agents' tool interface is a set of typed actions (`agents/actions.py`). The diagnostician's tools: `request_info` (evidence from the checker and tracker), `apply_remedy` (re-run the measurement with a remedy from a fixed list), `accept` and `decline`
- Each agent step is one non-interactive Claude Code call (`claude -p`) that returns one action as JSON under a fixed schema
- The orchestrator (`agents/orchestrator.py`, plain Python) checks the action against the fixed lists, carries it out, and calls the agent again with the result, until the agent accepts, declines or reaches the step limit
- The model ID and the Claude Code version are pinned in `config/models.yaml`. A call fails if any other model answers

## Setup
1. Install Miniforge (conda-forge). On Windows, create the target folder first, then run the installer. On Windows, `conda` is not on the PATH of a plain PowerShell: use the Miniforge Prompt, or run `conda init powershell` once and open a new shell
2. Create the environment: `conda env create -f environment.yml`, then `conda activate me295`
3. Install Claude Code at the version pinned in `config/models.yaml` and sign in with your own Claude seat: `claude auth login`. No API key is used
   - Check with `claude --version`. If it differs (Claude Code updates itself), install the pinned version: `claude install <version>`. To stop updates, set `DISABLE_AUTOUPDATER=1` in the `env` block of the Claude Code user settings
4. Check agent calls: `python scripts/check_cli.py`. It prints the Claude Code version, login type, the model that answered, and `OK`. On a version mismatch it prints `FAIL: Claude Code <found> found; config pins <pinned>` and makes no agent call
5. Run the offline tests: `python -m pytest -q tests`. The tests in `tests/test_ops.py` need `bash` on the PATH and are skipped without it
6. Before the first push, with the agents env active: `sh scripts/hooks/install.sh` installs the pre-push check (`scripts/hooks/pre_push_check.py`). On Windows, run it from Git Bash; `sh` is not on the PowerShell PATH
   - The check needs `private/blocklist.txt` in the main repo folder: one regular expression per line, `#` for comments. `private/` is git-ignored. Without the file, every push is blocked

## Measurement record, synthetic rods and checker
- Record format: `docs/context/measurement_record.md`. Code: `measure/record.py`
- Field-level rods (six cases, truth known): `measure/rod.py`. Checker: `checker/` (no LLM; definitions in `docs/decisions.md`). Both run in the agents env and are covered by `python -m pytest -q tests`
- Image-level rods need the tracker (Quantum Borland v1, private) in its own env (`envs/qb.yml`), on the machine where tracking runs. With that env's Python, from a copy of `measure/` and `scripts/`:
  - `python scripts/synth/run_batch.py --work DIR --case growth_zone --seeds 0 1 2 --moved-too [--fault low_texture]` renders each rod (`scripts/synth/make_rod.py`; options `--width-kappa-inv K` for the width_change curvature and `--rotation-deg R` for the rigid_rotation rate), tracks it (`scripts/remote/qb_track.py`) and writes `DIR/tracks/<id>.npz` with the truth beside it. About 13 s per rod
- Back in the agents env: `python scripts/synth/eval_rods.py --tracks DIR/tracks --out results/<date>_<name>` writes the field-level table, the image-level check values at the approved thresholds, per-seed values, truth errors, and a profile plot
- Checker thresholds: `config/checker_thresholds.yaml` (approved 2026-10-10)

## Sweeps on the shared tracker machine
- The tracker machine is shared. `scripts/synth/sweep.py` enforces the limits (`docs/decisions.md`, 2026-10-11): load check before start (1 min load at most half the cores; three 15 min retries) and before each run (pause above three quarters), at most 4 workers and one eighth of the cores, one thread per worker, `nice 19` and idle I/O, one sweep at a time (lock file), 2 h projected wall time and 10 GB of work space. Single runs through `RemoteRunner` are also load-checked and run at lowest priority
- Code goes to one directory per branch on the tracker machine: `<code_dir>/<branch with / replaced by _>` (`code_dir` from `private/runner.yaml`). Run from a checked-out branch; a detached HEAD is refused. The sweep lock and work directory stay shared, one sweep per machine
- From the agents env, with `private/runner.yaml` filled in: `python scripts/synth/fix_sweep.py start --part check`, then `status --part check`, `stop`, `fetch --part check`. `status` prints the preflight line (cores, load, memory, disk, work space, own processes) and the end line (load before and after, peak workers, wall time)
- On the tracker machine directly: `python scripts/synth/sweep.py run --plan P --work DIR`, `sweep.py status --work DIR`, `sweep.py stop --work DIR`
- Spec 2026-10-11 sweeps: `python scripts/synth/fix_sweep.py start --part P` (parts listed in the script; `--dry-run` prints the run count), `fetch --part P` copies outputs to `staging/tracks_2026-10-11/`, then `python scripts/synth/eval_fix.py --out results/2026-10-11_remedy_fixes` writes the tables
- The system runs uncoupled (Andrew, 2026-10-11): `couple` is a recorded run setting, false everywhere. The coupled tables are data in `results/2026-10-11_remedy_fixes/item6_clean_basis.md` and `results/2026-10-11b_padding_tolerance_coupling/b4_coupling_weight.md`. Scoring tolerance: `config/scoring_tolerance.yaml` (scoring only)
- Diagnostician on one rod: `python scripts/demo_slice.py --fault rigid_drift --size 0.5 --out results/<dir>`; `--replay` re-applies the remedies of an existing trace without calling the agent
- Held-out faults (branch `heldout/faults` until the freeze): `measure/render_heldout.py`; `make_rod.py --fault second_root|fast_rotation|bad_stage_correction|flank_swap|partial_occlusion --size Z`. Checker-only sweep: `python scripts/synth/heldout_sweep.py start` (`--dry-run` prints the run count), `status`, `fetch`, then `eval --out results/<dir>`. Proposal: `docs/proposals/2026-10-12_heldout-faults.md`

## Diagnostician on a synthetic rod (one slice)
- `request_info` answers come from the measurement record and the check results (`measure/info.py`). `apply_remedy` changes the run settings (`measure/remedies.py`; table in `docs/decisions.md`), re-runs the measurement and re-checks it (`agents/executors.py`)
- Runner (`measure/runner.py`), one interface with two forms: `FieldRunner` in process for field-level rods; `RemoteRunner` renders and tracks on the machine that has the tracker. For the remote form copy `config/runner.example.yaml` to `private/runner.yaml` and fill it in (ssh host alias, work and code directories there, tracker env Python)
- `python scripts/demo_slice.py --fault displacement_exceeds_patch` renders one rod with that fault, tracks and checks it, runs the diagnostician, and prints the truth, the error before and after, and the outcome. Trace and summary in `results/<date>_demo_slice/`. `--no-agent` stops after the first check; `--runner field` runs a field-level rod in process

## Single-agent baseline
- Same model, prompt (one sentence changed), actions, lists and step limit as the diagnostician, with no checker output in anything it sees: no check fields in the task, `check_report` answers not available, remedy results show the change only, no roll back. `agents/executors.py` (`BlindSlice`), `agents/prompts/single_agent.md`, `single_agent` in `config/models.yaml`. Definition: `docs/proposals/2026-10-12_single-agent-baseline.md`. Test: `tests/test_single_agent.py`

## Non-LLM baselines (no agent call)
- Fixed-parameter script and rule-based remedy tree: `agents/baselines.py`. The tree is fixed in `docs/proposals/2026-10-12_remedy-tree.md`. Both use the diagnostician's `Slice` (same remedies, re-runs and roll back) and write the orchestrator's outcome record
- Development faults at their frozen sizes, seeds 0-2, in rounds: `python scripts/synth/baselines.py next` starts the tracker runs still needed as one sweep (refuses while another sweep holds the lock, and past 200 runs), `status`, `fetch` (to `staging/tracks_baselines/`); repeat until `next` needs nothing. Then `python scripts/synth/baselines.py write --out results/<dir>` writes a trace and a summary per task
- Scoring: `python scripts/synth/eval_baselines.py --runs results/<dir> [--agent-runs DIR] --out results/<dir>` writes `table.md` and `scores.json` (`measure/score.py`, freeze labels)

## Scored runs (four methods)
- `python scripts/synth/scored_v1.py next --set dev|heldout` starts the tracker runs the script and remedy tree still need as one sweep; `status`, `fetch`; repeat until `next` needs nothing. Then `rules --set S`, `agents --set S --method diagnostician|single_agent` (needs a clean tracked tree; each run records the freeze tag and commit; runs with a summary are skipped), and `eval`, which writes `results/2026-10-12b_scored_v1/table_dev.md`, `table_heldout.md` and `scores.json`
- Held-out labels: `python scripts/synth/heldout_labels.py start`, `status`, `fetch`, `eval --out results/2026-10-12b_heldout_labels`

## Freeze v3 scored runs (51 rods, five methods, repeats)
- Definition: `docs/proposals/2026-10-23_freeze-v3.md`. Driver `scripts/synth/scored_v3.py`; outputs in `results/2026-10-23_freeze_v3/`; tracker cache `staging/tracks_freeze_v3/`
- Each phase: `python scripts/synth/scored_v3.py plan --phase P` (`--dry-run` prints the run count) starts one sweep of the tracker runs still needed; `status`; `fetch` after it ends; then the phase's report. Repeat `plan` until it needs nothing (registration and `enlarge_patch` states need the unremedied run first)
  1. `--phase basis`, then `basis`: clean v3 rods, seeds 10-14, against the approved thresholds and flank tolerance (`basis.md`)
  2. `--phase sizing`, then `sizing`: held-out sizes at v3 geometry, seeds 10-12 (`sizing.md`, `sizing.json`)
  3. `--phase labels`, then `labels`: labels of the 51 scored rods, seeds 20-22 (`labels.md`, `labels.json`)
  4. Tag `freeze-v3`. `--phase methods`, then `rules` (script and remedy tree), then `agents --method diagnostician|single_agent --repeat 0|1|2` (clean tracked tree needed)
  5. `eval`: metrics from `measure/metrics.py` (`table_metrics.md`, `metrics.json`, `scores.json`)
- Stops: a clean basis value over a threshold or the flank tolerance, a held-out size that changes, more than half of the labelled set in decline, or more than 600 tracker runs. Each stop is for Andrew
- On the tracker machine nothing is renamed or overwritten: outputs and rods are complete when their `.ok` marker exists; code goes to a folder per commit (`docs/decisions.md`, 2026-10-23)

## Auditor v1 (scored runs v1, no tracker runs)
- Reads the cached final records of `results/2026-10-12b_scored_v1/` from `staging/` (the scored runs' caches). Definition: `docs/proposals/2026-10-13_auditor-v1.md`
- `python scripts/synth/auditor_v1.py views` writes the 8 batch views; `rule` runs the rule auditor; `llm --set dev|heldout [--method M] [--repeat K]` runs the LLM auditor (needs a clean tracked tree); `eval` writes `results/2026-10-13_auditor_v1/scores.md`. Test: `tests/test_auditor.py`

## Task board
- One file per task in `tasks/` (format in `tasks/README.md`). Research-lane tasks use the same format in a folder outside every git repo
- Optional: copy `config/board.example.conf` to `private/board.conf` and set the research folder and the page path
- `python scripts/board.py` prints one table of all tasks; a `working` task with `last_update` older than 30 min shows as stale. `--html` also writes the local page (never inside a git repo). Test: `tests/test_board.py`

## VM heartbeat and backup by hand (Windows VM)
- Copy `config/backup.example.conf` to `private/backup.conf` and fill it in (server alias and backup folder, sources, scheduler paths)
- `powershell -File scripts/ops/install_schedule.ps1` copies `heartbeat.sh` and `hidden.vbs` to `OPS_DIR` and registers the scheduled task `me295-heartbeat`, every 5 min: it appends date and uptime to the health log; a gap over 10 min adds a `GAP` line, the first gap also writes `FIRST_GAP` beside the log. `-S4U` (elevated shell) runs it when nobody is logged on; `-Remove` unregisters it
- There is no scheduled backup. `bash scripts/ops/backup_vm.sh --conf private/backup.conf [--tag T] run` makes one backup by hand: bundles, tarballs, `SHA256SUMS`, `RESTORE.md` in a dated folder on the server, checked there with `sha256sum -c`. It never overwrites a folder and never deletes anything on the server. Test: `tests/test_ops.py`

## Tools
- Root manifest review app: `python scripts/manifest/review_server.py`, then open http://localhost:8295

Run instructions for the full system will be added as it is built.
