# Proposal: agents choose typed actions; the orchestrator executes them

From: build account. Date: 2026-10-09. Status: awaiting planning-account approval. Andrew chose this option.

## Why
- The CLI agent design (approved with conditions, 2026-10-08) gave agents tools through a local MCP server
- Condition 1 test failed: the account's organization-managed settings allow only MCP servers on an administrator list. Local servers are dropped before start, with or without `--safe-mode`. Evidence: `results/2026-10-09_safe_mode_mcp/`
- Getting around the list would circumvent a security control. Not done
- Andrew is asking the course staff whether a project MCP server can be added to the list. This design does not depend on the answer

## Design
- Agents get no tools. Each agent step is one `claude -p` call that returns one action as JSON, constrained by `--json-schema`
- The orchestrator (plain Python) validates the action, executes it, records the result, and calls the agent again with the task history. It stops on a terminal action or at a step limit
- Agents cannot run code, read files or reach any machine. Everything they see is passed in by the orchestrator
- Information separation holds by construction: each call receives only the history the orchestrator gives that agent

## Action sets (draft)
Diagnostician, per root-by-window task:
- `request_info(kind)`: kind from a fixed list, e.g. `check_report`, `velocity_profile`, `displacement_vs_patch_radius`, `midline_jitter`, `stage_log_summary`, `frame_quality`
- `apply_remedy(fault, remedy, setting)`: fault from the fault table, remedy and setting from the fixed remedy list
- `accept(confidence)`: report the measurement
- `decline(fault, reason)`: do not report it
- Every action carries a short `rationale` field, stored in the trace

Dispatcher, per batch:
- `propose_plan(tasks, machine, estimated_core_hours)`: the orchestrator stops for Andrew's approval before any job is submitted

Auditor, per batch:
- `flag_root(id, reason)`, `compare_groups(groups, quantity)`, `write_section(name, text)`, `finish()`

## Call shape
```
claude -p --safe-mode --model claude-opus-5-5 --effort <level>
  --output-format json --json-schema <action schema>
  --system-prompt-file <agent prompt>
  --tools "" --strict-mcp-config --permission-mode dontAsk
  --no-session-persistence --max-turns 3
```
- `--tools ""` with no MCP config: the only tool is the built-in structured-output tool. The 2026-10-08 test call used this shape and passed
- One call per step; the history is sent in the prompt. No session resume, so each call is self-contained and logged in full

## Safety and provenance
- Each action is checked against its schema and the fixed lists before it runs. An invalid action counts as a failed step and is logged
- Step limit per task (e.g. 8). Reaching it counts as `decline` with reason `step_limit`
- Human approval points unchanged: compute budget, threshold changes, deletions
- Per call the orchestrator stores the action JSON, `modelUsage`, `claude --version`, the prompt file hash and the history hash. Conditions 2-7 of the 2026-10-08 approval still apply

## Effects on the evaluation
- What an agent can find out is limited to the `request_info` kinds. This is stated as a limit. Held-out faults test whether the kinds are enough
- Baselines use the same actions: the rule-based remedy tree maps check results to actions without an LLM; the single-agent version gets the union of the action sets
- Diagnosis accuracy, false-accept rate and abstention are read directly from the action traces
- If an MCP server is approved later, each action maps one-to-one to a tool. The action lists and traces stay the same

## Changes if approved
- `agents/actions.py`: action schemas and fixed lists. `agents/orchestrator.py`: step loop, validation, trace writing. `agents/launcher.py`: clean environment and the call shape
- `scripts/check_cli.py` replaces `scripts/check_api.py`; runs through the launcher (conditions 3 and 4)
- `config/models.yaml`: drop `max_tokens` and `fallbacks`; add step limit and max turns per agent
- `environment.yml`: remove `anthropic`. Delete `.env.example`. README: `claude auth login` instead of an API key
- `scripts/cli_probe/` stays as the record of the MCP test
