"""What each agent is allowed to see of other agents' work.

The auditor sees the batch but not the diagnostician's reasoning: no
`rationale`, no raw model output, and no free-text argument (such as a
decline `reason`). It keeps actions, arguments from the fixed lists,
numbers, executor results and task outcomes.
"""
from .actions import ACTION_SETS


def _fixed_args(action_set, name, args):
    """Keep only arguments whose values come from a fixed list or are numbers."""
    act = action_set.by_name().get(name)
    if act is None:
        return {}
    schemas = dict(act.args, **act.optional)
    return {k: v for k, v in (args or {}).items()
            if k in schemas and ("enum" in schemas[k] or schemas[k].get("type") == "number")}


def auditor_input(trace_records, agent="diagnostician"):
    """Per-task summary of one agent's trace, for the auditor."""
    action_set = ACTION_SETS[agent]
    tasks = {}
    for r in trace_records:
        if r.get("agent") != agent:
            continue
        t = tasks.setdefault(r["task_id"], {"task_id": r["task_id"], "steps": [], "outcome": None})
        if r.get("status") == "task_end":
            o = r["outcome"]
            t["outcome"] = {"status": o["status"], "args": _fixed_args(action_set, o["status"], o.get("args")),
                            "steps": o["steps"], "failed_steps": o["failed_steps"]}
        elif r.get("status") in ("executed", "terminal"):
            a = r["action"]
            step = {"step": r["step"], "action": a["name"], "args": _fixed_args(action_set, a["name"], a["args"])}
            if r.get("status") == "executed":
                step["result"] = r.get("result")
            t["steps"].append(step)
        elif r.get("status") == "failed_step":
            t["steps"].append({"step": r["step"], "failed": r.get("cause")})
    return list(tasks.values())
