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
- The account's organization-managed Claude Code settings allow only MCP servers on an administrator list. Servers not on the list are dropped before start, with no error in the init event
- The local probe server is not on the list. This blocks local MCP tools for every flag set, not only `--safe-mode`
- Variant B (no `--safe-mode`, separate config directory) was not run: the managed setting applies to the account, so it would be blocked the same way

## Status
Stopped and reported, as condition 1 requires. The tool interface needs a decision before agent code is built.
