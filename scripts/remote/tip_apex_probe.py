"""Net midline end against the root-mask apex on a few window frames (inbox item 29, control-root rule).

usage: python tip_apex_probe.py QB_CODE HTPMID.npz SEG_MIDLINE.npz FRAMES.imgdir [N]

N (optional): probe only N frames of HTPMID, the first, the last and N-2 evenly spaced between (real calibration
screen, docs/proposals/2026-10-24_real-calibration.md). Without N every HTPMID frame is probed.

HTPMID: batch_midlines output for the probe frames (any subset of the window). SEG_MIDLINE: the window's segmentation
midline (scripts/remote/real_midline.py), for the tip side. Per probe frame: root mask (real_midline.root_mask) of
channel 0; tip direction u = unit(seg tip - seg point 40 px behind it along the seg midline); apex = the mask pixel
within 80 px of the seg tip with the largest projection on u. Net end = the tip end of the net polyline (the same
valley_to_polyline conversion as net_to_midline.py; the end nearer the seg tip). Net tip = the net's own tip point
(`tip_xy`), as autotrace compared it with the mask apex. Prints JSON: per-frame distances to the apex (px) and medians.
Reads only.
"""
import json
import sys
from pathlib import Path

import numpy as np

qb = Path(sys.argv[1]); sys.path.insert(0, str(qb / "scripts")); sys.path.insert(0, str(Path(__file__).parent))
from htpmid_to_csv import valley_to_polyline  # noqa: E402
from real_midline import root_mask  # noqa: E402

z = np.load(sys.argv[2], allow_pickle=True)
seg = np.load(sys.argv[3])
imgdir = Path(sys.argv[4])
tf = z["transform"].item() if z["transform"].dtype == object else json.loads(str(z["transform"]))
seg_frames = list(np.asarray(seg["frames"], int))
pick = np.arange(len(z["frames"]))
if len(sys.argv) > 5:
    pick = np.unique(np.round(np.linspace(0, len(pick) - 1, int(sys.argv[5]))).astype(int))
rows = []
for f, v, txy in zip(np.asarray(z["frames"], int)[pick], np.asarray(z["midline"])[pick],
                     np.asarray(z["tip_xy"], float)[pick]):
    img = np.load(imgdir / f"ImageData_Ch0_TP{f:07d}.npy")
    img = np.asarray(img[0] if img.ndim == 3 else img, float)
    m = root_mask(img)
    P = seg["midline_image"][seg_frames.index(f)]                       # (K, 2) row, col, tip first
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    k = int(np.searchsorted(s, 40.0))
    apex = None
    if k < len(P):                                                      # seg midline shorter than 40 px: no apex
        u = (P[0] - P[k]) / np.linalg.norm(P[0] - P[k])
        ys, xs = np.nonzero(m)
        pts = np.column_stack([ys, xs]).astype(float)
        near = np.linalg.norm(pts - P[0], axis=1) < 80.0
        apex = pts[near][np.argmax((pts[near] - P[0]) @ u)] if near.any() else None
    poly = valley_to_polyline(v, float(tf["scale"]), valley_thresh=128, spacing=10.5 / 2.105)
    if poly is None or apex is None:
        rows.append({"frame": int(f), "end_to_apex_px": None, "seg_tip_in_mask": bool(m[tuple(np.round(P[0]).astype(int))])})
        continue
    rc = poly[:, ::-1]                                                   # (x, y) -> (row, col)
    end = rc[0] if np.linalg.norm(rc[0] - P[0]) < np.linalg.norm(rc[-1] - P[0]) else rc[-1]
    rows.append({"frame": int(f), "end_to_apex_px": round(float(np.linalg.norm(end - apex)), 1),
                 "net_tip_to_apex_px": round(float(np.linalg.norm(txy[::-1] - apex)), 1),
                 "end_behind_apex_px": round(float((apex - end) @ u), 1),
                 "seg_tip_to_apex_px": round(float(np.linalg.norm(P[0] - apex)), 1),
                 "seg_tip_in_mask": bool(m[tuple(np.round(P[0]).astype(int))])})
med = {}
for k in ("end_to_apex_px", "net_tip_to_apex_px"):
    d = [r[k] for r in rows if r.get(k) is not None]
    med["median_" + k] = round(float(np.median(d)), 1) if d else None
print(json.dumps({"frames": rows, **med}))
