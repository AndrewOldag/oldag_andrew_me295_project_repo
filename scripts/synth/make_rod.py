"""Render one image-level synthetic rod.

  python scripts/synth/make_rod.py --out DIR --case growth_zone [--fault low_texture] [--seed 0] [--moved]

Writes DIR/<id>.imgdir (tracker input), DIR/<id>_midline.npz (midline source,
tracker seed, frame-0 mask, track length) and DIR/<id>_truth.npz, then
DIR/<id>.ok, and prints <id> and the analysis stride. Refuses a rod whose
.imgdir exists (write once). Held-out faults are rendered by
measure/render_heldout.py.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from measure import render, render_heldout  # noqa: E402
from measure.render import DEV_FAULTS, rod_id  # noqa: E402
from measure.render_heldout import HELDOUT_FAULTS  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--case", default="growth_zone")
ap.add_argument("--fault", choices=DEV_FAULTS + HELDOUT_FAULTS, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--moved", action="store_true", help="add the rigid motion of the invariance check")
ap.add_argument("--width-kappa-inv", type=float, default=None, help="width_change curvature 1/K px (default 400)")
ap.add_argument("--rotation-deg", type=float, default=None, help="rigid_rotation rate, deg/frame (default 0.1)")
ap.add_argument("--size", default=None, help="fault size, see measure.render.fault_settings")
ap.add_argument("--dry-run", action="store_true", help="print the id and stride only")
a = ap.parse_args()
build, image_case = ((render_heldout.build, render_heldout.image_case) if a.fault in HELDOUT_FAULTS
                     else (render.build, render.image_case))
t0 = time.time()
if a.dry_run:
    _, movie = image_case(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg, a.size)
    rid = rod_id(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg, a.size)
    print(json.dumps({"id": rid, "stride": movie.stride}))
    sys.exit(0)
rid = rod_id(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg, a.size)
if (Path(a.out) / f"{rid}.imgdir").exists():          # write once: never overwrite a rendered rod (CLAUDE.md)
    sys.exit(f"rod exists, not overwritten: {rid}")
rid = build(a.out, a.case, a.fault, a.seed, a.moved, width_kappa_inv=a.width_kappa_inv,
            rotation_deg=a.rotation_deg, size=a.size)
fd = os.open(Path(a.out) / f"{rid}.ok", os.O_CREAT | os.O_EXCL | os.O_WRONLY)    # the rod is complete
os.close(fd)
_, movie = image_case(a.case, a.fault, a.seed, a.moved, a.width_kappa_inv, a.rotation_deg, a.size)
print(json.dumps({"id": rid, "stride": movie.stride, "render_s": round(time.time() - t0, 1)}))
