"""Compound and novel fault injectors (measure/render_compound.py).

Short movies (5 frames, 320 px high) keep the renders fast. A compound movie equals the movie of its
components rendered by render.py and render_heldout.py where those can render it; with no fault it
equals render.render exactly.
"""
from dataclasses import replace

import numpy as np
import pytest

from measure import render as base
from measure import render_compound as C
from measure import render_heldout as H

N, HEIGHT = 5, 320
KEYS = ("frames", "stage_px", "midline_image", "mask0", "times")


def short(spec, movie, height=HEIGHT):
    return replace(spec, n_frames=N), replace(movie, height=height)


def same(a, b):
    return all(np.array_equal(a[k], b[k]) for k in KEYS)


def test_lists():
    from agents.actions import FAULTS
    assert set(C.COMPOUND_FAULTS) == set(C.COMPOUND) | set(C.NOVEL)
    assert not set(C.COMPOUND_FAULTS) & (set(base.DEV_FAULTS) | set(H.HELDOUT_FAULTS) | set(FAULTS))
    for f, comp in C.COMPOUND.items():
        assert len(comp) == 2 and set(comp) <= set(base.DEV_FAULTS) | set(H.HELDOUT_FAULTS)


def test_clean_equals_render():
    spec, movie = short(*C.image_case("v3_growth_zone", None, 40))
    s0, m0 = short(*base.image_case("v3_growth_zone", None, 40))
    assert same(C.render(spec, movie), base.render(s0, m0))


@pytest.mark.parametrize("fault", ["drift_low_texture", "drift_jitter", "low_texture_fast"])
def test_dev_pairs_equal_render_with_both_settings(fault):
    spec, movie = short(*C.image_case("v3_growth_zone", fault, 40))
    kw, speed = {}, 1.0
    for f, z in C.COMPOUND[fault].items():
        m, _, sp = base.fault_settings(f, z)
        kw.update(m)
        speed *= sp
    s0, m0 = base._image_case_v3("v3_growth_zone", None, kw, speed, 40, False)
    s0, m0 = short(s0, m0)
    assert same(C.render(spec, movie), base.render(s0, m0))
    assert not same(C.render(spec, movie), base.render(*short(*base.image_case("v3_growth_zone", None, 40))))


@pytest.mark.parametrize("comp,size", [("second_root", "30"), ("partial_occlusion", "20")])
def test_heldout_component_alone_equals_render_heldout(comp, size, monkeypatch):
    monkeypatch.setitem(C.COMPOUND, "one", {comp: size})
    spec, movie = short(*C.image_case("v3_growth_zone", "one", 40), height=768)
    s0, m0 = short(*H.image_case("v3_growth_zone", comp, 40, size=size), height=768)
    assert same(C.render(spec, movie), H.render(s0, m0))


def test_second_root_occlusion_differs_from_each_component():
    spec, movie = short(*C.image_case("v3_growth_zone", "second_root_occlusion", 40), height=768)
    both = C.render(spec, movie)
    for comp, size in C.COMPOUND["second_root_occlusion"].items():
        s0, m0 = short(*H.image_case("v3_growth_zone", comp, 40, size=size), height=768)
        assert not same(both, H.render(s0, m0))


def test_focus_drift_blurs_later_frames_only():
    spec, movie = short(*C.image_case("v3_growth_zone", "focus_drift", 40, size="4"))
    clean = base.render(*short(*base.image_case("v3_growth_zone", None, 40)))
    r = C.render(spec, movie)
    assert np.array_equal(r["frames"][0], clean["frames"][0])
    assert all(not np.array_equal(r["frames"][i], clean["frames"][i]) for i in range(1, N))
    assert C.blur_at(N - 1, N, movie) == 4.0 and C.blur_at(0, N, movie) == 0.0
    # blur lowers the frame-to-frame texture variance inside the root
    assert r["frames"][-1].astype(float).std() < clean["frames"][-1].astype(float).std()
    assert same({k: r[k] for k in KEYS if k != "frames"} | {"frames": r["frames"][:1]},
                {k: clean[k] for k in KEYS if k != "frames"} | {"frames": clean["frames"][:1]})


def test_flicker_changes_brightness_not_geometry():
    spec, movie = short(*C.image_case("v3_growth_zone", "illumination_flicker", 40, size="0.2"))
    clean = base.render(*short(*base.image_case("v3_growth_zone", None, 40)))
    r = C.render(spec, movie)
    g = C.gains(N, movie)
    assert not np.allclose(g, 1.0) and g.min() >= 0.5 and g.max() <= 1.5
    for k in ("stage_px", "midline_image", "mask0", "times"):
        assert np.array_equal(r[k], clean[k])
    ratio = np.median(r["frames"].reshape(N, -1).astype(float), axis=1) / \
        np.median(clean["frames"].reshape(N, -1).astype(float), axis=1)
    assert np.allclose(ratio, g, rtol=0.03)


def test_novel_needs_size_and_v3_only():
    with pytest.raises(ValueError):
        C.image_case("v3_growth_zone", "focus_drift", 40)
    with pytest.raises(ValueError):
        C.image_case("growth_zone", "drift_jitter", 40)


def test_moved_copy_adds_the_invariance_motion():
    _, m = C.image_case("v3_growth_zone", "drift_jitter", 40, moved=True)
    _, m0 = C.image_case("v3_growth_zone", "drift_jitter", 40)
    assert m.rigid_rotation > m0.rigid_rotation and m.midline_jitter == 3.0 and m.contrast == m0.contrast


def test_rod_id():
    assert base.rod_id("v3_growth_zone", "drift_jitter", 40) == "v3_growth_zone_drift_jitter_s40"
    assert base.rod_id("v3_growth_zone", "focus_drift", 41, size="4") == "v3_growth_zone_focus_drift_z4_s41"
