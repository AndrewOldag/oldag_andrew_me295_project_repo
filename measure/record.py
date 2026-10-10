"""Measurement record: one root over one window.

The record is what the tracker returns and what the checker reads. The
primary content is three tracked material chains (centre and two flanks), the
per-frame midline from the midline source, the stage log and the frame times.
The grid fields (velocity, strain rate, flank spacing, curvature rate) are
derived from these by `derive`, the same way for every source. Format and
conventions: docs/context/measurement_record.md.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path

import numpy as np

PER_S_TO_PCT_PER_H = 3.6e5   # strain rate 1/s -> %/h

DEFAULT_SETTINGS = {
    "grid_px": 5.0,              # arc-length grid spacing for derived fields
    "curvature_smooth_px": 0.0,  # Gaussian smoothing of midline tangent angle; 0 = none
}

GRID_FIELDS = ("v_mid", "regr_mid", "regr_plus", "regr_minus", "spacing",
               "kappa", "kappa_rate")


@dataclass
class MeasurementRecord:
    root_id: str
    source: str                  # "field", "image" or "tracker"
    frame_times_s: np.ndarray    # (T,)
    pixel_um: float
    stage_px: np.ndarray         # (T, 2) row, col; world = image + stage_px
    centre: np.ndarray           # (T, M, 2) world, tip first; NaN = lost
    plus: np.ndarray             # (T, M, 2) flank on the +N side
    minus: np.ndarray            # (T, M, 2) flank on the -N side
    midline: np.ndarray          # (T, K, 2) world, tip first, from the midline source
    settings: dict = field(default_factory=dict)
    truth: dict = field(default_factory=dict)
    _fields: dict = field(default=None, repr=False, compare=False)

    @property
    def n_frames(self):
        return len(self.frame_times_s)

    @property
    def tip_image(self):
        """(T, 2) tip in image coordinates (midline source plus stage log)."""
        return self.midline[:, 0, :] - self.stage_px

    def setting(self, key):
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))

    @property
    def fields(self):
        if self._fields is None:
            self._fields = derive(self)
        return self._fields

    def save(self, path):
        path = Path(path)
        arrays = {k: getattr(self, k) for k in
                  ("frame_times_s", "stage_px", "centre", "plus", "minus", "midline")}
        arrays.update({f"field_{k}": v for k, v in self.fields.items()})
        arrays.update({f"truth_{k}": np.asarray(v) for k, v in self.truth.items()})
        meta = {"root_id": self.root_id, "source": self.source,
                "pixel_um": self.pixel_um, "settings": self.settings}
        np.savez_compressed(path, meta=json.dumps(meta), **arrays)

    @classmethod
    def load(cls, path):
        with np.load(path, allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            truth = {k[6:]: z[k] for k in z.files if k.startswith("truth_")}
            return cls(root_id=meta["root_id"], source=meta["source"],
                       frame_times_s=z["frame_times_s"], pixel_um=meta["pixel_um"],
                       stage_px=z["stage_px"], centre=z["centre"], plus=z["plus"],
                       minus=z["minus"], midline=z["midline"],
                       settings=meta["settings"], truth=truth)


# ---------------------------------------------------------------- geometry

def arclength(chain):
    """(T, M, 2) -> (T, M) arc length from index 0; NaN propagates baseward."""
    seg = np.linalg.norm(np.diff(chain, axis=1), axis=2)
    s = np.concatenate([np.zeros(seg.shape[:1] + (1,)), np.cumsum(seg, axis=1)], axis=1)
    s[np.isnan(chain[..., 0])] = np.nan
    return s


def tangent_angle(chain):
    """Angle of the tip->base tangent per segment, atan2(dcol, drow), unwrapped."""
    d = np.diff(chain, axis=-2)
    return np.unwrap(np.arctan2(d[..., 1], d[..., 0]), axis=-1)


def curvature_along(line, smooth_px=0.0):
    """Curvature of one (K, 2) polyline at its vertices, with arc length.

    kappa = dphi/ds with phi = atan2(dcol, drow) and the tangent pointing
    tip -> base. With N = tangent rotated +90 degrees in (row, col), the
    tangent turns toward +N where kappa > 0.
    """
    ok = ~np.isnan(line[:, 0])
    line = line[ok]
    seg = np.linalg.norm(np.diff(line, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    phi = tangent_angle(line)
    s_seg = 0.5 * (s[:-1] + s[1:])
    if smooth_px > 0:
        from scipy.ndimage import gaussian_filter1d
        step = np.median(seg)
        phi = gaussian_filter1d(phi, smooth_px / step, mode="nearest")
    kappa = np.gradient(phi, s_seg)
    return s_seg, kappa


def _interp(xq, x, y):
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 2:
        return np.full(np.shape(xq), np.nan)
    return np.interp(xq, x[ok], y[ok], left=np.nan, right=np.nan)


# ---------------------------------------------------------------- derivation

def derive(rec):
    """Grid fields from the tracked chains, per frame pair, on one arc-length grid.

    All fields are (T-1, G) on `s_grid` (px from the tip). Units: px/s for
    velocity, 1/s for strain rates and curvature rate, px for spacing, 1/px
    for curvature. Each value is a finite difference over one frame pair,
    placed at the mean arc length of the two frames.
    """
    t = np.asarray(rec.frame_times_s, float)
    dt = np.diff(t)
    s_c = arclength(rec.centre)                                   # (T, M)
    l_c = np.diff(s_c, axis=1)
    l_p = np.diff(arclength(rec.plus), axis=1)
    l_m = np.diff(arclength(rec.minus), axis=1)
    gap = np.linalg.norm(rec.plus - rec.minus, axis=2)             # (T, M)

    grid_px = float(rec.setting("grid_px"))
    s_max = np.nanmax(s_c)
    s_grid = np.arange(0.0, s_max + 1e-9, grid_px)
    n = len(dt)
    out = {k: np.full((n, len(s_grid)), np.nan) for k in GRID_FIELDS}

    smooth = float(rec.setting("curvature_smooth_px"))
    curv = [curvature_along(rec.midline[i], smooth) for i in range(rec.n_frames)]

    for i in range(n):
        s_node = 0.5 * (s_c[i] + s_c[i + 1])
        s_seg = 0.5 * (s_node[:-1] + s_node[1:])
        v = (s_c[i + 1] - s_c[i]) / dt[i]
        with np.errstate(divide="ignore", invalid="ignore"):
            r_c = np.log(l_c[i + 1] / l_c[i]) / dt[i]
            r_p = np.log(l_p[i + 1] / l_p[i]) / dt[i]
            r_m = np.log(l_m[i + 1] / l_m[i]) / dt[i]
        sp = 0.5 * (gap[i] + gap[i + 1])
        # Curvature of the midline source, sampled at the tracked material
        # points in each frame: a material derivative, not one at fixed s.
        k0 = _interp(s_c[i], *curv[i])
        k1 = _interp(s_c[i + 1], *curv[i + 1])
        out["v_mid"][i] = _interp(s_grid, s_node, v)
        out["regr_mid"][i] = _interp(s_grid, s_seg, r_c)
        out["regr_plus"][i] = _interp(s_grid, s_seg, r_p)
        out["regr_minus"][i] = _interp(s_grid, s_seg, r_m)
        out["spacing"][i] = _interp(s_grid, s_node, sp)
        out["kappa"][i] = _interp(s_grid, s_node, 0.5 * (k0 + k1))
        out["kappa_rate"][i] = _interp(s_grid, s_node, (k1 - k0) / dt[i])
    out["s_grid"] = s_grid
    return out


def rigid_moved(rec, rotation_rate, velocity=(0.0, 0.0), about=None):
    """Copy of a record with a rigid motion added to every world position.

    Frame i is turned by rotation_rate * t_i (rad, rad/s) about `about` (row,
    col; default the frame-0 tip) and shifted by velocity * t_i (px/s). The
    stage log is unchanged. Used for the rigid-invariance check on records
    that are not re-tracked (field-level rods).
    """
    t = np.asarray(rec.frame_times_s, float) - rec.frame_times_s[0]
    about = np.asarray(rec.centre[0, 0] if about is None else about, float)

    def move(a):
        out = np.empty_like(a)
        for i, ti in enumerate(t):
            c, s = np.cos(rotation_rate * ti), np.sin(rotation_rate * ti)
            rot = np.array([[c, -s], [s, c]])
            out[i] = (a[i] - about) @ rot.T + about + np.asarray(velocity) * ti
        return out
    return MeasurementRecord(
        root_id=rec.root_id + "_moved", source=rec.source, frame_times_s=rec.frame_times_s,
        pixel_um=rec.pixel_um, stage_px=rec.stage_px, centre=move(rec.centre),
        plus=move(rec.plus), minus=move(rec.minus), midline=move(rec.midline),
        settings=dict(rec.settings, rigid_motion={"rotation_rate": rotation_rate,
                                                  "velocity": list(velocity)}))


def orient_flanks(centre, a, b):
    """Return (plus, minus) from two flank chains, by the side of frame 0.

    plus is the flank on the +N side, N = tip->base tangent rotated +90
    degrees in (row, col): N = (-dcol, drow).
    """
    c = centre[0]
    tang = np.gradient(c, axis=0)
    normal = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
    side = np.nanmean(np.sum((a[0] - c) * normal, axis=1))
    return (a, b) if side > 0 else (b, a)


def from_tracker_npz(path, root_id=None):
    """Build a record from the raw arrays saved by scripts/remote/qb_track.py."""
    with np.load(path, allow_pickle=False) as z:
        meta = json.loads(str(z["meta"]))
        to_tm2 = lambda a: np.transpose(a, (2, 0, 1)).astype(float)   # (M,2,T) -> (T,M,2)
        centre = to_tm2(z["centre_track"])
        left, right = to_tm2(z["left_track"]), to_tm2(z["right_track"])
        for name, frozen in (("centre", "centre_frozen"), ("left", "left_frozen"),
                             ("right", "right_frozen")):
            if frozen in z.files:
                chain = {"centre": centre, "left": left, "right": right}[name]
                chain[np.transpose(z[frozen]).astype(bool)] = np.nan
        plus, minus = orient_flanks(centre, left, right)
        return MeasurementRecord(
            root_id=root_id or meta["root_id"], source="tracker",
            frame_times_s=z["elapsed_s"], pixel_um=float(meta["pixel_um"]),
            stage_px=z["stage_px"], centre=centre, plus=plus, minus=minus,
            midline=z["midline_world"], settings=meta["settings"])
