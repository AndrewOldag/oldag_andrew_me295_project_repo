"""Growth-zone placement checks (spec 2026-11-23, task c034). Report-only.

Closure uses only the summed tip displacement, so a growth zone displaced
along s can pass every check in `checks.py`. These two compare the reported
profile (window-mean v_mid and regr_mid on s_grid) with what it does not set:
the midline tip path and the tracked points placed by their distance from the
midline tip. Definitions: docs/proposals/2026-11-23_zone-checks.md.
Deterministic, no LLM. Not part of `run_checks`; they gate nothing.
"""
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

from checker.checks import _common_base, _project, _window_mean
from measure.record import PER_S_TO_PCT_PER_H, arclength, derive

ZONE_FILE = Path(__file__).resolve().parents[1] / "config" / "zone_thresholds.yaml"
BASAL_FRACTION = 1.0 / 3.0      # basal part = covered s >= (1 - 1/3) s_end
MIN_TIP_SPEED_PX_H = 10.0       # below: plateau_speed not computable
MIN_DISPLACEMENT_PX = 2.0       # below: relative particle-path values not computable
SUBSTEPS = 4                    # RK4 steps per frame interval


@dataclass
class ZoneResult:
    check: str
    passed: Optional[bool]       # None when no gating value could be computed or no thresholds given
    values: dict
    thresholds: dict = field(default_factory=dict)
    detail: str = ""

    def to_dict(self):
        return asdict(self)


def load_zone_thresholds(path=ZONE_FILE):
    with open(path) as fh:
        return yaml.safe_load(fh)


def _decide(values, thresholds, keys):
    """False if any gating value is over its threshold, True if all computable ones are within, else None."""
    th = thresholds or {}
    got = [(values[k], th[k]) for k in keys if k in th and values.get(k) is not None and np.isfinite(values[k])]
    if not got:
        return None
    return bool(all(v <= t for v, t in got))


def _profile(fields):
    s = np.asarray(fields["s_grid"], float)
    v = _window_mean(fields["v_mid"])
    r = _window_mean(fields["regr_mid"])
    ok = np.isfinite(v)
    return s, v, r, ok


def _along_midline(points, midline):
    """(T,) arc length along each frame's midline from its tip to the projection of points (T, 2)."""
    return np.array([_project(p[None], m)[0][0] if np.isfinite(p[0]) else np.nan
                     for p, m in zip(points, midline)])


def tip_speed_px_h(rec):
    """Growth speed: change over the window of the arc length along the midline from the midline tip
    to the most basal centre point tracked in every frame, over the duration, px/h. None without one."""
    b = _common_base(rec.centre)
    if b is None or b == 0:
        return None
    L = _along_midline(rec.centre[:, b], rec.midline)
    duration_h = (rec.frame_times_s[-1] - rec.frame_times_s[0]) / 3600.0
    return float((L[-1] - L[0]) / duration_h)


def plateau(rec, thresholds=None, fields=None):
    """Past the growth zone the tip-frame profile is flat at the tip speed with zero strain rate.

    plateau_regr: largest |mean regr_mid| over the basal third of the covered span, %/h.
    plateau_speed: |mean v_mid over that part - v_tip| / v_tip.
    """
    s, v, r, ok = _profile(fields if fields is not None else rec.fields)
    if not ok.any():
        return ZoneResult("plateau", None, {"plateau_regr": None, "plateau_speed": None},
                          dict(thresholds or {}), "no covered span")
    s_end = float(s[ok][-1])
    basal = ok & (s >= (1.0 - BASAL_FRACTION) * s_end)
    rb = r[basal]
    regr = float(np.nanmax(np.abs(rb)) * PER_S_TO_PCT_PER_H) if np.isfinite(rb).any() else None
    v_tip = tip_speed_px_h(rec)
    v_base = float(np.mean(v[basal]) * 3600.0)
    speed = abs(v_base - v_tip) / v_tip if v_tip is not None and v_tip >= MIN_TIP_SPEED_PX_H else None
    values = {"plateau_regr": regr, "plateau_speed": speed}
    return ZoneResult("plateau", _decide(values, thresholds, ("plateau_regr", "plateau_speed")), values,
                      dict(thresholds or {}),
                      f"basal part {int(basal.sum())} grid points" +
                      ("" if speed is not None else "; growth speed under 10 px/h or no common base: plateau_speed not computable"))


def tip_frame_positions(rec):
    """(T, M) distance of each centre point from the midline tip: chain arc length plus the arc
    length along the midline from its tip to the first chain point."""
    off = _along_midline(rec.centre[:, 0], rec.midline)
    return arclength(rec.centre) + off[:, None]


