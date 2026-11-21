"""register_frames_v2 (spec 2026-11-20 R2): direct to frame 0 against the chained v1 on textured frames with a
known rigid drift; near identity under pure growth; the plausibility bound."""
import numpy as np
import pytest
from scipy.ndimage import gaussian_filter

cv2 = pytest.importorskip("cv2")
from measure.preprocess import _affine_cv, _rigid_motion, register_frames, register_frames_v2  # noqa: E402

N, T = 240, 24
BAND = 60.0          # px; a 20 px strip hardly constrains rotation (0.2 deg moves its ends 0.35 px)
CENTRE = np.array([120.0, 120.0])


def rigid(deg, shift):
    a = np.radians(deg)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    C = np.eye(3)
    C[:2, :2] = R
    C[:2, 2] = CENTRE - R @ CENTRE + shift
    return C


def texture(rng):
    return gaussian_filter(rng.normal(0, 1, (N, N)), 2.0) * 400 + 2000


def frames_for(maps, rng, noise=8.0, base=None):
    g0 = texture(rng) if base is None else base
    out = []
    for C in maps:   # g_t(C_t x) = g_0(x): output y reads g_0(C_t^-1 y)
        g = cv2.warpAffine(g0.astype(np.float32), _affine_cv(np.linalg.inv(C)), (N, N),
                           flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
        out.append(np.clip(g + rng.normal(0, noise, g.shape), 0, 65535).astype(np.uint16))
    return np.array(out)


def midline():
    line = np.column_stack([np.full(200, 120.0), np.linspace(220, 21, 200)])   # tip at index 0
    return np.repeat(line[None], T, axis=0)


def final_error(C_fit, C_true):
    rot, disp = _rigid_motion(np.linalg.inv(C_true) @ C_fit, CENTRE)
    return abs(rot), disp


def test_direct_recovers_drift_better_than_chained():
    rng = np.random.default_rng(3)
    truth = [rigid(0.05 * t, np.array([0.4, -0.3]) * t) for t in range(T)]
    fr = frames_for(truth, rng)
    stage = np.zeros((T, 2))
    *_, C2, rep = register_frames_v2(fr, stage, midline(), 0, np.inf, max_shift_px=50, band_px=BAND)
    *_, C1, _ = register_frames(fr, stage, midline(), 0, np.inf, band_px=BAND)
    rot2, d2 = final_error(C2[-1], truth[-1])
    rot1, d1 = final_error(C1[-1], truth[-1])
    assert rot2 < 0.05 and d2 < 0.3
    assert d2 < d1
    assert rep["plausible"] and abs(rep["final_rotation_deg"] - 0.05 * (T - 1)) < 0.05


def test_pure_growth_is_near_identity():
    rng = np.random.default_rng(4)
    base = texture(rng)
    fr = []
    for t in range(T):   # basal half static; the tip half changes every frame
        g = base.copy()
        g[:, 200:] = texture(rng)[:, 200:]
        fr.append(np.clip(g + rng.normal(0, 8.0, g.shape), 0, 65535).astype(np.uint16))
    *_, C, rep = register_frames_v2(np.array(fr), np.zeros((T, 2)), midline(), 90, np.inf, max_shift_px=20, band_px=BAND)
    assert abs(rep["final_rotation_deg"]) < 0.05 and rep["final_band_motion_px"] < 0.3 and rep["plausible"]


def test_bound_trips_on_9_degrees():
    rng = np.random.default_rng(5)
    truth = [rigid(9.0 * t / (T - 1), np.zeros(2)) for t in range(T)]
    *_, rep = register_frames_v2(frames_for(truth, rng), np.zeros((T, 2)), midline(), 0, np.inf, max_shift_px=500, band_px=BAND)
    assert abs(rep["final_rotation_deg"] - 9.0) < 0.2 and rep["plausible"] is False


def test_diag_chain_equals_register_frames():
    pytest.importorskip("root_kinematics")
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "remote"))
    from register_diag import chained_pairs
    rng = np.random.default_rng(7)
    fr = frames_for([rigid(0.1 * t, np.array([0.2, 0.1]) * t) for t in range(8)], rng)
    mid = midline()[:8]
    E, ecc = chained_pairs(fr, np.zeros((8, 2)), mid, 0, np.inf, band_px=BAND)
    C = np.eye(3)
    for e in E:
        C = e @ C
    *_, C1, _ = register_frames(fr, np.zeros((8, 2)), mid, 0, np.inf, band_px=BAND)
    assert np.allclose(C, C1[-1], atol=1e-9) and len(ecc) == 7


def test_bound_trips_on_shift():
    rng = np.random.default_rng(6)
    truth = [rigid(0.0, np.array([0.0, 1.0]) * t) for t in range(T)]
    *_, rep = register_frames_v2(frames_for(truth, rng), np.zeros((T, 2)), midline(), 0, np.inf, max_shift_px=10, band_px=BAND)
    assert rep["final_band_motion_px"] > 20 and rep["plausible"] is False
