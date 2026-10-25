"""Freeze v3 (docs/proposals/2026-10-23_freeze-v3.md): rod geometry, width-free ratio, no-growth tolerance,
v3 renders, metrics."""
import warnings
from dataclasses import replace

import numpy as np
import pytest

from checker import run_checks
from measure import info, metrics
from measure import render as base
from measure import render_heldout as H
from measure.record import PER_S_TO_PCT_PER_H, rigid_moved
from measure.rod import field_cases, make_record, simulate, stage_track, v3_cases
from measure.score import load_tolerance, rod_tolerance, truth_summary

V3 = {s.name: s for s in v3_cases()}
FIELD_SEPARATION = {"rigid_invariance": 0.05, "closure": 0.5, "plane_sections": 0.5}


# ---------------------------------------------------------------- geometry

def test_v3_growth_zone_values():
    t = make_record(V3["v3_growth_zone"]).truth
    s = truth_summary(t, 2.105)
    assert abs(s["peak_regr_pct_per_h"] - 54.0) < 0.3 and abs(s["peak_at_um"] - 421) <= 11
    spec = V3["v3_growth_zone"]
    assert np.isclose(spec.v(1e4) - spec.v(0.0), 96.0 / 3600.0)
    regr = np.asarray(spec.regr(np.arange(470.0, 501.0)))
    assert np.all(regr < 0.01 * float(spec.regr(200.0)))          # basal tracked end (500 px) not growing


def test_v3_stage_follows_tip_in_whole_pixels():
    spec = V3["v3_growth_zone"]
    times, X, S, K, centre = simulate(spec)
    stage = stage_track(spec, times, centre[:, 0])
    steps = np.abs(np.diff(stage, axis=0))
    assert np.allclose(stage, np.round(stage)) and (steps.max(axis=1) > 0).all() and steps.max() <= 4
    assert np.allclose(stage_track(V3["v3_still"], times, simulate(V3["v3_still"])[4][:, 0]), 0)


def test_v2_stage_unchanged():
    spec = next(s for s in field_cases() if s.name == "growth_zone")
    times, X, S, K, centre = simulate(spec)
    st = stage_track(spec, times, centre[:, 0])
    assert int((np.abs(np.diff(st, axis=0)).max(axis=1) > 0).sum()) == 5 and np.isclose(st[-1, 0], 52.5)


@pytest.mark.parametrize("name", sorted(V3))
def test_v3_field_cases_pass_the_approved_checker(name):
    """Field level, approved thresholds: every v3 case passes (v3_width_change at 3.0 against 3.25)."""
    import yaml
    from pathlib import Path
    thr = yaml.safe_load((Path(__file__).resolve().parents[1] / "config" / "checker_thresholds.yaml").read_text())
    rec = make_record(V3[name])
    moved = rigid_moved(rec, np.deg2rad(0.1) / 90.0, (0.5 / 90.0, 0.3 / 90.0))
    for r in run_checks(rec, moved, {k: thr[k] for k in FIELD_SEPARATION}):
        assert r.passed is True, (name, r)


def test_v3_bend_rates():
    for deg in (16, 20, 24, 30):
        spec = V3[f"v3_bend{deg}"]
        s = np.arange(-400.0, 800.0, 0.5)
        assert np.isclose(np.rad2deg(np.trapezoid(spec.kappa_rate(s), s)) * 3600.0, deg, rtol=1e-6)


# ---------------------------------------------------------------- width-free ratio (kinematics-1)

def _true_ratio(rec):
    t = rec.truth
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        h = np.nanmean(t["spacing"], axis=0) / 2.0
        return -h * np.nanmean(t["kappa_rate"], axis=0) / np.nanmean(t["regr_mid"], axis=0)


@pytest.mark.parametrize("spec", [s for s in field_cases() + v3_cases()
                                  if s.name in ("growth_zone", "bending", "width_change", "bend_continue",
                                                "bend_reverse") or (s.name.startswith("v3_")
                                                                    and s.name != "v3_still")],
                         ids=lambda s: s.name)
def test_width_free_ratio_equals_truth(spec):
    rec = make_record(spec)
    w = info.width_free_ratio(rec)
    got = np.array(w["width_free_ratio"], float)
    want = np.interp(w["width_free_ratio_s_um"], rec.fields["s_grid"] * rec.pixel_um, _true_ratio(rec))
    assert len(got) >= 10 and np.nanmax(np.abs(got - want)) < 1e-3


