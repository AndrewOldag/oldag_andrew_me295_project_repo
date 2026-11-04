# Audit A1: Second reader of the RAG gold set

- Date: 2026-11-03
- Session: `argon-audit`
- Branch: `audit/argon`
- Task: `c025` (`docs/specs/2026-11-03_argon-audit.md`, section A1; `docs/agents/inbox/argon-audit.md`, item 2)

## Summary

- Corpus integrity: 17 of 17 files with `included = yes` in `docs/context/literature/rag_corpus.csv` matched their SHA256 digests (`317` pages total across the 17 PDFs extracted with `rag/corpus.py:extract_pages`). The 11 rows with `included = no` (OUP and Wiley) were not present in `staging/rag_corpus/` and were not read.
- Gold code check: `rag/score.py:check_gold` passed with `0` errors across all `25` questions in `rag/gold.yaml` (`20` answerable, `5` out-of-corpus).
- Answerable questions (`a01`–`a20`): All `20` gold answers are stated on their designated gold `(key, page)` in the PDF text and are answerable from text alone (not only from a figure). However, `18` of `20` answerable questions (`a01`–`a03`, `a05`–`a06`, `a08`–`a20`) also have the answer stated on at least one other page of the same paper or another included paper (`45` alternative page occurrences recorded in `docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv`), while `rag/gold.yaml` defines `0` `alt` entries.
- Cross-paper disagreement on `a05`: `Morris1992` p. 1 and p. 4 state `3` fitting parameters ($v_f$ or $v_0$, $k$, $n$, with $x_0$ chosen arbitrarily and $v_f$ or $v_0$ empirical), whereas `Henry2023` p. 6 Eq. (5) fits `4` parameters ($v_f$, $k$, $x_0$, $n$) by Nelder–Mead optimization when applying the `Morris1992` flexible logistic function.
- Out-of-corpus questions (`o01`–`o05`): All `5` questions have answers that are absent from all `317` pages of the `17` included PDFs.

## Findings

### A1-F1
- **id**: A1-F1
- **severity**: high
- **file and line**: `rag/gold.yaml:7-146`, `rag/score.py:21-24`, `rag/score.py:59-61`
- **claim**: `rag/gold.yaml` omits `alt` pages for all `20` answerable questions, and `rag/score.py:gold_pages` cannot represent alternative pages in another included file, so valid answers citing any of the `45` non-gold pages in `alt_pages.csv` are scored as `wrong_source`.
- **evidence**: `docs/proposals/2026-11-02_rag.md:35` specifies optional `alt` pages where the same fact is stated. In `rag/gold.yaml:7-146`, `0` of `20` answerable questions contain an `alt` key. Across the `317` pages of the `17` included PDFs, `18` of `20` answerable questions (`45` rows in `docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv`) are also stated in the body text, methods, tables, or figure captions on other pages of the gold paper or on pages of another included file (`Morris1992` p. 3 for `a03`; `Henry2023` p. 6 for `a05`; `Nolan2023_supplement` p. 5 and p. 10 for `a20`). In addition, `rag/score.py:23` computes `{(q["key"], q["page"])} | {(q["key"], a["page"]) for a in q.get("alt", [])}`, which hardcodes `q["key"]` and cannot accept an `alt` entry from a different corpus key (such as `Nolan2023_supplement` when `q["key"]` is `Nolan2023`).
- **what would confirm it**: Inspecting system run predictions in `results/2026-11-02_rag/` for items scored `wrong_source` whose cited `(key, page)` appears in `docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv`.

### A1-F2
- **id**: A1-F2
- **severity**: medium
- **file and line**: `rag/gold.yaml:36-41` (`a05`), `staging/rag_corpus/Morris1992.pdf` p. 1 and p. 4, `staging/rag_corpus/Henry2023.pdf` p. 6
- **claim**: Question `a05` asks how many fitting parameters the sigmoid model of the spatial velocity field has without naming `Morris1992`, and two included papers give different counts (`3` in `Morris1992` p. 1 vs `4` in `Henry2023` p. 6).
- **evidence**: `Morris1992` p. 1 states *"A sigmoid curve with three fitting parameters is proposed as a descriptive model for the spatial velocity field"*, and p. 4 Eq. (1) writes
  $$v(x) = \frac{v_f}{\left[v_0^n + (v_f^n - v_0^n)e^{-k(x - x_0)}\right]^{1/n}}$$
  with empirical $v_f$, arbitrarily chosen $x_0$, and `3` fitted parameters ($n$, $k$, and $v_0$). By contrast, `Henry2023` p. 6 Eq. (5) cites `Morris1992` (`[10]`) for the flexible logistic function
  $$v(x) = \frac{v_f}{\left[1 + e^{-k(x - x_0)}\right]^{1/n}}$$
  and states that the Nelder–Mead method was used *"to find the values for $v_f$, $k$, $x_0$, and $n$ that gave the best fit for each point cloud"* (`4` fitted parameters).
