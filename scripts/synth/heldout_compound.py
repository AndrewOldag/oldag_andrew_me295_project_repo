"""Held-out compound and novel faults (spec 2026-11-18, section D; task c029). VM only: renders and
tracker runs on this machine (scripts/synth/local_qb.py), no lab server, no cluster.

  python scripts/synth/heldout_compound.py sizing-sweep [--dry-run]   # novel faults, sizing seeds, unremedied
  python scripts/synth/heldout_compound.py sizing                     # sizing.md; sizing.json when complete
  python scripts/synth/heldout_compound.py label-sweep [--dry-run]    # every remedy and pair, 24 rods
  python scripts/synth/heldout_compound.py labels                     # labels.md; labels.json when complete
  python scripts/synth/heldout_compound.py rules                      # fixed script and remedy tree
  python scripts/synth/heldout_compound.py agents --method M --repeat K [--max-runs N]
  python scripts/synth/heldout_compound.py eval                       # table_metrics.md, metrics.json, scores.json

The freeze v3 driver (scored_v3.py) pointed at this set, as scored_v4.py points it at v4: candidate v4 on,
freeze v4 prompts, pinned model. Proposal: docs/proposals/2026-11-18_heldout-compound.md.
Local tracker: private/local_tracker.yaml (`python`: the tracker env's interpreter), tracker source in
staging/qb_tracker. Renders in staging/rods_c029, tracks in staging/tracks_c029 (git-ignored).
Before each tracker run and each LLM run: free VM memory at least MIN_FREE_GB, else wait.
"""
import argparse
import ctypes
import json
import subprocess
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from itertools import combinations
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scored_v3 as v3  # noqa: E402
from agents import candidate  # noqa: E402
from agents.actions import REMEDIES  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import NotAvailable, TrackSettings, apply_remedy  # noqa: E402
from measure.render_compound import COMPOUND, NOVEL  # noqa: E402
from measure.runner import Measurement, Rod  # noqa: E402

FREEZE_TAG = "freeze-v4"                      # prompts and agents of freeze v4 (spec D3)
OUT = ROOT / "results" / "2026-11-18_heldout_compound"
CACHE = ROOT / "staging" / "tracks_c029"
RODS = ROOT / "staging" / "rods_c029"
GZ = "v3_growth_zone"
SCORING_SEEDS = (40, 41, 42, 43)              # not used before (proposal, section 2)
SIZING_SEEDS = (50, 51)
NOVEL_CANDIDATES = {"focus_drift": ("3", "6"), "illumination_flicker": ("0.1", "0.3")}
MAX_LLM_RUNS = 450                            # spec D3
MAX_TRACKER_RUNS = 3000                       # local runs; label sweep about 1,400 (proposal, section 4)
MIN_FREE_GB = 3.0                             # before each batch: one rod's runs, or one LLM run (spec 2026-11-18)
RUN_FLOOR_GB = 2.0                            # before each tracker run inside a batch (decisions, 2026-11-20)
WORKERS = 2
# fault names counted correct (reported, not a main metric): any component's name; unknown for the novel faults
NAMES = {"drift_low_texture": {"rigid_drift", "low_texture"},
         "second_root_occlusion": {"second_root", "low_texture", "unknown"},
         "drift_jitter": {"rigid_drift", "midline_jitter"},
         "low_texture_fast": {"low_texture", "displacement_exceeds_patch"},
         "focus_drift": {"low_texture", "unknown"},
         "illumination_flicker": {"unknown", "low_texture"}}
# expected class written before the labels (proposal, section 3); the label sweep decides
EXPECTED = {f: "decline" for f in COMPOUND} | {"focus_drift": "decline", "illumination_flicker": "accept_clean"}


# ------------------------------------------------------------------ rods

def novel_sizes():
    f = OUT / "sizing.json"
    return json.loads(f.read_text())["sizes"] if f.exists() else None


