"""Limits for the shared tracker machine in scripts/synth/sweep.py (decisions, 2026-10-11)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "synth"))
import sweep  # noqa: E402


def test_workers_at_most_four_and_one_eighth_of_cores(monkeypatch):
    for n, want in ((64, 4), (32, 4), (24, 3), (16, 2), (8, 1), (4, 1)):
        monkeypatch.setattr(sweep, "cores", lambda n=n: n)
        assert sweep.max_workers(8) == want
        assert sweep.max_workers(1) == 1


def test_single_thread_env(monkeypatch):
    for v in sweep.THREAD_VARS:
        monkeypatch.setenv(v, "8")
    sweep.single_thread_env()
    assert all(os.environ[v] == "1" for v in sweep.THREAD_VARS)
    assert os.environ["CUDA_VISIBLE_DEVICES"] == ""


def test_tasks_carry_moved_ids(tmp_path):
    plan = {"rods": [{"id": "growth_zone_clean_s0", "options": ["--case", "growth_zone"],
                      "runs": [{"tag": "st1", "args": ["--stride", "1"]}, {"tag": "st1_cpl", "args": ["--couple"]}]}]}
    t = sweep.tasks_of(plan, tmp_path, tmp_path)
    assert [x["rid"] for x in t] == ["growth_zone_clean_s0"] * 2 + ["growth_zone_clean_s0_moved"] * 2
    assert t[2]["options"][-1] == "--moved"


def _task(tmp_path):
    (tmp_path / "rods").mkdir(exist_ok=True)
    (tmp_path / "tracks").mkdir(exist_ok=True)
    return {"rid": "r_s0", "options": [], "tag": "st1", "args": [], "rods": str(tmp_path / "rods"),
            "tracks": str(tmp_path / "tracks")}


def test_output_done_only_with_marker(tmp_path):
    t = _task(tmp_path)
    out = tmp_path / "tracks" / "r_s0__st1.npz"
    out.write_bytes(b"partial")
    rec = sweep.run_one(t)                       # a stopped run's file: left in place, reported, not re-run
    assert rec["ok"] is False and rec["partial"] and out.read_bytes() == b"partial"
    (tmp_path / "tracks" / "r_s0__st1.npz.ok").write_bytes(b"")
    assert sweep.run_one(t) == {"id": "r_s0", "tag": "st1", "cached": True}


def test_rod_done(tmp_path):
    rods = tmp_path / "rods"
    rods.mkdir()
    (rods / "a.imgdir").mkdir()
    assert not sweep.rod_done(rods, "a")
    (rods / "a.ok").write_bytes(b"")
    assert sweep.rod_done(rods, "a")
    (rods / "b_truth.npz").write_bytes(b"")      # rendered before the marker existed
    assert sweep.rod_done(rods, "b")
