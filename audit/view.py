"""Auditor view (spec 2026-10-13, Task A1). Deterministic code, no LLM.

Per run, the record the auditor sees: status, final checks, remedies kept, roll backs, steps, final settings,
and field summaries from the final measurement record. Built from an allow-list of summary keys; nothing else
of the run summary is read; a real-movie run also shows its root's condition. Withheld: fault, size, seed, label, truth, error_before, error_after, category,
correct, good, named fault, traces, the method and the run's file name. Runs get opaque ids.

Batch statistics: per field summary, batch median, MAD and robust z per run, z = (x - median) / (1.4826 MAD).
All runs of the batch with a value count. MAD 0: z = (x - median) / (1.2533 mean absolute deviation), the usual
fallback (Iglewicz and Hoaglin); both 0: z = 0. Fewer than 3 values: z is null.
"""
import random
import warnings

import numpy as np

from measure import info
from measure.record import PER_S_TO_PCT_PER_H

GROWTH_ZONE_FRACTION = 0.10      # growth zone: centre strain rate above 10 % of its peak
MIN_COVERAGE = 0.5               # window mean only where at least half the frame pairs are finite (as measure/info.py)
MAD_SCALE = 1.4826
MEAN_AD_SCALE = 1.2533           # used when MAD is 0
SUMMARIES = ("centre_peak_regr_pct_per_h", "centre_peak_at_um", "growth_zone_length_um",
             "flank_difference_max_pct_per_h", "flank_difference_at_um", "width_free_ratio_max")
STATUS = {"accept": "accept", "decline": "decline"}          # step_limit, error -> not_reported
VIEW_KEYS = ("run_id", "status", "final_checks", "remedies_kept", "roll_backs", "steps", "final_settings",
             "summaries")


def _wmean(a):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m = np.nanmean(a, axis=0)
    m[np.mean(np.isfinite(a), axis=0) < MIN_COVERAGE] = np.nan
    return m


def _r(x, n):
    return None if x is None or not np.isfinite(x) else round(float(x), n)


def field_summaries(rec, width_free=False):
    """Centre REGR peak and position, growth-zone length, largest flank difference and position, and the
    largest width-free ratio and position when the width-free ratio is used. Window means, %/h and um."""
    f = rec.fields
    s_um = f["s_grid"] * rec.pixel_um
    regr = _wmean(f["regr_mid"]) * PER_S_TO_PCT_PER_H
    out = dict.fromkeys(SUMMARIES)
    out["width_free_ratio_at_um"] = None
    if np.isfinite(regr).any():
        i = int(np.nanargmax(regr))
        peak = regr[i]
        out["centre_peak_regr_pct_per_h"], out["centre_peak_at_um"] = _r(peak, 2), _r(s_um[i], 0)
        above = np.isfinite(regr) & (regr > GROWTH_ZONE_FRACTION * peak) if peak > 0 else np.zeros_like(regr, bool)
        if above[i]:
            a = b = i                                    # contiguous run of grid points around the peak
            while a > 0 and above[a - 1]:
                a -= 1
            while b < len(above) - 1 and above[b + 1]:
                b += 1
            out["growth_zone_length_um"] = _r(s_um[b] - s_um[a], 0)
    diff = _wmean(f["regr_plus"] - f["regr_minus"]) * PER_S_TO_PCT_PER_H
    if np.isfinite(diff).any():
        j = int(np.nanargmax(np.abs(diff)))
        out["flank_difference_max_pct_per_h"], out["flank_difference_at_um"] = _r(diff[j], 2), _r(s_um[j], 0)
    if width_free:
        w = info.width_free_ratio(rec)
        vals = [(v, s) for v, s in zip(w["width_free_ratio"], w["width_free_ratio_s_um"]) if v is not None]
        if vals:
            v, s = max(vals, key=lambda x: abs(x[0]))
            out["width_free_ratio_max"], out["width_free_ratio_at_um"] = round(v, 3), s
    return out


def remedies_kept(changes):
    """Remedy changes not undone: each 'rolled back: X' removes the X before it."""
    kept = []
    for c in changes:
        if c.startswith("rolled back: "):
            undone = c[len("rolled back: "):]
            if kept and kept[-1] == undone:
                kept.pop()
        else:
            kept.append(c)
    return kept