def scored_rods():
    sizes = novel_sizes()
    if sizes is None:
        sys.exit("novel-fault sizes not set: run sizing-sweep, then sizing")
    out = [Rod(GZ, f, s) for f in COMPOUND for s in SCORING_SEEDS]
    return out + [Rod(GZ, f, s, size=sizes[f]) for f in NOVEL for s in SCORING_SEEDS]


def sizing_rods():
    return [Rod(GZ, f, s, size=z) for f, zs in NOVEL_CANDIDATES.items() for z in zs for s in SIZING_SEEDS]


def initial(rod):
    from measure import render_compound
    _, movie = render_compound.image_case(rod.case, rod.fault, rod.seed, False, size=rod.size)
    return TrackSettings(stride=movie.stride)


# ------------------------------------------------------------------ label states: every remedy and pair

def steps():
    """Every single remedy step of the action schema, in schema order: [(remedy, setting)]."""
    return [(r, s) for r, ss in REMEDIES.items() for s in ss]


def step_name(r, s):
    return r if s is None else f"{r}/{s}"


def label_states(rod):
    """[(sequence, TrackSettings or None)]: unremedied, every single step, every pair of steps of two different
    remedies (schema order: register_frames first, so its band start is read from the unremedied run). A step
    the remedy code refuses (NotAvailable, e.g. half the stride at stride 1) gives no state. None until the
    unremedied run is cached (band start, base disk radius)."""
    base = initial(rod)
    out = [([], base)]
    if not v3.cached(rod, base):
        rec, radius = None, None
    else:
        rec = from_tracker_npz(v3.out_file(rod, base))
        radius = int(rec.settings.get("disk_radius") or 15)
    seqs = [[a] for a in steps()] + [[a, b] for a, b in combinations(steps(), 2) if a[0] != b[0]]
    for seq in seqs:
        names = [step_name(*x) for x in seq]
        if rec is None:
            out.append((names, None))
            continue
        st = base
        try:
            for r, s in seq:
                st, _ = apply_remedy(st, r, s, radius, rec)
        except NotAvailable:
            continue
        out.append((names, st))
    return out


def tracked(states):
    """Distinct tracker settings of a state list (width_free needs no tracker run)."""
    return list({replace(st, width_free=False).tag(): replace(st, width_free=False)
                 for _, st in states if st is not None}.values())


# ------------------------------------------------------------------ local renders and tracker runs

def private_config():
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()
    for p in (ROOT / "private" / "local_tracker.yaml",
              (ROOT / common).resolve().parent / "private" / "local_tracker.yaml"):
        if p.exists():
            return yaml.safe_load(p.read_text())
    sys.exit("private/local_tracker.yaml missing (key python: the tracker env's interpreter)")


def free_gb():
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = MS()
    m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2 ** 30


def wait_memory(floor=MIN_FREE_GB):
    while (f := free_gb()) < floor:
        print(f"free VM memory {f:.2f} GB, under {floor} GB; waiting 60 s", flush=True)
        time.sleep(60)


def tracker_runs_cached():
    return len(list(CACHE.glob("*__*.npz.ok"))) if CACHE.exists() else 0


