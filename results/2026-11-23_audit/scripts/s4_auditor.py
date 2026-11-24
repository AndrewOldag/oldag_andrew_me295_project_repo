"""S4 audit: recompute results/2026-11-18_auditor_check from batches.json, run_map.json, rule/*.json and
llm/*_result.json (not from scores.json). Read-only."""
import json
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).resolve().parents[3] / "results"
A = R / "2026-11-18_auditor_check"
js = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))  # noqa: E731
batches = {b["batch"]: b for b in js(A / "batches.json")["batches"]}
rmap = js(A / "run_map.json")
print("batches", len(batches), "sizes", Counter(len(b["runs"]) for b in batches.values()))
plant = {}
for b, m in rmap.items():
    p = [(rid, v.split(":")[1]) for rid, v in m.items() if v.startswith("PLANT:")]
    plant[b] = p[0] if p else (None, "none")
print("plants per kind", Counter(k for _, k in plant.values()))

# are all batch runs good accepted freeze v4 runs?
v4 = {(f"{r['method']}_{r['rod']}" + (f"_r{r['repeat']}" if r["method"] in ("diagnostician", "single_agent") else "")): r
      for r in js(R / "2026-10-25_freeze_v4" / "scores.json")}
notgood = [(b, x) for b, B in batches.items() for x in B["runs"] if x not in v4 or v4[x]["status"] != "accept" or not v4[x]["good"]]
print("batch runs not a good accepted v4 run:", notgood[:10], len(notgood))
rows_ok = all(len({v4[x]["kind"] for x in B["runs"] if x in v4}) == 1 for B in batches.values())
print("each batch from one row:", rows_ok)

dec = defaultdict(dict)   # (auditor, repeat) -> {(batch, rid): decision}
for b in batches:
    for rid, d in js(A / "rule" / f"{b}.json")["decisions"].items():
        dec[("rule", 0)][(b, rid)] = d["decision"]
llm_res = {}
for k in (0, 1, 2):
    for b in batches:
        res = js(A / "llm" / f"{b}_r{k}_result.json")
        llm_res[(b, k)] = res
        for rid in rmap[b]:
            d = (res.get("decisions") or {}).get(rid)
            dec[("llm", k)][(b, rid)] = d["decision"] if d else "undecided"
for key, D in dec.items():
    catch, fa = Counter(), Counter()
    for b in batches:
        prid, kind = plant[b]
        for rid in rmap[b]:
            f = D[(b, rid)] == "flag"
            if rid == prid:
                catch[kind] += f
                catch["all"] += f
            else:
                fa[kind] += f
                fa["all"] += f
    print(key, "catches", dict(catch), "| false alarms by batch plant", dict(fa),
          "| undecided", sum(v == "undecided" for v in D.values()))

# agreement over the 3 LLM repeats (flag, clear, undecided)
keys = list(dec[("llm", 0)])
decided = [x for x in keys if all(dec[("llm", k)][x] != "undecided" for k in (0, 1, 2))]
un = [x for x in decided if len({dec[("llm", k)][x] for k in (0, 1, 2)}) == 1]
cats = ("flag", "clear", "undecided")
counts = [[sum(dec[("llm", k)][x] == c for k in (0, 1, 2)) for c in cats] for x in keys]
n, N = 3, len(counts)
pbar = sum((sum(v * v for v in c) - n) / (n * (n - 1)) for c in counts) / N
pj = [sum(c[j] for c in counts) / (N * n) for j in range(3)]
pe = sum(p * p for p in pj)
print("runs", len(keys), "decided in all 3", len(decided), "unanimous", len(un), "kappa over all runs %.3f" % ((pbar - pe) / (1 - pe)))
counts_d = [[sum(dec[("llm", k)][x] == c for k in (0, 1, 2)) for c in cats] for x in decided]
N = len(counts_d)
pbar = sum((sum(v * v for v in c) - n) / (n * (n - 1)) for c in counts_d) / N
pj = [sum(c[j] for c in counts_d) / (N * n) for j in range(3)]
pe = sum(p * p for p in pj)
print("kappa over decided runs %.3f" % ((pbar - pe) / (1 - pe)))
pl = [(b, plant[b][0]) for b in batches if plant[b][0]]
split = [(b, [dec[("llm", k)][(b, r)] for k in (0, 1, 2)]) for b, r in pl if len({dec[("llm", k)][(b, r)] for k in (0, 1, 2)}) > 1]
print("planted unanimous", len(pl) - len(split), "of", len(pl), "split", split, [batches[b]["row"] for b, _ in split])

# reasons on planted runs
for kind in ("closure_relabelled", "wrong_unit", "doubled_frame", "other_rod_track"):
    rs = Counter()
    for b in batches:
        prid, k = plant[b]
        if k != kind:
            continue
        for kk in (0, 1, 2):
            d = (llm_res[(b, kk)].get("decisions") or {}).get(prid) or {}
            rs[(d.get("decision"), d.get("reason"), tuple(d.get("evidence") or []))] += 1
        rr = js(A / "rule" / f"{b}.json")["decisions"][prid]
        rs[("rule", rr["decision"], tuple(rr["reasons"]))] += 1
    print(kind, dict(rs))

# cost
o = [llm_res[k]["outcome"] for k in llm_res]
print("LLM runs", len(o), "status", Counter(x["status"] for x in o), "steps", sum(x["steps"] for x in o), "calls",
      sum(x.get("calls") or 0 for x in o), "tokens in", sum(x["input_tokens"] for x in o), "out",
      sum(x["output_tokens"] for x in o), "call s %.1f" % (sum(x["call_ms"] for x in o) / 1000),
      "commits", sorted({llm_res[k]["commit"] for k in llm_res}))
print("usage_limit files", sorted(p.name for p in (A / "llm" / "usage_limit").glob("*")))
