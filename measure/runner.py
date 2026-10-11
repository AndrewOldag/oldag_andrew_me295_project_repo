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

    def id(self, moved=False):
        from measure.render import rod_id
        return rod_id(self.case, self.fault, self.seed, moved, self.width_kappa_inv, self.rotation_deg, self.size)

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

    def __init__(self, config=RUNNER_CONFIG, cache=None, couple=False):
        """couple: tracking mode for every run of this runner (a run setting, not a remedy)."""
        self.couple = couple
        cfg = yaml.safe_load(Path(config).read_text())
        self.host, self.work, self.code, self.python = (cfg["host"], cfg["work_dir"],
                                                        cfg["code_dir"], cfg["python"])
        self.cache = Path(cache or ROOT / "staging" / "tracks")
        self.cache.mkdir(parents=True, exist_ok=True)
        self.log = []

    @staticmethod
    def initial_stride(rod):
        from measure.render import image_case
        _, movie = image_case(rod.case, rod.fault, rod.seed, False, rod.width_kappa_inv, rod.rotation_deg,
                              rod.size)
        return movie.stride

    def initial_settings(self, rod):
        """The rod's own analysis frame stride; tracker defaults otherwise."""
        return TrackSettings(stride=self.initial_stride(rod), couple=self.couple)

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

    def _low(self, cmd):
        """Lowest CPU and I/O priority on the shared machine (decisions, 2026-10-11)."""
        return f"nice -n 19 $(command -v ionice >/dev/null && echo ionice -c 3) {cmd}"

    def _load_ok(self):
        """A single job starts only if the 1 min load is at most half the cores."""
        n, l1 = self._ssh("nproc; cut -d' ' -f1 /proc/loadavg").decode().split()
        if float(l1) > 0.5 * int(n):
            raise RuntimeError(f"load {l1} is above half of {n} cores; not starting a job on the shared machine")

    # ---- sweeps (scripts/synth/sweep.py holds the limits for the shared machine)

    @property
    def size_root(self):
        """The space the 10 GB limit applies to: the directory holding the work and code directories."""
        import posixpath
        return posixpath.commonpath([self.work, self.code])

    def sweep_start(self, plan, name, tracks="tracks", max_hours=2.0):
        """Write the plan and start sweep.py detached at lowest priority. Refuses while a sweep runs."""
        self.sync_code()
        st = self.sweep_status()
        if st.get("running"):
            raise RuntimeError(f"a sweep is running ({st.get('plan')}); not starting another")
        q = shlex.quote
        self._ssh(f"mkdir -p {q(self.work)} && cat > {q(self.work)}/plan_{name}.json", stdin=json.dumps(plan).encode())
        self.start_detached(f"cd {q(self.work)} && " + self._low(
            self._py("scripts/synth/sweep.py", ["run", "--plan", f"plan_{name}.json", "--work", ".",
                                                "--tracks", tracks, "--rods", "rods", "--size-root", self.size_root,
                                                "--max-hours", str(max_hours)]))
            + f" > sweep_{name}.log 2>&1")

    def sweep_status(self, name=None):
        out = json.loads(self._ssh(self._py("scripts/synth/sweep.py", ["status", "--work", self.work]))
                         .decode().strip().splitlines()[-1])
        if name:
            q = shlex.quote
            log = self._ssh(f"cd {q(self.work)} && cat sweep_{name}.log 2>/dev/null || true").decode()
            out["log"] = [json.loads(x) for x in log.splitlines() if x.startswith("{")]
        return out

    def sweep_stop(self):
        return json.loads(self._ssh(self._py("scripts/synth/sweep.py", ["stop", "--work", self.work]))
                          .decode().strip().splitlines()[-1])

    def sweep_fetch(self, tracks="tracks", cache=None):
        """Copy finished tracker outputs (not partial ones) and the truth of each rod to a local folder."""
        cache = Path(cache or self.cache)
        cache.mkdir(parents=True, exist_ok=True)
        q = shlex.quote
        data = self._ssh(f"cd {q(self.work)}/{q(tracks)} && ls | grep -E '__.+[.]npz$' | grep -v '[.]part[.]npz$' "
                         f"| tar cf - -T -")
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(cache, filter="data")
        for rid in {f.name.split("__")[0] for f in cache.glob("*__*.npz") if "_moved__" not in f.name}:
            local = cache / f"{rid}_truth.npz"
            if not local.exists():
                self._fetch(f"{self.work}/rods/{rid}_truth.npz", local)
        return cache

    def render(self, rod, moved=False):
        """Render the rod on the tracker machine unless it exists. Returns the rod id."""
        args = ["--out", f"{self.work}/rods"] + rod.options() + (["--moved"] if moved else [])
        cmd = (f"mkdir -p {shlex.quote(self.work)}/rods {shlex.quote(self.work)}/tracks && "
               + self._py("scripts/synth/make_rod.py", args + ["--dry-run"]))
        rid = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])["id"]
        exists = self._ssh(f"test -d {shlex.quote(self.work)}/rods/{rid}.imgdir && echo yes || echo no")
        if exists.decode().strip() != "yes":
            self._load_ok()
            out = json.loads(self._ssh(self._low(self._py("scripts/synth/make_rod.py", args)))
                             .decode().strip().splitlines()[-1])
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
            self._load_ok()
            out = json.loads(self._ssh(self._low(self._py("scripts/remote/qb_track.py", args)))
                             .decode().strip().splitlines()[-1])
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
