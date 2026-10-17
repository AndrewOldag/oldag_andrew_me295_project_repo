"""Auditor v1 (spec 2026-10-13, Task A): view, leak test, batch statistics, rule auditor, LLM auditor actions.
No LLM calls; tracker outputs from the fixtures, run summaries from results/2026-10-12b_scored_v1/."""
import json
from pathlib import Path

import pytest

from agents.launcher import CallResult
from agents.orchestrator import Orchestrator
from audit import rule
from audit.llm import AuditBatch
from audit.view import batch_table, batch_view, field_summaries, opaque_ids, remedies_kept, robust_z
from measure.record import from_tracker_npz

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
SCORED = ROOT / "results" / "2026-10-12b_scored_v1" / "dev"
WITHHELD_KEYS = {"fault", "size", "seed", "label", "truth", "error_before", "error_after", "category", "correct",
                 "good", "named_fault", "trace", "traces", "method", "rod", "rationale", "reason", "initial_checks",
                 "runner_log", "root_id", "commit", "freeze_tag"}
SENTINEL_TEXT = "zzwithheldzz"
SENTINEL_NUM = 987654.321


def keys(x):
    if isinstance(x, dict):
        return set(x) | set().union(*(keys(v) for v in x.values())) if x else set()
    if isinstance(x, list):
        return set().union(*(keys(v) for v in x)) if x else set()
    return set()


def poisoned(path):
    """A real run summary with every withheld field replaced by sentinels."""
    s = json.loads(path.read_text())
    s["rod"] = {"case": SENTINEL_TEXT, "fault": SENTINEL_TEXT, "size": SENTINEL_TEXT, "seed": SENTINEL_NUM}
    s["truth"] = {k: SENTINEL_NUM for k in s["truth"]}
    s["error_before"] = {k: SENTINEL_NUM for k in s["error_before"]}
    s["error_after"] = {k: SENTINEL_NUM for k in s["error_after"]}
    s["initial_checks"] = [dict(c, value=SENTINEL_NUM, detail=SENTINEL_TEXT) for c in s["initial_checks"]]
    s["method"] = s["commit"] = s["freeze_tag"] = s["runner"] = SENTINEL_TEXT
    s["outcome"]["args"] = {"fault": SENTINEL_TEXT, "reason": SENTINEL_TEXT, "confidence": SENTINEL_NUM}
    s["outcome"]["task_id"] = SENTINEL_TEXT
    for k in ("label", "category", "correct", "good", "named_fault"):
        s[k] = SENTINEL_TEXT
    s["final_checks"] = [dict(c, detail=SENTINEL_TEXT) for c in s["final_checks"]]
    return s


def record(name="growth_zone_width_change_s0"):
    rec = from_tracker_npz(FIX / f"{name}.npz")
    rec.truth = {"regr_mid": SENTINEL_NUM}
    rec.root_id = SENTINEL_TEXT
    return rec


def batch():
    paths = sorted(SCORED.glob("diagnostician_*_summary.json"))[:6]
    names = ["growth_zone_clean_s0", "growth_zone_clean_s1", "growth_zone_width_change_s0",
             "growth_zone_rigid_drift_z0.5_s0", "growth_zone_low_texture_z0.03_s0", "growth_zone_clean_s0"]
    return [poisoned(p) for p in paths], [record(n) for n in names]


def test_no_withheld_key_or_value_reaches_the_view():
    summaries, records = batch()
    views, stats, _ = batch_view(summaries, records, key="test")
    task = AuditBatch({"runs": views, "table": batch_table(views, stats)}).task()
    for obj in (views, stats, task):
        text = json.dumps(obj)
        assert not keys(obj) & WITHHELD_KEYS, keys(obj) & WITHHELD_KEYS
        assert SENTINEL_TEXT not in text and str(SENTINEL_NUM) not in text and "987654" not in text
    # every run name and fault name of the batch stays out
    text = json.dumps(task)
    for p in sorted(SCORED.glob("diagnostician_*_summary.json"))[:6]:
        assert p.name.replace("_summary.json", "") not in text


def test_leak_test_sees_a_leak():
    summaries, records = batch()
    views, _, _ = batch_view(summaries, records, key="test")
    views[0]["note"] = summaries[0]["rod"]
    assert SENTINEL_TEXT in json.dumps(views) and "fault" in keys(views)


def test_view_contents():
    s = json.loads((SCORED / "diagnostician_width_change_s1_summary.json").read_text())
    views, _, _ = batch_view([s], [from_tracker_npz(FIX / "growth_zone_width_change_s0.npz")], key="k")
    v = views[0]
    assert v["status"] == "accept" and v["steps"] == s["outcome"]["steps"]
    assert {c["check"] for c in v["final_checks"]} == {"rigid_invariance", "closure", "plane_sections"}
    assert v["final_settings"]["width_free"] is True and v["summaries"]["width_free_ratio_max"] is not None
    assert v["remedies_kept"] == s["remedies"]


def test_status_mapping():
    s = json.loads((SCORED / "diagnostician_width_change_s1_summary.json").read_text())
    rec = from_tracker_npz(FIX / "growth_zone_clean_s0.npz")
    for st, want in (("decline", "decline"), ("step_limit", "not_reported"), ("error", "not_reported")):
        s["outcome"]["status"] = st
        assert batch_view([s], [rec], key="k")[0][0]["status"] == want


def test_field_summaries_clean_rod():
    f = field_summaries(from_tracker_npz(FIX / "growth_zone_clean_s0.npz"))
    assert 35 < f["centre_peak_regr_pct_per_h"] < 50 and 200 < f["centre_peak_at_um"] < 450
    assert 300 < f["growth_zone_length_um"] < 900
    assert abs(f["flank_difference_max_pct_per_h"]) < 10
    assert f["width_free_ratio_max"] is None


