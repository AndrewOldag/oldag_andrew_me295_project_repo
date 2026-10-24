"""Run Quantum Borland two-side tracking on one .imgdir and save the raw arrays.

Runs in the tracker environment (envs/qb.yml) with the tracker importable.
Writes the arrays `measure.record.from_tracker_npz` reads: the three tracked
chains in the world frame, edge-frozen masks, stage correction, frame times,
the per-frame midline in the world frame and the settings used.

  python qb_track.py --imgdir X.imgdir --midline X_midline.npz --out X_track.npz
      [--stride 1] [--disk-radius R] [--spacing 15] [--couple]
      [--register] [--midline-smooth light|strong]
      [--band-mask mask_second_root|crop_to_main_root]

The last three run before tracking (measure/preprocess.py); they carry out
remedies the tracker has no setting for.

The midline file holds `midline_image` (T, K, 2; row, col; tip first) for
every frame of the movie, `seed` (frame-0 midline for the tracker) and
`mask0` (frame-0 root mask).
"""
import argparse
import json
import os
import sys
import time
from dataclasses import replace
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"                       # one thread per run on the shared machine (decisions, 2026-10-11)

import cv2                                      # noqa: E402
import numpy as np                              # noqa: E402
import torch                                    # noqa: E402

cv2.setNumThreads(1)
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from measure import preprocess                                 # noqa: E402
from measure.render import seed_midline                         # noqa: E402

from root_kinematics.slidebook_io import load_root_recording
from root_kinematics.stage_correction import cumulative_correction_px
from root_kinematics.tracking import edge_frozen_mask
from two_side_tracking.pipeline import run_two_side


def mark_done(path):
    """Create <path>.ok, once (O_EXCL). Its presence marks <path> complete."""
    fd = os.open(f"{path}.ok", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.close(fd)


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
    ap.add_argument("--couple-lambda", type=float, default=2.0, help="inextensibility weight (tracker default 2.0)")
    ap.add_argument("--couple-mu", type=float, default=2.0, help="smoothness weight (tracker default 2.0)")
    ap.add_argument("--pixel-um", type=float, default=2.105)
    ap.add_argument("--register", action="store_true")
    ap.add_argument("--register-from-px", type=float, default=None,
                    help="registration band start, px from the tip (preprocess.registration_band_start)")
    ap.add_argument("--register-to-px", type=float, default=None,
                    help="registration band end, px from the tip (default: the basal end of the midline)")
    ap.add_argument("--midline-smooth", choices=sorted(preprocess.MIDLINE_SMOOTH), default=None)
    ap.add_argument("--band-mask", choices=["mask_second_root", "crop_to_main_root"], default=None)
    ap.add_argument("--band-radius", type=float, default=45.0, help="px, for --band-mask and frame quality")
    ap.add_argument("--movie", choices=["synthetic", "real"], default="synthetic",
                    help="selects the frame_quality reference in measure/info.py")
    ap.add_argument("--track-length", type=float, default=None,
                    help="px of midline handed to the tracker (default: the rod's own, from the midline file; "
                         "400 for files without it)")
    a = ap.parse_args()
    if Path(a.out).exists():
        sys.exit(f"output exists, not overwritten: {Path(a.out).name}")

    imgdir = Path(a.imgdir)
    rec = load_root_recording(imgdir, pixel_size_um=a.pixel_um, lazy=False)
    keep = np.arange(0, rec.images.shape[0], a.stride)
    rec = replace(rec, images=np.asarray(rec.images)[keep], stage_xy_um=rec.stage_xy_um[keep],
                  elapsed_s=rec.elapsed_s[keep])
    m = np.load(a.midline)
    mask = m["mask0"].astype(bool) if "mask0" in m.files else None
    mid_img = m["midline_image"][keep].astype(float)
    if a.track_length is None:
        a.track_length = float(m["track_length"]) if "track_length" in m.files else 400.0
    corr0 = cumulative_correction_px(rec)
    pre = {}
    if a.midline_smooth:
        mid_img = preprocess.smooth_midline(mid_img, a.midline_smooth, corr0)   # time smoothing in the world frame
    if a.register:
        if a.register_from_px is None:
            ap.error("--register needs --register-from-px")
        frames, mid_img, _, pre["register"] = preprocess.register_frames(
            np.asarray(rec.images), corr0, mid_img, a.register_from_px,
            np.inf if a.register_to_px is None else a.register_to_px)
        rec = replace(rec, images=frames)
    if a.band_mask:
        rec = replace(rec, images=preprocess.band_mask(np.asarray(rec.images), mid_img,
                                                       a.band_radius, a.band_mask))
    seed = seed_midline(mid_img[0], a.track_length)   # same as the saved seed when nothing changed it
    quality = preprocess.frame_quality(np.asarray(rec.images), mid_img, a.band_radius)

    t0 = time.time()
    res = run_two_side(rec, seed, mask, spacing=a.spacing, half_fraction=a.half_fraction,
                       disk_radius=a.disk_radius, track_centre=True, couple=a.couple,
                       couple_lambda=a.couple_lambda, couple_mu=a.couple_mu,
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
                "couple_lambda": a.couple_lambda, "couple_mu": a.couple_mu,
                "threads": {"torch": torch.get_num_threads(), "opencv": cv2.getNumThreads()},
                "track_centre": True, "used_mask": bool(res.split.used_mask),
                "run_s": round(run_s, 1), "n_frames": int(len(keep)),
                "register": bool(a.register), "midline_smooth": a.midline_smooth,
                "band_mask": a.band_mask, "movie": a.movie, "track_length": a.track_length, "preprocess": pre, "frame_quality": quality}
    meta = {"root_id": imgdir.stem, "pixel_um": a.pixel_um, "settings": settings}
    # Write once, never rename or overwrite (no move or rename on the lab server, CLAUDE.md; spec audit rules-2).
    # The output is complete only when <out>.ok exists; a stopped run leaves the .npz without it
    with open(a.out, "xb") as fh:
        np.savez_compressed(
            fh, meta=json.dumps(meta),
        centre_track=res.centre_track, left_track=res.left_track, right_track=res.right_track,
        centre_frozen=frozen["centre"], left_frozen=frozen["left"], right_frozen=frozen["right"],
        elapsed_s=rec.elapsed_s, stage_px=corr, midline_world=mid_img + corr[:, None, :],
        qb_l_domain=res.l_domain, qb_regr_left=res.regr_left, qb_regr_right=res.regr_right,
            qb_valid_max=res.valid_max)
    mark_done(a.out)
    print(json.dumps({"out": a.out, "run_s": round(run_s, 1), "frames": int(len(keep)),
                      "points": int(res.centre_track.shape[0]), "disk_radius": int(res.disk_radius)}))


if __name__ == "__main__":
    main()
