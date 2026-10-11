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
