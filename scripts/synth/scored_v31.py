"""Freeze v3.1 (docs/specs/2026-10-24_freeze-v3.1.md, approved by Andrew 2026-10-24): new accept_repaired rods
that need their repair; methods rerun on them; v3.1 table = v3 accept_clean and decline runs + the new runs.

  python scripts/synth/scored_v31.py plan   --phase sizing|labels|methods [--dry-run]   # start one sweep
  python scripts/synth/scored_v31.py status
  python scripts/synth/scored_v31.py fetch                          # to staging/tracks_freeze_v31/
  python scripts/synth/scored_v31.py sizing                         # sizes on seeds 10-12 (sizing.md, .json)
  python scripts/synth/scored_v31.py labels                         # labels of the new rods, seeds 23-25
  python scripts/synth/scored_v31.py rules                          # script and remedy tree
  python scripts/synth/scored_v31.py agents --method diagnostician|single_agent --repeat 0|1|2 [--max-runs N]
  python scripts/synth/scored_v31.py second-root                    # second_root note from the v3 runs
  python scripts/synth/scored_v31.py eval                           # v3.1 metrics, v3 side by side

Everything else is the freeze v3 driver (scripts/synth/scored_v3.py), unchanged: this module points its cache,
output folder, rod set and tag at v3.1. Tracker states already in the v3 cache (staging/tracks_freeze_v3, a
local copy) are read from there and not run again; new runs go to CACHE and count against MAX_NEW.
Rule for a v3.1 accept_repaired rod, on 3 of 3 seeds: a listed check fails unremedied; the unremedied
measurement fails the scoring tolerance; a listed remedy state (the v3 label sweep's) passes every check and is
good.
"""
import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scored_v3 as v3  # noqa: E402
from measure import metrics  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402
from measure.score import load_tolerance, measurement_good, rod_tolerance  # noqa: E402

FREEZE_TAG = "freeze-v3.1"
OUT = ROOT / "results" / "2026-10-24_freeze_v3.1"
CACHE = ROOT / "staging" / "tracks_freeze_v31"
V3_CACHE = v3.CACHE
V3_OUT = v3.OUT
TRACKS, SWEEP = "tracks_freeze_v31", "freeze_v31"
MAX_NEW = 300                                  # new tracker runs (spec, Runs)
GZ = v3.GZ
SCORING_SEEDS = (23, 24, 25)                   # spec: never used before
# Sizes tried, smallest first, at most 6 (spec, Sizing): from the v3 size upward in the fault's own unit.
# rigid_drift: factor, unit 1 (= the 2026-10-10 drift). bad_stage_correction: px, unit 1. stage_log_missing:
# fraction of the frames, v3 size 1 is the largest possible. width_change: no size at v3 geometry (one
# curvature). displacement_exceeds_patch: the spec's smaller stride products.
SIZES = {"rigid_drift": ["0.5", "1.5", "2.5", "3.5", "4.5", "5.5"],
         "width_change": [None],
         "bad_stage_correction": ["3", "4", "5", "6", "7", "8"],
         "stage_log_missing": ["1"],
         "displacement_exceeds_patch": ["2x2", "2x3", "2x4"]}
FAULTS = tuple(SIZES)
MIN_FAULTS, MIN_RODS = 3, 9                    # stop for Andrew below these (spec)


# ------------------------------------------------------------------ v3 driver, pointed at v3.1

def _lookup(name):
    for c in (CACHE, V3_CACHE):
        if (c / name).exists():
            return c / name
    return CACHE / name


def out_file(rod, st, moved=False):
    return _lookup(f"{rod.id(moved)}__{replace(st, width_free=False).tag()}.npz")


def truth(rod):
    import numpy as np
    f = _lookup(f"{rod.id()}_truth.npz")
    if not f.exists():
        return None
    with np.load(f) as z:
        return {k: z[k] for k in z.files}


_v3_label_states = v3.label_states


