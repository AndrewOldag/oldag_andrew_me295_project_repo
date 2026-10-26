"""Freeze v4 (inbox diag-analysis items 3-4; Andrew 2026-10-25): the v3 scored set on unseen seeds 26-28, with
the freeze v4 candidate on (C1, C2, C3 option a; agents/candidate.py).

  python scripts/synth/scored_v4.py plan   --phase labels|methods [--dry-run]   # start one sweep
  python scripts/synth/scored_v4.py status
  python scripts/synth/scored_v4.py fetch                          # to staging/tracks_freeze_v4/
  python scripts/synth/scored_v4.py labels                         # labels of the 51 rods, seeds 26-28
  python scripts/synth/scored_v4.py dev-check                      # diagnostician, v3 seed 20, one run per row
  python scripts/synth/scored_v4.py rules                          # script and remedy tree
  python scripts/synth/scored_v4.py agents --method diagnostician|single_agent --repeat 0|1|2 [--max-runs N]
  python scripts/synth/scored_v4.py eval                           # metrics and tables, v3 layout

Everything else is the freeze v3 driver (scripts/synth/scored_v3.py) pointed at v4: cache, output folder, rod
set, tag. Rods: every v3 class at its v3 size (clean rods; development faults at the freeze v2 sizes; held-out
faults at the v3 sizes in results/2026-10-23_freeze_v3/sizing.json). Labels: v3 repair criteria with C3 (a).
Caps: the label sweep at most LABEL_CAP tracker runs; MAX_TRACKER_RUNS tracker runs and MAX_LLM_RUNS
LLM runs in all (items 3-5). Host: the lab server (item 5). Free VM memory at least MIN_FREE_GB before each batch of LLM runs.
Development check (item 3 (3)): the diagnostician on v3 scoring seed 20, whose traces C1 and C2 were written
from, so it is a check, not a score. States from the v3 cache only (no tracker runs); a state not cached ends
that run and is listed.
"""
import argparse
import ctypes
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scored_v3 as v3  # noqa: E402
from scored_v3 import DEV as V3_DEV  # noqa: E402
from agents import candidate  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

FREEZE_TAG = "freeze-v4"
OUT = ROOT / "results" / "2026-10-25_freeze_v4"
CACHE = ROOT / "staging" / "tracks_freeze_v4"
V3_CACHE, V3_OUT = v3.CACHE, v3.OUT
TRACKS, SWEEP = "tracks_freeze_v4", "freeze_v4"
SCORING_SEEDS = (26, 27, 28)                   # never used before (planning, 2026-10-25 00:40)
DEV_SEED = 20
LABEL_CAP = 228                                # Andrew, 2026-10-25 17:10 (item 5; was 150, item 3 (2))
MAX_TRACKER_RUNS = 420                         # Andrew, 2026-10-25 17:10 (item 5; was 300, item 4 (3))
MAX_LLM_RUNS = 400                             # item 4 (3)
MIN_FREE_GB = 4.0                              # items 3 (3), 4 (3)
# expected classes as labelled in v3, and stage_log_missing under C3 (a); used only to list labels that differ
EXPECTED = {**v3.EXPECTED, "displacement_exceeds_patch": "decline", "stage_log_missing": "decline"}
DEV_OUT = OUT / "dev_check"


def scored_rods():
    sizes = {**V3_DEV, **json.loads((V3_OUT / "sizing.json").read_text())["sizes"]}
    out = [Rod(c, None, s) for c in v3.CLEAN for s in SCORING_SEEDS]
    out += [Rod(v3.GZ, f, s, size=sizes[f]) for f in list(V3_DEV) + list(v3.HELDOUT) for s in SCORING_SEEDS]
    return out


def point_v3_at_v4():
    candidate.use("v4")
    v3.CACHE, v3.OUT, v3.TRACKS, v3.SWEEP = CACHE, OUT, TRACKS, SWEEP
    v3.FREEZE_TAG, v3.MAX_TRACKER_RUNS = FREEZE_TAG, MAX_TRACKER_RUNS
    v3.scored_rods, v3.EXPECTED, v3.CLEAN_FALSE_ALARM = scored_rods, EXPECTED, set()


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


def memory_ok():
    f = free_gb()
    if f < MIN_FREE_GB:
        sys.exit(f"free VM memory {f:.1f} GB, under {MIN_FREE_GB} GB: wait")
    print(f"free VM memory {f:.1f} GB", flush=True)


def llm_runs():
    """LLM runs so far: scored runs and development-check runs (summaries written)."""
    n = sum(1 for m in v3.LLM for _ in (OUT / "runs").glob(f"{m}_*_summary.json")) if (OUT / "runs").exists() else 0
    return n + (len(list(DEV_OUT.glob("*_summary.json"))) if DEV_OUT.exists() else 0)


