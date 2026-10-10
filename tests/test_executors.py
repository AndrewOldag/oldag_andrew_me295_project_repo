"""Real executors with the in-process runner on field-level rods. No LLM, no tracker."""
import json
from pathlib import Path

import pytest

from agents.actions import INFO_KINDS, REMEDIES
from agents.executors import Slice
from agents.orchestrator import Orchestrator
from measure import info
from measure.record import from_tracker_npz
from measure.remedies import NotAvailable, TrackSettings, apply_remedy
from measure.runner import FieldRunner, Rod
from tests.test_orchestrator import ScriptedLauncher, act

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="module")
def sl():
    return Slice(FieldRunner(), Rod("growth_zone"))


def test_every_remedy_in_the_list_is_handled():
    s = TrackSettings(stride=4)
    for remedy, settings in REMEDIES.items():
        for setting in settings:
            try:
                new, change = apply_remedy(s, remedy, setting, 15)
                assert new != s and change
            except NotAvailable as e:
                assert remedy in ("switch_midline_source", "use_width_free_ratio"), (remedy, e)


def test_remedy_settings():
    s = TrackSettings(stride=12)
    assert apply_remedy(s, "change_frame_stride", "half", 15)[0].stride == 6
    assert apply_remedy(s, "enlarge_patch", "2x", 15)[0].disk_radius == 30
    with pytest.raises(NotAvailable):
        apply_remedy(TrackSettings(), "change_frame_stride", "half", 15)
    assert "--register" in apply_remedy(s, "register_frames", None, 15)[0].args()


def test_task_hides_the_rod(sl):
    task = sl.task()
    text = json.dumps(task)
    assert "growth_zone" not in text and "truth" not in text
    assert set(task["passed_checks"]) == {"rigid_invariance", "closure", "plane_sections"}


@pytest.mark.parametrize("kind", INFO_KINDS)
def test_request_info_every_kind(sl, kind):
    out = sl.request_info({"kind": kind}, {})
    json.dumps(out)
    assert isinstance(out, dict) and out


def test_info_on_tracker_record():
    rec = from_tracker_npz(FIXTURES / "growth_zone_clean_s0.npz")
    d = info.displacement_vs_patch_radius(rec)
    assert d["disk_radius_px"] == 15 and d["fraction_points_lost"] == 0
    v = info.velocity_profile(rec)
    assert 35 < v["peak_strain_rate_pct_per_h"] < 50


def test_apply_remedy_reruns_and_rechecks():
    s = Slice(FieldRunner(), Rod("growth_zone"))
    r = s.apply_remedy({"fault": "displacement_exceeds_patch", "remedy": "change_frame_stride",
                        "setting": "double"}, {})
    assert r["rechecked"] and r["change"] == "frame stride 1 -> 2" and len(s.runs) == 2
    assert s.current.record.n_frames == 21
    r = s.apply_remedy({"fault": "unknown", "remedy": "switch_midline_source", "setting": "ml"}, {})
    assert not r["rechecked"] and "not available" in r["error"] and len(s.runs) == 2


def test_loop_with_real_executors(tmp_path):
    s = Slice(FieldRunner(), Rod("growth_zone"))
    L = ScriptedLauncher([act(action="request_info", kind="velocity_profile"),
                          act(action="apply_remedy", fault="midline_jitter", remedy="smooth_midline", setting="light"),
                          act(action="accept", confidence=0.8)])
    out = Orchestrator(L, tmp_path / "t.jsonl").run("diagnostician", "rod-1", s.task(), s.executors())
    assert out.status == "accept" and out.steps == 3
    assert "peak_strain_rate_pct_per_h" in L.prompts[1]
    assert '"rechecked": true' in L.prompts[2]
