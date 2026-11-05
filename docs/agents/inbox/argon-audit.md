# Inbox: argon-audit

Antigravity agent (Gemini 4 Argon). Read `AGENTS.md` first; it binds you.

1. `git fetch origin`. Clone this repo into a folder of your own (not the Claude sessions' checkouts). Branch `audit/argon` from `origin/main`. Read `AGENTS.md`, `CLAUDE.md`, `docs/agents/README.md`, `docs/specs/2026-11-03_argon-audit.md`. Write your first status (format in `docs/agents/README.md`), push to `audit/argon`
2. Task A1, second reader of the RAG gold set (spec A1). Done: `docs/reviews/2026-11-03_argon-rag-gold/`, status pushed, then item 3
3. Task A2, independent recompute of freeze v4 and the v3-to-v4 split (spec A2). Done: `docs/reviews/2026-11-03_argon-v4-recompute/`, status pushed, then item 4
4. Task A3, synthetic trace audit of freeze v4 (spec A3). Done: `docs/reviews/2026-11-03_argon-v4-traces/`, status `done`
5. Planning, 2026-11-04 (Andrew). Start only when real-calib's status says ready to merge. Branch `audit/argon` (fetch, rebase on `origin/main`). Audit batch 2 from `origin/wip/real-calib` (files in the repo only; you have no server or cluster access). Output `docs/reviews/<date>_argon-batch2/review.md`:
   - Deletes: every row in `audit/deletes.csv` deletes only a Claude-staged root or a moved copy; every output it lists was verified on storage before the delete time; no output of a deleted item is missing from `outputs.csv`
   - Outputs: every include-yes batch-2 window in `manifest/root_manifest.csv` (usable windows only) has a row; counts match the README; `reverify.md` agrees with `outputs.csv`
   - Spend: ledger totals, worst case under the cap at every submit, total under $15
   - Rules: code diff of `wip/real-calib` against `main`: nothing runs Python or jobs on the storage host; one persistent connection; no new cluster login path. Cite file and line
   - Checker equivalence record in decisions (5 windows, difference at most 1e-9)
