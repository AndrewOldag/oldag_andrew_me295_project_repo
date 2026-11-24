"""Reference-set helpers (task c035): overlay predictions agree with the particle-path check; sample rule."""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checker.zone_checks import particle_path, tip_frame_positions  # noqa: E402
from measure.rod import make_record, v3_cases  # noqa: E402
from zone_reference import (_draw, _hours, allocate, append_labels, on_midline, predicted_positions,  # noqa: E402
                            read_labels, reference_thresholds, window_frames)

CASES = {c.name: c for c in v3_cases()}


def test_overlay_prediction_matches_check():
    rec = make_record(CASES["v3_growth_zone"])
    P, S = predicted_positions(rec), tip_frame_positions(rec)
    e = (P[-1] - S[-1])[np.isfinite(P[-1])]
    v = particle_path(rec).values
    assert np.isclose(np.mean(e), v["pp_common_px"]) and np.isclose(np.sqrt(np.mean(e ** 2)), v["pp_rms_px"])
    assert np.allclose(P[0][np.isfinite(P[0])], S[0][np.isfinite(P[0])])


def test_on_midline_walks_arc_length():
    line = np.array([[0.0, 0.0], [0.0, 10.0], [10.0, 10.0]])
    p = on_midline(line, np.array([0.0, 5.0, 15.0, 25.0, -1.0]))
    assert np.allclose(p[:3], [[0, 0], [0, 5], [5, 10]]) and np.isnan(p[3:]).all()


def test_window_frames_and_hours():
    assert _hours("0727_cc4__w22-23.63") == (22.0, 23.63)
    el = np.arange(0, 3 * 3600 + 1, 90.0)
    assert len(window_frames(el, 0, 2)) == 81 and window_frames(el, 2, 4)[0] == 80


def test_allocate_extension_quota():
    sizes = {"control": 368, "control then control": 42, "mannitol": 291, "mannitol then control": 272,
             "mannitol then mannitol": 61}
    assert allocate(126, sizes) == {"control": 45, "control then control": 5, "mannitol": 36,
                                    "mannitol then control": 33, "mannitol then mannitol": 7}
    assert allocate(3, {"a": 1, "b": 1, "c": 1, "d": 1}) == {"a": 1, "b": 1, "c": 1, "d": 0}


def test_draw_caps_windows_per_root_and_skips_taken():
    pool = {"x": [{"window": f"r{i % 3}__w{i}", "root": f"r{i % 3}"} for i in range(12)]}
    taken = {"r0__w0": {"window": "r0__w0", "root": "r0"}}
    rows = _draw(pool, {"x": 10}, np.random.default_rng(1), taken, 2)
    roots = [r["root"] for r in rows]
    assert len(rows) == 5 and roots.count("r0") == 1 and roots.count("r1") == 2 and roots.count("r2") == 2
    assert "r0__w0" not in {r["window"] for r in rows} and [r["order"] for r in rows] == [1, 2, 3, 4, 5]


def test_append_labels_keeps_existing(tmp_path):
    p = tmp_path / "labels.csv"
    append_labels(p, ["a", "b"])
    p.write_text(p.read_text().replace("a,\n", "a,clean\n"))
    append_labels(p, ["a", "b", "c", "d"])
    assert p.read_text() == "window,label\na,clean\nb,\nc,\nd,\n"


def test_reference_thresholds_rule_and_labels(tmp_path):
    rows = [{"label": "clean", "pp_shape_rel": x, "pp_common_rel": 2 * x} for x in np.linspace(0.01, 0.02, 20)]
    rows.append({"label": "not clean", "pp_shape_rel": 9.0, "pp_common_rel": 9.0})
    th = reference_thresholds(rows)
    assert th == {"pp_shape_rel": 0.03, "pp_common_rel": 0.06}
    assert reference_thresholds(rows[:11] + rows[-1:]) is None
    p = tmp_path / "labels.csv"
    p.write_text("window,label\na,clean\nb,not clean\n")
    assert read_labels(p, ["a", "b"]) == {"a": "clean", "b": "not clean"}
    p.write_text("window,label\na,clean\nb,\n")
    with pytest.raises(AssertionError):
        read_labels(p, ["a", "b"])


def test_slide_moves_common_mode_only():
    rec = make_record(CASES["v3_growth_zone"])
    v0 = particle_path(rec).values
    v1 = particle_path(rec, slide_px=30.0).values
    assert np.isclose(v1["pp_common_px"], v0["pp_common_px"] - 30.0)
    assert np.isclose(v1["pp_shape_rms_px"], v0["pp_shape_rms_px"])


def test_ref_flags_and_smallest_caught():
    from zone_reference import ref_flags, smallest_caught
    th = {"pp_shape_rel": 0.14, "pp_common_rel": 0.5}
    assert ref_flags({"pp_shape_rel": 0.2, "pp_common_rel": None}, th) == {"shape": True, "common": None}
    res = {-30: [True] * 9 + [False], 30: [True] * 10, -15: [True] * 10, 15: [True] * 8 + [False] * 2}
    assert smallest_caught(res, (-30, -15, 15, 30)) == 30
    assert smallest_caught({-15: [False], 15: [True]}, (-15, 15)) is None
