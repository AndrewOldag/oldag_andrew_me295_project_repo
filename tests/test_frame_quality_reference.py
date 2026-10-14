"""Real-movie frame_quality reference (spec 2026-10-13 Task B4; inbox fq-real item 5).

measure/info.py gives the `real` reference for records with settings movie: real and the
synthetic one otherwise. The synthetic output is unchanged (freeze v2).
"""
import copy
from pathlib import Path

import yaml

from measure import info
from measure.record import from_tracker_npz

FIX = Path(__file__).resolve().parent / "fixtures"


def rec(name, movie=None):
    r = from_tracker_npz(FIX / f"{name}.npz")
    if movie:
        r = copy.copy(r)
        r.settings = {**r.settings, "movie": movie}
    return r


def test_synthetic_reference_unchanged():
    ref = info.frame_quality(rec("growth_zone_clean_s1"))["reference"]
    assert ref == {"basis": "15 clean synthetic rods, 3 frames each",
                   "texture_contrast": {"median": 0.193, "lowest": 0.155},
                   "focus": {"median": 0.090, "lowest": 0.073}}
    assert info.frame_quality(rec("growth_zone_clean_s1", "synthetic"))["reference"] == ref


def test_real_reference_for_real_records():
    ref = info.frame_quality(rec("growth_zone_clean_s1", "real"))["reference"]
    assert set(ref) == {"basis", "texture_contrast", "focus"}
    assert ref["basis"].startswith("PROVISIONAL")
    assert ref["texture_contrast"] == {"median": 0.0648, "lowest": 0.0439}
    assert ref["focus"] == {"median": 0.0286, "lowest": 0.0213}


def test_real_section_marked_provisional():
    cfg = yaml.safe_load(info.FRAME_QUALITY_REFERENCE.read_text())
    assert cfg["real"]["provisional"] is True
    for k in ("texture_contrast", "focus"):
        assert cfg["real"][k]["lowest"] <= cfg["real"][k]["median"]
