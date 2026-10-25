"""Spatial spline fit of a midline, per frame (docs/proposals/2026-10-23_real-midline-smoothing.md, option 1).

Approved by Andrew 2026-10-23 (inbox item 17). Midline source only: the checker, `curvature_smooth_px` and
freeze v3 are unchanged. One parameter, fixed before any real-movie result: the fit residual equals the
pixel quantization, rms 1/sqrt(12) = 0.289 px, i.e. smoothing factor s = K x 0.289^2 for K points
(scipy `splprep`, cubic, parametric in x and y). No extra end conditions.
"""
import numpy as np
from scipy.interpolate import splev, splprep

QUANT_RMS_PX = 1.0 / np.sqrt(12.0)


def spline_fit(points, rms=QUANT_RMS_PX):
    """(K, 2) polyline -> (K, 2) smoothing-spline fit at the same parameter values. NaN rows are kept as NaN;
    fewer than 5 finite points are returned unchanged."""
    P = np.asarray(points, float)
    out = P.copy()
    ok = np.all(np.isfinite(P), axis=1)
    Q = P[ok]
    if len(Q) < 5:
        return out
    keep = np.concatenate([[True], np.linalg.norm(np.diff(Q, axis=0), axis=1) > 1e-9])
    Qk = Q[keep]
    if len(Qk) < 5:
        return out
    tck, u = splprep([Qk[:, 0], Qk[:, 1]], s=len(Qk) * rms ** 2, k=3)
    fit = np.column_stack(splev(u, tck))
    full = np.empty_like(Q)
    full[keep] = fit
    for i in np.nonzero(~keep)[0]:            # repeated points take the fit of the point they repeat
        full[i] = full[i - 1]
    out[ok] = full
    return out


def fit_midlines(midlines, rms=QUANT_RMS_PX):
    """(T, K, 2) midlines, one fit per frame."""
    return np.stack([spline_fit(m, rms) for m in np.asarray(midlines, float)])