def test_width_free_ratio_removes_width_change_term():
    """v2 width_change: zero curvature rate. The v2 form D/S gave -0.035 to -0.435 (spec audit kinematics-1)."""
    rec = make_record(next(s for s in field_cases() if s.name == "width_change"))
    got = np.array(info.width_free_ratio(rec)["width_free_ratio"], float)
    assert np.nanmax(np.abs(got)) < 1e-3
    f = rec.fields
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        p, m = np.nanmean(f["regr_plus"], axis=0), np.nanmean(f["regr_minus"], axis=0)
        old = np.where((p + m) * PER_S_TO_PCT_PER_H > 5.0, (p - m) / (p + m), np.nan)
    assert np.nanmax(np.abs(old)) > 0.03


# ---------------------------------------------------------------- tolerance

def test_no_growth_tolerance():
    cfg = load_tolerance()
    still = make_record(V3["v3_still"]).truth
    assert rod_tolerance(still, 2.105, cfg)["regr_rms_pct_per_h"] == 0.5
    gz = make_record(V3["v3_growth_zone"]).truth
    assert np.isclose(rod_tolerance(gz, 2.105, cfg)["regr_rms_pct_per_h"],
                      0.025 * truth_summary(gz, 2.105)["peak_regr_pct_per_h"])


# ---------------------------------------------------------------- renders (short movies)

N = 5


@pytest.mark.parametrize("case", ["v3_growth_zone", "v3_bend30", "v3_still"])
def test_v3_render_keeps_tracked_part_in_frame(case):
    spec, movie = base.image_case(case, None, 20, moved=True)
    assert movie.track_length == 500.0
    times, X, S, K, centre = simulate(spec)
    stage = stage_track(spec, times, centre[:, 0])
    shift = np.array([0.0, movie.width / 2.0 - np.mean(centre[0, :, 1])])
    img = centre[:, X <= 500] + shift - stage[:, None, :]
    r = 2.0 * float(spec.h(0.0))
    assert img[..., 0].min() > r and img[..., 0].max() + 60 < movie.height
    assert img[..., 1].min() > r + 20 and img[..., 1].max() < movie.width - r - 20


def test_v3_width_change_in_frame():
    spec, movie = base.image_case("v3_growth_zone", "width_change", 20)
    assert spec.name == "v3_width_change"
    times, X, S, K, centre = simulate(spec)
    stage = stage_track(spec, times, centre[:, 0])
    shift = np.array([0.0, movie.width / 2.0 - np.mean(centre[0, :, 1])])
    img = centre[:, X <= 500] + shift - stage[:, None, :]
    assert img[..., 1].min() > 50 and img[..., 1].max() < movie.width - 50 and img[..., 0].min() > 30


def test_v3_render_and_stage_log_missing():
    spec, movie = H.image_case("v3_growth_zone", "stage_log_missing", 20, size=1)
    spec = replace(spec, n_frames=N)
    r = H.render(spec, movie)
    c = base.render(spec, base.image_case("v3_growth_zone", None, 20)[1])
    assert r["frames"].shape == (N, 768, 320)
    assert all(np.array_equal(a, b) for a, b in zip(r["frames"], c["frames"]))
    assert np.allclose(r["stage_px"], 0) and not np.allclose(c["stage_px"], 0)


def test_v3_heldout_uses_v3_zone():
    assert H.zone(V3["v3_growth_zone"])[0] == 200.0
    assert H.zone(next(s for s in field_cases() if s.name == "growth_zone"))[0] == 150.0


# ---------------------------------------------------------------- driver (offline)

def test_scored_set_and_plans_offline():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "synth"))
    import scored_v3 as S
    rods = S.scored_rods()
    assert len(rods) == 51 and len({r.id() for r in rods}) == 51
    exp = [S.EXPECTED[S.kind(r)] for r in rods]
    assert (exp.count("accept_clean"), exp.count("accept_repaired"), exp.count("decline")) == (18, 15, 18)
    assert {r.seed for r in rods} == {20, 21, 22} and {r.seed for r in S.basis_rods()} == {10, 11, 12, 13, 14}
    assert all(r.case.startswith("v3_") for r in rods + S.basis_rods())
    dpx = next(r for r in rods if r.fault == "displacement_exceeds_patch")
    assert S.initial(dpx).stride == 6
    assert [s for s, _ in S.label_states(dpx)] == [[], ["change_frame_stride/half"], ["change_frame_stride/half"] * 2]


