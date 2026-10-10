"""Live demo of the diagnostician loop on a made-up task.

    python scripts/demo_diagnostician.py

The task and every executor answer are invented to exercise the loop; they
are not data and not an evaluation case. Hidden cause: per-frame displacement
larger than the patch radius. Only `change_frame_stride` with `half` fixes it.
Writes the trace to results/<date>_demo_diagnostician/trace.jsonl.
"""
import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.launcher import Launcher  # noqa: E402
from agents.orchestrator import Orchestrator  # noqa: E402

TASK = {
    "task": "demo root, window 0-6 h (made-up example)",
    "failed_checks": ["tip_displacement_closure"],
    "passed_checks": ["rigid_body_invariance"],
    "check_values": {"closure_ratio_integrated_over_stage_log": 0.62, "closure_tolerance": [0.9, 1.1]},
    "tracking": {"frame_stride": 4, "patch_radius_px": 20},
}

INFO = {
    "check_report": {"closure_ratio": 0.62, "note": "integrated strain rate gives 62% of the tip displacement"},
    "velocity_profile": {"shape": "rises from tip, then drops to near zero beyond 0.6 mm; expected plateau missing"},
    "displacement_vs_patch_radius": {"median_px_per_step": 28, "p95_px_per_step": 34, "patch_radius_px": 20},
    "midline_jitter": {"sideways_px_rms": 0.8},
    "stage_log_summary": {"stage_moves": 3, "velocity_jump_at_moves": False},
    "frame_quality": {"focus": "good", "texture": "good", "second_object": False},
}


def request_info(args, task):
    return INFO[args["kind"]]


def apply_remedy(args, task):
    if args["remedy"] == "change_frame_stride" and args["setting"] == "half":
        return {"rechecked": True, "failed_checks": [], "closure_ratio": 0.97,
                "displacement_vs_patch_radius": {"median_px_per_step": 14, "patch_radius_px": 20}}
    return {"rechecked": True, "failed_checks": ["tip_displacement_closure"], "closure_ratio": 0.6}


def main():
    out_dir = ROOT / "results" / f"{datetime.date.today().isoformat()}_demo_diagnostician"
    trace = out_dir / "trace.jsonl"
    trace.unlink(missing_ok=True)
    orch = Orchestrator(Launcher(), trace)
    outcome = orch.run("diagnostician", "demo", TASK, {"request_info": request_info, "apply_remedy": apply_remedy})
    print(f"outcome: {outcome.status} {outcome.args}; steps {outcome.steps}; failed calls {outcome.failed_calls}")
    print(f"trace: {trace.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
