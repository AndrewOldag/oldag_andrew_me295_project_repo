"""Preprocessing steps for remedies (measure/preprocess.py). Spec 2026-10-11, items 2 and 3."""
import numpy as np
import pytest

from measure.preprocess import smooth_midline


def translating(T=73, K=200, v=(0.0, 1.5), shape="straight"):
    """Midline (T, K, 2), tip first, moving at v px per frame, no jitter."""
    s = np.arange(K) * 2.0
    if shape == "straight":
        base = np.stack([200.0 - 0.6 * s, 100.0 + 0.8 * s], axis=1)
    else:                                         # arc of radius 300 px
        th = s / 300.0
        base = np.stack([200.0 - 300.0 * np.sin(th), 100.0 + 300.0 * (1 - np.cos(th))], axis=1)
    return base[None] + np.arange(T)[:, None, None] * np.asarray(v)[None, None, :]


@pytest.mark.parametrize("level", ["light", "strong"])
def test_straight_translating_midline_unchanged(level):
    m = translating()
    out = smooth_midline(m, level)
    assert np.max(np.abs(out - m)) < 0.01


@pytest.mark.parametrize("level", ["light", "strong"])
def test_tip_path_keeps_its_length(level):
    m = translating(shape="arc")
    out = smooth_midline(m, level)
    tip = out[:, 0]
    assert abs((tip[-1] - tip[0])[1] - 1.5 * (len(m) - 1)) < 0.01
    # over time only a translation: every frame is frame 0 moved by v t
    assert np.max(np.abs(out - out[:1] - (m - m[:1]))) < 0.01


def test_jitter_is_reduced():
    rng = np.random.default_rng(0)
    m = translating()
    noisy = m + rng.normal(0, 1.0, m.shape)
    for level in ("light", "strong"):
        assert np.sqrt(np.mean((smooth_midline(noisy, level) - m)[:, 1:] ** 2)) < 0.5


def test_band_start_from_the_measured_profile():
    from pathlib import Path
    from measure.preprocess import registration_band_start
    from measure.record import from_tracker_npz
    rec = from_tracker_npz(Path(__file__).resolve().parent / "fixtures" / "growth_zone_clean_s0.npz")
    s0 = registration_band_start(rec)
    assert 250 <= s0 <= 350                      # the clean rod's growth zone ends near 300 px


def test_band_kept_inside_both_frames():
    from measure.preprocess import _inside
    m = _inside((100, 80), np.array([10.0, 0.0]), 25)
    rows = np.flatnonzero(m.any(axis=1))
    assert rows.min() == 35 and rows.max() == 84    # image rows 25..74, moved by the stage


def _space_only(midline, level):
    """smooth_midline along s only (the time sigma set to 0)."""
    from unittest import mock
    from measure import preprocess
    sig_s, _ = preprocess.MIDLINE_SMOOTH[level]
    with mock.patch.dict(preprocess.MIDLINE_SMOOTH, {level: (sig_s, 0.0)}):
        return preprocess.smooth_midline(midline, level)


def end_frame_jitter(level, seed=0, std=1.0):
    """RMS sideways error in the first and last frame of a jittered translating midline: raw, after the
    old odd-reflection padding over time, after the fitted-line padding (smooth_midline)."""
    from measure.preprocess import MIDLINE_SMOOTH, _smooth_linear_ends
    rng = np.random.default_rng(seed)
    m = translating(T=41)
    noisy = m.copy()
    noisy[..., 1] += rng.normal(0, std, len(m))[:, None]           # independent sideways shift, every frame
    sig_s, sig_t = MIDLINE_SMOOTH[level]
    old = _smooth_linear_ends(_space_only(noisy, level), sig_t, axis=0)
    new = smooth_midline(noisy, level)
    ends = [0, -1]
    rms = lambda x: float(np.sqrt(np.mean((x[ends, 1:-20, 1] - m[ends, 1:-20, 1]) ** 2)))   # sideways, away from the base end
    return rms(noisy), rms(old), rms(new)


@pytest.mark.parametrize("level,most", [("light", 0.99), ("strong", 0.75)])
def test_end_frame_jitter_lowered(level, most):
    r = np.array([end_frame_jitter(level, seed=k) for k in range(50)])
    assert np.allclose(r[:, 1], r[:, 0])                            # odd reflection kept the end frames
    ratio = np.sqrt(np.mean(r[:, 2] ** 2) / np.mean(r[:, 1] ** 2))  # measured: 0.969 light, 0.731 strong
    assert ratio < most
