# rag
Updated: 2026-11-02 14:40 (local)
Lane: course
Branch: wip/rag
Last inbox item done: 2
State: working
Now: item 3, B4: build rag/ and tests/test_rag.py
Done since last update:
- B2: zip unzipped to staging/rag_corpus/: 17 PDFs plus SHA256SUMS (the zip's own manifest, equal to the csv); 17 of 17 sha256 match the csv; no missing, no extra
- B2: DOI filled for Baskin2020 (printed on page 1). Morris1992, Mullen1998, Silk1979 print no DOI on their first pages; left empty
- pypdf 6.21.4 and fastembed 0.9.1 (ONNX CPU embeddings) installed in the agents env and added to environment.yml
- B3: proposal docs/proposals/2026-11-02_rag.md committed (chunks in page, bge-small embeddings top 6, BM25 baseline, 75 LLM calls planned, cap 150)
Needs Andrew:
- none
