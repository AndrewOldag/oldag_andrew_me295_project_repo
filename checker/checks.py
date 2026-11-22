"""The three checks. Definitions and costs: docs/decisions.md (2026-10-10).

Each check is a plain function of measurement records and returns a
CheckResult: pass or fail, the value, the threshold, and where it failed.
Profiles are window means over frame pairs. A grid point enters a window
mean only where at least MIN_COVERAGE of the frame pairs have a value.
"""
from dataclasses import dataclass, asdict
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

from measure.record import PER_S_TO_PCT_PER_H

MIN_COVERAGE = 0.5
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
        m = np.nanmean(a, axis=0)
    m[np.mean(np.isfinite(a), axis=0) < MIN_COVERAGE] = np.nan
    return m


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


def run_checks(rec, rec_moved=None, thresholds=None, skip=()):
    """All three checks. thresholds: dict check -> value, or None for values only.

    skip: checks not applied (passed None, value still computed). The
    plane-sections check is skipped when the width-free ratio is reported
    (decisions, 2026-10-10).
    """
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
    for r in out:
        if r.check in skip:
            r.passed = None
            r.detail = "skipped: width-free ratio reported; " + r.detail
    return out


# ---------------------------------------------------------------- track integrity (spec 2026-11-20 R3)

INTEGRITY_FILE = Path(__file__).resolve().parents[1] / "config" / "integrity_thresholds.yaml"


def _project(points, line):
    """Arc length along `line` (K, 2) of the nearest point to each of `points` (M, 2), and the distance."""
    line = line[np.isfinite(line[:, 0])]
    a, b = line[:-1], line[1:]
    ab = b - a
    seg = np.linalg.norm(ab, axis=1)
    s0 = np.concatenate([[0.0], np.cumsum(seg)])[:-1]
    d = points[:, None, :] - a[None]
    u = np.clip(np.sum(d * ab[None], axis=2) / np.maximum(seg ** 2, 1e-12)[None], 0.0, 1.0)
    dist = np.linalg.norm(d - u[..., None] * ab[None], axis=2)
    k = np.argmin(dist, axis=1)
    i = np.arange(len(points))
    return s0[k] + u[i, k] * seg[k], dist[i, k]


def track_integrity(rec, thresholds=None):
    """Point order, neighbour gaps and lateral scatter of the centre chain against the midline, per frame.

    inversions: neighbour pairs (both tracked) whose arc length along the frame's midline does not increase from
    tip to base, summed over frames. gap_ratio: largest centre-neighbour distance over the median, largest over
    frames. lateral_px: RMS distance of centre points from the frame's midline. registration_plausible: the
    register_v2 report of a registered track (1 plausible, 0 not); unknown for v1 and unregistered tracks.
    Reported on every track; a gate only for tracks made by a remedy (integrity_gate).
    """
    th = thresholds or {}
    inv, ratio, lat, worst = 0, 0.0, [], (0, 0)
    for t in range(rec.n_frames):
        c = rec.centre[t]
        ok = np.isfinite(c[:, 0])
        line = rec.midline[t]
        if ok.sum() < 3 or np.isfinite(line[:, 0]).sum() < 2:
            continue
        s, dist = _project(c[ok], line)
        pair_ok = ok[:-1] & ok[1:]
        s_full = np.full(len(c), np.nan)
        s_full[ok] = s
        n_inv = int(np.sum(pair_ok & ~(np.diff(s_full) > 0)))
        inv += n_inv
        if n_inv > worst[1]:
            worst = (t, n_inv)
        g = np.linalg.norm(np.diff(c, axis=0), axis=1)[pair_ok]
        if len(g) and np.median(g) > 0:
            ratio = max(ratio, float(np.max(g) / np.median(g)))
        lat.append(dist)
    lateral = float(np.sqrt(np.mean(np.concatenate(lat) ** 2))) if lat else float("nan")
    out = [CheckResult("integrity_inversions", _decide(float(inv), th.get("inversions")), float(inv),
                       th.get("inversions"), "pairs", where_frame_pair=worst[0] if inv else None,
                       detail=f"most in frame {worst[0]} ({worst[1]})" if inv else "point order kept in every frame"),
           CheckResult("integrity_gap_ratio", _decide(ratio, th.get("gap_ratio")), ratio, th.get("gap_ratio"), "ratio"),
           CheckResult("integrity_lateral", _decide(lateral, th.get("lateral_px")), lateral, th.get("lateral_px"), "px")]
    reg = ((rec.settings or {}).get("preprocess") or {}).get("register")
    if reg is None:
        out.append(CheckResult("registration_plausible", None, float("nan"), None, "", detail="not registered"))
    elif "plausible" not in reg:
        out.append(CheckResult("registration_plausible", None, float("nan"), None, "",
                               detail="registered without a plausibility bound (register_frames v1)"))
    else:
        out.append(CheckResult("registration_plausible", bool(reg["plausible"]), float(bool(reg["plausible"])), None,
                               "", detail=f"final rotation {reg.get('final_rotation_deg')} deg, "
                                          f"shift {reg.get('final_shift_px')} px, bound {reg.get('bound')}"))
    return out


def integrity_gate(results):
    """False when any integrity value fails or the registration is not plausible; True otherwise."""
    return not any(r.passed is False for r in results)


RELATIVE_FILE = Path(__file__).resolve().parents[1] / "config" / "integrity_relative_k.yaml"


def load_relative_k(path=RELATIVE_FILE):
    with open(path) as fh:
        return {k: v for k, v in yaml.safe_load(fh).items() if k in ("inversions", "gap_ratio", "lateral")}


def integrity_ratios(remedied, base):
    """Remedied over base (Andrew, 2026-11-21, option A): (inversions + 1) ratio, gap ratio, lateral.
    `remedied`, `base`: track_integrity results of the two tracks of one window."""
    r = {x.check: x.value for x in remedied}
    b = {x.check: x.value for x in base}
    with np.errstate(divide="ignore", invalid="ignore"):
        return {"inversions": float((r["integrity_inversions"] + 1) / (b["integrity_inversions"] + 1)),
                "gap_ratio": float(np.divide(r["integrity_gap_ratio"], b["integrity_gap_ratio"])),
                "lateral": float(np.divide(r["integrity_lateral"], b["integrity_lateral"]))}


def relative_integrity(rec_remedied, rec_base, k=None):
    """The integrity gate for a remedied track: each ratio to the window's own base track against its k, and the
    registration plausibility of the remedied track. Absolute values stay reported (track_integrity), not gating.
    Use integrity_gate on the result."""
    k = k or {}
    rem = track_integrity(rec_remedied)
    ratios = integrity_ratios(rem, track_integrity(rec_base))
    out = [CheckResult(f"integrity_rel_{name}",
                       False if np.isposinf(v) and k.get(name) is not None else _decide(v, k.get(name)),
                       v, k.get(name), "ratio", detail="remedied over base") for name, v in ratios.items()]
    return out + [x for x in rem if x.check == "registration_plausible"]
