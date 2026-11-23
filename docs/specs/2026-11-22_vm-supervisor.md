# Spec: VM supervisor (no LLM)

From: planning account. Date: 2026-11-22. Approved by Andrew 2026-11-22. Lane: course (ops). Task: c032. Session: real-calib.

## Why
- Sessions are `claude -p` passes that exit; today they are restarted by hand or by an hourly Task Scheduler job (`agents.ps1 -Fresh`)
- Nothing stops a second copy of a detached cycle; nothing reports VM liveness when no session runs
- Decisions stay with the planning account through GitHub; the supervisor only watches and starts. No LLM in it

## What
`scripts/ops/supervisor.ps1`, one long-running hidden process, started at logon:
1. Every 10 min (configurable), for each course session (dispatcher, real-calib, compound):
   - running? (pid file and process alive)
   - pending work? `git fetch` and compare the session's inbox last item number on `origin/main` with `Last inbox item done` in its status on its branch; or status `State` is `working` with `Updated` older than 2 h and no live process
   - start it with `agents.ps1 -Names <name> -Fresh` only if not running and pending work; at most one start per tick; 60 s between starts
2. Detached processes: a registry file `%USERPROFILE%\claude_agents\detached.json` (name, pid, command, log path, started). Sessions register each detached process there (helper `scripts/ops/register_detached.ps1`). Supervisor reports dead entries in the heartbeat; it never restarts a detached process itself
3. Single instance: a lock file with pid; a second supervisor exits at once
4. Heartbeat: every tick, append one line to `docs/agents/status/supervisor.md` on branch `ops/heartbeat` (time, free memory, each session running/exited, starts this tick, dead detached entries) and push; keep the last 48 lines
5. Free memory under 3 GB: start nothing that tick, say so in the heartbeat
6. Never deletes, never kills a process, never touches the cluster or the lab server
7. Install: `scripts/ops/install_supervisor.ps1` registers a logon Task Scheduler entry and removes the hourly "ME295 agents ping" task; `-Uninstall` reverses both. Not run until planning says switch over

## Tests
- Pester or a Python harness with a fake clock, fake git and fake process table: pending vs not pending, running session not restarted, low memory blocks starts, lock file stops a second instance, heartbeat trimmed to 48 lines

## Limits
- Build and test only. Switch-over after the c027 cut-off (Thu 26 Nov 12:00) on a planning inbox item
- Branch `wip/supervisor` from `origin/main`; status ready to merge when tests pass
