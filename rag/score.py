"""Gold set, outcomes and metrics (proposal docs/proposals/2026-11-02_rag.md).

Outcomes, answerable: correct, wrong_source, unverified, declined, error.
Outcomes, out of corpus: declined (correct), answered_verified, unverified, error.
"""
from pathlib import Path
from statistics import median

import yaml

from rag.answer import check

GOLD = Path(__file__).resolve().parent / "gold.yaml"
GOLD_QUOTE_WORDS = 25


def load_gold(path=GOLD):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["questions"]


def gold_pages(q):
    """Accepted (key, page) pairs: the gold page and its alt pages."""
    return {(q["key"], q["page"])} | {(q["key"], a["page"]) for a in q.get("alt", [])}


def check_gold(gold, pages, doi_by_key):
    """Problems with the gold set itself; empty = every gold quote passes the answer check."""
    problems = []
    if len({q["id"] for q in gold}) != len(gold):
        problems.append("duplicate ids")
    for q in gold:
        if q["expect"] == "decline":
            if any(f in q for f in ("key", "page", "quote", "answer")):
                problems.append(f"{q['id']}: out-of-corpus entry holds a key, page, quote or answer")
            continue
        for p, quote in [(q["page"], q["quote"])] + [(a["page"], a["quote"]) for a in q.get("alt", [])]:
            act = {"action": "answer", "text": q["answer"], "quote": quote, "key": q["key"], "page": p,
                   "doi": doi_by_key.get(q["key"], "")}
            _, errs = check(act, pages, doi_by_key, quote_words=GOLD_QUOTE_WORDS)
            problems += [f"{q['id']} p{p}: {e}" for e in errs]
        if q["quote"].lower() in q["question"].lower():
            problems.append(f"{q['id']}: question contains its gold quote")
    return problems


def outcome(q, call_ok, action, pages, doi_by_key):
    if not call_ok:
        return "error"
    kind, problems = check(action, pages, doi_by_key)
    if kind == "invalid":
        return "error"
    if q["expect"] == "decline":
        if kind == "decline":
            return "declined"
        return "unverified" if problems else "answered_verified"
    if kind == "decline":
        return "declined"
    if problems:
        return "unverified"
    return "correct" if (action["key"], action["page"]) in gold_pages(q) else "wrong_source"


def repeat_metrics(gold, outcomes):
    """outcomes: id -> outcome for one repeat."""
    ans = [q for q in gold if q["expect"] == "answer"]
    ooc = [q for q in gold if q["expect"] == "decline"]
    o = [outcomes[q["id"]] for q in gold]
    answers = sum(x in ("correct", "wrong_source", "unverified", "answered_verified") for x in o)
    verified = sum(x in ("correct", "wrong_source", "answered_verified") for x in o)
    declines = sum(x == "declined" for x in o)
    ooc_declines = sum(outcomes[q["id"]] == "declined" for q in ooc)
    return {
        "correct": sum(outcomes[q["id"]] == "correct" for q in ans), "n_answerable": len(ans),
        "accuracy": sum(outcomes[q["id"]] == "correct" for q in ans) / len(ans),
        "answers": answers, "verified": verified,
        "verified_quote_rate": verified / answers if answers else None,
        "declines": declines, "ooc_declines": ooc_declines, "n_ooc": len(ooc),
        "decline_precision": ooc_declines / declines if declines else None,
        "decline_recall": ooc_declines / len(ooc),
        "errors": sum(x == "error" for x in o),
    }


def agreement(gold, repeats):
    """Fraction of questions with the same outcome in every repeat."""
    same = sum(len({r[q["id"]] for r in repeats}) == 1 for q in gold)
    return same / len(gold)


def summary(values):
    vals = [v for v in values if v is not None]
    return {"median": median(vals), "min": min(vals), "max": max(vals)} if vals else None


def retrieval_hits(gold, ranked, chunks, ks=(1, 5, 6)):
    """ranked: id -> chunk indices best first. Returns per-question hit flags and counts at each k."""
    ans = [q for q in gold if q["expect"] == "answer"]
    per_q = {}
    for q in ans:
        target = gold_pages(q)
        hits = [(chunks[i].key, chunks[i].page) in target for i in ranked[q["id"]]]
        per_q[q["id"]] = {k: any(hits[:k]) for k in ks}
    counts = {k: sum(per_q[i][k] for i in per_q) for k in ks}
    return per_q, counts
