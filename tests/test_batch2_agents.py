"""Task c026 adapter: the remedy tree on real windows, run records, stops, staged-root clearing. No ssh, no LLM."""
import importlib.util
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from measure.cluster_compute import ClusterCompute, JobFailed
from measure.real_runner import RealWindow, _ledger_from
from measure.runner import FieldRunner, Rod

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("batch2_agents", ROOT / "scripts" / "batch2_agents.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


class RealStyleRunner:
    """A field-level rod record marked movie=real, with a world-tip drift that fails closure; a remedy in `fixes`
    removes it. `error` raises that exception on the first remedy run."""

    def __init__(self, fixes=None, error=None):
        self.field, self.fixes, self.error, self.calls = FieldRunner(), fixes, error, []

    def initial_settings(self, w):
        return self.field.initial_settings(Rod())

    def measure(self, w, settings):
        self.calls.append((w.id(), settings.tag()))
        if self.error and len(self.calls) > 1:
            raise self.error
        m = self.field.measure(Rod(), settings)
        rec = m.record
        rec.settings = dict(rec.settings, movie="real")
        fixed = self.fixes and getattr(settings, self.fixes[0]) == self.fixes[1]
        if not fixed:
            drift = np.linspace(0, 400, rec.n_frames)[:, None, None] * np.array([1.0, 0.0])
            rec = replace(rec, midline=rec.midline + drift, _fields=None)
            rec.settings = m.record.settings
        m.record, m.moved = rec, None
        return m


def windows(n=2):
    return [(RealWindow("r1", 2.0 * i, 2.0 * i + 2), 50.0) for i in range(n)]


def test_failing_windows_of_batch_2():
    ws = B.failing_windows()
    assert len(ws) == 84 and len({w.root_id for w, _ in ws}) == 50
    assert all(c > 19.0 for _, c in ws) and sum(w.from_h == 10 for w, _ in ws) == 3


def test_tree_on_real_window_declines_after_closure_list(tmp_path):
    runner = RealStyleRunner()
    status = B.run_tree_windows(runner, windows(1), tmp_path, free_gb=lambda: 99.0)
    rec = json.loads((tmp_path / "windows" / "r1__w0-2.json").read_text())
    assert status == "done" and rec["outcome"]["status"] == "decline"
    assert rec["initial_closure"]["passed"] is False
    assert all(not s["kept"] for s in rec["remedies"])           # each retrack rolled back
    # stride 1: halving skipped; enlarge 1.5x, 2x and smoothing tried (registration needs a profile band)
    assert [s["settings"] for s in rec["remedies"]][-1].endswith("mslight4")
    trace = [json.loads(x) for x in (tmp_path / "tree_trace.jsonl").read_text().splitlines()]
    assert trace[-1]["status"] == "task_end" and trace[-1]["agent"] == "remedy_tree"


def test_tree_on_real_window_accepts_after_kept_remedy(tmp_path):
    runner = RealStyleRunner(fixes=("disk_radius", 22))           # enlarge_patch 1.5x of the base 15 px
    B.run_tree_windows(runner, windows(1), tmp_path, free_gb=lambda: 99.0)
    rec = json.loads((tmp_path / "windows" / "r1__w0-2.json").read_text())
    assert rec["outcome"]["status"] == "accept" and rec["final_closure"]["passed"] is True
    kept = [s for s in rec["remedies"] if s["kept"]]
    assert len(kept) == 1 and kept[0]["closure_after"]["passed"] is True and kept[0]["settings"] == "st1_r22"


def test_window_error_recorded_and_run_resumes(tmp_path):
    runner = RealStyleRunner(error=JobFailed("track job: FAILED"))
    cleared = []
    B.run_tree_windows(runner, windows(2), tmp_path, free_gb=lambda: 99.0, clear=lambda r: cleared.append(r) or [])
    recs = {p.stem: json.loads(p.read_text()) for p in (tmp_path / "windows").glob("*.json")}
    assert {r["outcome"]["status"] for r in recs.values()} == {"error"} and "JobFailed" in recs["r1__w0-2"]["error"]
    assert cleared == ["r1"] and (tmp_path / "tree.done").exists()
    n = len(runner.calls)
    B.run_tree_windows(runner, windows(2), tmp_path, free_gb=lambda: 99.0)
    assert len(runner.calls) == n                                  # finished windows are skipped


def test_budget_stop_stops_the_run(tmp_path):
    class BudgetStop(RuntimeError):
        pass
    runner = RealStyleRunner(error=BudgetStop("ledger refused"))
    status = B.run_tree_windows(runner, windows(2), tmp_path, free_gb=lambda: 99.0)
    assert status.startswith("stopped: BudgetStop") and (tmp_path / "stopped").exists()
    assert not list((tmp_path / "windows").glob("*.json"))


def test_memory_wait_before_each_window(tmp_path):
    free, slept = iter([1.0, 5.0, 5.0]), []
    B.run_tree_windows(RealStyleRunner(fixes=("stride", 1)), windows(2), tmp_path, free_gb=lambda: next(free),
                       sleep=slept.append)
    assert slept == [60]


def test_ledger_spend_stop(monkeypatch):
    import subprocess

    class P:
        returncode, stderr = 0, ""
        stdout = "spent 7.240 + worst case 0.012 = 7.252 (cap 15.00) -> ok\n"
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: P())
    assert _ledger_from({"ledger": ["py", "l.py"], "spend_stop_usd": 12})("check", "d")[0] == 0
    P.stdout = "spent 11.990 + worst case 0.012 = 12.002 (cap 15.00) -> ok\n"
    rc, msg = _ledger_from({"ledger": ["py", "l.py"], "spend_stop_usd": 12})("check", "d")
    assert rc == 1 and "$12 stop" in msg
    assert _ledger_from({"ledger": ["py", "l.py"]})("check", "d")[0] == 0     # no stop key: unchanged


