"""Step loop: ask an agent for one action, check it, execute it, repeat.

The orchestrator is plain code. It decides what each agent sees, runs every
action itself, and writes one trace line per step. Agents run nothing.

Stops when the agent returns a terminal action, at the step limit, or after
two failed calls in a row. Failed calls (CLI error, model check, invalid
action) count as steps.
"""
import datetime
import json
from dataclasses import dataclass, field
from pathlib import Path

from .actions import ACTION_SETS, SCHEMAS

PROMPTS = Path(__file__).resolve().parent / "prompts"


@dataclass
class Outcome:
    task_id: str
    agent: str
    status: str            # terminal action name, "step_limit" or "error"
    args: dict = field(default_factory=dict)
    steps: int = 0
    failed_calls: int = 0


def build_prompt(action_set, task, history):
    parts = [
        "TASK",
        json.dumps(task, indent=1),
        "",
        "ACTIONS",
        action_set.describe(),
        "",
        "HISTORY (oldest first)" if history else "HISTORY: none yet",
    ]
    for h in history:
        parts.append(json.dumps(h))
    parts += ["", "Return the next action. Set every argument the action does not use to null."]
    return "\n".join(parts)


class Orchestrator:
    def __init__(self, launcher, trace_path):
        self.launcher = launcher
        self.trace_path = Path(trace_path)
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)

    def _trace(self, rec):
        rec["time"] = datetime.datetime.now().isoformat(timespec="seconds")
        with self.trace_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    def run(self, agent, task_id, task, executors):
        """executors: action name -> function(args, task) -> JSON-serializable result.

        Terminal actions need no executor. A non-terminal action without an
        executor is reported back to the agent as unavailable.
        """
        cfg = self.launcher.cfg["agents"][agent]
        action_set = ACTION_SETS[agent]
        schema = SCHEMAS[agent]()
        system = (PROMPTS / f"{agent}.md").read_text(encoding="utf-8")
        history, failed_in_row, failed = [], 0, 0
        terminal = {a.name for a in action_set.actions if a.terminal}

        for step in range(1, cfg["step_limit"] + 1):
            prompt = build_prompt(action_set, task, history)
            call = self.launcher.call(prompt, system, schema, cfg["effort"], cfg["max_turns"])
            rec = {"agent": agent, "task_id": task_id, "step": step, "call": call.record()}
            if not call.ok:
                failed += 1
                failed_in_row += 1
                rec["status"] = "call_failed"
                self._trace(rec)
                if failed_in_row >= 2:
                    return Outcome(task_id, agent, "error", {"reason": call.error}, step, failed)
                continue
            out = call.structured_output
            rec["output"] = out
            try:
                name, args = action_set.validate(out)
            except ValueError as e:
                failed += 1
                failed_in_row += 1
                rec["status"] = "invalid_action"
                rec["error"] = str(e)
                self._trace(rec)
                history.append({"step": step, "action": out.get("action"), "result": {"error": f"invalid action: {e}"}})
                if failed_in_row >= 2:
                    return Outcome(task_id, agent, "error", {"reason": str(e)}, step, failed)
                continue
            failed_in_row = 0
            rec["action"] = {"name": name, "args": args}
            if name in terminal:
                rec["status"] = "terminal"
                self._trace(rec)
                return Outcome(task_id, agent, name, args, step, failed)
            fn = executors.get(name)
            if fn is None:
                result = {"error": f"{name} is not available for this task"}
            else:
                try:
                    result = fn(args, task)
                except Exception as e:  # executor failure is shown to the agent and logged
                    result = {"error": f"{type(e).__name__}: {e}"}
            rec["status"] = "executed"
            rec["result"] = result
            self._trace(rec)
            history.append({"step": step, "action": name, "args": args, "rationale": out.get("rationale", ""),
                            "result": result})

        self._trace({"agent": agent, "task_id": task_id, "step": cfg["step_limit"], "status": "step_limit"})
        return Outcome(task_id, agent, "step_limit", {}, cfg["step_limit"], failed)
