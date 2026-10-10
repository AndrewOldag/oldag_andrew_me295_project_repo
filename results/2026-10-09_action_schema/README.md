# Action schema test, 2026-10-09

Condition 2 of the typed-action review: send the diagnostician action schema through `claude -p --json-schema` with the agent call shape and record the result.

## Setup
- `python scripts/cli_probe/test_action_schema.py`: one call per schema form and scenario, through `agents/launcher.py` (`--safe-mode`, no built-in tools, `--json-schema`, pinned model)
- Claude Code 2.1.293, `claude-opus-5-5`, effort high, max 3 turns per call
- Four made-up scenarios, each set up to call for one action: fresh task, evidence in, remedy passed, remedy failed. Not data
- Valid means: the CLI returned structured output from the pinned model, and it passed the orchestrator's validation (`agents/actions.py`)

## Schema forms
- `optional`: one flat object; `action` and `rationale` required, all arguments optional
- `nullable`: one flat object; every field required, unused ones null
- `union`: `anyOf` with one object type per action

## Results
| Form | Valid calls | Turns | Time per call | Actions returned |
| :-- | :-- | :-- | :-- | :-- |
| optional | 4 of 4 | 2 each | 3.7-4.7 s | request_info, apply_remedy, accept, decline |
| nullable | 4 of 4 | 2, 3, 3, 2 | 4.6-12.7 s | request_info, apply_remedy, accept, decline |
| union | 0 of 4 | 1 | about 0.5 s | none: API error 400, the schema needs `type` at the top level |

- Each scenario returned the action it was set up for, in both flat forms
- `nullable` needed an extra turn in two calls, which doubles the time
- `union` is rejected before the model runs. A top-level `anyOf` is not accepted as a tool input schema
- Raw fields per call: `result.json`

## Decision
`optional` is the default (`schema_form` in `config/models.yaml`), as the review asks. The orchestrator checks the chosen action's arguments.
