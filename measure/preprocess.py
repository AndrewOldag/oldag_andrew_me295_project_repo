"""Steps applied to a movie before tracking, used by remedies the tracker has no setting for.

All run on the tracker machine inside scripts/remote/qb_track.py. Frames are
(T, H, W) arrays; midlines (T, K, 2) in image (row, col); stage_px (T, 2),
world = image + stage_px.

- register_frames: remove rigid motion that the stage log does not hold, by
  registering the basal part of the root frame to frame (OpenCV ECC,
  Euclidean). Assumes the basal tissue is fixed in the world, the same
  assumption as the closure check
- smooth_midline: Gaussian smoothing of the midline source along s and over time
- band_mask: keep only a band around the midline source (mask_second_root), or
  that band's bounding box (crop_to_main_root)
- frame_quality: texture, focus and object count, for request_info
"""
import numpy as np
from scipy.ndimage import gaussian_filter, gaussian_filter1d, label, map_coordinates

MIDLINE_SMOOTH = {"light": (10.0, 1.0), "strong": (25.0, 3.0)}   # (sigma along s, px; sigma in time, frames)


def _arclength(line):
    seg = np.linalg.norm(np.diff(line, axis=0), axis=1)
    return np.concatenate([[0.0], np.cumsum(seg)])


def _band(shape, line, radius):
    """Boolean mask of pixels within `radius` of a polyline (dense enough to treat as points)."""
    from scipy.spatial import cKDTree
    ok = np.isfinite(line[:, 0])
    rows, cols = np.mgrid[0:shape[0], 0:shape[1]]
    d, _ = cKDTree(line[ok]).query(np.stack([rows.ravel(), cols.ravel()], axis=1),
                                   distance_upper_bound=radius + 1)
    return (d <= radius).reshape(shape)


def _affine_cv(R):
    """3x3 (row, col) affine -> 2x3 (x=col, y=row) matrix for OpenCV."""
    P = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], float)
    return (P @ R @ P)[:2]


def _from_cv(W):
    P = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], float)
    return P @ np.vstack([W, [0, 0, 1]]) @ P


def _shift(t):
    M = np.eye(3)
    M[:2, 2] = t
    return M


def register_frames(frames, stage_px, midline, track_length, basal_from=0.6, band_px=20.0):
    """Remove unlogged rigid motion. Returns (frames, midline, per-frame 3x3 maps, report).

    World-aligned frames g_t(x) = f_t(x - stage_t) are registered pairwise on
    the basal band (arc length basal_from x track_length .. track_length of
    the previous frame's midline): g_t(E_t x) = g_{t-1}(x). With
    C_t = E_t ... E_1, the corrected frame is f'_t(u) = f_t(C_t(u + s_t) - s_t).
    """
    import cv2
    T = len(frames)
    f = np.asarray(frames, np.float32)
    world = []
    for t in range(T):
        M = _affine_cv(_shift(-stage_px[t]))          # g_t(x) = f_t(x - s_t): output x reads input x - s_t
        world.append(cv2.warpAffine(f[t], M, f[t].shape[::-1], flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP))
    C = [np.eye(3)]
    ecc = []
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    for t in range(1, T):
        line_w = midline[t - 1] + stage_px[t - 1]
        s = _arclength(line_w)
        part = line_w[(s >= basal_from * track_length) & (s <= track_length)]
        mask = _band(f[t].shape, part, band_px).astype(np.uint8)
        W = np.eye(2, 3, dtype=np.float32)
        try:
            cc, W = cv2.findTransformECC(world[t - 1], world[t], W, cv2.MOTION_EUCLIDEAN, crit, mask, 5)
        except cv2.error:
            cc = float("nan")
        ecc.append(float(cc))
        C.append(_from_cv(W) @ C[-1])
    out_f, out_m = np.empty_like(np.asarray(frames)), np.empty_like(midline)
    for t in range(T):
        A = _shift(-stage_px[t]) @ C[t] @ _shift(stage_px[t])     # u -> C_t(u + s) - s
        out = cv2.warpAffine(f[t], _affine_cv(A), f[t].shape[::-1],
                             flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
        out_f[t] = np.clip(out, 0, np.iinfo(out_f.dtype).max if out_f.dtype.kind == "u" else None)
        Ainv = np.linalg.inv(A)
        pts = np.column_stack([midline[t], np.ones(len(midline[t]))])
        out_m[t] = (pts @ Ainv.T)[:, :2]
    angles = [float(np.degrees(np.arctan2(c[1, 0], c[0, 0]))) for c in C]
    shifts = [float(np.hypot(*(c[:2, 2]))) for c in C]
    report = {"ecc_min": float(np.nanmin(ecc)) if ecc else None,
              "final_rotation_deg": round(angles[-1], 3), "final_shift_px": round(shifts[-1], 2)}
    return out_f, out_m, C, report


def smooth_midline(midline, level):
    """Gaussian smoothing along s (resampled per frame) and over time, for 'light' or 'strong'."""
    sig_s, sig_t = MIDLINE_SMOOTH[level]
    out = midline.copy()
    for t in range(len(out)):
        line = out[t]
        ok = np.isfinite(line[:, 0])
        step = np.median(np.linalg.norm(np.diff(line[ok], axis=0), axis=1))
        sm = gaussian_filter1d(line[ok], sig_s / step, axis=0, mode="nearest")
        sm[0] = line[ok][0]                       # keep the tip
        out[t, ok] = sm
    if sig_t > 0:
        out = gaussian_filter1d(out, sig_t, axis=0, mode="nearest")
    return out


def band_mask(frames, midline, radius_px, mode):
    """mask_second_root: set pixels outside the band to the background level.

    crop_to_main_root: the same, outside the band's bounding box over all
    frames (the frame size is kept so coordinates do not change).
    """
    out = np.array(frames, copy=True)
    bg = np.percentile(frames[0], 5)
    if mode == "crop_to_main_root":
        allpts = midline.reshape(-1, 2)
        allpts = allpts[np.isfinite(allpts[:, 0])]
        r0, c0 = np.floor(allpts.min(0) - radius_px).astype(int)
        r1, c1 = np.ceil(allpts.max(0) + radius_px).astype(int)
        keep = np.zeros(frames.shape[1:], bool)
        keep[max(r0, 0):r1 + 1, max(c0, 0):c1 + 1] = True
        out[:, ~keep] = bg
        return out
    for t in range(len(out)):
        out[t][~_band(out.shape[1:], midline[t], radius_px)] = bg
    return out


def frame_quality(frames, midline, radius_px, sample=(0, -1)):
    """Texture contrast and focus inside the root band, and bright-object count, on sample frames."""
    rows = []
    idx = sorted({i % len(frames) for i in (*sample, len(frames) // 2)})
    for i in idx:
        img = np.asarray(frames[i], float)
        band = _band(img.shape, midline[i], radius_px)
        hp = img - gaussian_filter(img, 3.0)
        gy, gx = np.gradient(gaussian_filter(img, 1.0))
        fg = img > 0.5 * (np.percentile(img, 1) + np.percentile(img, 99))
        lab, n = label(fg)
        sizes = np.bincount(lab.ravel())[1:]
        rows.append({"frame": int(i),
                     "texture_contrast": round(float(hp[band].std() / max(img[band].mean(), 1e-9)), 4),
                     "focus": round(float(np.mean(np.hypot(gx, gy)[band]) / max(img[band].mean(), 1e-9)), 4),
                     "bright_objects_over_500px": int(np.sum(sizes > 500))})
    return rows
