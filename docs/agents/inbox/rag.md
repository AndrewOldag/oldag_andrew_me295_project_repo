# Inbox: rag

1. Read `CLAUDE.md`, `docs/agents/README.md` and `docs/specs/2026-11-02_lab-report-3.md` (section B and the Limits). `git fetch origin`; branch `wip/rag` from `origin/main` in your own worktree, never main. Task `tasks/c024-rag.md`. First status, push
2. Andrew, 2026-11-02: corpus is the 17 files in `docs/context/literature/rag_corpus.csv` with `included = yes` only. No OUP or Wiley paper (Plant Physiology counts as OUP) goes into the index, the gold set or any prompt. Andrew copies `rag_corpus_2026-11-02b.zip` to the VM; find it (Downloads first). Not found: `State: waiting on Andrew`, Needs Andrew: copy the zip, and stop
3. Do section B in order: corpus check (B2), proposal (B3), build and tests (B4), gold set committed (B5), scoring (B6), results (B7). Push status after each step. VM only. When done: decisions, log, `State: ready to merge`
