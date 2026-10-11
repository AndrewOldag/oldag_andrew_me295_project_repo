"""One synthetic rod with one injected fault, from start to finish.

    python scripts/demo_slice.py [--fault displacement_exceeds_patch] [--size 2x6] [--case growth_zone] [--seed 0]
                                 [--runner remote|field] [--no-agent] [--out results/<dir>] [--replay]

Renders the rod and tracks it on the tracker machine (remote runner; needs
private/runner.yaml), checks it at the approved thresholds, and hands any
failure to the diagnostician with the real request_info and apply_remedy.
Prints the truth, the error before and after, and the outcome. Writes the
trace and a summary to results/<date>_demo_slice/ (or --out), named by
fault, size and seed. --replay re-applies the remedies recorded in the
existing trace (no agent call; tracker outputs come from the runner's cache)
and rewrites the summary.
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


def replay(trace, sl):
    """Re-apply the apply_remedy actions of a trace to the slice; return the recorded outcome."""
    from types import SimpleNamespace
    outcome = None
    for line in trace.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        act = d.get("action") or {}
        if d.get("status") == "executed" and act.get("name") == "apply_remedy":
            sl.apply_remedy(act["args"], {})
        if d.get("status") == "task_end":
            outcome = SimpleNamespace(**d["outcome"])
    return outcome


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fault", choices=DEV_FAULTS, default="displacement_exceeds_patch")
    ap.add_argument("--case", default="growth_zone")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--runner", choices=["remote", "field"], default="remote")
    ap.add_argument("--no-agent", action="store_true", help="measure and check only")
    ap.add_argument("--size", default=None, help="fault size (measure.render.fault_settings)")
    ap.add_argument("--out", default=None, help="results folder (default results/<date>_demo_slice)")
    ap.add_argument("--replay", action="store_true", help="replay the remedies of the existing trace; no agent call")
    a = ap.parse_args()

    rod = Rod(a.case, a.fault if a.runner == "remote" else None, a.seed, size=a.size if a.runner == "remote" else None)
    if a.runner == "remote":
        runner = RemoteRunner()
        runner.sync_code()
    else:
        runner = FieldRunner()
    out_dir = Path(a.out).resolve() if a.out else ROOT / "results" / f"{datetime.date.today().isoformat()}_demo_slice"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"{a.fault or 'clean'}" + (f"_z{a.size}" if a.size else "") + f"_s{a.seed}"
    trace = out_dir / f"{name}_trace.jsonl"
    if not a.replay:
        trace.unlink(missing_ok=True)

    sl = Slice(runner, rod)
    first = sl.current
    truth = truth_summary(first.truth, first.record.pixel_um)
    print(f"truth: {a.case} rod, injected fault {rod.fault}; {truth}")
    print(f"initial run ({sl.runs[0][0].tag()}):")
    show_checks(sl.checks)
    err_before = truth_error(first.record, first.truth)
    print(f"  error against truth: {err_before}")

    summary = {"rod": {"case": a.case, "fault": rod.fault, "size": a.size, "seed": a.seed}, "runner": runner.form,
               "truth": truth, "error_before": err_before,
               "initial_checks": [c.to_dict() for c in sl.checks]}
    if not a.no_agent:
        from agents.launcher import Launcher
        from agents.orchestrator import Orchestrator
        if a.replay:
            outcome = replay(trace, sl)
        else:
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
                       roll_backs=sum(ch.startswith("rolled back") for _, _, _, ch in sl.runs[1:]),
                       final_settings=sl.runs[-1][0].to_dict(),
                       final_checks=[c.to_dict() for c in sl.checks],
                       reported=outcome.status == "accept")
        print(f"trace: {trace.relative_to(ROOT)}")
    if getattr(runner, "log", None):
        summary["runner_log"] = runner.log
    (out_dir / f"{name}_summary.json").write_text(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
