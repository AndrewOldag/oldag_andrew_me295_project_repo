"""The two non-LLM baselines: fixed-parameter script and rule-based remedy tree. No LLM calls.

Both act on a Slice (agents/executors.py), so remedies, re-runs and roll back
are the same code the diagnostician uses, and both return the orchestrator's
Outcome and write trace lines in its format (agents/orchestrator.py).
The tree is fixed in docs/proposals/2026-10-12_remedy-tree.md.
"""
import datetime
import json
from dataclasses import asdict
from pathlib import Path

from .orchestrator import Outcome

ORDER = ("closure", "rigid_invariance", "plane_sections")      # rule 1: first failing check picks the list

# rule 1 lists: (remedy, setting, fault named)
TREE = {
    "closure": [("register_frames", None, "rigid_drift"),
                ("change_frame_stride", "half", "displacement_exceeds_patch"),
                ("enlarge_patch", "1.5x", "low_texture"),
                ("enlarge_patch", "2x", "low_texture"),
                ("smooth_midline", "light", "midline_jitter")],
    "rigid_invariance": [("change_frame_stride", "half", "displacement_exceeds_patch"),
                         ("enlarge_patch", "1.5x", "low_texture"),
                         ("enlarge_patch", "2x", "low_texture"),
                         ("crop_or_mask", "mask_second_root", "second_root")],
    "plane_sections": [("smooth_midline", "light", "midline_jitter"),
                       ("use_width_free_ratio", None, "width_change")],
}


def failing(checks):
    """Failing checks; a check that cannot be computed counts as failing, one skipped on purpose does not."""
    return [c.check for c in checks
            if c.passed is False or (c.passed is None and not c.detail.startswith("skipped"))]


def next_remedy(fail, tried, stride):
    """Rule 2. tried: list of (remedy, setting, fault, kept), oldest first. Returns a TREE entry or None."""
    first = next(c for c in ORDER if c in fail)
    for remedy, setting, fault in TREE[first]:
        same = [t for t in tried if t[:2] == (remedy, setting)]
        if remedy == "change_frame_stride":
            if stride == 1 or (same and not same[-1][3]):
                continue
        elif same:
            continue
        if (remedy, setting) == ("enlarge_patch", "1.5x") and any(t[:2] == ("enlarge_patch", "2x") and t[3]
                                                                  for t in tried):
            continue
        return remedy, setting, fault
    return None


class _Trace:
    def __init__(self, path, agent, task_id):
        self.path, self.agent, self.task_id = Path(path) if path else None, agent, task_id
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, rec):
        if not self.path:
            return
        rec = {"agent": self.agent, "task_id": self.task_id, **rec,
               "time": datetime.datetime.now().isoformat(timespec="seconds")}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")


def _terminal(trace, out, step, name, args, rationale):
    out.steps, out.status, out.args = step, name, args
    trace.write({"step": step, "status": "terminal", "output": {"action": name, "rationale": rationale, **args},
                 "action": {"name": name, "args": args}})
    trace.write({"status": "task_end", "outcome": asdict(out)})
    return out


def run_script(sl, trace_path=None):
    """Fixed-parameter script: the initial run with the base settings is reported; no check is acted on."""
    trace = _Trace(trace_path, "script", sl.label)
    out = Outcome(sl.label, "script", "accept")
    return _terminal(trace, out, 1, "accept", {"confidence": None},
                     "fixed-parameter script: base settings, checks not acted on")


def run_tree(sl, step_limit=8, trace_path=None):
    """Rule-based remedy tree (docs/proposals/2026-10-12_remedy-tree.md)."""
    trace = _Trace(trace_path, "remedy_tree", sl.label)
    out = Outcome(sl.label, "remedy_tree", "step_limit")
    tried = []
    for step in range(1, step_limit + 1):
        out.steps = step
        fail = failing(sl.checks)
        if not fail:
            return _terminal(trace, out, step, "accept", {"confidence": None}, "rule 0: no check fails")
        pick = next_remedy(fail, tried, sl.runs[-1][0].stride)
        if pick is None:
            kept = [t for t in tried if t[3]]
            fault = kept[-1][2] if kept else tried[0][2] if tried else "unknown"
            return _terminal(trace, out, step, "decline", {"fault": fault, "reason": f"rule 3: no remedy left "
                             f"for {next(c for c in ORDER if c in fail)}"},
                             f"rule 3: failing {', '.join(fail)}; list exhausted")
        remedy, setting, fault = pick
        args = {"fault": fault, "remedy": remedy, "setting": setting}
        result = sl.apply_remedy(args, {})
        tried.append((remedy, setting, fault, bool(result.get("rechecked")) and not result.get("rolled_back")))
        trace.write({"step": step, "status": "executed",
                     "output": {"action": "apply_remedy", "rationale": f"rule 1: failing {', '.join(fail)}", **args},
                     "action": {"name": "apply_remedy", "args": args}, "result": result})
    trace.write({"status": "task_end", "outcome": asdict(out)})
    return out
