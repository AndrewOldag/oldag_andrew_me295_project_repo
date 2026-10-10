# ME 295: agents for strain-rate measurement in growing roots

Course project for AM/ME/CE 295, Caltech, Fall 2026. Start with `CLAUDE.md` and `docs/context/project_summary.md`.

## Setup
1. Install Miniforge (conda-forge). On Windows, create the target folder first, then run the installer
2. Create the environment: `conda env create -f environment.yml`, then `conda activate me295`
3. Set `ANTHROPIC_API_KEY` as an environment variable, or copy `.env.example` to `.env` and fill it in. `.env` is git-ignored
4. Check the API: `python scripts/check_api.py`. It prints the model, stop reason and token use

The model ID is pinned in `config/models.yaml`.

Run instructions will be added as the system is built.