class LocalRunner(v3.V3Runner):
    """Measurements from CACHE. remote=False: a run not cached raises v3.Missing. remote=True: the rod is
    rendered and tracked on this machine and the output lands in CACHE (scripts/synth/local_qb.py)."""

    def __init__(self, remote=False):
        self.remote, self.log, self.cache, self.couple = remote, [], CACHE, False
        self.python = private_config()["python"] if remote else None
        if remote:
            wait_memory()                      # one per rule or agent run: MIN_FREE_GB before each run

    def _run(self, script, args):
        wait_memory(RUN_FLOOR_GB)
        p = subprocess.run([self.python, str(ROOT / "scripts" / "synth" / "local_qb.py"), str(ROOT / script)] + args,
                           capture_output=True, text=True, cwd=ROOT)
        if p.returncode != 0:
            raise RuntimeError(f"{Path(script).name} failed: {(p.stderr or p.stdout).strip().splitlines()[-1:]}")
        return json.loads(p.stdout.strip().splitlines()[-1])

    def render(self, rod, moved=False):
        rid = rod.id(moved)
        if (RODS / f"{rid}.ok").exists():
            return rid
        if (RODS / f"{rid}.imgdir").exists():          # a stopped render (VM staging, this task's own files)
            import shutil
            shutil.rmtree(RODS / f"{rid}.imgdir")
            for f in (RODS / f"{rid}_midline.npz", RODS / f"{rid}_truth.npz"):
                f.unlink(missing_ok=True)
        RODS.mkdir(parents=True, exist_ok=True)
        out = self._run("scripts/synth/make_rod.py", ["--out", str(RODS)] + rod.options() + (["--moved"] if moved else []))
        self.log.append({"render": out})
        if not moved and not (CACHE / f"{rid}_truth.npz").exists():
            CACHE.mkdir(parents=True, exist_ok=True)
            (CACHE / f"{rid}_truth.npz").write_bytes((RODS / f"{rid}_truth.npz").read_bytes())
        return rid

    def track(self, rid, settings):
        settings = replace(settings, width_free=False)
        out = CACHE / f"{rid}__{settings.tag()}.npz"
        if Path(f"{out}.ok").exists():
            return out
        if out.exists():
            out.unlink()                       # local output of a stopped run (VM staging, this task's own file)
        CACHE.mkdir(parents=True, exist_ok=True)
        if tracker_runs_cached() >= MAX_TRACKER_RUNS:
            raise RuntimeError(f"tracker-run cap {MAX_TRACKER_RUNS} reached")
        r = self._run("scripts/remote/qb_track.py",
                      ["--imgdir", str(RODS / f"{rid}.imgdir"), "--midline", str(RODS / f"{rid}_midline.npz"),
                       "--out", str(out)] + settings.args())
        r["out"] = out.name
        self.log.append({"track": r})
        with (CACHE / "runs.jsonl").open("a") as f:
            f.write(json.dumps({"rid": rid, "tag": settings.tag(), "run_s": r.get("run_s"), "time": time.strftime("%F %T")}) + "\n")
        return out

    def measure(self, rod, settings):
        st = replace(settings, width_free=False)
        if not v3.cached(rod, st) or v3.truth(rod) is None:
            if not self.remote:
                raise v3.Missing(rod, st)
            rid, rid_m = self.render(rod), self.render(rod, moved=True)
            self.track(rid, st), self.track(rid_m, st)
        return Measurement(from_tracker_npz(v3.out_file(rod, st)), from_tracker_npz(v3.out_file(rod, st, True)),
                           settings, v3.truth(rod))


def cached(rod, st):
    st = replace(st, width_free=False)
    return all(Path(f"{v3.out_file(rod, st, m)}.ok").exists() for m in (False, True))


