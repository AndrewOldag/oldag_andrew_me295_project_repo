"""Post-hoc re-score of the saved RAG answers (inbox rag item 4, Andrew 2026-11-03). No LLM calls.

The scored result (rag/score.py) stays primary. This adds, from the saved traces:
- alt pages from a second reader who had not seen the results
  (docs/reviews/2026-11-03_argon-rag-gold/alt_pages.csv, rows with agrees_with_gold = yes)
- a05 marked ambiguous (two included papers give different counts); metrics with and without it
- Mullen1998 extraction artefacts mapped in the quote check, if the mapping is exact on all its pages
"""
import csv
import re
from pathlib import Path

from rag.answer import check
from rag.score import gold_pages

ROOT = Path(__file__).resolve().parents[1]
ALT_CSV = ROOT / "docs" / "reviews" / "2026-11-03_argon-rag-gold" / "alt_pages.csv"
AMBIGUOUS = {"a05"}

PLUS_MINUS = r"\x8b"
MICRO = r"(?<![A-Za-z])lm(?![A-Za-z])"   # standalone token only; lmh, lmol, lma, lmb are left as they are
ARTEFACTS = {"Mullen1998": [(PLUS_MINUS, "±"), (MICRO, "µm")]}


def load_alt(path=ALT_CSV):
    """qid -> {(key, page)} from rows that agree with the gold answer."""
    out = {}
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["agrees_with_gold"].strip().lower() == "yes":
                out.setdefault(r["qid"], set()).add((r["key"], int(r["page"])))
    return out


def artefact_map_exact(pages):
    """The mapping is exact when every \\x8b sits between numbers or in 'mean \\x8b SD' (plus-minus), and every
    standalone 'lm' follows a number (micrometre). Returns (exact, counts, misfits)."""
    misfits, n_pm, n_mu = [], 0, 0
    for i, p in enumerate(pages, start=1):
        for m in re.finditer(PLUS_MINUS, p):
            n_pm += 1
            before, after = p[max(0, m.start() - 6):m.start()], p[m.end():m.end() + 4]
            if not ((re.search(r"(\d|mean) ?$", before)) and re.match(r" ?(\d|SD)", after)):
                misfits.append(f"p{i} plus-minus: {before!r}|{after!r}")
        for m in re.finditer(MICRO, p):
            n_mu += 1
            if not re.search(r"\d[ -]?$", p[max(0, m.start() - 3):m.start()]):
                misfits.append(f"p{i} micrometre: {p[max(0, m.start() - 10):m.end()]!r}")
    return not misfits, {"plus_minus": n_pm, "micrometre": n_mu}, misfits


def outcome(q, rec, pages, doi_by_key, alt, artefacts=None):
    """Post-hoc outcome of one saved trace: as rag/score.outcome, with the alt pages accepted and the
    artefact map in the quote check."""
    if q["expect"] == "decline" or rec["action"] is None:
        return rec["outcome"]
    kind, problems = check(rec["action"], pages, doi_by_key, artefacts=artefacts)
    if kind == "invalid":
        return "error"
    if kind == "decline":
        return "declined"
    if problems:
        return "unverified"
    a = rec["action"]
    return "correct" if (a["key"], a["page"]) in gold_pages(q) | alt.get(q["id"], set()) else "wrong_source"
