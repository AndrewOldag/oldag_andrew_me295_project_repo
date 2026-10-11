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
