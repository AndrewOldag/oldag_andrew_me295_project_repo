"""Render synthetic rods and track them, on the machine that has the tracker.

  python scripts/synth/run_batch.py --work DIR --case growth_zone --seeds 0 1 2 [--fault F] [--moved-too]

Runs with the tracker environment's Python (it has numpy and scipy, which the
renderer needs). For each rod: render into DIR/rods, track into
DIR/tracks/<id>.npz, copy the truth next to it, and print one JSON line.
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--work", required=True)
ap.add_argument("--case", default="growth_zone")
ap.add_argument("--fault", default=None)
ap.add_argument("--seeds", type=int, nargs="+", default=[0])
ap.add_argument("--moved-too", action="store_true", help="also the rigidly moved run for the invariance check")
a = ap.parse_args()
work = Path(a.work)
(work / "rods").mkdir(parents=True, exist_ok=True)
(work / "tracks").mkdir(parents=True, exist_ok=True)
for seed in a.seeds:
    for moved in ([False, True] if a.moved_too else [False]):
        t0 = time.time()
        cmd = [sys.executable, str(HERE / "make_rod.py"), "--out", str(work / "rods"),
               "--case", a.case, "--seed", str(seed)] + (["--fault", a.fault] if a.fault else []) \
              + (["--moved"] if moved else [])
        info = json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1])
        rid = info["id"]
        cmd = [sys.executable, str(HERE.parent / "remote" / "qb_track.py"),
               "--imgdir", str(work / "rods" / f"{rid}.imgdir"),
               "--midline", str(work / "rods" / f"{rid}_midline.npz"),
               "--out", str(work / "tracks" / f"{rid}.npz"), "--stride", str(info["stride"])]
        p = subprocess.run(cmd, capture_output=True, text=True)
        shutil.copy(work / "rods" / f"{rid}_truth.npz", work / "tracks" / f"{rid}_truth.npz")
        out = {"id": rid, "ok": p.returncode == 0, "render_s": info["render_s"],
               "total_s": round(time.time() - t0, 1)}
        if p.returncode == 0:
            out.update(json.loads(p.stdout.strip().splitlines()[-1]))
        else:
            out["error"] = p.stderr.strip().splitlines()[-1:] 
        print(json.dumps(out), flush=True)
