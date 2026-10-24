"""batch_midlines output (one window) -> the midline file qb_track.py reads (window mode).

usage: python net_to_midline.py QB_CODE HTPMID.npz SEG_MIDLINE.npz OUT.npz
Per frame: valley map -> polyline (threshold 128, 10.5 um spacing; htpmid_to_csv.valley_to_polyline),
tip-first order over the sequence (htpmid_to_csv.orient_sequence), resampled to K points (K from frame 0
at about 2 px spacing). mask0 and the movie frame list come from the segmentation midline file of the
same window (mask0 is used only to split the flanks).
"""
import json
import sys
from pathlib import Path

import numpy as np

qb = Path(sys.argv[1]); sys.path.insert(0, str(qb / "scripts"))
from htpmid_to_csv import orient_sequence, valley_to_polyline  # noqa: E402

z = np.load(sys.argv[2], allow_pickle=True)
seg = np.load(sys.argv[3])
tf = z["transform"].item() if z["transform"].dtype == object else json.loads(str(z["transform"]))
frames = np.asarray(z["frames"], int)
assert np.array_equal(frames, seg["frames"]), (frames[:3], seg["frames"][:3])
polys = [valley_to_polyline(v, float(tf["scale"]), valley_thresh=128, spacing=10.5 / 2.105) for v in z["midline"]]
bad = [int(f) for f, p in zip(frames, polys) if p is None or len(p) < 5]
if bad:
    raise SystemExit(f"no midline on frames {bad}")
orient_sequence(polys, np.asarray(z["tip_xy"], float), np.asarray(z["tip_val"], float))
rc = [p[:, ::-1] for p in polys]                                   # (x, y) -> (row, col), tip first


def resample(P, k):
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    u = np.linspace(0.0, s[-1], k)
    return np.column_stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])])


L0 = float(np.linalg.norm(np.diff(rc[0], axis=0), axis=1).sum())
k = max(50, int(round(L0 / 2.0)))
mid = np.stack([resample(P, k) for P in rc])
np.savez_compressed(sys.argv[4], midline_image=mid, seed=mid[0], mask0=seg["mask0"], frames=frames,
                    tip_val=np.asarray(z["tip_val"], float))
print(json.dumps({"frames": int(len(frames)), "points": k, "length_px_frame0": round(L0, 1),
                  "tip_conf_median": round(float(np.median(z["tip_val"])), 3),
                  "tip_dist_to_seg_tip_px_median": round(float(np.median(np.linalg.norm(mid[:, 0] - seg["midline_image"][:, 0], axis=1))), 1)}))
