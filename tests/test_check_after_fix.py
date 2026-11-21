"""scripts/check_after_fix.py: batch-2 rows kept, one row appended per arange window, rerun writes the same file."""
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_after_fix  # noqa: E402

COLS = ["window", "root", "condition", "from_h", "to_h", "status", "outcome", "closure_px_per_h",
        "rigid_invariance_pct_per_h", "plane_sections_pct_per_h", "moved_copy", "n_frames",
        "tracked_length_reached_px", "frame0_midline_px", "flag", "error"]


def setup(tmp_path, monkeypatch):
    batch, tracks, records = tmp_path / "batch", tmp_path / "tracks", tmp_path / "rec"
    (batch / "audit").mkdir(parents=True)
    tracks.mkdir()
    (records / "windows").mkdir(parents=True)
    rows = [dict.fromkeys(COLS, "") | {"window": "r1__w0-2", "root": "r1", "condition": "control",
                                        "status": "measured", "outcome": "pass"},
            dict.fromkeys(COLS, "") | {"window": "r1__w2-4", "root": "r1", "condition": "control",
                                        "status": "failed", "error": "ValueError: arange: cannot compute length"}]
    with open(batch / "windows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    (tracks / "r1__w2-4_ft2__st1__L1000.npz").write_bytes(b"track")
    with open(batch / "audit" / "outputs.csv", "w", newline="") as f:
        f.write("root,window,kind,track_md5\n")
        f.write(f"r1,r1__w2-4,track,{hashlib.md5(b'track').hexdigest()}\n")
    rec = {"window": "r1__w2-4", "root": "r1", "window_h": [2.0, 4.0], "status": "measured",
           "outcome": "not computable", "values": {"closure": None}, "moved_copy": False, "n_frames": 80, "base": {}}
    (records / "windows" / "r1__w2-4.json").write_text(json.dumps(rec))
    monkeypatch.setattr(check_after_fix, "BATCH2", batch)
    monkeypatch.setattr(sys, "argv", ["x", "--tracks", str(tracks), "--records", str(records)])
    return batch


def test_rows_kept_and_appended_and_rerun_same(tmp_path, monkeypatch):
    batch = setup(tmp_path, monkeypatch)
    check_after_fix.main()
    first = (batch / "windows.csv").read_text()
    rows = list(csv.DictReader(open(batch / "windows.csv", newline="")))
    assert [r["window"] for r in rows] == ["r1__w0-2", "r1__w2-4", "r1__w2-4"]
    assert [r["checked_after_fix"] for r in rows] == ["", "", "yes"]
    assert rows[1]["status"] == "failed" and rows[2]["outcome"] == "not computable"
    check_after_fix.main()
    assert (batch / "windows.csv").read_text() == first