# ---------------------------------------------------------------- metrics

def _run(rod, cls, status, good=True, repeat=0, kept=0):
    return {"method": "m", "rod": rod, "cls": cls, "repeat": repeat, "status": status,
            "category": metrics.category(status, cls, good), "remedies_kept": kept}


RODS = [("c1", "accept_clean"), ("c2", "accept_clean"), ("r1", "accept_repaired"), ("d1", "decline"),
        ("d2", "decline")]


def test_all_decline_reference():
    m = metrics.summarize(metrics.reference_runs(RODS, "all_decline"))
    assert m["accuracy_per_class"] == {"accept_clean": 0.0, "accept_repaired": 0.0, "decline": 1.0}
    assert np.isclose(m["balanced_accuracy"], 1 / 3) and m["overall_accuracy"] == 0.4
    assert m["abstention_precision"] == 0.4 and m["abstention_recall"] == 1.0
    assert m["coverage"] == 0.0 and m["false_accept_rate"] is None
    assert m["unnecessary_decline_rate"] == {"accept_clean": 1.0, "accept_repaired": 1.0}


def test_all_accept_reference():
    good = {"c1": True, "c2": False, "r1": False, "d1": False, "d2": True}
    m = metrics.summarize(metrics.reference_runs(RODS, "all_accept", good))
    assert m["accuracy_per_class"] == {"accept_clean": 0.5, "accept_repaired": 0.0, "decline": 0.0}
    assert m["false_accepts"] == 3 and m["false_accept_rate"] == 0.6 and m["coverage"] == 1.0
    assert m["categories"]["accept_on_decline"] == 1 and m["abstention_precision"] is None


def test_mixed_method():
    runs = [_run("c1", "accept_clean", "accept", kept=1), _run("c2", "accept_clean", "step_limit"),
            _run("r1", "accept_repaired", "accept", kept=2), _run("d1", "decline", "decline"),
            _run("d2", "decline", "accept", good=False)]
    m = metrics.summarize(runs)
    assert m["accuracy_per_class"] == {"accept_clean": 0.5, "accept_repaired": 1.0, "decline": 0.5}
    assert np.isclose(m["balanced_accuracy"], 2 / 3)
    assert np.isclose(m["false_accept_rate"], 1 / 3) and m["abstention_precision"] == 1.0
    assert m["abstention_recall"] == 0.5 and m["not_reported_per_class"]["accept_clean"] == 1
    assert m["remedies_kept_per_class"]["accept_clean"] == 1 and m["runs_with_remedy_kept_per_class"]["accept_clean"] == 1


def test_fleiss_kappa():
    assert metrics.fleiss_kappa([[3, 0], [0, 3], [3, 0]]) == 1.0
    assert metrics.fleiss_kappa([[3, 0], [3, 0]]) is None              # one category only
    # Fleiss 1971 style check: hand-computed value
    k = metrics.fleiss_kappa([[2, 1], [1, 2], [3, 0], [0, 3]])
    p_bar = (1 / 3 + 1 / 3 + 1 + 1) / 4
    assert np.isclose(k, (p_bar - 0.5) / 0.5)


def test_agreement_and_repeats():
    runs = []
    for k in range(3):
        runs += [_run("c1", "accept_clean", "accept", repeat=k), _run("d1", "decline", "decline", repeat=k),
                 _run("r1", "accept_repaired", "accept" if k < 2 else "decline", repeat=k)]
    a = metrics.agreement(runs)
    assert a["repeats"] == 3 and a["unanimous"] == 2 and np.isclose(a["unanimity_rate"], 2 / 3)
    assert a["unanimity_rate_per_class"]["accept_repaired"] == 0.0
    o = metrics.over_repeats(runs)
    assert o["accuracy_per_class"]["accept_repaired"] == {"mean": 2 / 3, "min": 0.0, "max": 1.0}
