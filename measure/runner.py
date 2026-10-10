"""One interface for producing a measurement: `runner.measure(rod, settings)`.

Two forms:
- FieldRunner: in process, for field-level rods. No images and no tracker;
  only settings that act on the record (frame stride, midline smoothing)
  change anything, and the result says which settings had no effect
- RemoteRunner: renders an image-level rod and runs the tracker as a job on
  the machine that has it (scripts/remote/qb_track.py), then fetches the
  output. Host, paths and Python come from private/runner.yaml (git-ignored;
  template config/runner.example.yaml)

Both return a Measurement: the record, the rigidly moved record for the
invariance check, and the settings used.
"""
from dataclasses import dataclass, field, replace
import json
from pathlib import Path
import shlex
import subprocess
import tarfile
import io
from typing import Optional

import numpy as np
import yaml

from measure.record import MeasurementRecord, from_tracker_npz, rigid_moved
from measure.remedies import TrackSettings
from measure import preprocess

ROOT = Path(__file__).resolve().parents[1]
RUNNER_CONFIG = ROOT / "private" / "runner.yaml"
MOVED = (np.deg2rad(0.1) / 90.0, (0.5 / 90.0, 0.3 / 90.0))   # rotation rad/s, translation px/s


@dataclass(frozen=True)
class Rod:
    case: str = "growth_zone"
    fault: Optional[str] = None
    seed: int = 0
    width_kappa_inv: Optional[float] = None
    rotation_deg: Optional[float] = None
    size: Optional[str] = None

    def options(self):
        o = ["--case", self.case, "--seed", str(self.seed)]
        if self.fault:
            o += ["--fault", self.fault]
        if self.width_kappa_inv:
            o += ["--width-kappa-inv", str(self.width_kappa_inv)]
        if self.rotation_deg:
            o += ["--rotation-deg", str(self.rotation_deg)]
        if self.size:
            o += ["--size", str(self.size)]
        return o


@dataclass
class Measurement:
    record: MeasurementRecord
    moved: Optional[MeasurementRecord]
    settings: TrackSettings
    truth: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)


class FieldRunner:
    form = "in_process"

    def initial_settings(self, rod):
        return TrackSettings()

    def measure(self, rod, settings):
        from measure.rod import field_cases, make_record
        spec = next(s for s in field_cases() if s.name == rod.case)
        rec = make_record(spec)
        truth = rec.truth
        notes = []
        if settings.stride > 1:
            k = np.arange(0, rec.n_frames, settings.stride)
            rec = replace(rec, frame_times_s=rec.frame_times_s[k], stage_px=rec.stage_px[k],
                          centre=rec.centre[k], plus=rec.plus[k], minus=rec.minus[k],
                          midline=rec.midline[k], _fields=None)
        if settings.midline_smooth:
            rec = replace(rec, midline=preprocess.smooth_midline(rec.midline, settings.midline_smooth),
                          _fields=None)
        for name in ("disk_radius", "register", "band_mask"):
            if getattr(settings, name) not in (None, False):
                notes.append(f"{name} has no effect on a field-level rod")
        rec.settings = dict(rec.settings, **settings.to_dict())
        return Measurement(rec, rigid_moved(rec, *MOVED), settings, truth, notes)


class RemoteRunner:
    form = "remote_job"

    def __init__(self, config=RUNNER_CONFIG, cache=None):
        cfg = yaml.safe_load(Path(config).read_text())
        self.host, self.work, self.code, self.python = (cfg["host"], cfg["work_dir"],
                                                        cfg["code_dir"], cfg["python"])
        self.cache = Path(cache or ROOT / "staging" / "tracks")
        self.cache.mkdir(parents=True, exist_ok=True)
        self.log = []

    def initial_settings(self, rod):
        """The rod's own analysis frame stride; tracker defaults otherwise."""
        from measure.render import image_case
        _, movie = image_case(rod.case, rod.fault, rod.seed, False, rod.width_kappa_inv, rod.rotation_deg,
                              rod.size)
        return TrackSettings(stride=movie.stride)

    def _ssh(self, cmd, stdin=None):
        p = subprocess.run(["ssh", "-o", "BatchMode=yes", self.host, cmd], input=stdin,
                           capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"remote command failed ({p.returncode}): "
                               f"{p.stderr.decode(errors='replace').strip().splitlines()[-1:]}")
        return p.stdout

    def start_detached(self, cmd):
        """Start a long job remotely and return at once (ssh -f; the job is detached with setsid)."""
        subprocess.run(["ssh", "-o", "BatchMode=yes", "-f", self.host,
                        f"setsid nohup sh -c {shlex.quote(cmd)} > /dev/null 2>&1 < /dev/null &"],
                       check=True, capture_output=True)

    def sync_code(self):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for d in ("measure", "scripts/synth", "scripts/remote"):
                tar.add(ROOT / d, arcname=d,
                        filter=lambda ti: None if "__pycache__" in ti.name else ti)
        self._ssh(f"mkdir -p {shlex.quote(self.code)} && cd {shlex.quote(self.code)} && tar xf -",
                  stdin=buf.getvalue())

    def _py(self, script, args):
        return " ".join([self.python, shlex.quote(f"{self.code}/{script}")] + [shlex.quote(a) for a in args])

    def render(self, rod, moved=False):
        """Render the rod on the tracker machine unless it exists. Returns the rod id."""
        args = ["--out", f"{self.work}/rods"] + rod.options() + (["--moved"] if moved else [])
        cmd = (f"mkdir -p {shlex.quote(self.work)}/rods {shlex.quote(self.work)}/tracks && "
               + self._py("scripts/synth/make_rod.py", args + ["--dry-run"]))
        rid = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])["id"]
        exists = self._ssh(f"test -d {shlex.quote(self.work)}/rods/{rid}.imgdir && echo yes || echo no")
        if exists.decode().strip() != "yes":
            out = json.loads(self._ssh(self._py("scripts/synth/make_rod.py", args)).decode().strip().splitlines()[-1])
            self.log.append({"render": out})
        return rid

    def _fetch(self, remote, local):
        local.write_bytes(self._ssh(f"cat {shlex.quote(remote)}"))
        return local

    def track(self, rid, settings):
        settings = replace(settings, width_free=False)      # not a tracker setting
        name = f"{rid}__{settings.tag()}.npz"
        local = self.cache / name
        if not local.exists():
            args = ["--imgdir", f"{self.work}/rods/{rid}.imgdir",
                    "--midline", f"{self.work}/rods/{rid}_midline.npz",
                    "--out", f"{self.work}/tracks/{name}"] + settings.args()
            out = json.loads(self._ssh(self._py("scripts/remote/qb_track.py", args)).decode().strip().splitlines()[-1])
            out["out"] = Path(out.get("out", name)).name        # no remote paths in logs
            self.log.append({"track": out})
            self._fetch(f"{self.work}/tracks/{name}", local)
        return local

    def truth(self, rid):
        local = self.cache / f"{rid}_truth.npz"
        if not local.exists():
            self._fetch(f"{self.work}/rods/{rid}_truth.npz", local)
        with np.load(local) as z:
            return {k: z[k] for k in z.files}

    def measure(self, rod, settings):
        rid = self.render(rod)
        rid_moved = self.render(rod, moved=True)
        rec = from_tracker_npz(self.track(rid, settings))
        moved = from_tracker_npz(self.track(rid_moved, settings))
        return Measurement(rec, moved, settings, self.truth(rid))
