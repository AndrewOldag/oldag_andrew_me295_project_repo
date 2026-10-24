# coord-tick
Updated: 2026-10-24 13:05
Lane: course
Branch: wip/coord-tick
Last inbox item done: 1
State: waiting on Andrew
Now: item 2 (hand test) needs Andrew: this session's guard refuses git commands on the main checkout, and a live coordinator session was busy there
Done since last update:
- 1: `scripts/ops/coordinator_tick.ps1`, `scripts/ops/install_coordinator_tick.ps1`, tick tests in `tests/test_ops.py` (2adff36); `tests/test_ops.py` 8 passed
- 3: `CLAUDE.md` Agents, `docs/agents/README.md` (tick section, roster), `docs/decisions.md`, coordinator inbox item 19, `README.md`, `config/backup.example.conf` (this commit)
Needs Andrew:
- Item 2 hand test. First stop every live coordinator session (two coordinators must not merge on main at once). Then from the main repo folder run twice: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\worktrees\coord-tick\scripts\ops\coordinator_tick.ps1` (first run: full pass, no state yet; second: skip). Then `check github` here: I read the tick log and report run time and tokens
- After that, item 4: install from an elevated shell in the main repo folder: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\worktrees\coord-tick\scripts\ops\install_coordinator_tick.ps1`; check: `Get-ScheduledTask me295-coordinator-tick | Get-ScheduledTaskInfo`
- After install: confirm in the tick log one scheduled full pass that pushed. The hand test runs logged on; the scheduled one runs S4U (git uses an SSH key file, so it should work; Claude sign-in under S4U is untested)
