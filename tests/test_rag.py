"""Tests for rag/: normalisation, chunks, the answer check, outcomes, metrics, BM25, gold set.

Offline. The gold-set test needs the staged page text (staging/rag/pages.json) and is skipped without it.
"""
import pytest

from rag import corpus, score
from rag.answer import SCHEMA, build_prompt, check
from rag.corpus import Chunk, chunk_page, match_key, norm
from rag.retrieve import BM25

PAGES = {"A2000": ["Title page.", "The relative elemental growth rate peaks 0.5 mm from the tip in these roots."],
         "B2001": [norm("Roots were imaged every 5 min under infra-\nred light.")]}   # pages are stored normalised
DOIS = {"A2000": "10.1/a", "B2001": ""}


def answer(**kw):
    a = {"action": "answer", "text": "About 0.5 mm.", "quote": "peaks 0.5 mm from the tip", "key": "A2000",
         "page": 2, "doi": "10.1/a"}
    a.update(kw)
    return a


def test_norm_ligatures_hyphens_whitespace():
    assert norm("eﬃcient  \n flow") == "efficient flow"
    assert norm("elon-\ngation") == "elongation"
    assert norm("“growth” – rate­") == '"growth" - rate'
    assert norm(norm("elon-\n gation x")) == norm("elon-\n gation x")


def test_norm_keeps_hyphen_before_capital_or_inside_line():
    assert norm("REGR-\nBased") == "REGR- Based"
    assert norm("time-lapse") == "time-lapse"


def test_decode_glyphs():
    assert corpus.decode_glyphs("/C84/C104/C101 /C174/C110/C100 di/C128er /C49/C177/C50 /C20x") == "The find differ 1-2 x"


def test_chunk_page_sizes():
    assert chunk_page([]) == []
    assert len(chunk_page(["w"] * 350)) == 1
    w = [str(i) for i in range(1000)]
    ch = chunk_page(w)
    assert all(250 <= len(c) <= 350 for c in ch)
    assert ch[0][-50:] == ch[1][:50]          # 50-word overlap
    assert ch[-1][-1] == "999"


def test_chunk_page_merges_short_last_window_into_the_one_before():
    ch = chunk_page([str(i) for i in range(560)])   # windows 0-300, 250-550, 500-560 (60 words): merged
    assert [len(c) for c in ch] == [300, 310]
    assert ch[-1][0] == "250" and ch[-1][-1] == "559"


def test_build_chunks_carry_key_page_doi():
    ch = corpus.build_chunks(PAGES, DOIS)
    assert [(c.key, c.page, c.doi) for c in ch] == [("A2000", 1, "10.1/a"), ("A2000", 2, "10.1/a"), ("B2001", 1, "")]
    assert ch[2].text == "Roots were imaged every 5 min under infrared light."


def test_check_verified_answer():
    assert check(answer(), PAGES, DOIS) == ("answer", [])


def test_check_quote_normalised_case_and_hyphenation():
    a = answer(key="B2001", page=1, doi="", quote="Imaged every 5 min under infra-\n red LIGHT")
    assert check(a, PAGES, DOIS) == ("answer", [])


@pytest.mark.parametrize("kw, problem", [
    ({"page": 1}, "quote not on that page"),
    ({"quote": "peaks 0.7 mm from the tip"}, "quote not on that page"),
    ({"doi": "10.1/b"}, "doi differs from the csv"),
    ({"key": "C1999"}, "key C1999 not in corpus"),
    ({"page": 9}, "page 9 outside 1-2"),
    ({"quote": "  "}, "empty quote"),
    ({"page": "2"}, "field page missing or wrong type"),
])
def test_check_failures_are_reported_not_repaired(kw, problem):
    kind, problems = check(answer(**kw), PAGES, DOIS)
    assert kind == "answer" and problem in problems


def test_check_word_limits():
    assert "quote over 40 words" in check(answer(quote="x " * 41), PAGES, DOIS)[1]
    assert "text over 60 words" in check(answer(text="x " * 61), PAGES, DOIS)[1]


def test_check_decline_and_invalid():
    assert check({"action": "decline", "reason": "not in corpus"}, PAGES, DOIS) == ("decline", [])
    assert check({"action": "decline"}, PAGES, DOIS)[0] == "invalid"
    assert check({"action": "guess"}, PAGES, DOIS)[0] == "invalid"
    assert check(None, PAGES, DOIS)[0] == "invalid"


