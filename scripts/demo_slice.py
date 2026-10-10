"""One synthetic rod with one injected fault, from start to finish.

    python scripts/demo_slice.py [--fault displacement_exceeds_patch] [--case growth_zone] [--seed 0]
                                 [--runner remote|field] [--no-agent]

Renders the rod and tracks it on the tracker machine (remote runner; needs
private/runner.yaml), checks it at the approved thresholds, and hands any
failure to the diagnostician with the real request_info and apply_remedy.
Prints the truth, the error before and after, and the outcome. Writes the
trace and a summary to results/<date>_demo_slice/.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.executors import Slice  # noqa: E402
from measure.render import DEV_FAULTS  # noqa: E402
from measure.runner import FieldRunner, RemoteRunner, Rod  # noqa: E402
from measure.score import truth_error, truth_summary  # noqa: E402


def show_checks(checks):
    for c in checks:
        state = {True: "pass", False: "FAIL", None: "not run"}[c.passed]
        print(f"  {c.check:17s} {c.value:9.3f} {c.unit:5s} (threshold {c.threshold}) {state}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fault", choices=DEV_FAULTS, default="displacement_exceeds_patch")
    ap.add_argument("--case", default="growth_zone")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--runner", choices=["remote", "field"], default="remote")
    ap.add_argument("--no-agent", action="store_true", help="measure and check only")
    a = ap.parse_args()

    rod = Rod(a.case, a.fault if a.runner == "remote" else None, a.seed)
    if a.runner == "remote":
        runner = RemoteRunner()
        runner.sync_code()
    else:
        runner = FieldRunner()
    out_dir = ROOT / "results" / f"{datetime.date.today().isoformat()}_demo_slice"
    out_dir.mkdir(parents=True, exist_ok=True)
    trace = out_dir / "trace.jsonl"
    trace.unlink(missing_ok=True)

    sl = Slice(runner, rod)
    first = sl.current
    truth = truth_summary(first.truth, first.record.pixel_um)
    print(f"truth: {a.case} rod, injected fault {rod.fault}; {truth}")
    print(f"initial run ({sl.runs[0][0].tag()}):")
    show_checks(sl.checks)
    err_before = truth_error(first.record, first.truth)
    print(f"  error against truth: {err_before}")

    summary = {"rod": {"case": a.case, "fault": rod.fault, "seed": a.seed}, "runner": runner.form,
               "truth": truth, "error_before": err_before,
               "initial_checks": [c.to_dict() for c in sl.checks]}
    if not a.no_agent:
        from agents.launcher import Launcher
        from agents.orchestrator import Orchestrator
        outcome = Orchestrator(Launcher(), trace).run("diagnostician", sl.label, sl.task(), sl.executors())
        last = sl.current
        err_after = truth_error(last.record, last.truth)
        print("remedies applied: " + ("; ".join(ch for _, _, _, ch in sl.runs[1:]) or "none"))
        print(f"final run ({sl.runs[-1][0].tag()}):")
        show_checks(sl.checks)
        print(f"  error against truth: {err_after}")
        print(f"outcome: {outcome.status} {outcome.args}; steps {outcome.steps}; failed steps {outcome.failed_steps}; "
              f"calls {outcome.calls}; tokens in {outcome.input_tokens}, out {outcome.output_tokens}; "
              f"call time {outcome.call_ms / 1000:.1f} s")
        summary.update(outcome=outcome.__dict__, error_after=err_after,
                       remedies=[ch for _, _, _, ch in sl.runs[1:]],
                       final_checks=[c.to_dict() for c in sl.checks],
                       reported=outcome.status == "accept")
        print(f"trace: {trace.relative_to(ROOT)}")
    if getattr(runner, "log", None):
        summary["runner_log"] = runner.log
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
