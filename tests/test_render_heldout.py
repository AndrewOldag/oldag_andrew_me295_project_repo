"""Held-out fault injectors (measure/render_heldout.py): each changes the movie; size 0 leaves it unchanged.

Short movies (9 frames) keep the renders fast; every injector acts inside 9 frames.
"""
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial import cKDTree

from measure import render as base
from measure import render_heldout as H

ROOT = Path(__file__).resolve().parents[1]
SIZES = {"second_root": 30, "fast_rotation": 4, "bad_stage_correction": 10, "flank_swap": 0.5,
         "partial_occlusion": 30}
N = 9


def short(fault, size, moved=False):
    spec, movie = H.image_case("growth_zone", fault, 0, moved, size=size)
    return replace(spec, n_frames=N), movie


@pytest.fixture(scope="module")
def clean():
    spec, movie = base.image_case("growth_zone", None, 0)
    return base.render(replace(spec, n_frames=N), movie)


def same(a, b):
    return all(np.array_equal(a[k], b[k]) for k in ("frames", "stage_px", "midline_image", "mask0", "times"))


def test_lists_match_agent_faults():
    from agents.actions import FAULTS
    assert set(H.HELDOUT_FAULTS) == set(SIZES)
    assert not set(H.HELDOUT_FAULTS) & set(base.DEV_FAULTS)
    for f, e in H.EXPECTED.items():
        assert e["fault"] in FAULTS and e["outcome"] in ("accept", "decline")


def test_no_fault_equals_render(clean):
    assert same(H.render(*short(None, None)), clean)


@pytest.mark.parametrize("fault", sorted(SIZES))
def test_size_zero_unchanged(fault, clean):
    assert same(H.render(*short(fault, 0)), clean)


@pytest.mark.parametrize("fault", sorted(SIZES))
def test_injector_changes_movie(fault, clean):
    r = H.render(*short(fault, SIZES[fault]))
    assert not same(r, clean)
    T = len(clean["frames"])
    changed = [not np.array_equal(r["frames"][i], clean["frames"][i]) for i in range(T)]
    if fault == "bad_stage_correction":
        _, k = H.logged_stage(clean["stage_px"], SIZES[fault])
        assert not any(changed)                                     # images as recorded; only the log is wrong
        err = np.linalg.norm(clean["stage_px"] - r["stage_px"], axis=1)
        assert np.allclose(err[:k], 0) and np.allclose(err[k:], SIZES[fault])
    elif fault == "flank_swap":
        k = H.swap_from(T, SIZES[fault])
        assert changed == [i >= k for i in range(T)]
    elif fault == "partial_occlusion":
        assert changed == [H.occluded(i, T) for i in range(T)]
    elif fault == "fast_rotation":
        assert not any(changed[:T // 2]) and all(changed[T // 2:])
        assert np.isclose(H.burst_angle(T - 1, T, 4), np.deg2rad(4 * H.BURST_FRAMES))
    else:
        assert all(changed)


def test_second_root_reaches_size_past_edge():
    """The second root's outline ends `size` px past the main root's near edge: its pixels at the last
    frame reach the main midline for size 30 (the main radius), and stay outside the root for size 1."""
    for size, reach in ((30, True), (1, False)):
        spec, movie = short("second_root", size)
        r = H.render(spec, movie)
        c = base.render(spec, base.image_case("growth_zone", None, 0)[1])
        diff = np.abs(r["frames"][-1].astype(float) - c["frames"][-1]) > 200
        mid = r["midline_image"][-1]
        d, _ = cKDTree(mid).query(np.argwhere(diff))
        assert (d.min() < 3) == reach


def test_make_rod_dry_run_heldout():
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "synth" / "make_rod.py"), "--out", ".",
                          "--fault", "flank_swap", "--size", "0.5", "--seed", "1", "--dry-run"],
                         capture_output=True, text=True, check=True).stdout
    assert json.loads(out.strip().splitlines()[-1]) == {"id": "growth_zone_flank_swap_z0.5_s1", "stride": 1}
