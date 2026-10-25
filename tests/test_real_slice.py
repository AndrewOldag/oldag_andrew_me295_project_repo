"""Real-slice plumbing with a fake runner: no ssh, no tracker, no LLM call."""
import importlib.util
from pathlib import Path

import pytest

from agents import dispatcher as D
from agents.executors import Slice
from measure.real_runner import RealRunner, RealWindow
from measure.runner import FieldRunner, Rod

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("real_slice", ROOT / "scripts" / "real_slice.py")
RS = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RS)

ROW = {"id": "r1", "include": "yes", "usable_from_h": "4", "usable_to_h": "6", "step_s": "90.0",
       "condition": "mannitol", "experiment_type": "drought"}


class FakeRunner:
    """Stands in for RealRunner: a field-level rod record for any window; can fail the first job."""
    form = "fake"

    def __init__(self, fail_first=False):
        self.field, self.calls, self.fail_first = FieldRunner(), [], fail_first

    def initial_settings(self, w):
        return self.field.initial_settings(Rod())

    def measure(self, w, settings):
        self.calls.append((w.id(), settings.tag()))
        if self.fail_first and len(self.calls) == 1:
            raise RuntimeError("host busy")
        m = self.field.measure(Rod(), settings)
        m.moved = None                                # as for real movies
        return m

    def host_state(self):
        return {"cores": 14, "load1": 0.1, "own_jobs": 0, "free_gb": 30.0}


def test_window_id():
    assert RealWindow("0708_m12", 4.0, 6.0).id() == "0708_m12__w4-6"


def test_inline_queue_runs_job_and_engine_collects():
    runner, seen = FakeRunner(), []
    q = RS.InlineQueue(runner)
    e = D.Engine(q, D.load_config(), rows=[ROW], budget={"core_hours": 0.0, "usd": 0.0, "approved": False},
                 collector=lambda t: seen.append(t.id) or {"ok": True})
    out = D.run_script_batch(e, poll_minutes=15, round_limit=5)
    assert out["status"] == "finish" and out["states"] == {"collected": 1} and seen == ["r1__w4"]
    assert runner.calls[0][0] == "r1__w4-6"
    assert e.max_lab_workers() == 1                   # 14 cores: one eighth rounds down to 1


def test_failed_job_is_retried():
    runner = FakeRunner(fail_first=True)
    e = D.Engine(RS.InlineQueue(runner), D.load_config(), rows=[ROW],
                 budget={"core_hours": 0.0, "usd": 0.0, "approved": False})
    out = D.run_script_batch(e, poll_minutes=15, round_limit=5)
    assert out["retries"] == 1 and out["states"] == {"collected": 1}


def test_cluster_backend_refused_by_inline_queue():
    q = RS.InlineQueue(FakeRunner())
    t = D.make_tasks(ROW, D.load_config())[0]
    with pytest.raises(RuntimeError, match="no cluster job"):
        q.start(t, "cluster")


def test_slice_on_real_style_measurement_has_no_rigid_check():
    sl = Slice(FakeRunner(), RealWindow("r1", 4, 6))
    rigid = next(c for c in sl.checks if c.check == "rigid_invariance")
    assert rigid.passed is None and "no rigidly moved run" in rigid.detail
    s = RS.summarize(sl, RS.Accepted())
    assert s["outcome"]["status"] == "accept" and s["remedies"] == []


def test_real_runner_reads_config(tmp_path):
    cfg = tmp_path / "r.yaml"
    cfg.write_text("host: h\nwork_dir: /w\ncode_dir: /c\ntracker_code: /t\npython: /p\n"
                   "windows:\n  r1__w4-6:\n    imgdir: /d.imgdir\n    midline: /m.npz\n")
    r = RealRunner(cfg, cache=tmp_path / "cache")
    assert r.min_free_gb == 21 and r.windows["r1__w4-6"]["midline"] == "/m.npz"
    assert r.initial_settings(RealWindow("r1", 4, 6)).tag() == "st1"