def test_schema_and_prompt():
    assert SCHEMA["properties"]["action"]["enum"] == ["answer", "decline"]
    p = build_prompt("Where?", [Chunk("A2000:p2:c0", "A2000", 2, "10.1/a", "text")])
    assert "[1] key: A2000 | page: 2 | doi: 10.1/a" in p and p.startswith("Question: Where?")


Q_ANS = {"id": "q1", "expect": "answer", "key": "A2000", "page": 2, "quote": "peaks 0.5 mm", "answer": "0.5 mm",
         "alt": [{"page": 1, "quote": "Title page"}]}
Q_OOC = {"id": "q2", "expect": "decline", "question": "x"}


def test_outcomes_answerable():
    o = lambda ok, a: score.outcome(Q_ANS, ok, a, PAGES, DOIS)  # noqa: E731
    assert o(True, answer()) == "correct"
    assert o(True, answer(page=1, quote="Title page")) == "correct"           # alt page
    assert o(True, answer(key="B2001", page=1, doi="", quote="imaged every 5 min")) == "wrong_source"
    assert o(True, answer(quote="peaks 9 mm")) == "unverified"
    assert o(True, {"action": "decline", "reason": "not in corpus"}) == "declined"
    assert o(False, None) == "error"
    assert o(True, {"action": "decline"}) == "error"


def test_outcomes_out_of_corpus():
    o = lambda a: score.outcome(Q_OOC, True, a, PAGES, DOIS)  # noqa: E731
    assert o({"action": "decline", "reason": "not in corpus"}) == "declined"
    assert o(answer()) == "answered_verified"
    assert o(answer(quote="nothing like this")) == "unverified"


def test_repeat_metrics_and_agreement():
    gold = [Q_ANS, dict(Q_ANS, id="q3"), Q_OOC, dict(Q_OOC, id="q4")]
    m = score.repeat_metrics(gold, {"q1": "correct", "q3": "declined", "q2": "declined", "q4": "unverified"})
    assert (m["correct"], m["accuracy"]) == (1, 0.5)
    assert (m["answers"], m["verified"], m["verified_quote_rate"]) == (2, 1, 0.5)
    assert (m["decline_precision"], m["decline_recall"]) == (0.5, 0.5)
    r1 = {"q1": "correct", "q3": "declined", "q2": "declined", "q4": "declined"}
    r2 = dict(r1, q4="unverified")
    assert score.agreement(gold, [r1, r1, r2]) == 0.75


def test_retrieval_hits_use_gold_and_alt_pages():
    ch = corpus.build_chunks(PAGES, DOIS)              # 0: A2000 p1, 1: A2000 p2, 2: B2001 p1
    per_q, counts = score.retrieval_hits([Q_ANS, Q_OOC], {"q1": [2, 0, 1]}, ch)
    assert per_q["q1"] == {1: False, 5: True, 6: True} and counts == {1: 0, 5: 1, 6: 1}


def test_check_gold_flags_bad_entries():
    good = dict(Q_ANS, question="Where does growth peak?")
    assert score.check_gold([good, Q_OOC], PAGES, DOIS) == []
    bad_quote = dict(good, id="q5", quote="peaks 2 mm")
    leak = dict(Q_OOC, id="q6", key="A2000")
    probs = score.check_gold([bad_quote, leak], PAGES, DOIS)
    assert any("q5 p2: quote not on that page" in p for p in probs)
    assert any("q6: out-of-corpus entry" in p for p in probs)


def test_bm25_ranks_the_matching_chunk_first():
    texts = ["growth rate peaks near the tip", "images every five minutes", "the cell wall is rigid"]
    b = BM25(texts)
    assert b.top("where does the growth rate peak", 3)[0] == 0
    assert b.top("five minutes images", 1) == [1]


def test_match_key_is_case_insensitive():
    assert match_key("REGR  Peaks") == "regr peaks"


@pytest.mark.skipif(not (corpus.WORK / "pages.json").exists() or not score.GOLD.exists(),
                    reason="needs staged page text and rag/gold.yaml")
def test_gold_set_passes_its_own_check():
    pages, _ = corpus.load()
    gold = score.load_gold()
    assert score.check_gold(gold, pages, {r["key"]: r["doi"] for r in corpus.load_rows()}) == []
    assert sum(q["expect"] == "answer" for q in gold) == 20 and sum(q["expect"] == "decline" for q in gold) == 5
    assert len({q["key"] for q in gold if q["expect"] == "answer"}) >= 10
    assert all(len(q["quote"].split()) <= score.GOLD_QUOTE_WORDS for q in gold if q["expect"] == "answer")
