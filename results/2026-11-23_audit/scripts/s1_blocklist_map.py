"""S1 audit: map blocklist hits to blocklist line numbers. Prints no matched text.

Usage: s1_blocklist_map.py BLOCKLIST REV:PATH [REV:PATH ...]
Prints: REV:PATH line N -> blocklist line K
"""
import re, subprocess, sys

pats = []
for k, line in enumerate(open(sys.argv[1], encoding="utf-8").read().splitlines(), 1):
    if line.strip() and not line.startswith("#"):
        pats.append((k, re.compile(line.strip(), re.I)))
for spec in sys.argv[2:]:
    r = subprocess.run(["git", "show", spec], capture_output=True)
    if r.returncode:
        print(f"{spec}: absent")
        continue
    for n, l in enumerate(r.stdout.decode("utf-8", "replace").splitlines(), 1):
        ks = [k for k, p in pats if p.search(l)]
        if ks:
            print(f"{spec} line {n} -> blocklist lines {ks}")
