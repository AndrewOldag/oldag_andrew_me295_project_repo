"""Merge section CSVs into findings.csv. Applies the severity alignment stated in README.md."""
import csv, sys
from collections import Counter
OVERRIDE = {"S3-5": "blocker"}
rows = []
for n, name in enumerate(["s1_rules", "s2_equations", "s3_freezes", "s4_results",
                          "s5_decisions", "s6_reports", "s7_repro"], 1):
    for r in csv.DictReader(open(f"{name}.csv", encoding="utf-8")):
        r["severity"] = OVERRIDE.get(r["id"], r["severity"].strip().lower())
        rows.append(r)
cols = ["id", "section", "severity", "where", "what", "evidence", "fix"]
with open("findings.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)
c = Counter((r["id"].split("-")[0], r["severity"]) for r in rows)
for s in sorted({k[0] for k in c}):
    print(s, {sev: c[(s, sev)] for sev in ("blocker", "major", "minor")})
print("total", Counter(r["severity"] for r in rows))