def sweep(jobs, dry, label):
    """jobs: [(rod, TrackSettings)]; each tracked as is and rigidly moved. Renders first, then runs, WORKERS at once.
    Restartable: cached runs are skipped."""
    todo = [(r, st) for r, st in {(r.id(), replace(st, width_free=False).tag()): (r, replace(st, width_free=False))
                                  for r, st in jobs}.values() if not cached(r, st)]
    rods = list({r.id(): r for r, _ in todo}.values())
    print(f"{label}: {len(todo)} states to run ({2 * len(todo)} tracker runs), {len(rods)} rods; "
          f"cached runs {tracker_runs_cached()}; free VM memory {free_gb():.2f} GB", flush=True)
    if dry or not todo:
        return
    runner = LocalRunner(remote=True)
    t0 = time.time()
    done, failed = 0, []
    for rod in rods:                                   # one batch per rod: MIN_FREE_GB before it
        wait_memory()
        with ThreadPoolExecutor(WORKERS) as ex:
            list(ex.map(lambda m: runner.render(rod, m), (False, True)))
            fut = {ex.submit(runner.track, rod.id(m), st): (st, m) for r, st in todo if r.id() == rod.id()
                   for m in (False, True)}
            for f in as_completed(fut):
                st, m = fut[f]
                try:
                    f.result()
                    done += 1
                except Exception as e:
                    failed.append({"rod": rod.id(m), "tag": st.tag(), "error": f"{type(e).__name__}: {e}"})
                    print(f"FAILED {rod.id(m)} {st.tag()}: {e}", flush=True)
        print(f"{rod.id()}: {done} runs done, {len(failed)} failed, {time.time() - t0:.0f} s; "
              f"free {free_gb():.2f} GB", flush=True)
    with (CACHE / "sweeps.jsonl").open("a") as f:
        f.write(json.dumps({"sweep": label, "runs": done, "failed": failed, "wall_s": round(time.time() - t0),
                            "workers": WORKERS, "end": time.strftime("%F %T")}) + "\n")
    print(f"{label}: {done} runs, {len(failed)} failed, {time.time() - t0:.0f} s", flush=True)


# ------------------------------------------------------------------ sizing of the novel faults

def sizing_report():
    """Rule (proposal, section 2): per novel fault, the smallest candidate size at which the unremedied checker
    fails on both sizing seeds; if none does, the largest candidate."""
    L = ["# Novel-fault sizes", "", f"Sizing seeds {', '.join(map(str, SIZING_SEEDS))}, unremedied, {GZ}. Rule: the smallest "
         "candidate at which the checker fails on both seeds; else the largest candidate.", "",
         "| Fault | Size | Seed | rigid_invariance | closure | plane_sections | REGR err (limit) | All pass | Good |",
         "| :-- | --: | --: | --: | --: | --: | --: | :-- | :-- |"]
    sizes, complete = {}, True
    for f, zs in NOVEL_CANDIDATES.items():
        pick = None
        for z in zs:
            ev = []
            for s in SIZING_SEEDS:
                rod = Rod(GZ, f, s, size=z)
                e = v3.evaluate(rod, initial(rod)) if cached(rod, initial(rod)) else None
                if e is None:
                    complete = False
                    continue
                ev.append(e)
                L.append(f"| {f} | {z} | {s} | " + " | ".join(v3._cell(e, c) for c in v3.CHECKS)
                         + f" | {e['regr_rms_pct_per_h']:.2f} ({e['regr_limit']:.2f}) | {'yes' if e['all_pass'] else 'no'} | "
                         f"{'yes' if e['good'] else 'no'} |")
            if pick is None and len(ev) == len(SIZING_SEEDS) and all(not e["all_pass"] for e in ev):
                pick = z
        sizes[f] = pick or zs[-1]
    L += ["", f"- Sizes: {sizes}" if complete else "- Incomplete"]
    return "\n".join(L) + "\n", {"sizes": sizes, "complete": complete}


# ------------------------------------------------------------------ labels

