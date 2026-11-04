# RAG over the papers, scored against keyword search (task c024)

Spec 2026-11-02 section B. Proposal `docs/proposals/2026-11-02_rag.md` (b69a95a, amended before any run). Gold set `rag/gold.yaml` (ea43149), committed before any retrieval or run. Run 2026-11-02 on the VM.

## Setup
- Corpus: 17 files with `included = yes` in `docs/context/literature/rag_corpus.csv` (16 papers, one supplement); 17 of 17 sha256 match. No OUP or Wiley paper in the index, the gold set or any prompt
- 317 pages, 693 chunks (median 300 words, max 349). Build 309 s on the 2-core VM
- RAG: `BAAI/bge-small-en-v1.5` embeddings (fastembed 0.9.1), top 6 chunks, one `claude -p` call per question (claude-opus-5-5, Claude Code 2.1.310, effort medium). Baseline: BM25 over the same chunks
- Gold: 20 answerable questions over 15 papers; 5 whose answer is only in an excluded paper (correct outcome: decline)

## Commands
- `python scripts/rag.py build`, `gold`, `retrieval`, `run --repeat 1`, `run --repeat 2`, `run --repeat 3`, `report`

## Retrieval, 20 answerable questions (no LLM)
| Retriever | Gold page top 1 | Gold page top 5 | Gold page top 6 |
| :-- | :-- | :-- | :-- |
| BM25 (baseline) | 11 | 19 | 19 |
| Embeddings (RAG retriever) | 8 | 14 | 15 |

## RAG answers, 3 repeats (75 LLM calls of 150 allowed)
| Metric | Repeat 1 | Repeat 2 | Repeat 3 | Median (range) |
| :-- | :-- | :-- | :-- | :-- |
| Correct (gold page, quote verified) | 11 / 20 | 12 / 20 | 11 / 20 | 11 (11-12) |
| Verified quotes / answers | 18 / 20 | 17 / 20 | 18 / 20 | 0.90 (0.85-0.90) |
| Declines on out-of-corpus / all declines (precision) | 5 / 5 | 5 / 5 | 5 / 5 | 1.0 |
| Declines on out-of-corpus / 5 (recall) | 5 / 5 | 5 / 5 | 5 / 5 | 1.0 |
| Errors (no valid action) | 0 | 0 | 0 | 0 |

- Agreement across repeats: 21 of 25 questions (0.84) have the same outcome in all 3
- Call time: median 3.6 s (1.6-7.4 s). Free VM memory before each repeat 4.41-4.45 GB. No usage-limit stop

## Misses (repeat 1 / 2 / 3)
- `wrong_source` 7 / 5 / 7: quote verified, cited page not the gold page. Every cited source is the gold paper (or, for a20, its supplement). In 5 questions (a06, a08, a10, a12, a16) the gold page was not in the 6 retrieved chunks; the answer came from another page of the same paper. The gold set lists no alt pages, so these count as misses. Whether the cited page states the answer was not checked
- `unverified` 2 / 3 / 2:
  - a01, all 3 repeats: quote not on the page. The page text holds a control character (`\x8b`, from the plus-minus sign) that the model's quote leaves out. Extraction artefact; the answer is not repaired
  - a04 (repeats 1, 3): quote over 40 words
  - a07, a16 (repeat 2): answer text over 60 words

## Post hoc (2026-11-03; the scored result above stays primary)
- Source: a second reader's review of the gold set, written without seeing these results (`docs/reviews/2026-11-03_argon-rag-gold/`). Inbox rag item 4 (Andrew, 2026-11-03). Re-scored from the saved answers in `staging/rag/runs/`; no new LLM call
- Alt pages: a cited page also counts when it is a row of `alt_pages.csv` with `agrees_with_gold` yes for that question (44 rows; may be in another included file, e.g. a20 and `Nolan2023_supplement`). Fix in `rag/score.py`: `gold_pages` takes an alt page's own key
- a05 is ambiguous: Morris1992 gives 3 fitting parameters, Henry2023 fits 4 parameters of the same function. All 3 repeats cited Morris1992 p1 (correct as scored)

| Correct of answerable | Repeat 1 | Repeat 2 | Repeat 3 | Agreement (all questions) |
| :-- | :-- | :-- | :-- | :-- |
| Scored, 20 questions | 11 / 20 | 12 / 20 | 11 / 20 | 21 / 25 |
| Scored, without a05 | 10 / 19 | 11 / 19 | 10 / 19 | 20 / 24 |
| Post hoc, alt pages, 20 questions | 18 / 20 | 17 / 20 | 18 / 20 | 22 / 25 |
| Post hoc, alt pages, without a05 | 17 / 19 | 16 / 19 | 17 / 19 | 21 / 24 |

- With alt pages every `wrong_source` answer becomes correct (a06, a08, a10, a12, a15, a16, a20). The misses left are the `unverified` answers: a01 in 3 repeats, a04 in 2, a07 and a16 in 1
- a01, Mullen1998 artefacts: the map (`\x8b` to plus-minus, standalone `lm` to micrometre) is exact on all 6 pages: 21 of 21 `\x8b` sit between numbers or in "mean `\x8b` SD"; 27 of 27 standalone `lm` follow a number. Embedded forms (`lmh`, `lmol`, `lma`, `lmb`) are left as they are. Applied in the quote check only (`rag/posthoc.py`). Re-check: a01 stays unverified in 3 of 3 repeats. The saved quotes leave the character out ("481  50 lm"), so they do not match "481 ± 50 µm" either
- a17: the gold page (Chaiwanon2015 p1) is the journal's Highlights and graphical-abstract page, not the article body. The same finding is on p2, p3, p6, p8 and p11 (alt pages)

## Per question
`per_question.csv`: BM25 and embedding hits (1 = gold page in top k), the RAG outcome per repeat, and the post-hoc outcome per repeat (`posthoc_r*`: alt pages and artefact map). Metrics: `metrics.json`. Answer texts and traces stay in `staging/rag/runs/` (git-ignored).

## Limits
- One gold page per question. A fact stated on several pages is scored on one
- Gold set written by the build account from the page text, not by a second reader
- 25 questions; differences of one question are 5 points of accuracy
