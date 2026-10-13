"""Real executors for the diagnostician's tools: request_info and apply_remedy.

A Slice holds one rod, one runner and the current measurement. request_info
answers from the current record and its check results (measure/info.py).
apply_remedy changes the settings (measure/remedies.py), re-runs the
measurement through the runner and re-checks it; the re-run becomes the
current measurement. The result shows each check's value before and after.
Roll back (spec 2026-10-10, repair criteria, part D): if a remedy makes no
failing check pass and lowers no failing check by at least a quarter, the
settings and measurement from before it are restored and the result says so.
The step still counts. The agent never sees the rod's name, fault or truth.
"""
import math

from agents.actions import REMEDIES
from checker import run_checks, load_thresholds
from measure import info
from measure.remedies import NotAvailable, apply_remedy


ROLL_BACK_FRACTION = 0.75      # a failing check must fall to at most 3/4 of its value to count as lowered


def _before_after(before, after):
    b = {c.check: c for c in before}
    return {c.check: {"before": None if b[c.check].passed is None else round(b[c.check].value, 3),
                      "after": None if c.passed is None else round(c.value, 3),
                      "threshold": c.threshold, "unit": c.unit} for c in after}


def no_progress(before, after):
    """True if the measurement before had a failing check and the remedy made none of them pass (or no
    longer apply, as plane sections under the width-free ratio) and lowered none by at least a quarter.
    A check that can no longer be computed (no coverage) is not resolved."""
    failing = [c for c in before if c.passed is False]
    if not failing:
        return False
    a = {c.check: c for c in after}
    for c in failing:
        n = a[c.check]
        if n.passed is True or (n.passed is None and n.detail.startswith("skipped")):
            return False
        if math.isfinite(n.value) and math.isfinite(c.value) and n.value <= ROLL_BACK_FRACTION * c.value:
            return False
    return True


def _summary(checks):
    return {"failed_checks": [c.check for c in checks if c.passed is False],
            "passed_checks": [c.check for c in checks if c.passed is True],
            "not_run": [c.check for c in checks if c.passed is None],
            "check_values": {c.check: {"value": round(c.value, 3), "threshold": c.threshold, "unit": c.unit}
                             for c in checks}}


class Slice:
    def __init__(self, runner, rod, label="rod-1", thresholds=None):
        self.runner, self.rod, self.label = runner, rod, label
        self.thresholds = thresholds or load_thresholds()
        self.runs = []                       # (settings, measurement, checks, change)
        self._measure(runner.initial_settings(rod), "initial run")
        self.base_disk_radius = int(self.current.record.settings.get("disk_radius") or 15)

    def _measure(self, settings, change):
        m = self.runner.measure(self.rod, settings)
        skip = ("plane_sections",) if settings.width_free else ()
        checks = run_checks(m.record, m.moved, self.thresholds, skip)
        self.runs.append((settings, m, checks, change))

    @property
    def current(self):
        return self.runs[-1][1]

    @property
    def checks(self):
        return self.runs[-1][2]

    def task(self):
        s = self.current.record.settings
        return {"task": f"{self.label}, one window of {self.current.record.n_frames} frames",
                **_summary(self.checks),
                "tracking": {"frame_stride": s.get("stride"), "disk_radius_px": s.get("disk_radius"),
                             "pixel_um": self.current.record.pixel_um}}

    def request_info(self, args, task):
        out = info.request_info(args["kind"], self.current.record, self.checks)
        if args["kind"] == "velocity_profile" and self.runs[-1][0].width_free:
            out.update(info.width_free_ratio(self.current.record))
        return out

    def apply_remedy(self, args, task):
        settings, before_m, before, _ = self.runs[-1]
        try:
            new, change = apply_remedy(settings, args["remedy"], args.get("setting"), self.base_disk_radius,
                                       self.current.record)
        except NotAvailable as e:
            return {"rechecked": False, "error": f"remedy not available: {e}"}
        self._measure(new, change)
        after = self.checks
        out = {"rechecked": True, "change": change, **_summary(after),
               "check_values": _before_after(before, after)}
        if no_progress(before, after):
            self.runs.append((settings, before_m, before, f"rolled back: {change}"))
            out.update({k: v for k, v in _summary(before).items() if k != "check_values"}, rolled_back=True,
                       note="the remedy made no failing check pass and lowered none by a quarter; "
                            "the settings and measurement from before it are restored. The step counts")
        if not self.settings_left(args["remedy"]):
            out["settings_left"] = f"no further setting: {args['remedy']} cannot be applied again or at another setting"
        return out

    def settings_left(self, remedy):
        """Settings of `remedy` (REMEDIES) that can still be applied to the current settings (P3, 2026-10-12)."""
        left = []
        for s in REMEDIES[remedy]:
            try:
                apply_remedy(self.runs[-1][0], remedy, s, self.base_disk_radius, self.current.record)
                left.append(s)
            except NotAvailable:
                pass
        return left

    def executors(self):
        return {"request_info": self.request_info, "apply_remedy": self.apply_remedy}
