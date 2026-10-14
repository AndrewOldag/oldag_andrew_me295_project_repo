# Single-agent baseline: definition

From: build account. Date: 2026-10-12. Spec `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md`, item 4. Choices on `check_report`, remedy results, roll back and prompt: Andrew, 2026-10-12, in chat. Written and committed before any run.

## Purpose
- Measures what the deterministic checker adds: the same agent loop as the diagnostician, with no checker output in anything the agent sees

## Same as the diagnostician
- Model, Claude Code version, effort, turns per call, step limit 8, schema form (`config/models.yaml`; entry `single_agent` with the diagnostician's values)
- Action set: `request_info`, `apply_remedy`, `accept`, `decline`; the same fault, remedy, setting and info-kind lists (`agents/actions.py`, `ACTION_SETS["single_agent"]` is the diagnostician's set)
- Orchestrator (`agents/orchestrator.py`) unchanged: same step loop, failed-step rule, trace format and totals
- Remedies, re-runs and runner: the same `Slice` code. The checker still runs on every measurement, for the record and for scoring only
- Scoring: the same outcome categories (`measure/score.py`), labels and tolerance

## Different from the diagnostician
- First view (task): the task line and the tracking settings (frame stride, disk radius, pixel size). No failed, passed or not-run check lists and no check values
- `request_info`: every kind answers as for the diagnostician, except `check_report`, which stays on the list and answers `{"error": "check_report is not available for this task"}`. The request counts as a step
- `apply_remedy`: the result says the remedy was applied and the measurement re-run, what changed, and the `settings_left` note when no further setting exists. No check values, no check pass or fail lists, no before/after
- Roll back: off. It is decided by the checker values (`agents/executors.py`, `no_progress`). A remedy stays applied until the agent applies another
- Prompt (`agents/prompts/single_agent.md`): the diagnostician prompt with one sentence replaced. "The task tells you which checks failed." becomes "No checker report is given. Judge the measurement from the evidence you request." The three check descriptions (P1), every rule and the frame-quality reference (P5) stay, per the 2026-10-12 decision. Rules that refer to checks ("accept only when the checks pass", "a remedy that lowered a failing check") stay as written

## Rule
- No check value appears in any message to the single agent: first view, info answers, remedy results, error messages
- Info answers are computed from the measurement record, not from the checker. `stage_log_summary` (P1) reports closure residuals per hour at stage moves and elsewhere; these are info fields the diagnostician also gets. The test below checks that none of them equals a check value

## Tests (`tests/test_single_agent.py`)
- The first view holds no check value and no check list
- The single agent can request every info kind and apply every remedy and setting the diagnostician can; `check_report` answers "not available"
- A scripted run through the orchestrator (every info kind, a remedy, accept) on fixture records: no check value, at 2 or 3 decimals, and no check field name appears in any prompt sent to the agent
- No roll back after a remedy that the diagnostician's rule would roll back
