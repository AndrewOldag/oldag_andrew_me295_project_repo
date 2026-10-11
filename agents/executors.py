"""Real executors for the diagnostician's tools: request_info and apply_remedy.

A Slice holds one rod, one runner and the current measurement. request_info
answers from the current record and its check results (measure/info.py).
apply_remedy changes the settings (measure/remedies.py), re-runs the
measurement through the runner and re-checks it; the re-run becomes the
current measurement. The agent never sees the rod's name, fault or truth.
"""
from checker import run_checks, load_thresholds
from measure import info
from measure.remedies import NotAvailable, apply_remedy


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
        settings = self.runs[-1][0]
        try:
            new, change = apply_remedy(settings, args["remedy"], args.get("setting"), self.base_disk_radius,
                                       self.current.record)
        except NotAvailable as e:
            return {"rechecked": False, "error": f"remedy not available: {e}"}
        self._measure(new, change)
        return {"rechecked": True, "change": change, **_summary(self.checks)}

    def executors(self):
        return {"request_info": self.request_info, "apply_remedy": self.apply_remedy}
