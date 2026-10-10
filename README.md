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
  - `python scripts/synth/run_batch.py --work DIR --case growth_zone --seeds 0 1 2 --moved-too [--fault low_texture]` renders each rod (`scripts/synth/make_rod.py`), tracks it (`scripts/remote/qb_track.py`) and writes `DIR/tracks/<id>.npz` with the truth beside it. About 13 s per rod
- Back in the agents env: `python scripts/synth/eval_rods.py --tracks DIR/tracks --out results/<date>_<name>` writes the field-level table, the image-level check values and truth errors, and a profile plot
- Checker thresholds: `config/checker_thresholds.yaml`. Provisional until approved

## Tools
- Root manifest review app: `python scripts/manifest/review_server.py`, then open http://localhost:8295

Run instructions for the full system will be added as it is built.
