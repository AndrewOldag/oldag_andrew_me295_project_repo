"""Action sets for each agent: fixed lists, JSON schema, validation.

The typed actions are the agents' tool interface: each agent step returns one
action, and the orchestrator checks it and carries it out.

The lists below are a DRAFT. They must be fixed, with a decisions entry,
before any evaluation run; after that they do not change.

Schema forms (see results/2026-10-09_action_schema/):
- "optional": one flat object; `action` and `rationale` required, every
  argument optional. Default, as the planning-account review asks
- "nullable": one flat object; every field required, unused ones null
- "union": one object type per action
The orchestrator validates the chosen action's arguments in every form.
"""
from dataclasses import dataclass, field

FAULTS = [
    "rigid_drift",                 # drift or rotation not removed
    "displacement_exceeds_patch",  # per-frame displacement above patch radius
    "midline_jitter",              # sideways midline jitter
    "second_root",                 # second root in frame
    "low_texture",                 # low texture or blur
    "fast_rotation",               # rotation near the tracker limit
    "bad_stage_correction",        # jump in the velocity field at a stage move
    "width_change",                # physical: constant-width assumption broken
    "unknown",
]

# remedy -> allowed settings (None = no setting)
REMEDIES = {
    "register_frames": [None],
    "change_frame_stride": ["half", "double"],
    "smooth_midline": ["light", "strong"],
    "crop_or_mask": ["crop_to_main_root", "mask_second_root"],
    "enlarge_patch": ["1.5x", "2x"],
    "use_width_free_ratio": [None],
}

INFO_KINDS = [
    "check_report",
    "velocity_profile",
    "displacement_vs_patch_radius",
    "midline_jitter",
    "stage_log_summary",
    "frame_quality",
]

FORMS = ("optional", "nullable", "union")


@dataclass
class Action:
    name: str
    args: dict = field(default_factory=dict)       # required: name -> JSON schema of the value
    optional: dict = field(default_factory=dict)   # may be missing or null
    terminal: bool = False
    description: str = ""


@dataclass
class ActionSet:
    agent: str
    actions: list = field(default_factory=list)
    notes: str = ""           # extra lines for the prompt, e.g. remedy settings

    def by_name(self):
        return {a.name: a for a in self.actions}

    def all_args(self):
        out = {}
        for a in self.actions:
            out.update(a.args)
            out.update(a.optional)
        return out

    def schema(self, form="optional"):
        base = {"action": {"type": "string", "enum": [a.name for a in self.actions]}, "rationale": {"type": "string"}}
        if form == "optional":
            props = dict(base, **self.all_args())
            return {"type": "object", "properties": props, "required": ["action", "rationale"],
                    "additionalProperties": False}
        if form == "nullable":
            props = dict(base, **{n: {"anyOf": [s, {"type": "null"}]} for n, s in self.all_args().items()})
            return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
        if form == "union":
            variants = []
            for a in self.actions:
                props = {"action": {"type": "string", "enum": [a.name]}, "rationale": {"type": "string"}}
                props.update(a.args)
                props.update({n: {"anyOf": [s, {"type": "null"}]} for n, s in a.optional.items()})
                variants.append({"type": "object", "properties": props, "required": list(props),
                                 "additionalProperties": False})
            return {"anyOf": variants}
        raise ValueError(f"unknown schema form {form!r}")

    def describe(self):
        """Plain-text list of actions for the prompt."""
        lines = []
        for a in self.actions:
            args = ", ".join(list(a.args) + [f"{n} (optional)" for n in a.optional]) or "no arguments"
            lines.append(f"- {a.name} ({args}){' [ends the task]' if a.terminal else ''}: {a.description}")
        for n, s in self.all_args().items():
            if "enum" in s:
                lines.append(f"Allowed {n}: {', '.join(s['enum'])}")
        if self.notes:
            lines.append(self.notes)
        return "\n".join(lines)

    @staticmethod
    def _check(name, s, v):
        if "enum" in s and v not in s["enum"]:
            raise ValueError(f"{name}={v!r} not in the allowed list")
        if s.get("type") == "number" and not isinstance(v, (int, float)):
            raise ValueError(f"{name} must be a number")
        if s.get("type") == "string" and not isinstance(v, str):
            raise ValueError(f"{name} must be a string")
        if ("minimum" in s and v < s["minimum"]) or ("maximum" in s and v > s["maximum"]):
            raise ValueError(f"{name}={v} out of range")

    def validate(self, out):
        """Return (action_name, args) or raise ValueError with a reason."""
        if not isinstance(out, dict):
            raise ValueError("output is not an object")
        act = self.by_name().get(out.get("action"))
        if act is None:
            raise ValueError(f"unknown action {out.get('action')!r}")
        args = {}
        for name, s in act.args.items():
            v = out.get(name)
            if v is None:
                raise ValueError(f"{act.name} needs {name}")
            self._check(name, s, v)
            args[name] = v
        for name, s in act.optional.items():
            v = out.get(name)
            if v is not None:
                self._check(name, s, v)
            args[name] = v
        if act.name == "apply_remedy":
            allowed = REMEDIES[args["remedy"]]
            if args["setting"] not in allowed:
                raise ValueError(f"setting {args['setting']!r} not allowed for {args['remedy']}; allowed: {allowed}")
        return act.name, args


def _enum(xs):
    return {"type": "string", "enum": list(xs)}


DIAGNOSTICIAN = ActionSet("diagnostician", [
    Action("request_info", {"kind": _enum(INFO_KINDS)},
           description="get one more piece of evidence about this task"),
    Action("apply_remedy", {"fault": _enum(FAULTS), "remedy": _enum(REMEDIES)},
           {"setting": _enum(sorted({s for v in REMEDIES.values() for s in v if s}))},
           description="re-run the measurement with a remedy and setting from the fixed list"),
    Action("accept", {"confidence": {"type": "number", "minimum": 0, "maximum": 1}}, terminal=True,
           description="report the measurement"),
    Action("decline", {"fault": _enum(FAULTS), "reason": {"type": "string"}}, terminal=True,
           description="do not report the measurement"),
], notes="Allowed setting per remedy: " + "; ".join(
    f"{r}: {', '.join(s or 'none (leave setting out)' for s in v)}" for r, v in REMEDIES.items()))

ACTION_SETS = {"diagnostician": DIAGNOSTICIAN}
