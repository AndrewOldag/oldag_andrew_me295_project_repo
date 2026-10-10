"""Outcome categories and repair labels (spec 2026-10-10, repair criteria). Made-up outcomes."""
import pytest

from checker.checks import CheckResult
from measure.score import (checks_pass, diagnosis_correct, label_rod, measurement_good,
                           outcome_category)

TOL = {"regr_rms_pct_per_h": 1.0, "flank_difference_rms_pct_per_h": 1.0}


@pytest.mark.parametrize("status,label,good,expected", [
    ("accept", "repairable", True, "good_report"),
    ("accept", "not repairable", True, "good_report"),
    ("accept", "repairable", False, "false_accept"),
    ("accept", "not repairable", False, "false_accept"),
    ("decline", "not repairable", False, "correct_decline"),
    ("decline", "repairable", False, "unnecessary_decline"),
    ("step_limit", "repairable", True, "not_reported"),
    ("error", "not repairable", False, "not_reported"),
])
def test_outcome_table(status, label, good, expected):
    assert outcome_category(status, label, good) == expected


def test_measurement_good_and_width_free():
    err = {"regr_rms_pct_per_h": 0.5, "flank_difference_rms_pct_per_h": 2.0}
    assert not measurement_good(err, TOL)
    assert measurement_good(err, TOL, width_free=True)


def test_checks_pass_ignores_skipped():
    c = lambda name, p: CheckResult(name, p, 0.0, 1.0, "u")
    assert checks_pass([c("a", True), c("b", True), c("plane_sections", None)])
    assert not checks_pass([c("a", True), c("b", False)])
    assert not checks_pass([c("a", None)])


def test_label_rod():
    states = [{"sequence": [], "checks_pass": False, "good": False},
              {"sequence": ["change_frame_stride/half"], "checks_pass": False, "good": True},
              {"sequence": ["change_frame_stride/half"] * 2, "checks_pass": True, "good": True}]
    assert label_rod(states) == ("repairable", ["change_frame_stride/half"] * 2)
    states[2]["good"] = False
    assert label_rod(states) == ("not repairable", None)
    assert label_rod([{"sequence": ["a", "b", "c"], "checks_pass": True, "good": True}])[0] == "not repairable"


def test_diagnosis():
    assert diagnosis_correct("rigid_drift", "rigid_drift") and not diagnosis_correct("low_texture", "rigid_drift")
