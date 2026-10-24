"""Provisional midline for one time window of a real movie, in the file qb_track.py reads.

No midline source exists yet for real movies. This one follows the medial
line of a dark-root segmentation (the same segmentation as the provisional
real frame_quality reference, docs/decisions.md 2026-10-13). It is for the
tracker timing of spec 2026-10-23 B2, not for results.

  python real_midline.py --imgdir X.imgdir --from-h 2 --to-h 4 --out X_midline.npz

Per frame: dark-root mask (largest component), skeleton, longest geodesic
path. The tip end is the end away from the image border (else the end that
moves more in the world frame); each later frame is oriented to the previous tip. Every frame is
resampled to the same number of points (about 2 px apart in frame 0).
Writes `midline_image` (T, K, 2; row, col; tip first) for the window frames,
`seed`, `mask0` and `frames` (movie frame indices). Reads only.
"""
import argparse
import json
import os
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np                              # noqa: E402
from scipy import ndimage as ndi                # noqa: E402
from scipy.sparse import csr_matrix             # noqa: E402
from scipy.sparse.csgraph import dijkstra       # noqa: E402
from skimage.morphology import skeletonize      # noqa: E402

from root_kinematics.slidebook_io import load_root_recording
from root_kinematics.stage_correction import cumulative_correction_px


EDGE_PX = 40.0          # an end this close to the image border is the cut base


def window_frames(elapsed_s, from_h, to_h):
    t_h = np.asarray(elapsed_s) / 3600.0
    return np.nonzero((t_h >= from_h) & (t_h <= to_h))[0]


def root_mask(img):
    sm = ndi.gaussian_filter(img, 4.0)
    bg = ndi.median_filter(ndi.zoom(img, 0.1, order=1), size=15)
    bg = ndi.zoom(bg, (img.shape[0] / bg.shape[0], img.shape[1] / bg.shape[1]), order=1)
    m = sm < 0.85 * bg
    m[:5], m[-5:], m[:, :5], m[:, -5:] = False, False, False, False
    lab, n = ndi.label(m)
    if n == 0:
        return None
    k = 1 + int(np.argmax(np.bincount(lab.ravel())[1:]))
    return ndi.binary_fill_holes(ndi.binary_opening(lab == k, iterations=3))


def longest_path(mask):
    """Skeleton geodesic diameter as an ordered (M, 2) row, col array."""
    skel = skeletonize(ndi.binary_opening(mask, iterations=6))   # root hairs drop out
    ys, xs = np.nonzero(skel)
    n = len(ys)
    if n < 2:
        return None
    index = -np.ones(skel.shape, np.int64)
    index[ys, xs] = np.arange(n)
    rows, cols, wts = [], [], []
    for dy, dx in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        ny, nx = ys + dy, xs + dx
        ok = (ny >= 0) & (ny < skel.shape[0]) & (nx >= 0) & (nx < skel.shape[1])
        nb = -np.ones(n, np.int64)
        nb[ok] = index[ny[ok], nx[ok]]
        m = nb >= 0
        rows.append(np.nonzero(m)[0]); cols.append(nb[m]); wts.append(np.full(int(m.sum()), np.hypot(dy, dx)))
    g = csr_matrix((np.concatenate(wts), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    d0 = dijkstra(g, indices=0); d0[~np.isfinite(d0)] = -1
    a = int(d0.argmax())
    da, pred = dijkstra(g, indices=a, return_predecessors=True); da[~np.isfinite(da)] = -1
    j, path = int(da.argmax()), []
    while j != a and j >= 0:
        path.append(j); j = pred[j]
    path.append(a)
    return np.array([[ys[k], xs[k]] for k in path[::-1]], float)


def resample(P, k):
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    u = np.linspace(0.0, s[-1], k)
    return np.column_stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", required=True)
    ap.add_argument("--from-h", type=float, required=True)
    ap.add_argument("--to-h", type=float, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pixel-um", type=float, default=2.105)
    a = ap.parse_args()
    t0 = time.time()
    rec = load_root_recording(Path(a.imgdir), pixel_size_um=a.pixel_um, lazy=True)
    frames = window_frames(rec.elapsed_s, a.from_h, a.to_h)
    corr = cumulative_correction_px(rec)[frames]                   # (T, 2) row, col
    paths, mask0 = [], None
    for i, f in enumerate(frames):
        m = root_mask(np.asarray(rec.images[int(f)], float))
        if m is None:
            raise SystemExit(f"no root found in frame {int(f)}")
        if i == 0:
            mask0 = m
        P = longest_path(m)
        if P is None:
            raise SystemExit(f"no midline in frame {int(f)}")
        paths.append(P)
    # tip: the end away from the image border (the base leaves the frame); if
    # neither or both ends are at the border, the end that moves more in the world frame
    first, last = paths[0] + corr[0], paths[-1] + corr[-1]
    shape = mask0.shape
    edge = [min(P[e][0], P[e][1], shape[0] - 1 - P[e][0], shape[1] - 1 - P[e][1]) < EDGE_PX
            for P in (paths[0],) for e in (0, -1)]
    if edge[0] != edge[1]:
        tip = first[-1] if edge[0] else first[0]
    else:
        move = [min(np.linalg.norm(last[[0, -1]] - first[e], axis=1)) for e in (0, -1)]
        tip = first[0] if move[0] > move[1] else first[-1]
    for i, P in enumerate(paths):
        w = P + corr[i]
        if np.linalg.norm(w[-1] - tip) < np.linalg.norm(w[0] - tip):
            P = P[::-1]; w = w[::-1]
        paths[i], tip = P, w[0]
    k = max(50, int(round(np.linalg.norm(np.diff(paths[0], axis=0), axis=1).sum() / 2.0)))
    mid = np.stack([resample(P, k) for P in paths])
    np.savez_compressed(a.out, midline_image=mid, seed=mid[0], mask0=mask0, frames=frames)
    print(json.dumps({"out": a.out, "frames": int(len(frames)), "first_frame": int(frames[0]),
                      "points": k, "length_px_frame0": round(float(np.linalg.norm(np.diff(mid[0], axis=0),
                                                                                    axis=1).sum()), 1),
                      "run_s": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main()
