"""Real executors with the in-process runner on field-level rods. No LLM, no tracker."""
import json
from dataclasses import replace
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
    rec = from_tracker_npz(FIXTURES / "growth_zone_clean_s0.npz")
    for remedy, settings in REMEDIES.items():
        for setting in settings:
            try:
                new, change = apply_remedy(s, remedy, setting, 15, rec)
                assert new != s and change
            except NotAvailable as e:
                raise AssertionError((remedy, setting, e))


def test_remedy_settings():
    s = TrackSettings(stride=12)
    assert apply_remedy(s, "change_frame_stride", "half", 15)[0].stride == 6
    assert apply_remedy(s, "enlarge_patch", "2x", 15)[0].disk_radius == 30
    with pytest.raises(NotAvailable):
        apply_remedy(TrackSettings(), "change_frame_stride", "half", 15)
    rec = from_tracker_npz(FIXTURES / "growth_zone_clean_s0.npz")
    new = apply_remedy(s, "register_frames", None, 15, rec)[0]
    assert new.args()[-3:] == ["--register", "--register-from-px", str(new.register_from_px)]
    assert 250 <= new.register_from_px <= 350          # growth zone of the clean rod ends near 300 px
    with pytest.raises(NotAvailable):
        apply_remedy(s, "register_frames", None, 15)    # no record, no band


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
    s2 = Slice(FieldRunner(), Rod("growth_zone"))
    r = s2.apply_remedy({"fault": "unknown", "remedy": "change_frame_stride", "setting": "half"}, {})
    assert not r["rechecked"] and "not available" in r["error"] and len(s2.runs) == 1


def test_width_free_ratio_skips_plane_sections():
    s = Slice(FieldRunner(), Rod("width_change"))
    r = s.apply_remedy({"fault": "width_change", "remedy": "use_width_free_ratio", "setting": None}, {})
    assert r["rechecked"] and "plane_sections" in r["not_run"]
    assert "plane_sections" not in r["failed_checks"]
    out = s.request_info({"kind": "velocity_profile"}, {})
    assert "width_free_ratio" in out and out["width_free_ratio"]


def test_switch_midline_source_removed():
    assert "switch_midline_source" not in REMEDIES


def test_loop_with_real_executors(tmp_path):
    s = Slice(FieldRunner(), Rod("growth_zone"))
    L = ScriptedLauncher([act(action="request_info", kind="velocity_profile"),
                          act(action="apply_remedy", fault="midline_jitter", remedy="smooth_midline", setting="light"),
                          act(action="accept", confidence=0.8)])
    out = Orchestrator(L, tmp_path / "t.jsonl").run("diagnostician", "rod-1", s.task(), s.executors())
    assert out.status == "accept" and out.steps == 3
    assert "peak_strain_rate_pct_per_h" in L.prompts[1]
    assert '"rechecked": true' in L.prompts[2]


def test_couple_is_a_run_setting_not_a_remedy():
    s = TrackSettings(couple=True)
    assert s.args()[-1] == "--couple" and s.tag().endswith("_cpl")
    assert TrackSettings().tag() != s.tag()
    assert "couple" not in REMEDIES and all("couple" not in str(v) for v in REMEDIES.values())
    rec = from_tracker_npz(FIXTURES / "growth_zone_clean_s0.npz")
    for remedy, settings in REMEDIES.items():          # every remedy keeps the mode
        for setting in settings:
            assert apply_remedy(replace(s, stride=4), remedy, setting, 15, rec)[0].couple


# ---- part D of spec 2026-10-10 (repair criteria): before-and-after values and roll back

def test_no_progress_rule():
    from checker.checks import CheckResult
    from agents.executors import no_progress
    c = lambda name, passed, value: CheckResult(name, passed, value, 1.0, "u")
    before = [c("closure", False, 4.0), c("plane_sections", True, 0.5)]
    assert no_progress(before, [c("closure", False, 3.5), c("plane_sections", True, 0.5)])        # lowered 12 %
    assert not no_progress(before, [c("closure", False, 3.0), c("plane_sections", True, 0.5)])    # lowered 25 %
    assert not no_progress(before, [c("closure", True, 0.5), c("plane_sections", True, 0.5)])     # now passes
    skipped = c("closure", None, float("nan")); skipped.detail = "skipped: width-free ratio reported; "
    assert not no_progress(before, [skipped, c("plane_sections", True, 0.5)])                     # skipped on purpose
    assert no_progress(before, [c("closure", None, float("nan")), c("plane_sections", True, 0.5)])  # no longer computable
    assert not no_progress([c("closure", True, 0.1)], [c("closure", True, 0.9)])                 # nothing failed


def test_roll_back_restores_settings_and_counts_the_step():
    s = Slice(FieldRunner(), Rod("rotation_basal_pivot"))             # closure fails at field level
    assert "closure" in s.task()["failed_checks"]
    r = s.apply_remedy({"fault": "rigid_drift", "remedy": "change_frame_stride", "setting": "double"}, {})
    assert r["rechecked"] and r["rolled_back"] and "closure" in r["failed_checks"]
    v = r["check_values"]["closure"]
    assert v["before"] is not None and v["after"] is not None and v["after"] > 0.75 * v["before"]
    assert s.runs[-1][0].stride == 1 and len(s.runs) == 3          # restored; the attempt is kept in the runs
    assert s.current.record.n_frames == s.runs[0][1].record.n_frames


def test_width_free_ratio_is_not_rolled_back():
    s = Slice(FieldRunner(), Rod("width_change"))
    r = s.apply_remedy({"fault": "width_change", "remedy": "use_width_free_ratio", "setting": None}, {})
    assert not r.get("rolled_back") and r["check_values"]["plane_sections"]["after"] is None
