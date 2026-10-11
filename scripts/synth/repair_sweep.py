"""No-agent sweeps for the repair-criteria spec (docs/specs/2026-10-10_repair-criteria.md).

  python scripts/synth/repair_sweep.py start [--part A|B|all]   # write the plan, start it on the tracker machine
  python scripts/synth/repair_sweep.py status
  python scripts/synth/repair_sweep.py stop
  python scripts/synth/repair_sweep.py fetch                    # copy tracker outputs to staging/tracks

Part A: clean growth_zone and bending, seeds 0-2, each remedy setting alone.
Part B: fault sizes with the fitting remedy's states (one and two steps);
width_change at its approved size, unremedied.
Uses private/runner.yaml (measure.runner.RemoteRunner). The limits for the
shared machine are in scripts/synth/sweep.py.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

SEEDS = (0, 1, 2)
BASE_RADIUS = 15

# Part A: every remedy setting applied alone to a clean rod
A_SETTINGS = [TrackSettings(), TrackSettings(stride=2),
              TrackSettings(disk_radius=round(1.5 * BASE_RADIUS)), TrackSettings(disk_radius=2 * BASE_RADIUS),
              TrackSettings(register=True), TrackSettings(midline_smooth="light"),
              TrackSettings(midline_smooth="strong"), TrackSettings(band_mask="mask_second_root"),
              TrackSettings(band_mask="crop_to_main_root")]

# Part B: sizes per fault, and the states the fitting remedy reaches in one or two steps
B_SIZES = {
    "rigid_drift": ["0.25", "0.5", "0.75", "1"],
    "displacement_exceeds_patch": ["2x6", "3x4", "4x3"],
    "midline_jitter": ["0.5", "1", "2", "3"],
    "low_texture": ["0.06", "0.1", "0.15", "0.03"],
}


def b_states(fault, size):
    if fault == "rigid_drift":
        return [TrackSettings(), TrackSettings(register=True)]
    if fault == "displacement_exceeds_patch":
        k = int(size.split("x")[1])
        ks = sorted({k, max(1, k // 2), max(1, k // 4)}, reverse=True)
        return [TrackSettings(stride=x) for x in ks]
    if fault == "midline_jitter":
        return [TrackSettings(), TrackSettings(midline_smooth="light"), TrackSettings(midline_smooth="strong")]
    if fault == "low_texture":
        return [TrackSettings(), TrackSettings(disk_radius=round(1.5 * BASE_RADIUS)),
                TrackSettings(disk_radius=2 * BASE_RADIUS)]
    raise ValueError(fault)


def plan(part):
    rods = []
    if part in ("A", "all"):
        for case in ("growth_zone", "bending"):
            for seed in SEEDS:
                rods.append((Rod(case, None, seed), A_SETTINGS))
    if part in ("B", "all"):
        for fault, sizes in B_SIZES.items():
            for size in sizes:
                for seed in SEEDS:
                    rods.append((Rod("growth_zone", fault, seed, size=size), b_states(fault, size)))
        # width_change keeps its size; its remedy needs no tracker re-run (decisions, 2026-10-10)
        for seed in SEEDS:
            rods.append((Rod("growth_zone", "width_change", seed), [TrackSettings()]))
    return {"rods": [{"id": rod.id(), "options": rod.options(), "runs": [{"tag": s.tag(), "args": s.args()} for s in states]}
                     for rod, states in rods]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "stop", "fetch"])
    ap.add_argument("--part", default="all", choices=["A", "B", "all"])
    a = ap.parse_args()
    r = RemoteRunner()
    name = f"repair_{a.part}"
    if a.cmd == "start":
        p = plan(a.part)
        n = sum(2 * len(x["runs"]) for x in p["rods"])
        r.sweep_start(p, name)
        print(f"started: {len(p['rods'])} rods, {n} tracker runs")
    elif a.cmd == "status":
        st = r.sweep_status(name)
        log = st.pop("log")
        print(json.dumps(st))
        print(f"runs logged {sum('tag' in x for x in log)}, failed {sum(x.get('ok') is False for x in log)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "stop":
        print(json.dumps(r.sweep_stop()))
    else:
        r.sweep_fetch()
        print(f"fetched to {r.cache.relative_to(ROOT)}: {len(list(r.cache.glob('*__*.npz')))} files")


if __name__ == "__main__":
    main()
