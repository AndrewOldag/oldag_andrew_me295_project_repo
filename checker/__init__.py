"""Deterministic checks on a measurement record. No LLM calls; nothing from agents/."""
from checker.checks import (CheckResult, rigid_invariance, closure, plane_sections,
                            run_checks, load_thresholds)

__all__ = ["CheckResult", "rigid_invariance", "closure", "plane_sections",
           "run_checks", "load_thresholds"]
