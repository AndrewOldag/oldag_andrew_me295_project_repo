"""Checker profiles (inbox item 18): synthetic keeps three gating checks; real reports plane sections without
gating. The checker itself is unchanged."""
from dataclasses import replace

import numpy as np

from agents.baselines import failing
from agents.executors import CHECK_PROFILES, NOT_GATING, Slice, _summary, apply_profile, profile_of
from checker import load_thresholds, run_checks
from measure.runner import FieldRunner, Rod

TH = load_thresholds()


def failing_record():
    """A field-level rod whose plane sections fails: flank strain rates pushed apart."""
    m = FieldRunner().measure(Rod(), FieldRunner().initial_settings(Rod()))
    rec = m.record
    plus = rec.plus.copy()
    s = np.linspace(0, 1, plus.shape[1])[None, :, None]
    plus = plus + (plus - plus[:, :1]) * 0.002 * np.arange(len(plus))[:, None, None] * s
    return replace(rec, plus=plus, _fields=None), m.moved


def test_rigid_profile_window():
    from agents.executors import coverage_s, real_rigid_invariance, windowed
    from checker.checks import rigid_invariance
    from measure.record import arclength
    rec, mov = failing_record()
    s_cov = coverage_s(rec, mov)
    assert s_cov == min(float(np.nanmin(arclength(r.centre)[:, -1])) for r in (rec, mov))
    w = windowed(rec, 100.0)
    cut = w.fields["s_grid"] > 100.0
    assert np.all(np.isnan(w.fields["regr_mid"][:, cut])) and np.array_equal(
        w.fields["regr_mid"][:, ~cut], rec.fields["regr_mid"][:, ~cut], equal_nan=True)
    full = rigid_invariance(rec, mov, TH["rigid_invariance"])
    win = real_rigid_invariance(rec, mov, TH)
    assert win.detail.startswith("real-movie profile window") and win.value <= full.value + 1e-12


def test_profiles_defined():
    assert CHECK_PROFILES["synthetic"] == ("rigid_invariance", "closure", "plane_sections")
    assert CHECK_PROFILES["real"] == ("closure",)          # inbox item 20: rigid invariance reported, not gating


def test_synthetic_profile_unchanged():
    rec, mov = failing_record()
    raw = run_checks(rec, mov, TH)
    prof = apply_profile(run_checks(rec, mov, TH), "synthetic")
    assert [(c.check, c.passed, c.value, c.detail) for c in raw] == [(c.check, c.passed, c.value, c.detail) for c in prof]


def test_real_profile_reports_plane_sections_without_gating():
    rec, mov = failing_record()
    raw = {c.check: c for c in run_checks(rec, mov, TH)}
    assert raw["plane_sections"].passed is False
    prof = {c.check: c for c in apply_profile(run_checks(rec, mov, TH), "real")}
    ps = prof["plane_sections"]
    assert ps.passed is None and ps.value == raw["plane_sections"].value
    assert ps.detail.startswith(NOT_GATING) and "would fail" in ps.detail
    assert prof["closure"].passed == raw["closure"].passed and prof["closure"].detail == raw["closure"].detail
    rig = prof["rigid_invariance"]
    assert rig.passed is None and rig.value == raw["rigid_invariance"].value and rig.detail.startswith(NOT_GATING)
    s = _summary(list(prof.values()))
    assert "plane_sections" not in s["failed_checks"]
    assert s["reported_not_gating"] == ["rigid_invariance", "plane_sections"]
    assert "plane_sections" not in s["not_run"] and s["check_values"]["plane_sections"]["value"] == round(ps.value, 3)
    assert "plane_sections" not in failing(list(prof.values()))


def test_profile_from_record_setting():
    rec, _ = failing_record()
    assert profile_of(rec) == "synthetic"
    rec.settings = dict(rec.settings, movie="real")
    assert profile_of(rec) == "real"


class RealLikeRunner:
    """A field-level rod presented as a real movie (settings movie=real)."""
    def __init__(self):
        self.f = FieldRunner()

    def initial_settings(self, w):
        return self.f.initial_settings(Rod())

    def measure(self, w, settings):
        m = self.f.measure(Rod(), settings)
        rec, mov = failing_record()
        rec.settings = dict(rec.settings, movie="real")
        m.record, m.moved = rec, mov
        return m


def test_slice_uses_real_profile_for_real_movies():
    sl = Slice(RealLikeRunner(), Rod())
    t = sl.task()
    assert "plane_sections" not in t["failed_checks"] and t["reported_not_gating"] == ["rigid_invariance", "plane_sections"]
    sl2 = Slice(RealLikeRunner(), Rod(), profile="synthetic")
    assert "plane_sections" in sl2.task()["failed_checks"]


def _view(passed_ps, detail_ps):
    from audit.view import SUMMARIES, _check
    checks = [{"check": "closure", "value": 0.5, "threshold": 1.0, "unit": "px/h", "passed": True, "detail": "x"},
              {"check": "plane_sections", "value": 9.0, "threshold": 3.25, "unit": "%/h", "passed": passed_ps,
               "detail": detail_ps}]
    return {"run_id": "r01", "status": "decline", "final_checks": [_check(c) for c in checks], "steps": 1,
            "remedies_kept": [], "roll_backs": 0, "final_settings": {"width_free": False},
            "summaries": {k: None for k in SUMMARIES}, "z": {k: None for k in SUMMARIES}}


def test_auditor_table_unchanged_for_synthetic_and_marks_not_gating():
    from audit.view import batch_table
    syn = batch_table([_view(False, "flank difference")], {})
    assert syn["columns"]["checks"] == "check: [value, threshold, passed]; passed null = not run"
    assert syn["runs"][0]["checks"]["plane_sections"] == [9.0, 3.25, False]
    assert "gating" not in _view(False, "flank difference")["final_checks"][1]
    real = batch_table([_view(None, NOT_GATING + " (real-movie profile; would fail): x")], {})
    assert real["runs"][0]["checks"]["plane_sections"] == [9.0, 3.25, "not gating"]
    assert "not a pass/fail gate" in real["columns"]["checks"]


def test_real_windows_use_real_thresholds():
    from agents.executors import REAL_THRESHOLDS_FILE
    real = load_thresholds(REAL_THRESHOLDS_FILE)
    assert real["closure"] == 19.0 and real["rigid_invariance"] is None and real["plane_sections"] is None
    assert TH["closure"] == 1.0                                   # synthetic thresholds unchanged
    sl = Slice(RealLikeRunner(), Rod())
    assert next(c for c in sl.checks if c.check == "closure").threshold == 19.0
    sl2 = Slice(RealLikeRunner(), Rod(), thresholds=TH)           # explicit thresholds win
    assert next(c for c in sl2.checks if c.check == "closure").threshold == 1.0
