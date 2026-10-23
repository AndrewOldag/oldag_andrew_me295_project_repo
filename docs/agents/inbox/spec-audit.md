# Inbox: spec-audit

1. Read `CLAUDE.md`, `docs/agents/README.md` and `docs/specs/2026-10-23_spec-audit.md`. Create worktree and branch `wip/spec-audit`. Task file `tasks/c008-spec-audit.md` (exists on main; update it on your branch). Write your first status and push
2. Do the spec: copy the literature network to the VM, write the six reviewer subagents in `.claude/agents/audit-<name>.md`, run them (in parallel where they do not share files), merge into SUMMARY.md. Push after each reviewer file
3. Standing rule: read-only on code, config and results; no PDFs opened; never delete, move or rename anything on the lab server
4. When SUMMARY.md is pushed: status `ready to merge`, Needs Andrew lists the findings rated "would change a reported number" and the "needs Andrew to check the paper" list
