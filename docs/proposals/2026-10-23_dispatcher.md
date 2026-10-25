# Dispatcher: proposal

From: build account, dispatcher session. Date: 2026-10-23. Spec `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md`, item B1. Written and committed before any dispatcher code. Needs Andrew's approval before code.

## Job
- Turns the manifest into tracking jobs, chooses where and in what order they run, and keeps compute use inside a budget
- Plain-Python orchestrator executes every action. The agent submits nothing itself
- Same pattern as the diagnostician: one `claude -p` call returns one typed action (`agents/actions.py`, `agents/orchestrator.py`, `agents/launcher.py`). Model and CLI version from `config/models.yaml`

## Input
- `manifest/root_manifest.csv`: rows with `include` yes only. Time inside `usable_from_h` to `usable_to_h` only. The orchestrator filters; the agent never sees other rows or hours
- A cost budget: core-hours and dollars for the computing cluster, from an approval file written after Andrew approves it (see Approval). No file: budget zero
- Queue state, built by the orchestrator: per task `queued | submitted | running | done | failed | collected`, backend, attempts, elapsed and estimated core-hours; lab-server load and free worker slots; budget used and left
- The timing model from B2/B3 (`results/2026-10-23_tracker_timing/`): core-hours per frame and per window, peak memory, output size

## Task unit
- One task = one root x one window. Window length is a fixed setting, not an agent choice. Proposed: 2 h, non-overlapping, from `usable_from_h`; a last partial window kept if at least 1 h `[ANDREW]`
- One task = midline for the window frames, then tracking (`scripts/remote/qb_track.py`, uncoupled, current settings), then the checker on the VM. Checker failures go to the diagnostician, not back to the dispatcher
- Task id `<root_id>__w<start_h>`. A task's output file is its done marker; a restarted batch skips finished tasks

## Actions (typed; orchestrator validates and executes)
| Action | Arguments | Orchestrator does |
| :-- | :-- | :-- |
| `split_root` | `root_ids` | makes root-by-window tasks from the manifest windows; refuses rows not `include` yes |
| `estimate_cost` | `task_ids`, `backend` (`lab_server` \| `cluster`) | returns core-hours, wall time, dollars (cluster), work-space size, from the timing model |
| `request_approval` | `task_ids`, `core_hours`, `reason` | writes a budget request for Andrew and pauses the batch; never approves itself |
| `submit` | `task_ids`, `backend` | lab server: queued under the shared-machine limits. Cluster: refused unless an approved budget covers the estimate |
| `wait` | `minutes` (15 \| 30 \| 60) | sleeps, then returns the new queue state |
| `collect` | `task_ids` | fetches finished outputs, runs the checker, hands failures to the diagnostician |
| `retry` | `task_ids` | resubmits tasks whose job failed (crash, timeout, preemption). At most 2 attempts per task |
| `finish` | `summary` | ends the batch [terminal]; refused while a task is submitted or running |

- What the agent decides: which roots go first, which backend, when to ask for budget, what to retry, when to stop. What it cannot do: change windows, settings, remedies, thresholds, worker counts or the budget
- One dispatcher call = one round. Up to `step_limit` actions per round (4 in `config/models.yaml`); a round ends at `wait` or `finish`. The batch is a loop of rounds. A round limit per batch `[ANDREW]`, proposed 200
- Two invalid actions in a row end the round, as in the orchestrator now

## Approval
- Cluster: a budget approved by Andrew before any cluster job. The approval is a dated entry in `docs/decisions.md` and a file `config/compute_budget.yaml` (core-hours, dollars, date, `approved_by: Andrew`). The orchestrator reads it; no agent writes it. Spending stops at the budget, counted from the estimate before submit and from measured core-hours after
- Lab server: no budget approval. The orchestrator, not the agent, enforces the shared-machine limits (`docs/decisions.md`, 2026-10-11): at most 4 single-thread workers and at most one eighth of the cores, `nice -n 19` and `ionice -c 3`, load check before and between runs, one sweep at a time (lock file), 2 h per sweep, 10 GB work space. Reuses the code in `scripts/synth/sweep.py`
- No action deletes, moves or renames anything on the lab server. Staged images on the VM are deleted after use, one root at a time

## Baseline
- Fixed script: splits all include-yes roots in manifest order, submits in that order to the lab server (cluster only with an approved budget, same rule), polls every 30 min, retries a failed job once, collects everything, stops when the queue is empty
- Same orchestrator, same limits, same timing model. Only the decision maker differs

## Measures (agent behaviour only)
- Budget overrun: count, must be 0 for both (the orchestrator enforces it; any attempt is logged)
- Batch wall time and core-hours to finish a fixed set, against the script
- Invalid actions; approvals requested and whether each was needed; retries of failed jobs and how many then succeeded
- Order: time until the 12-16 root evaluation subset is complete, when it is a stated priority

## Tests (fake queue; no real jobs)
- `FakeQueue` backend: deterministic job times from the timing model, injected job crash, timeout and preemption, a scripted lab-server load trace, a cluster that bills core-hours
- Tests: rows not include-yes and hours outside the windows never become tasks; cluster submit refused with no budget file and when the estimate exceeds the budget left; worker limit and load rule hold under the fake load trace; `finish` refused while jobs run; a restarted batch skips done tasks; the script baseline runs the fake batch to the end
- Agent tests with a scripted launcher (no LLM), as for the diagnostician. One live smoke round on the fake queue

## Open, for Andrew
- No midline source exists yet for real movies. The B2 timing uses a provisional midline from a dark-root segmentation (as the provisional real `frame_quality` reference). The midline step of a real task is open; the Quantum Borland midline nets are a candidate, not tested here
- Window length 2 h and last-window rule
- Round limit per batch
- Retries per task: 2
- Whether the cluster is needed at all; see the cost estimate in `results/2026-10-23_tracker_timing/`