def test_moved_copy_warp_matches_point_transform():
    pytest.importorskip("cv2")                         # tracker environment only (envs/qb.yml)
    spec2 = importlib.util.spec_from_file_location("real_moved", ROOT / "scripts" / "remote" / "real_moved.py")
    RM = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(RM)
    import numpy as np
    img = np.zeros((300, 500), np.float32)
    p = np.array([120.0, 340.0])                       # (row, col)
    img[int(p[0]) - 2:int(p[0]) + 3, int(p[1]) - 2:int(p[1]) + 3] = 1000.0
    about, t = np.array([150.0, 250.0]), 3600.0         # 1 h: 4 deg and (20, 12) px
    out = RM.warp(img, t, about)
    rr, cc = np.nonzero(out > 500)
    q = RM.move_points(p[None], t, about)[0]
    assert abs(rr.mean() - q[0]) < 0.6 and abs(cc.mean() - q[1]) < 0.6
    assert np.allclose(RM.move_points(p[None], 0.0, about)[0], p)


def test_whole_pixel_moved_copy(tmp_path, monkeypatch):
    import shutil
    import types
    import numpy as np
    spec3 = importlib.util.spec_from_file_location("real_moved_wp", ROOT / "scripts" / "remote" / "real_moved.py")
    RM = importlib.util.module_from_spec(spec3)
    spec3.loader.exec_module(RM)
    monkeypatch.setattr(RM.os, "symlink", lambda s, d: shutil.copy(s, d))   # links need privileges on Windows
    src = tmp_path / "x.imgdir"
    src.mkdir()
    rng = np.random.default_rng(0)
    frames = [rng.integers(0, 4000, (1, 60, 80)).astype(np.uint16) for _ in range(3)]
    for k, f in enumerate(frames):
        np.save(src / f"ImageData_Ch0_TP{k:07d}.npy", f)
    (src / "ElapsedTimes.yaml").write_text("theElapsedTimes: [3, 0, 900000, 1800000]\n")
    m = {"midline_image": np.tile(np.array([[30.0, 50.0], [30.0, 20.0]]), (3, 1, 1)), "mask0": np.ones((60, 80), bool)}
    np.savez(tmp_path / "m.npz", **m)
    a = types.SimpleNamespace(out_imgdir=str(tmp_path / "mv.imgdir"), out_midline=str(tmp_path / "mv.npz"),
                              out_ref_imgdir=str(tmp_path / "ref.imgdir"), out_ref_midline=str(tmp_path / "ref.npz"),
                              shift_scale=1.0, pad=False)
    tw = np.array([0.0, 900.0, 1800.0])                # shifts round((5, 3) px per 900 s): (0,0), (5,3), (10,6)
    RM.whole_pixel(src, np.load(tmp_path / "m.npz"), np.arange(3), tw, a)
    ref = [np.load(tmp_path / "ref.imgdir" / f"ImageData_Ch0_TP{k:07d}.npy")[0] for k in range(3)]
    mov = [np.load(tmp_path / "mv.imgdir" / f"ImageData_Ch0_TP{k:07d}.npy")[0] for k in range(3)]
    assert ref[0].shape == mov[2].shape == (50, 74)    # cropped by the largest shift (10, 6)
    for k, (dr, dc) in enumerate([(0, 0), (5, 3), (10, 6)]):
        assert np.array_equal(ref[k], frames[k][0, 10:, 6:])
        assert np.array_equal(mov[k][dr:, dc:], ref[k][:50 - dr, :74 - dc])   # content moved by (dr, dc), exactly
    rm, mm = np.load(tmp_path / "ref.npz"), np.load(tmp_path / "mv.npz")
    assert np.allclose(rm["midline_image"][2, 0], [20.0, 44.0]) and np.allclose(mm["midline_image"][2, 0], [30.0, 50.0])
    assert rm["mask0"].shape == (50, 74)
    # a second midline for the same window reuses the copies (inbox item 22): frames untouched, new midline files
    stamp = (tmp_path / "mv.imgdir" / "ImageData_Ch0_TP0000002.npy").stat().st_mtime_ns
    np.savez(tmp_path / "m2.npz", **dict(m, midline_image=m["midline_image"] + 1.0))
    a2 = types.SimpleNamespace(**dict(vars(a), out_midline=str(tmp_path / "mv2.npz"),
                                      out_ref_midline=str(tmp_path / "ref2.npz")))
    RM.whole_pixel(src, np.load(tmp_path / "m2.npz"), np.arange(3), tw, a2)
    assert (tmp_path / "mv.imgdir" / "ImageData_Ch0_TP0000002.npy").stat().st_mtime_ns == stamp
    assert np.allclose(np.load(tmp_path / "mv2.npz")["midline_image"][2, 0], [31.0, 51.0])
    assert np.allclose(np.load(tmp_path / "mv.npz")["midline_image"][2, 0], [30.0, 50.0])


