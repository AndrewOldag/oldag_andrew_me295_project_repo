# Inbox: rag

1. Read `CLAUDE.md`, `docs/agents/README.md` and `docs/specs/2026-11-02_lab-report-3.md` (section B and the Limits). `git fetch origin`; branch `wip/rag` from `origin/main` in your own worktree, never main. Task `tasks/c024-rag.md`. First status, push
2. Andrew, 2026-11-02: corpus is the 17 files in `docs/context/literature/rag_corpus.csv` with `included = yes` only. No OUP or Wiley paper (Plant Physiology counts as OUP) goes into the index, the gold set or any prompt. Andrew copies `rag_corpus_2026-11-02b.zip` to the VM; find it (Downloads first). Not found: `State: waiting on Andrew`, Needs Andrew: copy the zip, and stop
3. Do section B in order: corpus check (B2), proposal (B3), build and tests (B4), gold set committed (B5), scoring (B6), results (B7). Push status after each step. VM only. When done: decisions, log, `State: ready to merge`
4. Planning, 2026-11-03 (Andrew): Argon's second read of the gold set (`docs/reviews/2026-11-03_argon-rag-gold/`). The scored result stays as is. Add, without new LLM calls (re-score the saved answers in `staging/rag/runs/`):
   - A post-hoc column: correct when the cited page is the gold page or a row of `alt_pages.csv` with `agrees_with_gold` yes for that question. Gold alt pages from a reader who had not seen the results. Label it post-hoc in the README; the original column stays primary. Fix `gold_pages` so an alt page may be in another included file (a20 and the supplement)
   - a05: two included papers give different counts (Morris1992 3, Henry2023 4). Mark a05 ambiguous in the README; report results with and without it
   - a01: map the extraction artefacts of Mullen1998 (`\x8b` for plus-minus, `lm` for micrometre) in the quote check only if the mapping is exact on all its pages; re-check a01 quotes; report
   - a17: gold page is the Highlights page; note it
   - Decisions entry, log, status `ready to merge`
