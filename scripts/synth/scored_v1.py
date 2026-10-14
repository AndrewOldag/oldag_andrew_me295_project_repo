"""Scored runs v1 (spec 2026-10-12b, items 5-7): four methods on the development and held-out faults.

  python scripts/synth/scored_v1.py next   --set dev|heldout [--dry-run]   # tracker runs the two rule methods still need, as one sweep
  python scripts/synth/scored_v1.py status
  python scripts/synth/scored_v1.py fetch                                  # to staging/tracks_scored_v1/
  python scripts/synth/scored_v1.py rules  --set dev|heldout               # script and remedy tree, from the cache
  python scripts/synth/scored_v1.py agents --set dev|heldout --method diagnostician|single_agent
  python scripts/synth/scored_v1.py eval

Sets: dev = the five development faults at their frozen sizes, scoring seeds (config/scoring_seeds.yaml);
heldout = the five held-out faults at the approved sizes, seeds 0-2.
Methods: script and remedy_tree (agents/baselines.py), diagnostician (Slice), single_agent (BlindSlice;
docs/proposals/2026-10-12_single-agent-baseline.md). Every method acts on the same rod and runner code.
Tracker outputs: read from this spec's cache and from the 2026-10-12 caches (baselines, seeds 3-5, held-out
sizes and labels), all made with the current tracking code. The rule methods are deterministic and run in
rounds: missing runs go out as one sweep (scripts/synth/sweep.py limits and lock). The agents run their
missing runs as single load-checked jobs at lowest priority (measure/runner.py).
Each run writes <method>_<fault>[_z<size>]_s<seed>_trace.jsonl and _summary.json under
results/2026-10-12b_scored_v1/<set>/ with the freeze tag, commit, method, outcome, steps, remedies, roll
backs, tokens and call time. Runs with a summary are skipped. Agent runs need a clean tracked tree.
"""
import argparse
import json
import subprocess
import sys
import time
import traceback
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents.baselines import run_script, run_tree  # noqa: E402
from agents.executors import BlindSlice, Slice  # noqa: E402
from agents.launcher import load_config  # noqa: E402
from fix_sweep import entry  # noqa: E402
from heldout_labels import APPROVED  # noqa: E402
from heldout_sweep import config as runner_config  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import Measurement, RemoteRunner, Rod  # noqa: E402
from measure.score import (diagnosis_correct, load_tolerance, measurement_good, outcome_category,  # noqa: E402
                           rod_tolerance, truth_error, truth_summary)

FREEZE_TAG = "freeze-v2"
OUT = ROOT / "results" / "2026-10-12b_scored_v1"
ST = ROOT / "staging"
CACHE = ST / "tracks_scored_v1"
TRACKS, SWEEP = "tracks_scored_v1", "scored_v1"
READ = [CACHE, ST / "tracks_baselines", ST / "tracks_2026-10-12" / "tracks_freeze", ST / "tracks_heldout",
        ST / "tracks_heldout_labels"]
MAX_SWEEP_RUNS = 300
PIXEL_UM = 2.105
# development faults at their frozen sizes (freeze v2); None = the default size, which has two ids in the caches
DEV = {"displacement_exceeds_patch": "2x6", "width_change": None, "rigid_drift": "0.5", "low_texture": None,
       "midline_jitter": None}
DEFAULT_SIZE = {"low_texture": "0.03", "midline_jitter": "3"}
DEV_LABEL = {"displacement_exceeds_patch": "repairable", "width_change": "repairable", "rigid_drift": "repairable",
             "low_texture": "not repairable", "midline_jitter": "not repairable"}     # freeze v2, seeds 0-5
# fault names counted correct (held-out: spec 2026-10-12b decisions and the held-out proposal, section 2)
NAMES = {f: {f} for f in DEV} | {"second_root": {"second_root"}, "fast_rotation": {"fast_rotation"},
                                 "bad_stage_correction": {"bad_stage_correction"}, "flank_swap": {"unknown"},
                                 "partial_occlusion": {"low_texture", "unknown"}}
