"""Field-level synthetic rods: record round trip, derived fields and closure of the strain rate."""
import numpy as np
import pytest

from measure.record import MeasurementRecord, PER_S_TO_PCT_PER_H
from measure.rod import field_cases, make_record

CASES = {spec.name: spec for spec in field_cases()}


@pytest.fixture(scope="module")
def records():
    return {name: make_record(spec) for name, spec in CASES.items()}


def test_cases():
    assert set(CASES) == {"rigid_translation", "rigid_rotation", "rotation_basal_pivot",
                          "uniform_strain", "growth_zone", "bending", "width_change"}


@pytest.mark.parametrize("name", list(CASES))
def test_derived_fields_match_truth(records, name):
    rec = records[name]
    s = rec.fields["s_grid"]
    # interior only: the last 10 px are the end segment of the chain
    cov = rec.truth["covered"] & (s <= s[rec.truth["covered"]].max() - 10.0)
    for k in ("regr_mid", "regr_plus", "regr_minus"):
        err = np.nanmax(np.abs(rec.fields[k] - rec.truth[k])[:, cov]) * PER_S_TO_PCT_PER_H
        assert err < 0.1, (k, err)          # %/h
    err_v = np.nanmax(np.abs(rec.fields["v_mid"] - rec.truth["v_mid"])[:, cov]) * 3600
    assert err_v < 0.05                     # px/h


@pytest.mark.parametrize("name", list(CASES))
def test_integrated_strain_rate_equals_tip_velocity(records, name):
    """Integral of REGR from tip to base = tip speed relative to the base.

    For a straight anchored rod whose growth zone ends inside the chain, this is
    also the tip speed in the world.
    """
    rec = records[name]
    f = rec.fields
    s = f["s_grid"]
    ok = np.all(np.isfinite(f["regr_mid"]) & np.isfinite(f["v_mid"]), axis=0)
    regr = np.nanmean(f["regr_mid"][:, ok], axis=0)
    v = np.nanmean(f["v_mid"][:, ok], axis=0)
    integ = np.trapezoid(regr, s[ok])                                        # px/s
    assert integ == pytest.approx(v[-1] - v[0], abs=0.01 / 3600)             # 0.01 px/h
    if name == "growth_zone":      # v is flat beyond the zone, so v at the grid end = v at the anchored base
        tip = rec.midline[:, 0]
        speed = np.linalg.norm(tip[-1] - tip[0]) / (rec.frame_times_s[-1] - rec.frame_times_s[0])
        assert v[-1] == pytest.approx(speed, rel=0.01)


def test_record_round_trip(tmp_path, records):
    rec = records["bending"]
    path = tmp_path / "bending.npz"
    rec.save(path)
    back = MeasurementRecord.load(path)
    assert back.root_id == "bending" and back.source == "field"
    np.testing.assert_array_equal(back.centre, rec.centre)
    np.testing.assert_allclose(back.fields["regr_plus"], rec.fields["regr_plus"], equal_nan=True)
    np.testing.assert_allclose(back.truth["kappa_rate"], rec.truth["kappa_rate"], equal_nan=True)
