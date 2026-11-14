"""Task c026 report: fixed script, remedy tree and diagnostician over the batch-2 windows that fail closure.

Called as `python scripts/batch2_agents.py report --tree DIR --agents DIR --out results/2026-11-12_batch2_agents`.
Reads the tree records and trace (DIR/windows/*.json, tree_trace.jsonl), the agent run (summary.json merged over the
groups, g*/diagnostician_trace.jsonl, auditor in summary.json) and writes tables.md, windows.csv and example_traces.md.
Outcome and check values only: REGR, growth-zone and flank values are masked.
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from audit.view import opaque_ids

MASK_KEYS = re.compile(r"regr|growth|zone|flank|plane|peak|velocity|width|curvature|kappa|profile", re.I)
MASK_TEXT = re.compile(r"((?:REGR|growth[- ]zone|growth|flank|peak|zone length)[^.;\d]{0,40}?)(-?\d[\d.,]*\s*(?:%/h|um|µm|px)?)",
                       re.I)


def mask(obj):
    """Values under biology keys become '[masked]'; numbers right after a biology word in text too."""
    if isinstance(obj, dict):
        return {k: "[masked]" if MASK_KEYS.search(k) else mask(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mask(v) for v in obj]
    if isinstance(obj, str):
        prev = None
        while prev != obj:
            prev, obj = obj, MASK_TEXT.sub(lambda m: m.group(1) + "[masked]", obj)
        return obj
    return obj


def remedy_of(args):
    return f"{args.get('remedy')}{' ' + args['setting'] if args.get('setting') else ''}"


def remedy_steps(trace_lines, task_id=None):
    """Executed apply_remedy steps of one task: remedy, result kind, closure before and after."""
    out = []
    for d in trace_lines:
        if task_id is not None and d.get("task_id") != task_id:
            continue
        act = d.get("action") or {}
        if d.get("status") != "executed" or act.get("name") != "apply_remedy":
            continue
        res = d.get("result") or {}
        kind = ("not available" if not res.get("rechecked") else "rolled back" if res.get("rolled_back") else "kept")
        cv = res.get("check_values") or {}
        clo = cv.get("closure") or {}
        out.append({"remedy": remedy_of(act.get("args") or {}), "result": kind,
                    "closure_before": clo.get("before"), "closure_after": clo.get("after"),
                    "error": res.get("error", "")})
    return out


def read_jsonl(path):
    p = Path(path)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def load_tree(tree_dir):
    recs = {json.loads(p.read_text())["window"]: json.loads(p.read_text())
            for p in sorted((tree_dir / "windows").glob("*.json"))}
    trace = read_jsonl(tree_dir / "tree_trace.jsonl")
    by_task = defaultdict(list)
    for d in trace:
        by_task[d.get("task_id", "")].append(d)
    out = {}
    for wid, r in recs.items():
        lines = by_task.get(f"{wid} window", [])
        starts = [i for i, d in enumerate(lines) if d.get("step") == 1]
        lines = lines[starts[-1]:] if starts else lines      # an interrupted, restarted window: its last attempt
        steps = remedy_steps(lines)
        st = r["outcome"]["status"]
        final = (r.get("final_closure") or {}).get("passed")
        out[wid] = {"status": st, "accepted_repaired": st == "accept" and final is True,
                    "fault": (r["outcome"].get("args") or {}).get("fault", ""), "steps": steps,
                    "kept": [s["remedy"] for s in steps if s["result"] == "kept"],
                    "final_closure": (r.get("final_closure") or {}).get("value"), "error": r.get("error", ""),
                    "initial_closure": (r.get("initial_closure") or {}).get("value", r.get("batch2_closure")),
                    "task_id": f"{wid} window", "lines": lines}
    return out


def load_agents(agents_dir):
    summ = json.loads((agents_dir / "summary.json").read_text())
    traces = []
    for g in sorted(agents_dir.glob("g[0-9]*")):
        traces += read_jsonl(g / "diagnostician_trace.jsonl")
    out, calls = {}, Counter()
    for tid, s in summ["tasks"].items():
        wid = f"{s['root_id']}__w{s['window_h'][0]:g}-{s['window_h'][1]:g}"
        o = s["outcome"]
        task_lines = [d for d in traces if d.get("task_id") == tid]
        steps = remedy_steps(task_lines)
        final = next((c for c in s["final_checks"] if c["check"] == "closure"), {})
        init = next((c for c in s["initial_checks"] if c["check"] == "closure"), {})
        kept = [st["remedy"] for st in steps if st["result"] == "kept"]
        out[wid] = {"task_id": tid, "status": o["status"], "accepted_repaired": o["status"] == "accept"
                    and final.get("passed") is True, "fault": (o.get("args") or {}).get("fault", ""),
                    "steps": steps, "kept": kept, "final_closure": final.get("value"),
                    "initial_closure": init.get("value"), "calls": o.get("calls", 0),
                    "input_tokens": o.get("input_tokens", 0), "output_tokens": o.get("output_tokens", 0),
                    "call_ms": o.get("call_ms", 0), "condition": s.get("condition", "")}
        calls["diagnostician"] += o.get("calls", 0)
    for g in sorted(agents_dir.glob("g[0-9]*")):
        calls["dispatcher"] += sum("call" in d for d in read_jsonl(g / "dispatcher_trace.jsonl"))
    aud = summ.get("auditor") or {}
    calls["auditor"] = aud.get("calls", 0) or sum("call" in d for d in read_jsonl(agents_dir / "auditor_trace.jsonl"))
    rid = dict(zip(summ["tasks"], opaque_ids(len(summ["tasks"]), "real_slice")))      # the auditor's run ids
    for wid, r in out.items():
        dec = (aud.get("decisions") or {}).get(rid[r["task_id"]], {})
        r["auditor"], r["auditor_reason"] = dec.get("decision", ""), dec.get("reason", "")
    return out, calls, summ, traces


def method_row(name, recs, n):
    st = Counter(r["status"] for r in recs.values())
    rep = sum(r["accepted_repaired"] for r in recs.values())
    tried = Counter(s["result"] for r in recs.values() for s in r["steps"])
    return (f"| {name} | {n} | {len(recs)} | {rep} | {st['accept'] - rep} | {st['decline']} | {st['step_limit']} | "
            f"{st['error']} | {sum(tried.values())} | {tried['kept']} | {tried['rolled back']} | "
            f"{tried['not available']} |")


def outcome_class(r):
    if r is None:
        return "not run"
    return "accept" if r["status"] == "accept" else r["status"]


def main(tree_dir, agents_dir, out, windows):
    out.mkdir(parents=True, exist_ok=True)
    tree = load_tree(tree_dir) if (tree_dir / "windows").exists() else {}
    agents, calls, summ, traces = load_agents(agents_dir) if (agents_dir / "summary.json").exists() \
        else ({}, Counter(), {}, [])
    n = len(windows)
    md = ["# c026 tables", "", "Generated by `python scripts/batch2_agents.py report`. Real windows have no ground truth: "
          "'accepted after repair' means closure passes on the recheck after a kept remedy.", "",
          "## Outcome per method", "",
          "| Method | Windows | Run | Accepted after repair | Accepted, closure failing | Declined | Step limit | Error | "
          "Remedies tried | Kept | Rolled back | Not available |",
          "| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |",
          f"| fixed script | {n} | {n} | 0 | 0 | {n} | 0 | 0 | 0 | 0 | 0 | 0 |",
          method_row("remedy tree", tree, n)] + ([method_row("diagnostician", agents, n)] if agents else []) + [""]
    cond = condition_of()
    if tree:
        per = defaultdict(Counter)
        for w, _ in windows:
            per[cond.get(w.id(), "")][outcome_class(tree.get(w.id())) if w.id() in tree else "not run"] += 1
        md += ["## Remedy tree per condition", "", "| Condition | Windows | Accepted after repair | Declined | Error | "
               "Not run |", "| :-- | --: | --: | --: | --: | --: |"]
        md += [f"| {c} | {sum(k.values())} | {k['accept']} | {k['decline']} | {k['error']} | {k['not run']} |"
               for c, k in sorted(per.items())] + [""]
    # agreement
    both = [w.id() for w, _ in windows if w.id() in tree and w.id() in agents]
    same_out = sum(outcome_class(tree[w]) == outcome_class(agents[w]) for w in both)
    same_kept = sum(sorted(tree[w]["kept"]) == sorted(agents[w]["kept"]) for w in both)
    agree = ["## Agreement, diagnostician vs tree", "",
           f"- Windows run by both: {len(both)}", f"- Same outcome: {same_out} of {len(both)}",
           f"- Same remedies kept (none counts as the same when both kept none): {same_kept} of {len(both)}",
           "- Outcome pairs (tree, diagnostician): " + ", ".join(
               f"{a} / {b} {k}" for (a, b), k in sorted(Counter((outcome_class(tree[w]), outcome_class(agents[w]))
                                                                 for w in both).items())), ""]
    md += agree if agents else []
    # LLM use
    if agents:
        ins = sum(r["input_tokens"] for r in agents.values())
        outs = sum(r["output_tokens"] for r in agents.values())
        ms = [r["call_ms"] / r["calls"] for r in agents.values() if r["calls"]]
        md += ["## Diagnostician use", "",
               f"- LLM calls: diagnostician {calls['diagnostician']}, dispatcher {calls['dispatcher']}, auditor "
               f"{calls['auditor']}; total {sum(calls.values())} (cap 700)",
               f"- Diagnostician tokens: in {ins}, out {outs}; mean call time per window "
               f"{sum(ms) / len(ms) / 1000:.1f} s" if ms else "- no diagnostician call",
               "- Faults named: " + ", ".join(f"{k or 'none'} {v}" for k, v in
                                              Counter(r["fault"] for r in agents.values()).most_common()),
               "- Remedies tried: " + ", ".join(f"{k} {v}" for k, v in Counter(
                   s["remedy"] for r in agents.values() for s in r["steps"]).most_common()), ""]
    if tree:
        md += ["## Remedy tree", "",
               "- Faults named: " + ", ".join(f"{k or 'none'} {v}" for k, v in
                                              Counter(r["fault"] for r in tree.values()).most_common()),
               "- Remedies tried: " + ", ".join(f"{k} {v}" for k, v in Counter(
                   s["remedy"] for r in tree.values() for s in r["steps"]).most_common()),
               "- Errors: " + ("; ".join(f"{w}: {r['error'][:100]}" for w, r in tree.items() if r["error"]) or "none"),
               ""]
    # auditor on repaired windows
    rep = {w: r for w, r in agents.items() if r["accepted_repaired"]}
    md += ["## Auditor on windows the diagnostician accepted after repair", ""] if agents else []
    md += [] if not agents else [f"- {w}: {r['auditor'] or 'no decision'}{' (' + r['auditor_reason'] + ')' if r['auditor_reason'] else ''}"
           for w, r in sorted(rep.items())] or ["- none accepted after repair"]
    md += [] if not agents else ["", "## Disagreement list", "",
           "Closure in px/h before -> after each remedy tried (kept, rolled back or not available).", ""]

    def fmt(steps):
        return "; ".join(f"{s['remedy']} {s['result']}" + (
            f" ({s['closure_before']:.1f} -> {s['closure_after']:.1f})" if isinstance(s["closure_before"], (int, float))
            and isinstance(s["closure_after"], (int, float)) else "") for s in steps) or "no remedy"
    dis = [w for w in both if outcome_class(tree[w]) != outcome_class(agents[w])
           or sorted(tree[w]["kept"]) != sorted(agents[w]["kept"])]
    md += [] if not agents else ["| Window | Closure | Tree | Tree remedies | Diagnostician | Fault named | "
                                 "Diagnostician remedies |", "| :-- | --: | :-- | :-- | :-- | :-- | :-- |"]
    md += [f"| {w} | {tree[w]['initial_closure']:.1f} | {outcome_class(tree[w])} | {fmt(tree[w]['steps'])} | "
           f"{outcome_class(agents[w])} | {agents[w]['fault']} | {fmt(agents[w]['steps'])} |" for w in dis]
    md += ["", f"{len(dis)} windows differ."] if agents else []
    if tree:
        md += ["## Remedy tree, per window", "", "Closure in px/h before -> after each remedy (kept, rolled back or not "
               "available).", "", "| Window | Closure | Outcome | Fault named | Remedies |", "| :-- | --: | :-- | :-- | :-- |"]
        md += [f"| {w} | {r['initial_closure']:.1f} | {outcome_class(r)} | {r['fault']} | {fmt(r['steps'])} |"
               for w, r in sorted(tree.items())]
    (out / "tables.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    with open(out / "windows.csv", "w", newline="") as f:
        cols = ["window", "root", "condition", "from_h", "to_h", "batch2_closure_px_per_h", "tree_outcome", "tree_fault",
                "tree_kept", "tree_tried", "tree_final_closure_px_per_h", "diag_outcome", "diag_fault", "diag_kept",
                "diag_tried", "diag_final_closure_px_per_h", "diag_calls", "auditor", "same_outcome", "same_kept"]
        wr = csv.DictWriter(f, cols)
        wr.writeheader()
        for w, c in windows:
            t, a = tree.get(w.id()), agents.get(w.id())
            wr.writerow({"window": w.id(), "root": w.root_id, "condition": cond.get(w.id(), ""),
                         "from_h": w.from_h, "to_h": w.to_h, "batch2_closure_px_per_h": round(c, 3),
                         "tree_outcome": outcome_class(t), "tree_fault": (t or {}).get("fault", ""),
                         "tree_kept": ";".join((t or {}).get("kept", [])),
                         "tree_tried": ";".join(f"{s['remedy']}:{s['result']}" for s in (t or {}).get("steps", [])),
                         "tree_final_closure_px_per_h": _r((t or {}).get("final_closure")),
                         "diag_outcome": outcome_class(a), "diag_fault": (a or {}).get("fault", ""),
                         "diag_kept": ";".join((a or {}).get("kept", [])),
                         "diag_tried": ";".join(f"{s['remedy']}:{s['result']}" for s in (a or {}).get("steps", [])),
                         "diag_final_closure_px_per_h": _r((a or {}).get("final_closure")),
                         "diag_calls": (a or {}).get("calls", ""), "auditor": (a or {}).get("auditor", ""),
                         "same_outcome": "" if not (t and a) else outcome_class(t) == outcome_class(a),
                         "same_kept": "" if not (t and a) else sorted(t["kept"]) == sorted(a["kept"])})
    if agents:
        write_examples(out, agents, traces, "Diagnostician")
    else:
        write_examples(out, tree, [d for r in tree.values() for d in r["lines"]], "Remedy tree")
    print(f"wrote {out}: tree {len(tree)}, diagnostician {len(agents)} windows; {len(dis)} differ")


def _r(v):
    return "" if v is None else round(v, 3)


def condition_of(path=Path(__file__).resolve().parents[1] / "results" / "2026-10-25_full_batch_2" / "windows.csv"):
    with open(path, newline="") as f:
        return {r["window"]: r["condition"] for r in csv.DictReader(f)}


def write_examples(out, agents, traces, who):
    """Two windows: one accepted after a kept remedy (else one with a kept remedy), one declined."""
    kept = [w for w, r in agents.items() if r["accepted_repaired"]] or [w for w, r in agents.items() if r["kept"]]
    declined = [w for w, r in agents.items() if r["status"] == "decline" and r["steps"]] or \
        [w for w, r in agents.items() if r["status"] == "decline"]
    md = ["# Example traces (c026)", "", f"{who} on two batch-2 windows that fail closure. For each step: the "
          "action sent (name, arguments, rationale), the tool result, and the final outcome. REGR, "
          "growth-zone and flank values are `[masked]`.", ""]
    for title, ws in (("Remedy kept", kept), ("Declined", declined)):
        if not ws:
            md += [f"## {title}", "", "No such window in this run.", ""]
            continue
        w = sorted(ws)[0]
        r = agents[w]
        md += [f"## {title}: {w} (initial closure {r['initial_closure']:.1f} px/h, threshold 19)", ""]
        for d in [d for d in traces if d.get("task_id") == r["task_id"] and d.get("status") in ("executed", "terminal")]:
            o = d.get("output") or {}
            act = d.get("action") or {}
            md += [f"### Step {d.get('step')}: {act.get('name')}", "",
                   f"- Arguments: `{json.dumps(mask(act.get('args') or {}))}`",
                   f"- Rationale: {mask(o.get('rationale', ''))}"]
            if "result" in d:
                md += [f"- Result: `{json.dumps(mask(d['result']), default=str)[:1500]}`"]
            md += [""]
        md += [f"Outcome: {r['status']}" + (f", fault {r['fault']}" if r["fault"] else "")
               + f"; final closure {r['final_closure']:.1f} px/h" if r["final_closure"] is not None else "", ""]
    (out / "example_traces.md").write_text("\n".join(md) + "\n", encoding="utf-8")
