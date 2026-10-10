"""Synthetic rods with prescribed kinematics, written as measurement records.

A rod is a chain of material points X (initial arc length from the tip). Each
point's arc length s from the tip follows ds/dt = v(s), with v the integral of
the prescribed strain rate REGR(s). Each point's curvature follows the
prescribed material rate dkappa/dt = c(s). The base end is anchored (fixed
position and tangent) unless a rigid rotation about it is set. Flanks lie at
+-h(t) along the normal N. All lengths px, times s.

Flank strain rate, exactly (flank element (1 - kappa n) ds at offset n = +-h):
    REGR_plus  = REGR - (h dkappa/dt + kappa dh/dt) / (1 - kappa h)
    REGR_minus = REGR + (h dkappa/dt + kappa dh/dt) / (1 + kappa h)
so plus minus minus = -2 (h dkappa/dt + kappa dh/dt) / (1 - kappa^2 h^2).
The checker uses the plane-sections form: plus minus minus = -2h dkappa/dt.
"""
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from measure.record import MeasurementRecord, PER_S_TO_PCT_PER_H

PCT_PER_H = 1.0 / PER_S_TO_PCT_PER_H      # %/h -> 1/s


def richards_velocity(v_end, s_mid, width, shape=1.0):
    """Tip-relative velocity of a flexible-logistic growth zone, zero at the tip.

    v(s) = v_end (g(s) - g(0)) / (1 - g(0)), g = (1 + exp(-(s - s_mid)/width))^(-1/shape)
    """
    g = lambda s: (1.0 + np.exp(-(np.asarray(s, float) - s_mid) / width)) ** (-1.0 / shape)
    g0 = g(0.0)
    v = lambda s: v_end * (g(s) - g0) / (1.0 - g0)

    def regr(s):
        s = np.asarray(s, float)
        e = np.exp(-(s - s_mid) / width)
        dg = (1.0 / shape) * (1.0 + e) ** (-1.0 / shape - 1.0) * e / width
        return v_end * dg / (1.0 - g0)
    return v, regr


@dataclass
class RodSpec:
    name: str
    length: float = 480.0                    # initial chain length, px
    dX: float = 1.0                          # material node spacing, px
    n_frames: int = 41
    dt: float = 90.0
    v: Callable = lambda s: 0.0 * np.asarray(s, float)        # tip-relative velocity, px/s
    regr: Callable = lambda s: 0.0 * np.asarray(s, float)     # dv/ds, 1/s
    kappa0: Callable = lambda X: 0.0 * np.asarray(X, float)   # initial curvature, 1/px
    kappa_rate: Callable = lambda s: 0.0 * np.asarray(s, float)  # material dkappa/dt, 1/(px s)
    h: Callable = lambda t: 15.0 + 0.0 * t                    # flank half-spacing, px
    dh: Callable = lambda t: 0.0 * t
    base_xy: tuple = (40.0, 128.0)           # anchored base, world (row, col)
    base_angle: float = np.pi                # tip->base tangent angle at the base; pi = root grows toward +row
    rotation_rate: float = 0.0               # rigid rotation, rad/s, about the pivot
    pivot_offset: float = 0.0                # pivot distance basal to the base along the base tangent, px; 0 = the base
    stage_velocity: Optional[tuple] = None   # logged stage velocity, px/s (world static)
    stage_follow_px: Optional[float] = 10.0  # stage step to follow the tip, px; None = fixed
    substeps: int = 20
    notes: str = ""
    expected: dict = field(default_factory=dict)


def simulate(spec):
    """Integrate the rod. Returns times, material X, s (T,N), kappa (T,N), centre (T,N,2)."""
    X = np.arange(0.0, spec.length + 1e-9, spec.dX)
    T = spec.n_frames
    times = np.arange(T) * spec.dt
    s = X.copy()
    kap = np.asarray(spec.kappa0(X), float) + 0.0 * X
    S = np.empty((T, len(X)))
    K = np.empty((T, len(X)))
    S[0], K[0] = s, kap
    h = spec.dt / spec.substeps
    rhs = lambda s_: np.asarray(spec.v(s_), float) - np.asarray(spec.v(0.0), float)
    for i in range(1, T):
        for _ in range(spec.substeps):
            k1 = rhs(s); c1 = spec.kappa_rate(s)
            k2 = rhs(s + 0.5 * h * k1); c2 = spec.kappa_rate(s + 0.5 * h * k1)
            k3 = rhs(s + 0.5 * h * k2); c3 = spec.kappa_rate(s + 0.5 * h * k2)
            k4 = rhs(s + h * k3); c4 = spec.kappa_rate(s + h * k3)
            s = s + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            kap = kap + h * (c1 + 2 * c2 + 2 * c3 + c4) / 6.0
        S[i], K[i] = s, kap
    centre = np.stack([shape_from_curvature(S[i], K[i], spec, times[i]) for i in range(T)])
    return times, X, S, K, centre


