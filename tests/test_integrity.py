"""Track-integrity check (spec 2026-11-20 R3) on the clean tracker fixture and on damaged copies of it."""
from dataclasses import replace
from pathlib import Path

import numpy as np

from checker import integrity_gate, track_integrity
from measure.record import from_tracker_npz

DATA = Path(__file__).resolve().parent / "fixtures"
TH = {"inversions": 0, "gap_ratio": 3.0, "lateral_px": 2.0}


def clean():
    return from_tracker_npz(DATA / "growth_zone_clean_s0.npz")


def values(rec, th=TH):
    return {r.check: r for r in track_integrity(rec, th)}


def test_clean_track_passes():
    v = values(clean())
    assert v["integrity_inversions"].value == 0 and v["integrity_inversions"].passed
    assert v["integrity_gap_ratio"].passed and v["integrity_lateral"].value < 0.5
    assert v["registration_plausible"].passed is None
    assert integrity_gate(list(v.values()))


def test_swapped_points_are_inversions():
    rec = clean()
    c = rec.centre.copy()
    c[10, [5, 6]] = c[10, [6, 5]]
    v = values(replace(rec, centre=c))
    assert v["integrity_inversions"].value >= 1 and v["integrity_inversions"].passed is False
    assert v["integrity_inversions"].where_frame_pair == 10
    assert not integrity_gate(list(v.values()))


def test_lateral_scatter_and_gap():
    rec = clean()
    rng = np.random.default_rng(0)
    c = rec.centre + rng.normal(0, 10, rec.centre.shape) * np.array([0, 1])
    v = values(replace(rec, centre=c), {})
    assert v["integrity_lateral"].value > 5 and v["integrity_lateral"].passed is None
    c = rec.centre.copy()
    c[:, 8:] += 200 * (c[:, 8:9] - c[:, 7:8]) / np.linalg.norm(c[:, 8:9] - c[:, 7:8], axis=2, keepdims=True)
    assert values(replace(rec, centre=c))["integrity_gap_ratio"].passed is False


def test_registration_report():
    rec = clean()
    for report, expect in (({"final_rotation_deg": 9.2}, None),
                           ({"plausible": False, "final_rotation_deg": 9.2}, False),
                           ({"plausible": True, "final_rotation_deg": 0.1}, True)):
        s = dict(rec.settings, preprocess={"register": report})
        assert values(replace(rec, settings=s))["registration_plausible"].passed is expect


def test_threshold_rounding():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from integrity_thresholds import round_up_2sf
    assert [round_up_2sf(x) for x in (2.3295, 0.0537, 123.4, 0.0)] == [2.4, 0.054, 130, 0.0]


K = {"inversions": 1.5, "gap_ratio": 1.5, "lateral": 3.0}


def test_relative_gate_same_track_passes():
    from checker import load_relative_k, relative_integrity
    assert set(load_relative_k()) == set(K)
    res = {r.check: r for r in relative_integrity(clean(), clean(), load_relative_k())}
    assert res["integrity_rel_inversions"].value == 1.0 and res["integrity_rel_lateral"].value == 1.0
    assert integrity_gate(list(res.values()))


def test_relative_gate_fails_on_lost_order_and_scatter():
    from checker import relative_integrity
    rec = clean()
    c = rec.centre.copy()
    c[10, [5, 6]] = c[10, [6, 5]]
    c[20, [8, 9]] = c[20, [9, 8]]
    res = {r.check: r for r in relative_integrity(replace(rec, centre=c), rec, K)}
    assert res["integrity_rel_inversions"].value >= 3 and res["integrity_rel_inversions"].passed is False
    rng = np.random.default_rng(1)
    scattered = rec.centre + rng.normal(0, 2.0, rec.centre.shape) * np.array([0, 1])
    res = {r.check: r for r in relative_integrity(replace(rec, centre=scattered), rec, K)}
    assert res["integrity_rel_lateral"].passed is False and not integrity_gate(list(res.values()))


def test_relative_gate_keeps_registration_plausibility():
    from checker import relative_integrity
    rec = clean()
    rem = replace(rec, settings=dict(rec.settings, preprocess={"register": {"plausible": False}}))
    res = relative_integrity(rem, rec, K)
    assert [r.passed for r in res if r.check == "registration_plausible"] == [False] and not integrity_gate(res)


def test_zero_base_lateral_uses_clean_floor():
    """Field-level synthetic rod: base lateral exactly 0 -> ratio against lateral_px, finite; zero over zero -> 0."""
    from checker.checks import integrity_ratios, CheckResult
    def res(lat):
        return [CheckResult("integrity_inversions", True, 0, 0, ""), CheckResult("integrity_gap_ratio", True, 1.2, 2.4, ""),
                CheckResult("integrity_lateral", True, lat, 0.081, "px")]
    assert integrity_ratios(res(0.0), res(0.0))["lateral"] == 0.0
    r = integrity_ratios(res(0.1), res(0.0))["lateral"]
    assert np.isfinite(r) and abs(r - 0.1 / 0.081) < 1e-9
    assert integrity_ratios(res(0.3), res(0.1))["lateral"] == 0.3 / 0.1
