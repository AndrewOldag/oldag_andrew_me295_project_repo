"""Evidence for request_info, computed from the measurement record and the check results.

One function per info kind in agents/actions.py INFO_KINDS. Each returns a
small JSON-serializable dict. The truth of a synthetic rod is never read here.
"""
import warnings
from pathlib import Path

import numpy as np
import yaml

from measure.record import PER_S_TO_PCT_PER_H

FRAME_QUALITY_REFERENCE = Path(__file__).resolve().parents[1] / "config" / "frame_quality_reference.yaml"


def _wmean(a):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m = np.nanmean(a, axis=0)
    m[np.mean(np.isfinite(a), axis=0) < 0.5] = np.nan
    return m


def _r(x, n=2):
    return None if x is None or not np.isfinite(x) else round(float(x), n)


def check_report(rec, checks):
    return {"checks": [{"check": c.check, "passed": c.passed, "value": _r(c.value, 3),
                        "threshold": c.threshold, "unit": c.unit,
                        "where_s_um": _r(c.where_s_px * rec.pixel_um, 0) if c.where_s_px is not None else None,
                        "where_frame_pair": c.where_frame_pair, "detail": c.detail} for c in checks],
            "settings": {k: rec.settings.get(k) for k in ("stride", "disk_radius", "register",
                                                          "midline_smooth", "band_mask", "n_frames")}}


def velocity_profile(rec, checks=None, step_um=50.0):
    f = rec.fields
    s_um = f["s_grid"] * rec.pixel_um
    v = _wmean(f["v_mid"]) * rec.pixel_um * 3600.0             # um/h
    regr = _wmean(f["regr_mid"]) * PER_S_TO_PCT_PER_H
    grid = np.arange(0.0, np.nanmax(s_um[np.isfinite(regr)]) + 1e-9, step_um)
    tip = rec.midline[:, 0]
    dur_h = (rec.frame_times_s[-1] - rec.frame_times_s[0]) / 3600.0
    spacing_rate = flank_spacing_rate(rec)
    return {"s_um": [round(x) for x in grid],
            "velocity_um_per_h": [_r(x, 1) for x in np.interp(grid, s_um, v)],
            "strain_rate_pct_per_h": [_r(x, 1) for x in np.interp(grid, s_um, regr)],
            "peak_strain_rate_pct_per_h": _r(np.nanmax(regr), 1),
            "peak_at_um": _r(s_um[np.nanargmax(regr)], 0),
            "negative_strain_rate_min_pct_per_h": _r(np.nanmin(regr), 1),
            "basal_velocity_um_per_h": _r(v[np.isfinite(v)][-1], 1),
            "tip_path_um_per_h": _r(np.linalg.norm(np.diff(tip, axis=0), axis=1).sum() * rec.pixel_um / dur_h, 1),
            "tip_net_displacement_um_per_h": _r(np.linalg.norm(tip[-1] - tip[0]) * rec.pixel_um / dur_h, 1),
            "flank_spacing_rate_pct_per_h": [_r(x, 1) for x in np.interp(grid, s_um, spacing_rate)],
            "flank_spacing_rate_max_abs_pct_per_h": (_r(np.nanmax(np.abs(spacing_rate)), 1)
                                                     if np.isfinite(spacing_rate).any() else None)}