METHODS = ("script", "remedy_tree", "diagnostician", "single_agent")
CORRECT = {"repairable": "good_report", "not repairable": "correct_decline"}


def seeds(set_):
    if set_ == "heldout":
        return (0, 1, 2)
    return tuple(yaml.safe_load((ROOT / "config" / "scoring_seeds.yaml").read_text())["scoring_seeds"])


def rods(set_):
    faults = DEV if set_ == "dev" else APPROVED
    return [Rod("growth_zone", f, s, size=z) for f, z in faults.items() for s in seeds(set_)]


def stem(method, rod):
    return f"{method}_{rod.fault}" + (f"_z{rod.size}" if rod.size else "") + f"_s{rod.seed}"


def ids(rod, moved=False):
    out = [rod.id(moved)]
    if rod.size is None and rod.fault in DEFAULT_SIZE:
        out.append(replace(rod, size=DEFAULT_SIZE[rod.fault]).id(moved))
    return out


def find(name_of, rod, moved=False):
    for d in READ:
        for i in ids(rod, moved):
            f = d / name_of(i)
            if f.exists():
                return f
    return None


def load_truth(rod):
    f = find(lambda i: f"{i}_truth.npz", rod)
    if f is None:
        return None
    with np.load(f) as z:
        return {k: z[k] for k in z.files}


class Missing(Exception):
    def __init__(self, rod, settings):
        super().__init__(f"{rod.id()} {settings.tag()}")
        self.rod, self.settings = rod, settings


class ScoredRunner(RemoteRunner):
    """Measurements from the caches. remote=False: a run not cached raises Missing. remote=True: it is run as
    a single job on the tracker machine (render if needed, track, fetch to CACHE)."""

    def __init__(self, remote=False):
        self.remote, self.log, self.cache, self.couple = remote, [], CACHE, False
        if remote:
            super().__init__(runner_config(), cache=CACHE)

    @staticmethod
    def initial_stride(rod):
        """The rod's own analysis stride; held-out rods from measure/render_heldout.py."""
        from measure import render, render_heldout
        mod = render_heldout if rod.fault in APPROVED else render
        _, movie = mod.image_case(rod.case, rod.fault, rod.seed, False, size=rod.size)
        return movie.stride

    def measure(self, rod, settings):
        st = replace(settings, width_free=False)
        files = [find(lambda i: f"{i}__{st.tag()}.npz", rod, m) for m in (False, True)]
        truth = load_truth(rod)
        if None in files or truth is None:
            if not self.remote:
                raise Missing(rod, st)
            rid, rid_m = self.render(rod), self.render(rod, moved=True)
            files = [files[0] or self.track(rid, st), files[1] or self.track(rid_m, st)]
            truth = truth if truth is not None else self.truth(rid)
        return Measurement(from_tracker_npz(files[0]), from_tracker_npz(files[1]), settings, truth)


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def write_summary(path, rod, sl, outcome, method, extra):
    first, last = sl.runs[0][1], sl.current
    s = {"freeze_tag": FREEZE_TAG, "commit": git("rev-parse", "--short", "HEAD"), "method": method,
         "rod": {"case": rod.case, "fault": rod.fault, "size": rod.size, "seed": rod.seed}, "runner": "remote_job",
         "truth": truth_summary(first.truth, first.record.pixel_um),
         "error_before": truth_error(first.record, first.truth),
         "initial_checks": [c.to_dict() for c in sl.runs[0][2]],
         "outcome": outcome.__dict__, "error_after": truth_error(last.record, last.truth),
         "remedies": [ch for _, _, _, ch in sl.runs[1:]],
         "roll_backs": sum(ch.startswith("rolled back") for _, _, _, ch in sl.runs[1:]),
         "final_settings": sl.runs[-1][0].to_dict(), "final_checks": [c.to_dict() for c in sl.checks],
         "reported": outcome.status == "accept", **extra}
    path.write_text(json.dumps(s, indent=1, default=str))


