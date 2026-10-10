"""Clean image-level rods at the approved thresholds give the outcomes in IMAGE_EXPECTED.

Fixtures (tests/fixtures/): tracker output for seed 0 of the clean growth_zone
and rigid_rotation rods, each with its rigidly moved run.
"""
from pathlib import Path

import pytest

from checker import run_checks, load_thresholds
from measure.record import from_tracker_npz
from measure.render import IMAGE_EXPECTED

DATA = Path(__file__).resolve().parent / "fixtures"


def test_thresholds_are_approved():
    th = load_thresholds()
    assert th["status"] == "approved"
    assert (th["rigid_invariance"], th["closure"], th["plane_sections"]) == (2.0, 1.0, 3.25)


def test_rigid_rotation_expected_to_fail_closure_only():
    assert IMAGE_EXPECTED["rigid_rotation"] == {"rigid_invariance": True, "closure": False,
                                                "plane_sections": True}


@pytest.mark.parametrize("case", ["growth_zone", "rigid_rotation"])
def test_fixture_outcomes_match_expected(case):
    rec = from_tracker_npz(DATA / f"{case}_clean_s0.npz")
    moved = from_tracker_npz(DATA / f"{case}_clean_s0_moved.npz")
    res = {r.check: r.passed for r in run_checks(rec, moved, load_thresholds())}
    assert res == IMAGE_EXPECTED[case]
