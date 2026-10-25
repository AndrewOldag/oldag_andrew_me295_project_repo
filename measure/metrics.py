"""Freeze v3 metrics (docs/proposals/2026-10-23_freeze-v3.md, section 3). Scoring only; never shown to agents.

A run is a dict with at least: method, rod (id), cls (CLASSES), repeat (int), status (accept, decline,
step_limit or error), category (CATEGORIES). Optional: remedies_kept (int), fault_correct (bool or None,
None on clean rods).
"""
from collections import Counter, defaultdict

CLASSES = ("accept_clean", "accept_repaired", "decline")
ACCEPT_CLASSES = ("accept_clean", "accept_repaired")
CATEGORIES = ("good_report", "false_accept", "correct_decline", "unnecessary_decline", "not_reported",
              "accept_on_decline")
CORRECT = {"accept_clean": "good_report", "accept_repaired": "good_report", "decline": "correct_decline"}


def category(status, cls, good):
    """Outcome category of one run. A good report on a decline rod is accept_on_decline: neither correct nor
    a false accept (v2 rule, named in v3)."""
    if status == "accept":
        if not good:
            return "false_accept"
        return "accept_on_decline" if cls == "decline" else "good_report"
    if status == "decline":
        return "correct_decline" if cls == "decline" else "unnecessary_decline"
    return "not_reported"


def correct(run):
    return run["category"] == CORRECT[run["cls"]]


def _ratio(a, b):
    return None if b == 0 else a / b


def summarize(runs):
    """Metrics over one set of runs (one method, one repeat). Fractions are None where undefined."""
    by = defaultdict(list)
    for r in runs:
        by[r["cls"]].append(r)
    n = len(runs)
    acc = {c: _ratio(sum(correct(r) for r in by[c]), len(by[c])) for c in CLASSES}
    present = [a for c, a in acc.items() if by[c]]
    cats = Counter(r["category"] for r in runs)
    accepts = sum(r["status"] == "accept" for r in runs)
    declines = sum(r["status"] == "decline" for r in runs)
    out = {
        "runs": n, "runs_per_class": {c: len(by[c]) for c in CLASSES},
        "correct": sum(correct(r) for r in runs),
        "accuracy_per_class": acc,
        "balanced_accuracy": _ratio(sum(present), len(present)) if present else None,
        "overall_accuracy": _ratio(sum(correct(r) for r in runs), n),
        "false_accepts": cats["false_accept"],
        "false_accept_rate": _ratio(cats["false_accept"], accepts),
        "coverage": _ratio(accepts, n),
        "abstention_precision": _ratio(cats["correct_decline"], declines),
        "abstention_recall": _ratio(cats["correct_decline"], len(by["decline"])),
        "unnecessary_decline_rate": {c: _ratio(sum(r["category"] == "unnecessary_decline" for r in by[c]),
                                               len(by[c])) for c in ACCEPT_CLASSES},
        "not_reported_per_class": {c: sum(r["category"] == "not_reported" for r in by[c]) for c in CLASSES},
        "categories": {k: cats[k] for k in CATEGORIES},
        "remedies_kept_per_class": {c: sum(r.get("remedies_kept", 0) for r in by[c]) for c in CLASSES},
        "runs_with_remedy_kept_per_class": {c: sum(r.get("remedies_kept", 0) > 0 for r in by[c]) for c in CLASSES},
    }
    fc = [r["fault_correct"] for r in runs if r.get("fault_correct") is not None]
    out["fault_named_correct"] = sum(bool(x) for x in fc)
    out["fault_rods"] = len(fc)
    return out


def over_repeats(runs):
    """summarize() per repeat, then mean and (min, max) over repeats of every scalar and per-class value."""
    reps = sorted({r["repeat"] for r in runs})
    per = [summarize([r for r in runs if r["repeat"] == k]) for k in reps]

    def agg(vals):
        v = [x for x in vals if x is not None]
        return {"mean": sum(v) / len(v), "min": min(v), "max": max(v)} if v else None

    out = {"repeats": reps, "per_repeat": per}
    for key, val in per[0].items():
        if isinstance(val, dict):
            out[key] = {k: agg([p[key][k] for p in per]) for k in val}
        else:
            out[key] = agg([p[key] for p in per])
    return out


def fleiss_kappa(counts):
    """Fleiss' kappa. counts: one list of category counts per subject, the same number of raters each.
    None if undefined (one category only, or fewer than 2 raters)."""
    counts = [list(c) for c in counts]
    if not counts:
        return None
    n = sum(counts[0])
    if n < 2 or any(sum(c) != n for c in counts):
        raise ValueError("every subject needs the same number of ratings, at least 2")
    N, k = len(counts), len(counts[0])
    p_bar = sum((sum(x * x for x in c) - n) / (n * (n - 1)) for c in counts) / N
    p_j = [sum(c[j] for c in counts) / (N * n) for j in range(k)]
    pe = sum(p * p for p in p_j)
    return None if pe >= 1.0 else (p_bar - pe) / (1.0 - pe)


def agreement(runs):
    """Repeated-run agreement for one method: unanimity rate (rods whose repeats all give the same category)
    overall and per class, and Fleiss' kappa over CATEGORIES. Rods with fewer repeats than the most are left out
    and counted."""
    by_rod = defaultdict(list)
    for r in runs:
        by_rod[r["rod"]].append(r)
    n_rep = max(len(v) for v in by_rod.values())
    full = {k: v for k, v in by_rod.items() if len(v) == n_rep}
    unan = {k: len({r["category"] for r in v}) == 1 for k, v in full.items()}
    cls = {k: v[0]["cls"] for k, v in full.items()}
    counts = [[sum(r["category"] == c for r in v) for c in CATEGORIES] for v in full.values()]
    return {"repeats": n_rep, "rods": len(full), "rods_left_out": len(by_rod) - len(full),
            "unanimous": sum(unan.values()), "unanimity_rate": _ratio(sum(unan.values()), len(full)),
            "unanimity_rate_per_class": {c: _ratio(sum(u for k, u in unan.items() if cls[k] == c),
                                                   sum(cls[k] == c for k in unan)) for c in CLASSES},
            "fleiss_kappa": fleiss_kappa(counts) if n_rep >= 2 else None,
            "category_counts": {c: sum(x[i] for x in counts) for i, c in enumerate(CATEGORIES)}}


def reference_runs(rods, policy, good_unremedied=None):
    """Runs of a reference policy. rods: [(rod id, cls)]. policy: all_decline or all_accept (accept the
    unremedied measurement; good_unremedied: {rod id: bool})."""
    out = []
    for rid, cls in rods:
        if policy == "all_decline":
            status, good = "decline", False
        elif policy == "all_accept":
            status, good = "accept", bool(good_unremedied[rid])
        else:
            raise ValueError(policy)
        out.append({"method": policy, "rod": rid, "cls": cls, "repeat": 0, "status": status,
                    "category": category(status, cls, good), "remedies_kept": 0})
    return out
