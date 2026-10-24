import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import real_calib  # noqa: E402


def test_ceil_2sf():
    assert real_calib.ceil_2sf(6.213) == 6.3
    assert real_calib.ceil_2sf(0.4471) == 0.45
    assert real_calib.ceil_2sf(20.0) == 20.0
    assert real_calib.ceil_2sf(7.13) == 7.2
    assert real_calib.ceil_2sf(123.4) == 130.0


def test_windows_match_proposal():
    ids = [w.id() for w in real_calib.WINDOWS]
    assert len(ids) == 16 and len({i[:4] for i in ids}) == 4
    assert "0711_c7__w15-17" in ids and "0708_c8__w7-9" in ids
