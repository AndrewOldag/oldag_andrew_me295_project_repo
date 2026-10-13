"""Diagnostician fixes P1-P5 (docs/proposals/2026-10-12_diagnostician-misses.md; spec 2026-10-12 item 4).

Fixtures: tracker output, seed 0 (development only), of the clean growth_zone rod (s0; s1 from the basis
runs, which carries frame quality) and of the fault each field targets.
"""
from pathlib import Path

from agents.executors import Slice
from measure import info
from measure.record import from_tracker_npz
from measure.runner import FieldRunner, Rod

FIX = Path(__file__).resolve().parent / "fixtures"
PROMPT = Path(__file__).resolve().parents[1] / "agents" / "prompts" / "diagnostician.md"


def rec(name):
    return from_tracker_npz(FIX / f"{name}.npz")


def test_p1_closure_residual_per_hour():
    """Unlogged drift: the closure residual comes from pairs without a stage move."""
    clean = info.stage_log_summary(rec("growth_zone_clean_s0"))
    drift = info.stage_log_summary(rec("growth_zone_rigid_drift_z0.5_s0"))
    assert clean["closure_residual_px_per_h_elsewhere"] < 0.5 and clean["closure_residual_px_per_h_at_moves"] < 0.5
    assert drift["closure_residual_px_per_h_elsewhere"] > 5.0                       # measured 7.12
    assert drift["closure_residual_px_per_h_elsewhere"] > 3 * drift["closure_residual_px_per_h_at_moves"]


def test_p4_flank_spacing_rate():
    """width_change: flank spacing +40 % per hour, ln(1.4) = 33.6 %/h; clean rod about zero."""
    clean = info.velocity_profile(rec("growth_zone_clean_s0"))
    wide = info.velocity_profile(rec("growth_zone_width_change_s0"))
    assert len(clean["flank_spacing_rate_pct_per_h"]) == len(clean["s_um"])
    assert clean["flank_spacing_rate_max_abs_pct_per_h"] < 5.0                      # measured 2.7
    assert 30.0 < wide["flank_spacing_rate_max_abs_pct_per_h"] < 40.0                # measured 35.3
    mid = sorted(x for x in wide["flank_spacing_rate_pct_per_h"] if x is not None)
    assert 30.0 < mid[len(mid) // 2] < 37.0


def test_p5_frame_quality_reference():
    ref = info.frame_quality(rec("growth_zone_clean_s1"))["reference"]
    assert set(ref) == {"basis", "texture_contrast", "focus"}
    assert ref["texture_contrast"]["lowest"] <= ref["texture_contrast"]["median"]
    clean = info.frame_quality(rec("growth_zone_clean_s1"))["frames"]
    low = info.frame_quality(rec("growth_zone_low_texture_z0.03_s0"))["frames"]
    assert all(f["texture_contrast"] >= ref["texture_contrast"]["lowest"] for f in clean)
    assert all(f["focus"] >= ref["focus"]["lowest"] for f in clean)
    assert all(f["texture_contrast"] < ref["texture_contrast"]["lowest"] / 2 for f in low)   # 0.06 against 0.155
    assert all(f["focus"] < ref["focus"]["lowest"] / 2 for f in low)


def test_p3_no_further_setting_after_light():
    s = Slice(FieldRunner(), Rod("growth_zone"))
    r = s.apply_remedy({"fault": "midline_jitter", "remedy": "smooth_midline", "setting": "light"}, {})
    assert r["rechecked"] and r["settings_left"].startswith("no further setting")
    r = s.apply_remedy({"fault": "displacement_exceeds_patch", "remedy": "change_frame_stride", "setting": "double"}, {})
    assert "settings_left" not in r                       # stride can still be halved or doubled


def test_prompt_has_each_new_line():
    text = PROMPT.read_text()
    for line in [
        "- Rigid-body invariance adds a known rigid motion to the images and checks that the strain rate does not "
        "change. It tests the tracker. Drift or rotation of the whole root in the movie passes it",
        "- Closure compares the tip motion from the midline and stage log with the tip motion given by the tracked "
        "kinematics. Unlogged drift or rotation fails closure",
        "- Plane sections compares the flank difference with flank spacing times the curvature rate, for constant width",
        "- If a remedy lowered a failing check and can be applied again or has a next setting, do that before testing "
        "another fault",
        "- After a stride or patch remedy, request `displacement_vs_patch_radius` again before choosing the next action",
        "- A remedy has failed when a failing check still fails and the remedy cannot be applied again or has no next "
        "setting. Then decline, naming the fault the remedy targeted, unless another fault has its own evidence",
        "- A flank spacing that changes in time is a width change: a physical cause, not a measurement fault. "
        "Use the width-free ratio",
        "- Low texture or blur also makes the midline and the tracked points jitter. Check `frame_quality` before "
        "naming `midline_jitter`",
    ]:
        assert line in text, line
    assert "may be applied again or at its next setting" not in text
    assert "under osmotic treatment" not in text
