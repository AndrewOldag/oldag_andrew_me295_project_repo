"""S3 usable-window check (audit c033). Read-only.

Collects (root, from_h, to_h) from tracked files (window ids `<root>__wA-B`, `<root> A-B h`,
csv from_h/to_h columns) and, if given, the private fq-real frame list, and tests each against
manifest/root_manifest.csv: include == yes and usable_from_h <= from_h, to_h <= usable_to_h.
Prints counts and out-of-rule items by root id and hours only.

Usage: python s3_windows_check.py [--private DIR]
"""
import argparse, csv, json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAT = re.compile(r"\b(07\d\d_[a-z]{1,3}\d+)(?:__w| )(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(?=\b| h|\.json)")


def manifest():
    m = {}
    with open(ROOT / "manifest" / "root_manifest.csv", newline="") as f:
        for r in csv.DictReader(f):
            m[r["id"]] = (r["include"].strip().lower(), float(r["usable_from_h"]), float(r["usable_to_h"]))
    return m


def verdict(m, root, a, b):
    if root not in m:
        return "not in manifest"
    inc, lo, hi = m[root]
    if inc != "yes":
        return f"include {inc}"
    if a < lo - 1e-6 or b > hi + 1e-6:
        return f"outside {lo:g}-{hi:g} h"
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", default=None)
    a = ap.parse_args()
    m = manifest()
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    hits = defaultdict(set)               # (root, a, b) -> files
    for fn in files:
        if not fn or fn.startswith("results/2026-11-23_audit/"):
            continue
        p = ROOT / fn
        for s in [fn]:
            for g in PAT.finditer(s):
                hits[(g[1], float(g[2]), float(g[3]))].add(fn)
        if p.suffix.lower() not in (".csv", ".md", ".json", ".jsonl", ".txt", ".yaml", ".yml", ".py", ".tsv"):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for g in PAT.finditer(txt):
            hits[(g[1], float(g[2]), float(g[3]))].add(fn)
        if p.suffix == ".csv":
            with open(p, newline="", encoding="utf-8", errors="ignore") as f:
                rd = csv.DictReader(f)
                if rd.fieldnames and {"root", "from_h", "to_h"} <= set(rd.fieldnames):
                    for r in rd:
                        try:
                            hits[(r["root"], float(r["from_h"]), float(r["to_h"]))].add(fn)
                        except ValueError:
                            pass
    bad = defaultdict(list)
    n_ok = 0
    for (root, x, y), fns in sorted(hits.items()):
        v = verdict(m, root, x, y)
        if v == "ok":
            n_ok += 1
        else:
            bad[v].append((root, x, y, sorted(fns)))
    print(f"tracked files scanned: {len([f for f in files if f])}; distinct (root, window) items: {len(hits)}; in rule: {n_ok}")
    for v, items in bad.items():
        print(f"\n== {v}: {len(items)}")
        for root, x, y, fns in items:
            print(f"  {root} {x:g}-{y:g} h  files={len(fns)}: {'; '.join(fns[:6])}{' ...' if len(fns) > 6 else ''}")
    if a.private:
        pr = Path(a.private)
        cand = {}
        with open(pr / "fq_real_candidates.csv", newline="") as f:
            for r in csv.DictReader(f):
                cand[r["id"]] = r
        frames = json.loads((pr / "fq_real_frames.json").read_text())
        print(f"\nfq-real: candidates {len(cand)}, frame sets {len(frames)}")
        for k, v in frames.items():
            c = cand.get(k)
            if not c:
                print(f"  {k}: no candidate row"); continue
            t = v.get("t_h", [])
            res = verdict(m, c["root"], min(t), max(t)) if t else "no times"
            print(f"  {k} {c['root']} {min(t):.2f}-{max(t):.2f} h status={c.get('status')} -> {res}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
