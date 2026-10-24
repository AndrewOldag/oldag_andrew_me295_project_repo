"""Cause test for rigid invariance on a real window (dispatcher inbox item 20, step A). Diagnostic only.

  python scripts/rigid_cause_test.py [--tracks staging/tracks_real] [--margin-shift 40 --disk 14]

Reads the cached tracker outputs of the real slice (whole-pixel reference and moved copies) and the two
controls (zero-shift pair `ctrl_zero_ref.npz`/`ctrl_zero_moved.npz`; padded, uncropped moved copy
`ctrl_pad_moved.npz` against the window as is). Prints: rigid invariance of each pair; for the basal
points (mean s > 250 px) of each chain and copy, the smallest distance to the frame edge, the number of
point-frames within (largest shift + disk radius) of an edge, frozen points; valid frame pairs per s.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker import load_thresholds  # noqa: E402
from checker.checks import rigid_invariance  # noqa: E402
from measure.record import arclength, from_tracker_npz  # noqa: E402

WINDOW = "0708_m12__w4-6"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks", default=str(ROOT / "staging" / "tracks_real"))
    ap.add_argument("--margin-shift", type=int, default=40)
    ap.add_argument("--disk", type=int, default=14)
    ap.add_argument("--frame", default="1160x2376", help="cropped frame size, rows x cols")
    a = ap.parse_args()
    D = Path(a.tracks)
    th = load_thresholds()["rigid_invariance"]
    H, W = (int(x) for x in a.frame.split("x"))
    margin = a.margin_shift + a.disk

    def rig(x, y):
        c = rigid_invariance(from_tracker_npz(D / x), from_tracker_npz(D / y), th)
        return [round(c.value, 6), c.detail, c.where_s_px]

    out = {"controls": {"zero_shift": rig("ctrl_zero_ref.npz", "ctrl_zero_moved.npz"),
                        "padded_no_crop": rig(f"{WINDOW}__st1__L400.npz", "ctrl_pad_moved.npz"),
                        "whole_pixel_cropped": rig(f"{WINDOW}_wp_ref__st1__L400.npz", f"{WINDOW}_wp_moved__st1__L400.npz")},
           "margin_px": margin, "basal_geometry": []}
    for copy in ("ref", "moved"):
        f = D / f"{WINDOW}_wp_{copy}__st1__L400.npz"
        z, rec = np.load(f), from_tracker_npz(f)
        basal = np.nanmean(arclength(rec.centre), axis=0) > 250
        for side in ("centre", "plus", "minus"):
            im = getattr(rec, side) - z["stage_px"][:, None, :]
            de = np.minimum.reduce([im[..., 0], H - 1 - im[..., 0], im[..., 1], W - 1 - im[..., 1]])
            out["basal_geometry"].append({
                "copy": copy, "chain": side, "basal_points": int(basal.sum()),
                "min_dist_to_frame_edge_px": round(float(np.nanmin(de[:, basal])), 1),
                "frames_points_within_margin": int(np.sum(de[:, basal] < margin)),
                "frozen_basal": int(np.isnan(getattr(rec, side)[:, basal, 0]).sum())})
        sg, valid = rec.fields["s_grid"], np.isfinite(rec.fields["regr_mid"]).sum(axis=0)
        out[f"valid_pairs_{copy}"] = {int(x): int(valid[np.argmin(abs(sg - x))])
                                      for x in (100, 250, 300, 350, 375, 400, 425, 450, 475)}
        out[f"n_pairs_{copy}"] = int(rec.fields["regr_mid"].shape[0])
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
