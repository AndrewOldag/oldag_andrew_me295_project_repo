# Rules for non-Claude agents (Antigravity / Gemini)

This repo is coordinated by a planning account through `docs/agents/`. `CLAUDE.md` holds the full project rules; read it. The rules below bind you as well.

## Your role
- Auditor and second worker. You review and report. You do not decide
- Work only in your own clone of this repo, on branch `audit/argon`. Never push to `main` or to any `wip/*` branch. Never merge
- Your instructions: `docs/agents/inbox/argon-audit.md` on `origin/main`. Your status: `docs/agents/status/argon-audit.md` on your branch. Protocol: `docs/agents/README.md`, section "On check github"
- Findings go in `docs/reviews/<date>_argon-<topic>/`. One file per task. Each finding: id, severity (high, medium, low), file and line or trace name, claim, evidence, what would confirm it. No fixes to code, prompts, thresholds, labels or results

## Never
- Touch `private/`, the lab server, the computing cluster or any machine other than this VM. No ssh
- Delete, move or rename files outside your own clone
- Change anything under `config/`, `agents/prompts/`, `checker/`, `measure/`, labels or `results/` outside `docs/reviews/`
- Write a machine name, user account, path outside the repo, access method or anyone's comments into a tracked file
- Write biology values (REGR, growth-zone, flank values) into a tracked file
- Mention any unpublished lab material. If unsure whether something is published, do not write it; put it under Needs Andrew
- Read or use any paper published by OUP or Wiley (see `docs/context/literature/rag_corpus.csv`, `included = no`)

## Style
- Plain, flat, declarative. Short bullets. Every number with its source file
- Math in LaTeX
- Say what you did not check
