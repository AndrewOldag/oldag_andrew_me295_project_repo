"""Task c027 report: integrated run, remedy tree and fixed script over every include-yes window (spec 2026-11-18 B7-B9).

Called as `python scripts/run_all.py report --run DIR --tree DIR --out results/2026-11-18_integrated_run`. Reads the run
records (DIR/windows/*.json, traces/, audit/<root>/audit.json, run_log.jsonl), the tree records (this run's and the
c026 ones), the retrack queue (staging/c027/queue.csv, queue_log.jsonl) and the batch windows. Writes tables.md,
failure_modes.md, windows.csv and example_traces.md. Outcome and check values only: REGR, growth-zone and flank values
are masked.
"""
import csv
import json
import re
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

from batch2_agents_report import mask

ROOT = Path(__file__).resolve().parents[1]
C026_TREE = ROOT / "staging" / "c026" / "tree"
QUEUE = ROOT / "staging" / "c027"


def read_json_dir(d):
    return {p.stem: json.loads(p.read_text()) for p in sorted(Path(d).glob("*.json"))} if Path(d).exists() else {}


def read_jsonl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def cls(r):
    """Outcome class of one integrated-run record."""
    if r is None:
        return "not reached"
    if r["status"] in ("paused", "error"):
        return r["status"]
    o, by = r["outcome"]["status"], r.get("decided_by")
    if o == "accept":
        return "accepted after repair" if any(s["kept"] for s in r["remedies"]) else "accepted"
    if o == "decline":
        return "declined by rule" if by == "rule" else "declined by agent"
    return o                                                  # step_limit, error


def tree_cls(t):
    if t is None:
        return "not reached"
    st = t["outcome"]["status"]
    if st == "accept":
        return "accepted after repair" if any(s.get("kept") for s in t.get("remedies", [])) else "accepted"
    return {"decline": "declined by tree"}.get(st, st)


def script_cls(r):
    if r is None or r["status"] != "final":
        return cls(r)
    if r.get("decided_by") == "rule":
        return cls(r)
    return "declined by check"                               # first check fails, no remedy


CLASSES = ["accepted", "accepted after repair", "declined by rule", "declined by check", "declined by agent",
           "declined by tree", "step_limit", "error", "paused", "not reached"]


def table(title, counts_by, keys, cols):
    md = [f"### {title}", "", "| " + " | ".join([keys] + cols + ["total"]) + " |",
          "| " + " | ".join([":--"] + ["--:"] * (len(cols) + 1)) + " |"]
    for k, c in counts_by.items():
        md.append("| " + " | ".join([str(k)] + [str(c.get(x, 0)) for x in cols] + [str(sum(c.values()))]) + " |")
    return md + [""]


def _last_line(err):
    """Last line of a cluster error, folders dropped (no host path in a tracked file)."""
    line = next((l for l in reversed(str(err).splitlines()) if l.strip()), "")
    return re.sub(r"/[^\s'\"]*/", "", line).strip()[:120]


