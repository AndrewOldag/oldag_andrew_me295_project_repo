"""Dispatcher tests on the fake queue with a scripted launcher. No LLM calls, no real jobs."""
import json

import pytest

from agents import dispatcher as D
from agents.launcher import CallResult

CFG = D.load_config()
ROWS = [
    {"id": "r1", "include": "yes", "usable_from_h": "0", "usable_to_h": "24.01", "step_s": "90.0",
     "condition": "control", "experiment_type": "drought"},
    {"id": "r2", "include": "yes", "usable_from_h": "0", "usable_to_h": "9.5", "step_s": "96.6",
     "condition": "mannitol", "experiment_type": "drought"},
    {"id": "r3", "include": "yes", "usable_from_h": "2", "usable_to_h": "4.05", "step_s": "103.7",
     "condition": "control then control", "experiment_type": "recovery"},
]
NO_BUDGET = {"core_hours": 0.0, "usd": 0.0, "approved": False}
BUDGET = {"core_hours": 5.0, "usd": 0.06, "approved": True}


def engine(queue=None, budget=NO_BUDGET, rows=ROWS, **kw):
    return D.Engine(queue or D.FakeQueue(), CFG, rows=rows, budget=budget, **kw)


class ScriptedLauncher:
    def __init__(self, outputs, step_limit=4):
        self.cfg = {"model": "m", "agents": {"dispatcher": {"effort": "low", "max_turns": 3,
                                                            "step_limit": step_limit}}}
        self.outputs, self.prompts = list(outputs), []

    def call(self, prompt, system, schema, effort, max_turns):
        self.prompts.append(prompt)
        o = self.outputs.pop(0) if self.outputs else {"action": "wait", "minutes": 60}
        return CallResult(ok=True, structured_output=dict(rationale="r", **o), models=["m"],
                          subtype="success", input_tokens=10, output_tokens=5, duration_ms=1)


# ── windows and manifest ─────────────────────────────────────────────────────

def test_windows_and_last_window_rule():
    assert D.windows(0, 24.01, 2.0, 1.0)[-1] == (22.0, 24.0)            # 0.01 h left over, dropped
    assert len(D.windows(0, 24.01, 2.0, 1.0)) == 12
    assert D.windows(0, 9.5, 2.0, 1.0)[-1] == (8.0, 9.5)          # 1.5 h kept
    assert D.windows(2, 4.05, 2.0, 1.0) == [(2, 4.0)]             # 0.05 h dropped


def test_only_include_yes_rows_and_usable_hours():
    rows = D.manifest_rows()
    assert rows and all(r["include"] == "yes" for r in rows)
    e = engine(rows=rows)
    e.split_root({"root_ids": [r["id"] for r in rows]})
    for t in e.tasks.values():
        r = e.rows[t.root_id]
        assert float(r["usable_from_h"]) <= t.from_h < t.to_h <= float(r["usable_to_h"]) + 1e-9


def test_unknown_root_refused():
    e = engine()
    with pytest.raises(ValueError, match="include-yes"):
        e.split_root({"root_ids": ["not_a_root"]})


# ── budget and cluster ───────────────────────────────────────────────────────

def test_cluster_refused_without_budget():
    e = engine()
    e.split_root({"root_ids": ["r3"]})
    r = e.submit({"root_ids": ["r3"], "backend": "cluster"})
    assert "refused" in r["error"] and e.stats["cluster_refused"] == 1
    assert not e.queue.jobs


def test_cluster_refused_over_budget_left():
    e = engine(budget={"core_hours": 0.5, "usd": 0.006, "approved": True})
    e.split_root({"root_ids": ["r1"]})                              # 12 windows, about 0.7 core-h
    assert "refused" in e.submit({"root_ids": ["r1"], "backend": "cluster"})["error"]
    e.split_root({"root_ids": ["r3"]})                              # 1 window, about 0.04 core-h
    assert e.submit({"root_ids": ["r3"], "backend": "cluster"})["submitted_windows"] == 1
    assert e.cluster_left_h() < 0.5


