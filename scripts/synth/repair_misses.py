"""Freeze v3 accept_repaired rods: per-run table of the diagnostician against the remedy tree, from the
committed traces only (spec 2026-10-24b, section D). No tracker run, no LLM call, writes nothing.

  python scripts/synth/repair_misses.py            # one line per run, then counts per group

Columns: method, rod, repeat, outcome, fault named at the end, steps, step of the first remedy, remedy rolled
back, actions in order. Groups: A = declined with no remedy tried; B = declined after a rolled-back remedy.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results" / "2026-10-23_freeze_v3"


def actions(trace):
    out = []
    for line in trace.read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if "step" not in e:
            continue
        a = e.get("action") or {}
        args = a.get("args") or {}
        out.append((e["step"], a.get("name"), args.get("kind") or args.get("remedy") or args.get("fault"),
                    bool((e.get("result") or {}).get("rolled_back"))))
    return out


def group(status, acts):
    if status == "accept":
        return "correct"
    remedies = [a for a in acts if a[1] == "apply_remedy"]
    if not remedies:
        return "A"
    return "B" if all(a[3] for a in remedies) else "other"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    labels = json.loads((RES / "labels.json").read_text())["labels"]
    rods = [r for r, v in labels.items() if v["class"] == "accept_repaired"]
    counts = Counter()
    for rod in rods:
        for method in ("remedy_tree", "diagnostician"):
            for f in sorted((RES / "runs").glob(f"{method}_{rod}*_summary.json")):
                s = json.loads(f.read_text())
                o = s["outcome"]
                acts = actions(RES / "runs" / s["trace"]) if method == "diagnostician" else []
                rem = [a for a in acts if a[1] == "apply_remedy"]
                g = group(o["status"], acts) if method == "diagnostician" else (
                    "correct" if o["status"] == "accept" else "miss")
                counts[(method, s["rod"]["fault"], g)] += 1
                rolled = any("rolled back" in r for r in s.get("remedies") or [])
                print(f"{method:13s} {rod.replace('v3_growth_zone_', ''):30s} r{s.get('repeat', '-')} "
                      f"{o['status']:8s} {(o.get('args') or {}).get('fault') or '-':22s} steps {o['steps']} "
                      f"remedy@{rem[0][0] if rem else '-'} rolled_back {'yes' if rolled else 'no '} {g:7s} "
                      + " ".join(f"{a[1]}:{a[2]}" for a in acts))
    print()
    for (m, fault, g), n in sorted(counts.items()):
        print(f"{m:13s} {fault:22s} {g:7s} {n}")


if __name__ == "__main__":
    main()
