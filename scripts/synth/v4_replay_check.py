"""Freeze v4 candidate: check against freeze v3 with the switch off and on (inbox diag-analysis item 3 (1)).

  python scripts/synth/v4_replay_check.py [--part labels|rules|traces] [--limit N] [--out FILE]

From the v3 tracker cache (staging/tracks_freeze_v3, a local copy); no tracker runs, no LLM calls.
- labels: the 51 v3 labels recomputed with the switch off equal `labels.json`. With it on, the rods whose label
  changes are listed (C3 option a)
- rules: script and remedy tree rerun from the cache give the outcome of each v3 summary (switch off and on)
- traces: every executed request_info and apply_remedy of the v3 LLM runs (the trace each summary names),
  re-executed in order on a new slice, returns the recorded result, check values included. With the switch on,
  the same except the C2 fields added to stage_log_summary
Writes a markdown table to --out (default results/2026-10-25_freeze_v4/switch_check.md).
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scored_v3 as v3  # noqa: E402
from agents import candidate  # noqa: E402
from agents.executors import BlindSlice, Slice  # noqa: E402

C2_FIELDS = ("moves_every_pair", "moves_every_pair_note", "closure_residual_px_per_pair_median",
             "closure_residual_px_per_pair_max", "closure_residual_max_pair_index")
OUT = ROOT / "results" / "2026-10-25_freeze_v4" / "switch_check.md"


def _norm(x):
    return json.dumps(json.loads(json.dumps(x, default=str)), sort_keys=True)


def labels_part():
    recorded = json.loads((v3.OUT / "labels.json").read_text())["labels"]
    out = {}
    for name in (None, "v4"):
        candidate.use(name)
        _, info = v3.labels_report()
        got = info["labels"]
        diff = sorted(r for r in recorded if got.get(r, {}).get("class") != recorded[r]["class"]
                      or got.get(r, {}).get("sequence") != recorded[r]["sequence"])
        out[name or "off"] = {"rods": len(got), "differ": diff,
                              "changes": {r: f"{recorded[r]['class']} -> {got[r]['class']}" for r in diff if r in got}}
    candidate.reset()
    return out


def rules_part():
    out = {}
    for name in (None, "v4"):
        candidate.use(name)
        same, diff = 0, []
        for rod in v3.scored_rods():
            for m, fn in v3.RULES.items():
                s = json.loads((v3.OUT / "runs" / f"{v3.stem(m, rod)}_summary.json").read_text())["outcome"]
                o = fn(v3.Slice(v3.V3Runner(), rod), None)
                if (o.status, o.steps, _norm(o.args)) == (s["status"], s["steps"], _norm(s["args"])):
                    same += 1
                else:
                    diff.append(v3.stem(m, rod))
        out[name or "off"] = {"runs": same + len(diff), "same": same, "differ": diff}
    candidate.reset()
    return out


def replay_trace(method, rod, trace):
    """(steps compared, [step numbers that differ]) for one trace, with the switch as set now."""
    cls = {"diagnostician": Slice, "single_agent": BlindSlice}[method]
    sl = cls(v3.V3Runner(), rod)
    ex = sl.executors()
    n, bad = 0, []
    for line in trace.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        act = d.get("action") or {}
        if d.get("status") != "executed" or act.get("name") not in ex:
            continue
        got = ex[act["name"]](act["args"], {})
        if candidate.v4() and act["name"] == "request_info" and act["args"].get("kind") == "stage_log_summary":
            got = {k: v for k, v in got.items() if k not in C2_FIELDS}
        n += 1
        if _norm(got) != _norm(d["result"]):
            bad.append(d["step"])
    return n, bad


def traces_part(limit=None):
    out = {}
    for name in (None, "v4"):
        candidate.use(name)
        runs, steps, diff, t0 = 0, 0, [], time.time()
        for rod in v3.scored_rods():
            for m in v3.LLM:
                for k in v3.REPEATS:
                    if limit is not None and runs >= limit:
                        break
                    s = json.loads((v3.OUT / "runs" / f"{v3.stem(m, rod, k)}_summary.json").read_text())
                    n, bad = replay_trace(m, rod, v3.OUT / "runs" / s["trace"])
                    runs, steps = runs + 1, steps + n
                    if bad:
                        diff.append(f"{v3.stem(m, rod, k)} steps {bad}")
        out[name or "off"] = {"runs": runs, "steps": steps, "differ": diff, "wall_s": round(time.time() - t0)}
    candidate.reset()
    return out


def report(res):
    L = ["# Freeze v4 candidate: switch check against freeze v3", "",
         "From the v3 tracker cache and run records; no tracker runs, no LLM calls. "
         "`python scripts/synth/v4_replay_check.py`.", ""]
    if "labels" in res:
        L += ["## Labels (51 rods)", "", "| Switch | Rods | Label or sequence differs from v3 |", "| :-- | --: | :-- |"]
        for k, v in res["labels"].items():
            L.append(f"| {k} | {v['rods']} | {len(v['differ'])}"
                     + (": " + "; ".join(f"{r} {c}" for r, c in v["changes"].items()) if v["differ"] else "") + " |")
        L.append("")
    if "rules" in res:
        L += ["## Rule methods rerun from the cache", "", "| Switch | Runs | Same outcome | Differ |",
              "| :-- | --: | --: | :-- |"]
        for k, v in res["rules"].items():
            L.append(f"| {k} | {v['runs']} | {v['same']} | {', '.join(v['differ']) or 'none'} |")
        L.append("")
    if "traces" in res:
        L += ["## LLM traces re-executed (request_info and apply_remedy results)", "",
              "| Switch | Runs | Steps compared | Runs with a differing step | Wall (s) |", "| :-- | --: | --: | :-- | --: |"]
        for k, v in res["traces"].items():
            L.append(f"| {k} | {v['runs']} | {v['steps']} | {len(v['differ'])}"
                     + (": " + "; ".join(v["differ"]) if v["differ"] else "") + f" | {v['wall_s']} |")
        L += ["", "Switch on: the C2 fields of stage_log_summary are removed before the comparison; every other "
              "result, check values included, must be equal.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["labels", "rules", "traces"], action="append")
    ap.add_argument("--limit", type=int, default=None, help="traces: at most this many runs per switch setting")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()
    if not v3.CACHE.exists():
        sys.exit(f"no v3 cache at {v3.CACHE.relative_to(ROOT)}")
    parts = a.part or ["labels", "rules", "traces"]
    res = {}
    for p in parts:
        res[p] = {"labels": labels_part, "rules": rules_part, "traces": lambda: traces_part(a.limit)}[p]()
        print(p, json.dumps(res[p]), flush=True)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(report(res) + "\n", encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
