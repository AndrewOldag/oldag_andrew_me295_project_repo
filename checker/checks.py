"""The three checks. Definitions and costs: docs/decisions.md (2026-10-10).

Each check is a plain function of measurement records and returns a
CheckResult: pass or fail, the value, the threshold, and where it failed.
Profiles are window means over frame pairs.
"""
from dataclasses import dataclass, asdict
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

from measure.record import PER_S_TO_PCT_PER_H

THRESHOLDS_FILE = Path(__file__).resolve().parents[1] / "config" / "checker_thresholds.yaml"


@dataclass
class CheckResult:
    check: str
    passed: Optional[bool]       # None when the check could not be run
    value: float
    threshold: Optional[float]
    unit: str
    where_s_px: Optional[float] = None
    where_frame_pair: Optional[int] = None
    detail: str = ""

    def to_dict(self):
        return asdict(self)


def load_thresholds(path=THRESHOLDS_FILE):
    with open(path) as fh:
        return yaml.safe_load(fh)


def _window_mean(a):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)    # all-NaN columns
        return np.nanmean(a, axis=0)


def _decide(value, threshold):
    if threshold is None or not np.isfinite(value):
        return None
    return bool(value <= threshold)


def rigid_invariance(rec, rec_moved, threshold=None):
    """Strain-rate profiles unchanged when a known rigid motion is added.

    value = max over s and over (centre, plus, minus) of the absolute
    difference of the window-mean strain-rate profiles, %/h.
    """
    fa, fb = rec.fields, rec_moved.fields
    n = min(len(fa["s_grid"]), len(fb["s_grid"]))
    s = fa["s_grid"][:n]
    worst, where, which = -np.inf, None, None
    for k in ("regr_mid", "regr_plus", "regr_minus"):
        d = np.abs(_window_mean(fa[k][:, :n]) - _window_mean(fb[k][:, :n])) * PER_S_TO_PCT_PER_H
        if np.all(np.isnan(d)):
            continue
        j = int(np.nanargmax(d))
        if d[j] > worst:
            worst, where, which = float(d[j]), float(s[j]), k
    if where is None:
        return CheckResult("rigid_invariance", None, float("nan"), threshold, "%/h",
                           detail="no overlapping profile")
    return CheckResult("rigid_invariance", _decide(worst, threshold), worst, threshold,
                       "%/h", where_s_px=where, detail=f"largest change in {which}")


def _common_base(centre):
    """Most basal chain index tracked in every frame."""
    ok = np.all(np.isfinite(centre[..., 0]), axis=0)
    idx = np.flatnonzero(ok)
    return int(idx[-1]) if len(idx) else None


def closure(rec, threshold=None):
    """Tip displacement from the stage log against the tracked kinematics.

    Per frame pair: r = d(tip_world) - d(c_0 - c_b). tip_world is the tip from
    the midline source in image coordinates plus the stage log. c_0 - c_b is
    the tip position relative to the most basal tracked point, from the
    tracked chain alone (the stage log cancels in it); its change is the
    integrated strain rate and rotation along the midline. With an anchored
    base the two agree. value = |sum of r| over the window / window duration,
    px/h.
    """
    b = _common_base(rec.centre)
    if b is None or b == 0:
        return CheckResult("closure", None, float("nan"), threshold, "px/h",
                           detail="no basal point tracked in every frame")
    tip_w = rec.midline[:, 0, :]
    rel = rec.centre[:, 0, :] - rec.centre[:, b, :]
    r = np.diff(tip_w, axis=0) - np.diff(rel, axis=0)          # (T-1, 2)
    duration_h = (rec.frame_times_s[-1] - rec.frame_times_s[0]) / 3600.0
    value = float(np.linalg.norm(r.sum(axis=0)) / duration_h)
    tip_speed = float(np.linalg.norm(np.diff(tip_w, axis=0), axis=1).sum() / duration_h)
    worst = int(np.argmax(np.linalg.norm(r, axis=1)))
    s_b = float(np.nanmean(np.linalg.norm(np.diff(rec.centre[:, :b + 1], axis=1), axis=2).sum(axis=1)))
    return CheckResult("closure", _decide(value, threshold), value, threshold, "px/h",
                       where_s_px=s_b, where_frame_pair=worst,
                       detail=f"tip path {tip_speed:.1f} px/h; base at s = {s_b:.0f} px; "
                              f"largest single-pair residual at pair {worst}")


def plane_sections(rec, threshold=None):
    """Flank difference against flank spacing times material curvature rate.

    residual(s) = mean(regr_plus - regr_minus) + mean(spacing * kappa_rate),
    the plane-sections relation for constant width (plus is the +N flank, so
    plus minus minus = -2h dkappa/dt). value = max |residual| over s, %/h.
    """
    f = rec.fields
    diff = _window_mean(f["regr_plus"] - f["regr_minus"])
    pred = -_window_mean(f["spacing"] * f["kappa_rate"])
    res = np.abs(diff - pred) * PER_S_TO_PCT_PER_H
    if np.all(np.isnan(res)):
        return CheckResult("plane_sections", None, float("nan"), threshold, "%/h",
                           detail="no profile where both sides and the midline are covered")
    j = int(np.nanargmax(res))
    return CheckResult("plane_sections", _decide(float(res[j]), threshold), float(res[j]),
                       threshold, "%/h", where_s_px=float(f["s_grid"][j]),
                       detail=f"flank difference {diff[j] * PER_S_TO_PCT_PER_H:.2f} %/h, "
                              f"predicted {pred[j] * PER_S_TO_PCT_PER_H:.2f} %/h")


def run_checks(rec, rec_moved=None, thresholds=None):
    """All three checks. thresholds: dict check -> value, or None for values only."""
    th = (thresholds or {})
    out = []
    if rec_moved is not None:
        out.append(rigid_invariance(rec, rec_moved, th.get("rigid_invariance")))
    else:
        out.append(CheckResult("rigid_invariance", None, float("nan"),
                               th.get("rigid_invariance"), "%/h",
                               detail="no rigidly moved run supplied"))
    out.append(closure(rec, th.get("closure")))
    out.append(plane_sections(rec, th.get("plane_sections")))
    return out
