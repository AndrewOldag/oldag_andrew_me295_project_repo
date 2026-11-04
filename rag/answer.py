"""Answerer: one `claude -p` call returns one typed action; plain-Python code checks it.

- `answer` {text, quote, key, page, doi} or `decline` {reason: not in corpus}
- Check: action valid; key in corpus; DOI equals the csv; the quote (normalised,
  lowercased) occurs on that page of that paper's extracted text
- A failed check is an unverified answer. It is never repaired
"""
import re
from pathlib import Path

from rag.corpus import match_key

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "answerer.md"
EFFORT = "medium"
MAX_TURNS = 3
TEXT_WORDS = 60
QUOTE_WORDS = 40
DECLINE_REASON = "not in corpus"

SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["answer", "decline"]},
        "text": {"type": "string"},
        "quote": {"type": "string"},
        "key": {"type": "string"},
        "page": {"type": "integer"},
        "doi": {"type": "string"},
        "reason": {"type": "string", "enum": [DECLINE_REASON]},
    },
    "required": ["action"],
    "additionalProperties": False,
}


def build_prompt(question, chunks):
    parts = [f"Question: {question}", "", "Excerpts:"]
    for n, c in enumerate(chunks, start=1):
        parts += ["", f"[{n}] key: {c.key} | page: {c.page} | doi: {c.doi}", c.text]
    return "\n".join(parts)


def check(action, pages, doi_by_key, quote_words=QUOTE_WORDS, artefacts=None):
    """Return (kind, problems). kind: answer, decline or invalid. problems empty = verified.

    artefacts: optional {key: [(regex, replacement), ...]} applied to that paper's page text and to the
    quote before matching (post-hoc only, rag/posthoc.py; the scored check uses none)."""
    if not isinstance(action, dict) or action.get("action") not in ("answer", "decline"):
        return "invalid", ["no valid action"]
    if action["action"] == "decline":
        ok = action.get("reason") == DECLINE_REASON
        return ("decline", []) if ok else ("invalid", ["decline without reason 'not in corpus'"])
    problems = []
    for f, t in (("text", str), ("quote", str), ("key", str), ("page", int), ("doi", str)):
        if not isinstance(action.get(f), t) or isinstance(action.get(f), bool):
            problems.append(f"field {f} missing or wrong type")
    if problems:
        return "answer", problems
    key, page, quote = action["key"], action["page"], action["quote"]
    if len(action["text"].split()) > TEXT_WORDS:
        problems.append(f"text over {TEXT_WORDS} words")
    if not quote.strip():
        problems.append("empty quote")
    elif len(quote.split()) > quote_words:
        problems.append(f"quote over {quote_words} words")
    if key not in pages:
        return "answer", problems + [f"key {key} not in corpus"]
    if action["doi"].strip() != doi_by_key[key]:
        problems.append("doi differs from the csv")
    if not 1 <= page <= len(pages[key]):
        return "answer", problems + [f"page {page} outside 1-{len(pages[key])}"]
    page_text = pages[key][page - 1]
    for pat, rep in (artefacts or {}).get(key, []):
        page_text, quote = re.sub(pat, rep, page_text), re.sub(pat, rep, quote)
    if quote.strip() and match_key(quote) not in match_key(page_text):
        problems.append("quote not on that page")
    return "answer", problems


def ask(launcher, question, chunks, system_prompt=None):
    """One call. Returns the launcher's CallResult."""
    system_prompt = system_prompt or PROMPT_FILE.read_text(encoding="utf-8")
    return launcher.call(build_prompt(question, chunks), system_prompt, SCHEMA, EFFORT, MAX_TURNS)