def test_remedies_kept():
    ch = ["a", "rolled back: a", "b", "c", "rolled back: c"]
    assert remedies_kept(ch) == ["b"]
    assert remedies_kept([]) == []


def test_robust_z():
    r = robust_z([1.0, 2.0, 3.0, 4.0, 100.0, None])
    assert r["median"] == 3.0 and r["mad"] == 1.0
    assert r["z"][2] == 0.0 and r["z"][4] > 3 and r["z"][5] is None
    r = robust_z([5.0, 5.0, 5.0, 5.0, 50.0])              # MAD 0: mean absolute deviation
    assert r["mad"] == 0.0 and r["z"][0] == 0.0 and r["z"][4] > 3
    assert robust_z([1.0, 1.0, 1.0])["z"] == [0.0, 0.0, 0.0]
    assert robust_z([1.0, None, 2.0])["z"] == [None, None, None]


def test_opaque_ids_shuffled_and_fixed():
    a, b = opaque_ids(25, "dev/script"), opaque_ids(25, "dev/script")
    assert a == b and sorted(a) == [f"r{i:02d}" for i in range(1, 26)] and a != sorted(a)


def view(rid, status="accept", passed=(True, True, True), z=0.0):
    checks = [{"check": c, "value": 1.0, "threshold": 2.0, "unit": "", "passed": p}
              for c, p in zip(("rigid_invariance", "closure", "plane_sections"), passed)]
    return {"run_id": rid, "status": status, "final_checks": checks, "remedies_kept": [], "roll_backs": 0,
            "steps": 1, "final_settings": {"width_free": False}, "summaries": {"centre_peak_regr_pct_per_h": 1.0},
            "z": {"centre_peak_regr_pct_per_h": z, "growth_zone_length_um": None}}


def test_rule_auditor():
    vs = [view("r01"), view("r02", passed=(True, False, True)), view("r03", z=3.5), view("r04", z=-3.01),
          view("r05", status="decline", passed=(False, False, False)), view("r06", passed=(True, True, None), z=3.0)]
    d = rule.audit(vs)
    assert set(d) == {"r01", "r02", "r03", "r04", "r06"}
    assert [d[i]["decision"] for i in ("r01", "r02", "r03", "r04", "r06")] == ["clear", "flag", "flag", "flag", "clear"]
    assert d["r02"]["reasons"] == ["check_failed:closure"]


# ------------------------------------------------------------------ LLM auditor actions, scripted launcher

CFG = {"model": "m", "agents": {"auditor": {"effort": "low", "max_turns": 3, "step_limit": 20}}}


class ScriptedLauncher:
    def __init__(self, outputs):
        self.cfg, self.outputs, self.prompts = CFG, list(outputs), []

    def call(self, prompt, system, schema, effort, max_turns):
        self.prompts.append(prompt)
        o = self.outputs.pop(0)
        return CallResult(ok=True, structured_output=dict(rationale="r", **o), models=["m"], subtype="success",
                          input_tokens=100, output_tokens=10, duration_ms=50)


def audit_batch():
    vs = [view("r01"), view("r02"), view("r03", status="decline")]
    return AuditBatch({"runs": vs, "table": {"runs": []}})


def run(tmp_path, outputs):
    b = audit_batch()
    L = ScriptedLauncher(outputs)
    o = Orchestrator(L, tmp_path / "t.jsonl").run("auditor", b.label, b.task(), b.executors())
    return o, b, L


def test_flag_clear_report(tmp_path):
    o, b, L = run(tmp_path, [{"action": "request_info", "kind": "run_record", "run_id": "r02"},
                             {"action": "flag", "run_ids": ["r02"], "reason": "summary_outlier",
                              "evidence": ["centre_peak_regr_pct_per_h"]},
                             {"action": "clear", "run_ids": ["r01"]},
                             {"action": "report", "text": "two accepted; one flagged"}])
    assert o.status == "report" and o.steps == 4 and b.undecided() == []
    assert b.decisions["r02"]["decision"] == "flag" and b.decisions["r01"]["decision"] == "clear"
    assert '"run_id": "r02"' in L.prompts[1]


def test_report_refused_while_undecided(tmp_path):
    o, b, L = run(tmp_path, [{"action": "clear", "run_ids": ["r01"]},
                             {"action": "report", "text": "x"},
                             {"action": "clear", "run_ids": ["r02"]},
                             {"action": "report", "text": "x"}])
    assert o.status == "report" and o.failed_steps == 1
    assert "not yet flagged or cleared: r02" in L.prompts[2]


@pytest.mark.parametrize("bad", [
    {"action": "flag", "run_ids": ["r03"], "reason": "other", "evidence": ["steps"]},          # not accepted
    {"action": "flag", "run_ids": ["r01"], "reason": "other", "evidence": ["truth"]},          # not a field
    {"action": "flag", "run_ids": [], "reason": "other", "evidence": ["steps"]},
    {"action": "clear", "run_ids": ["r09"]},
    {"action": "request_info", "kind": "run_record"},                                          # no run_id
    {"action": "flag", "run_ids": ["r01"], "reason": "fault_named", "evidence": ["steps"]},
])
def test_invalid_actions(tmp_path, bad):
    o, b, _ = run(tmp_path, [bad, bad])
    assert o.status == "error" and b.decisions == {}


def test_auditor_config_and_prompt():
    from agents.launcher import load_config
    from agents.orchestrator import PROMPTS
    cfg = load_config()
    assert cfg["agents"]["auditor"]["step_limit"] == 20
    assert cfg["model"] == "claude-opus-5-5" and str(cfg["claude_code_version"]) == "2.1.302"
    assert (PROMPTS / "auditor.md").exists()