def test_budget_file_needs_andrew(tmp_path):
    cfg = dict(CFG, budget_file="b.yaml")
    assert D.load_budget(cfg, repo=tmp_path)["core_hours"] == 0
    (tmp_path / "b.yaml").write_text("core_hours: 10\nusd: 0.12\napproved_by: someone\n")
    assert D.load_budget(cfg, repo=tmp_path)["core_hours"] == 0
    (tmp_path / "b.yaml").write_text("core_hours: 10\nusd: 0.12\napproved_by: Andrew\ndate: 2026-10-23\n")
    assert D.load_budget(cfg, repo=tmp_path)["core_hours"] == 10


def test_no_budget_file_in_repo_means_zero():
    if not (D.REPO / CFG["budget_file"]).exists():
        assert D.load_budget(CFG) == NO_BUDGET


# ── shared-machine limits ────────────────────────────────────────────────────

def test_lab_worker_limit():
    e = engine()
    e.split_root({"root_ids": ["r1", "r2"]})
    e.submit({"root_ids": ["r1", "r2"], "backend": "lab_server"})
    assert e.lab_workers() == 4 and len(e.lab_queue) == len(e.tasks) - 4
    for _ in range(40):
        e.queue.advance(15); e.refresh()
        assert e.lab_workers() <= 4
    assert e.stats["lab_peak_workers"] == 4


def test_lab_worker_limit_one_eighth_of_cores():
    e = engine(D.FakeQueue(cores=16))
    e.split_root({"root_ids": ["r1"]})
    e.submit({"root_ids": ["r1"], "backend": "lab_server"})
    assert e.lab_workers() == 2


def test_load_rule_pauses_and_resumes():
    load = {"v": 30.0}                                             # above 3/4 of 32 cores
    q = D.FakeQueue(load=lambda t: load["v"])
    e = engine(q)
    e.split_root({"root_ids": ["r1"]})
    e.submit({"root_ids": ["r1"], "backend": "lab_server"})
    assert e.lab_workers() == 0 and e.lab_paused
    load["v"] = 20.0                                               # between 1/2 and 3/4: still held
    q.advance(15); e.refresh()
    assert e.lab_workers() == 0
    load["v"] = 10.0                                               # under half: starts again
    q.advance(15); e.refresh()
    assert e.lab_workers() == 4 and not e.lab_paused


# ── failures and retries ─────────────────────────────────────────────────────

def test_retry_limit_then_gave_up():
    tid = "r3__w2"
    e = engine(D.FakeQueue(faults={tid: ["crash", "timeout", "preempt"]}))
    e.split_root({"root_ids": ["r3"]})
    e.submit({"root_ids": ["r3"], "backend": "lab_server"})
    for _ in range(3):
        e.queue.advance(60); e.refresh()
        assert e.tasks[tid].state == "failed"
        e.retry({"root_ids": ["r3"]})
    assert e.tasks[tid].state == "gave_up" and e.tasks[tid].retries == 2


def test_retry_success_counted():
    tid = "r3__w2"
    e = engine(D.FakeQueue(faults={tid: ["crash", "ok"]}))
    e.split_root({"root_ids": ["r3"]})
    e.submit({"root_ids": ["r3"], "backend": "lab_server"})
    e.queue.advance(60); e.refresh(); e.retry({"root_ids": ["r3"]})
    e.queue.advance(60); e.refresh()
    assert e.tasks[tid].state == "done" and e.stats["retry_successes"] == 1


# ── agent action set ─────────────────────────────────────────────────────────

def test_finish_refused_while_jobs_live():
    e = engine()
    acts = D.DispatcherActions(e, CFG)
    e.split_root({"root_ids": ["r3"]})
    e.submit({"root_ids": ["r3"], "backend": "lab_server"})
    with pytest.raises(ValueError, match="finish refused"):
        acts.validate({"action": "finish", "summary": "s", "rationale": "r"})
    e.queue.advance(60); e.refresh(); e.collect({"root_ids": ["r3"]})
    assert acts.validate({"action": "finish", "summary": "s", "rationale": "r"})[0] == "finish"


