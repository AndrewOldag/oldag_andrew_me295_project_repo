"""Orchestrator and action tests with a scripted launcher. No LLM calls."""
import json

import pytest

from agents.actions import DIAGNOSTICIAN, diagnostician_schema
from agents.launcher import CallResult
from agents.orchestrator import Orchestrator

CFG = {"model": "m", "agents": {"diagnostician": {"effort": "low", "max_turns": 3, "step_limit": 4}}}
NULLS = {k: None for k in diagnostician_schema()["properties"]}


def act(**kw):
    out = dict(NULLS, rationale="r")
    out.update(kw)
    return out


class ScriptedLauncher:
    """Returns the queued outputs in order; a CallResult in the queue is returned as is."""

    def __init__(self, outputs):
        self.cfg = CFG
        self.outputs = list(outputs)
        self.prompts = []

    def call(self, prompt, system, schema, effort, max_turns):
        self.prompts.append(prompt)
        o = self.outputs.pop(0)
        if isinstance(o, CallResult):
            return o
        return CallResult(ok=True, structured_output=o, models=["m"], subtype="success")


def run(tmp_path, outputs, executors=None):
    L = ScriptedLauncher(outputs)
    orch = Orchestrator(L, tmp_path / "trace.jsonl")
    out = orch.run("diagnostician", "t1", {"failed_checks": ["closure"]}, executors or {})
    trace = [json.loads(x) for x in (tmp_path / "trace.jsonl").read_text().splitlines()]
    return out, trace, L


def test_info_then_accept(tmp_path):
    ex = {"request_info": lambda a, t: {"kind": a["kind"], "value": 3.2}}
    out, trace, L = run(tmp_path, [act(action="request_info", kind="check_report"), act(action="accept", confidence=0.9)], ex)
    assert out.status == "accept" and out.args == {"confidence": 0.9} and out.steps == 2
    assert [r["status"] for r in trace] == ["executed", "terminal"]
    assert '"value": 3.2' in L.prompts[1]          # result fed back to the agent


def test_remedy_setting_checked(tmp_path):
    bad = act(action="apply_remedy", fault="displacement_exceeds_patch", remedy="change_frame_stride", setting="2x")
    good = act(action="apply_remedy", fault="displacement_exceeds_patch", remedy="change_frame_stride", setting="half")
    ex = {"apply_remedy": lambda a, t: {"checks_pass": True}}
    out, trace, L = run(tmp_path, [bad, good, act(action="accept", confidence=0.8)], ex)
    assert [r["status"] for r in trace] == ["invalid_action", "executed", "terminal"]
    assert "not allowed for change_frame_stride" in trace[0]["error"]
    assert "invalid action" in L.prompts[1]
    assert out.status == "accept" and out.failed_calls == 1


def test_missing_argument_and_unknown_action():
    with pytest.raises(ValueError, match="needs kind"):
        DIAGNOSTICIAN.validate(act(action="request_info"))
    with pytest.raises(ValueError, match="unknown action"):
        DIAGNOSTICIAN.validate(act(action="delete_data"))
    with pytest.raises(ValueError, match="out of range"):
        DIAGNOSTICIAN.validate(act(action="accept", confidence=1.5))


def test_two_failures_in_a_row_stop(tmp_path):
    fail = CallResult(ok=False, error="model check failed: ['other'] (pinned m)")
    out, trace, _ = run(tmp_path, [fail, fail])
    assert out.status == "error" and out.steps == 2 and "model check" in out.args["reason"]


def test_step_limit(tmp_path):
    ex = {"request_info": lambda a, t: {"ok": 1}}
    out, trace, _ = run(tmp_path, [act(action="request_info", kind="frame_quality")] * 4, ex)
    assert out.status == "step_limit" and trace[-1]["status"] == "step_limit"


def test_executor_error_reported_not_raised(tmp_path):
    def boom(a, t):
        raise RuntimeError("tracker unavailable")
    out, trace, L = run(tmp_path, [act(action="request_info", kind="velocity_profile"),
                                   act(action="decline", fault="unknown", reason="no data")], {"request_info": boom})
    assert trace[0]["result"] == {"error": "RuntimeError: tracker unavailable"}
    assert out.status == "decline"


def test_schema_is_strict():
    s = diagnostician_schema()
    assert s["additionalProperties"] is False and set(s["required"]) == set(s["properties"])
