"""Single-agent baseline (docs/proposals/2026-10-12_single-agent-baseline.md; spec 2026-10-12b item 4).

No check value reaches the agent: not in the first view, info answers, remedy results or error messages.
No LLM calls; tracker outputs from the fixtures (seed 0, development only).
"""
import json
import math
import re
from dataclasses import replace
from pathlib import Path

from agents.actions import ACTION_SETS, INFO_KINDS, REMEDIES
from agents.executors import BlindSlice, Slice
from agents.launcher import CallResult, load_config
from agents.orchestrator import PROMPTS, Orchestrator
from measure.record import from_tracker_npz, rigid_moved
from measure.remedies import TrackSettings
from measure.runner import MOVED, Measurement, Rod

FIX = Path(__file__).resolve().parent / "fixtures"
CHECK_KEYS = ("failed_checks", "passed_checks", "not_run", "check_values", "threshold", "rolled_back",
              "rechecked", "rigid_invariance", "plane_sections", '"closure"', '"passed"')


class FixtureRunner:
    """Unremedied: the rigid_drift fixture. Any remedy: the clean rod, or `after` if given."""
    form = "fixture"

    def __init__(self, after="growth_zone_clean_s0"):
        self.after = after

    def initial_settings(self, rod):
        return TrackSettings()

    def measure(self, rod, settings):
        name = "growth_zone_rigid_drift_z0.5_s0" if settings == TrackSettings() else self.after
        rec = from_tracker_npz(FIX / f"{name}.npz")
        rec.settings = dict(rec.settings, **settings.to_dict())
        return Measurement(rec, rigid_moved(rec, *MOVED), settings)


def slice_(cls=BlindSlice, after="growth_zone_clean_s0"):
    return cls(FixtureRunner(after), Rod("growth_zone", "rigid_drift", 0, size="0.5"))


def check_values(sl):
    """Every check value of every measurement of the slice, as the strings it could appear as."""
    out = set()
    for _, _, checks, _ in sl.runs:
        for c in checks:
            if c.value is None or not math.isfinite(c.value):
                continue
            for n in (3, 2):
                s = json.dumps(round(float(c.value), n))
                if len(s.replace("-", "").replace(".", "").lstrip("0")) >= 2:    # skip one-digit strings
                    out.add(s)
    return out


def leaks(text, values):
    hits = [k for k in CHECK_KEYS if k in text]
    hits += [v for v in values if re.search(rf"(?<![\d.]){re.escape(v)}(?![\d])", text)]
    return hits


def test_first_view_has_no_check_values():
    sl = slice_()
    assert any(c.passed is False for c in sl.checks)                 # the rod fails a check
    t = json.dumps(sl.task())
    assert leaks(t, check_values(sl)) == []
    assert set(sl.task()) == {"task", "tracking"}
    assert Slice.task(sl).keys() >= {"failed_checks", "check_values"}  # the diagnostician's view has them


def test_same_actions_info_kinds_and_remedies():
    assert ACTION_SETS["single_agent"] is ACTION_SETS["diagnostician"]
    cfg = load_config()["agents"]
    assert cfg["single_agent"] == cfg["diagnostician"]
    for kind in INFO_KINDS:
        r = slice_().request_info({"kind": kind}, {})
        if kind == "check_report":
            assert r == {"error": "check_report is not available for this task"}
        else:
            assert r == Slice.request_info(slice_(Slice), {"kind": kind}, {})
    for remedy, settings in REMEDIES.items():
        for s in settings:
            r = slice_().apply_remedy({"fault": "unknown", "remedy": remedy, "setting": s}, {})
            assert "rerun" in r                                         # carried out or refused with a reason


def test_prompt_differs_by_one_sentence():
    d = (PROMPTS / "diagnostician.md").read_text(encoding="utf-8").splitlines()
    s = (PROMPTS / "single_agent.md").read_text(encoding="utf-8").splitlines()
    diff = [(a, b) for a, b in zip(d, s) if a != b]
    assert len(d) == len(s) and len(diff) == 1
    assert diff[0][1] == diff[0][0].replace("The task tells you which checks failed.",
                                            "No checker report is given. Judge the measurement from the evidence you request.")


def test_no_roll_back():
    # a remedy that changes nothing in the measurement: the diagnostician's slice rolls back, the baseline's does not
    args = {"fault": "low_texture", "remedy": "enlarge_patch", "setting": "1.5x"}
    d = slice_(Slice, after="growth_zone_rigid_drift_z0.5_s0")
    d.runner.measure = lambda rod, st, f=d.runner.measure: f(rod, TrackSettings()) if st.disk_radius else f(rod, st)
    assert d.apply_remedy(args, {}).get("rolled_back")
    b = slice_(BlindSlice, after="growth_zone_rigid_drift_z0.5_s0")
    b.runner.measure = d.runner.measure
    r = b.apply_remedy(args, {})
    assert r == {"rerun": True, "change": r["change"]}
    assert b.runs[-1][0].disk_radius == 22 and not b.runs[-1][3].startswith("rolled back")


class ScriptedLauncher:
    def __init__(self, outputs):
        self.cfg = {"model": "m", "agents": {"single_agent": {"effort": "low", "max_turns": 3, "step_limit": 12}}}
        self.outputs, self.prompts, self.systems = list(outputs), [], []

    def call(self, prompt, system, schema, effort, max_turns):
        self.prompts.append(prompt)
        self.systems.append(system)
        return CallResult(ok=True, structured_output=self.outputs.pop(0), models=["m"], subtype="success")


def test_no_check_value_in_any_message(tmp_path):
    """Every info kind, a remedy that is carried out, one that is refused, then accept."""
    acts = [{"action": "request_info", "kind": k, "rationale": "r"} for k in INFO_KINDS]
    acts += [{"action": "apply_remedy", "fault": "rigid_drift", "remedy": "register_frames", "rationale": "r"},
             {"action": "apply_remedy", "fault": "rigid_drift", "remedy": "register_frames", "rationale": "r"},
             {"action": "request_info", "kind": "stage_log_summary", "rationale": "r"},
             {"action": "accept", "confidence": 0.5, "rationale": "r"}]
    L = ScriptedLauncher(acts)
    sl = slice_()
    out = Orchestrator(L, tmp_path / "t.jsonl").run("single_agent", sl.label, sl.task(), sl.executors())
    assert out.status == "accept" and out.steps == len(acts)
    assert len(sl.runs) == 2                                         # register_frames ran once, then was refused
    values = check_values(sl)
    assert len(values) >= 6
    for p in L.prompts:
        assert leaks(p, values) == []
    assert "not available" in L.prompts[1] and "remedy not available" in L.prompts[-1]
    assert L.systems[0] == (PROMPTS / "single_agent.md").read_text(encoding="utf-8")
