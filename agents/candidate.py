"""Freeze v4 candidate switch (config/models.yaml `candidate`; inbox diag-analysis items 3-4).

Off (null) by default: v3 and v3.1 run unchanged. `v4` turns on, from
docs/proposals/2026-10-25_diagnostician-repair-misses.md:
- C1: the prompt files <agent>_v4.md (fault-to-remedy map), diagnostician and single agent
- C2: per-pair closure-residual spread in stage_log_summary (measure/info.py, stage_log_spread)
- C3 option (a): in labels, a check that cannot be computed after a remedy counts as failing
A driver may turn it on for its own process with use("v4"); the config file stays off.
"""
from agents.launcher import load_config

CANDIDATES = (None, "v4")
_UNSET = object()
_override = _UNSET


def use(name):
    """Set the candidate for this process (None = off). Overrides the config value."""
    global _override
    if name not in CANDIDATES:
        raise ValueError(f"unknown candidate {name!r}; known: {CANDIDATES}")
    _override = name


def reset():
    """Back to the config value."""
    global _override
    _override = _UNSET


def active():
    name = load_config().get("candidate") if _override is _UNSET else _override
    if name not in CANDIDATES:
        raise ValueError(f"config/models.yaml candidate {name!r} not in {CANDIDATES}")
    return name


def v4():
    return active() == "v4"
