"""No-agent sweeps for docs/specs/2026-10-11_remedy-fixes-coupled-mode-shared-compute.md.

  python scripts/synth/fix_sweep.py start  --part P [--dry-run]
  python scripts/synth/fix_sweep.py status --part P
  python scripts/synth/fix_sweep.py stop
  python scripts/synth/fix_sweep.py fetch  --part P        # to staging/tracks_2026-10-11/<tracks dir>

Parts:
- check: 8 clean runs under the limits for the shared machine (item 1)
- band: registration band at 0.6, 0.8, 0.9 of the tracked length on one clean rod (item 3)
- band2: band from the measured profile, two band ends, clean and rigid_drift rods (item 3)
- band3: band from the measured profile to the midline end, inside the frames (item 3)
- u_clean: clean rods through the fixed remedies, uncoupled (item 4)
- u_faults: rigid_drift, midline_jitter and low_texture sizes with the fixed remedies, uncoupled (item 4)
Each part writes its tracker outputs to its own directory on the tracker
machine, so a run made with older code is never reused by name. The limits
for the shared machine are in scripts/synth/sweep.py.
"""
import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

CACHE = ROOT / "staging" / "tracks_2026-10-11"
SEEDS = (0, 1, 2)
BASE_RADIUS = 15


def entry(rod, runs):
    """runs: TrackSettings, or (tag, args) for runs that are not a remedy state."""
    out = []
    for r in runs:
        tag, args = (r.tag(), r.args()) if isinstance(r, TrackSettings) else r
        out.append({"tag": tag, "args": args})
    return {"id": rod.id(), "options": rod.options(), "runs": out}


def part_check():
    rods = [Rod(c, None, s) for c in ("growth_zone", "bending") for s in (0, 1)]
    return [entry(r, [TrackSettings()]) for r in rods]


def part_band():
    """Item 3: one clean rod, registration band starting at 0.6, 0.8 and 0.9 of the tracked length (400 px)."""
    runs = [(f"st1_regb{int(100 * f)}", ["--stride", "1", "--register", "--register-from-px", str(400 * f)])
            for f in (0.6, 0.8, 0.9)]
    return [entry(Rod("growth_zone", None, 0), runs)]


def band_start(rod):
    """Registration band start from the rod's unremedied record (preprocess.registration_band_start)."""
    from measure.preprocess import registration_band_start
    from measure.record import from_tracker_npz
    for cache in (CACHE / "tracks_check", ROOT / "staging" / "tracks"):
        f = cache / f"{rod.id()}__st{RemoteRunner.initial_stride(rod)}.npz"
        if f.exists():
            return registration_band_start(from_tracker_npz(f))
    raise FileNotFoundError(f"no unremedied record for {rod.id()}; run and fetch it first")


def part_band2():
    """Item 3: band from the measured profile, ending at the tracked length or at the end of the midline."""
    rods = [Rod(c, None, s) for c in ("growth_zone", "bending") for s in SEEDS] +            [Rod("growth_zone", "rigid_drift", s, size="1") for s in SEEDS]
    out = []
    for rod in rods:
        s0 = band_start(rod)
        out.append(entry(rod, [(f"st1_regp{s0:.0f}_400", ["--stride", "1", "--register", "--register-from-px", str(s0)]),
                               (f"st1_regp{s0:.0f}_end", ["--stride", "1", "--register", "--register-from-px", str(s0),
                                                           "--register-to-px", "10000"])]))
    return out


def part_band3():
    """Item 3: band from the measured profile to the end of the midline, kept 25 px inside the frames."""
    rods = [Rod(c, None, s) for c in ("growth_zone", "bending") for s in SEEDS] +            [Rod("growth_zone", "rigid_drift", s, size="1") for s in SEEDS]
    out = []
    for rod in rods:
        s0 = band_start(rod)
        out.append(entry(rod, [(f"st1_regp{s0:.0f}_in", ["--stride", "1", "--register", "--register-from-px", str(s0),
                                                         "--register-to-px", "10000"])]))
    return out


def register_state(rod, base=None):
    """register_frames as apply_remedy carries it out: band start from the rod's unremedied record."""
    base = base or TrackSettings(stride=RemoteRunner.initial_stride(rod))
    return replace(base, register=True, register_from_px=int(round(band_start(rod))))


CLEAN = [Rod(c, None, s) for c in ("growth_zone", "bending") for s in SEEDS]
U_SIZES = {"rigid_drift": ["0.25", "0.5", "0.75", "1"], "midline_jitter": ["0.5", "1", "2", "3"],
           "low_texture": ["0.2", "0.25"]}


def fault_states(rod):
    """The fixed remedy's states for a fault rod, unremedied first."""
    base = TrackSettings(stride=RemoteRunner.initial_stride(rod))
    if rod.fault == "rigid_drift":
        return [base, register_state(rod, base)]
    if rod.fault == "midline_jitter":
        return [base, replace(base, midline_smooth="light"), replace(base, midline_smooth="strong")]
    if rod.fault == "low_texture":
        return [base, replace(base, disk_radius=round(1.5 * BASE_RADIUS)), replace(base, disk_radius=2 * BASE_RADIUS)]
    raise ValueError(rod.fault)


def part_u_clean():
    """Item 4: clean rods, unremedied and through register_frames, smooth_midline light and strong."""
    return [entry(r, [TrackSettings(), register_state(r), TrackSettings(midline_smooth="light"),
                      TrackSettings(midline_smooth="strong")]) for r in CLEAN]


def part_u_faults():
    """Item 4: rigid_drift and midline_jitter at four sizes, low_texture at 0.2 and 0.25, with the fixed remedies."""
    return [entry(r, fault_states(r)) for r in fault_rods()]


def fault_rods():
    return [Rod("growth_zone", f, s, size=z) for f, sizes in U_SIZES.items() for z in sizes for s in SEEDS]


PARTS = {"check": (part_check, "tracks_check"), "band": (part_band, "tracks_band"),
         "u_clean": (part_u_clean, "tracks_uncoupled"), "u_faults": (part_u_faults, "tracks_uncoupled"),
         "band2": (part_band2, "tracks_band"), "band3": (part_band3, "tracks_band")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "stop", "fetch"])
    ap.add_argument("--part", choices=sorted(PARTS))
    ap.add_argument("--dry-run", action="store_true", help="print the plan size only")
    a = ap.parse_args()
    if a.cmd != "stop" and not a.part:
        ap.error("--part is required")
    name = f"fix_{a.part}"
    if a.cmd == "start":
        make, tracks = PARTS[a.part]
        plan = {"rods": make()}
        n = sum(2 * len(x["runs"]) for x in plan["rods"])
        if a.dry_run:
            print(f"{a.part}: {len(plan['rods'])} rods, {n} tracker runs")
            return
        RemoteRunner().sweep_start(plan, name, tracks=tracks)
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
        tracks = PARTS[a.part][1]
        cache = r.sweep_fetch(tracks, CACHE / tracks)
        print(f"fetched to {cache.relative_to(ROOT)}: {len(list(cache.glob('*__*.npz')))} files")


if __name__ == "__main__":
    main()
