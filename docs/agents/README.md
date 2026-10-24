# Agents: inbox and status

The planning account gives instructions through this folder. Andrew's only message to a session after its first is `check github`.

## Files
- `inbox/<name>.md` on `main`: written by the planning account only. Numbered items, newest last
- `status/<name>.md`: written by the agent only
  - Course-lane agents: on their own work branch (`wip/<name>`, or `main` for the coordinator)
  - Research-lane agents: on branch `status/<name>`, in a clone of this repo kept only for this (the agent's status clone; location in `private/paths.md`). Nothing else from the research lane goes into this repo

## On `check github`
1. `git fetch origin`
2. Read `origin/main:docs/agents/inbox/<name>.md` and `CLAUDE.md` from `origin/main`
3. Do every item numbered after `Last inbox item done` in your status file, in order. A standing item applies on every check
4. Update `status/<name>.md`, commit, push. Then keep working on the item until done or blocked
5. When an item is done or blocked, update status again and push

## Coordinator tick (Andrew, 2026-10-24)
- The coordinator is not a live session. The scheduled task `me295-coordinator-tick` runs `scripts/ops/coordinator_tick.ps1` every 10 min
- Each tick: lock, `git fetch origin` in the main checkout, hash of the sorted `git ls-remote origin`. Hash unchanged and last full pass under 60 min old: one log line, no Claude call. Else one headless pass (`claude -p`) that does one coordinator check (this protocol and every standing item of `inbox/coordinator.md`), pushes `status/coordinator.md` and exits. A pass over 20 min is stopped
- The hourly full pass also covers server-job markers (coordinator item 16) when no ref changed
- Pings: the pass sends `check github` if it has the message tool; else it lists the names under Needs Andrew. The tick log records both. The tick never starts sessions and never runs tracker or server jobs
- Tick log, state and lock live in a local ops folder outside the repo (location in `private/`)
- Install (Andrew, elevated shell): `powershell -File scripts/ops/install_coordinator_tick.ps1`. Check: `Get-ScheduledTask me295-coordinator-tick | Get-ScheduledTaskInfo`

## Status file (replace the whole file each time)
```
# <name>
Updated: YYYY-MM-DD HH:MM (local)
Lane: course | research
Branch: <branch>
Last inbox item done: <number>
State: working | waiting on Andrew | waiting on <agent> | done | ready to merge
Now: one line
Done since last update:
- one line per item, with commit hashes
Needs Andrew:
- one line per decision, or none
```
- Research-lane status: state, counts, pass or fail, file names. No result values, no biology, no machine names, paths or people. Details stay in the vault note or on the VM
- The pre-push hook applies to every push

## Roster
| Name | Lane | Branch | Source prompt | State known to planning |
| :-- | :-- | :-- | :-- | :-- |
| coordinator | course | main | VM-Parallel-Agents, How to run | scheduled tick from 2026-10-24 (no live session) |
| gatekeeper | course | wip/gatekeeper | 1 | done, merged |
| diag-review | course | wip/diag-review | 2 | done, merged |
| baselines | course | wip/baselines | 3 | done, merged |
| heldout | course | heldout/faults | 4 | done, merged |
| lab-report-1 | course | wip/lab-report-1 | 5 | done, merged; report on hold |
| review | course | wip/review | 6 | never run; not needed after freeze v2 |
| freeze-v2 | course | wip/freeze-v2 | spec 2026-10-12 | done, merged |
| scored-v1 | course | wip/scored-v1 | spec 2026-10-12b | done, merged |
| auditor-v1 | course | wip/auditor-v1 | spec 2026-10-13 Task A | done, merged (f52dbdd) |
| fq-real | course | wip/fq-real | spec 2026-10-13 Task B | done, merged (742dc79) |
| data-steward | research | status/data-steward | 7 | unknown |
| gate2 | research | status/gate2 | 8 | unknown |
| litreview | research | status/litreview | 9 | unknown |
| readme-check | course | wip/readme-check | inbox readme-check | done (2026-10-17) |
| spec-audit | course | wip/spec-audit | spec 2026-10-23_spec-audit | to start (2026-10-23) |
| spec-audit-check | course | wip/spec-audit-check | spec 2026-10-23_spec-audit | after spec-audit |
| lab-report-2 | course | wip/lab-report-2 | spec 2026-10-23_next-steps | to start (2026-10-23) |
| dispatcher | course | wip/dispatcher | spec 2026-10-23_next-steps | to start (2026-10-23) |
| spec-audit-r | research | status/spec-audit-r | research spec, tracker repo | done (2026-10-23) |
| freeze-v3 | course | wip/freeze-v3 | spec 2026-10-23b_freeze-v3 | working (2026-10-23) |
| turn-long | research | status/turn-long | research spec, tracker repo | done (2026-10-24) |
| freeze-v31 | course | wip/freeze-v31 | spec 2026-10-24_freeze-v3.1 | to start (2026-10-24) |
| coord-tick | course | wip/coord-tick | inbox coord-tick (task c016) | working (2026-10-24) |

Finished sessions can be closed. A new task gets a new name and a new inbox.