def _cumtrapz_from_base(y, s):
    """Integral of y over s from each node to the last node (the base)."""
    seg = 0.5 * (y[1:] + y[:-1]) * np.diff(s)
    tail = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    return tail


def shape_from_curvature(s, kap, spec, t):
    """World positions of the nodes; base anchored, integrated toward the tip.

    The tangent points tip -> base, angle phi = atan2(dcol, drow), dphi/ds = kappa.
    """
    phi_base = spec.base_angle + spec.rotation_rate * t
    phi = phi_base - _cumtrapz_from_base(kap, s)
    tr = np.cos(phi)
    tc = np.sin(phi)
    base = np.asarray(spec.base_xy, float)
    if spec.pivot_offset:
        # Turning about a point basal to the base moves the base on a circle.
        a0, a = spec.base_angle, phi_base
        pivot = base + spec.pivot_offset * np.array([np.cos(a0), np.sin(a0)])
        base = pivot - spec.pivot_offset * np.array([np.cos(a), np.sin(a)])
    row = base[0] - _cumtrapz_from_base(tr, s)
    col = base[1] - _cumtrapz_from_base(tc, s)
    return np.stack([row, col], axis=1)


def normals(chain):
    """Unit +N normal per node, N = tangent (tip->base) rotated +90 deg in (row, col)."""
    tng = np.gradient(chain, axis=-2)
    tng = tng / np.linalg.norm(tng, axis=-1, keepdims=True)
    return np.stack([-tng[..., 1], tng[..., 0]], axis=-1)


def stage_track(spec, times, tip_world):
    """Stage position (world = image + stage_px) for each frame."""
    T = len(times)
    if spec.stage_velocity is not None:
        return np.outer(times, spec.stage_velocity)
    stage = np.zeros((T, 2))
    if spec.stage_follow_px is None:
        return stage
    for i in range(1, T):
        stage[i] = stage[i - 1]
        off = (tip_world[i] - tip_world[0]) - stage[i]
        if np.linalg.norm(off) > spec.stage_follow_px:
            stage[i] = np.round(tip_world[i] - tip_world[0], 1)
    return stage


def make_record(spec, chain_step=2.0, midline_step=2.0):
    """Field-level record: chains sampled from the simulated rod, with the truth."""
    times, X, S, K, centre = simulate(spec)
    N = normals(centre)
    hh = np.asarray(spec.h(times), float)[:, None, None]
    plus_d = centre + hh * N
    minus_d = centre - hh * N
    pick = np.arange(0, len(X), int(round(chain_step / spec.dX)))
    stage = stage_track(spec, times, centre[:, 0])
    mid_pick = np.arange(0, len(X), int(round(midline_step / spec.dX)))
    rec = MeasurementRecord(
        root_id=spec.name, source="field", frame_times_s=times, pixel_um=2.105,
        stage_px=stage, centre=centre[:, pick], plus=plus_d[:, pick],
        minus=minus_d[:, pick], midline=centre[:, mid_pick],
        settings={"generator": "measure.rod", "chain_step_px": chain_step})
    rec.truth = truth_fields(spec, rec, times, S, K)
    return rec


def truth_fields(spec, rec, times, S, K):
    """Analytic fields on the record's grid at each frame pair's mid-time."""
    s_grid = rec.fields["s_grid"]
    n = len(times) - 1
    tm = 0.5 * (times[:-1] + times[1:])
    v0 = np.asarray(spec.v(0.0), float)
    v = np.broadcast_to(np.asarray(spec.v(s_grid), float) - v0, (n, len(s_grid))).copy()
    regr = np.broadcast_to(np.asarray(spec.regr(s_grid), float), (n, len(s_grid))).copy()
    krate = np.broadcast_to(np.asarray(spec.kappa_rate(s_grid), float), (n, len(s_grid))).copy()
    h = np.asarray(spec.h(tm), float)[:, None]
    dh = np.asarray(spec.dh(tm), float)[:, None]
    kap = np.stack([np.interp(s_grid, 0.5 * (S[i] + S[i + 1]), 0.5 * (K[i] + K[i + 1]))
                    for i in range(n)])
    common = (h * krate + kap * dh)
    plus = regr - common / (1.0 - kap * h)
    minus = regr + common / (1.0 + kap * h)
    covered = s_grid <= np.min(S[:, -1])
    out = {"s_grid": s_grid, "v_mid": v, "regr_mid": regr, "regr_plus": plus,
           "regr_minus": minus, "spacing": 2 * h + 0 * regr, "kappa": kap,
           "kappa_rate": krate, "covered": covered}
    for k in ("v_mid", "regr_mid", "regr_plus", "regr_minus", "spacing", "kappa", "kappa_rate"):
        out[k][:, ~covered] = np.nan
    return out


