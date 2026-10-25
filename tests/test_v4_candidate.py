"""Freeze v4 candidate switch (agents/candidate.py; inbox diag-analysis item 3): off by default, and C1, C2 and
C3 option (a) only when on. The check against the v3 runs is scripts/synth/v4_replay_check.py."""
from pathlib import Path

import pytest

from agents import candidate
from agents.executors import BlindSlice, Slice
from agents.launcher import load_config
from agents.orchestrator import PROMPTS, system_prompt_file
from checker.checks import CheckResult
from measure import info
from measure.record import from_tracker_npz
from measure.runner import FieldRunner, Rod
from measure.score import checks_pass

FIX = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(autouse=True)
def _reset():
    candidate.reset()
    yield
    candidate.reset()


def test_off_by_default():
    assert load_config()["candidate"] is None
    assert candidate.active() is None and not candidate.v4()
    for agent in ("diagnostician", "single_agent", "dispatcher", "auditor"):
        assert system_prompt_file(agent) == PROMPTS / f"{agent}.md"


def test_unknown_candidate_refused():
    with pytest.raises(ValueError):
        candidate.use("v5")


def test_c1_prompts_on():
    candidate.use("v4")
    assert system_prompt_file("diagnostician") == PROMPTS / "diagnostician_v4.md"
    assert system_prompt_file("single_agent") == PROMPTS / "single_agent_v4.md"
    assert system_prompt_file("dispatcher") == PROMPTS / "dispatcher.md"


def _added(agent):
    old = (PROMPTS / f"{agent}.md").read_text(encoding="utf-8").splitlines()
    new = (PROMPTS / f"{agent}_v4.md").read_text(encoding="utf-8").splitlines()
    it = iter(new)
    assert all(line in it for line in old)            # every v3 line kept, in order
    rest = list(new)
    for line in old:
        rest.remove(line)
    return rest


def test_c1_same_section_for_both_agents():
    added = _added("diagnostician")
    assert added == _added("single_agent")
    text = "\n".join(added)
    assert "Listed remedies by fault:" in text
    assert "- rigid_drift, bad_stage_correction: `register_frames`." in text
    assert "- Decline without a remedy only when no listed remedy is mapped to the fault you name" in text


def test_c2_only_when_on():
    sl = Slice(FieldRunner(), Rod("growth_zone"))
    off = sl.request_info({"kind": "stage_log_summary"}, {})
    assert off == info.stage_log_summary(sl.current.record)
    candidate.use("v4")
    on = sl.request_info({"kind": "stage_log_summary"}, {})
    assert {k: on[k] for k in off} == off
    assert {"moves_every_pair", "closure_residual_px_per_pair_median", "closure_residual_px_per_pair_max",
            "closure_residual_max_pair_index"} <= set(on)
    blind = BlindSlice(FieldRunner(), Rod("growth_zone")).request_info({"kind": "stage_log_summary"}, {})
    assert set(blind) == set(on)                       # single agent gets the same evidence


def test_c2_spread_on_drift():
    """Steady drift: residual on every pair, so the max is close to the median."""
    s = info.stage_log_spread(from_tracker_npz(FIX / "growth_zone_rigid_drift_z0.5_s0.npz"))
    assert s["closure_residual_px_per_pair_median"] > 0
    assert s["closure_residual_px_per_pair_max"] < 3 * s["closure_residual_px_per_pair_median"]


def _c(name, passed, detail="", value=1.0):
    return CheckResult(name, passed, value, 1.0, "u", detail=detail)


def test_c3a_not_computable_fails_only_when_asked():
    checks = [_c("rigid_invariance", True), _c("closure", None, "no basal point tracked in every frame",
                                                float("nan")), _c("plane_sections", True)]
    assert checks_pass(checks)                         # v3 label rule: dropped
    assert not checks_pass(checks, not_computable_fails=True)


def test_c3a_skipped_and_not_gating_still_dropped():
    checks = [_c("rigid_invariance", None, "reported, not gating (real-movie profile; would pass): x"),
              _c("closure", True), _c("plane_sections", None, "skipped: width-free ratio reported; x")]
    assert checks_pass(checks, not_computable_fails=True)
