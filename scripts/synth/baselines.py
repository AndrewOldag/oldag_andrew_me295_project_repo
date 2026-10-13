"""Run the two non-LLM baselines on the development faults at their frozen sizes, seeds 0-2.

  python scripts/synth/baselines.py next   [--dry-run]   # find the tracker runs still needed; start them as one sweep
  python scripts/synth/baselines.py status               # the running sweep
  python scripts/synth/baselines.py fetch                # copy finished outputs to staging/tracks_baselines/
  python scripts/synth/baselines.py write  --out results/<date>_baselines

The baselines are deterministic, so they are run in rounds: each round runs
both baselines on every rod from the local cache only, collects the tracker
runs a baseline asked for and does not have, and starts them as one sweep
(scripts/synth/sweep.py: shared-machine limits, one sweep at a time). After
fetch, the next round goes one remedy further. `write` runs both baselines
once more, all from the cache, and writes a trace and a summary per task in
the format of scripts/demo_slice.py. Refuses to go past 200 tracker runs.
"""
import argparse
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents.baselines import run_script, run_tree  # noqa: E402
from agents.executors import Slice  # noqa: E402
from agents.launcher import load_config  # noqa: E402
from fix_sweep import entry  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.runner import RUNNER_CONFIG, Measurement, RemoteRunner, Rod  # noqa: E402
from measure.score import truth_error, truth_summary  # noqa: E402

CACHE = ROOT / "staging" / "tracks_baselines"
TRACKS = "tracks_baselines"          # own directory on the tracker machine: no run made with older code is reused
SWEEP = "baselines"
MAX_RUNS = 200
SEEDS = (0, 1, 2)
# development faults at their frozen sizes (docs/proposals/2026-10-11_freeze-v1.md, section 1); None = default size
FAULTS = (("displacement_exceeds_patch", "2x6"), ("width_change", None), ("rigid_drift", "0.5"),
          ("low_texture", None), ("midline_jitter", None))
BASELINES = {"script": lambda sl, trace: run_script(sl, trace),
             "remedy_tree": lambda sl, trace: run_tree(sl, load_config()["agents"]["diagnostician"]["step_limit"],
                                                       trace)}


def rods():
    return [Rod("growth_zone", f, s, size=z) for f, z in FAULTS for s in SEEDS]


def runner_config():
    """private/runner.yaml of this checkout, or of the main repo folder (beside the git common dir)."""
    if RUNNER_CONFIG.exists():
        return RUNNER_CONFIG
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True)
    return (ROOT / common.stdout.strip()).resolve().parent / "private" / "runner.yaml"


class Missing(Exception):
    def __init__(self, rod, settings):
        super().__init__(f"{rod.id()} {settings.tag()}")
        self.rod, self.settings = rod, settings


class CacheRunner:
    """The RemoteRunner interface, from local files only. A run not in the cache raises Missing."""
    form = "remote_job"

    def __init__(self, cache=CACHE):
        self.cache, self.log = Path(cache), []

    def initial_settings(self, rod):
        from measure.remedies import TrackSettings
        return TrackSettings(stride=RemoteRunner.initial_stride(rod))

    def measure(self, rod, settings):
        tag = replace(settings, width_free=False).tag()
        files = [self.cache / f"{rod.id(m)}__{tag}.npz" for m in (False, True)]
        truth = self.cache / f"{rod.id()}_truth.npz"
        if not all(f.exists() for f in files + [truth]):
            raise Missing(rod, settings)
        with np.load(truth) as z:
            t = {k: z[k] for k in z.files}
        return Measurement(from_tracker_npz(files[0]), from_tracker_npz(files[1]), settings, t)


