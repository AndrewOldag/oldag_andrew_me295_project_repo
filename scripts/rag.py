"""RAG over the papers (spec 2026-11-02 B; proposal docs/proposals/2026-11-02_rag.md).

  python scripts/rag.py build              corpus check, page text, chunks, chunk embeddings (staging/rag/)
  python scripts/rag.py gold               check rag/gold.yaml against the page text
  python scripts/rag.py retrieval          BM25 and embedding ranks for every gold question (no LLM)
  python scripts/rag.py run --repeat R     one RAG repeat (R = 1, 2, 3): one claude -p call per question
  python scripts/rag.py report             results/2026-11-02_rag/: README, per-question table, metrics.json

`retrieval` and `run` refuse while rag/gold.yaml is not committed or has local changes.
Traces (with answer texts) stay in staging/rag/runs/. A restarted run skips finished questions.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag import corpus, retrieve, score  # noqa: E402
from rag.answer import ask, check  # noqa: E402

WORK = corpus.WORK
RUNS = WORK / "runs"
LIMIT_OUT = RUNS / "usage_limit"   # calls ended by the account usage limit: set aside, run again, counted
OUT = ROOT / "results" / "2026-11-02_rag"
REPEATS = (1, 2, 3)
MAX_CALLS = 150
MIN_FREE_GB = 3.0


def doi_by_key():
    return {r["key"]: r["doi"] for r in corpus.load_rows()}


def gold_committed():
    rel = "rag/gold.yaml"
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, capture_output=True).returncode == 0
    dirty = subprocess.run(["git", "status", "--porcelain", rel], cwd=ROOT, capture_output=True, text=True).stdout
    if not tracked or dirty.strip():
        sys.exit("rag/gold.yaml must be committed and unchanged before any retrieval or run")
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", rel], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()


def calls_so_far():
    n = len(list(RUNS.glob("r*_*.json"))) if RUNS.exists() else 0
    return n + (len(list(LIMIT_OUT.glob("*.json"))) if LIMIT_OUT.exists() else 0)


def cmd_build(_):
    pages, chunks = corpus.build()
    retrieve.Embedder([c.text for c in chunks], [c.cid for c in chunks])
    print(f"{len(pages)} papers, {sum(map(len, pages.values()))} pages, {len(chunks)} chunks; embeddings cached")


def cmd_gold(_):
    pages, _chunks = corpus.load()
    gold = score.load_gold()
    problems = score.check_gold(gold, pages, doi_by_key())
    text = {k: corpus.match_key(" ".join(v)) for k, v in pages.items()}
    for q in gold:
        if q["expect"] == "decline":
            for term in q.get("absent_terms", []):
                found = [k for k, t in text.items() if corpus.match_key(term) in t]
                if found:
                    problems.append(f"{q['id']}: term '{term}' found in {found}")
    n_ans = sum(q["expect"] == "answer" for q in gold)
    keys = {q["key"] for q in gold if q["expect"] == "answer"}
    print(f"{len(gold)} questions: {n_ans} answerable over {len(keys)} papers, {len(gold) - n_ans} out of corpus")
    print("\n".join(problems) if problems else "gold OK: every gold quote passes the check; absent terms absent")
    return 1 if problems else 0


def cmd_retrieval(_):
    sha = gold_committed()
    _pages, chunks = corpus.load()
    gold = score.load_gold()
    texts = [c.text for c in chunks]
    bm25, emb = retrieve.BM25(texts), retrieve.Embedder(texts, [c.cid for c in chunks])
    ranked = {"gold_commit": sha,
              "bm25": {q["id"]: bm25.top(q["question"], 10) for q in gold},
              "embed": {q["id"]: emb.top(q["question"], 10) for q in gold}}
    (WORK / "retrieval.json").write_text(json.dumps(ranked, indent=1), encoding="utf-8")
    for m in ("bm25", "embed"):
        print(m, score.retrieval_hits(gold, ranked[m], chunks)[1])


def is_usage_limit(rec):
    err = (rec.get("call") or {}).get("error", "").lower()
    return "session limit" in err or "usage limit" in err


def cmd_run(a):
    from agents.launcher import Launcher
    from measure.real_runner import vm_free_gb
    sha = gold_committed()
    free = vm_free_gb()
    if free < MIN_FREE_GB:
        sys.exit(f"free VM memory {free:.2f} GB, under {MIN_FREE_GB} GB: stop")
    print(f"free VM memory {free:.2f} GB; gold {sha}", flush=True)
    pages, chunks = corpus.load()
    dois = doi_by_key()
    gold = score.load_gold()
    emb = retrieve.Embedder([c.text for c in chunks], [c.cid for c in chunks])
    launcher = Launcher()
    RUNS.mkdir(parents=True, exist_ok=True)
    for q in gold:
        f = RUNS / f"r{a.repeat}_{q['id']}.json"
        if f.exists():
            continue
        if calls_so_far() >= MAX_CALLS:
            sys.exit(f"cap: {MAX_CALLS} LLM calls reached; stop")
        top = emb.top(q["question"], retrieve.TOP_K)
        t0 = time.time()
        res = ask(launcher, q["question"], [chunks[i] for i in top])
        action = res.structured_output if res.ok else None
        rec = {"id": q["id"], "repeat": a.repeat, "gold_commit": sha, "chunks": [chunks[i].cid for i in top],
               "call": res.record(), "action": action,
               "outcome": score.outcome(q, res.ok, action, pages, dois),
               "check": None if action is None else list(check(
                   action, pages, dois)), "wall_s": round(time.time() - t0, 1)}
        if is_usage_limit(rec):
            LIMIT_OUT.mkdir(parents=True, exist_ok=True)
            (LIMIT_OUT / f"{f.stem}_{time.strftime('%H%M%S')}.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
            sys.exit(f"usage limit on {q['id']}: call set aside in {LIMIT_OUT.name}/; stop")
        f.write_text(json.dumps(rec, indent=1), encoding="utf-8")
        print(f"r{a.repeat} {q['id']}: {rec['outcome']} ({rec['wall_s']} s)", flush=True)
    print(f"repeat {a.repeat} done; LLM calls so far {calls_so_far()}")


def cmd_report(_):
    _pages, chunks = corpus.load()
    gold = score.load_gold()
    reps = {}
    for r in REPEATS:
        recs = {q["id"]: RUNS / f"r{r}_{q['id']}.json" for q in gold}
        if all(f.exists() for f in recs.values()):
            reps[r] = {i: json.loads(f.read_text(encoding="utf-8")) for i, f in recs.items()}
    ranked = json.loads((WORK / "retrieval.json").read_text(encoding="utf-8"))
    hits = {m: score.retrieval_hits(gold, ranked[m], chunks) for m in ("bm25", "embed")}
    outcomes = {r: {i: rec["outcome"] for i, rec in v.items()} for r, v in reps.items()}
    per_rep = {r: score.repeat_metrics(gold, o) for r, o in outcomes.items()}
    calls = [rec["call"] for v in reps.values() for rec in v.values()]
    metrics = {
        "gold_commit": ranked["gold_commit"], "repeats": sorted(reps),
        "per_repeat": per_rep,
        "summary": {k: score.summary([m[k] for m in per_rep.values()])
                    for k in ("correct", "accuracy", "verified_quote_rate", "decline_precision", "decline_recall",
                              "errors")} if per_rep else {},
        "agreement": score.agreement(gold, list(outcomes.values())) if len(outcomes) > 1 else None,
        "retrieval": {m: {f"top{k}": n for k, n in h[1].items()} for m, h in hits.items()},
        "llm_calls": calls_so_far(), "set_aside_usage_limit": len(list(LIMIT_OUT.glob("*.json"))) if LIMIT_OUT.exists() else 0,
        "models": sorted({m for c in calls for m in c["models"]}),
        "claude_code": sorted({c["claude_version"] for c in calls}),
        "median_call_s": score.summary([c["duration_ms"] / 1000 for c in calls]),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf-8")
    rows = ["id,expect,key,bm25_top1,bm25_top5,embed_top1,embed_top5,embed_top6,"
            + ",".join(f"rag_r{r}" for r in sorted(reps))]
    for q in gold:
        h = [hits[m][0].get(q["id"]) for m in ("bm25", "embed")]
        cells = ["" if x is None else str(int(x[k])) for x, ks in zip(h, ((1, 5), (1, 5, 6))) for k in ks]
        rows.append(",".join([q["id"], q["expect"], q.get("key", "")] + cells
                             + [outcomes[r][q["id"]] for r in sorted(reps)]))
    (OUT / "per_question.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({k: metrics[k] for k in ("summary", "agreement", "retrieval", "llm_calls")}, indent=1))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("build", "gold", "retrieval", "report"):
        sub.add_parser(name)
    r = sub.add_parser("run")
    r.add_argument("--repeat", type=int, choices=REPEATS, required=True)
    a = p.parse_args()
    sys.exit({"build": cmd_build, "gold": cmd_gold, "retrieval": cmd_retrieval, "run": cmd_run,
              "report": cmd_report}[a.cmd](a))


if __name__ == "__main__":
    main()
