"""No-agent sweeps for docs/specs/2026-10-11_remedy-fixes-coupled-mode-shared-compute.md.

  python scripts/synth/fix_sweep.py start  --part P [--dry-run]
  python scripts/synth/fix_sweep.py status --part P
  python scripts/synth/fix_sweep.py stop
  python scripts/synth/fix_sweep.py fetch  --part P        # to staging/tracks_2026-10-11/<tracks dir>

Parts:
- check: 8 clean runs under the limits for the shared machine (item 1)
Each part writes its tracker outputs to its own directory on the tracker
machine, so a run made with older code is never reused by name. The limits
for the shared machine are in scripts/synth/sweep.py.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RemoteRunner, Rod  # noqa: E402

CACHE = ROOT / "staging" / "tracks_2026-10-11"


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


PARTS = {"check": (part_check, "tracks_check")}


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