# ------------------------------------------------------------------ rule methods

RULES = {"script": lambda sl, trace: run_script(sl, trace),
         "remedy_tree": lambda sl, trace: run_tree(sl, load_config()["agents"]["diagnostician"]["step_limit"], trace)}


def rules_round(set_, write=False):
    """Script and tree on every rod of the set from the cache. Returns {(id, tag): (rod, settings)} still needed."""
    need, out = {}, OUT / set_
    for rod in rods(set_):
        for m, fn in RULES.items():
            trace = out / f"{stem(m, rod)}_trace.jsonl" if write else None
            if trace:
                out.mkdir(parents=True, exist_ok=True)
                trace.unlink(missing_ok=True)
            try:
                sl = Slice(ScoredRunner(), rod)
                o = fn(sl, trace)
            except Missing as e:
                need[(e.rod.id(), e.settings.tag())] = (e.rod, e.settings)
                continue
            if write:
                write_summary(out / f"{stem(m, rod)}_summary.json", rod, sl, o, m, {})
    return need


# ------------------------------------------------------------------ agents

def run_agents(set_, method):
    from agents.launcher import Launcher
    from agents.orchestrator import Orchestrator
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files are modified; commit first (each run records the commit)")
    out = OUT / set_
    out.mkdir(parents=True, exist_ok=True)
    launcher = Launcher()
    cls = {"diagnostician": Slice, "single_agent": BlindSlice}[method]
    errors = []
    for rod in rods(set_):
        name = stem(method, rod)
        summ, trace = out / f"{name}_summary.json", out / f"{name}_trace.jsonl"
        if summ.exists():
            continue
        trace.unlink(missing_ok=True)
        runner = ScoredRunner(remote=True)
        t0 = time.time()
        try:
            sl = cls(runner, rod)
            o = Orchestrator(launcher, trace).run(method, sl.label, sl.task(), sl.executors())
        except Exception as e:                          # harness error: logged, the run has no summary
            errors.append(name)
            with (out / "harness_errors.jsonl").open("a") as f:
                f.write(json.dumps({"run": name, "error": f"{type(e).__name__}: {e}",
                                    "traceback": traceback.format_exc()[-2000:]}) + "\n")
            print(f"{name}: HARNESS ERROR {type(e).__name__}: {e}", flush=True)
            continue
        tracker = [x["track"] for x in runner.log if "track" in x]
        write_summary(summ, rod, sl, o, method, {"claude_code": launcher.version, "wall_s": round(time.time() - t0, 1),
                                                 "tracker_runs_new": len(tracker), "runner_log": runner.log})
        print(f"{name}: {o.status} {o.args.get('fault', '')} steps {o.steps} tokens {o.input_tokens}/{o.output_tokens} "
              f"call {o.call_ms / 1000:.1f} s; new tracker runs {len(tracker)}", flush=True)
    print(f"harness errors: {len(errors)} {errors}")


# ------------------------------------------------------------------ scoring

def named_fault(trace):
    name = None
    for line in trace.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        act = d.get("action") or {}
        if act.get("name") in ("apply_remedy", "decline") and d.get("status") in ("executed", "terminal"):
            name = act["args"].get("fault")
    return name


def labels(set_):
    if set_ == "dev":
        return {r.id(): DEV_LABEL[r.fault] for r in rods(set_)}
    js = json.loads((ROOT / "results" / "2026-10-12b_heldout_labels" / "labels.json").read_text())
    return {x["rod"]: x["label"] for x in js}


