"""Held-out supplement c029b: milder compound and novel faults (inbox compound item 10; proposal
docs/proposals/2026-11-22_heldout-supplement.md). The c029 driver (heldout_compound.py) pointed at this set:
48 candidate rods, labels as c029, then 20 selected rods for the methods. c029's files are not touched.

  python scripts/synth/heldout_supplement.py render                     # 48 candidates and moved copies, VM
  python scripts/synth/compound_queue.py --set c029b jobs|submit|fetch  # label runs on the cluster
  python scripts/synth/heldout_supplement.py labels                     # labels.md; labels.json, selected.json when complete
  python scripts/synth/heldout_supplement.py rules
  python scripts/synth/heldout_supplement.py agents --method M --repeat K [--max-runs N]
  python scripts/synth/heldout_supplement.py eval

Renders in staging/rods_c029b, tracks in staging/tracks_c029b (git-ignored). No tracker run on the VM.
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import heldout_compound as hc  # noqa: E402
from measure.render_compound import MILD, NOVEL  # noqa: E402
from measure.runner import Rod  # noqa: E402

OUT = hc.OUT / "supplement"
SEEDS = tuple(range(60, 68))                  # not used before (proposal, section 3)
NOVEL_SIZES = {"focus_drift": "1.5", "illumination_flicker": "0.03"}
KINDS = list(MILD) + list(NOVEL)              # candidate order: seed, then kind (proposal, section 3)
QUOTA = {"accept_repaired": 10, "accept_clean": 4, "decline": 6}
MAX_LLM_RUNS = 150                            # inbox item 10 (4)
EXPECTED = {f: "accept_repaired" for f in MILD} | {f: "accept_clean" for f in NOVEL}
NAMES = {f"{f}_mild": hc.NAMES[f] for f in hc.COMPOUND} | {f: hc.NAMES[f] for f in NOVEL}


def candidates():
    return [Rod(hc.GZ, f, s, size=NOVEL_SIZES.get(f)) for s in SEEDS for f in KINDS]


def select(labels):
    """Proposal, section 5: in candidate order, the first QUOTA[c] rods of each class."""
    keep, short = [], {}
    for c, n in QUOTA.items():
        ids = [r.id() for r in candidates() if labels[r.id()]["class"] == c]
        keep += ids[:n]
        if len(ids) < n:
            short[c] = n - len(ids)
    order = [r.id() for r in candidates()]
    return sorted(keep, key=order.index), short


def selected():
    f = OUT / "selected.json"
    return json.loads(f.read_text())["selected"] if f.exists() else None


def scored_rods():
    """The 20 selected rods once selected.json exists, else the 48 candidates."""
    sel = selected()
    return candidates() if sel is None else [r for r in candidates() if r.id() in sel]


def use():
    """Point heldout_compound (and through it the v3 driver) at this set."""
    hc.OUT, hc.CACHE, hc.RODS = OUT, ROOT / "staging" / "tracks_c029b", ROOT / "staging" / "rods_c029b"
    hc.PAUSED = ROOT / "staging" / "c029b_queue" / "paused.jsonl"
    hc.SCORING_SEEDS, hc.MAX_LLM_RUNS, hc.EXPECTED, hc.NAMES = SEEDS, MAX_LLM_RUNS, EXPECTED, NAMES
    hc.COMPOUND = MILD                       # rows of the per-row table: the mild kinds, then the novel ones
    hc.scored_rods = scored_rods


MISSING = OUT / "runs" / "missing_state"   # inbox item 12: kept, not scored, redone from step 0 once cached


def missing_in(trace):
    """(rod id, settings tag) of the first "Missing" tool error in an agent trace, else None."""
    m = re.search(r"Missing: (\S+) (\S+?)\"", trace.read_text(encoding="utf-8")) if trace.exists() else None
    return (m.group(1), m.group(2).rstrip("\\")) if m else None


def state_cached(rid, tag):
    return all(Path(f"{hc.CACHE / f'{r}__{tag}.npz'}.ok").exists() for r in (rid, f"{rid}_moved"))


def set_aside_missing_state_runs():
    """LLM runs whose remedy needed a state not cached (the agent got a Missing tool error) move to
    runs/missing_state/ with a line in pending.jsonl (inbox item 12)."""
    n, runs = 0, OUT / "runs"
    for f in runs.glob("*_summary.json"):
        s = json.loads(f.read_text())
        if s["method"] not in hc.v3.LLM or not (miss := missing_in(runs / s["trace"])):
            continue
        MISSING.mkdir(parents=True, exist_ok=True)
        for g in (f, runs / s["trace"]):
            dest = MISSING / g.name
            if dest.exists():
                dest = MISSING / f"{g.stem}_{time.strftime('%H%M%S')}{g.suffix}"
            g.rename(dest)
        with (MISSING / "pending.jsonl").open("a") as h:
            h.write(json.dumps({"run": f.name[:-len("_summary.json")], "rod": miss[0], "tag": miss[1],
                                "time": time.strftime("%F %T")}) + "\n")
        n += 1
    return n


def waiting_on_state(method, repeat):
    """Rod ids whose set-aside run of this method and repeat still waits for its state."""
    f = MISSING / "pending.jsonl"
    rows = [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []
    return {r["rod"] for r in rows if r["run"].startswith(method + "_") and r["run"].endswith(f"_r{repeat}")
            and not state_cached(r["rod"], r["tag"])}


def committed(f):
    return f.exists() and not hc.v3.git("status", "--porcelain", "--", str(f)) and bool(hc.v3.git("ls-files", "--", str(f)))


def main():
    use()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "labels":
        hc.scored_rods = candidates
        hc.point_v3_here()
        OUT.mkdir(parents=True, exist_ok=True)
        text, info = hc.labels_report()
        text = text.replace("# Labels of the held-out compound and novel set",
                            "# Labels of the held-out supplement c029b (48 candidates)", 1)
        if info["complete"]:
            keep, short = select(info["labels"])
            sel = {"selected": keep, "quota": QUOTA, "shortfall": short, "counts_all_48": info["counts"],
                   "counts_selected": {c: sum(info["labels"][r]["class"] == c for r in keep) for c in QUOTA}}
            text = text.replace("## Per state", "## Selection (proposal, section 5)\n\n"
                                f"- Selected {len(keep)} rods: {sel['counts_selected']}\n"
                                f"- Shortfall: {short or 'none'}\n"
                                f"- All-decline would score {sel['counts_selected']['decline']} of {len(keep)} "
                                "on the selected set\n\n" + "\n".join(f"- {r}" for r in keep) + "\n\n## Per state", 1)
            (OUT / "labels.json").write_text(json.dumps(info, indent=1, default=str))
            (OUT / "selected.json").write_text(json.dumps(sel, indent=1))
        (OUT / "labels.md").write_text(text)
        print(text.split("## Per state")[0])
        return
    if cmd in ("rules", "agents") and not committed(OUT / "selected.json"):
        sys.exit("selected.json not committed: no method runs before (proposal, section 5)")
    if cmd == "render" and selected() is not None:
        sys.exit("selection made; renders are of the 48 candidates only")
    if cmd == "agents":
        n = set_aside_missing_state_runs()
        a = sys.argv
        m, k = a[a.index("--method") + 1], int(a[a.index("--repeat") + 1])
        wait = waiting_on_state(m, k)
        if wait:
            print(f"{m} repeat {k}: {len(wait)} rods wait for a state not cached, skipped: {sorted(wait)}", flush=True)
            hc.scored_rods = lambda: [r for r in scored_rods() if r.id() not in wait]
        try:
            hc.main()
        finally:
            n += set_aside_missing_state_runs()
            print(f"missing-state runs set aside this call: {n}", flush=True)
        return
    hc.main()


if __name__ == "__main__":
    main()
