"""Rigidly moved copy of one window of a real movie, for the rigid-invariance check (inbox item 18).

  python real_moved.py --imgdir X.imgdir --midline W_midline.npz --from-h H0 --to-h H1 --out-imgdir Y.imgdir
                       --out-midline Y_midline.npz

The same rigid motion as the synthetic rods' moved twin (measure/render.py, image_case moved=True):
rotation 0.1 deg per 90 s about the frame-0 tip and translation (0.5, 0.3) px per 90 s in (row, col),
growing with the time since the first window frame. It is unlogged: the stage tables are unchanged.
Applied in image coordinates: window frame i is warped by T_i (bilinear; uncovered pixels take the frame
median), and the window midline (and nothing else) is moved by the same T_i. Every other file of the
movie folder is linked, not copied, so the tracker's loader sees the full frame count. Writes only the
two outputs. Reads only.
"""
import argparse
import json
import os
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import cv2                                      # noqa: E402
import numpy as np                              # noqa: E402

cv2.setNumThreads(1)
ROT_RATE = np.deg2rad(0.1) / 90.0               # rad/s, as measure/render.image_case(moved=True)
VELOCITY = np.array([0.5, 0.3]) / 90.0          # px/s, (row, col)


def transform(t, about):
    """2x2 rotation and offset of T(p) = R (p - about) + about + v t, p in (row, col)."""
    c, s = np.cos(ROT_RATE * t), np.sin(ROT_RATE * t)
    R = np.array([[c, -s], [s, c]])
    return R, about - R @ about + VELOCITY * t


def move_points(P, t, about):
    R, b = transform(t, about)
    return P @ R.T + b


def warp(img, t, about):
    R, b = transform(t, about)
    # (row, col) map -> OpenCV (x=col, y=row) forward matrix
    M = np.array([[R[1, 1], R[1, 0], b[1]], [R[0, 1], R[0, 0], b[0]]])
    fill = float(np.median(img))
    return cv2.warpAffine(img.astype(np.float32), M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=fill)


def elapsed_s(imgdir):
    import re
    txt = (imgdir / "ElapsedTimes.yaml").read_text()
    v = [float(x) for x in re.search(r"theElapsedTimes:\s*\[(.*?)\]", txt, re.S).group(1).split(",") if x.strip()]
    return np.array(v[1:]) / 1000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", required=True)
    ap.add_argument("--midline", required=True)
    ap.add_argument("--from-h", type=float, required=True)
    ap.add_argument("--to-h", type=float, required=True)
    ap.add_argument("--out-imgdir", required=True)
    ap.add_argument("--out-midline", required=True)
    a = ap.parse_args()
    t0 = time.time()
    src, dst = Path(a.imgdir), Path(a.out_imgdir)
    m = np.load(a.midline)
    t = elapsed_s(src)
    win = np.nonzero((t / 3600 >= a.from_h) & (t / 3600 <= a.to_h))[0]
    if "frames" in m.files and not np.array_equal(m["frames"], win):
        raise SystemExit("midline file frames do not match the window")
    tw = t[win] - t[win[0]]
    about = np.asarray(m["midline_image"][0, 0], float)        # frame-0 tip, (row, col)
    tmp = dst.with_name(dst.name + ".part")
    tmp.mkdir(parents=True, exist_ok=False)
    names = {f"ImageData_Ch0_TP{int(f):07d}.npy": k for k, f in enumerate(win)}
    for p in sorted(src.iterdir()):
        if p.name in names:
            k = names[p.name]
            a3 = np.load(p)
            img = warp(a3[0], tw[k], about)
            np.save(tmp / p.name, np.clip(np.round(img), 0, np.iinfo(a3.dtype).max).astype(a3.dtype)[None])
        else:
            os.symlink(p.resolve(), tmp / p.name)
    mid = np.stack([move_points(m["midline_image"][k], tw[k], about) for k in range(len(win))])
    out = {k: m[k] for k in m.files}
    out.update(midline_image=mid, seed=mid[0])
    np.savez_compressed(a.out_midline, **out)
    os.rename(tmp, dst)
    print(json.dumps({"frames_moved": int(len(win)), "rotation_deg_end": round(float(np.rad2deg(ROT_RATE * tw[-1])), 2),
                      "shift_px_end": np.round(VELOCITY * tw[-1], 1).tolist(), "run_s": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main()