def main(run_dir, tree_dir, out, rows, demo=None):
    import run_all as RA
    out.mkdir(parents=True, exist_ok=True)
    if demo:
        print("demo: same outcome %d of %d windows" % write_demo(out, run_dir, demo[0], demo[1]))
    order = [w.id() for w in RA.window_list()]
    recs = read_json_dir(run_dir / "windows")
    tree = read_json_dir(C026_TREE / "windows")
    tree_new = read_json_dir(tree_dir / "windows")
    tree.update(tree_new)              # c027 tree records replace c026 ones (register v1, no gate; spec 2026-11-20)
    audits = {p.parent.name: json.loads(p.read_text()) for p in sorted((run_dir / "audit").glob("*/audit.json"))}

    methods = OrderedDict()
    methods["integrated"] = Counter(cls(recs.get(w)) for w in order)
    methods["remedy tree (+ rule and pass as integrated)"] = Counter(
        tree_cls(tree.get(w)) if recs.get(w, {}).get("decided_by") == "diagnostician" else cls(recs.get(w))
        for w in order)
    methods["fixed script"] = Counter(script_cls(recs.get(w)) for w in order)
    cols = [c for c in CLASSES if any(m.get(c) for m in methods.values())]
    md = ["# c027 integrated run: tables", "", f"Windows: {len(order)}. Records: {len(recs)}. "
          "Real windows have no ground truth; 'accepted after repair' means the checker passes after a kept remedy.", ""]
    md += table("Outcome per method", methods, "method", cols)

    by_cond, by_exp = defaultdict(Counter), defaultdict(Counter)
    for w in order:
        c = cls(recs.get(w))
        by_cond[rows.get(w, {}).get("condition") or "-"][c] += 1
        by_exp[w[:4]][c] += 1
    cols_i = [c for c in CLASSES if methods["integrated"].get(c)]
    md += table("Integrated run per condition", dict(sorted(by_cond.items())), "condition", cols_i)
    md += table("Integrated run per experiment (date)", dict(sorted(by_exp.items())), "experiment", cols_i)

    # diagnostician vs tree
    both = [w for w in order if recs.get(w, {}).get("decided_by") == "diagnostician" and w in tree
            and tree[w]["outcome"]["status"] not in ("paused", "error")]
    kept = lambda steps: next((s["settings"] for s in reversed(steps) if s.get("kept")), "none")   # noqa: E731
    agree_o = sum(recs[w]["outcome"]["status"] == tree[w]["outcome"]["status"] for w in both)
    agree_r = sum(kept(recs[w]["remedies"]) == kept(tree[w].get("remedies", [])) for w in both)
    md += ["### Diagnostician vs remedy tree", "",
           f"- Windows with both final: {len(both)}. Same outcome: {agree_o}. Same final kept settings: {agree_r}", ""]
    dis = [w for w in both if recs[w]["outcome"]["status"] != tree[w]["outcome"]["status"]
           or kept(recs[w]["remedies"]) != kept(tree[w].get("remedies", []))]
    if dis:
        md += ["| window | diagnostician | its remedies (closure before -> after, kept) | tree | its remedies |",
               "| :-- | :-- | :-- | :-- | :-- |"]
        fmt = lambda steps: "; ".join(                                                            # noqa: E731
            f"{s['settings']} {_v(s['closure_before'])} -> {_v(s['closure_after'])}{'' if s['kept'] else ' rolled back'}"
            for s in steps) or "none"
        for w in dis:
            md.append(f"| {w} | {recs[w]['outcome']['status']} | {fmt(recs[w]['remedies'])} | "
                      f"{tree[w]['outcome']['status']} | {fmt(tree[w].get('remedies', []))} |")
        md.append("")

    # remedies, LLM, auditor, cluster
    rem = Counter()
    for src, rs in (("diagnostician", [recs[w] for w in order if recs.get(w, {}).get("status") == "final"]),
                    ("tree", [tree[w] for w in order if w in tree])):
        for r in rs:
            for s in r.get("remedies", []):
                rem[(src, "tried")] += 1
                rem[(src, "kept" if s["kept"] else "rolled back")] += 1
    md += ["### Remedies", "", "| method | tried | kept | rolled back |", "| :-- | --: | --: | --: |"]
    md += [f"| {m} | {rem[(m, 'tried')]} | {rem[(m, 'kept')]} | {rem[(m, 'rolled back')]} |"
           for m in ("diagnostician", "tree")] + [""]
    llm = Counter()
    for r in recs.values():
        for k, v in (r.get("llm") or {}).items():
            llm[k] += v or 0
    a_calls = sum(a.get("calls") or 0 for a in audits.values())
    all_calls = RA.count_calls(run_dir.rglob("*trace*.jsonl"))[0]
    flags = [(root, rid, d) for root, a in audits.items() for rid, d in (a.get("decisions") or {}).items()
             if d.get("decision") == "flag"]
    md += ["### LLM use", "", f"- Diagnostician (recorded windows): {llm['calls']} calls, {llm['input_tokens']} input "
           f"tokens, {llm['output_tokens']} output tokens, {llm['call_ms'] / 3.6e6:.2f} h of call time",
           f"- Auditor: {len([a for a in audits.values() if a.get('status') != 'not_called'])} runs, {a_calls} calls; "
           f"{len([a for a in audits.values() if a.get('status') == 'not_called'])} roots with no accepted window "
           "(no call)", f"- All traces under the run folder, paused and set-aside included: {all_calls} calls "
           "(cap 900)", f"- Auditor flags: {len(flags)}", ""]
    queue = list(csv.DictReader(open(QUEUE / "queue.csv"))) if (QUEUE / "queue.csv").exists() else []
    qs = Counter(r["state"] for r in queue)
    md += ["### Cluster", "", f"- Retrack tasks recorded: {len(queue)} ({', '.join(f'{k} {v}' for k, v in sorted(qs.items()))}); "
           f"arrays {len({r['array'] for r in queue})}", ""]
    (out / "tables.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # failure modes
    fm = [("tracker error in the batch run (no base track)",
           [w for w in order if rows.get(w, {}).get("status") == "failed"]),
          ("window not measured in any batch", [w for w in order if w not in rows]),
          ("declined by rule (gating check not computable)",
           [w for w in order if cls(recs.get(w)) == "declined by rule"]),
          ("diagnostician step limit", [w for w in order if cls(recs.get(w)) == "step_limit"]),
          ("tree step limit", [w for w in order if tree_cls(tree.get(w)) == "step_limit"]),
          ("window error in the run", [w for w in order if cls(recs.get(w)) == "error"]),
          ("paused at the cut-off (track not cached)", [w for w in order if cls(recs.get(w)) == "paused"]),
          ("rolled-back remedy that made closure worse (diagnostician)",
           [w for w in order if recs.get(w, {}).get("status") == "final" and any(_worse(s) for s in recs[w]["remedies"])]),
          ("rolled-back remedy that made closure worse (tree)",
           [w for w in order if w in tree and any(_worse(s) for s in tree[w].get("remedies", []))]),
          ("auditor flag", [f"{root}: {rid}" for root, rid, _ in flags]),
          ("retrack task failed on the cluster", [f"{r['job']} ({_last_line(r['error'])})" for r in queue if r["state"] == "failed"])]
    links = [e for l in read_jsonl(QUEUE / "queue_log.jsonl") for e in l.get("link", []) if "connected" not in e[1]]
    links += [{"status": l["status"]} for l in read_jsonl(QUEUE / "queue_log.jsonl") if l["status"] == "connection down"]
    fm.append(("link or master down (queue)", [json.dumps(e) for e in links]))
    md = ["# c027 failure modes (from the run)", "", "| failure mode | count | example |", "| :-- | --: | :-- |"]
    md += [f"| {name} | {len(xs)} | {xs[0] if xs else '-'} |" for name, xs in fm]
    md += ["", "Synthetic findings (spec section C) are reported by task c029 and c030 in their own results.", ""]
    (out / "failure_modes.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # windows.csv
    fields = ["window", "root", "condition", "batch", "integrated", "fixed_script", "remedy_tree", "initial_closure_px_per_h",
              "final_closure_px_per_h", "final_settings", "remedies_tried", "remedies_kept", "diagnostician_calls",
              "paused_needs", "auditor"]
    with open(out / "windows.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fields)
        wr.writeheader()
        for w in order:
            r, row = recs.get(w) or {}, rows.get(w, {})
            dec = next((d.get("decision") for a in audits.values() for rid, d in (a.get("decisions") or {}).items()
                        if rid == w), "")
            wr.writerow({"window": w, "root": w.split("__w")[0], "condition": row.get("condition", ""),
                         "batch": row.get("batch", ""), "integrated": cls(recs.get(w)), "fixed_script": script_cls(recs.get(w)),
                         "remedy_tree": tree_cls(tree.get(w)) if r.get("decided_by") == "diagnostician" else "",
                         "initial_closure_px_per_h": _v(r.get("initial_closure")),
                         "final_closure_px_per_h": _v(r.get("final_closure")), "final_settings": r.get("final_tag", ""),
                         "remedies_tried": len(r.get("remedies", [])),
                         "remedies_kept": sum(s["kept"] for s in r.get("remedies", [])),
                         "diagnostician_calls": (r.get("llm") or {}).get("calls", ""),
                         "paused_needs": r.get("reason", "") if r.get("status") == "paused" else "", "auditor": dec})
    write_examples(out, run_dir, recs, order, flags)
    print(f"wrote {out}")
    return 0


DEMO_STAGES = [("stage the root's images to the cluster", "driver", r"staging \d+ MB", "driver", r": job \d+"),
               ("cluster job: midline net, QC, track, checker; collect, md5 (includes queue wait)", "driver", r": job \d+",
                "driver", r"collected"),
               ("fetch base tracks to the VM", "after", r"fetch start", "after", r"fetch end"),
               ("agents and auditor", "after", r"run start", "after", r"run end")]


def _stamps(log):
    p = Path(log)
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines() if p.exists() else []
    return [(l[:19], l[20:]) for l in lines if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} ", l)]


def _at(stamps, pat):
    import datetime
    t = next((t for t, m in stamps if re.search(pat, m)), None)
    return datetime.datetime.fromisoformat(t) if t else None


def write_demo(out, run_dir, demo_dir, root):
    """B5: fresh one-root demo against the cached run, window by window; wall time per stage from the demo logs."""
    a, b = read_json_dir(run_dir / "windows"), read_json_dir(demo_dir / "run" / "windows")
    ws = sorted((w for w in set(a) | set(b) if w.startswith(root + "__")), key=lambda w: int(w.split("__w")[1].split("-")[0]))
    md = [f"# c027 B5: fresh one-root demo ({root})", "", "| window | cached run | demo | closure before (px/h) cached / demo | match |",
          "| :-- | :-- | :-- | :-- | :-- |"]
    same = 0
    for w in ws:
        ca, cb = cls(a.get(w)), cls(b.get(w))
        va = _v(next((c for c in (a.get(w) or {}).get("initial_checks", []) if c["check"] == "closure"), None))
        vb = _v(next((c for c in (b.get(w) or {}).get("initial_checks", []) if c["check"] == "closure"), None))
        same += ca == cb
        md.append(f"| {w} | {ca} | {cb} | {va} / {vb} | {'yes' if ca == cb else 'no'} |")
    md += ["", f"Same outcome: {same} of {len(ws)} windows.", ""]
    fa, fb = [json.loads(p.read_text()) if p.exists() else {} for p in
              (run_dir / "audit" / root / "audit.json", demo_dir / "run" / "audit" / root / "audit.json")]
    flags = [sorted((r, d.get("reason")) for r, d in (x.get("decisions") or {}).items() if d.get("decision") == "flag")
             for x in (fa, fb)]
    md += [f"Auditor flags: cached {flags[0] or 'none'}; demo {flags[1] or 'none'}; "
           f"{'same' if flags[0] == flags[1] else 'different'}. LLM calls: cached {fa.get('calls', '-')}, demo {fb.get('calls', '-')}.",
           "", "| stage | wall time (min) |", "| :-- | --: |"]
    logs = {"driver": _stamps(demo_dir / "driver.log"), "after": _stamps(demo_dir / "after.log")}
    for name, l0, p0, l1, p1 in DEMO_STAGES:
        t0, t1 = _at(logs[l0], p0), _at(logs[l1], p1)
        md.append(f"| {name} | {(t1 - t0).total_seconds() / 60:.1f} |" if t0 and t1 else f"| {name} | - |")
    (out / "demo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return same, len(ws)


def _v(c):
    return "" if not c or c.get("value") is None else f"{c['value']:.2f}"


def _worse(s):
    b, a = (s.get("closure_before") or {}).get("value"), (s.get("closure_after") or {}).get("value")
    return not s.get("kept") and b is not None and a is not None and a > b


def write_examples(out, run_dir, recs, order, flags):
    md = ["# c027 example traces", "", "Outcome and check values only; REGR, growth-zone and flank values are `[masked]`.", ""]
    picks = [("Accepted after repair", next((w for w in order if cls(recs.get(w)) == "accepted after repair"), None)),
             ("Declined by the agent", next((w for w in order if cls(recs.get(w)) == "declined by agent"), None))]
    for title, w in picks:
        md += [f"## {title}: {w or 'none in the run'}", ""]
        t = run_dir / "traces" / f"{w}_diagnostician_trace.jsonl"
        if not w or not t.exists():
            continue
        r = recs[w]
        md += [f"- Initial closure {_v(r['initial_closure'])} px/h; final {_v(r['final_closure'])} px/h; "
               f"final settings {r['final_tag']}", ""]
        for d in read_jsonl(t):
            if "step" not in d or "output" not in d:
                continue
            act = d.get("action") or {}
            md += [f"### Step {d['step']}: {act.get('name', d.get('status'))}",
                   f"- Arguments: `{json.dumps(mask(act.get('args') or {}))}`",
                   f"- Rationale: {mask(d['output'].get('rationale', ''))}"]
            if "result" in d:
                md += [f"- Result: `{json.dumps(mask(d['result']), default=str)[:1500]}`"]
            md.append("")
    md += ["## Auditor flag", ""]
    if flags:
        root, rid, d = flags[0]
        md += [f"- Root {root}, run {rid}: `{json.dumps(mask(d), default=str)[:1500]}`", ""]
    else:
        md += ["- No auditor flag in the run", ""]
    (out / "example_traces.md").write_text("\n".join(md) + "\n", encoding="utf-8")
