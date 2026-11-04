---
id: c024
title: RAG index over the non-OUP, non-Wiley papers, scored against keyword search
lane: course
owner: rag
state: working
branch: wip/rag
host: VM
created: 2026-11-02 14:10
last_update: 2026-11-02 16:20
blocker: none
done_marker: results/2026-11-02_rag/README.md
---

Inbox: rag. Spec 2026-11-02 section B.

## Parts
- [x] Corpus zip found, unzipped to staging/rag_corpus/, sha256 checked, DOIs filled
- [x] Proposal docs/proposals/2026-11-02_rag.md committed
- [x] rag/ code and tests/test_rag.py
- [x] Gold set rag/gold.yaml committed (20 answerable, 5 out of corpus)
- [x] Scoring: RAG 3 repeats, keyword baseline
- [x] Results README, decisions, log