def labels_report():
    """Per rod: accept_clean if the unremedied run passes all checks and is good; accept_repaired if a state of
    one or two steps passes and is good (the first such state in schema order is named); decline otherwise.
    measure.score.label_rod, as freeze v3/v4, with the unremedied state split out as accept_clean."""
    L = ["# Labels of the held-out compound and novel set", "",
         f"Seeds {', '.join(map(str, SCORING_SEEDS))}. Tracker only, no agent. States: unremedied, every single remedy "
         "step of the action schema and every pair of steps of two different remedies (schema order). Candidate v4 "
         "on: a check that cannot be computed after a remedy fails (C3 option a). A state is good when its centre "
         "REGR error and flank-difference error are within the scoring tolerance.", "",
         "| Rod | Expected (proposal) | Label | Repairing states (first named) | Unremedied: checks pass, good |",
         "| :-- | :-- | :-- | :-- | :-- |"]
    per = ["| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |",
           "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"]
    labels, missing = {}, 0
    for rod in scored_rods():
        sts = label_states(rod)
        ev = []
        for seq, st in sts:
            e = v3.evaluate(rod, st, after_remedy=bool(seq)) if st is not None and cached(rod, st) else None
            if e is None:
                missing += 1
                continue
            ev.append((seq, e))
            per.append(f"| {rod.id()} | {' + '.join(seq) or 'none'} | " + " | ".join(v3._cell(e, c) for c in v3.CHECKS)
                       + f" | {e['regr_rms_pct_per_h']:.2f} ({e['regr_limit']:.2f}) | "
                       f"{e['flank_difference_rms_pct_per_h']:.2f} ({e['flank_limit']:.2f}) | "
                       f"{'yes' if e['all_pass'] else 'no'} | {'yes' if e['good'] else 'no'} |")
        if len(ev) < len(sts) or any(st is None for _, st in sts):
            continue
        u = ev[0][1]
        lab, seq = v3.label_rod([{"sequence": s, "checks_pass": e["all_pass"], "good": e["good"]} for s, e in ev])
        cls = "decline" if lab != "repairable" else ("accept_clean" if not seq else "accept_repaired")
        fixes = [" + ".join(s) for s, e in ev if s and e["all_pass"] and e["good"]]
        labels[rod.id()] = {"class": cls, "expected": EXPECTED[rod.fault], "sequence": seq, "kind": rod.fault,
                            "seed": rod.seed, "size": rod.size, "repairing_states": fixes,
                            "states": len(ev)}
        L.append(f"| {rod.id()} | {EXPECTED[rod.fault]} | {cls} | {len(fixes)}" + (f" ({fixes[0]})" if fixes else "")
                 + f" | {'yes' if u['all_pass'] else 'no'}, {'yes' if u['good'] else 'no'} |")
    n = len(scored_rods())
    counts = {c: sum(v["class"] == c for v in labels.values()) for c in v3.metrics.CLASSES}
    complete = len(labels) == n
    odd = [r for r, v in labels.items() if v["class"] != v["expected"]]
    L += ["", f"- Rods labelled {len(labels)} of {n}; states not yet evaluated {missing}", f"- Classes: {counts}",
          f"- All-decline would score {counts['decline']} of {n}",
          f"- Label differs from the expected class: {len(odd)}" + (": " + ", ".join(odd) if odd else ""),
          f"- Result: {'complete' if complete else 'incomplete'}", "", "## Per state", ""]
    return "\n".join(L + per) + "\n", {"labels": labels, "counts": counts, "complete": complete, "stop": False}


# ------------------------------------------------------------------ v3 driver pointed at this set

def point_v3_here():
    candidate.use("v4")
    v3.CACHE, v3.OUT, v3.FREEZE_TAG, v3.MAX_TRACKER_RUNS = CACHE, OUT, FREEZE_TAG, MAX_TRACKER_RUNS
    v3.scored_rods, v3.initial, v3.label_states, v3.labels_report = scored_rods, initial, label_states, labels_report
    v3.EXPECTED, v3.NAMES, v3.CLEAN_FALSE_ALARM = EXPECTED, NAMES, set()
    # rows of the per-row table, in order: no clean or development rows
    vars(v3).update(CLEAN=[], DEV={}, HELDOUT={f: None for f in list(COMPOUND) + list(NOVEL)})
    v3.cached = cached
    v3.V3Runner = LocalRunner
    v3.seeds = lambda kind: SCORING_SEEDS


def llm_runs():
    runs = OUT / "runs"
    n = sum(1 for m in v3.LLM for _ in runs.glob(f"{m}_*_summary.json")) if runs.exists() else 0
    lim = runs / "usage_limit"
    return n + (len(list(lim.glob("*_summary.json"))) if lim.exists() else 0)


