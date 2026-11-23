# Brief for audit section workers (c033)

- Spec: `docs/specs/2026-11-23_audit.md`. Read it and `CLAUDE.md` first
- Worktree: this directory, branch `wip/audit` = `origin/main` plus audit files. Other branches: `git log --all`
- Private context: `../../../private/` (git-ignored, outside the repo). Read only. Never copy anything from it into an output
- Read-only everywhere. Write only your own section files in `results/2026-11-23_audit/` and scripts in `results/2026-11-23_audit/scripts/`. No git commits, no pushes, no deletes, no ssh, no cluster or server commands, no tracker runs, no project agent (LLM) runs, no PDFs
- Short recompute scripts (under 1 min) allowed, in `scripts/`
- Output names no machine, account, path outside the repo, or person other than Andrew. No REGR, growth-zone or flank values. When a finding concerns such a string, give file, line and commit only; never quote it
- Plain, flat, declarative bullets. State what was found, as measured

## Section output
- `results/2026-11-23_audit/sN_<topic>.md`: findings, then a "Checked, no finding" list (one line per check: what, command or file, count)
- `results/2026-11-23_audit/sN_<topic>.csv`: header `id,section,severity,where,what,evidence,fix` (quote fields with commas)
- Finding id: `S<N>-<k>`
- Severity: `blocker` = a claim in a results README or lab report is wrong or unsupported; `major` = a rule or protocol was broken, or a number is off; `minor` = documentation, wording, missing provenance
- Each finding: where (file:line or commit), what the evidence shows, what would fix it. Do not fix it
