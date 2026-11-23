"""Supplement c029b driver (scripts/synth/heldout_supplement.py): candidates and the selection rule."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "synth"))
import heldout_supplement as S  # noqa: E402


def test_candidates_48_in_seed_then_kind_order_and_new_seeds():
    c = S.candidates()
    assert len(c) == 48 and len({r.id() for r in c}) == 48
    assert [(r.seed, r.fault) for r in c[:7]] == [(60, f) for f in S.KINDS] + [(61, S.KINDS[0])]
    assert not set(S.SEEDS) & {40, 41, 42, 43, 50, 51}
    assert c[4].id() == "v3_growth_zone_focus_drift_z1.5_s60"


def test_select_first_of_each_class_in_candidate_order():
    ids = [r.id() for r in S.candidates()]
    labels = {r: {"class": "accept_repaired"} for r in ids}
    for r in ids[1::4]:
        labels[r]["class"] = "accept_clean"
    for r in ids[2::4]:
        labels[r]["class"] = "decline"
    keep, short = S.select(labels)
    assert len(keep) == 20 and short == {}
    assert keep == sorted(keep, key=ids.index)
    assert [r for r in keep if labels[r]["class"] == "accept_clean"] == ids[1::4][:4]
    assert [r for r in keep if labels[r]["class"] == "decline"] == ids[2::4][:6]


def test_select_keeps_a_short_class_whole_and_states_the_shortfall():
    ids = [r.id() for r in S.candidates()]
    labels = {r: {"class": "decline"} for r in ids}
    labels[ids[5]]["class"] = labels[ids[9]]["class"] = "accept_repaired"
    keep, short = S.select(labels)
    assert len(keep) == 8 and short == {"accept_repaired": 8, "accept_clean": 4}
