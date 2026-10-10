"""Action sets for each agent: fixed lists, JSON schema, validation.

The lists below are a DRAFT. They must be fixed, with a decisions entry,
before any evaluation run; after that they do not change.

The output schema is one flat object: `action`, `rationale`, and every
argument any action can take. Arguments an action does not use are null.
Validation checks that the chosen action has its own arguments set.
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
    "switch_midline_source": ["classical", "ml"],
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


@dataclass
class Action:
    name: str
    args: dict            # argument name -> JSON schema of its non-null value
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
        return out

    def schema(self):
        props = {
            "action": {"type": "string", "enum": [a.name for a in self.actions]},
            "rationale": {"type": "string"},
        }
        for name, s in self.all_args().items():
            props[name] = {"anyOf": [s, {"type": "null"}]}
        return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}

    def describe(self):
        """Plain-text list of actions for the prompt."""
        lines = []
        for a in self.actions:
            args = ", ".join(a.args) or "no arguments"
            lines.append(f"- {a.name} ({args}){' [ends the task]' if a.terminal else ''}: {a.description}")
        enums = {n: s["enum"] for n, s in self.all_args().items() if "enum" in s}
        for n, vals in enums.items():
            lines.append(f"Allowed {n}: {', '.join(vals)}")
        if self.notes:
            lines.append(self.notes)
        return "\n".join(lines)

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
            if "enum" in s and v not in s["enum"]:
                raise ValueError(f"{name}={v!r} not in the allowed list")
            if s.get("type") == "number" and not isinstance(v, (int, float)):
                raise ValueError(f"{name} must be a number")
            if "minimum" in s and v < s["minimum"] or "maximum" in s and v > s["maximum"]:
                raise ValueError(f"{name}={v} out of range")
            args[name] = v
        if act.name == "apply_remedy":
            allowed = REMEDIES[args["remedy"]]
            setting = out.get("setting")
            if setting not in allowed:
                raise ValueError(f"setting {setting!r} not allowed for {args['remedy']}; allowed: {allowed}")
            args["setting"] = setting
        return act.name, args


_enum = lambda xs: {"type": "string", "enum": list(xs)}  # noqa: E731

DIAGNOSTICIAN = ActionSet("diagnostician", [
    Action("request_info", {"kind": _enum(INFO_KINDS)},
           description="get one more piece of evidence about this task"),
    Action("apply_remedy", {"fault": _enum(FAULTS), "remedy": _enum(REMEDIES)},
           description="re-run the measurement with a remedy; also set `setting` to an allowed value or null"),
    Action("accept", {"confidence": {"type": "number", "minimum": 0, "maximum": 1}}, terminal=True,
           description="report the measurement"),
    Action("decline", {"fault": _enum(FAULTS), "reason": {"type": "string"}}, terminal=True,
           description="do not report the measurement"),
], notes="Allowed setting per remedy: " + "; ".join(
    f"{r}: {', '.join(s or 'null' for s in v)}" for r, v in REMEDIES.items()))
# `setting` is an argument of apply_remedy checked against REMEDIES, so it is
# added to the schema separately.
DIAGNOSTICIAN_SETTING = {"type": "string", "enum": sorted({s for v in REMEDIES.values() for s in v if s})}


def diagnostician_schema():
    s = DIAGNOSTICIAN.schema()
    s["properties"]["setting"] = {"anyOf": [DIAGNOSTICIAN_SETTING, {"type": "null"}]}
    s["required"].append("setting")
    return s


ACTION_SETS = {"diagnostician": DIAGNOSTICIAN}
SCHEMAS = {"diagnostician": diagnostician_schema}