def start_label_sweep(dry):
    need = v3.need_labels()
    n_new = 2 * len({(r.id(), s.tag()) for r, s in need})
    if v3.tracker_runs_cached() + n_new > LABEL_CAP and not dry:
        sys.exit(f"stop: label sweep would reach {v3.tracker_runs_cached() + n_new} tracker runs, over the "
                 f"label cap {LABEL_CAP}; ask Andrew")
    v3.start_sweep(need, dry)


# ------------------------------------------------------------------ development check

_V3_SCORED = v3.scored_rods                    # the v3 set (seeds 20-22), kept before point_v3_at_v4


class _V3CacheRunner(v3.V3Runner):
    """States from the local v3 cache only; a missing state raises v3.Missing."""

    def measure(self, rod, settings):
        cache = v3.CACHE
        v3.CACHE = V3_CACHE
        try:
            return super().measure(rod, settings)
        finally:
            v3.CACHE = cache


def run_dev_check():
    from agents.launcher import Launcher
    from agents.orchestrator import Orchestrator
    if v3.git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files are modified; commit first (each run records the commit)")
    if not (OUT / "labels.json").exists() or v3.git("status", "--porcelain", "--", str(OUT / "labels.json")):
        sys.exit("labels for seeds 26-28 not committed: no agent run before (item 3 (2))")
    memory_ok()
    DEV_OUT.mkdir(parents=True, exist_ok=True)
    launcher = Launcher()
    for rod in [r for r in _V3_SCORED() if r.seed == DEV_SEED]:
        name = f"diagnostician_{rod.id()}"
        summ, trace = DEV_OUT / f"{name}_summary.json", DEV_OUT / f"{name}_trace.jsonl"
        if summ.exists():
            continue
        if llm_runs() >= MAX_LLM_RUNS:
            sys.exit(f"LLM-run cap {MAX_LLM_RUNS} reached; stop and report")
        if trace.exists():
            trace = DEV_OUT / f"{name}_trace_{time.strftime('%H%M%S')}.jsonl"
        t0 = time.time()
        try:
            sl = v3.Slice(_V3CacheRunner(), rod)
            o = Orchestrator(launcher, trace).run("diagnostician", sl.label, sl.task(), sl.executors())
        except v3.Missing as e:
            with (DEV_OUT / "missing_states.jsonl").open("a") as f:
                f.write(json.dumps({"run": name, "state": str(e)}) + "\n")
            print(f"{name}: state not in the v3 cache: {e}", flush=True)
            continue
        except Exception as e:
            with (DEV_OUT / "harness_errors.jsonl").open("a") as f:
                f.write(json.dumps({"run": name, "error": f"{type(e).__name__}: {e}",
                                    "traceback": traceback.format_exc()[-2000:]}) + "\n")
            print(f"{name}: HARNESS ERROR {type(e).__name__}: {e}", flush=True)
            continue
        v3.write_summary(summ, rod, sl, o, "diagnostician", {"dev_check": True, "candidate": candidate.active(),
                                                              "trace": trace.name, "claude_code": launcher.version,
                                                              "wall_s": round(time.time() - t0, 1)})
        print(f"{name}: {o.status} {o.args.get('fault', '')} steps {o.steps}", flush=True)


