"""Schema test (condition 2 of the typed-action review).

    python scripts/cli_probe/test_action_schema.py [--forms optional nullable union] [--reps 1]

Sends the diagnostician action schema through the agent call shape
(`agents/launcher.py`) in each schema form, on four made-up scenarios set up
to call for each of the four actions. Records for each call whether the CLI
returned structured output, whether it passed the orchestrator's validation,
and which action came back. The scenarios are invented; they are not data.
Writes results/<date>_action_schema/result.json.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from agents.actions import DIAGNOSTICIAN, FORMS  # noqa: E402
from agents.launcher import Launcher  # noqa: E402
from agents.orchestrator import PROMPTS, build_prompt  # noqa: E402

TASK = {"task": "made-up schema test task", "failed_checks": ["tip_displacement_closure"],
        "check_values": {"closure_ratio": 0.62, "closure_tolerance": [0.9, 1.1]},
        "tracking": {"frame_stride": 4, "patch_radius_px": 20}}
DISP = {"step": 1, "action": "request_info", "args": {"kind": "displacement_vs_patch_radius"},
        "result": {"median_px_per_step": 28, "p95_px_per_step": 34, "patch_radius_px": 20}}
FIX = {"step": 2, "action": "apply_remedy",
       "args": {"fault": "displacement_exceeds_patch", "remedy": "change_frame_stride", "setting": "half"},
       "result": {"failed_checks": [], "closure_ratio": 0.97}}
BLUR = {"step": 1, "action": "request_info", "args": {"kind": "frame_quality"},
        "result": {"focus": "poor", "texture": "very low", "note": "root out of focus for the whole window"}}
NOFIX = {"step": 2, "action": "apply_remedy", "args": {"fault": "low_texture", "remedy": "enlarge_patch", "setting": "2x"},
         "result": {"failed_checks": ["tip_displacement_closure"], "closure_ratio": 0.55}}
SCENARIOS = {
    "fresh_task": ([], "request_info or apply_remedy"),
    "evidence_in": ([DISP], "apply_remedy"),
    "remedy_passed": ([DISP, FIX], "accept"),
    "remedy_failed": ([BLUR, NOFIX], "decline"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forms", nargs="+", default=list(FORMS), choices=FORMS)
    ap.add_argument("--reps", type=int, default=1)
    a = ap.parse_args()
    launcher = Launcher()
    system = (PROMPTS / "diagnostician.md").read_text(encoding="utf-8")
    effort = launcher.cfg["agents"]["diagnostician"]["effort"]
    calls = []
    for form in a.forms:
        schema = DIAGNOSTICIAN.schema(form)
        for name, (history, expected) in SCENARIOS.items():
            for rep in range(a.reps):
                r = launcher.call(build_prompt(DIAGNOSTICIAN, TASK, history), system, schema, effort, 3)
                valid, err, action = False, r.error, None
                if r.ok:
                    try:
                        action, _ = DIAGNOSTICIAN.validate(r.structured_output)
                        valid = True
                    except ValueError as e:
                        err = f"validation: {e}"
                calls.append({"form": form, "scenario": name, "rep": rep, "expected": expected,
                              "cli_ok": r.ok, "cause": r.cause, "valid": valid, "action": action,
                              "error": err, "output": r.structured_output, "num_turns": r.num_turns,
                              "duration_ms": r.duration_ms, "input_tokens": r.input_tokens,
                              "output_tokens": r.output_tokens, "models": r.models})
                print(f"{form:9s} {name:14s} cli_ok={r.ok} valid={valid} action={action} "
                      f"turns={r.num_turns} {r.duration_ms} ms {err}")
    summary = {f: {"calls": sum(c["form"] == f for c in calls),
                   "valid": sum(c["form"] == f and c["valid"] for c in calls)} for f in a.forms}
    report = {"date": datetime.date.today().isoformat(), "claude_version": launcher.version,
              "model": launcher.cfg["model"], "effort": effort, "summary": summary, "calls": calls}
    out = ROOT / "results" / f"{report['date']}_action_schema"
    out.mkdir(parents=True, exist_ok=True)
    (out / "result.json").write_text(json.dumps(report, indent=2))
    print("summary:", summary)


if __name__ == "__main__":
    main()