class FakeRelay:
    """Cluster and storage command stand-in: md5 listings and rm calls are recorded."""

    def __init__(self, cluster_md5, storage_md5, staged=("r0", "r1")):
        self.cluster_md5, self.storage_md5, self.staged, self.cmds = cluster_md5, storage_md5, staged, []
        self.link = self
        self.where = None

    def run(self, cmd, stdin=None, check=True):
        self.cmds.append(cmd)
        if "wc -l" in cmd:                         # file counts: storage 3, cluster copy 0
            return b"0" if "/cl/data" in cmd else b"3"
        if "du -sm" in cmd:
            return b"100"
        if "md5sum" in cmd:
            return (self.storage_md5 if "/storage" in cmd else self.cluster_md5).encode()
        if cmd.startswith("ls /cl/data"):
            return " ".join(f"{r}.imgdir" for r in self.staged).encode()
        if "rm -r" in cmd:
            return b"2026-11-12T16:00:00-08:00 4.1G"
        return b""

    def require_master(self):
        pass

    def push(self, src, dest):
        self.cmds.append(f"push {src} {dest}")


def cc(relay):
    return ClusterCompute(relay, {"work_dir": "/cl/work", "stage_dir": "/cl/data", "one_staged_root": True,
                                  "storage_work": "/storage/c026"}, ledger=lambda *a: (0, ""))


def test_clear_root_deletes_after_md5_match():
    r = FakeRelay("aa  ./r0__w0-2_ft2__st1_r22__L1000.npz\n", "aa  ./r0__w0-2_ft2__st1_r22__L1000.npz\n")
    out = cc(r).clear_root("r0", "/storage/c026", "test")
    assert [d["path_kind"] for d in out] == ["staged_root"] and out[0]["tracks_checked"] == 1
    assert any("rm -r /cl/data/r0.imgdir" in c and "DELETED.log" in c for c in r.cmds)