- **what would confirm it**: Checking whether top-5 retrieval for `a05` surfaces `Henry2023` p. 6 alongside `Morris1992` p. 1 and p. 4.

### A1-F3
- **id**: A1-F3
- **severity**: medium
- **file and line**: `rag/gold.yaml:7-13` (`a01`), `rag/corpus.py:13-30`, `staging/rag_corpus/Mullen1998.pdf` p. 1, p. 3, p. 4
- **claim**: Font-encoding corruption in `Mullen1998.pdf` turns `±` into control character `U+008B` and `µm` into `lm` in extracted text, forcing the gold quote in `rag/gold.yaml:12` to truncate before the standard deviation, units, and reference landmark (`tip of root cap`).
- **evidence**: In `staging/rag_corpus/Mullen1998.pdf` p. 1, `rag/corpus.py:extract_pages` produces `"When growing vertically, the maximum elongation rate occurred 481 \x8b 50 lm back from the extreme tip of the root (tip of root cap)"` (and similarly on p. 3 and p. 4 Table 1, where `=` is also extracted as `ˆ`). Because `\x8b` and `lm` are not mapped in `rag/corpus.py:13-30`, `rag/gold.yaml:12` truncates `quote` to `"When growing vertically, the maximum elongation rate occurred 481"`, omitting the units and `"from the tip of the root cap"` that `rag/gold.yaml:13` requires in `answer`.
- **what would confirm it**: Running `rag.corpus.extract_pages` on `staging/rag_corpus/Mullen1998.pdf` and inspecting the raw code points around the reported distance on p. 1, p. 3, and p. 4.

### A1-F4
- **id**: A1-F4
- **severity**: low
- **file and line**: `rag/gold.yaml:56-62` (`a08`), `staging/rag_corpus/Baskin2020.pdf` p. 2, p. 4, p. 46
- **claim**: The gold quote for `a08` on `Baskin2020` p. 2 does not include the `"horizontal microscope"` condition in the quote span, whereas `Baskin2020` p. 4 and p. 46 state the full experimental protocol in contiguous prose.
- **evidence**: `Baskin2020` p. 2 (Summary) states `"We imaged individual roots of A. thaliana through a horizontal microscope and used image analysis to obtain velocity profiles. For a root, velocity profiles obtained every 5 min over 3 h coincided closely"`. `Baskin2020` p. 4 (Results) states `"we imaged a root for 3 h so that a velocity profile could be obtained every 5 min. Roots were imaged through a horizontal microscope"`, and p. 46 (Transparent Methods) repeats both the horizontal microscope setup and the `3 h` / `5 min` sampling interval (`37` profiles per root).
- **what would confirm it**: Checking whether retrieval ranks `Baskin2020` p. 4 or p. 46 above `Baskin2020` p. 2 on `a08`.

### A1-F5
- **id**: A1-F5
- **severity**: low
- **file and line**: `rag/gold.yaml:119-125` (`a17`), `staging/rag_corpus/Chaiwanon2015.pdf` p. 1, p. 2, p. 3, p. 6, p. 8, p. 11
- **claim**: The gold page for `a17` (`Chaiwanon2015` p. 1) is the journal cover/Highlights page rather than the article body (`Chaiwanon2015` p. 2–11), where the Summary, Introduction, Results, and Discussion state the same finding.
- **evidence**: `staging/rag_corpus/Chaiwanon2015.pdf` p. 1 contains only the Elsevier cover header, Highlights bullets (`"BR and auxin have opposite patterns and effects on cell elongation in root tip"`), and Graphical Abstract. The article title, Summary, and main text start on p. 2 (`"oppositely patterned and antagonistic actions of BR and auxin"`) and continue on p. 3, p. 6, p. 8, and p. 11.
- **what would confirm it**: Checking whether chunk/page retrieval for `a17` retrieves `Chaiwanon2015` p. 2, p. 6, p. 8, or p. 11 instead of the cover page p. 1.

## Per-Question Audit (`25` questions)

### Answerable questions (`a01`–`a20`)

All `20` questions are clear and answerable from text alone without reading a figure. Exact quotes ($\le 25$ words) for all `45` alternative page occurrences are in `docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv`.