def score_set(set_, cfg):
    lab, rows = labels(set_), []
    for rod in rods(set_):
        tol = rod_tolerance(load_truth(rod), PIXEL_UM, cfg)
        for m in METHODS:
            f = OUT / set_ / f"{stem(m, rod)}_summary.json"
            if not f.exists():
                rows.append({"method": m, "fault": rod.fault, "seed": rod.seed, "missing": True})
                continue
            s = json.loads(f.read_text())
            o = s["outcome"]
            good = measurement_good(s["error_after"], tol, bool(s["final_settings"].get("width_free")))
            cat = outcome_category(o["status"], lab[rod.id()], good)
            nf = named_fault(f.with_name(f.name.replace("_summary.json", "_trace.jsonl")))
            rows.append({"set": set_, "method": m, "fault": rod.fault, "size": rod.size, "seed": rod.seed,
                         "label": lab[rod.id()], "status": o["status"], "category": cat,
                         "correct": cat == CORRECT[lab[rod.id()]], "named_fault": nf,
                         "fault_correct": nf in NAMES[rod.fault] if set_ == "heldout" else diagnosis_correct(nf, rod.fault),
                         "steps": o["steps"], "failed_steps": o.get("failed_steps", 0),
                         "remedies": s["remedies"], "roll_backs": s["roll_backs"],
                         "tokens_in": o.get("input_tokens", 0), "tokens_out": o.get("output_tokens", 0),
                         "call_s": round(o.get("call_ms", 0) / 1000, 1), "good": good,
                         "regr_rms": s["error_after"].get("regr_rms_pct_per_h"),
                         "flank_rms": s["error_after"].get("flank_difference_rms_pct_per_h"),
                         "regr_tol": round(tol["regr_rms_pct_per_h"], 3), "commit": s.get("commit"),
                         "freeze_tag": s.get("freeze_tag"), "claude_code": s.get("claude_code"),
                         "tracker_runs_new": s.get("tracker_runs_new")})
    return rows


def tables(set_, rows):
    faults = list(DEV if set_ == "dev" else APPROVED)
    rs = [r for r in rows if not r.get("missing")]
    n_seeds = len(seeds(set_))
    L = [f"## {'Development' if set_ == 'dev' else 'Held-out'} faults, seeds {', '.join(map(str, seeds(set_)))}", "",
         "Cells: correct outcomes / false accepts / unnecessary declines / terminal fault correct, "
         f"each out of {n_seeds}.", "",
         "| Fault | Label | " + " | ".join(METHODS) + " |", "| :-- | :-- | " + " | ".join(":--" for _ in METHODS) + " |"]
    for f in faults:
        labs = sorted({r["label"] for r in rs if r["fault"] == f})
        cells = []
        for m in METHODS:
            x = [r for r in rs if r["fault"] == f and r["method"] == m]
            cells.append(f"{sum(r['correct'] for r in x)} / {sum(r['category'] == 'false_accept' for r in x)} / "
                         f"{sum(r['category'] == 'unnecessary_decline' for r in x)} / "
                         f"{sum(bool(r['fault_correct']) for r in x)}" + ("" if len(x) == n_seeds else f" (of {len(x)})"))
        L.append(f"| {f} | {', '.join(labs)} | " + " | ".join(cells) + " |")
    L += ["", "| Method | Runs | Correct | good_report | false_accept | correct_decline | unnecessary_decline | "
              "not_reported | Terminal fault correct | Steps | Remedies kept | Roll backs | Tokens in | Tokens out | "
              "Call time (s) |", "| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |"]
    for m in METHODS:
        x = [r for r in rs if r["method"] == m]
        c = [sum(r["category"] == k for r in x) for k in ("good_report", "false_accept", "correct_decline",
                                                          "unnecessary_decline", "not_reported")]
        L.append(f"| {m} | {len(x)} | {sum(r['correct'] for r in x)} | " + " | ".join(map(str, c))
                 + f" | {sum(bool(r['fault_correct']) for r in x)} | {sum(r['steps'] for r in x)} | "
                 f"{sum(len(r['remedies']) - 2 * r['roll_backs'] for r in x)} | {sum(r['roll_backs'] for r in x)} | "
                 f"{sum(r['tokens_in'] for r in x)} | {sum(r['tokens_out'] for r in x)} | "
                 f"{sum(r['call_s'] for r in x):.1f} |")
    L += ["", "Per run:", "", "| Method | Fault | Seed | Label | Status | Category | Named fault | Fault correct | Steps | "
          "Remedies | Roll backs | Tokens in / out | Call (s) | Centre RMS (tol) | Flank RMS |",
          "| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- | --: | :-- | --: | :-- | --: | :-- | --: |"]
    for r in sorted(rs, key=lambda r: (METHODS.index(r["method"]), faults.index(r["fault"]), r["seed"])):
        L.append(f"| {r['method']} | {r['fault']} | {r['seed']} | {r['label']} | {r['status']} | {r['category']} | "
                 f"{r['named_fault'] or '-'} | {'yes' if r['fault_correct'] else 'no'} | {r['steps']} | "
                 f"{'; '.join(r['remedies']) or 'none'} | {r['roll_backs']} | {r['tokens_in']} / {r['tokens_out']} | "
                 f"{r['call_s']} | {r['regr_rms']} ({r['regr_tol']}) | {r['flank_rms']} |")
    missing = [r for r in rows if r.get("missing")]
    if missing:
        L += ["", f"Not run: {len(missing)}: " + ", ".join(f"{r['method']} {r['fault']} s{r['seed']}" for r in missing)]
    return "\n".join(L) + "\n"


