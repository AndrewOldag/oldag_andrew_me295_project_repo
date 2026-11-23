"""S4 audit: secondary numbers of freeze v4 (v3 alongside, decomposition, known limits a-d, compute counts) and of
c029 / c029b (runs without the missing-state runs, expected vs label, equivalence, flicker counts). Read-only."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "results"
V3, V4 = ROOT / "2026-10-23_freeze_v3", ROOT / "2026-10-25_freeze_v4"
HC = ROOT / "2026-11-18_heldout_compound"
CORR = {"accept_clean": "good_report", "accept_repaired": "good_report", "decline": "correct_decline"}
CL = ("accept_clean", "accept_repaired", "decline")


def js(p):
    return json.loads(Path(p).read_text())


def trace(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def recat(r, cls):
    st, good = r["status"], r["good"]
    if st == "accept":
        return "false_accept" if not good else ("accept_on_decline" if cls == "decline" else "good_report")
    if st == "decline":
        return "correct_decline" if cls == "decline" else "unnecessary_decline"
    return "not_reported"


def metr(rs, relabel=None, rows=None):
    """mean over repeats of balanced, overall, acc per class, false accepts."""
    out = defaultdict(list)
    for k in sorted({r["repeat"] for r in rs}):
        sub = [r for r in rs if r["repeat"] == k and (rows is None or rows(r))]
        by = defaultdict(list)
        for r in sub:
            c = relabel(r) if relabel else r["cls"]
            by[c].append(recat(r, c) == CORR[c])
        acc = {c: sum(v) / len(v) for c, v in by.items()}
        out["bal"].append(sum(acc.values()) / len(acc))
        out["overall"].append(sum(sum(v) for v in by.values()) / len(sub))
        for c in CL:
            if c in acc:
                out[c].append(acc[c])
        out["fa"].append(sum(recat(r, relabel(r) if relabel else r["cls"]) == "false_accept" for r in sub))
    return {k: round(sum(v) / len(v), 2) for k, v in out.items()}


print("=== freeze v4: v3 alongside and decomposition")
s3, s4 = js(V3 / "scores.json"), js(V4 / "scores.json")
slm = lambda r: "stage_log_missing" in r["rod"]  # noqa: E731
for m in ("script", "remedy_tree", "diagnostician", "single_agent", "all_decline"):
    a, b = [r for r in s3 if r["method"] == m], [r for r in s4 if r["method"] == m]
    print(m, "v3", metr(a), "| v3 C3a", metr(a, relabel=lambda r: "decline" if slm(r) else r["cls"]),
          "| v4", metr(b), "| v3 unchanged", metr(a, rows=lambda r: not slm(r)),
          "| v4 unchanged", metr(b, rows=lambda r: not slm(r)))
print("v3 labels", Counter(v["class"] for v in js(V3 / "labels.json")["labels"].values()))
for m in ("remedy_tree", "diagnostician", "script", "single_agent"):
    print("v3 stage_log_missing", m, Counter(r["status"] for r in s3 if r["method"] == m and slm(r)))

print("\n=== freeze v4: accepted runs keeping a remedy on clean rods")
for m in ("script", "remedy_tree", "diagnostician", "single_agent"):
    rs = [r for r in s4 if r["method"] == m and r["cls"] == "accept_clean" and r["remedies_kept"] > 0]
    print(m, "kept any status", len(rs), "accepted", sum(r["status"] == "accept" for r in rs))

print("\n=== freeze v4 known limit (a): second_root")
for m in ("diagnostician", "single_agent"):
    rs = [r for r in s4 if r["method"] == m and "second_root" in r["rod"]]
    wf = crop = 0
    for r in rs:
        t = trace(V4 / "runs" / f"{m}_{r['rod']}_r{r['repeat']}_trace.jsonl")
        rem = [((d.get("action") or {}).get("args") or {}) for d in t
               if (d.get("action") or {}).get("name") == "apply_remedy" and d.get("status") == "executed"]
        wf += any(a.get("remedy") == "use_width_free_ratio" for a in rem)
        crop += any(a.get("setting") == "crop_to_main_root" for a in rem)
    print(m, Counter(r["category"] for r in rs), "width_free in", wf, "of", len(rs), "crop_to_main_root runs", crop)

print("\n=== freeze v4 known limit (b): single agent")
first_cr = n = rem_n = 0
after = Counter()
SA = sorted((V4 / "runs").glob("single_agent_*_trace.jsonl"))
# the cut-off run s27 r2: the scored rerun trace has a _trace_<time> name (README run record)
SA = [p if "stage_log_missing_z1_s27_r2" not in p.name else next((V4 / "runs").glob(p.name.replace(".jsonl", "_*.jsonl")))
      for p in SA]
for p in SA:
    t = [d for d in trace(p) if "step" in d]
    n += 1
    first_cr += bool(t) and ((t[0].get("action") or {}).get("args") or {}).get("kind") == "check_report"
    acts = [(d.get("action") or {}) for d in t if d.get("status") == "executed"]
    for i, a in enumerate(acts):
        if a.get("name") == "apply_remedy":
            rem_n += 1
            k = 0
            for b in acts[i + 1:]:
                if b.get("name") != "request_info":
                    break
                k += 1
            after[k] += 1
print("single agent trace files", n, "step 1 check_report", first_cr, "executed remedies", rem_n,
      "info calls right after a remedy", dict(sorted(after.items())))

print("\n=== freeze v4 known limit (c): single agent bad_stage_correction")
for r in [r for r in s4 if r["method"] == "single_agent" and "bad_stage" in r["rod"]]:
    t = trace(V4 / "runs" / f"single_agent_{r['rod']}_r{r['repeat']}_trace.jsonl")
    rem = [((d.get("action") or {}).get("args") or {}).get("remedy") for d in t
           if (d.get("action") or {}).get("name") == "apply_remedy" and d.get("status") == "executed"]
    print(r["rod"][-3:], r["repeat"], r["status"], r["category"], rem)

print("\n=== freeze v4 compute: tracker_runs_new over summaries")
tr = Counter()
for p in (V4 / "runs").glob("*_summary.json"):
    s = js(p)
    tr[s["method"]] += s.get("tracker_runs_new") or 0
print(dict(tr), "sum", sum(tr.values()))

print("\n=== c029: metrics without the 3 missing-state runs")
sc = js(HC / "scores.json")
drop = {("diagnostician", "v3_growth_zone_drift_jitter_s40", 1), ("single_agent", "v3_growth_zone_low_texture_fast_s42", 1),
        ("single_agent", "v3_growth_zone_low_texture_fast_s43", 0)}
for m in ("diagnostician", "single_agent"):
    rs = [r for r in sc if r["method"] == m and (m, r["rod"], r["repeat"]) not in drop]
    per = defaultdict(list)
    for k in (0, 1, 2):
        sub = [r for r in rs if r["repeat"] == k]
        by = defaultdict(list)
        for r in sub:
            by[r["cls"]].append(r["category"] == CORR[r["cls"]])
        acc = {c: sum(v) / len(v) for c, v in by.items()}
        per["bal"].append(sum(acc.values()) / len(acc))
        per["rep"].append(acc["accept_repaired"])
        per["dec"].append(acc["decline"])
        per["overall"].append(sum(sum(v) for v in by.values()) / len(sub))
        per["fa"].append(sum(r["category"] == "false_accept" for r in sub))
    f = lambda v: f"{sum(v)/len(v):.2f} ({min(v):.2f}-{max(v):.2f})"  # noqa: E731
    print(m, "runs", len(rs), {k: f(v) for k, v in per.items()}, "not reported",
          sum(r["category"] == "not_reported" for r in rs))
for k in sorted(drop):
    r = next(x for x in sc if (x["method"], x["rod"], x["repeat"]) == k)
    t = trace(HC / "runs" / f"{k[0]}_{k[1]}_r{k[2]}_trace.jsonl")
    miss = sum("Missing" in json.dumps(d.get("result", "")) or "Missing" in json.dumps(d.get("error", "")) for d in t)
    print("dropped", k, r["status"], r["category"], "trace lines mentioning Missing", miss)
allmiss = []
for p in sorted((HC / "runs").glob("*_trace.jsonl")):
    if any("Missing" in json.dumps({k: v for k, v in d.items() if k in ("result", "error")}) for d in trace(p)):
        allmiss.append(p.name)
print("c029 traces with a Missing tool result:", allmiss)

print("\n=== c029 and c029b: expected vs label")
lab = js(HC / "labels.json")["labels"]
print("c029 differ", sum(v["class"] != v["expected"] for v in lab.values()),
      Counter((v["kind"], v["expected"], v["class"]) for v in lab.values() if v["class"] != v["expected"]))
sl = js(HC / "supplement" / "labels.json")["labels"]
sel = js(HC / "supplement" / "selected.json")["selected"]
print("c029b selected", len(sel), "differ", sum(sl[x]["class"] != sl[x]["expected"] for x in sel),
      Counter((sl[x]["kind"], sl[x]["expected"], sl[x]["class"]) for x in sel if sl[x]["class"] != sl[x]["expected"]))
# selection rule: first 4 accept_clean, 10 accept_repaired, 6 decline in seed order
order = sorted(sl, key=lambda x: (sl[x]["seed"], list(sl).index(x)))
pick, need = [], {"accept_clean": 4, "accept_repaired": 10, "decline": 6}
for x in order:
    if need[sl[x]["class"]] > 0:
        need[sl[x]["class"]] -= 1
        pick.append(x)
print("selection rule reproduces selected.json:", sorted(pick) == sorted(sel))
for name, L in (("c029", js(HC / "labels.json")), ("c029b", js(HC / "supplement" / "labels.json"))):
    print(name, "labels.json top keys", [k for k in L if k != "labels"],
          {k: L[k] for k in L if k != "labels" and not isinstance(L[k], (dict, list))})
    print("  states per rod", Counter(v.get("states") for v in L["labels"].values()),
          "sum", sum(v.get("states") or 0 for v in L["labels"].values()))
ce = js(HC / "cluster_equivalence.json")
print("cluster_equivalence", json.dumps(ce)[:600])

print("\n=== c029 flicker: unremedied checks (script runs)")
for p in sorted((HC / "runs").glob("script_*illumination_flicker*_summary.json")):
    s = js(p)
    print(p.name[:60], {c["check"]: c["passed"] for c in s["initial_checks"]})

print("\n=== freeze v4 known limit (d): diagnostician remedies applied with no failing check")
nd = []
for p in sorted((V4 / "runs").glob("diagnostician_*_summary.json")):
    s = js(p)
    fail = {c["check"] for c in s["initial_checks"] if c["passed"] is False}
    hit = []
    for d in trace(str(p).replace("_summary.json", "_trace.jsonl")):
        a = d.get("action") or {}
        if a.get("name") == "apply_remedy" and d.get("status") == "executed":
            r = d.get("result") or {}
            if not fail:
                hit.append((a["args"].get("remedy"), a["args"].get("setting"), bool(r.get("rolled_back"))))
            if not r.get("rolled_back"):
                fail = set(r.get("failed_checks") or [])
    if hit:
        nd.append((p.name.replace("_summary.json", ""), s["outcome"]["status"], hit))
print(len(nd), "runs;", "rolled back", sum(h[2] for x in nd for h in x[2]))
for x in nd:
    print(" ", x)
