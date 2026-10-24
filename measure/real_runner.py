"""Measurement runner for one window of a real movie: `RealRunner().measure(window, settings)`.

Same interface as the synthetic runners (measure/runner.py), so the diagnostician's Slice
(agents/executors.py) works on real windows unchanged. It runs scripts/remote/qb_track.py for the
window on the compute host with the window's midline file (net midline, decisions 2026-10-23) and the
remedy settings, then fetches the output. Outputs are cached locally by window and settings tag.

Host, folders, Python, tracker code and the per-window movie and midline paths come from
private/real_runner.yaml (git-ignored; template config/real_runner.example.yaml).

Limits on the host, checked before every tracker run: 1 min load at most half the cores; fewer than
2 jobs of this account already running; at least `min_free_gb` free on the work disk (workstation rule,
2026-10-23). Single-thread tracker, nice 19.

No rigidly moved copy exists for real movies yet: `moved` is None, so rigid invariance is "not run".
"""
from dataclasses import dataclass, replace
import io
import json
from pathlib import Path
import shlex
import subprocess
import tarfile

import yaml

from measure.record import from_tracker_npz
from measure.remedies import TrackSettings
from measure.runner import Measurement

ROOT = Path(__file__).resolve().parents[1]
REAL_CONFIG = ROOT / "private" / "real_runner.yaml"
JOB_PATTERN = "qb_track.py|batch_midlines.py|sweep.py run"


@dataclass(frozen=True)
class RealWindow:
    root_id: str
    from_h: float
    to_h: float

    def id(self):
        return f"{self.root_id}__w{self.from_h:g}-{self.to_h:g}"


class HostBusy(RuntimeError):
    pass


class RealRunner:
    form = "real_window"

    def __init__(self, config=REAL_CONFIG, cache=None, track_length=400.0):
        cfg = yaml.safe_load(Path(config).read_text())
        self.host, self.work, self.code, self.tracker, self.python = (
            cfg["host"], cfg["work_dir"], cfg["code_dir"], cfg["tracker_code"], cfg["python"])
        self.min_free_gb = float(cfg.get("min_free_gb", 21))
        self.windows = cfg["windows"]                 # window id -> {imgdir, midline}
        self.track_length = float(track_length)
        self.cache = Path(cache or ROOT / "staging" / "tracks_real")
        self.cache.mkdir(parents=True, exist_ok=True)
        self.log = []

    def initial_settings(self, window):
        return TrackSettings(stride=1)                 # every frame; uncoupled (the frozen mode)

    def _ssh(self, cmd, stdin=None):
        p = subprocess.run(["ssh", "-o", "BatchMode=yes", self.host, cmd], input=stdin, capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"host command failed ({p.returncode}): "
                               f"{p.stderr.decode(errors='replace').strip().splitlines()[-1:]}")
        return p.stdout

    def sync_code(self):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for d in ("measure", "scripts/remote"):
                tar.add(ROOT / d, arcname=d, filter=lambda ti: None if "__pycache__" in ti.name else ti)
        q = shlex.quote
        self._ssh(f"mkdir -p {q(self.code)} && cd {q(self.code)} && tar xf -", stdin=buf.getvalue())

    def host_state(self):
        q = shlex.quote
        out = self._ssh(f"nproc; cut -d' ' -f1 /proc/loadavg; pgrep -u $(id -u) -fc {q(JOB_PATTERN)} || true; "
                        f"df -BG --output=avail {q(self.work)} | tail -1").decode().split()
        return {"cores": int(out[0]), "load1": float(out[1]), "own_jobs": int(out[2]),
                "free_gb": float(out[3].rstrip("G"))}

    def check_host(self):
        s = self.host_state()
        if s["load1"] > 0.5 * s["cores"]:
            raise HostBusy(f"load {s['load1']} above half of {s['cores']} cores")
        if s["own_jobs"] >= 2:
            raise HostBusy(f"{s['own_jobs']} jobs of this account running (limit 2)")
        if s["free_gb"] < self.min_free_gb:
            raise HostBusy(f"{s['free_gb']} GB free, below {self.min_free_gb} GB")
        return s

    def track(self, window, settings):
        settings = replace(settings, width_free=False)
        w = self.windows[window.id()]
        name = f"{window.id()}__{settings.tag()}__L{self.track_length:g}.npz"
        local = self.cache / name
        if not local.exists():
            before = self.check_host()
            q = shlex.quote
            args = (["--imgdir", w["imgdir"], "--midline", w["midline"], "--out", f"{self.work}/tracks/{name}",
                     "--movie", "real", "--from-h", f"{window.from_h:g}", "--to-h", f"{window.to_h:g}",
                     "--track-length", f"{self.track_length:g}"] + settings.args())
            cmd = (f"mkdir -p {q(self.work)}/tracks && cd {q(self.code)} && "
                   f"OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 "
                   f"PYTHONPATH={q(self.tracker)}:{q(self.code)} nice -n 19 {q(self.python)} "
                   f"scripts/remote/qb_track.py " + " ".join(q(a) for a in args))
            out = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])
            local.write_bytes(self._ssh(f"cat {q(self.work)}/tracks/{q(name)}"))
            after = self.host_state()
            self.log.append({"track": name, "run_s": out.get("run_s"), "frames": out.get("frames"),
                             "load1_before": before["load1"], "free_gb_before": before["free_gb"],
                             "free_gb_after": after["free_gb"]})
        return local

    def measure(self, window, settings):
        rec = from_tracker_npz(self.track(window, settings), root_id=window.id())
        return Measurement(rec, None, settings, {})
