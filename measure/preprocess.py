"""Steps applied to a movie before tracking, used by remedies the tracker has no setting for.

All run on the tracker machine inside scripts/remote/qb_track.py. Frames are
(T, H, W) arrays; midlines (T, K, 2) in image (row, col); stage_px (T, 2),
world = image + stage_px.

- register_frames: remove rigid motion that the stage log does not hold, by
  registering a band of non-growing basal tissue frame to frame (OpenCV ECC,
  Euclidean). Assumes that tissue is fixed in the world, the same assumption
  as the closure check. registration_band_start finds where the band can
  start from the measured strain-rate profile of the current record
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


def registration_band_start(rec, fraction=0.05, min_cov=0.5):
    """Arc length (px from the tip) beyond which the window-mean centre strain rate of a record stays
    under `fraction` of its peak. Read from the measurement, never from the truth. None if the
    profile has no finite peak."""
    import warnings
    f = rec.fields
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m = np.nanmean(f["regr_mid"], axis=0)
    m[np.mean(np.isfinite(f["regr_mid"]), axis=0) < min_cov] = np.nan
    if not np.any(np.isfinite(m)) or np.nanmax(m) <= 0:
        return None
    above = np.flatnonzero(m >= fraction * np.nanmax(m))
    s = f["s_grid"]
    return float(s[min(above[-1] + 1, len(s) - 1)])


def _inside(shape, stage, margin):
    """World-frame pixels whose image position (world - stage) lies at least `margin` px inside the frame."""
    r = np.arange(shape[0])[:, None] - stage[0]
    c = np.arange(shape[1])[None, :] - stage[1]
    return (r >= margin) & (r < shape[0] - margin) & (c >= margin) & (c < shape[1] - margin)


def register_frames(frames, stage_px, midline, s_from, s_to, band_px=20.0, edge_px=25.0):
    """Remove unlogged rigid motion. Returns (frames, midline, per-frame 3x3 maps, report).

    World-aligned frames g_t(x) = f_t(x - stage_t) are registered pairwise on
    the basal band (arc length s_from .. s_to px from the tip along the
    previous frame's midline, within band_px of it), keeping only pixels at
    least edge_px inside both frames: g_t(E_t x) = g_{t-1}(x). With
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
        part = line_w[(s >= s_from) & (s <= s_to)]
        mask = _band(f[t].shape, part, band_px) & _inside(f[t].shape, stage_px[t - 1], edge_px)             & _inside(f[t].shape, stage_px[t], edge_px)
        mask = mask.astype(np.uint8)
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
    report = {"ecc_min": float(np.nanmin(ecc)) if ecc else None, "band_px": [round(s_from), round(s_to)],
              "final_rotation_deg": round(angles[-1], 3), "final_shift_px": round(shifts[-1], 2)}
    return out_f, out_m, C, report


def _smooth_linear_ends(a, sigma, axis):
    """Gaussian smoothing with the ends padded by linear extrapolation (odd reflection about the end
    value), so a quantity that changes linearly along the axis comes out unchanged. Padding with the
    end value (mode 'nearest') pulled a steadily moving tip path short (decisions, 2026-10-11)."""
    pad = int(np.ceil(4.0 * sigma))
    if pad == 0:
        return a
    widths = [(0, 0)] * a.ndim
    widths[axis] = (pad, pad)
    padded = np.pad(a, widths, mode="reflect", reflect_type="odd")
    sm = gaussian_filter1d(padded, sigma, axis=axis, mode="nearest", truncate=4.0)
    return np.take(sm, np.arange(pad, pad + a.shape[axis]), axis=axis)


def smooth_midline(midline, level):
    """Gaussian smoothing along s (resampled per frame) and over time, for 'light' or 'strong'.

    Both ends are padded by linear extrapolation, so a straight midline that
    moves at constant velocity comes out unchanged.
    """
    sig_s, sig_t = MIDLINE_SMOOTH[level]
    out = midline.copy()
    for t in range(len(out)):
        line = out[t]
        ok = np.isfinite(line[:, 0])
        step = np.median(np.linalg.norm(np.diff(line[ok], axis=0), axis=1))
        sm = _smooth_linear_ends(line[ok], sig_s / step, axis=0)
        sm[0] = line[ok][0]                       # keep the tip
        out[t, ok] = sm
    if sig_t > 0:
        out = _smooth_linear_ends(out, sig_t, axis=0)
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
