"""S1 audit: count numeric biology values (REGR, strain-rate profile, growth zone,
flank, velocity profile) in real-movie result dirs at a git revision.
Prints file and counts only, never values.

Usage: s1_bio_tip.py REV
"""
import re, subprocess, sys

rev = sys.argv[1]
REAL = re.compile(r"^results/[^/]*(real|full_batch|batch2|integrated|registration_fix|arange_fix|"
                  r"dispatcher_eval|rigid|closure|midline_fit|autotrace|tracker_timing)")
KEY = re.compile(r'"?([a-z_]*(regr|growth_zone|gz_len|flank|strain_rate_pct|peak_at_um|velocity_um_per_h|'
                 r'centre_peak|strain_rate_min)[a-z_]*)"?\s*[:=]\s*\[?\s*(-?\d)', re.I)
COL = re.compile(r"(regr|growth_zone|gz_|flank|strain_rate)", re.I)
files = subprocess.run(["git", "ls-tree", "-r", "--name-only", rev], capture_output=True, text=True).stdout.split("\n")
for f in files:
    if not REAL.search(f):
        continue
    data = subprocess.run(["git", "show", f"{rev}:{f}"], capture_output=True).stdout
    if b"\0" in data[:8000]:
        continue
    text = data.decode("utf-8", "replace")
    keys = {}
    for line in text.splitlines():
        for m in KEY.finditer(line):
            keys[m.group(1)] = keys.get(m.group(1), 0) + 1
    if f.endswith(".csv"):
        head = text.splitlines()[0] if text else ""
        cols = [c for c in head.split(",") if COL.search(c)]
        if cols:
            keys["csv columns: " + " ".join(cols)] = len(text.splitlines()) - 1
    if keys:
        print(f, "; ".join(f"{k} x{v}" for k, v in sorted(keys.items())))
