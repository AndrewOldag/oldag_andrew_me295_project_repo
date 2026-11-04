## 2026-11-03 (build account, rag session, inbox item 4)
- Done: post-hoc re-score of the saved RAG answers against the second reader's alt pages (`docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv`, 44 agreeing rows); no LLM call. `rag/posthoc.py`, `scripts/rag.py report`
- Done: correct, scored (primary) 11 / 12 / 11 of 20; post hoc 18 / 17 / 18 of 20. Without a05 (ambiguous: Morris1992 3 parameters, Henry2023 4): scored 10 / 11 / 10 of 19, post hoc 17 / 16 / 17 of 19. Agreement post hoc 22 of 25
- Done: `gold_pages` accepts an alt page in another included file (a20, `Nolan2023_supplement`)
- Done: Mullen1998 artefact map exact on all 6 pages (21 plus-minus, 27 micrometre); a01 still unverified 3 of 3 (saved quotes omit the character)
- Done: a17 gold page noted as the Highlights page. Tests 30 passed in `tests/test_rag.py`
- Demo: `python scripts/rag.py report` prints scored and post-hoc metrics and writes `results/2026-11-02_rag/metrics.json` and `per_question.csv`
- Remaining: merge `wip/rag`
- Bottlenecks: none
