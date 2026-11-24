"""S3: usable-window check over older trees (files since removed). Read-only.
For each commit given, git grep window ids `<root>__wA-B` / `<root> A-B h` and test against the current manifest.
Usage: python s3_windows_history.py COMMIT [COMMIT ...]
"""
import csv, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
PAT = re.compile(r"\b(07\d\d_[a-z]{1,3}\d+)(?:__w| )(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(?=\b| h|\.json)")
man = {r["id"]: (r["include"], float(r["usable_from_h"]), float(r["usable_to_h"]))
       for r in csv.DictReader(open(ROOT / "manifest/root_manifest.csv", newline=""))}
for c in sys.argv[1:]:
    out = subprocess.run(["git", "grep", "-I", "-o", "-E", r"07[0-9]{2}_[a-z]{1,3}[0-9]+(__w| )[0-9.]+-[0-9.]+", c],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
    seen, bad = set(), {}
    for line in out.splitlines():
        parts = line.split(":", 2)
        if len(parts) < 3 or parts[1].startswith("results/2026-11-23_audit/"):
            continue
        for g in PAT.finditer(parts[2] + " "):
            k = (g[1], float(g[2]), float(g[3])); seen.add(k)
            inc, lo, hi = man.get(g[1], ("missing", 0, 0))
            if inc != "yes" or k[1] < lo - 1e-6 or k[2] > hi + 1e-6:
                bad.setdefault(k, set()).add(parts[1])
    print(f"{c}: {len(seen)} items, {len(bad)} out of rule")
    for k, f in sorted(bad.items()):
        print(f"  {k[0]} {k[1]:g}-{k[2]:g} h ({man.get(k[0], ('missing',))[0]}): {'; '.join(sorted(f)[:4])}")
