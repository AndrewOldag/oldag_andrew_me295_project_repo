"""Information separation: the auditor never sees the diagnostician's reasoning."""
import json

from agents.views import auditor_input
from tests.test_orchestrator import act, run

RATIONALE = "RATIONALE-TEXT-7f3a"
REASON = "REASON-TEXT-91c2"


def test_auditor_input_has_no_reasoning(tmp_path):
    outputs = [
        dict(act(action="request_info", kind="frame_quality"), rationale=RATIONALE + " one"),
        dict(act(action="apply_remedy", fault="low_texture", remedy="enlarge_patch", setting="2x"), rationale=RATIONALE + " two"),
        dict(act(action="decline", fault="low_texture", reason=REASON), rationale=RATIONALE + " three"),
    ]
    ex = {"request_info": lambda a, t: {"focus": "poor"}, "apply_remedy": lambda a, t: {"failed_checks": ["closure"]}}
    _, trace, _ = run(tmp_path, outputs, ex)
    assert any(RATIONALE in json.dumps(r) for r in trace)        # the trace keeps it

    view = auditor_input(trace)
    text = json.dumps(view)
    assert RATIONALE not in text and REASON not in text and "rationale" not in text
    task = view[0]
    assert task["outcome"] == {"status": "decline", "args": {"fault": "low_texture"}, "steps": 3, "failed_steps": 0}
    assert task["steps"][1] == {"step": 2, "action": "apply_remedy",
                                "args": {"fault": "low_texture", "remedy": "enlarge_patch", "setting": "2x"},
                                "result": {"failed_checks": ["closure"]}}
