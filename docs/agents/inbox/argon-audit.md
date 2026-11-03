# Inbox: argon-audit

Antigravity agent (Gemini 4 Argon). Read `AGENTS.md` first; it binds you.

1. `git fetch origin`. Clone this repo into a folder of your own (not the Claude sessions' checkouts). Branch `audit/argon` from `origin/main`. Read `AGENTS.md`, `CLAUDE.md`, `docs/agents/README.md`, `docs/specs/2026-11-03_argon-audit.md`. Write your first status (format in `docs/agents/README.md`), push to `audit/argon`
2. Task A1, second reader of the RAG gold set (spec A1). Done: `docs/reviews/2026-11-03_argon-rag-gold/`, status pushed, then item 3
3. Task A2, independent recompute of freeze v4 and the v3-to-v4 split (spec A2). Done: `docs/reviews/2026-11-03_argon-v4-recompute/`, status pushed, then item 4
4. Task A3, synthetic trace audit of freeze v4 (spec A3). Done: `docs/reviews/2026-11-03_argon-v4-traces/`, status `done`
