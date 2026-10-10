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
from measure.render import DEV_FAULTS, build, image_case, rod_id  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--case", default="growth_zone")
ap.add_argument("--fault", choices=DEV_FAULTS, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--moved", action="store_true", help="add the rigid motion of the invariance check")
ap.add_argument("--width-kappa-inv", type=float, default=None, help="width_change curvature 1/K px (default 400)")
ap.add_argument("--rotation-deg", type=float, default=None, help="rigid_rotation rate, deg/frame (default 0.1)")
ap.add_argument("--dry-run", action="store_true", help="print the id and stride only")
a = ap.parse_args()
t0 = time.time()
if a.dry_run:
    _, movie = image_case(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg)
    rid = rod_id(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg)
    print(json.dumps({"id": rid, "stride": movie.stride}))
    sys.exit(0)
rid = build(a.out, a.case, a.fault, a.seed, a.moved, width_kappa_inv=a.width_kappa_inv,
            rotation_deg=a.rotation_deg)
_, movie = image_case(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg)
print(json.dumps({"id": rid, "stride": movie.stride, "render_s": round(time.time() - t0, 1)}))
