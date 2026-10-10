# ME 295: agents for strain-rate measurement in growing roots

Course project for AM/ME/CE 295, Caltech, Fall 2026. Start with `CLAUDE.md` and `docs/context/project_summary.md`.

## How the agents run
- Each agent step is one non-interactive Claude Code call (`claude -p`) that returns one typed action as JSON
- The orchestrator (`agents/orchestrator.py`, plain Python) checks the action against fixed lists, runs it, and calls the agent again with the result. Agents run nothing themselves
- The model ID and the Claude Code version are pinned in `config/models.yaml`. A call fails if any other model answers

## Setup
1. Install Miniforge (conda-forge). On Windows, create the target folder first, then run the installer
2. Create the environment: `conda env create -f environment.yml`, then `conda activate me295`
3. Install Claude Code at the version pinned in `config/models.yaml` and sign in with your own Claude seat: `claude auth login`. No API key is used
4. Check agent calls: `python scripts/check_cli.py`. It prints the Claude Code version, login type, the model that answered, and `OK`
5. Run the offline tests: `python -m pytest -q tests`

## Tools
- Root manifest review app: `python scripts/manifest/review_server.py`, then open http://localhost:8295

Run instructions for the full system will be added as it is built.
