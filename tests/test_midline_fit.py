"""Spline fit of a midline (proposal 2026-10-23, option 1)."""
import numpy as np

from measure.midline_fit import QUANT_RMS_PX, fit_midlines, spline_fit
from measure.record import curvature_along


def arc(radius=200.0, length=600.0, step=2.0):
    th = np.arange(0.0, length, step) / radius
    return np.column_stack([300 + radius * np.sin(th), 100 + radius * (1 - np.cos(th))])


def test_staircase_arc_fit_close_and_curvature_kept():
    true = arc()
    noisy = np.round(true)                                   # whole-pixel staircase, up to 0.5 px
    fit = spline_fit(noisy)
    assert np.sqrt(np.mean(np.sum((fit - true) ** 2, axis=1))) < 0.3
    s, k = curvature_along(fit)
    inner = (s > 50) & (s < s[-1] - 50)
    assert abs(np.median(np.abs(k[inner])) - 1 / 200.0) < 0.05 / 200.0
    _, k_noisy = curvature_along(noisy)
    assert np.std(k[inner]) < 0.2 * np.std(k_noisy[inner])  # staircase curvature noise mostly removed


def test_residual_rule():
    assert abs(QUANT_RMS_PX - 0.2887) < 1e-4


def test_smooth_line_within_residual_budget_and_nans_kept():
    true = arc()
    d = np.linalg.norm(spline_fit(true) - true, axis=1)
    assert np.sqrt(np.mean(d ** 2)) <= QUANT_RMS_PX + 1e-3   # the fit uses its budget, also on a smooth line
    with_nan = true.copy(); with_nan[-3:] = np.nan
    out = spline_fit(with_nan)
    assert np.all(np.isnan(out[-3:])) and np.all(np.isfinite(out[:-3]))


def test_short_and_stacked():
    short = arc()[:4]
    assert np.array_equal(spline_fit(short), short)
    stack = np.stack([arc(), np.round(arc())])
    assert fit_midlines(stack).shape == stack.shape
