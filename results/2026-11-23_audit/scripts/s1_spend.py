"""S1 audit: sum the private cluster spend ledger (read only). Prints totals only.

Usage: s1_spend.py LEDGER_CSV
"""
import csv, sys, collections

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
f = lambda x: float(x) if x not in ("", None) else None
act = [f(r["actual_usd"]) for r in rows]
wc = [f(r["worst_case_usd"]) for r in rows]
rt = [f(r["running_total_usd"]) for r in rows]
print("rows", len(rows), "first", rows[0]["time"], "last", rows[-1]["time"])
print("rows with actual", sum(a is not None for a in act), "without", sum(a is None for a in act))
print("sum actual_usd %.3f" % sum(a for a in act if a is not None))
print("sum worst_case_usd (all rows) %.3f" % sum(w for w in wc if w is not None))
print("sum worst_case for rows without actual %.3f" % sum(w for a, w in zip(act, wc) if a is None and w is not None))
print("max running_total_usd %.3f ; last running_total %.3f" % (max(x for x in rt if x is not None), rt[-1]))
print("first row: running_total %.3f worst %.3f" % (rt[0], wc[0]))
dup = [k for k, v in collections.Counter(r["job_id"] for r in rows).items() if v > 1]
print("duplicate job ids", len(dup))
by = collections.defaultdict(lambda: [0, 0.0, 0.0])
for r, a, w in zip(rows, act, wc):
    k = (r["time"][:10], r["partition"], r["gres"])
    by[k][0] += 1; by[k][1] += a or 0; by[k][2] += w or 0
for k in sorted(by):
    print(k, "jobs %d actual %.3f worst %.3f" % tuple(by[k]))
over = [(r["time"], r["job_id"], x) for r, x in zip(rows, rt) if x is not None and x > 15]
print("rows with running_total > 15:", len(over))
gres = collections.Counter(r["gres"] for r in rows)
print("gres", dict(gres))