| QID | Gold `(key, page)` | Gold answer correct & on gold page? | Text-only (not figure-only)? | Other pages stating the answer (`key:page`) |
| :-- | :-- | :-- | :-- | :-- |
| `a01` | `Mullen1998:1` | Yes (see A1-F3 on font encoding) | Yes | `Mullen1998:3`, `Mullen1998:4` (Table 1) |
| `a02` | `Mullen1998:1` | Yes | Yes | `Mullen1998:2` |
| `a03` | `Silk1979:1` | Yes | Yes | `Silk1979:5`, `Morris1992:3` |
| `a04` | `Silk1979:7` | Yes | Yes | None (`Silk1979:1` and `Silk1979:8` give only the 1D partial derivative $\partial v / \partial x$) |
| `a05` | `Morris1992:1` | Yes for `Morris1992` (`3`); see A1-F2 for `Henry2023` (`4`) | Yes | `Morris1992:4` (agrees: `3`), `Henry2023:6` (disagrees: `4`) |
| `a06` | `Wolverton2002:1` | Yes | Yes | `Wolverton2002:2` |
| `a07` | `Wolverton2002:3` | Yes | Yes | None |
| `a08` | `Baskin2020:2` | Yes | Yes | `Baskin2020:4`, `Baskin2020:5`, `Baskin2020:19`, `Baskin2020:29`, `Baskin2020:33`, `Baskin2020:36`, `Baskin2020:46` |
| `a09` | `Baskin2020:2` | Yes | Yes | `Baskin2020:4`, `Baskin2020:7`, `Baskin2020:8` |
| `a10` | `Henry2023:1` | Yes | Yes | `Henry2023:2`, `Henry2023:6`, `Henry2023:9` |
| `a11` | `Chaudhary2025:1` | Yes | Yes | `Chaudhary2025:5` |
| `a12` | `Krupar2026:1` | Yes | Yes | `Krupar2026:2`, `Krupar2026:3` |
| `a13` | `Krupar2026:1` | Yes | Yes | `Krupar2026:2`, `Krupar2026:3`, `Krupar2026:4` |
| `a14` | `Shih2014:1` | Yes | Yes | `Shih2014:4`, `Shih2014:5` |
| `a15` | `deBang2020:1` | Yes | Yes | `deBang2020:5`, `deBang2020:6` |
| `a16` | `Retzer2019:1` | Yes | Yes | `Retzer2019:9`, `Retzer2019:12` |
| `a17` | `Chaiwanon2015:1` | Yes (on Highlights page; see A1-F5) | Yes | `Chaiwanon2015:2`, `Chaiwanon2015:3`, `Chaiwanon2015:6`, `Chaiwanon2015:8`, `Chaiwanon2015:11` |
| `a18` | `Fridman2021:1` | Yes | Yes | `Fridman2021:2`, `Fridman2021:7`, `Fridman2021:8` |
| `a19` | `Bastien2014:1` | Yes | Yes | `Bastien2014:2`, `Bastien2014:8` |
| `a20` | `Nolan2023:3` | Yes | Yes | `Nolan2023_supplement:5`, `Nolan2023_supplement:10` |

### Out-of-corpus questions (`o01`–`o05`)

All `5` questions are clear and their answers are absent from all `17` included PDFs (`317` pages searched).

| QID | Topic | Absent terms in `rag/gold.yaml` | Truly absent from all 17 included files? | Notes from full-text search across 317 pages |
| :-- | :-- | :-- | :-- | :-- |
| `o01` | Poplar adventitious roots analysed with KymoRod (strain-rate threshold for end of growth zone) | `KymoRod`, `adventitious` | Yes | `KymoRod` and `adventitious` have `0` hits across all 17 PDFs. `Bastien2014:4` mentions poplar trunks (`Populus deltoides x nigra`), not adventitious roots or KymoRod. |
| `o02` | Poplar adventitious roots analysed with KymoRod (single kinematic proxy for root growth rate) | `KymoRod`, `adventitious`, `proxy for growth` | Yes | `0` hits for `KymoRod`, `adventitious`, or `proxy for growth` across all 17 PDFs. |
| `o03` | Root Walker automated root-imaging system fraction of roots lost in 12 h runs | `Root Walker`, `RootWalker`, `12 h runs` | Yes | `0` hits for `Root Walker`, `RootWalker`, or `Platre` across all 17 PDFs. |
| `o04` | Units of differential growth curvature rate (DGCR) along Arabidopsis roots | `DGCR`, `differential growth curvature rate` | Yes | `0` hits for `DGCR` or `differential growth curvature rate`. `Baskin2020:9,16` and `Bastien2014:2,10` cite `Chavarria-Krauser` (`2006`/`2008`) only in bibliography or general discussion without defining `DGCR` or its units. |
| `o05` | Kinematic analysis of bean basal roots over 6 h (upper vs lower root edge growth) | `basal root`, `upper edge` | Yes | `0` hits for `basal root` or `upper edge`. `Henry2023:2,6,12` and `Shih2014:6` cite `Basu et al. 2007` (`KineRoot`) only as prior software for tracking carborundum specks on bean roots without stating the 6 h upper-vs-lower edge result. |

## What was not checked

- Did not read `results/2026-11-02_rag/` or `staging/rag/` before writing this review (`docs/specs/2026-11-03_argon-audit.md:13`).
- Did not open, read, or use any excluded paper (`included = no` in `docs/context/literature/rag_corpus.csv`, OUP and Wiley).
- Did not re-score any RAG run (`docs/specs/2026-11-03_argon-audit.md:19`).
- Did not inspect bitmap/vector graphics inside PDF figures beyond the text layer extracted by `pypdf` (`rag/corpus.py:extract_pages`).
