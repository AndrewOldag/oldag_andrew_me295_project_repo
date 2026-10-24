"""Rigidly moved copy of one window of a real movie, for the rigid-invariance check (inbox items 18, 19).

  python real_moved.py --imgdir X.imgdir --midline W_midline.npz --from-h H0 --to-h H1 --out-imgdir Y.imgdir
                       --out-midline Y_midline.npz [--mode whole_pixel --out-ref-imgdir R.imgdir
                       --out-ref-midline R_midline.npz | --mode rotate]

whole_pixel (default, Andrew 2026-10-24): translation only, by whole pixels, round(v t) with the synthetic
rods' velocity (0.5, 0.3) px per 90 s; no rotation, no resampling. Both copies are cropped to the common
area: a reference copy (the cropped window) and the moved copy (the same crop box shifted back by each
frame's offset). The two are compared by rigid invariance.

rotate (2026-10-24 first run): the same rigid motion as the synthetic rods' moved twin (measure/render.py, image_case moved=True):
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

import numpy as np                              # noqa: E402

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
    import cv2
    cv2.setNumThreads(1)
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


def whole_pixel(src, m, win, tw, a):
    """Whole-pixel translation only (inbox item 19): shift d_i = round(v t_i) px, no rotation, no resampling.
    Both copies are cropped to the common area: rows from max d_row, cols from max d_col. Reference copy:
    the crop of each window frame; moved copy: the same box shifted back by d_i, so content moves by +d_i."""
    d = np.rint(np.outer(tw, VELOCITY) * a.shift_scale).astype(int)  # (T, 2) row, col; >= 0
    D = d.max(axis=0)
    t0 = time.time()
    if a.pad:
        return whole_pixel_padded(src, m, win, d, a, t0)
    for name, shift in (("ref", np.zeros_like(d)), ("moved", d)):
        dst = Path(a.out_ref_imgdir if name == "ref" else a.out_imgdir)
        tmp = dst.with_name(dst.name + ".part")
        tmp.mkdir(parents=True, exist_ok=False)
        names = {f"ImageData_Ch0_TP{int(f):07d}.npy": k for k, f in enumerate(win)}
        for p in sorted(src.iterdir()):
            if p.name in names:
                k = names[p.name]
                a3 = np.load(p)
                H, W = a3.shape[-2:]
                r0, c0 = D - shift[k]                                     # box of size (H - D0, W - D1)
                np.save(tmp / p.name, np.ascontiguousarray(a3[:, r0:r0 + H - D[0], c0:c0 + W - D[1]]))
            else:
                os.symlink(p.resolve(), tmp / p.name)
        mid = m["midline_image"][:len(win)] - D + shift[:, None, :]
        out = {k: m[k] for k in m.files}
        out.update(midline_image=mid, seed=mid[0])
        if "mask0" in m.files:
            out["mask0"] = m["mask0"][D[0]:, D[1]:]
        np.savez_compressed(a.out_ref_midline if name == "ref" else a.out_midline, **out)
        os.rename(tmp, dst)
    print(json.dumps({"mode": "whole_pixel", "frames": int(len(win)), "shift_px_end": d[-1].tolist(),
                      "crop_px": D.tolist(), "run_s": round(time.time() - t0, 1)}))


def whole_pixel_padded(src, m, win, d, a, t0):
    """Control (inbox item 20): the same whole-pixel shift without cropping. Moved frame i = window frame i
    shifted by d_i, uncovered pixels set to the frame median (background). Its reference is the window as is."""
    dst = Path(a.out_imgdir)
    tmp = dst.with_name(dst.name + ".part")
    tmp.mkdir(parents=True, exist_ok=False)
    names = {f"ImageData_Ch0_TP{int(f):07d}.npy": k for k, f in enumerate(win)}
    for p in sorted(src.iterdir()):
        if p.name in names:
            k = names[p.name]
            a3 = np.load(p)
            dr, dc = d[k]
            out = np.full_like(a3, np.median(a3[0]).astype(a3.dtype))
            out[:, dr:, dc:] = a3[:, :a3.shape[1] - dr, :a3.shape[2] - dc]
            np.save(tmp / p.name, out)
        else:
            os.symlink(p.resolve(), tmp / p.name)
    out = {k: m[k] for k in m.files}
    mid = m["midline_image"][:len(win)] + d[:, None, :]
    out.update(midline_image=mid, seed=mid[0])
    np.savez_compressed(a.out_midline, **out)
    os.rename(tmp, dst)
    print(json.dumps({"mode": "whole_pixel_padded", "frames": int(len(win)), "shift_px_end": d[-1].tolist(),
                      "run_s": round(time.time() - t0, 1)}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", required=True)
    ap.add_argument("--midline", required=True)
    ap.add_argument("--from-h", type=float, required=True)
    ap.add_argument("--to-h", type=float, required=True)
    ap.add_argument("--out-imgdir", required=True)
    ap.add_argument("--out-midline", required=True)
    ap.add_argument("--mode", choices=["whole_pixel", "rotate"], default="whole_pixel",
                    help="whole_pixel (item 19; needs --out-ref-*) or rotate (the synthetic rods' motion, bilinear)")
    ap.add_argument("--out-ref-imgdir", default=None, help="whole_pixel: cropped reference copy")
    ap.add_argument("--out-ref-midline", default=None)
    ap.add_argument("--shift-scale", type=float, default=1.0, help="whole_pixel: 0 = zero-shift control (item 20)")
    ap.add_argument("--pad", action="store_true",
                    help="whole_pixel control (item 20): no crop; shifted frames padded with background")
    a = ap.parse_args()
    t0 = time.time()
    src, dst = Path(a.imgdir), Path(a.out_imgdir)
    m = np.load(a.midline)
    t = elapsed_s(src)
    win = np.nonzero((t / 3600 >= a.from_h) & (t / 3600 <= a.to_h))[0]
    if "frames" in m.files and not np.array_equal(m["frames"], win):
        raise SystemExit("midline file frames do not match the window")
    tw = t[win] - t[win[0]]
    if a.mode == "whole_pixel":
        if not a.pad and not (a.out_ref_imgdir and a.out_ref_midline):
            ap.error("whole_pixel needs --out-ref-imgdir and --out-ref-midline")
        return whole_pixel(src, m, win, tw, a)
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