def one_round(write_to=None):
    """Both baselines on every rod. Returns {(rod id, tag): (rod, settings)} of the runs still needed."""
    need = {}
    for rod in rods():
        for name, fn in BASELINES.items():
            stem = f"{name}_{rod.fault}" + (f"_z{rod.size}" if rod.size else "") + f"_s{rod.seed}"
            trace = write_to / f"{stem}_trace.jsonl" if write_to else None
            if trace:
                trace.unlink(missing_ok=True)
            try:
                sl = Slice(CacheRunner(), rod)
                outcome = fn(sl, trace)
            except Missing as m:
                need[(m.rod.id(), replace(m.settings, width_free=False).tag())] = (m.rod, replace(m.settings,
                                                                                                  width_free=False))
                continue
            if write_to:
                write_summary(write_to / f"{stem}_summary.json", rod, sl, outcome)
    return need


def write_summary(path, rod, sl, outcome):
    """Same fields as scripts/demo_slice.py."""
    first, last = sl.runs[0][1], sl.current
    summary = {"rod": {"case": rod.case, "fault": rod.fault, "size": rod.size, "seed": rod.seed},
               "runner": "remote_job", "baseline": outcome.agent,
               "truth": truth_summary(first.truth, first.record.pixel_um),
               "error_before": truth_error(first.record, first.truth),
               "initial_checks": [c.to_dict() for c in sl.runs[0][2]],
               "outcome": outcome.__dict__, "error_after": truth_error(last.record, last.truth),
               "remedies": [ch for _, _, _, ch in sl.runs[1:]],
               "roll_backs": sum(ch.startswith("rolled back") for _, _, _, ch in sl.runs[1:]),
               "final_settings": sl.runs[-1][0].to_dict(), "final_checks": [c.to_dict() for c in sl.checks],
               "reported": outcome.status == "accept"}
    path.write_text(json.dumps(summary, indent=1, default=str))


def cached_runs():
    return len([f for f in CACHE.glob("*__*.npz")]) if CACHE.exists() else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["next", "status", "fetch", "write"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.cmd == "next":
        need = one_round()
        n_new, n_have = 2 * len(need), cached_runs()
        print(f"tracker runs in the cache {n_have}; needed now {n_new} ({len(need)} settings x rod and moved)")
        for rid, tag in sorted(need):
            print(f"  {rid} {tag}")
        if not need or a.dry_run:
            return
        if n_have + n_new > MAX_RUNS:
            sys.exit(f"stop: {n_have + n_new} tracker runs would pass the limit of {MAX_RUNS}; ask Andrew")
        r = RemoteRunner(runner_config(), cache=CACHE)
        st = r.sweep_status()
        if st.get("running"):
            sys.exit(f"a sweep is running ({st.get('plan')}); wait and try again")
        by_rod = {}
        for rod, settings in need.values():
            by_rod.setdefault(rod, []).append(settings)
        plan = {"rods": [entry(rod, runs) for rod, runs in by_rod.items()]}
        r.sweep_start(plan, SWEEP, tracks=TRACKS)
        print(f"started: {len(plan['rods'])} rods, {n_new} tracker runs")
    elif a.cmd == "status":
        st = RemoteRunner(runner_config(), cache=CACHE).sweep_status(SWEEP)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}, "
              f"cached {sum(bool(x.get('cached')) for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "fetch":
        r = RemoteRunner(runner_config(), cache=CACHE)
        st = r.sweep_status(SWEEP)
        if st.get("running"):
            sys.exit(f"a sweep is running ({st.get('plan')}); fetch after it ends")
        CACHE.mkdir(parents=True, exist_ok=True)
        with (CACHE / "sweeps.jsonl").open("a") as f:      # end lines of each round, for the results table
            for x in st["log"]:
                if "tag" not in x:
                    f.write(json.dumps(x) + "\n")
        r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched: {cached_runs()} tracker outputs in {CACHE.relative_to(ROOT)}")
    else:
        if not a.out:
            ap.error("--out is required")
        out = Path(a.out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        need = one_round(out)
        if need:
            sys.exit(f"{len(need)} runs still needed; run `next` first")
        print(f"wrote {len(list(out.glob('*_summary.json')))} summaries to {out}")


if __name__ == "__main__":
    main()
