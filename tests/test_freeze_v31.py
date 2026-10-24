"""Freeze v3.1 (docs/specs/2026-10-24_freeze-v3.1.md): label states at the new sizes, sizing plan limits."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "synth"))
import scored_v3 as v3  # noqa: E402
import scored_v31 as v31  # noqa: E402
from measure.remedies import TrackSettings, apply_remedy  # noqa: E402
from measure.runner import Rod  # noqa: E402


def strides(size):
    return [st.stride for _, st in v31.label_states(Rod(v3.GZ, "displacement_exceeds_patch", 10, size=size))]


def test_stride_states_follow_the_remedy():
    assert strides("2x2") == [2, 1]
    assert strides("2x3") == [3, 1]
    assert strides("2x4") == [4, 2, 1]
    assert strides("2x6") == [6, 3, 1]          # the v3 states
    st, seq = TrackSettings(stride=4), []
    while st.stride > 1:
        st, _ = apply_remedy(st, "change_frame_stride", "half", 14)
        seq.append(st.stride)
    assert seq == strides("2x4")[1:]


def test_other_faults_keep_v3_states():
    rod = Rod(v3.GZ, "width_change", 10)
    assert [s for s, _ in v31.label_states(rod)] == [s for s, _ in v3.label_states(rod)]


def test_sizes_within_spec():
    assert set(v31.SIZES) == {"rigid_drift", "width_change", "bad_stage_correction", "stage_log_missing",
                              "displacement_exceeds_patch"}
    assert all(1 <= len(z) <= 6 for z in v31.SIZES.values())
    assert v31.SIZES["rigid_drift"][0] == "0.5"              # the v3 size
    assert v31.SIZES["bad_stage_correction"][0] == v3.HELDOUT["bad_stage_correction"]
    assert v31.SIZES["stage_log_missing"] == [v3.HELDOUT["stage_log_missing"]]
    assert not set(v31.SCORING_SEEDS) & set(v3.seeds("scoring_seeds") + v3.seeds("sizing_seeds")
                                            + v3.seeds("basis_seeds"))