def flank_spacing_rate(rec):
    """Window mean of d ln(flank spacing)/dt on the record's s grid, %/h (P4, 2026-10-12).
    A width change shows here; a constant-width root gives about zero."""
    sp = np.asarray(rec.fields["spacing"], dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        ln = np.log(np.where(sp > 0, sp, np.nan))
    dt = np.diff(rec.frame_times_s)
    dt = dt[:len(sp)]                                          # one row of fields per frame pair
    t_mid = np.cumsum(dt) - dt / 2.0
    rate = np.diff(ln, axis=0) / np.diff(t_mid)[:, None]       # 1/s
    return _wmean(rate) * PER_S_TO_PCT_PER_H


def width_free_ratio(rec, step_um=50.0):
    """(plus - minus) / (plus + minus) of the window-mean flank strain rates, where the sum exceeds 5 %/h."""
    f = rec.fields
    s_um = f["s_grid"] * rec.pixel_um
    p, m = _wmean(f["regr_plus"]), _wmean(f["regr_minus"])
    total = (p + m) * PER_S_TO_PCT_PER_H
    ratio = np.where(total > 5.0, (p - m) / (p + m), np.nan)
    grid = np.arange(0.0, np.nanmax(s_um[np.isfinite(ratio)]) + 1e-9, step_um) if np.isfinite(ratio).any() else []
    return {"width_free_ratio_s_um": [round(x) for x in grid],
            "width_free_ratio": [_r(x, 3) for x in np.interp(grid, s_um, ratio)] if len(grid) else []}


def displacement_vs_patch_radius(rec, checks=None):
    """Motion per analysed frame pair against the tracker's disk radius.

    The tip displacement comes from the midline source and the stage log,
    independent of the patch tracker. The tracked displacement is that of the
    centre chain in the world frame.
    """
    tip = rec.midline[:, 0]
    tip_step = np.linalg.norm(np.diff(tip, axis=0), axis=1)
    c = rec.centre
    d = np.linalg.norm(np.diff(c, axis=0), axis=2)               # (T-1, M)
    lost = float(np.mean(~np.isfinite(c[..., 0])))
    radius = rec.settings.get("disk_radius")
    return {"disk_radius_px": radius,
            "frame_stride": rec.settings.get("stride"),
            "frame_interval_s": _r(np.median(np.diff(rec.frame_times_s)), 0),
            "tip_px_per_pair_median": _r(np.median(tip_step)),
            "tip_px_per_pair_max": _r(np.max(tip_step)),
            "tracked_px_per_pair_median": _r(np.nanmedian(d)),
            "tracked_px_per_pair_p95": _r(np.nanpercentile(d, 95)),
            "tip_step_over_radius": _r(np.median(tip_step) / radius, 2) if radius else None,
            "fraction_points_lost": _r(lost, 3)}


def midline_jitter(rec, checks=None):
    """Sideways offset of the midline source from the tracked centre points, per frame.

    jitter = RMS frame-to-frame change of that offset; a smooth midline that
    follows the tissue gives small values.
    """
    offs = []
    for t in range(rec.n_frames):
        line = rec.midline[t]
        line = line[np.isfinite(line[:, 0])]
        pts = rec.centre[t][np.isfinite(rec.centre[t][:, 0])]
        from scipy.spatial import cKDTree
        _, j = cKDTree(line).query(pts)
        j = np.clip(j, 1, len(line) - 2)
        tng = line[j + 1] - line[j - 1]
        tng /= np.linalg.norm(tng, axis=1, keepdims=True)
        nrm = np.stack([-tng[:, 1], tng[:, 0]], axis=1)
        o = np.full(rec.centre.shape[1], np.nan)
        o[np.isfinite(rec.centre[t][:, 0])] = np.sum((pts - line[j]) * nrm, axis=1)
        offs.append(o)
    offs = np.array(offs)
    step = np.diff(offs, axis=0)
    tipjit = np.linalg.norm(np.diff(np.diff(rec.midline[:, 0], axis=0), axis=0), axis=1)
    return {"sideways_offset_rms_px": _r(np.sqrt(np.nanmean(offs ** 2))),
            "frame_to_frame_change_rms_px": _r(np.sqrt(np.nanmean(step ** 2))),
            "tip_second_difference_rms_px": _r(np.sqrt(np.mean(tipjit ** 2))),
            "midline_smooth": rec.settings.get("midline_smooth")}


def stage_log_summary(rec, checks=None):
    ds = np.linalg.norm(np.diff(rec.stage_px, axis=0), axis=1)
    moves = ds > 0.5
    # closure residual per pair: tip from midline + stage against the tracked chain
    ok = np.all(np.isfinite(rec.centre[..., 0]), axis=0)
    b = int(np.flatnonzero(ok)[-1]) if ok.any() else None
    out = {"stage_moves": int(moves.sum()), "frame_pairs": int(len(ds)),
           "move_size_px_median": _r(np.median(ds[moves])) if moves.any() else None,
           "move_size_px_max": _r(ds.max())}
    if b:
        rel = rec.centre[:, 0] - rec.centre[:, b]
        r = np.linalg.norm(np.diff(rec.midline[:, 0], axis=0) - np.diff(rel, axis=0), axis=1)
        out["closure_residual_px_at_moves"] = _r(np.mean(r[moves])) if moves.any() else None
        out["closure_residual_px_elsewhere"] = _r(np.mean(r[~moves])) if (~moves).any() else None
        # net residual per hour summed over each set of pairs, as the closure check sums it (P1, 2026-10-12)
        rv = np.diff(rec.midline[:, 0], axis=0) - np.diff(rel, axis=0)
        dur_h = (rec.frame_times_s[-1] - rec.frame_times_s[0]) / 3600.0
        out["closure_residual_px_per_h_at_moves"] = _r(np.linalg.norm(rv[moves].sum(axis=0)) / dur_h)
        out["closure_residual_px_per_h_elsewhere"] = _r(np.linalg.norm(rv[~moves].sum(axis=0)) / dur_h)
        v = np.nanmean(rec.fields["v_mid"], axis=1) * 3600.0
        out["velocity_jump_at_moves_px_per_h"] = (_r(np.nanmean(np.abs(v[moves] - np.nanmedian(v))))
                                                  if moves.any() else None)
    return out


def frame_quality(rec, checks=None):
    q = rec.settings.get("frame_quality")
    if not q:
        return {"error": "no frame-quality measures for this record (no images)"}
    ref = yaml.safe_load(FRAME_QUALITY_REFERENCE.read_text())
    return {"frames": q, "note": "texture_contrast: high-pass std / mean inside the root band; "
                                 "focus: mean gradient / mean; bright_objects_over_500px: count",
            "reference": {"basis": ref["basis"], **{k: ref[k] for k in ("texture_contrast", "focus")}}}


INFO = {"check_report": check_report, "velocity_profile": velocity_profile,
        "displacement_vs_patch_radius": displacement_vs_patch_radius,
        "midline_jitter": midline_jitter, "stage_log_summary": stage_log_summary,
        "frame_quality": frame_quality}


def request_info(kind, rec, checks):
    return INFO[kind](rec, checks)