# ---------------------------------------------------------------- field-level cases

V_END = 60.0 / 3600.0     # tip speed, px/s (60 px/h; 126 um/h at 2.105 um/px)


def growth_zone():
    return richards_velocity(V_END, s_mid=150.0, width=35.0, shape=1.0)


WIDTH_RATE = 0.40          # flank half-spacing growth, 1/h, in the width-change cases


def width_change_spec(kappa_inv=800.0):
    """Curved rod (constant curvature 1/kappa_inv px) whose flank spacing grows 40 %/h.

    True plane-sections residual 2 kappa dh/dt: 1.5 %/h at 1/800, 3.0 at 1/400, 4.5 at 1/267.
    """
    v_gz, regr_gz = growth_zone()
    h0, hdot = 15.0, 15.0 * WIDTH_RATE / 3600.0
    k0 = 1.0 / kappa_inv
    return RodSpec("width_change", v=v_gz, regr=regr_gz, kappa0=lambda X: k0 + 0 * np.asarray(X, float),
                   h=lambda t: h0 + hdot * np.asarray(t, float), dh=lambda t: hdot + 0 * np.asarray(t, float),
                   notes=f"constant curvature 1/{kappa_inv:g} px; flank spacing grows 40 %/h; constant-width assumption broken",
                   expected={"rigid_invariance": True, "closure": True, "plane_sections": False})


def rigid_rotation_spec(deg_per_frame=0.1, pivot_offset=0.0, name="rigid_rotation"):
    """No growth; the whole rod turns at deg_per_frame (frames 90 s apart) about a pivot."""
    return RodSpec(name, rotation_rate=np.deg2rad(deg_per_frame) / 90.0, stage_follow_px=None,
                   pivot_offset=pivot_offset,
                   notes=f"no growth; whole rod turns {deg_per_frame:g} deg/frame about a point "
                         f"{pivot_offset:g} px basal to the last chain point",
                   expected={"rigid_invariance": True, "closure": pivot_offset == 0.0,
                             "plane_sections": True})


def field_cases():
    """The field-level cases. `expected` gives the pass/fail of each check."""
    v_gz, regr_gz = growth_zone()
    zero = lambda s: 0.0 * np.asarray(s, float)
    all_pass = {"rigid_invariance": True, "closure": True, "plane_sections": True}
    eps = 30.0 * PCT_PER_H
    # Curvature-rate bump inside the growth zone. With 2h = 30 px the flank
    # difference at the peak is 30 c_peak = 1.8 %/h.
    c_peak = 6e-4 / 3600.0
    bump = lambda s: c_peak * np.exp(-0.5 * ((np.asarray(s, float) - 150.0) / 40.0) ** 2)
    return [
        RodSpec("rigid_translation", stage_velocity=(0.6 / 90.0, 0.3 / 90.0),
                notes="no growth; stage moves 0.67 px/frame and is logged; world static",
                expected=dict(all_pass)),
        rigid_rotation_spec(0.1),
        # The basal tracked tissue moves: closure flags it (decisions, 2026-10-10)
        rigid_rotation_spec(0.1, pivot_offset=200.0, name="rotation_basal_pivot"),
        RodSpec("uniform_strain", v=lambda s: eps * np.asarray(s, float),
                regr=lambda s: eps + zero(s),
                notes="REGR 30 %/h along the whole chain", expected=dict(all_pass)),
        RodSpec("growth_zone", v=v_gz, regr=regr_gz,
                notes="flexible logistic, tip speed 60 px/h, peak REGR about 43 %/h",
                expected=dict(all_pass)),
        RodSpec("bending", v=v_gz, regr=regr_gz, kappa_rate=bump,
                notes="growth zone plus a curvature-rate bump at s = 150 px; constant width",
                expected=dict(all_pass)),
        width_change_spec(800.0),
    ]
