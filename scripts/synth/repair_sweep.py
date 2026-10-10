"""No-agent sweeps for the repair-criteria spec (docs/specs/2026-10-10_repair-criteria.md).

  python scripts/synth/repair_sweep.py start [--part A|B|all]   # write the plan, start it on the tracker machine
  python scripts/synth/repair_sweep.py status
  python scripts/synth/repair_sweep.py fetch                    # copy tracker outputs to staging/tracks

Part A: clean growth_zone and bending, seeds 0-2, each remedy setting alone.
Part B: fault sizes with the fitting remedy's states (one and two steps).
Uses private/runner.yaml (measure.runner.RemoteRunner).
"""
import argparse
import io
import json
import shlex
import sys
import tarfile
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
    return {"rods": [{"options": rod.options(), "runs": [{"tag": s.tag(), "args": s.args()} for s in states]}
                     for rod, states in rods]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "fetch"])
    ap.add_argument("--part", default="all", choices=["A", "B", "all"])
    a = ap.parse_args()
    r = RemoteRunner()
    q = shlex.quote
    if a.cmd == "start":
        p = plan(a.part)
        n = sum(2 * len(x["runs"]) for x in p["rods"])
        r.sync_code()
        r._ssh(f"mkdir -p {q(r.work)} && cat > {q(r.work)}/plan.json", stdin=json.dumps(p).encode())
        r._ssh(f"cd {q(r.work)} && setsid nohup {r.python} {q(r.code)}/scripts/synth/sweep.py "
               f"--plan plan.json --work . --workers 4 > sweep.log 2>&1 < /dev/null &")
        print(f"started: {len(p['rods'])} rods, {n} tracker runs")
    elif a.cmd == "status":
        print(r._ssh(f"cd {q(r.work)} && wc -l < sweep.log && grep -c '\"ok\": false' sweep.log; "
                     f"tail -n 1 sweep.log").decode())
    else:
        data = r._ssh(f"cd {q(r.work)}/tracks && tar cf - *__*.npz")
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(r.cache, filter="data")
        print(f"fetched to {r.cache.relative_to(ROOT)}: {len(list(r.cache.glob('*__*.npz')))} files")
        for rid in {p.name.split("__")[0] for p in r.cache.glob("*__*.npz") if "_moved__" not in p.name}:
            if not (r.cache / f"{rid}_truth.npz").exists():
                r.truth(rid)


if __name__ == "__main__":
    main()
