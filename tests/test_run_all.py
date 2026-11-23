"""scripts/run_all.py: pause on a cache miss, restart, cap and auditor readiness. No host or LLM is called."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_all as RA  # noqa: E402
from measure.real_runner import RealWindow  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402


def runner(tmp_path, moved=()):
    cfg = {"host": "h", "work_dir": "/w", "code_dir": "/c", "tracker_code": "/t", "python": "py",
           "midline_tag": "ft2", "windows": {}}
    return RA.RunRunner(cfg, moved, cache=tmp_path / "cache")


def test_paused_passes_executor_guard():
    assert issubclass(RA.Paused, BaseException) and not issubclass(RA.Paused, Exception)


def test_measure_pauses_on_cache_miss(tmp_path):
    r = runner(tmp_path, moved=["a__w10-12"])
    w = RealWindow("a", 10, 12)
    s = TrackSettings(stride=2, width_free=True)
    with pytest.raises(RA.Paused) as e:
        r.measure(w, s)
    assert e.value.kinds == ["ref", "moved"] and e.value.settings == TrackSettings(stride=2)
    assert "paused: needs st2" in str(e.value)
    r.cache_path(w, s, "ref").write_bytes(b"x")
    assert r.missing(w, s) == ["moved"]
    assert r.kinds(RealWindow("a", 0, 2)) == ["window"]


def task(root, a, b):
    return SimpleNamespace(root_id=root, from_h=a, to_h=b)


def make_run(tmp_path, recs, **kw):
    run = RA.Run(runner(tmp_path), tmp_path / "out", rows={}, free_gb=lambda: 99, log=lambda *x: None, **kw)
    run.windows_of = {"a": ["a__w0-2", "a__w2-4"], "b": ["b__w0-2"]}
    calls = []

    def window(w):
        calls.append(w.id())
        return dict(recs[w.id()], window=w.id(), root=w.root_id)
    run.window = window
    return run, calls


def test_collector_records_pauses_and_restarts(tmp_path):
    final = {"status": "final", "outcome": {"status": "accept"}}
    paused = {"status": "paused", "needs_settings": TrackSettings(stride=2).to_dict(), "needs_kinds": ["window"]}
    run, calls = make_run(tmp_path, {"a__w0-2": final, "a__w2-4": paused, "b__w0-2": final})
    for t in (task("a", 0, 2), task("a", 2, 4), task("b", 0, 2)):
        run.collector(t)
    lines = (tmp_path / "out" / "paused.jsonl").read_text().splitlines()
    assert [json.loads(l)["window"] for l in lines] == ["a__w2-4"]
    assert [r for r, _ in run.audit_ready()] == ["b"]                       # a has a paused window
    assert [r for r, _ in run.audit_ready(final_now=True)] == ["a", "b"]
    run2, calls2 = make_run(tmp_path, {"a__w0-2": final, "a__w2-4": final, "b__w0-2": final})
    for t in (task("a", 0, 2), task("a", 2, 4), task("b", 0, 2)):
        run2.collector(t)
    assert calls2 == ["a__w2-4"]                                            # final windows skipped; paused rerun


def test_stop_at_and_stoprun(tmp_path):
    import datetime
    final = {"status": "final", "outcome": {"status": "accept"}}
    t = datetime.datetime(2026, 11, 21, 20, 0)
    run, calls = make_run(tmp_path, {"a__w0-2": final}, stop_at=t, clock=lambda: t)
    run.collector(task("a", 0, 2))
    assert calls == [] and run.stopping.startswith("--stop-at")
    run2, _ = make_run(tmp_path, {})

    def boom(w):
        raise RA.StopRun("cap")
    run2.window = boom
    run2.collector(task("a", 0, 2))
    assert run2.stopping == "cap" and not (tmp_path / "out" / "windows" / "a__w0-2.json").exists()


def test_count_calls_and_limit(tmp_path):
    p = tmp_path / "x_trace.jsonl"
    p.write_text("\n".join([json.dumps({"call": {"text": "ok"}}), json.dumps({"step": 1}),
                            json.dumps({"call": {"text": "You've hit your session limit"}})]))
    assert RA.count_calls([p]) == (2, True)


def test_auditor_skips_root_without_accepted(tmp_path):
    decl = {"status": "final", "outcome": {"status": "decline"}}
    run, _ = make_run(tmp_path, {"a__w0-2": decl, "a__w2-4": decl, "b__w0-2": decl})
    for t in (task("a", 0, 2), task("a", 2, 4), task("b", 0, 2)):
        run.collector(t)
    seen = []
    run._auditor = lambda *a: seen.append(a) or {"status": "report"}
    assert run.audit() == 2 and seen == []
    rec = json.loads((tmp_path / "out" / "audit" / "a" / "audit.json").read_text())
    assert rec["status"] == "not_called" and rec["windows"] == ["a__w0-2", "a__w2-4"]


def test_remedy_hold_pauses_every_failing_window(tmp_path, monkeypatch):
    import retrack_queue as RQ
    r = runner(tmp_path)
    run = RA.Run(r, tmp_path / "out", rows={}, free_gb=lambda: 99, log=lambda *x: None)
    w = RealWindow("a", 0, 2)
    singles = [TrackSettings(stride=2), TrackSettings(midline_smooth="light")]
    monkeypatch.setattr(RQ, "single_remedies", lambda *a: [("x", None, s) for s in singles])
    monkeypatch.setattr(RA, "REMEDY_HOLD", True)
    r.cache_path(w, singles[1], "window").write_bytes(b"x")        # cached or not: held
    sl = SimpleNamespace(runs=[(TrackSettings(), SimpleNamespace(record=None), [], "")], base_disk_radius=15)
    with pytest.raises(RA.Paused) as e:
        run.pre_pause(w, sl)
    assert "remedy hold" in str(e.value)
    lines = [json.loads(l) for l in (tmp_path / "out" / "paused.jsonl").read_text().splitlines()]
    assert [l["settings"]["stride"] for l in lines] == [2]          # only the missing one is queued


def test_register_v2_not_held(tmp_path, monkeypatch):
    r = runner(tmp_path)
    w = RealWindow("a", 0, 2)
    v2 = TrackSettings(register=True, register_from_px=900, register_version=2, register_max_shift_px=50)
    r.cache_path(w, v2, "window").write_bytes(b"x")
    monkeypatch.setattr(RA, "REGISTER_HOLD", True)
    assert r.missing(w, v2) == []


def test_pre_pause_until_every_single_remedy_cached(tmp_path, monkeypatch):
    import retrack_queue as RQ
    monkeypatch.setattr(RA, "REMEDY_HOLD", False)
    r = runner(tmp_path)
    run = RA.Run(r, tmp_path / "out", rows={}, free_gb=lambda: 99, log=lambda *x: None)
    w = RealWindow("a", 0, 2)
    singles = [TrackSettings(stride=2), TrackSettings(midline_smooth="light")]
    monkeypatch.setattr(RQ, "single_remedies", lambda *a: [("x", None, s) for s in singles])
    sl = SimpleNamespace(runs=[(TrackSettings(), SimpleNamespace(record=None), [], "")], base_disk_radius=15)
    with pytest.raises(RA.Paused) as e:
        run.pre_pause(w, sl)
    assert e.value.settings == singles[0]
    lines = [json.loads(l) for l in (tmp_path / "out" / "paused.jsonl").read_text().splitlines()]
    assert [l["settings"]["midline_smooth"] for l in lines] == ["light"]
    r.cache_path(w, singles[1], "window").write_bytes(b"x")        # one of two cached: still paused
    with pytest.raises(RA.Paused) as e:
        run.pre_pause(w, sl)
    assert e.value.settings == singles[0]
    r.cache_path(w, singles[0], "window").write_bytes(b"x")        # every single cached: the agent runs
    run.pre_pause(w, sl)


def test_register_hold_counts_registered_tracks_as_missing(tmp_path, monkeypatch):
    r = runner(tmp_path)
    w = RealWindow("a", 0, 2)
    s = TrackSettings(register=True, register_from_px=900)
    r.cache_path(w, s, "window").write_bytes(b"x")
    monkeypatch.setattr(RA, "REGISTER_HOLD", True)
    assert r.missing(w, s) == ["window"]
    with pytest.raises(RA.Paused):
        r.measure(w, s)
    monkeypatch.setattr(RA, "REGISTER_HOLD", False)
    assert r.missing(w, s) == []


@pytest.mark.parametrize("argv, cap", [([], 900), (["--llm-cap", "1300"], 1300)])
def test_llm_cap_option(monkeypatch, argv, cap):
    seen = {}

    class FakeRun:
        def __init__(self, *a, **k):
            seen.update(k)
            self.windows_of, self.stopping = {}, None

        def audit(self, final_now=False):
            return 0
    monkeypatch.setattr(RA, "Run", FakeRun)
    monkeypatch.setattr(RA, "batch_rows", lambda: {})
    monkeypatch.setattr(RA, "make_runner", lambda config, rows: None)
    monkeypatch.setattr(RA, "window_list", lambda roots=None: [])
    monkeypatch.setitem(sys.modules, "agents.launcher", SimpleNamespace(Launcher=lambda: None))
    assert RA.main(["audit", "--out", "x"] + argv) == 0 and seen["cap"] == cap


def test_roots_limit_the_dispatcher():
    """--roots (B5 demo): the dispatcher lists only the windows of the given roots; without it every root."""
    some = RA.window_list({"0708_c4"})
    assert some and {w.root_id for w in some} == {"0708_c4"}
    assert len(RA.window_list()) > len(some)


def test_tree_reruns_every_diagnostician_window(tmp_path, monkeypatch):
    """The tree runs on every window the diagnostician decided, c026-reached ones included (register v1, no gate)."""
    from dataclasses import dataclass

    import agents.executors as E

    @dataclass
    class Outcome:
        status: str
    run = tmp_path / "run" / "windows"
    run.mkdir(parents=True)
    for wid, by in (("0711_c5__w6-8", "diagnostician"), ("0708_c4__w4-6", "rule")):
        (run / f"{wid}.json").write_text(json.dumps({"window": wid, "status": "final", "decided_by": by}))

    class FakeSlice:
        def __init__(self, runner, w, label=""):
            self.runs, self.checks = [(SimpleNamespace(tag=lambda: "st1"), None, {})], {}
    monkeypatch.setattr(E, "Slice", FakeSlice)
    monkeypatch.setattr(RA, "wait_memory", lambda: None)
    monkeypatch.setattr(RA, "remedy_steps", lambda sl: [])
    monkeypatch.setattr(RA, "closure", lambda c: None)
    out = tmp_path / "tree"
    RA.run_tree_all(None, tmp_path / "run", out, log=lambda m: None,
                    tree=lambda sl, step_limit, trace_path: Outcome("decline"))
    assert sorted(p.stem for p in (out / "windows").glob("*.json")) == ["0711_c5__w6-8"]
    assert json.loads((out / "windows" / "0711_c5__w6-8.json").read_text())["outcome"]["status"] == "decline"


def test_report_error_line_has_no_folder():
    import run_all_report as R
    err = 'Traceback\n  File "/a/b/c.py", line 1\nFileNotFoundError: No such file: \'/x/y/StagePositionData.yaml\'\n'
    assert R._last_line(err) == "FileNotFoundError: No such file: 'StagePositionData.yaml'"