def label_states(rod):
    """v3 label states. displacement_exceeds_patch: change_frame_stride/half as the remedy does it from the
    rod's own stride (v3 wrote strides 3 and 1 for its stride 6), at most two steps."""
    if rod.fault != "displacement_exceeds_patch":
        return _v3_label_states(rod)
    base, h = v3.initial(rod), "change_frame_stride/half"
    out, st, seq = [([], base)], base.stride, []
    while st > 1 and len(seq) < 2:
        st, seq = max(1, st // 2), seq + [h]
        out.append((list(seq), replace(base, stride=st)))
    return out


def new_rods():
    """The v3.1 accept_repaired rods: each qualifying fault at its size, scoring seeds 23-25."""
    sizes = json.loads((OUT / "sizing.json").read_text())["sizes"]
    return [Rod(GZ, f, s, size=None if z == "v3" else z) for f, z in sizes.items() if z != "none"
            for s in SCORING_SEEDS]


def point_v3_at(which):
    """which: 'v31' (new cache first, new rods and output) or 'v3' (the v3 set, for its reused runs)."""
    v3.out_file, v3.truth, v3.label_states = out_file, truth, label_states
    v3.CACHE, v3.TRACKS, v3.SWEEP, v3.MAX_TRACKER_RUNS = CACHE, TRACKS, SWEEP, MAX_NEW
    if which == "v31":
        v3.OUT, v3.FREEZE_TAG = OUT, FREEZE_TAG
        v3.scored_rods = new_rods
    else:
        v3.OUT, v3.FREEZE_TAG = V3_OUT, "freeze-v3"
        v3.scored_rods = _v3_scored_rods


_v3_scored_rods = v3.scored_rods


# ------------------------------------------------------------------ sizing

def sizing_rows():
    """Per fault and size: the rule on each sizing seed, and the tracker states needed next. Unremedied runs
    (and the stride states of displacement_exceeds_patch, which need no earlier run) for every size at once;
    registration states, which need the unremedied run, at one size per round: the smallest one where parts 1
    and 2 hold on 3 of 3 and the remedy is not yet ruled out. Returns ({fault: [row]}, [(rod, state)])."""
    rows, need = {}, []
    for f in FAULTS:
        rows[f], pending = [], False
        for z in SIZES[f]:
            per_seed = []
            for s in v3.seeds("sizing_seeds"):
                rod = Rod(GZ, f, s, size=z)
                sts = label_states(rod)
                per_seed.append((rod, sts, [v3.evaluate(rod, st) if st is not None else None for _, st in sts]))
            u = [ev[0] for _, _, ev in per_seed]
            for rod, sts, ev in per_seed:
                need += [(rod, st) for i, ((_, st), e) in enumerate(zip(sts, ev))
                         if e is None and st is not None and (i == 0 or f == "displacement_exceeds_patch")]
            r12 = all(e is not None and not e["all_pass"] and not e["good"] for e in u)
            rem_done = all(e is not None for _, _, ev in per_seed for e in ev[1:])
            if r12 and not rem_done and not pending:
                for rod, sts, ev in per_seed:
                    need += [(rod, st) for (_, st), e in zip(sts[1:], ev[1:]) if e is None and st is not None]
                pending = True
            r3 = [any(e is not None and e["all_pass"] and e["good"] for e in ev[1:]) for _, _, ev in per_seed]
            ok = r12 and all(r3)
            state = ("yes" if ok else "no" if (all(e is not None for e in u) and not r12) or (r12 and rem_done)
                     else "not yet")
            rows[f].append({"size": z, "rule_1": sum(e is not None and not e["all_pass"] for e in u),
                            "rule_2": sum(e is not None and not e["good"] for e in u), "rule_3": sum(r3),
                            "evaluated": sum(e is not None for e in u), "qualifies": state,
                            "runs": [{"seq": seq, **e} for _, sts, ev in per_seed for (seq, _), e in zip(sts, ev)
                                     if e is not None]})
            if ok:
                break
    return rows, list({(r.id(), st.tag()): (r, st) for r, st in need}.values())


def sizing_report():
    rows, need = sizing_rows()
    L = ["# Freeze v3.1 sizing: accept_repaired rods that need their repair", "",
         f"Sizing seeds {', '.join(map(str, v3.seeds('sizing_seeds')))}. Rule, each part on 3 of 3 seeds: (1) a "
         "listed check fails unremedied; (2) the unremedied measurement fails the scoring tolerance; (3) a remedy "
         "state of the v3 label sweep passes every check and is good. Smallest size meeting the rule; at most 6 "
         "sizes per fault. States already in the v3 cache are reused.", "",
         "| Fault | Size | Unremedied run | (1) check fails | (2) not good | (3) remedy repairs | Qualifies |",
         "| :-- | :-- | :-- | :-- | :-- | :-- | :-- |"]
    sizes, per = {}, []
    for f, tried in rows.items():
        for t in tried:
            L.append(f"| {f} | {t['size'] or 'v3 (one size)'} | {t['evaluated']} of 3 | {t['rule_1']} of 3 | "
                     f"{t['rule_2']} of 3 | {t['rule_3']} of 3 | {t['qualifies']} |")
            for e in t["runs"]:
                per.append(f"| {e['rod']} | {' + '.join(e['seq']) or 'none'} | " + " | ".join(v3._cell(e, c) for c in v3.CHECKS)
                           + f" | {e['regr_rms_pct_per_h']:.2f} ({e['regr_limit']:.2f}) | "
                           f"{e['flank_difference_rms_pct_per_h']:.2f} ({e['flank_limit']:.2f}) | "
                           f"{'yes' if e['all_pass'] else 'no'} | {'yes' if e['good'] else 'no'} |")
        q = [t["size"] for t in tried if t["qualifies"] == "yes"]
        sizes[f] = (q[0] or "v3") if q else None              # "v3": the fault's one size at v3 geometry
    complete = not need
    final = {f: (z if z is not None else "none") for f, z in sizes.items()}
    n_q = sum(z is not None for z in sizes.values())
    stop = complete and (n_q < MIN_FAULTS or 3 * n_q < MIN_RODS)
    L += ["", f"- Tracker states still needed: {len(need)}",
          f"- Sizes: {final}" if complete else f"- Sizes so far: {sizes}",
          f"- Faults qualifying: {n_q} of {len(FAULTS)}; new accept_repaired rods {3 * n_q}" if complete else "",
          f"- Result: {'STOP for Andrew (fewer than 3 faults qualify or fewer than 9 rods)' if stop else ('complete' if complete else 'incomplete')}",
          "", "## Per state", "",
          "| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |",
          "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"] + per
    return "\n".join(x for x in L) + "\n", {"sizes": final, "complete": complete, "stop": stop, "need": need,
                                             "qualifying": n_q}


# ------------------------------------------------------------------ labels

def labels_report():
    text, info = v3.labels_report()
    text = text.replace("# Labels of the freeze v3 scored set", "# Labels of the freeze v3.1 accept_repaired rods", 1)
    n_rep = info["counts"]["accept_repaired"]
    info["stop"] = info["complete"] and n_rep < MIN_RODS
    if info["complete"]:
        text = text.replace("## Per state", f"- accept_repaired rods {n_rep} (stop below {MIN_RODS}): "
                            f"{'STOP for Andrew' if info['stop'] else 'enough'}\n\n## Per state", 1)
    return text, info


# ------------------------------------------------------------------ second_root (v3 runs)

def second_root_note():
    point_v3_at("v3")
    labels = json.loads((V3_OUT / "labels.json").read_text())["labels"]
    rows = [r for r in v3.score_runs(labels) if r.get("kind") == "second_root"]
    by = {}
    for r in rows:
        f = V3_OUT / "runs" / f"{v3.stem(r['method'], v3.Rod(GZ, 'second_root', r['seed'], size='30'), r['repeat'])}_summary.json"
        s = json.loads(f.read_text())
        wf = bool(s["final_settings"].get("width_free"))
        alt = r["status"] == "accept" and wf and r["good"]
        mask = any("mask_second_root" in x or "crop_to_main_root" in x for x in s["remedies"])
        b = by.setdefault(r["method"], {"runs": 0, "alternative_repair": 0, "accept_unremedied_not_good": 0,
                                        "tried_crop_or_mask": 0, "not_reported": 0})
        b["runs"] += 1
        b["alternative_repair"] += alt
        b["accept_unremedied_not_good"] += r["status"] == "accept" and not r["good"]
        b["tried_crop_or_mask"] += mask
        b["not_reported"] += r["category"] == "not_reported"
    lab = [l for l in (V3_OUT / "labels.md").read_text().splitlines() if "second_root" in l and "|" in l][3:]
    L = ["# second_root in freeze v3: cause of 0 correct", "",
         "Label: decline (v2 rule kept, Andrew 2026-10-13; `use_width_free_ratio` is not in its label states).",
         "", "## Cause, from the v3 label sweep and traces",
         f"- Unremedied, every seed fails plane_sections only (4.79, 9.89, 9.07 %/h; threshold {v3.TH['plane_sections']}); rigid_invariance "
         "and closure pass. Centre RMS is within tolerance (1.09, 0.43, 0.60 against 1.35 %/h); flank-difference RMS "
         "is not (1.19, 2.05, 2.20 against 1.00 %/h)",
         "- Both crop_or_mask states give the same checker values and errors as the unremedied run on every seed: "
         "at size 30 the mask does not change the tracked flanks",
         "- `use_width_free_ratio` skips plane_sections and drops the flank error from the goodness test, so after it "
         "every check that is applied passes and the centre measurement is good. Methods then accept",
         "- Scoring: an accept with a good measurement on a decline rod is accept_on_decline (not correct, not a false "
         "accept). The script accepts the unremedied run (flank not good): false accept",
         "", "## Runs ending with a good field after `use_width_free_ratio` (alternative repair)", "",
         "| Method | Runs | Alternative repair | Tried crop_or_mask | Accept, not good | Not reported |",
         "| :-- | --: | --: | --: | --: | --: |"]
    for m in v3.METHODS:
        b = by.get(m)
        if b:
            L.append(f"| {m} | {b['runs']} | {b['alternative_repair']} | {b['tried_crop_or_mask']} | "
                     f"{b['accept_unremedied_not_good']} | {b['not_reported']} |")
    L += ["", "Label sweep rows (v3 `labels.md`):", ""] + lab
    point_v3_at("v31")
    return "\n".join(L) + "\n", by


# ------------------------------------------------------------------ metrics: v3.1 and v3 side by side

def score_set(which, labels):
    point_v3_at(which)
    rows = v3.score_runs(labels)
    good0 = {}
    for rod in v3.scored_rods():
        e = v3.evaluate(rod, v3.initial(rod))
        good0[rod.id()] = e["good"] if e else False
    point_v3_at("v31")
    return rows, good0


def method_table(res, title):
    L = [f"## {title}", "",
         "| Method | Runs | Balanced accuracy | accept_clean | accept_repaired | decline | False accepts | Coverage | "
         "Abst. precision | Abst. recall | not_reported |",
         "| :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | :-- | --: |"]
    for m, v in res.items():
        a = v["accuracy_per_class"]
        nr = sum(p["categories"]["not_reported"] for p in v["per_repeat"])
        L.append(f"| {m} | {sum(p['runs'] for p in v['per_repeat'])} | {v3._f(v['balanced_accuracy'])} | "
                 f"{v3._f(a['accept_clean'])} | {v3._f(a['accept_repaired'])} | {v3._f(a['decline'])} | "
                 f"{v3._f(v['false_accepts'], 1)} | {v3._f(v['coverage'])} | {v3._f(v['abstention_precision'])} | "
                 f"{v3._f(v['abstention_recall'])} | {nr} |")
    return L


def results_of(rows, refs):
    res = {}
    for m in v3.METHODS:
        x = [r for r in rows if r["method"] == m]
        if x:
            res[m] = metrics.over_repeats(x)
            if m in v3.LLM:
                res[m]["agreement"] = metrics.agreement(x)
    for k, v in refs.items():
        res[k] = metrics.over_repeats(v)
    return res


def evaluate_all():
    _, lab = labels_report()
    if not lab["complete"]:
        sys.exit("labels incomplete")
    v3_labels = json.loads((V3_OUT / "labels.json").read_text())["labels"]
    old, good_old = score_set("v3", v3_labels)
    new, good_new = score_set("v31", lab["labels"])
    keep = [r for r in old if not r.get("missing") and r["cls"] in ("accept_clean", "decline")]
    done_new = [r for r in new if not r.get("missing")]
    rows = keep + done_new
    (OUT / "scores.json").write_text(json.dumps(done_new, indent=1, default=str))
    rods31 = ([(rid, v["class"]) for rid, v in v3_labels.items() if v["class"] in ("accept_clean", "decline")]
              + [(rid, v["class"]) for rid, v in lab["labels"].items()])
    good = {**good_old, **good_new}
    refs = {p: metrics.reference_runs(rods31, p, good) for p in ("all_decline", "all_accept")}
    res31 = results_of(rows, refs)
    rods3 = [(rid, v["class"]) for rid, v in v3_labels.items()]
    res3 = results_of([r for r in old if not r.get("missing")],
                      {p: metrics.reference_runs(rods3, p, good_old) for p in ("all_decline", "all_accept")})
    (OUT / "metrics.json").write_text(json.dumps({"v3.1": res31, "v3": res3}, indent=1, default=str))
    cnt = lambda rods: ", ".join(f"{c} {sum(v == c for _, v in rods)}" for c in metrics.CLASSES)
    L = ["# Freeze v3.1 scored runs: metrics", "",
         f"v3.1: {len(rods31)} rods ({cnt(rods31)}): v3 accept_clean and decline runs (seeds 20-22) and the new "
         f"accept_repaired runs (seeds 23-25). v3: {len(rods3)} rods ({cnt(rods3)}), recomputed from the v3 runs. "
         "LLM methods 3 repeats; mean over repeats, (min-max) where they differ. Code `measure/metrics.py`.", ""]
    L += method_table(res31, "v3.1") + [""] + method_table(res3, "v3 (unchanged runs)")
    L += ["", "## Side by side: balanced accuracy and accept_repaired accuracy", "",
          "| Method | v3 balanced | v3.1 balanced | v3 accept_repaired | v3.1 accept_repaired | v3 false accepts | v3.1 false accepts |",
          "| :-- | :-- | :-- | :-- | :-- | --: | --: |"]
    for m in res31:
        a, b = res3.get(m), res31[m]
        L.append(f"| {m} | {v3._f(a['balanced_accuracy']) if a else '-'} | {v3._f(b['balanced_accuracy'])} | "
                 f"{v3._f(a['accuracy_per_class']['accept_repaired']) if a else '-'} | "
                 f"{v3._f(b['accuracy_per_class']['accept_repaired'])} | {v3._f(a['false_accepts'], 1) if a else '-'} | "
                 f"{v3._f(b['false_accepts'], 1)} |")
    L += ["", "## Agreement across repeats (LLM methods, v3.1)", "",
          "| Method | Rods | Unanimous | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |",
          "| :-- | --: | --: | :-- | :-- | :-- | :-- | :-- |"]
    for m in v3.LLM:
        if m in res31:
            g = res31[m]["agreement"]
            u = g["unanimity_rate_per_class"]
            L.append(f"| {m} | {g['rods']} | {g['unanimous']} | {v3._f(g['unanimity_rate'])} | {v3._f(u['accept_clean'])} | "
                     f"{v3._f(u['accept_repaired'])} | {v3._f(u['decline'])} | {v3._f(g['fleiss_kappa'], 3)} |")
    L += ["", "## Per row, new accept_repaired rods (correct runs / runs)", "",
          "| Row | Size | " + " | ".join(v3.METHODS) + " |", "| :-- | :-- | " + " | ".join(":--" for _ in v3.METHODS) + " |"]
    sizes = json.loads((OUT / "sizing.json").read_text())["sizes"]
    for f, z in sizes.items():
        x = [r for r in done_new if r["kind"] == f]
        if x:
            L.append(f"| {f} | {z} | " + " | ".join(
                f"{sum(metrics.correct(r) for r in x if r['method'] == m)} / {sum(r['method'] == m for r in x)}"
                for m in v3.METHODS) + " |")
    L += ["", "## Categories on the new rods (summed over repeats)", "",
          "| Method | " + " | ".join(metrics.CATEGORIES) + " | Fault named correct |",
          "| :-- | " + " | ".join("--:" for _ in metrics.CATEGORIES) + " | :-- |"]
    for m in v3.METHODS:
        x = [r for r in done_new if r["method"] == m]
        if x:
            fc = [r["fault_correct"] for r in x if r["fault_correct"] is not None]
            L.append(f"| {m} | " + " | ".join(str(sum(r["category"] == c for r in x)) for c in metrics.CATEGORIES)
                     + f" | {sum(map(bool, fc))} of {len(fc)} |")
    L += ["", "## Cost, new rods (all repeats)", "", "| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |",
          "| :-- | --: | --: | --: | --: | --: |"]
    for m in v3.METHODS:
        x = [r for r in done_new if r["method"] == m]
        if x:
            L.append(f"| {m} | {len(x)} | {sum(r['steps'] for r in x)} | {sum(r['tokens_in'] for r in x)} | "
                     f"{sum(r['tokens_out'] for r in x)} | {sum(r['call_s'] for r in x):.1f} |")
    miss = [r for r in new if r.get("missing")]
    if miss:
        L += ["", f"Not run: {len(miss)}"]
    L += ["", "## Per run, new rods", "",
          "| Method | Rod | Repeat | Class | Status | Category | Named fault | Steps | Remedies | Centre RMS (tol) | Flank RMS |",
          "| :-- | :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: |"]
    for r in done_new:
        L.append(f"| {r['method']} | {r['rod']} | {r['repeat']} | {r['cls']} | {r['status']} | {r['category']} | "
                 f"{r['named_fault'] or '-'} | {r['steps']} | {'; '.join(r['remedies']) or 'none'} | "
                 f"{r['regr_rms']} ({r['regr_tol']}) | {r['flank_rms']} |")
    (OUT / "table_metrics.md").write_text("\n".join(L) + "\n")
    print("\n".join(L).split("\n## Agreement")[0])


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "status", "fetch", "sizing", "labels", "rules", "agents",
                                    "second-root", "eval"])
    ap.add_argument("--phase", choices=["sizing", "labels", "methods"])
    ap.add_argument("--method", choices=v3.LLM)
    ap.add_argument("--repeat", type=int, choices=v3.REPEATS)
    ap.add_argument("--max-runs", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    point_v3_at("v31")
    if a.cmd == "plan":
        if not a.phase:
            ap.error("--phase is required")
        if a.phase != "sizing" and not (OUT / "sizing.json").exists():
            sys.exit("sizing.json missing: run sizing first")
        need = {"sizing": lambda: sizing_rows()[1], "labels": v3.need_labels, "methods": v3.need_methods}[a.phase]()
        v3.start_sweep(need, a.dry_run)
    elif a.cmd in ("status", "fetch"):
        if a.cmd == "status":
            st = RemoteRunner(v3.runner_config(), cache=CACHE).sweep_status(SWEEP)
            log = st.pop("log")
            print(json.dumps(st))
            runs = [x for x in log if "tag" in x]
            print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
            for x in log:
                if "tag" not in x:
                    print(json.dumps(x))
        else:
            r = RemoteRunner(v3.runner_config(), cache=CACHE)
            if r.sweep_status(SWEEP).get("running"):
                sys.exit("a sweep is running; fetch after it ends")
            st = r.sweep_status(SWEEP)
            CACHE.mkdir(parents=True, exist_ok=True)
            with (CACHE / "sweeps.jsonl").open("a") as f:
                for x in st["log"]:
                    if "tag" not in x:
                        f.write(json.dumps(x) + "\n")
            r.sweep_fetch(TRACKS, CACHE)
            print(f"fetched: {v3.tracker_runs_cached()} new tracker outputs in the cache (cap {MAX_NEW})")
    elif a.cmd == "sizing":
        text, info = sizing_report()
        (OUT / "sizing.md").write_text(text)
        if info["complete"]:
            (OUT / "sizing.json").write_text(json.dumps({"sizes": info["sizes"], "stop": info["stop"]}, indent=1))
        print(text.split("## Per state")[0])
    elif a.cmd == "labels":
        text, info = labels_report()
        (OUT / "labels.md").write_text(text)
        if info["complete"]:
            (OUT / "labels.json").write_text(json.dumps(info, indent=1, default=str))
        print(text.split("## Per state")[0])
    elif a.cmd == "rules":
        v3.run_rules()
    elif a.cmd == "agents":
        if a.method is None or a.repeat is None:
            ap.error("--method and --repeat are required")
        v3.run_agents(a.method, a.repeat, a.max_runs)
    elif a.cmd == "second-root":
        text, _ = second_root_note()
        (OUT / "second_root.md").write_text(text)
        print(text)
    else:
        evaluate_all()


if __name__ == "__main__":
    main()
