"""Error of a measurement against the truth of a synthetic rod. Used for scoring, never shown to agents."""
import warnings

import numpy as np

from measure.record import PER_S_TO_PCT_PER_H


def _wmean(a, min_cov=0.5):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m = np.nanmean(a, axis=0)
    m[np.mean(np.isfinite(a), axis=0) < min_cov] = np.nan
    return m


def truth_error(rec, truth):
    """RMS and max error (%/h) of the window-mean centre strain rate and of the flank difference."""
    f = rec.fields
    s = f["s_grid"]
    out = {}
    for name, meas, tru in (("regr", f["regr_mid"], truth["regr_mid"]),
                            ("flank_difference", f["regr_plus"] - f["regr_minus"],
                             truth["regr_plus"] - truth["regr_minus"])):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            t = np.interp(s, truth["s_grid"], np.nanmean(tru, axis=0), right=np.nan)
        e = (_wmean(meas) - t) * PER_S_TO_PCT_PER_H
        out[f"{name}_rms_pct_per_h"] = round(float(np.sqrt(np.nanmean(e ** 2))), 3)
        out[f"{name}_max_pct_per_h"] = round(float(np.nanmax(np.abs(e))), 3)
        out[f"{name}_covered_um"] = round(float(np.nanmax(s[np.isfinite(e)]) * rec.pixel_um))
    return out


def truth_summary(truth, pixel_um):
    regr = np.nanmean(truth["regr_mid"], axis=0) * PER_S_TO_PCT_PER_H
    diff = np.nanmean(truth["regr_plus"] - truth["regr_minus"], axis=0) * PER_S_TO_PCT_PER_H
    return {"peak_regr_pct_per_h": round(float(np.nanmax(regr)), 1),
            "peak_at_um": round(float(truth["s_grid"][np.nanargmax(regr)] * pixel_um)),
            "largest_flank_difference_pct_per_h": round(float(diff[np.nanargmax(np.abs(diff))]), 2)}


# ---------------------------------------------------------------- outcomes (spec 2026-10-10, repair criteria)

OUTCOME_CATEGORIES = ("good_report", "false_accept", "correct_decline", "unnecessary_decline", "not_reported")


def measurement_good(error, tolerance, width_free=False):
    """Within tolerance: centre REGR RMS error, and flank-difference RMS error unless the width-free ratio is reported."""
    ok = error["regr_rms_pct_per_h"] <= tolerance["regr_rms_pct_per_h"]
    if not width_free:
        ok = ok and error["flank_difference_rms_pct_per_h"] <= tolerance["flank_difference_rms_pct_per_h"]
    return bool(ok)


def checks_pass(checks):
    """Every check that was applied passed (a skipped check has passed None and does not count)."""
    applied = [c for c in checks if c.passed is not None]
    return bool(applied) and all(c.passed for c in applied)


def outcome_category(status, label, good):
    """status: accept, decline, step_limit or error. label: repairable or not repairable. good: the reported measurement is good."""
    if status == "accept":
        return "good_report" if good else "false_accept"
    if status == "decline":
        return "correct_decline" if label == "not repairable" else "unnecessary_decline"
    return "not_reported"


def diagnosis_correct(named_fault, injected_fault):
    """Fault named in the last apply_remedy or decline, against the injected one."""
    return named_fault == injected_fault


def label_rod(states):
    """Label from a no-agent sweep. states: list of dicts with `sequence` (remedy steps, at most two),
    `checks_pass` and `good`. Returns (label, sequence of the first repairing state or None)."""
    for s in sorted(states, key=lambda s: len(s["sequence"])):
        if len(s["sequence"]) <= 2 and s["checks_pass"] and s["good"]:
            return "repairable", s["sequence"]
    return "not repairable", None
