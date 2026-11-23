"""S4 audit: independent recompute of a freeze-v3-style scored set (labels.json, scores.json, runs/*_summary.json,
metrics.json). Read-only. Usage: s4_scored.py <results folder>. Prints mismatches and recomputed tables."""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(sys.argv[1])
labels = json.loads((D / "labels.json").read_text())["labels"]
scores = json.loads((D / "scores.json").read_text())
metrics = json.loads((D / "metrics.json").read_text())
CL = ("accept_clean", "accept_repaired", "decline")
CORR = {"accept_clean": "good_report", "accept_repaired": "good_report", "decline": "correct_decline"}
CATS = ("good_report", "false_accept", "correct_decline", "unnecessary_decline", "not_reported", "accept_on_decline")
bad = []


def note(*a):
    bad.append(" ".join(map(str, a)))
    print("MISMATCH", *a)


# 1. summaries vs scores
summ = {}
for p in sorted((D / "runs").glob("*_summary.json")):
    s = json.loads(p.read_text())
    m = re.search(r"_r(\d)_summary\.json$", p.name)
    summ[(s["method"], s["rod"]["id"], int(m.group(1)) if m else 0)] = s
print("summaries", len(summ), "scores rows", len(scores), "labels", len(labels))
sk = {(r["method"], r["rod"], r["repeat"]): r for r in scores}
real = [k for k in sk if k[0] in ("script", "remedy_tree", "diagnostician", "single_agent")]
print("scored runs of real methods", len(real), "missing summary", [k for k in real if k not in summ][:5],
      "summary not scored", [k for k in summ if k not in sk][:5])
for k in real:
    r, s = sk[k], summ.get(k)
    if s is None:
        continue
    o = s["outcome"]
    if o["status"] != r["status"]:
        note("status", k, r["status"], o["status"])
    if o["steps"] != r["steps"]:
        note("steps", k, r["steps"], o["steps"])
    if o.get("input_tokens", 0) != r["tokens_in"] or o.get("output_tokens", 0) != r["tokens_out"]:
        note("tokens", k)
    if abs(round((o.get("call_ms") or 0) / 1000, 1) - r["call_s"]) > 0.051:
        note("call_s", k, r["call_s"], o.get("call_ms"))
    ea = s["error_after"].get("regr_rms_pct_per_h")
    if ea is not None and r["regr_rms"] is not None and abs(ea - r["regr_rms"]) > 1e-6:
        note("error_after", k)
    if len(s.get("remedies", [])) != len(r["remedies"]):
        note("remedies", k)

# 2. classes and categories
for r in scores:
    lab = labels.get(r["rod"])
    if lab is None:
        note("no label", r["rod"])
        continue
    if lab["class"] != r["cls"]:
        note("cls", r["method"], r["rod"], r["cls"], lab["class"])
    st, good = r["status"], r["good"]
    if st == "accept":
        cat = "false_accept" if not good else ("accept_on_decline" if r["cls"] == "decline" else "good_report")
    elif st == "decline":
        cat = "correct_decline" if r["cls"] == "decline" else "unnecessary_decline"
    else:
        cat = "not_reported"
    if cat != r["category"]:
        note("category", r["method"], r["rod"], r["repeat"], r["category"], cat)
    if good and r["regr_rms"] is not None and r["regr_tol"] is not None and r["regr_rms"] > r["regr_tol"]:
        note("good but error over tolerance", r["method"], r["rod"])
print("label classes", dict(Counter(v["class"] for v in labels.values())))
print("label classes of scored rods", dict(Counter(labels[x]["class"] for x in {r["rod"] for r in scores})))


# 3. metrics
def summ_rep(rs):
    by = defaultdict(list)
    for r in rs:
        by[r["cls"]].append(r)
    ok = lambda r: r["category"] == CORR[r["cls"]]  # noqa: E731
    acc = {c: (sum(map(ok, by[c])) / len(by[c]) if by[c] else None) for c in CL}
    pres = [a for a in acc.values() if a is not None]
    cats = Counter(r["category"] for r in rs)
    nacc = sum(r["status"] == "accept" for r in rs)
    ndec = sum(r["status"] == "decline" for r in rs)
    out = {"runs": len(rs), "balanced_accuracy": sum(pres) / len(pres), "overall_accuracy": sum(map(ok, rs)) / len(rs),
           "false_accepts": cats["false_accept"], "false_accept_rate": cats["false_accept"] / nacc if nacc else None,
           "coverage": nacc / len(rs), "abstention_precision": cats["correct_decline"] / ndec if ndec else None,
           "abstention_recall": cats["correct_decline"] / len(by["decline"]) if by["decline"] else None,
           "not_reported": cats["not_reported"],
           "kept_clean_runs": sum(r["remedies_kept"] > 0 for r in by["accept_clean"]),
           "udr_repaired": (sum(r["category"] == "unnecessary_decline" for r in by["accept_repaired"])
                            / len(by["accept_repaired"])) if by["accept_repaired"] else None,
           "fault_named": sum(bool(r["fault_correct"]) for r in rs if r["fault_correct"] is not None),
           "fault_rods": sum(r["fault_correct"] is not None for r in rs)}
    out.update({"acc_" + c: acc[c] for c in CL})
    out.update({"cat_" + k: cats[k] for k in CATS})
    return out


