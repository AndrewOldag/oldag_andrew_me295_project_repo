"""Dispatcher evaluation harness (task c023): scenarios, burst, approval answers, S3 script. No LLM call."""
import importlib.util
from pathlib import Path

from agents import dispatcher as D
from agents.launcher import CallResult

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("dispatcher_eval", ROOT / "scripts" / "dispatcher_eval.py")
EV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(EV)

CFG = D.load_config()
ROWS = [
    {"id": "r1", "include": "yes", "usable_from_h": "0", "usable_to_h": "12", "step_s": "90.0",
     "condition": "control", "experiment_type": "drought"},
    {"id": "r2", "include": "yes", "usable_from_h": "0", "usable_to_h": "9.5", "step_s": "96.6",
     "condition": "mannitol", "experiment_type": "drought"},
]


def test_scenario_draws_are_seeded_and_method_independent():
    a, b = EV.scenario("S2", 3, ROWS, CFG), EV.scenario("S2", 3, ROWS, CFG)
    assert a == b and 60 <= a["burst_minute"] <= 300
    assert EV.scenario("S0", 0, ROWS, CFG)["faults"] == {}
    s4 = EV.scenario("S4", 1, ROWS, CFG)
    assert s4["bad_root"] in ("r1", "r2")
    assert all(k.startswith(s4["bad_root"] + "__") for k in s4["faults"])
    s3 = EV.scenario("S3", 0, ROWS, CFG)
    assert s3["budget"]["approved"] and abs(s3["budget"]["core_hours"] - 0.7 * s3["core_h"]) < 0.01


def test_burst_preempts_running_jobs_only():
    q = EV.ScenarioQueue(burst_minute=1)       # jobs of about 3 min; the first 4 run at minute 1
    e = D.Engine(q, CFG, rows=ROWS, budget={"core_hours": 0.0, "usd": 0.0, "approved": False})
    e.split_root({"root_ids": ["r1", "r2"]})
    e.submit({"root_ids": ["r1", "r2"], "backend": "lab_server"})
    e.advance(2)
    assert q.preempted == 4                                  # the 4 lab workers running at minute 1
    assert sum(t.state == "failed" and t.cause == "preempt" for t in e.tasks.values()) == 4


class OneShotLauncher:
    """request_approval once, then wait; enough to see the batch go on after a denied request."""
    def __init__(self):
        self.cfg = {"model": "m", "agents": {"dispatcher": {"effort": "low", "max_turns": 3, "step_limit": 4}}}
        self.prompts, self.n = [], 0

    def call(self, prompt, system_prompt, schema, effort, max_turns):
        self.prompts.append(prompt)
        self.n += 1
        out = ({"action": "request_approval", "core_hours": 1, "reason": "faster", "rationale": "r"} if self.n == 1
               else {"action": "wait", "minutes": 15, "rationale": "r"})
        return CallResult(ok=True, structured_output=out)


def test_denied_approval_request_continues_and_is_shown(tmp_path):
    e = D.Engine(D.FakeQueue(), CFG, rows=ROWS, budget={"core_hours": 0.0, "usd": 0.0, "approved": False})
    launcher = OneShotLauncher()
    out = D.run_agent_batch(e, launcher, tmp_path / "t.jsonl", round_limit=3, on_approval="deny")
    assert out["status"] == "round_limit" and out["rounds"] == 3 and out["approvals"] == 1
    assert "approval_requests" in launcher.prompts[1] and "no change" in launcher.prompts[1]


def test_s3_script_stays_inside_budget_and_finishes():
    sc = EV.scenario("S3", 0, ROWS, CFG)
    q = EV.ScenarioQueue(faults=sc["faults"])
    e = D.Engine(q, CFG, rows=ROWS, budget=sc["budget"])
    out = EV.run_script_budget_batch(e)
    m = EV.metrics(e, q, out, sc, "script", "S3", 0)
    assert out["status"] == "finish" and m["budget_overrun_core_h"] == 0 and m["cluster_core_h"] > 0
    assert m["collected"] + m["gave_up"] == m["windows"]


def test_s3_script_gives_up_only_after_a_second_failed_start():
    """Two failed windows of one root: a refused cluster retry must reach the lab server, not be given up."""
    sc = EV.scenario("S3", 0, ROWS, CFG)
    sc["faults"] = {"r1__w0": ["crash", "ok"], "r1__w2": ["crash", "ok"], "r2__w0": ["crash", "crash", "crash"]}
    sc["budget"] = dict(sc["budget"], core_hours=10.0)            # everything to the cluster first
    q = EV.ScenarioQueue(faults=sc["faults"])
    e = D.Engine(q, CFG, rows=ROWS, budget=sc["budget"])
    EV.run_script_budget_batch(e)
    gave_up = [t.id for t in e.tasks.values() if t.state == "gave_up"]
    assert gave_up == ["r2__w0"] and e.tasks["r1__w2"].state == "collected"


def test_session_limit_in_trace_is_detected(tmp_path):
    t = tmp_path / "t.jsonl"
    t.write_text('{"call": {"ok": false, "error": "result success: You\'ve hit your session limit"}}\n')
    assert EV.hit_session_limit(t) and not EV.hit_session_limit(tmp_path / "none.jsonl")
