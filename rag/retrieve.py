"""Retrievers over the same chunks: BM25 (keyword baseline) and local embeddings (RAG).

Both return chunk indices, best first.
"""
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from rag.corpus import WORK

EMBED_MODEL = "BAAI/bge-small-en-v1.5"   # fastembed 0.9.1, ONNX, CPU (proposal 2026-11-02)
TOP_K = 6
BATCH = 16
_TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    return [t for t in _TOKEN.findall(text.lower()) if len(t) >= 2]


class BM25:
    def __init__(self, texts, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / len(self.lens)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query):
        q = set(tokens(query))
        out = np.zeros(len(self.docs))
        for i, (d, dl) in enumerate(zip(self.docs, self.lens)):
            norm = self.k1 * (1 - self.b + self.b * dl / self.avg)
            out[i] = sum(self.idf[t] * d[t] * (self.k1 + 1) / (d[t] + norm) for t in q if t in d)
        return out

    def top(self, query, k):
        s = self.scores(query)
        return [int(i) for i in np.argsort(-s, kind="stable")[:k]]


class Embedder:
    """Chunk vectors cached in staging/rag/embeddings.npy, keyed by a hash of the model, ids and texts."""

    def __init__(self, texts, ids, work=WORK, cache_dir=None):
        from fastembed import TextEmbedding
        self.model = TextEmbedding(EMBED_MODEL, cache_dir=str(cache_dir or Path(work) / "models"))
        vec_file, key_file = Path(work) / "embeddings.npy", Path(work) / "embeddings.key"
        key = hashlib.sha256(json.dumps([EMBED_MODEL, list(ids), list(texts)]).encode("utf-8")).hexdigest()
        if vec_file.exists() and key_file.exists() and key_file.read_text(encoding="utf-8") == key:
            self.vecs = np.load(vec_file)
        else:
            # batch 16: the default 256 took about 5 GB on the VM (2026-11-02)
            self.vecs = self._unit(np.array(list(self.model.passage_embed(texts, batch_size=BATCH))))
            np.save(vec_file, self.vecs)
            key_file.write_text(key, encoding="utf-8")

    @staticmethod
    def _unit(v):
        return v / np.linalg.norm(v, axis=1, keepdims=True)

    def top(self, query, k):
        q = self._unit(np.array(list(self.model.query_embed([query]))))[0]
        return [int(i) for i in np.argsort(-(self.vecs @ q), kind="stable")[:k]]
