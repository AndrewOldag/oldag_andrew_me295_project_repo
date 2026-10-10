"""A record made from tracker output (spec item 2 check).

Fixture: tests/fixtures/growth_zone_clean_s0.npz is the raw output of
scripts/remote/qb_track.py for the clean image-level growth-zone rod, seed 0;
the truth file is beside it.
"""
from pathlib import Path

import numpy as np

from measure.record import MeasurementRecord, from_tracker_npz, PER_S_TO_PCT_PER_H
from checker import run_checks

DATA = Path(__file__).resolve().parent / "fixtures"


def load():
    return (from_tracker_npz(DATA / "growth_zone_clean_s0.npz"),
            np.load(DATA / "growth_zone_clean_s0_truth.npz"))


def test_shapes_and_settings():
    rec, _ = load()
    T, M, _ = rec.centre.shape
    assert rec.source == "tracker" and T == 41 and M > 10
    assert rec.plus.shape == rec.minus.shape == rec.centre.shape
    assert rec.stage_px.shape == (T, 2) and np.all(rec.stage_px[0] == 0)
    assert rec.midline.shape[0] == T
    assert rec.settings["tracker"] == "quantum_borland_v1" and rec.settings["track_centre"]


def test_plus_flank_is_on_plus_normal_side():
    rec, _ = load()
    c = rec.centre[0]
    tang = np.gradient(c, axis=0)
    normal = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
    assert np.nanmean(np.sum((rec.plus[0] - c) * normal, axis=1)) > 0
    assert np.nanmean(np.sum((rec.minus[0] - c) * normal, axis=1)) < 0


def test_strain_rate_close_to_truth():
    rec, truth = load()
    f = rec.fields
    s = f["s_grid"]
    t = np.interp(s, truth["s_grid"], np.nanmean(truth["regr_mid"], axis=0), right=np.nan)
    covered = np.mean(np.isfinite(f["regr_mid"]), axis=0) >= 0.5
    e = (np.nanmean(f["regr_mid"][:, covered], axis=0) - t[covered]) * PER_S_TO_PCT_PER_H
    assert np.sqrt(np.nanmean(e ** 2)) < 1.0          # %/h, peak about 43 %/h


def test_round_trip_and_checks(tmp_path):
    rec, _ = load()
    rec.save(tmp_path / "r.npz")
    back = MeasurementRecord.load(tmp_path / "r.npz")
    np.testing.assert_allclose(back.fields["regr_plus"], rec.fields["regr_plus"], equal_nan=True)
    res = {r.check: r for r in run_checks(back)}
    assert res["closure"].value < 2.0                 # px/h, tip path about 60 px/h
