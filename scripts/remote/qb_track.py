"""Run Quantum Borland two-side tracking on one .imgdir and save the raw arrays.

Runs in the tracker environment (envs/qb.yml) with the tracker importable.
Writes the arrays `measure.record.from_tracker_npz` reads: the three tracked
chains in the world frame, edge-frozen masks, stage correction, frame times,
the per-frame midline in the world frame and the settings used.

  python qb_track.py --imgdir X.imgdir --midline X_midline.npz --out X_track.npz
      [--stride 1] [--disk-radius R] [--spacing 15] [--couple]

The midline file holds `midline_image` (T, K, 2; row, col; tip first) for
every frame of the movie, `seed` (frame-0 midline for the tracker) and
`mask0` (frame-0 root mask).
"""
import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from root_kinematics.slidebook_io import load_root_recording
from root_kinematics.stage_correction import cumulative_correction_px
from root_kinematics.tracking import edge_frozen_mask
from two_side_tracking.pipeline import run_two_side


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", required=True)
    ap.add_argument("--midline", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--disk-radius", type=float, default=None)
    ap.add_argument("--spacing", type=float, default=15.0)
    ap.add_argument("--half-fraction", type=float, default=0.5)
    ap.add_argument("--threshold", type=float, default=10.0)
    ap.add_argument("--couple", action="store_true")
    ap.add_argument("--pixel-um", type=float, default=2.105)
    a = ap.parse_args()

    imgdir = Path(a.imgdir)
    rec = load_root_recording(imgdir, pixel_size_um=a.pixel_um, lazy=False)
    keep = np.arange(0, rec.images.shape[0], a.stride)
    rec = replace(rec, images=np.asarray(rec.images)[keep], stage_xy_um=rec.stage_xy_um[keep],
                  elapsed_s=rec.elapsed_s[keep])
    m = np.load(a.midline)
    seed = m["seed"].astype(float)
    mask = m["mask0"].astype(bool) if "mask0" in m.files else None
    mid_img = m["midline_image"][keep].astype(float)

    t0 = time.time()
    res = run_two_side(rec, seed, mask, spacing=a.spacing, half_fraction=a.half_fraction,
                       disk_radius=a.disk_radius, track_centre=True, couple=a.couple,
                       threshold=a.threshold)
    run_s = time.time() - t0

    corr = cumulative_correction_px(rec)                       # (T, 2)
    shape = rec.images.shape[1:]
    frozen = {}
    for name, world in (("centre", res.centre_track), ("left", res.left_track),
                        ("right", res.right_track)):
        raw = world - corr.T[None, :, :]
        frozen[name] = edge_frozen_mask(raw, shape, a.threshold)

    settings = {"tracker": "quantum_borland_v1", "disk_radius": int(res.disk_radius),
                "spacing": a.spacing, "half_fraction": a.half_fraction,
                "threshold": a.threshold, "couple": bool(a.couple), "stride": a.stride,
                "track_centre": True, "used_mask": bool(res.split.used_mask),
                "run_s": round(run_s, 1), "n_frames": int(len(keep))}
    meta = {"root_id": imgdir.stem, "pixel_um": a.pixel_um, "settings": settings}
    np.savez_compressed(
        a.out, meta=json.dumps(meta),
        centre_track=res.centre_track, left_track=res.left_track, right_track=res.right_track,
        centre_frozen=frozen["centre"], left_frozen=frozen["left"], right_frozen=frozen["right"],
        elapsed_s=rec.elapsed_s, stage_px=corr, midline_world=mid_img + corr[:, None, :],
        qb_l_domain=res.l_domain, qb_regr_left=res.regr_left, qb_regr_right=res.regr_right,
        qb_valid_max=res.valid_max)
    print(json.dumps({"out": a.out, "run_s": round(run_s, 1), "frames": int(len(keep)),
                      "points": int(res.centre_track.shape[0]), "disk_radius": int(res.disk_radius)}))


if __name__ == "__main__":
    main()
