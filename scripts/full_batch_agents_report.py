"""Public tables for the agent run over real-calib's first batch (task c022, dispatcher inbox item 39).

  python scripts/full_batch_agents_report.py --run staging/c022/run3 --out results/2026-10-25_full_batch_1_agents

Reads summary.json of a scripts/real_slice.py run. Writes windows.csv (per window: experiment, condition, outcome,
fault named, remedies kept, closure pass or fail, auditor decision) and tables.md (outcome counts per experiment and
condition group; the auditor's condition comparison with every number masked). No check values, no REGR or
growth-zone values (Andrew, 2026-10-25: biology values out of course scope). The run folder (traces, summary.json)
stays out of git.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.dispatcher import manifest_rows  # noqa: E402
from audit.view import opaque_ids  # noqa: E402

GROUP = {"control": "control", "control then control": "control", "mannitol": "drought",
         "mannitol then mannitol": "drought", "mannitol then control": "recovery"}


def mask(text):
    """Every number in the auditor's text becomes 'x' (run labels r01... keep their digits)."""
    return re.sub(r"(?<![rR\w])[-+]?\d+(?:\.\d+)?", "x", text)


def remedy_name(text):
    """'frames registered on ... (from 1015 px from the tip) before tracking' -> 'frames registered on ...'."""
    return text.removeprefix("rolled back: ").split(" (")[0].strip()


def remedy_cells(remedies):
    tried = [remedy_name(r) for r in remedies if not r.startswith("rolled back: ")]
    rolled = [remedy_name(r) for r in remedies if r.startswith("rolled back: ")]
    return "; ".join(tried), "; ".join(rolled)


def auditor_public(report):
    """The auditor's report reduced to agent behaviour: flag categories with run ids, what the flagged runs share,
    its closing line. The per-condition block (REGR and growth-zone medians, direction of change) is withheld:
    biology results are out of course scope (Andrew, 2026-10-25). Every remaining number is masked."""
    out, block = [], None
    for line in report.split("\n"):
        low = line.lower()
        if low.startswith("cleared runs by condition"):
            block = "withheld"
            out.append("[per-condition summary of cleared runs withheld: REGR and growth-zone medians]")
            continue
        if low.startswith(("flagged", "what the flagged", "batch:")):
            block = None
        if not line.strip():
            block = None if block != "withheld" else block
            out.append("")
            continue
        if block == "withheld" and line.startswith("- "):
            continue
        if line.startswith("- ") and ":" in line:          # flag category and run ids; drop the profile description
            head, rest = line.split(":", 1)
            ids = rest.split(".")[0]
            out.append(mask(f"{head}:{ids}."))
            continue
        if block == "withheld":
            block = None
            last = [x.strip() for x in line.split(". ") if "not faults" in x]
            out.append(mask(last[0] if last else "[withheld]"))
            continue
        out.append(mask(line))
    return [l for i, l in enumerate(out) if l or (i and out[i - 1])]


def window_rows(summ):
    man = {r["id"]: r for r in manifest_rows()}
    decisions = (summ.get("auditor") or {}).get("decisions") or {}
    rid = dict(zip(summ["tasks"], opaque_ids(len(summ["tasks"]), "real_slice")))     # the auditor's run ids
    rows = []
    for tid, s in summ["tasks"].items():
        root = s["root_id"]
        closure = next((c for c in s["final_checks"] if c["check"] == "closure"), {})
        dec = decisions.get(rid[tid], {})
        rows.append({
            "window": f"{root} {s['window_h'][0]:g}-{s['window_h'][1]:g} h", "run_id": rid[tid],
            "experiment": man[root]["experiment"][:8], "experiment_type": man[root]["experiment_type"],
            "condition": s["condition"], "group": GROUP.get(s["condition"], s["condition"]),
            "outcome": s["outcome"]["status"],
            "fault": (s["outcome"].get("args") or {}).get("fault", ""),
            "remedies_tried": remedy_cells(s["remedies"])[0], "rolled_back": remedy_cells(s["remedies"])[1],
            "closure": {True: "pass", False: "fail"}.get(closure.get("passed"), "not computable"),
            "auditor": dec.get("decision", ""), "auditor_reason": dec.get("reason", ""),
        })
    return sorted(rows, key=lambda r: r["window"])


def counts(rows, key):
    out = defaultdict(Counter)
    for r in rows:
        out[r[key]][r["outcome"]] += 1
        if r["auditor"]:
            out[r[key]]["auditor " + r["auditor"]] += 1
    return out


def table(title, per):
    keys = sorted({k for c in per.values() for k in c})
    md = [f"## {title}", "", "| | windows | " + " | ".join(keys) + " |", "|" + " :-- |" * (len(keys) + 2)]
    for g in sorted(per):
        n = sum(v for k, v in per[g].items() if not k.startswith("auditor "))
        md.append(f"| {g} | {n} | " + " | ".join(str(per[g][k]) for k in keys) + " |")
    return md + [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    summ = json.loads((Path(a.run) / "summary.json").read_text())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = window_rows(summ)
    with open(out / "windows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    md = ["# Agent run over the first batch: counts", "",
          f"Windows collected: {len(rows)} of {len(summ['windows'])}; dispatcher end states "
          f"{(summ.get('dispatcher') or {}).get('states')}. Outcome counts only; no check, REGR or growth-zone values.",
          ""]
    md += table("By condition group", counts(rows, "group"))
    md += table("By experiment", counts(rows, "experiment"))
    md += table("By experiment type and condition", counts(
        [dict(r, et=f"{r['experiment_type']}: {r['condition']}") for r in rows], "et"))
    faults = Counter(r["fault"] for r in rows if r["outcome"] == "decline")
    md += ["## Faults named on declined windows", ""] + [f"- {k or 'none'}: {v}" for k, v in faults.most_common()] + [""]
    tried = Counter(x for r in rows for x in r["remedies_tried"].split("; ") if x)
    rolled = Counter(x for r in rows for x in r["rolled_back"].split("; ") if x)
    md += ["## Remedies (windows)", "", "| remedy | tried | rolled back |", "| :-- | :-- | :-- |"]
    md += [f"| {k} | {v} | {rolled[k]} |" for k, v in tried.most_common()] + [""]
    nc = [r for r in rows if r["closure"] == "not computable"]
    md += ["## Closure not computable", "",
           f"{len(nc)} windows: " + (", ".join(r["window"] for r in nc) or "none") + ". Outcomes: "
           + ", ".join(f"{k} {v}" for k, v in Counter(r["outcome"] for r in nc).items()) + "; auditor: "
           + ", ".join(f"{k or 'no decision'} {v}" for k, v in Counter(r["auditor"] for r in nc).items()), ""]
    aud = summ.get("auditor") or {}
    md += ["## Auditor report, agent behaviour only (numbers masked as x)", "",
           f"Auditor status: {aud.get('status')}; decisions on {len(aud.get('decisions') or {})} accepted runs.", ""]
    md += auditor_public(aud.get("report") or "") + [""]
    (out / "tables.md").write_text("\n".join(md))
    print(f"wrote {out / 'windows.csv'} and {out / 'tables.md'}: {len(rows)} windows")


if __name__ == "__main__":
    main()