def evaluate():
    cfg = load_tolerance()
    allrows = []
    for set_ in ("dev", "heldout"):
        rows = score_set(set_, cfg)
        allrows += rows
        (OUT / f"table_{set_}.md").write_text(tables(set_, rows))
        print(tables(set_, rows).split("\nPer run:")[0])
    (OUT / "scores.json").write_text(json.dumps(allrows, indent=1, default=str))


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["next", "status", "fetch", "rules", "agents", "eval"])
    ap.add_argument("--set", choices=["dev", "heldout"])
    ap.add_argument("--method", choices=["diagnostician", "single_agent"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd in ("next", "rules", "agents") and not a.set:
        ap.error("--set is required")
    if a.cmd == "next":
        need = rules_round(a.set)
        n_new, n_have = 2 * len(need), len(list(CACHE.glob("*__*.npz"))) if CACHE.exists() else 0
        print(f"tracker runs in this spec's cache {n_have}; needed now {n_new}")
        for rid, tag in sorted(need):
            print(f"  {rid} {tag}")
        if not need or a.dry_run:
            return
        if n_have + n_new > MAX_SWEEP_RUNS:
            sys.exit(f"stop: {n_have + n_new} tracker runs would pass {MAX_SWEEP_RUNS}; ask Andrew")
        r = RemoteRunner(runner_config(), cache=CACHE)
        if r.sweep_status().get("running"):
            sys.exit("a sweep is running; wait and try again")
        by_rod = {}
        for rod, st in need.values():
            by_rod.setdefault(rod, []).append(st)
        r.sweep_start({"rods": [entry(rod, sts) for rod, sts in by_rod.items()]}, SWEEP, tracks=TRACKS)
        print(f"started: {len(by_rod)} rods, {n_new} tracker runs")
    elif a.cmd == "status":
        st = RemoteRunner(runner_config(), cache=CACHE).sweep_status(SWEEP)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "fetch":
        r = RemoteRunner(runner_config(), cache=CACHE)
        st = r.sweep_status(SWEEP)
        if st.get("running"):
            sys.exit("a sweep is running; fetch after it ends")
        CACHE.mkdir(parents=True, exist_ok=True)
        with (CACHE / "sweeps.jsonl").open("a") as f:
            for x in st["log"]:
                if "tag" not in x:
                    f.write(json.dumps(x) + "\n")
        r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched: {len(list(CACHE.glob('*__*.npz')))} tracker outputs")
    elif a.cmd == "rules":
        need = rules_round(a.set, write=True)
        if need:
            sys.exit(f"{len(need)} runs still needed; run `next` first")
        print(f"wrote rule-method runs for {a.set}")
    elif a.cmd == "agents":
        run_agents(a.set, a.method)
    else:
        evaluate()


if __name__ == "__main__":
    main()
