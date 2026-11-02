"""Corpus: the csv, page text, normalisation, chunks.

- Only rows with `included = yes` are read. The excluded papers are never opened
- Page number = PDF page index, from 1
- `norm` is the one normalisation used for chunks, BM25 and the quote check
"""
import csv
import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "docs" / "context" / "literature" / "rag_corpus.csv"
PDF_DIR = ROOT / "staging" / "rag_corpus"
WORK = ROOT / "staging" / "rag"

CHUNK_WORDS = 300
OVERLAP = 50
ONE_CHUNK_MAX = 350
MIN_LAST = 100

_MAP = {"­": "", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
        "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "−": "-",
        "‘": "'", "’": "'", "“": '"', "”": '"'}
_MAP_RE = re.compile("|".join(map(re.escape, _MAP)))


def norm(text):
    """NFKC; ligatures, soft hyphens, dashes, curly quotes; line-end hyphens joined; whitespace collapsed."""
    t = unicodedata.normalize("NFKC", text)
    t = _MAP_RE.sub(lambda m: _MAP[m.group(0)], t)
    t = re.sub(r"(?<=[A-Za-z])-[ \t]*\n\s*(?=[a-z])", "", t)
    return re.sub(r"\s+", " ", t).strip()


def match_key(text):
    """Form used to compare a quote with page text: normalised and lowercased."""
    return norm(text).lower()


def load_rows(path=CSV):
    with open(path, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["included"] == "yes"]


def check_hashes(rows, pdf_dir=PDF_DIR):
    """Return (missing, extra, mismatched) file names. SHA256SUMS is the zip's own manifest."""
    want = {r["file"]: r["sha256"] for r in rows}
    have = {p.name for p in Path(pdf_dir).iterdir() if p.name != "SHA256SUMS"}
    bad = [f for f in sorted(want) if f in have
           and hashlib.sha256((Path(pdf_dir) / f).read_bytes()).hexdigest() != want[f]]
    return sorted(set(want) - have), sorted(have - set(want)), bad


_GLYPH = re.compile(r"/C(\d{1,3})")
_GLYPH_MAP = {128: "ff", 174: "fi", 175: "fl", 177: "-"}


def decode_glyphs(text):
    """pypdf writes `/C<code>` for glyphs of a font without a Unicode map (all of Wolverton2002, a few
    ligatures in Mullen1998). Codes 32-126 are ASCII; 128, 174, 175 the ff, fi, fl ligatures; 177 an
    en dash; other codes (symbols) are dropped."""
    def sub(m):
        c = int(m.group(1))
        return chr(c) if 32 <= c <= 126 else _GLYPH_MAP.get(c, "")
    return _GLYPH.sub(sub, text)


def extract_pages(pdf_path):
    from pypdf import PdfReader
    return [norm(decode_glyphs(p.extract_text() or "")) for p in PdfReader(str(pdf_path)).pages]


def chunk_page(words):
    """Word windows inside one page (proposal: 300 words, 50 overlap, last window under 100 merged)."""
    if len(words) <= ONE_CHUNK_MAX:
        return [words] if words else []
    step = CHUNK_WORDS - OVERLAP
    spans = []
    start = 0
    while start < len(words):
        spans.append([start, min(start + CHUNK_WORDS, len(words))])
        if spans[-1][1] == len(words):
            break
        start += step
    if len(spans) > 1 and spans[-1][1] - spans[-1][0] < MIN_LAST:
        last = spans.pop()
        spans[-1][1] = last[1]
    return [words[a:b] for a, b in spans]


@dataclass
class Chunk:
    cid: str
    key: str
    page: int
    doi: str
    text: str


def build_chunks(pages_by_key, doi_by_key):
    chunks = []
    for key in sorted(pages_by_key):
        for i, text in enumerate(pages_by_key[key], start=1):
            for j, words in enumerate(chunk_page(text.split())):
                chunks.append(Chunk(f"{key}:p{i}:c{j}", key, i, doi_by_key[key], " ".join(words)))
    return chunks


def build(work=WORK, pdf_dir=PDF_DIR, csv_path=CSV):
    """Check hashes, extract every page, write pages.json and chunks.json under `work`."""
    rows = load_rows(csv_path)
    missing, extra, bad = check_hashes(rows, pdf_dir)
    if missing or extra or bad:
        raise RuntimeError(f"corpus check failed: missing {missing}, extra {extra}, sha256 mismatch {bad}")
    pages = {r["key"]: extract_pages(Path(pdf_dir) / r["file"]) for r in rows}
    chunks = build_chunks(pages, {r["key"]: r["doi"] for r in rows})
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    (work / "pages.json").write_text(json.dumps(pages), encoding="utf-8")
    (work / "chunks.json").write_text(json.dumps([asdict(c) for c in chunks]), encoding="utf-8")
    return pages, chunks


def load(work=WORK):
    work = Path(work)
    pages = json.loads((work / "pages.json").read_text(encoding="utf-8"))
    chunks = [Chunk(**c) for c in json.loads((work / "chunks.json").read_text(encoding="utf-8"))]
    return pages, chunks
