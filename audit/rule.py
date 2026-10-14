"""Rule auditor (spec 2026-10-13, Task A2): the baseline, written before any LLM auditor run.

Flags an accepted run if any final check failed, or if any field summary has |robust z| > Z_CUTOFF in its
batch. Every other accepted run is cleared. Declined and not-reported runs are not audited.
Rule: docs/proposals/2026-10-13_auditor-v1.md. Z_CUTOFF is provisional.
"""
Z_CUTOFF = 3.0


def audit(views):
    """views: from audit.view.batch_view (with z). Returns {run_id: {"decision": flag|clear, "reasons": [...]}}."""
    out = {}
    for v in views:
        if v["status"] != "accept":
            continue
        reasons = [f"check_failed:{c['check']}" for c in v["final_checks"] if c["passed"] is False]
        reasons += [f"summary_outlier:{k}" for k, z in v["z"].items() if z is not None and abs(z) > Z_CUTOFF]
        out[v["run_id"]] = {"decision": "flag" if reasons else "clear", "reasons": reasons}
    return out
