"""Agreement of repeated agent runs on the 16-root real subset (dispatcher inbox item 36 (2)), as in freeze v3:
per window, do all runs give the same outcome; unanimity rate and Fleiss' kappa (measure/metrics.py).

  python scripts/real_subset_agreement.py results/2026-10-25_real_subset results/2026-10-25_real_subset/run2 ...

Outcome per window: accept (as measured), accept_repaired (a remedy kept), decline. The auditor's decision per
accepted window (clear or flag) is compared the same way. Writes agreement.json and agreement.md into the first
run folder and prints the tables.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audit.view import opaque_ids  # noqa: E402
from measure.metrics import fleiss_kappa  # noqa: E402

OUTCOMES = ("accept", "accept_repaired", "decline")
AUDIT = ("clear", "flag", "declined")


def outcomes(run):
    s = json.loads((Path(run) / "summary.json").read_text())
    rid = dict(zip(s["tasks"], opaque_ids(len(s["tasks"]), "real_slice")))
    dec = (s.get("auditor") or {}).get("decisions") or {}
    out = {}
    for tid, t in s["tasks"].items():
        wid = f"{t.get('root_id') or tid.split('__')[0]}__w{t['window_h'][0]:g}-{t['window_h'][1]:g}"
        st = t["outcome"]["status"]
        kept = [x for x in t["remedies"] if not x.startswith("rolled back")]
        o = "decline" if st == "decline" else ("accept_repaired" if kept else "accept")
        a = "declined" if o == "decline" else (dec.get(rid[tid]) or {}).get("decision", "clear")
        out[wid] = {"outcome": o, "auditor": a, "fault": (t["outcome"].get("args") or {}).get("fault", "")}
    return out


def agree(per_run, key, cats):
    wins = sorted(set.intersection(*(set(r) for r in per_run)))
    votes = {w: [r[w][key] for r in per_run] for w in wins}
    unan = [w for w, v in votes.items() if len(set(v)) == 1]
    k = fleiss_kappa([[v.count(c) for c in cats] for v in votes.values()])
    return {"windows": len(wins), "unanimous": len(unan), "unanimity_rate": round(len(unan) / len(wins), 3),
            "fleiss_kappa": None if k is None else round(k, 3),
            "split": {w: dict(Counter(v)) for w, v in votes.items() if len(set(v)) > 1}}


def main():
    runs = sys.argv[1:]
    per_run = [outcomes(r) for r in runs]
    res = {"runs": runs, "outcome": agree(per_run, "outcome", OUTCOMES), "auditor": agree(per_run, "auditor", AUDIT),
           "counts": [dict(Counter(v["outcome"] for v in r.values())) for r in per_run]}
    declined = set.intersection(*({w for w, v in r.items() if v["outcome"] == "decline"} for r in per_run))
    if declined:                               # fault named, on the windows every run declined
        faults = sorted({r[w]["fault"] for r in per_run for w in declined})
        res["fault"] = agree([{w: r[w] for w in declined} for r in per_run], "fault", faults)
    md = [f"Runs: {len(runs)}", "", "| Decision | Windows | Unanimous | Unanimity rate | Fleiss kappa |",
          "| :-- | :-- | :-- | :-- | :-- |"]
    for k in [k for k in ("outcome", "auditor", "fault") if k in res]:
        g = res[k]
        md.append(f"| {k} | {g['windows']} | {g['unanimous']} | {g['unanimity_rate']} | {g['fleiss_kappa']} |")
    md += ["", "| Run | " + " | ".join(OUTCOMES) + " |", "| :-- | " + " | ".join(":--" for _ in OUTCOMES) + " |"]
    for r, c in zip(runs, res["counts"]):
        md.append(f"| {Path(r).name} | " + " | ".join(str(c.get(o, 0)) for o in OUTCOMES) + " |")
    md += ["", "Windows without a unanimous outcome:"]
    md += [f"- {w}: {v}" for w, v in res["outcome"]["split"].items()] or ["- none"]
    if "fault" in res:
        md += ["", "Declined windows without a unanimous fault:"]
        md += [f"- {w}: {v}" for w, v in res["fault"]["split"].items()] or ["- none"]
    md += ["", "Windows without a unanimous auditor decision:"]
    md += [f"- {w}: {v}" for w, v in res["auditor"]["split"].items()] or ["- none"]
    (Path(runs[0]) / "agreement.json").write_text(json.dumps(res, indent=1))
    (Path(runs[0]) / "agreement.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