def test_parse_window():
    assert RS.parse_window("0711_c1:4-6") == ("0711_c1", 4.0, 6.0)
    assert RS.parse_window("0721_m10:4.5-6.5") == ("0721_m10", 4.5, 6.5)


def test_several_windows_of_one_root_get_one_task_each():
    """Inbox item 37: a root with 3 windows gives 3 dispatcher rows and 3 tasks, each mapped back to its root."""
    cfg = D.load_config()
    m = {r["id"]: r for r in D.manifest_rows()}
    rows = [dict(m["0711_c2"], id=f"0711_c2~{a:g}-{b:g}", usable_from_h=str(a), usable_to_h=str(b))
            for a, b in [(4, 6), (11, 13), (17, 19)]]
    tasks = [t for r in rows for t in D.make_tasks(r, cfg)]
    assert [(t.from_h, t.to_h) for t in tasks] == [(4, 6), (11, 13), (17, 19)]
    assert {RS.root_of(t.root_id) for t in tasks} == {"0711_c2"} and RS.root_of("0711_c2") == "0711_c2"
    assert RealWindow(RS.root_of(tasks[1].root_id), tasks[1].from_h, tasks[1].to_h).id() == "0711_c2__w11-13"


def test_midline_path_default_and_cached_run_needs_no_host(tmp_path, monkeypatch):
    cfg = tmp_path / "r.yaml"
    cfg.write_text("host: h\nwork_dir: /w\ncode_dir: /c\ntracker_code: /t\npython: /p\n"
                   "windows:\n  r1__w4-6:\n    imgdir: /d.imgdir\n  r2__w4-6:\n    imgdir: /e.imgdir\n"
                   "    midline: /m.npz\n")
    r = RealRunner(cfg, cache=tmp_path / "cache")
    w, st = RealWindow("r1", 4, 6), r.initial_settings(RealWindow("r1", 4, 6))
    assert r.midline_path(w) == "/w/midline/r1__w4-6_netmid.npz"
    assert r.midline_path(RealWindow("r2", 4, 6)) == "/m.npz"
    assert r.cache_path(w, st, "ref").name == "r1__w4-6_wp_ref__st1__L1000.npz"
    calls = []
    monkeypatch.setattr(r, "_ssh", lambda cmd, stdin=None: calls.append(cmd) or b"")
    monkeypatch.setattr("measure.real_runner.from_tracker_npz", lambda path, root_id: (path.name, root_id))
    for k in ("ref", "moved"):
        r.cache_path(w, st, k).write_bytes(b"")
    m = r.measure(w, st)
    assert calls == [] and m.record == ("r1__w4-6_wp_ref__st1__L1000.npz", "r1__w4-6")


def test_job_count_pattern_does_not_match_its_own_command():
    import re
    from measure.real_runner import COUNT_PATTERN, JOB_PATTERN
    rx = re.compile(COUNT_PATTERN)
    assert rx.search("python scripts/remote/qb_track.py --imgdir x") and rx.search("python batch_midlines.py y")
    assert rx.search("python sweep.py run --cache z")
    assert not rx.search(f"bash -c ps -u 1 -o args= | grep -cE '{COUNT_PATTERN}'")
    assert set(JOB_PATTERN.split("|")) == {p.replace("[", "").replace("]", "") for p in COUNT_PATTERN.split("|")}


def test_condition_in_real_view_only():
    from audit.view import batch_table, batch_view
    sl = Slice(FakeRunner(), RealWindow("r1", 4, 6))
    plain = RS.summarize(sl, RS.Accepted())
    real = dict(plain, condition="control")
    rec = sl.current.record
    views, stats, _ = batch_view([plain, real], [rec, rec], key="k")
    assert sorted("condition" in v for v in views) == [False, True]
    rows = batch_table(views, stats)["runs"]
    assert sorted(r.get("condition", "") for r in rows) == ["", "control"]