def test_clear_root_keeps_copy_when_storage_differs():
    r = FakeRelay("aa  ./r0__w0-2_ft2__st1_r22__L1000.npz\n", "bb  ./r0__w0-2_ft2__st1_r22__L1000.npz\n")
    with pytest.raises(JobFailed, match="not md5-equal"):
        cc(r).clear_root("r0", "/storage/c026", "test")
    assert not any("rm -r" in c for c in r.cmds)


def test_stage_root_clears_other_staged_roots_first():
    r = FakeRelay("", "", staged=("r0",))
    c = cc(r)
    cleared = []
    c.clear_root = lambda root, sw, why: cleared.append((root, sw)) or []
    with pytest.raises(JobFailed):                 # the fake copies nothing: file count check fails after clearing
        c.stage_root("r1", "/storage/movie.imgdir")
    assert cleared == [("r0", "/storage/c026")]


def test_groups_and_session_limit_detection(tmp_path):
    ids = B.groups(windows(25))
    assert [len(g) for g in ids] == [21, 4] and ids[0][0] == "r1:0-2"
    g = tmp_path / "g01"
    g.mkdir()
    (g / "diagnostician_trace.jsonl").write_text(
        json.dumps({"call": {"ok": True}}) + "\n" + json.dumps({"call": {"error": "You've hit your session limit"}})
        + "\n" + json.dumps({"status": "task_end"}) + "\n")
    assert B.trace_calls(g) == (2, True)


def test_runner_cache_from_config(tmp_path):
    from measure.real_runner import RealRunner
    cfg = {"host": "h", "work_dir": "/w", "code_dir": "/c", "tracker_code": "/t", "python": "py", "windows": {},
           "cache": "staging/test_c026_cache"}
    r = RealRunner(cfg)
    assert r.cache == ROOT / "staging" / "test_c026_cache" and r.cache.is_dir()
    r.cache.rmdir()


def test_report_masks_biology_and_runs_on_tree_records(tmp_path):
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import batch2_agents_report as R
    m = R.mask({"closure": 30.1, "centre_peak_regr_pct_per_h": 41.0,
                "text": "REGR peak 41.2 %/h at 350 um; growth zone length 900 um; closure 30.1 px/h"})
    assert m["centre_peak_regr_pct_per_h"] == "[masked]" and m["closure"] == 30.1
    assert "41.2" not in m["text"] and "900" not in m["text"] and "30.1" in m["text"]
    ws = windows(2)
    B.run_tree_windows(RealStyleRunner(fixes=("disk_radius", 22)), ws, tmp_path / "tree", free_gb=lambda: 99.0)
    R.main(tmp_path / "tree", tmp_path / "agents", tmp_path / "out", ws)
    rows = (tmp_path / "out" / "windows.csv").read_text().splitlines()
    assert len(rows) == 3 and ",accept," in rows[1] and "enlarge_patch 1.5x" in rows[1]
    assert "| remedy tree | 2 | 2 | 2 |" in (tmp_path / "out" / "tables.md").read_text()


def test_clear_root_compares_track_files_only():
    r = FakeRelay("aa  ./r0__w0-2_ft2__st1_r22__L1000.npz\n", "aa  ./r0__w0-2_ft2__st1_r22__L1000.npz\n")
    cc(r).clear_root("r0", "/storage/c026", "test")
    assert all("'r0__w*.npz'" in c for c in r.cmds if "md5sum" in c)


def test_stop_at_starts_no_window_after_the_time(tmp_path):
    import datetime as dt
    t = iter([dt.datetime(2026, 11, 14, 7, 0), dt.datetime(2026, 11, 14, 8, 1)])
    cleared = []
    status = B.run_tree_windows(RealStyleRunner(fixes=("stride", 1)), windows(3), tmp_path, free_gb=lambda: 99.0,
                                clear=lambda r: cleared.append(r) or [], stop_at=dt.datetime(2026, 11, 14, 8, 0),
                                now=lambda: next(t))
    assert status.startswith("stopped: --stop-at") and len(list((tmp_path / "windows").glob("*.json"))) == 1
    assert cleared == ["r1"] and not (tmp_path / "tree.done").exists()