def set_aside_limit_runs():
    """Runs ended by the account session limit (no model answer) move to runs/usage_limit and run again (as v4)."""
    n, lim = 0, OUT / "runs" / "usage_limit"
    for f in (OUT / "runs").glob("*_summary.json"):
        s = json.loads(f.read_text())
        o = s["outcome"]
        if o["status"] == "error" and "session limit" in o.get("args", {}).get("reason", ""):
            lim.mkdir(parents=True, exist_ok=True)
            for g in (f, OUT / "runs" / s["trace"]):
                dest = lim / g.name
                if dest.exists():
                    dest = lim / f"{g.stem}_{time.strftime('%H%M%S')}{g.suffix}"
                g.rename(dest)
            n += 1
    return n


def labels_committed():
    f = OUT / "labels.json"
    return f.exists() and not v3.git("status", "--porcelain", "--", str(f)) and \
        bool(v3.git("ls-files", "--", str(f)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sizing-sweep", "sizing", "label-sweep", "labels", "rules", "agents", "eval"])
    ap.add_argument("--method", choices=v3.LLM)
    ap.add_argument("--repeat", type=int, choices=v3.REPEATS)
    ap.add_argument("--max-runs", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    point_v3_here()
    if a.cmd == "sizing-sweep":
        sweep([(r, initial(r)) for r in sizing_rods()], a.dry_run, "sizing")
    elif a.cmd == "sizing":
        text, info = sizing_report()
        (OUT / "sizing.md").write_text(text)
        if info["complete"]:
            (OUT / "sizing.json").write_text(json.dumps({"sizes": info["sizes"]}, indent=1))
        print(text)
    elif a.cmd == "label-sweep":
        rods = scored_rods()
        sweep([(r, initial(r)) for r in rods], a.dry_run, "labels, unremedied")
        if a.dry_run:
            n = sum(len(tracked([x for x in label_states(r) if x[0]])) for r in rods)
            print(f"remedied states after the unremedied runs (estimate if those are not cached): about {n}")
            return
        sweep([(r, st) for r in rods for st in tracked(label_states(r))], False, "labels, remedied")
    elif a.cmd == "labels":
        text, info = labels_report()
        (OUT / "labels.md").write_text(text)
        if info["complete"]:
            (OUT / "labels.json").write_text(json.dumps(info, indent=1, default=str))
        print(text.split("## Per state")[0])
    elif a.cmd in ("rules", "agents"):
        if not labels_committed():
            sys.exit("labels not committed: no method runs before (spec D2)")
        if v3.git("status", "--porcelain", "--untracked-files=no"):
            sys.exit("tracked files are modified; commit first (each run records the commit)")
        if a.cmd == "rules":
            v3.V3Runner = lambda remote=False: LocalRunner(remote=True)     # stacked tree states tracked on demand
            v3.run_rules()
            return
        if a.method is None or a.repeat is None:
            ap.error("--method and --repeat are required")
        wait_memory()
        left = MAX_LLM_RUNS - llm_runs()
        if left <= 0:
            sys.exit(f"LLM-run cap {MAX_LLM_RUNS} reached; stop and report")
        v3.run_agents(a.method, a.repeat, min(left, a.max_runs) if a.max_runs else left)
        n = set_aside_limit_runs()
        if n:
            sys.exit(f"usage limit: {n} runs ended on the account limit, set aside in runs/usage_limit/; stop")
    else:
        v3.evaluate_all()
        f = OUT / "table_metrics.md"
        f.write_text(f.read_text().replace("# Freeze v3 scored runs: metrics",
                                           "# Held-out compound and novel faults: metrics", 1)
                     .replace("Definitions: `docs/proposals/2026-10-23_freeze-v3.md`, section 3;",
                              "Seeds 40-43, candidate v4 on, freeze v4 prompts. Definitions as freeze v4 "
                              "(`docs/proposals/2026-10-23_freeze-v3.md`, section 3);", 1))


if __name__ == "__main__":
    main()
