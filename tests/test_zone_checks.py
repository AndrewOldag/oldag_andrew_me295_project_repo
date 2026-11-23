"""Growth-zone placement checks (spec 2026-11-23, task c034) on field-level and tracked rods."""
from pathlib import Path

import numpy as np
import pytest

from checker.zone_checks import particle_path, plateau, run_zone_checks, shifted_fields
from measure.record import from_tracker_npz
from measure.rod import make_record, v3_cases

DATA = Path(__file__).resolve().parent / "fixtures"
CASES = {c.name: c for c in v3_cases()}


def vals(rec, fields=None, th=None):
    return {k: v for r in run_zone_checks(rec, th, fields) for k, v in r.values.items()}


@pytest.mark.parametrize("name", ["v3_growth_zone", "v3_bend30"])
def test_correct_profile_is_consistent(name):
    v = vals(make_record(CASES[name]))
    assert v["plateau_speed"] < 0.01          # bending turns the tip; growth speed along the midline does not see it
    assert v["pp_rms_rel"] < 0.001 and v["pp_max_px"] < 0.1


@pytest.mark.parametrize("d", [-15, 15, 60])
def test_shifted_profile_moves_particles_off_their_tracks(d):
    rec = make_record(CASES["v3_growth_zone"])
    v0, v = vals(rec), vals(rec, shifted_fields(rec, d))
    assert v["pp_rms_rel"] > 100 * v0["pp_rms_rel"]
    assert v["pp_max_px"] > abs(d) * 0.5


def test_shift_grows_with_size():
    rec = make_record(CASES["v3_growth_zone"])
    r = [vals(rec, shifted_fields(rec, d))["pp_rms_px"] for d in (15, 30, 60)]
    assert r[0] < r[1] < r[2]


def test_still_rod_relative_values_not_computable():
    v = vals(make_record(CASES["v3_still"]))
    assert v["plateau_speed"] is None and v["pp_rms_rel"] is None and v["pp_max_rel"] is None
    assert v["plateau_regr"] == 0.0 and v["pp_max_px"] == 0.0


def test_thresholds_decide():
    rec = make_record(CASES["v3_growth_zone"])
    th = {"plateau_regr": 5.0, "plateau_speed": 0.05, "pp_rms_rel": 0.01, "pp_max_rel": 0.02}
    assert [r.passed for r in run_zone_checks(rec, th)] == [True, True]
    pp = particle_path(rec, {"pp_rms_rel": 0.01}, shifted_fields(rec, 30))
    assert pp.passed is False
    assert plateau(rec).passed is None           # no thresholds: values only


def test_shift_drops_negative_s():
    rec = make_record(CASES["v3_growth_zone"])
    f = shifted_fields(rec, -30)
    assert f["s_grid"][0] >= 0 and f["v_mid"].shape[1] == len(f["s_grid"])


def test_tracked_fixture_runs():
    rec = from_tracker_npz(DATA / "growth_zone_clean_s0.npz")
    v = vals(rec)
    assert all(v[k] is not None and np.isfinite(v[k]) for k in v)
