# ME 295: agents for strain-rate measurement in growing roots

Course project for AM/ME/CE 295, Caltech, Fall 2026. Start with `CLAUDE.md` and `docs/context/project_summary.md`.

## How the agents run
- The agents' tool interface is a set of typed actions (`agents/actions.py`). The diagnostician's tools: `request_info` (evidence from the checker and tracker), `apply_remedy` (re-run the measurement with a remedy from a fixed list), `accept` and `decline`
- Each agent step is one non-interactive Claude Code call (`claude -p`) that returns one action as JSON under a fixed schema
- The orchestrator (`agents/orchestrator.py`, plain Python) checks the action against the fixed lists, carries it out, and calls the agent again with the result, until the agent accepts, declines or reaches the step limit
- The model ID and the Claude Code version are pinned in `config/models.yaml`. A call fails if any other model answers

## Setup
1. Install Miniforge (conda-forge). On Windows, create the target folder first, then run the installer
2. Create the environment: `conda env create -f environment.yml`, then `conda activate me295`
3. Install Claude Code at the version pinned in `config/models.yaml` and sign in with your own Claude seat: `claude auth login`. No API key is used
4. Check agent calls: `python scripts/check_cli.py`. It prints the Claude Code version, login type, the model that answered, and `OK`
5. Run the offline tests: `python -m pytest -q tests`

## Measurement record, synthetic rods and checker
- Record format: `docs/context/measurement_record.md`. Code: `measure/record.py`
- Field-level rods (six cases, truth known): `measure/rod.py`. Checker: `checker/` (no LLM; definitions in `docs/decisions.md`). Both run in the agents env and are covered by `python -m pytest -q tests`
- Image-level rods need the tracker (Quantum Borland v1, private) in its own env (`envs/qb.yml`), on the machine where tracking runs. With that env's Python, from a copy of `measure/` and `scripts/`:
  - `python scripts/synth/run_batch.py --work DIR --case growth_zone --seeds 0 1 2 --moved-too [--fault low_texture]` renders each rod (`scripts/synth/make_rod.py`; options `--width-kappa-inv K` for the width_change curvature and `--rotation-deg R` for the rigid_rotation rate), tracks it (`scripts/remote/qb_track.py`) and writes `DIR/tracks/<id>.npz` with the truth beside it. About 13 s per rod
- Back in the agents env: `python scripts/synth/eval_rods.py --tracks DIR/tracks --out results/<date>_<name>` writes the field-level table, the image-level check values at the approved thresholds, per-seed values, truth errors, and a profile plot
- Checker thresholds: `config/checker_thresholds.yaml` (approved 2026-10-10)

## Sweeps on the shared tracker machine
- The tracker machine is shared. `scripts/synth/sweep.py` enforces the limits (`docs/decisions.md`, 2026-10-11): load check before start (1 min load at most half the cores; three 15 min retries) and before each run (pause above three quarters), at most 4 workers and one eighth of the cores, one thread per worker, `nice 19` and idle I/O, one sweep at a time (lock file), 2 h projected wall time and 10 GB of work space. Single runs through `RemoteRunner` are also load-checked and run at lowest priority
- From the agents env, with `private/runner.yaml` filled in: `python scripts/synth/fix_sweep.py start --part check`, then `status --part check`, `stop`, `fetch --part check`. `status` prints the preflight line (cores, load, memory, disk, work space, own processes) and the end line (load before and after, peak workers, wall time)
- On the tracker machine directly: `python scripts/synth/sweep.py run --plan P --work DIR`, `sweep.py status --work DIR`, `sweep.py stop --work DIR`
- Spec 2026-10-11 sweeps: `python scripts/synth/fix_sweep.py start --part P` (parts listed in the script; `--dry-run` prints the run count), `fetch --part P` copies outputs to `staging/tracks_2026-10-11/`, then `python scripts/synth/eval_fix.py --out results/2026-10-11_remedy_fixes` writes the tables
- Coupled tracking: `TrackSettings(couple=True)` or `RemoteRunner(couple=True)`; a run setting, not a remedy. Scoring tolerance: `config/scoring_tolerance.yaml` (scoring only)

## Diagnostician on a synthetic rod (one slice)
- `request_info` answers come from the measurement record and the check results (`measure/info.py`). `apply_remedy` changes the run settings (`measure/remedies.py`; table in `docs/decisions.md`), re-runs the measurement and re-checks it (`agents/executors.py`)
- Runner (`measure/runner.py`), one interface with two forms: `FieldRunner` in process for field-level rods; `RemoteRunner` renders and tracks on the machine that has the tracker. For the remote form copy `config/runner.example.yaml` to `private/runner.yaml` and fill it in (ssh host alias, work and code directories there, tracker env Python)
- `python scripts/demo_slice.py --fault displacement_exceeds_patch` renders one rod with that fault, tracks and checks it, runs the diagnostician, and prints the truth, the error before and after, and the outcome. Trace and summary in `results/<date>_demo_slice/`. `--no-agent` stops after the first check; `--runner field` runs a field-level rod in process

## Tools
- Root manifest review app: `python scripts/manifest/review_server.py`, then open http://localhost:8295

Run instructions for the full system will be added as it is built.
