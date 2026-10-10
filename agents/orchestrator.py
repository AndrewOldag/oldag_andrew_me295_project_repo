"""Step loop: ask an agent for one typed action, check it, carry it out, repeat.

The typed actions are the agents' tool interface. The orchestrator is plain
code: it decides what each agent sees, carries out every action itself, and
writes one trace line per step plus one summary line per task.

Stops when the agent returns a terminal action, at the step limit, or after
two failed steps in a row. A failed step is a failed call (timeout, non-zero
exit, turn limit, schema error, model check) or an invalid action; each is
logged with its cause and counts as a step.
"""
import datetime
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .actions import ACTION_SETS

PROMPTS = Path(__file__).resolve().parent / "prompts"


@dataclass
class Outcome:
    task_id: str
    agent: str
    status: str            # terminal action name, "step_limit" or "error"
    args: dict = field(default_factory=dict)
    steps: int = 0
    failed_steps: int = 0
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    call_ms: int = 0


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
    parts += ["", "Return the next action. Leave out arguments the action does not use."]
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
        schema = action_set.schema(cfg.get("schema_form", "optional"))
        system = (PROMPTS / f"{agent}.md").read_text(encoding="utf-8")
        terminal = {a.name for a in action_set.actions if a.terminal}
        history, failed_in_row = [], 0
        out = Outcome(task_id, agent, "step_limit")

        def finish(status, args=None):
            out.status, out.args = status, args or {}
            self._trace({"agent": agent, "task_id": task_id, "status": "task_end", "outcome": asdict(out)})
            return out

        for step in range(1, cfg["step_limit"] + 1):
            out.steps = step
            prompt = build_prompt(action_set, task, history)
            call = self.launcher.call(prompt, system, schema, cfg["effort"], cfg["max_turns"])
            out.calls += 1
            out.input_tokens += call.input_tokens
            out.output_tokens += call.output_tokens
            out.call_ms += call.duration_ms
            rec = {"agent": agent, "task_id": task_id, "step": step, "call": call.record()}
            if not call.ok:
                out.failed_steps += 1
                failed_in_row += 1
                rec.update(status="failed_step", cause=call.cause or "unknown", error=call.error)
                self._trace(rec)
                if failed_in_row >= 2:
                    return finish("error", {"cause": call.cause, "reason": call.error})
                continue
            output = call.structured_output
            rec["output"] = output
            try:
                name, args = action_set.validate(output)
            except ValueError as e:
                out.failed_steps += 1
                failed_in_row += 1
                rec.update(status="failed_step", cause="invalid_action", error=str(e))
                self._trace(rec)
                history.append({"step": step, "action": output.get("action"), "result": {"error": f"invalid action: {e}"}})
                if failed_in_row >= 2:
                    return finish("error", {"cause": "invalid_action", "reason": str(e)})
                continue
            failed_in_row = 0
            rec["action"] = {"name": name, "args": args}
            if name in terminal:
                rec["status"] = "terminal"
                self._trace(rec)
                return finish(name, args)
            fn = executors.get(name)
            if fn is None:
                result = {"error": f"{name} is not available for this task"}
            else:
                try:
                    result = fn(args, task)
                except Exception as e:  # executor failure is shown to the agent and logged
                    result = {"error": f"{type(e).__name__}: {e}"}
            rec.update(status="executed", result=result)
            self._trace(rec)
            history.append({"step": step, "action": name, "args": args, "rationale": output.get("rationale", ""),
                            "result": result})

        return finish("step_limit")