def dev_check_report():
    """The v3 per-row table for the development check (one run per row), labels from v3 with C3 (a)."""
    from measure import metrics
    rows, L = [], ["# Freeze v4 development check, not a score", "",
                   f"Diagnostician, candidate v4 on, v3 seed {DEV_SEED} (v3 scoring seed; C1 and C2 were written from "
                   "its traces), one run per row of the v3 set. Labels: v3 label sweep with C3 (a) "
                   "(`switch_check.md`). States from the v3 cache only.", "",
                   "| Row | Rod | Class | Status | Category | Named fault | Fault correct | Steps | Remedies | v3 diagnostician correct (seed 20, 3 repeats) |",
                   "| :-- | :-- | :-- | :-- | :-- | :-- | :-- | --: | :-- | :-- |"]
    candidate.use("v4")
    cache, out, rods = v3.CACHE, v3.OUT, v3.scored_rods
    v3.CACHE, v3.OUT, v3.scored_rods = V3_CACHE, V3_OUT, _V3_SCORED
    try:
        _, lab = v3.labels_report()
        tol_cfg = v3.load_tolerance()
        for rod in [r for r in _V3_SCORED() if r.seed == DEV_SEED]:
            f = DEV_OUT / f"diagnostician_{rod.id()}_summary.json"
            cls = lab["labels"][rod.id()]["class"]
            v3runs = [json.loads((V3_OUT / "runs" / f"{v3.stem('diagnostician', rod, k)}_summary.json").read_text())
                      for k in v3.REPEATS]
            tol = v3.rod_tolerance(v3.truth(rod), v3.PIXEL_UM, tol_cfg)
            v3c = sum(metrics.correct({"category": metrics.category(
                s["outcome"]["status"], cls, v3.measurement_good(s["error_after"], tol,
                                                                 bool(s["final_settings"].get("width_free"))))})
                      for s in v3runs)
            if not f.exists():
                L.append(f"| {v3.kind(rod)} | {rod.id()} | {cls} | not run | - | - | - | - | - | {v3c} / 3 |")
                continue
            s = json.loads(f.read_text())
            good = v3.measurement_good(s["error_after"], tol, bool(s["final_settings"].get("width_free")))
            cat = metrics.category(s["outcome"]["status"], cls, good)
            nf = v3.named_fault(DEV_OUT / s["trace"])
            fc = (nf in v3.NAMES[rod.fault]) if rod.fault else None
            rows.append({"category": cat, "cls": cls, "fault_correct": fc})
            L.append(f"| {v3.kind(rod)} | {rod.id()} | {cls} | {s['outcome']['status']} | {cat} | {nf or '-'} | "
                     f"{'-' if fc is None else ('yes' if fc else 'no')} | {s['outcome']['steps']} | "
                     f"{'; '.join(s['remedies']) or 'none'} | {v3c} / 3 |")
    finally:
        v3.CACHE, v3.OUT, v3.scored_rods = cache, out, rods
    n_ok = sum(metrics.correct(r) for r in rows)
    L += ["", f"- Runs {len(rows)}; correct {n_ok}", "- Development check only: seed 20 is not unseen. Not a score"]
    miss = DEV_OUT / "missing_states.jsonl"
    if miss.exists():
        L.append(f"- Runs ended on a state not in the v3 cache: {len(miss.read_text().splitlines())}")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "status", "fetch", "labels", "dev-check", "dev-report", "rules",
                                    "agents", "eval"])
    ap.add_argument("--phase", choices=["labels", "methods"])
    ap.add_argument("--method", choices=v3.LLM)
    ap.add_argument("--repeat", type=int, choices=v3.REPEATS)
    ap.add_argument("--max-runs", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    point_v3_at_v4()
    if a.cmd == "plan":
        if a.phase == "labels":
            start_label_sweep(a.dry_run)
        elif a.phase == "methods":
            v3.start_sweep(v3.need_methods(), a.dry_run)
        else:
            ap.error("--phase is required")
    elif a.cmd in ("status", "fetch"):
        r = RemoteRunner(v3.runner_config(), cache=CACHE)
        st = r.sweep_status(SWEEP)
        if a.cmd == "status":
            log = st.pop("log")
            print(json.dumps(st))
            runs = [x for x in log if "tag" in x]
            print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
            for x in log:
                if "tag" not in x:
                    print(json.dumps(x))
        else:
            if st.get("running"):
                sys.exit("a sweep is running; fetch after it ends")
            CACHE.mkdir(parents=True, exist_ok=True)
            with (CACHE / "sweeps.jsonl").open("a") as f:
                for x in st["log"]:
                    if "tag" not in x:
                        f.write(json.dumps(x) + "\n")
            r.sweep_fetch(TRACKS, CACHE)
            print(f"fetched: {v3.tracker_runs_cached()} tracker outputs in the cache (cap {MAX_TRACKER_RUNS})")
    elif a.cmd == "labels":
        text, info = v3.labels_report()
        text = text.replace("# Labels of the freeze v3 scored set", "# Labels of the freeze v4 scored set", 1)
        text = text.replace("(spec 2026-10-10, part C; measure.score.label_rod)",
                            "(spec 2026-10-10, part C; measure.score.label_rod; C3 option a: a check that cannot "
                            "be computed after a remedy fails)", 1)
        (OUT / "labels.md").write_text(text)
        if info["complete"]:
            (OUT / "labels.json").write_text(json.dumps(info, indent=1, default=str))
        print(text.split("## Per state")[0])
    elif a.cmd == "dev-check":
        run_dev_check()
    elif a.cmd == "dev-report":
        text = dev_check_report()
        (OUT / "dev_check.md").write_text(text)
        print(text)
    elif a.cmd == "rules":
        v3.run_rules()
    elif a.cmd == "agents":
        if a.method is None or a.repeat is None:
            ap.error("--method and --repeat are required")
        if not (OUT / "labels.json").exists():
            sys.exit("labels missing")
        memory_ok()
        left = MAX_LLM_RUNS - llm_runs()
        if left <= 0:
            sys.exit(f"LLM-run cap {MAX_LLM_RUNS} reached; stop and report")
        v3.run_agents(a.method, a.repeat, min(left, a.max_runs) if a.max_runs else left)
    else:
        v3.evaluate_all()
        f = OUT / "table_metrics.md"
        f.write_text(f.read_text().replace("# Freeze v3 scored runs: metrics", "# Freeze v4 scored runs: metrics", 1)
                     .replace("Definitions: `docs/proposals/2026-10-23_freeze-v3.md`, section 3;",
                              "Seeds 26-28, candidate v4 on. Definitions as freeze v3 "
                              "(`docs/proposals/2026-10-23_freeze-v3.md`, section 3);", 1))


if __name__ == "__main__":
    main()
