"""Non-LLM baselines: fixed-parameter script and remedy tree. No LLM, no tracker."""
import json

from agents.baselines import TREE, failing, next_remedy, run_script, run_tree
from agents.actions import FAULTS, REMEDIES
from agents.executors import Slice
from checker import CheckResult
from measure.remedies import TrackSettings
from measure.runner import FieldRunner, Rod


def chk(name, passed, detail=""):
    return CheckResult(name, passed, 1.0, 1.0, "u", detail=detail)


def test_tree_uses_the_fixed_lists_only():
    for entries in TREE.values():
        for remedy, setting, fault in entries:
            assert setting in REMEDIES[remedy] and fault in FAULTS


def test_failing_counts_uncomputable_not_skipped():
    checks = [chk("closure", True), chk("rigid_invariance", None, "no overlapping profile"),
              chk("plane_sections", None, "skipped: width-free ratio reported; x")]
    assert failing(checks) == ["rigid_invariance"]


def test_rule_order_and_skips():
    assert next_remedy(["plane_sections", "closure"], [], 1)[0] == "register_frames"
    # stride 1: halving skipped without a step
    assert next_remedy(["rigid_invariance"], [], 1)[:2] == ("enlarge_patch", "1.5x")
    # halving repeated while it is kept; not after a roll back
    kept = [("change_frame_stride", "half", "displacement_exceeds_patch", True)]
    assert next_remedy(["rigid_invariance"], kept, 3)[:2] == ("change_frame_stride", "half")
    rolled = kept + [("change_frame_stride", "half", "displacement_exceeds_patch", False)]
    assert next_remedy(["rigid_invariance"], rolled, 3)[:2] == ("enlarge_patch", "1.5x")
    # 1.5x skipped once 2x is kept
    big = [("register_frames", None, "rigid_drift", False), ("enlarge_patch", "2x", "low_texture", True)]
    assert next_remedy(["closure"], big, 1)[:2] == ("smooth_midline", "light")
    done = [(r, s, f, False) for r, s, f in TREE["plane_sections"]]
    assert next_remedy(["plane_sections"], done, 1) is None


def test_script_reports_initial_run(tmp_path):
    sl = Slice(FieldRunner(), Rod("growth_zone"))
    out = run_script(sl, tmp_path / "t.jsonl")
    assert (out.status, out.steps, out.calls, len(sl.runs)) == ("accept", 1, 0, 1)
    trace = [json.loads(x) for x in (tmp_path / "t.jsonl").read_text().splitlines()]
    assert [t["status"] for t in trace] == ["terminal", "task_end"]


def test_tree_accepts_clean_rod(tmp_path):
    out = run_tree(Slice(FieldRunner(), Rod("growth_zone")), trace_path=tmp_path / "t.jsonl")
    assert (out.status, out.steps) == ("accept", 1)


class FakeSlice:
    """Checks fail until a given remedy is applied; every other remedy is rolled back."""

    def __init__(self, fail, fixes=None):
        self.fail, self.fixes, self.applied = fail, fixes, []
        self.runs = [(TrackSettings(), None, None, "initial run")]
        self.label = "rod-1"

    @property
    def checks(self):
        return [chk(c, c not in self.fail) for c in ("rigid_invariance", "closure", "plane_sections")]

    def apply_remedy(self, args, task):
        self.applied.append(args["remedy"])
        if args["remedy"] == self.fixes:
            self.fail = []
            return {"rechecked": True}
        return {"rechecked": True, "rolled_back": True}


def test_tree_repairs_and_declines(tmp_path):
    sl = FakeSlice(["plane_sections"], fixes="use_width_free_ratio")
    out = run_tree(sl, trace_path=tmp_path / "a.jsonl")
    assert (out.status, out.steps, sl.applied) == ("accept", 3, ["smooth_midline", "use_width_free_ratio"])
    sl = FakeSlice(["plane_sections"])
    out = run_tree(sl, trace_path=tmp_path / "b.jsonl")
    assert (out.status, out.steps, out.args["fault"]) == ("decline", 3, "midline_jitter")


def test_tree_step_limit(tmp_path):
    sl = FakeSlice(["closure"])
    out = run_tree(sl, step_limit=3, trace_path=tmp_path / "c.jsonl")
    assert (out.status, out.steps, len(sl.applied)) == ("step_limit", 3, 3)
    out = run_tree(FakeSlice(["closure"]), step_limit=8)
    assert (out.status, out.steps) == ("decline", 5)        # stride 1: four remedies, then decline