def test_collect_error_fails_one_window_not_the_batch():
    """c022: a collector error (tracker 'arange' on one real window) fails that window; the others are collected."""
    def collector(t):
        if t.from_h == 0:
            raise ValueError("arange: cannot compute length")
        return {"collected": True}
    e = engine(collector=collector)
    e.split_root({"root_ids": ["r2"]})
    e.submit({"root_ids": ["r2"], "backend": "lab_server"})
    e.queue.advance(600); e.refresh()
    out = e.collect({"root_ids": ["r2"]})
    states = [t.state for t in e.tasks.values()]
    assert out["collected_windows"] == states.count("collected") >= 1 and len(out["failed_windows"]) == 1
    bad = e.tasks[out["failed_windows"][0]]
    assert bad.state == "failed" and bad.cause.startswith("collect: ValueError")


def test_unknown_root_and_bad_wait_invalid():
    acts = D.DispatcherActions(engine(), CFG)
    with pytest.raises(ValueError, match="unknown root"):
        acts.validate({"action": "split_root", "root_ids": ["x"], "rationale": "r"})
    with pytest.raises(ValueError):
        acts.validate({"action": "wait", "minutes": 5, "rationale": "r"})
    with pytest.raises(ValueError, match="non-empty"):
        acts.validate({"action": "submit", "root_ids": [], "backend": "lab_server", "rationale": "r"})


def test_agent_batch_runs_to_finish(tmp_path):
    e = engine(rows=ROWS[2:])
    outputs = [{"action": "split_root", "root_ids": ["r3"]},
               {"action": "submit", "root_ids": ["r3"], "backend": "lab_server"},
               {"action": "wait", "minutes": 60},
               {"action": "collect", "root_ids": ["r3"]},
               {"action": "finish", "summary": "all collected"}]
    out = D.run_agent_batch(e, ScriptedLauncher(outputs), tmp_path / "trace.jsonl")
    assert out["status"] == "finish" and out["states"] == {"collected": 1} and out["rounds"] == 2
    trace = [json.loads(x) for x in (tmp_path / "trace.jsonl").read_text().splitlines()]
    assert any(r.get("action", {}).get("name") == "submit" for r in trace)


def test_agent_cluster_attempt_without_budget_is_refused(tmp_path):
    e = engine(rows=ROWS[2:])
    outputs = [{"action": "split_root", "root_ids": ["r3"]},
               {"action": "submit", "root_ids": ["r3"], "backend": "cluster"},
               {"action": "request_approval", "core_hours": 1, "reason": "faster"}]
    out = D.run_agent_batch(e, ScriptedLauncher(outputs), tmp_path / "t.jsonl", round_limit=3)
    assert out["status"] == "waiting_for_approval" and out["cluster_refused"] == 1 and out["approvals"] == 1
    assert not e.queue.jobs


def test_approval_request_written(tmp_path):
    e = engine(approvals_dir=tmp_path / "approvals")
    e.request_approval({"core_hours": 2.0, "reason": "r", "root_ids": ["r1"]})
    req = json.loads((tmp_path / "approvals" / "request_001.json").read_text())
    assert req["core_hours"] == 2.0 and req["usd"] == 0.02


def test_restarted_batch_skips_done_windows():
    e = engine(rows=ROWS[2:])
    e.split_root({"root_ids": ["r3"]})
    n = len(e.tasks)
    assert e.split_root({"root_ids": ["r3"]})["windows_made"] == 0 and len(e.tasks) == n


# ── script baseline ──────────────────────────────────────────────────────────

def test_script_baseline_runs_fake_batch_to_end():
    q = D.FakeQueue(faults={"r2__w0": ["crash", "ok"], "r2__w2": ["crash", "crash"]})
    e = engine(q)
    out = D.run_script_batch(e)
    assert out["status"] == "finish"
    assert out["states"].get("collected") == len(e.tasks) - 1 and out["states"].get("gave_up") == 1
    assert out["lab_peak_workers"] <= 4 and out["cluster_core_hours"] == 0
