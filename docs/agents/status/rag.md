# rag
Updated: 2026-11-02 15:35 (local)
Lane: course
Branch: wip/rag
Last inbox item done: 2
State: working
Now: item 3, B6: retrieval (BM25, embeddings), then 3 RAG repeats once the embedding build ends and free memory is at least 3 GB
Done since last update:
- B2: zip unzipped to staging/rag_corpus/: 17 PDFs plus SHA256SUMS (the zip's own manifest, equal to the csv); 17 of 17 sha256 match the csv; no missing, no extra
- B2: DOI filled for Baskin2020 (printed on page 1). Morris1992, Mullen1998, Silk1979 print no DOI on their first pages; left empty
- pypdf 6.21.4 and fastembed 0.9.1 (ONNX CPU embeddings) installed in the agents env and added to environment.yml
- B3: proposal docs/proposals/2026-11-02_rag.md committed (chunks in page, bge-small embeddings top 6, BM25 baseline, 75 LLM calls planned, cap 150)
- B4: rag/ (corpus, retrieve, answer, score), scripts/rag.py, tests/test_rag.py 25 passed. 17 papers, 317 pages, 693 chunks (median 300 words, max 349). Proposal amended before any run: Wolverton2002 extracts as glyph codes; decoded
- B5: rag/gold.yaml committed before any retrieval or run: 20 answerable over 15 papers (each gold quote passes the code check), 5 out of corpus (question only; terms checked absent). Test suite for rag 26 passed
Needs Andrew:
- none
