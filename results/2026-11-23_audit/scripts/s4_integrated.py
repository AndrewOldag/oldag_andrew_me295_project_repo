"""S4 audit: recompute results/2026-11-18_integrated_run tables from windows.csv and tables.md (read-only)."""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path
R = Path(__file__).resolve().parents[3] / "results" / "2026-11-18_integrated_run"
rows = list(csv.DictReader(open(R / "windows.csv")))
print("windows", len(rows), "roots", len({r["root"] for r in rows}))
for m in ("integrated", "fixed_script"):
    print(m, dict(Counter(r[m] for r in rows)))
tree = Counter((r["remedy_tree"] or r["integrated"]) if r["remedy_tree"] else r["integrated"] for r in rows)
print("tree (+rule/pass as integrated)", dict(tree))
print("tree col only", dict(Counter(r["remedy_tree"] for r in rows if r["remedy_tree"])))
bc, be = defaultdict(Counter), defaultdict(Counter)
for r in rows:
    bc[r["condition"] or "-"][r["integrated"]] += 1
    be[r["window"][:4]][r["integrated"]] += 1
for k in sorted(bc): print("cond", k, dict(bc[k]), sum(bc[k].values()))
for k in sorted(be): print("exp", k, dict(be[k]), sum(be[k].values()))
fin = [r for r in rows if r["integrated"] not in ("paused",)]
print("diag remedies tried (all non-paused)", sum(int(r["remedies_tried"] or 0) for r in fin),
      "kept", sum(int(r["remedies_kept"] or 0) for r in fin))
print("diag calls sum", sum(int(r["diagnostician_calls"] or 0) for r in rows))
both = [r for r in rows if r["remedy_tree"] and r["remedy_tree"] != "paused"]
print("both final (tree col set, not paused)", len(both))
norm = lambda s: {"accepted": "accept", "accepted after repair": "accept", "declined by agent": "decline",
                  "declined by tree": "decline", "step_limit": "step_limit"}.get(s, s)
same = sum(norm(r["integrated"]) == norm(r["remedy_tree"]) for r in both)
print("same outcome", same)
dis = [r["window"] for r in both if norm(r["integrated"]) != norm(r["remedy_tree"])]
print("outcome disagreements", len(dis))
# table in tables.md
t = (R / "tables.md").read_text().splitlines()
trs = [l for l in t if l.startswith("| 07") and "__w" in l]
print("disagreement table rows", len(trs))
def kept(s):
    if s.strip() == "none": return "none"
    k = [p.strip().split()[0] for p in s.split(";") if "rolled back" not in p]
    return k[-1] if k else "none"
setdiff = 0; outdiff = []
for l in trs:
    c = [x.strip() for x in l.strip("|").split("|")]
    if kept(c[2]) != kept(c[4]): setdiff += 1
    if c[1] != c[3]: outdiff.append(c[0])
    w = next(r for r in rows if r["window"] == c[0])
    n = 0 if c[2] == "none" else len(c[2].split(";"))
    if n != int(w["remedies_tried"] or 0): print("  MISMATCH remedies", c[0], n, w["remedies_tried"])
    if norm(w["integrated"]) != c[1]: print("  MISMATCH outcome", c[0], c[1], w["integrated"])
    if norm(w["remedy_tree"]) != c[3]: print("  MISMATCH tree", c[0], c[3], w["remedy_tree"])
print("table rows with different kept settings", setdiff, "-> same settings", len(both) - setdiff)
print("table rows with different outcome", len(outdiff), "set==csv", set(outdiff) == set(dis))
print("tree accepts where diag not", sum(1 for r in both if norm(r["remedy_tree"]) == "accept" and norm(r["integrated"]) != "accept"),
      "diag step_limit & tree decline", sum(1 for r in both if r["integrated"] == "step_limit" and norm(r["remedy_tree"]) == "decline"))
# tree remedies from the table (only disagreement rows)
tr = [p for l in trs for p in [x.strip() for x in l.strip("|").split("|")][4].split(";") if p.strip() != "none"]
print("tree remedies visible in table rows", len(tr))
# worse rolled back for diag: initial vs ... not in csv
print("paused", [(r["window"], r["paused_needs"]) for r in rows if r["integrated"] == "paused"])
print("tree paused", [r["window"] for r in rows if r["remedy_tree"] == "paused"])
print("no batch", [r["window"] for r in rows if not r["batch"]])
print("first declined by rule", next(r["window"] for r in rows if r["integrated"] == "declined by rule"))
print("first step_limit", next(r["window"] for r in rows if r["integrated"] == "step_limit"))
print("auditor col nonempty", sum(1 for r in rows if r["auditor"]))
print("roots with paused windows", sorted({r["root"] for r in rows if r["integrated"] == "paused"}))
for w in ("0711_m1__w0-2", "0714_m7__w18-20", "0708_c10__w0-2", "0708_c10__w20-22", "0708_c4__w0-2"):
    print(w, next((dict(r) for r in rows if r["window"] == w), None))
print("accepted after repair", [r["window"] for r in rows if r["integrated"] == "accepted after repair"])
d = [r for r in rows if r["root"] == "0708_c4"]
print("0708_c4", [(r["window"], r["integrated"], r["initial_closure_px_per_h"]) for r in d])
# window list: the repo's dispatcher over the manifest, in memory (scripts/run_all.py window_list)
sys.path[:0] = [str(R.parents[1] / "scripts"), str(R.parents[1])]
import run_all  # noqa: E402
wl = [w.id() for w in run_all.window_list()]
print("run_all.window_list()", len(wl), "same order as windows.csv:", wl == [r["window"] for r in rows])
man = list(csv.DictReader(open(R.parents[1] / "manifest" / "root_manifest.csv")))
yes = {m["id"] for m in man if m["include"].strip().lower() == "yes"}
print("include-yes roots", len(yes), "roots in windows.csv", len({r["root"] for r in rows}), "equal", yes == {r["root"] for r in rows})