def _check(c):
    v = c.get("value")
    out = {"check": c["check"], "value": None if v is None or not np.isfinite(v) else round(float(v), 3),
           "threshold": c.get("threshold"), "unit": c.get("unit"), "passed": c.get("passed")}
    if str(c.get("detail", "")).startswith("reported, not gating"):
        out["gating"] = False             # real-movie profile: computed and reported, not a pass/fail gate
    return out


def run_view(run_id, summary, record):
    """The auditor's record of one run. summary: the run's _summary.json; record: its final measurement record.
    Reads only outcome.status, outcome.steps, remedies, roll_backs, final_settings and final_checks."""
    o = summary["outcome"]
    settings = summary["final_settings"]
    return {"run_id": run_id,
            "status": STATUS.get(o["status"], "not_reported"),
            "final_checks": [_check(c) for c in summary["final_checks"]],
            "remedies_kept": remedies_kept(summary["remedies"]),
            "roll_backs": int(summary["roll_backs"]),
            "steps": int(o["steps"]),
            "final_settings": {k: settings.get(k) for k in ("stride", "disk_radius", "register",
                                                            "register_from_px", "midline_smooth", "band_mask",
                                                            "width_free")},
            "summaries": field_summaries(record, bool(settings.get("width_free"))),
            **({"condition": summary["condition"]} if summary.get("condition") else {})}   # real movies only


def robust_z(values):
    """Median, MAD and robust z for a list with None for missing values."""
    x = np.array([np.nan if v is None else v for v in values], float)
    ok = np.isfinite(x)
    if ok.sum() < 3:
        return {"median": None, "mad": None, "z": [None] * len(values)}
    med = float(np.median(x[ok]))
    mad = float(np.median(np.abs(x[ok] - med)))
    scale = MAD_SCALE * mad if mad > 0 else MEAN_AD_SCALE * float(np.mean(np.abs(x[ok] - med)))
    z = [None if not ok[k] else (0.0 if scale == 0 else round(float((x[k] - med) / scale), 2))
         for k in range(len(x))]
    return {"median": round(med, 3), "mad": round(mad, 3), "z": z}


def batch_stats(views):
    """Per summary: batch median, MAD; per run: robust z. Adds `z` to each view's copy."""
    stats = {k: robust_z([v["summaries"][k] for v in views]) for k in SUMMARIES}
    out = []
    for i, v in enumerate(views):
        v = dict(v, z={k: stats[k]["z"][i] for k in SUMMARIES})
        out.append(v)
    return out, {k: {"median": s["median"], "mad": s["mad"]} for k, s in stats.items()}


def opaque_ids(n, key):
    """Run ids r01..rNN in an order shuffled by a fixed key, so that the id does not show the fault order."""
    order = list(range(n))
    random.Random(key).shuffle(order)
    ids = [None] * n
    for pos, k in enumerate(order):
        ids[k] = f"r{pos + 1:02d}"
    return ids


def batch_view(summaries, records, key):
    """summaries, records: per run, in any order. Returns (views sorted by id, batch stats, ids in input order)."""
    ids = opaque_ids(len(summaries), key)
    views = [run_view(i, s, r) for i, s, r in zip(ids, summaries, records)]
    views, stats = batch_stats(views)
    return sorted(views, key=lambda v: v["run_id"]), stats, ids


def batch_table(views, stats):
    """Compact table of the batch for the auditor: one row per run."""
    rows, any_not_gating = [], False
    for v in views:
        checks = {}
        for c in v["final_checks"]:
            not_gating = c.get("gating") is False
            any_not_gating |= not_gating
            checks[c["check"]] = [c["value"], c["threshold"], "not gating" if not_gating else c["passed"]]
        rows.append({"run_id": v["run_id"], **({"condition": v["condition"]} if "condition" in v else {}),
                     "status": v["status"], "checks": checks,
                     "steps": v["steps"], "remedies_kept": len(v["remedies_kept"]), "roll_backs": v["roll_backs"],
                     "width_free": v["final_settings"]["width_free"],
                     "summaries": {k: [v["summaries"][k], v["z"][k]] for k in SUMMARIES}})
    note = "check: [value, threshold, passed]; passed null = not run"
    if any_not_gating:                    # only real-movie batches; synthetic tables are unchanged
        note += "; passed 'not gating' = computed and reported, not a pass/fail gate (real-movie profile)"
    return {"columns": {"checks": note, "summaries": "summary: [value, robust z in this batch]"},
            "batch_median_mad": stats, "runs": rows}