def test_midline_tag_in_every_name_and_weights_passed(tmp_path, monkeypatch):
    cfg = tmp_path / "r.yaml"
    cfg.write_text("host: h\nwork_dir: /w\ncode_dir: /c\ntracker_code: /t\npython: /p\n"
                   "midline_weights: /x/net2_midline_ft2.pt\nmidline_tag: ft2\n"
                   "windows:\n  r1__w4-6:\n    imgdir: /d.imgdir\n")
    r = RealRunner(cfg, cache=tmp_path / "cache")
    w, st = RealWindow("r1", 4, 6), r.initial_settings(RealWindow("r1", 4, 6))
    assert r.midline_path(w) == "/w/midline/r1__w4-6_ft2_netmid.npz"
    assert r.copy_paths(w, "moved") == {"imgdir": "/w/moved/r1__w4-6_wp_moved.imgdir",
                                        "midline": "/w/moved/r1__w4-6_ft2_wp_moved_midline.npz"}
    assert r.cache_path(w, st, "ref").name == "r1__w4-6_ft2_wp_ref__st1__L1000.npz"
    calls = []

    def ssh(cmd, stdin=None):
        calls.append(cmd)
        if cmd.startswith("test -f"):
            return b"no\n"
        if "batch_midlines" in cmd:
            return b"1\n2\n"
        if "net_to_midline" in cmd:
            return b'{"frames": 80}\n'
        if "frames" in cmd:
            return b"[10, 89]\n"
        return b""
    monkeypatch.setattr(r, "_ssh", ssh)
    monkeypatch.setattr(r, "check_host", lambda: {"load1": 0.1, "free_gb": 900.0})
    monkeypatch.setattr(r, "host_state", lambda: {"load1": 0.1, "free_gb": 900.0})
    r.ensure_midline(w)
    net = next(c for c in calls if "batch_midlines" in c)
    assert "--midline-weights /x/net2_midline_ft2.pt" in net and "/w/midline/r1__w4-6_ft2_bm" in net
    assert r.log[-1]["weights"] == "net2_midline_ft2.pt"


def test_runner_set_routes_each_window_to_its_config(tmp_path):
    from measure.real_runner import RunnerSet
    base = "code_dir: /c\ntracker_code: /t\npython: /p\nmidline_tag: ft2\n"
    (tmp_path / "ws.yaml").write_text(f"host: ws\nwork_dir: /ws\n{base}windows:\n  a__w4-6:\n    imgdir: /a\n")
    (tmp_path / "lab.yaml").write_text(f"host: lab\nwork_dir: /lab\n{base}windows:\n  b__w4-6:\n    imgdir: /b\n")
    rs = RunnerSet([tmp_path / "ws.yaml", tmp_path / "lab.yaml"], cache=tmp_path / "cache")
    assert rs.runner_for(RealWindow("a", 4, 6)).host == "ws" and rs.runner_for(RealWindow("b", 4, 6)).host == "lab"
    with pytest.raises(KeyError):
        rs.runner_for(RealWindow("c", 4, 6))
    rs.runners[1].log.append({"track": "x"})
    assert rs.log == [{"track": "x", "host_config": 1}]
    assert isinstance(RS.make_runner([str(tmp_path / "ws.yaml")]), RealRunner)


def test_wait_vm_memory(tmp_path, monkeypatch):
    import measure.real_runner as RR
    cfg = tmp_path / "r.yaml"
    cfg.write_text("host: h\nwork_dir: /w\ncode_dir: /c\ntracker_code: /t\npython: /p\nwindows: {}\n")
    r = RealRunner(cfg, cache=tmp_path / "cache")
    free = iter([0.5, 1.0, 2.0])
    monkeypatch.setattr(RR, "vm_free_gb", lambda: next(free))
    monkeypatch.setattr(RR.time, "sleep", lambda s: None)
    assert r.wait_vm_memory() == 2.0
