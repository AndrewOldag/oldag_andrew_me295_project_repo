"""Render one image-level synthetic rod.

  python scripts/synth/make_rod.py --out DIR --case growth_zone [--fault low_texture] [--seed 0] [--moved]

Writes DIR/<id>.imgdir (tracker input), DIR/<id>_midline.npz (midline source,
tracker seed, frame-0 mask) and DIR/<id>_truth.npz, and prints <id> and the
analysis stride.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from measure.render import DEV_FAULTS, build, image_case  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--case", default="growth_zone")
ap.add_argument("--fault", choices=DEV_FAULTS, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--moved", action="store_true", help="add the rigid motion of the invariance check")
a = ap.parse_args()
t0 = time.time()
rid = build(a.out, a.case, a.fault, a.seed, a.moved)
_, movie = image_case(a.case, a.fault, a.seed, a.moved)
print(json.dumps({"id": rid, "stride": movie.stride, "render_s": round(time.time() - t0, 1)}))