def fleiss(counts):
    n, N, k = sum(counts[0]), len(counts), len(counts[0])
    pbar = sum((sum(x * x for x in c) - n) / (n * (n - 1)) for c in counts) / N
    pj = [sum(c[j] for c in counts) / (N * n) for j in range(k)]
    pe = sum(p * p for p in pj)
    return (pbar - pe) / (1 - pe)


def f(t):
    if t is None:
        return "-"
    return f"{t[0]:.2f}" if abs(t[1] - t[2]) < 1e-12 else f"{t[0]:.2f} ({t[1]:.2f}-{t[2]:.2f})"


methods = list(dict.fromkeys(r["method"] for r in scores))
for m in methods:
    rs = [r for r in scores if r["method"] == m]
    reps = sorted({r["repeat"] for r in rs})
    per = [summ_rep([r for r in rs if r["repeat"] == k]) for k in reps]
    agg = {}
    for key in per[0]:
        v = [p[key] for p in per if p[key] is not None]
        agg[key] = (sum(v) / len(v), min(v), max(v)) if v else None
    tot = {k: sum(p[k] for p in per) for k in per[0]
           if k.startswith("cat_") or k in ("runs", "not_reported", "kept_clean_runs", "fault_named", "fault_rods")}
    print(f"\n[{m}] runs {tot['runs']} bal {f(agg['balanced_accuracy'])} clean {f(agg['acc_accept_clean'])} "
          f"rep {f(agg['acc_accept_repaired'])} dec {f(agg['acc_decline'])} overall {f(agg['overall_accuracy'])} "
          f"FA/rep {f(agg['false_accepts'])} FAR {f(agg['false_accept_rate'])} cov {f(agg['coverage'])} "
          f"aprec {f(agg['abstention_precision'])} arec {f(agg['abstention_recall'])} notrep {tot['not_reported']} "
          f"udr_rep {f(agg['udr_repaired'])}")
    print("   cats", {k[4:]: tot[k] for k in tot if k.startswith("cat_")}, "kept_clean_runs", tot["kept_clean_runs"],
          "fault named", tot["fault_named"], "of", tot["fault_rods"])
    mj = metrics[m]
    for key in ("balanced_accuracy", "overall_accuracy", "false_accepts", "coverage", "false_accept_rate"):
        a, b = agg[key], mj.get(key)
        if b is not None and a is not None and abs(a[0] - b["mean"]) > 1e-9:
            note("metrics.json", m, key, b["mean"], a[0])
    if len(reps) > 1:
        byrod = defaultdict(list)
        for r in rs:
            byrod[r["rod"]].append(r)
        full = {k: v for k, v in byrod.items() if len(v) == len(reps)}
        un = {k: len({r["category"] for r in v}) == 1 for k, v in full.items()}
        kap = fleiss([[sum(r["category"] == c for r in v) for c in CATS] for v in full.values()])
        pc = {c: (sum(un[k] for k in un if full[k][0]["cls"] == c), sum(full[k][0]["cls"] == c for k in un)) for c in CL}
        print("   agreement: unanimous", sum(un.values()), "of", len(full), "kappa %.3f" % kap, "per class", pc)
        mk = (mj.get("agreement") or {}).get("fleiss_kappa")
        if mk is not None and abs(mk - kap) > 1e-9:
            note("kappa", m, mk, kap)
    calls = sum(((summ.get((r["method"], r["rod"], r["repeat"])) or {}).get("outcome") or {}).get("calls") or 0
                for r in rs)
    print("   cost steps %d tokens in %d out %d call_s %.1f; summary outcome.calls %d" % (
        sum(r["steps"] for r in rs), sum(r["tokens_in"] for r in rs), sum(r["tokens_out"] for r in rs),
        sum(r["call_s"] for r in rs), calls))

# 4. per row
print("\nper row (kind, class): correct / runs")
rows = defaultdict(lambda: defaultdict(lambda: [0, 0, set()]))
for r in scores:
    c = rows[(r["kind"], r["cls"])][r["method"]]
    c[1] += 1
    c[0] += r["category"] == CORR[r["cls"]]
    c[2].add(r["seed"])
for k, v in rows.items():
    print("  ", k, sorted(next(iter(v.values()))[2]),
          {m: f"{a}/{b}" for m, (a, b, _) in v.items() if m in ("script", "remedy_tree", "diagnostician", "single_agent")})
det = [json.loads(x) for x in (D / "runs" / "deterministic.jsonl").read_text().splitlines() if x.strip()]
print("deterministic identical", sum(d["identical"] for d in det), "of", len(det))
for sub in ("usage_limit", "missing_state"):
    p = D / "runs" / sub
    if p.exists():
        print(sub, "summaries", len(list(p.glob("*_summary.json"))), "traces", len(list(p.glob("*trace*.jsonl"))),
              "by method", dict(Counter(x.name.split("_v3_")[0] for x in p.glob("*trace*.jsonl"))))
print("not_reported statuses", dict(Counter(r["status"] for r in scores if r["category"] == "not_reported")))
print("\nMISMATCHES", len(bad))
