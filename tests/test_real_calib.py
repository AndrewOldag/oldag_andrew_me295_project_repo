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


def test_extension_windows():
    first = {w.id() for w in real_calib.WINDOWS} | {"0714_c13__w7-9", "0714_c13__w15-17"}
    ext = [w.id() for w in real_calib.EXT_RESCREEN + real_calib.EXT_NEW]
    assert len(ext) == 30 and len(set(ext)) == 30
    assert len(first | set(ext)) == 42                        # 14 roots x 3 windows
    assert {w.id() for w in real_calib.EXT_RESCREEN} <= first
    section_c = {"0711_c2", "0708_c5", "0714_c10", "0721_c1", "0711_c4"}
    assert not {w.root_id for w in real_calib.EXT_NEW + real_calib.EXT_FALLBACK} & section_c
