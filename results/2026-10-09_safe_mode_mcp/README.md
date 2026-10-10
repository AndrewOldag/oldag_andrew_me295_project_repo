# Safe-mode MCP test, 2026-10-09

Condition 1 of the CLI agent design: check that `claude -p --safe-mode` can call a local MCP tool given with `--mcp-config` and `--strict-mcp-config`.

## Setup
- `scripts/cli_probe/probe_server.py`: one-tool stdio MCP server (MCP Python SDK 2.3.0). The tool returns a random value set per run
- `scripts/cli_probe/test_safe_mode_mcp.py`: launches `claude -p` with the agent call shape and a clean environment from a fixed list, then checks the init event and the result
- Claude Code 2.1.293, model `claude-opus-5-5`, effort low
- Pass needs all four: probe server connected, tool listed, reported value equals the probe value, `modelUsage` holds only the pinned model

## Results
| Variant | Flags | MCP servers in init | Tools listed | Reported | Model check | Passed |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| A | `--safe-mode` + `--mcp-config` + `--strict-mcp-config` | none | `StructuredOutput` only | NO_TOOL | pass | no |
| C (control) | as A without `--safe-mode` | none | `StructuredOutput` only | NO_TOOL | pass | no |

- Both runs exit 0, `subtype` success, 2 turns, about 2.4 s
- The probe server answers an MCP `initialize` request when run by hand, so the server works
- Raw fields: `result_A.json`, `result_C.json`

## Cause
- `--safe-mode` turns off MCP servers by itself (Claude Code CLI reference). Variant A could not pass under any policy
- Variant C is the run that tests the policy. It failed: the account's organization-managed Claude Code settings allow only MCP servers on an administrator list, and drop others with no error, including servers passed with `--mcp-config`
- An allowlist entry would not rescue the MCP design: a stdio server is matched by its exact command and arguments, so an entry holds for one machine only, and `--safe-mode` would still have to be dropped

## How the policy was confirmed
- `claude mcp list` and `claude mcp get probe`, run with the agents' clean environment from a temporary folder whose project `.mcp.json` names the probe server:
  - `mcp list` shows only the organization's managed connectors (8). The probe server is absent
  - `mcp get probe` exits 1: `No MCP server named "probe"`
- The account's managed settings contain `allowManagedMcpServersOnly: true`

## Status
Stopped and reported, as condition 1 required. Replaced by typed actions executed by the orchestrator (`docs/decisions.md`, 2026-10-09). Variant B (no `--safe-mode`, separate config directory) was not run and has been removed from the script.
