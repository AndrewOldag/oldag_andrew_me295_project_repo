# Decisions log

One entry per decision: date, decision, reason. Decisions made before this repository was created are recorded outside it.

- 2026-10-09: Review launcher `open_review.bat` finds Python from `ME295_PYTHON`, then the `me295` conda env, then `python` on PATH. Reason: the repository must not name paths outside itself
- 2026-10-09: Review app movie player uses pre-made frames every 15 min with the elapsed time printed on each, made by `scripts/manifest/make_scrub.py`. Reason: the 2 h GIF was too coarse to see when a root leaves the frame; a slider with time sets usable windows directly
- 2026-10-09: Agents act through typed actions returned as JSON under `--json-schema`; the orchestrator validates and executes them. No MCP server. Reason: organization policy drops local MCP servers, `--safe-mode` turns MCP off in any case, and an allowlist entry would hold for one machine only, so another student could not run the system. Approved with seven conditions: `docs/proposals/2026-10-09_structured-action-agents.md`
- 2026-10-09: The typed actions are the project's tool interface and are described as such. Reason: the project guideline requires an agent with at least one domain tool
- 2026-10-09: Agents run as `claude -p` calls under the user's own Claude seat; no API key. `scripts/check_cli.py` replaces the API check; `anthropic` and `.env.example` removed. Reason: the course issues seats, not API keys
- 2026-10-09: Claude Code version pinned in `config/models.yaml` (2.1.293); the launcher refuses other versions and sets `DISABLE_AUTOUPDATER` for agent calls. Reason: a future release may change the default for `-p` and break seat login
