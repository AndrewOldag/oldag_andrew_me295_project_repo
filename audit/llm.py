"""LLM auditor (spec 2026-10-13, Task A3): typed actions through the existing orchestrator.

Actions: request_info (batch_table, run_record), flag, clear, report (ends the task). flag and clear take a
list of run ids, so that a batch of 25 accepted runs fits in the step limit of 20. Every accepted run must end
flagged or cleared: `report` is refused as an invalid action while any accepted run is undecided. A later
flag or clear of the same run replaces the earlier one. Only accepted runs can be flagged or cleared.

The auditor sees only the batch view (audit/view.py). The action set is built per batch (run ids as fixed
lists) and registered as ACTION_SETS["auditor"] for the orchestrator; agents/actions.py is not changed.
"""
from agents.actions import ACTION_SETS, Action, ActionSet
from audit.view import SUMMARIES

AUDIT_INFO_KINDS = ["batch_table", "run_record"]
REASONS = ["check_failed_but_accepted", "summary_outlier", "remedy_pattern", "width_free_ratio_used", "other"]
EVIDENCE = ["rigid_invariance", "closure", "plane_sections", *SUMMARIES, "remedies_kept", "roll_backs", "steps",
            "final_settings"]


def _enum(xs):
    return {"type": "string", "enum": list(xs)}


def _list(xs):
    return {"type": "array", "items": _enum(xs), "minItems": 1}


class AuditorActions(ActionSet):
    """The auditor's action set for one batch. validate also checks list arguments and the report gate."""

    def __init__(self, batch):
        self.batch = batch
        ids, acc = batch.run_ids, batch.accepted
        super().__init__("auditor", [
            Action("request_info", {"kind": _enum(AUDIT_INFO_KINDS)}, {"run_id": _enum(ids)},
                   description="batch_table: one row per run with checks and summaries; "
                               "run_record: the full record of one run (give run_id)"),
            Action("flag", {"run_ids": _list(acc), "reason": _enum(REASONS), "evidence": _list(EVIDENCE)},
                   description="mark accepted runs whose report should not be trusted, with one reason "
                               "and the fields that show it"),
            Action("clear", {"run_ids": _list(acc)}, description="mark accepted runs whose report stands"),
            Action("report", {"text": {"type": "string"}}, terminal=True,
                   description="the batch report; allowed once every accepted run is flagged or cleared"),
        ], notes="run_ids: accepted run ids from the task. Allowed evidence: " + ", ".join(EVIDENCE))

    def validate(self, out):
        name, args = super().validate(out)
        for k in ("run_ids", "evidence"):
            if k in args:
                v = args[k]
                allowed = self.by_name()[name].args[k]["items"]["enum"]
                if not isinstance(v, list) or not v or any(x not in allowed for x in v):
                    raise ValueError(f"{k} must be a non-empty list from: {', '.join(allowed)}")
        if name == "request_info" and args["kind"] == "run_record" and not args.get("run_id"):
            raise ValueError("run_record needs run_id")
        if name == "report" and self.batch.undecided():
            raise ValueError("not yet flagged or cleared: " + ", ".join(self.batch.undecided()))
        return name, args


class AuditBatch:
    """One batch for the LLM auditor: the view, the decisions so far, and the executors."""

    label = "batch-1"

    def __init__(self, view):
        self.view = view
        self.runs = {r["run_id"]: r for r in view["runs"]}
        self.run_ids = sorted(self.runs)
        self.accepted = [i for i in self.run_ids if self.runs[i]["status"] == "accept"]
        self.decisions = {}                  # run_id -> {"decision", "reason", "evidence", "step"}
        self.actions = AuditorActions(self)
        ACTION_SETS["auditor"] = self.actions
        self._step = 0

    def undecided(self):
        return [i for i in self.accepted if i not in self.decisions]

    def task(self):
        return {"task": f"audit one batch of {len(self.run_ids)} runs, {len(self.accepted)} accepted",
                "accepted": self.accepted,
                "batch_table": self.view["table"]}

    def request_info(self, args, task):
        if args["kind"] == "batch_table":
            return self.view["table"]
        return {k: v for k, v in self.runs[args["run_id"]].items()}

    def _decide(self, decision, args):
        self._step += 1
        for i in args["run_ids"]:
            d = {"decision": decision, "order": self._step}
            if decision == "flag":
                d.update(reason=args["reason"], evidence=args["evidence"])
            self.decisions[i] = d
        return {"recorded": decision, "run_ids": args["run_ids"], "undecided": self.undecided()}

    def flag(self, args, task):
        return self._decide("flag", args)

    def clear(self, args, task):
        return self._decide("clear", args)

    def executors(self):
        return {"request_info": self.request_info, "flag": self.flag, "clear": self.clear}
