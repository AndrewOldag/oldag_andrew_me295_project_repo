"""Real reference set for the particle-path zone check, report-only (spec 2026-11-23_zone-check-real-reference, task c035;
docs/proposals/2026-11-23_zone-reference.md).

synthetic   c034 freeze v4 set (18 clean, 90 shifted, 9 repaired) with the residual split into common mode and shape.
            Synthetic shape threshold by the R4 rule on the clean tracks (this test only). Writes synthetic.csv, synthetic.md
sample      24 accepted c027 windows by the proposal's rule (seed 20261123). Writes sample.csv

  python scripts/zone_reference.py synthetic --cache <freeze v4 track cache>
  python scripts/zone_reference.py sample --cache <c027 track cache>
"""
import argparse
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from checker.zone_checks import particle_path, shifted_fields  # noqa: E402
from integrity_thresholds import LABELS, round_up_2sf, track_set  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from zone_checks import SHIFTS, WINDOWS, track_file  # noqa: E402

OUT = ROOT / "results" / "2026-11-23_zone_reference"
MANIFEST = ROOT / "manifest" / "root_manifest.csv"
SEED = 20261123
STRATA = {"control": 5, "control then control": 4, "mannitol": 5, "mannitol then control": 5,
          "mannitol then mannitol": 5}
KEYS = ("pp_rms_px", "pp_common_px", "pp_shape_rms_px", "pp_rms_rel", "pp_common_rel", "pp_shape_rel")


def pp_values(rec, fields=None):
    return particle_path(rec, fields=fields).values


def _fmt(x):
    return "" if x is None else (f"{x:.6g}" if isinstance(x, float) else x)


def _write_csv(path, rows, cols):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: _fmt(r.get(k)) for k in cols})


def r4(v):
    return float(round_up_2sf(1.5 * np.percentile(np.asarray(v, float), 99.5)))


def synthetic(a):
    cache = Path(a.cache)
    labels = json.loads(LABELS.read_text())["labels"]
    rows = []
    for rod, path in track_set(cache):
        lab = labels[rod]
        rec = from_tracker_npz(path)
        base = {"rod": rod, "kind": lab["kind"], "seed": lab["seed"], "track": path.name}
        rows.append(base | {"class": lab["class"], "shift_px": 0} | pp_values(rec))
        if lab["class"] == "accept_clean" and lab["kind"] != "v3_still":
            for d in SHIFTS:
                rows.append(base | {"class": "shifted", "shift_px": d} | pp_values(rec, shifted_fields(rec, d)))
    OUT.mkdir(parents=True, exist_ok=True)
    _write_csv(OUT / "synthetic.csv", rows, ["rod", "class", "kind", "seed", "shift_px", "track", *KEYS])
    clean = [r for r in rows if r["class"] == "accept_clean"]
    th = r4([r["pp_shape_rel"] for r in clean if r["pp_shape_rel"] is not None])

    def line(name, d, sub):
        comp = [r for r in sub if r["pp_shape_rel"] is not None]
        flagged = sum(r["pp_shape_rel"] > th for r in comp)
        share = [r["pp_common_px"] ** 2 / r["pp_rms_px"] ** 2 for r in sub if r["pp_rms_px"]]
        sh = [r["pp_shape_rel"] for r in comp]
        rng = f"{min(sh):.3g}-{max(sh):.3g}" if sh else "-"
        med = f"{np.median(share):.2f}" if share else "-"
        return f"| {name} | {d} | {len(sub)} | {flagged} of {len(comp)} | {rng} | {med} |", flagged, len(comp)

    lines = ["# Synthetic re-run with the residual split (freeze v4, seeds 26-28)", "",
             f"Synthetic shape threshold (R4 rule on the 18 clean tracks, this test only): `pp_shape_rel` {th:g}", "",
             "| Set | Shift px | Records | shape flags | `pp_shape_rel` range | common share of squared residual (median) |",
             "| :-- | --: | --: | --: | :-- | --: |"]
    lines.append(line("accept_clean (threshold set)", 0, clean)[0])
    caught = {}
    for d in SHIFTS:
        ln, f, n = line("shifted", f"{d:+d}", [r for r in rows if r["class"] == "shifted" and r["shift_px"] == d])
        lines.append(ln)
        caught[d] = (f, n)
    lines.append(line("accept_repaired (not in the threshold set)", 0,
                      [r for r in rows if r["class"] == "accept_repaired"])[0])
    ok = all(f == n == 15 for f, n in caught.values())
    lines += ["", f"Stop rule (proposal): shape flags 15 of 15 at every shift: {'met' if ok else 'NOT met'}", ""]
    (OUT / "synthetic.md").write_text("\n".join(lines))
    print(json.dumps({"pp_shape_rel_threshold": th, "caught": {str(k): v for k, v in caught.items()},
                      "stop_rule_met": ok}))


def _hours(window):
    a, b = window.rsplit("__w", 1)[1].split("-")
    return float(a), float(b)


def sample(a):
    cache = Path(a.cache)
    man = {r["id"]: r for r in csv.DictReader(open(MANIFEST))}
    pool = collections.defaultdict(list)
    for r in csv.DictReader(open(WINDOWS)):
        if r["integrated"] != "accepted" or r["condition"] not in STRATA:
            continue
        m = man.get(r["root"])
        h0, h1 = _hours(r["window"])
        if m is None or m["include"] != "yes" or h0 < float(m["usable_from_h"]) or h1 > float(m["usable_to_h"]):
            continue
        p = track_file(cache, r["window"], "st1")
        if p is None:
            continue
        v = pp_values(from_tracker_npz(p, root_id=r["window"]))
        if v["pp_shape_rel"] is None or v["pp_common_rel"] is None:
            continue
        pool[r["condition"]].append(r)
    rng = np.random.default_rng(SEED)
    rows = []
    for cond in sorted(STRATA):
        cands = sorted(pool[cond], key=lambda r: r["window"])
        roots, n = set(), 0
        for i in rng.permutation(len(cands)):
            r = cands[i]
            if r["root"] in roots:
                continue
            roots.add(r["root"])
            n += 1
            rows.append({"window": r["window"], "root": r["root"], "condition": cond, "order": n,
                         "pool": len(cands)})
            if n == STRATA[cond]:
                break
    OUT.mkdir(parents=True, exist_ok=True)
    _write_csv(OUT / "sample.csv", rows, ["window", "root", "condition", "order", "pool"])
    print(json.dumps({c: len(pool[c]) for c in sorted(STRATA)} | {"sampled": len(rows)}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("synthetic"); s.add_argument("--cache", required=True)
    s = sub.add_parser("sample"); s.add_argument("--cache", required=True)
    a = ap.parse_args()
    {"synthetic": synthetic, "sample": sample}[a.cmd](a)


if __name__ == "__main__":
    main()
