"""Reference-set helpers (task c035): overlay predictions agree with the particle-path check; sample rule."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checker.zone_checks import particle_path, tip_frame_positions  # noqa: E402
from measure.rod import make_record, v3_cases  # noqa: E402
from zone_reference import _hours, on_midline, predicted_positions, window_frames  # noqa: E402

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
