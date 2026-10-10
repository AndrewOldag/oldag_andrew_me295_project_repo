"""Checker: no LLM dependency, and the expected pass or fail on every field-level rod."""
import ast
from pathlib import Path

import numpy as np
import pytest

from checker import run_checks
from measure.record import rigid_moved
from measure.rod import field_cases, make_record

CHECKER_DIR = Path(__file__).resolve().parents[1] / "checker"

# Separation thresholds for field-level rods only. They show the checks can
# tell the cases apart; they are not the thresholds used to score anything.
FIELD_SEPARATION = {"rigid_invariance": 0.05, "closure": 0.5, "plane_sections": 0.5}


def test_checker_imports_nothing_from_agents():
    for path in CHECKER_DIR.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for n in names:
                assert not n.split(".")[0] in ("agents", "anthropic", "claude_agent_sdk"), (path, n)


@pytest.mark.parametrize("spec", field_cases(), ids=lambda s: s.name)
def test_field_case_expected_outcome(spec):
    rec = make_record(spec)
    moved = rigid_moved(rec, np.deg2rad(0.1) / 90.0, (0.5 / 90.0, 0.3 / 90.0))
    results = {r.check: r for r in run_checks(rec, moved, FIELD_SEPARATION)}
    for check, expected in spec.expected.items():
        assert results[check].passed is expected, (check, results[check])


def test_failure_location_is_reported():
    spec = next(s for s in field_cases() if s.name == "width_change")
    r = {c.check: c for c in run_checks(make_record(spec), None, FIELD_SEPARATION)}
    ps = r["plane_sections"]
    assert ps.passed is False and ps.where_s_px is not None and ps.unit == "%/h"
    assert r["rigid_invariance"].passed is None      # no moved run supplied