def _velocity(s, v, ok):
    """v(S) px/s: linear between finite grid points, last finite value past them, 0 below s = 0."""
    xs, ys = s[ok], v[ok]

    def f(q):
        out = np.interp(q, xs, ys, left=ys[0], right=ys[-1])
        return np.where(q < 0.0, 0.0, out)
    return f


def particle_path(rec, thresholds=None, fields=None, slide_px=0.0):
    """Tracked points moved by the window-mean velocity profile against where they were tracked.

    Integrates dS/dt = v(S) (Silk particle path) from frame 0 to the last frame for every centre
    point tracked in both. pp_rms_px, pp_max_px: residuals, px; pp_rms_rel, pp_max_rel: the same
    over the RMS and the largest of the tracked tip-frame displacements. slide_px (fault injection
    only, c035 detection curve): every tracked point slides along s by slide_px x (t - t0)/(t_end - t0),
    an anchoring drift growing over the window; the profile is unchanged.
    """
    s, v, _, ok = _profile(fields if fields is not None else rec.fields)
    keys = ("pp_rms_px", "pp_max_px", "pp_rms_rel", "pp_max_rel", "pp_mean_px", "tip_offset_change_px",
            "pp_common_px", "pp_shape_rms_px", "pp_shape_max_px", "pp_common_rel", "pp_shape_rel")
    if ok.sum() < 2:
        return ZoneResult("particle_path", None, dict.fromkeys(keys), dict(thresholds or {}), "no covered span")
    S = tip_frame_positions(rec)
    if slide_px:
        t = np.asarray(rec.frame_times_s, float)
        S = S + (slide_px * (t - t[0]) / (t[-1] - t[0]))[:, None]
    seed = np.isfinite(S[0]) & np.isfinite(S[-1])
    if not seed.any():
        return ZoneResult("particle_path", None, dict.fromkeys(keys), dict(thresholds or {}),
                          "no centre point tracked in the first and last frame")
    vel = _velocity(s, v, ok)
    x = S[0, seed].copy()
    for dt in np.diff(np.asarray(rec.frame_times_s, float)):
        h = dt / SUBSTEPS
        for _ in range(SUBSTEPS):
            k1 = vel(x); k2 = vel(x + 0.5 * h * k1); k3 = vel(x + 0.5 * h * k2); k4 = vel(x + h * k3)
            x = x + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    e = x - S[-1, seed]
    d = S[-1, seed] - S[0, seed]
    rms, mx = float(np.sqrt(np.mean(e ** 2))), float(np.max(np.abs(e)))
    dmax = float(np.max(np.abs(d)))
    rel = dmax >= MIN_DISPLACEMENT_PX
    # Diagnostics, not gating: the signed mean residual, and the change over the window of the first chain
    # point's distance from the midline tip (S[:, 0]), a part common to every point's tracked position
    o = S[[0, -1], 0]
    diag = {"pp_mean_px": float(np.mean(e)),
            "tip_offset_change_px": float(o[1] - o[0]) if np.isfinite(o).all() else None}
    # Split (c035, docs/proposals/2026-11-23_zone-reference.md): common mode = mean residual, shape = the rest
    common = float(np.mean(e))
    shape = e - common
    shape_rms = float(np.sqrt(np.mean(shape ** 2)))
    drms = float(np.sqrt(np.mean(d ** 2)))
    split = {"pp_common_px": common, "pp_shape_rms_px": shape_rms, "pp_shape_max_px": float(np.max(np.abs(shape))),
             "pp_common_rel": abs(common) / drms if rel else None, "pp_shape_rel": shape_rms / drms if rel else None}
    values = {"pp_rms_px": rms, "pp_max_px": mx,
              "pp_rms_rel": rms / drms if rel else None,
              "pp_max_rel": mx / dmax if rel else None, **diag, **split}
    return ZoneResult("particle_path", _decide(values, thresholds, ("pp_rms_rel", "pp_max_rel")), values,
                      dict(thresholds or {}),
                      f"{int(seed.sum())} points" + ("" if rel else "; largest displacement under 2 px: "
                                                     "relative values not computable"))


def run_zone_checks(rec, thresholds=None, fields=None):
    th = thresholds or {}
    return [plateau(rec, {k: th[k] for k in ("plateau_regr", "plateau_speed") if k in th}, fields),
            particle_path(rec, {k: th[k] for k in ("pp_rms_rel", "pp_max_rel") if k in th}, fields)]


def shifted_fields(rec, d_px):
    """Derived fields of rec with the profile displaced along s by d_px (fault injection, synthetic
    only): s_grid + d_px, grid points with s < 0 dropped. Tracked points and midline unchanged."""
    f = derive(rec)
    s = f["s_grid"] + d_px
    keep = s >= 0.0
    out = {k: a[:, keep] for k, a in f.items() if k != "s_grid"}
    out["s_grid"] = s[keep]
    return out
