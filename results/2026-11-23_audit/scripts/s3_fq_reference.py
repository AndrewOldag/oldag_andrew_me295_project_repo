"""S3: recompute the provisional real frame_quality reference with and without windows now outside the
usable-window rule. Read-only; reads private and staging files given as arguments, prints aggregates only.
Usage: python s3_fq_reference.py PRIVATE_DIR LABELS_CSV
"""
import csv, statistics, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
priv, labels = Path(sys.argv[1]), Path(sys.argv[2])
man = {r["id"]: r for r in csv.DictReader(open(ROOT / "manifest/root_manifest.csv", newline=""))}
cand = {r["id"]: r for r in csv.DictReader(open(priv / "fq_real_candidates.csv", newline=""))}
lab = {r["id"]: r["label"] for r in csv.DictReader(open(labels, newline=""))}
vals = list(csv.DictReader(open(priv / "fq_real_values.csv", newline="")))
clean = [k for k, v in lab.items() if v == "clean" and cand.get(k, {}).get("status") == "active"]
def inrule(k):
    c = cand[k]; m = man[c["root"]]
    return m["include"] == "yes" and float(m["usable_from_h"]) <= float(c["start_h"]) and float(c["end_h"]) <= float(m["usable_to_h"])
out = [k for k in clean if not inrule(k)]
print(f"clean active windows: {len(clean)}; outside current rule: {len(out)} -> {[(k, cand[k]['root'], cand[k]['start_h'], cand[k]['end_h']) for k in out]}")
for name, keep in [("all clean", clean), ("in rule only", [k for k in clean if k not in out])]:
    v = [r for r in vals if r["id"] in keep]
    for q in ("texture_contrast", "focus"):
        x = [float(r[q]) for r in v]
        print(f"  {name}: n={len(x)} {q} median {statistics.median(x):.4f} lowest {min(x):.4f}")
