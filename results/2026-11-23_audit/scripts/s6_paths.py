"""S6: list backticked path-like tokens in lab reports and README; check existence on this tree."""
import re, sys, os, glob
FILES = ["docs/reports/2026-10-16_lab-report-1.md", "docs/reports/2026-10-30_lab-report-2.md",
         "docs/reports/2026-11-01_lab-report-2.md", "docs/reports/2026-11-15_lab-report-3.md", "README.md"]
PAT = re.compile(r"`([^`]+)`")
SKIP_PREFIX = ("private/", "staging/", "<", "OPS_DIR")
for f in FILES:
    for n, line in enumerate(open(f, encoding="utf-8"), 1):
        for tok in PAT.findall(line):
            for part in tok.split():
                p = part.strip(",;:()")
                if "/" not in p or p.startswith(("http", "-")) or "<" in p or "|" in p:
                    continue
                if not re.match(r"^[\w.\-/*]+$", p):
                    continue
                if p.startswith(SKIP_PREFIX) or "DIR" in p or p.startswith("results/<"):
                    continue
                ok = bool(glob.glob(p)) or os.path.exists(p)
                if not ok:
                    print(f"MISSING {f}:{n} {p}")
