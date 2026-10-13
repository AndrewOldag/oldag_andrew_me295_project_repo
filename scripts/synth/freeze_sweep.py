"""No-agent sweep for spec 2026-10-12 (freeze decisions), item 3: seeds 3-5 of the development faults.

  python scripts/synth/freeze_sweep.py start  --part seeds35|seeds35_reg [--dry-run]
  python scripts/synth/freeze_sweep.py status --part P
  python scripts/synth/freeze_sweep.py stop
  python scripts/synth/freeze_sweep.py fetch  --part P        # to staging/tracks_2026-10-12/tracks_freeze

Parts:
- seeds35: the five development faults at their frozen sizes, seeds 3-5, every state of the fitting remedy
  except register_frames
- seeds35_reg: register_frames on rigid_drift seeds 3-5; its band start is read from the fetched unremedied
  record, so it runs after seeds35 is fetched
States as in scripts/synth/eval_freeze.py; `strong` is withdrawn and not run. The limits for the shared
machine are in scripts/synth/sweep.py.
"""
import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_sweep import BASE_RADIUS, entry  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

TRACKS = "tracks_freeze"
CACHE = ROOT / "staging" / "tracks_2026-10-12" / TRACKS
SEEDS = (3, 4, 5)
FROZEN = {"displacement_exceeds_patch": "2x6", "width_change": None, "rigid_drift": "0.5",
          "low_texture": "0.03", "midline_jitter": "3"}


def rods():
    return [Rod("growth_zone", f, s, size=z) for f, z in FROZEN.items() for s in SEEDS]


def states(rod):
    """Tracker runs of the fitting remedy, unremedied first; register_frames is in seeds35_reg."""
    base = TrackSettings(stride=RemoteRunner.initial_stride(rod))
    if rod.fault == "displacement_exceeds_patch":
        return [base, replace(base, stride=3), replace(base, stride=1)]          # 6 -> 3 -> 1
    if rod.fault == "low_texture":
        return [base, replace(base, disk_radius=round(1.5 * BASE_RADIUS)), replace(base, disk_radius=2 * BASE_RADIUS)]
    if rod.fault == "midline_jitter":
        return [base, replace(base, midline_smooth="light")]
    return [base]                     # width_change (the width-free ratio needs no re-run), rigid_drift


def part_seeds35():
    return [entry(r, states(r)) for r in rods()]


def part_seeds35_reg():
    from measure.preprocess import registration_band_start
    from measure.record import from_tracker_npz
    out = []
    for r in rods():
        if r.fault != "rigid_drift":
            continue
        f = CACHE / f"{r.id()}__st1.npz"
        if not f.exists():
            raise FileNotFoundError(f"{f.name} not fetched; run and fetch --part seeds35 first")
        start = registration_band_start(from_tracker_npz(f))
        out.append(entry(r, [TrackSettings(register=True, register_from_px=int(round(start)))]))
    return out


PARTS = {"seeds35": part_seeds35, "seeds35_reg": part_seeds35_reg}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "stop", "fetch"])
    ap.add_argument("--part", choices=sorted(PARTS))
    ap.add_argument("--dry-run", action="store_true", help="print the plan size only")
    a = ap.parse_args()
    if a.cmd != "stop" and not a.part:
        ap.error("--part is required")
    name = f"freeze_{a.part}"
    if a.cmd == "start":
        plan = {"rods": PARTS[a.part]()}
        n = sum(2 * len(x["runs"]) for x in plan["rods"])
        if a.dry_run:
            print(f"{a.part}: {len(plan['rods'])} rods, {n} tracker runs")
            for x in plan["rods"]:
                print(x["id"], [r["tag"] for r in x["runs"]])
            return
        RemoteRunner().sweep_start(plan, name, tracks=TRACKS)
        print(f"started {a.part}: {len(plan['rods'])} rods, {n} tracker runs")
        return
    r = RemoteRunner()
    if a.cmd == "status":
        st = r.sweep_status(name)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "stop":
        print(json.dumps(r.sweep_stop()))
    else:
        cache = r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched to {cache.relative_to(ROOT)}: {len(list(cache.glob('*__*.npz')))} files")


if __name__ == "__main__":
    main()
