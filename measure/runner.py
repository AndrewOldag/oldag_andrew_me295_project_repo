"""One interface for producing a measurement: `runner.measure(rod, settings)`.

Two forms:
- FieldRunner: in process, for field-level rods. No images and no tracker;
  only settings that act on the record (frame stride, midline smoothing)
  change anything, and the result says which settings had no effect
- RemoteRunner: renders an image-level rod and runs the tracker as a job on
  the machine that has it (scripts/remote/qb_track.py), then fetches the
  output. Host, paths and Python come from private/runner.yaml (git-ignored;
  template config/runner.example.yaml)

Code goes to one directory per branch and commit on the tracker machine:
<code_dir>/<branch, "/" replaced by "_">/<commit>, written once from
`git archive` (freeze v3; nothing on the lab server is overwritten or
renamed, CLAUDE.md, spec audit rules-2). The sweep lock stays in the shared
work directory, one per machine (decisions, 2026-10-12). Sweep plans and logs
get a new name per start; tracker outputs and rendered rods are complete when
their `.ok` marker exists.

Both return a Measurement: the record, the rigidly moved record for the
invariance check, and the settings used.
"""
from dataclasses import dataclass, field, replace
import json
from pathlib import Path
import shlex
import subprocess
import tarfile
import time
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
SYNCED = ("measure", "scripts/synth", "scripts/remote")      # code copied to the tracker machine
MAX_JOBS = 2                 # jobs of this account at once on the lab server (CLAUDE.md, Andrew 2026-10-23)
JOB_PATTERN = "sweep|qb_track|make_rod|g2_run|st_run|curv.py|run_default"   # docs/decisions.md, 2026-10-23


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


def current_branch(root=ROOT):
    """The checked-out branch of this checkout. Refuses a detached HEAD (no branch to name the code directory)."""
    b = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, capture_output=True,
                       text=True, check=True).stdout.strip()
    if not b or b == "HEAD":
        raise RuntimeError("detached HEAD: check out a branch before syncing code to the tracker machine")
    return b


def branch_code_dir(base, branch):
    """<base>/<branch with "/" replaced by "_">. One code directory per branch."""
    name = branch.replace("/", "_")
    if name in ("", ".", "..") or "\\" in name:
        raise ValueError(f"branch name {branch!r} cannot name a code directory")
    return f"{base.rstrip('/')}/{name}"


class RemoteRunner:
    form = "remote_job"

    def __init__(self, config=RUNNER_CONFIG, cache=None, couple=False, branch=None):
        """couple: tracking mode for every run of this runner (a run setting, not a remedy).
        branch: names the code directory; default the checked-out branch."""
        self.couple = couple
        cfg = yaml.safe_load(Path(config).read_text())
        self.rods = cfg.get("rods_dir", "rods")           # rendered rods, under work_dir
        self.max_gb = cfg.get("max_gb")                    # sweep work-space limit; None = sweep.py default
        self.host, self.work, self.code_base, self.python = (cfg["host"], cfg["work_dir"],
                                                             cfg["code_dir"], cfg["python"])
        self.code_branch = branch_code_dir(self.code_base, branch or current_branch())
        self.code = None                        # the commit folder; set by sync_code on first use
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
        """Copy the committed code to <branch dir>/<commit>, once. Nothing there is overwritten (CLAUDE.md, spec
        audit rules-2): a new commit gets a new folder; a folder with its .ok marker is reused. Refuses when the
        synced folders have uncommitted changes, so every run's code is a commit."""
        if not self._code_committed():
            raise RuntimeError("uncommitted changes in the code synced to the tracker machine; commit first")
        code = f"{self.code_branch}/{self._git('rev-parse', '--short=12', 'HEAD').decode().strip()}"
        q = shlex.quote(code)
        self.code = code
        if self._ssh(f"test -e {q}/.ok && echo yes || echo no").decode().strip() == "yes":
            return self.code
        data = self._git("archive", "--format=tar", "HEAD", *SYNCED)
        # mkdir without -p on the commit folder: fails if a partial copy exists (left for Andrew)
        self._ssh(f"mkdir -p {shlex.quote(self.code_branch)} && mkdir {q} && cd {q} && tar xkf - && "
                  f"set -C && : > .ok", stdin=data)
        return self.code

    @staticmethod
    def _git(*args):
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout

    def _code_committed(self):
        return not self._git("status", "--porcelain", "--", *SYNCED).strip()

    def _py(self, script, args):
        if self.code is None:
            self.sync_code()
        return " ".join([self.python, shlex.quote(f"{self.code}/{script}")] + [shlex.quote(a) for a in args])

    def _low(self, cmd):
        """Lowest CPU and I/O priority on the shared machine (decisions, 2026-10-11)."""
        return f"nice -n 19 $(command -v ionice >/dev/null && echo ionice -c 3) {cmd}"

    def account_jobs(self):
        """Jobs of this account on the tracker machine: distinct process groups of its processes matching
        JOB_PATTERN (a sweep, its workers and their tracker runs share one group)."""
        cmd = (f"ps -u \"$(id -u)\" -o pgid=,args= | awk '$2 !~ /^(awk|ps|grep|sh|bash)$/' "
               f"| grep -E {shlex.quote(JOB_PATTERN)} | grep -v -E 'sweep[.]py (status|stop)' "
               f"| awk '{{print $1}}' | sort -u | wc -l")
        return int(self._ssh(cmd).decode().split()[-1])

    def _load_ok(self, wait_s=1800, poll_s=60):
        """A job starts only if the 1 min load is below half the cores and fewer than MAX_JOBS jobs of this
        account run (CLAUDE.md, Andrew 2026-10-23). Waits up to wait_s, then refuses."""
        t0 = time.time()
        while True:
            n, l1 = self._ssh("nproc; cut -d' ' -f1 /proc/loadavg").decode().split()
            jobs = self.account_jobs()
            if float(l1) < 0.5 * int(n) and jobs < MAX_JOBS:
                return
            if time.time() - t0 > wait_s:
                raise RuntimeError(f"load {l1} on {n} cores, {jobs} jobs of this account; not starting a job "
                                   "on the shared machine")
            time.sleep(poll_s)

    # ---- sweeps (scripts/synth/sweep.py holds the limits for the shared machine)

    @property
    def size_root(self):
        """The space the 10 GB limit applies to: the directory holding the work and code directories."""
        import posixpath
        return posixpath.commonpath([self.work, self.code_base])

    def sweep_start(self, plan, name, tracks="tracks", max_hours=2.0):
        """Write the plan and start sweep.py detached at lowest priority. Refuses while a sweep runs."""
        self.sync_code()
        st = self.sweep_status()
        if st.get("running"):
            raise RuntimeError(f"a sweep is running ({st.get('plan')}); not starting another")
        jobs = self.account_jobs()
        if jobs >= MAX_JOBS:
            raise RuntimeError(f"{jobs} jobs of this account run on the tracker machine; at most {MAX_JOBS}")
        q = shlex.quote
        # New plan and log names per start, written with noclobber: nothing on the lab server is overwritten
        stamp = time.strftime("%Y%m%d-%H%M%S")
        plan_f, log_f = f"plan_{name}_{stamp}.json", f"sweep_{name}_{stamp}.log"
        self._ssh(f"mkdir -p {q(self.work)} && set -C && cat > {q(self.work)}/{plan_f}", stdin=json.dumps(plan).encode())
        self.start_detached(f"cd {q(self.work)} && set -C && " + self._low(
            self._py("scripts/synth/sweep.py", ["run", "--plan", plan_f, "--work", ".",
                                                "--tracks", tracks, "--rods", self.rods, "--size-root", self.size_root,
                                                "--max-hours", str(max_hours)]
                                                + (["--max-gb", str(self.max_gb)] if self.max_gb else [])))
            + f" > {log_f} 2>&1")
        return log_f

    def sweep_status(self, name=None):
        out = json.loads(self._ssh(self._py("scripts/synth/sweep.py", ["status", "--work", self.work]))
                         .decode().strip().splitlines()[-1])
        if name:
            q = shlex.quote
            # the newest log of this sweep name by modification time (the VM clock is not monotonic), or the old single name
            log = self._ssh(f"cd {q(self.work)} && f=$(ls -1t sweep_{name}_*.log 2>/dev/null | head -1); "
                            f"cat \"${{f:-sweep_{name}.log}}\" 2>/dev/null || true").decode()
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
        # finished outputs only: those with their .ok marker (qb_track.py)
        data = self._ssh(f"cd {q(self.work)}/{q(tracks)} && ls | grep -E '__.+[.]npz[.]ok$' | sed 's/[.]ok$//' "
                         f"| tar cf - -T -")
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(cache, filter="data")
        for rid in {f.name.split("__")[0] for f in cache.glob("*__*.npz") if "_moved__" not in f.name}:
            local = cache / f"{rid}_truth.npz"
            if not local.exists():
                self._fetch(f"{self.work}/{self.rods}/{rid}_truth.npz", local)
        return cache

    def render(self, rod, moved=False):
        """Render the rod on the tracker machine unless it exists. Returns the rod id."""
        args = ["--out", f"{self.work}/{self.rods}"] + rod.options() + (["--moved"] if moved else [])
        cmd = (f"mkdir -p {shlex.quote(self.work)}/{self.rods} {shlex.quote(self.work)}/tracks && "
               + self._py("scripts/synth/make_rod.py", args + ["--dry-run"]))
        rid = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])["id"]
        r = f"{shlex.quote(self.work)}/{self.rods}/{rid}"
        state = self._ssh(f"if test -e {r}.ok -o -e {r}_truth.npz; then echo done; elif test -e {r}.imgdir; "
                          f"then echo partial; else echo none; fi").decode().strip()
        if state == "partial":
            raise RuntimeError(f"partial render left in place on the tracker machine: {rid}; needs Andrew")
        if state == "none":
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
        remote = f"{shlex.quote(self.work)}/tracks/{name}"
        state = "local" if local.exists() else self._ssh(
            f"if test -e {remote}.ok; then echo done; elif test -e {remote}; then echo partial; else echo none; fi"
        ).decode().strip()
        if state == "partial":
            raise RuntimeError(f"partial tracker output left in place on the tracker machine: {name}; needs Andrew")
        if state == "done":
            self._fetch(f"{self.work}/tracks/{name}", local)
        if state == "none":
            args = ["--imgdir", f"{self.work}/{self.rods}/{rid}.imgdir",
                    "--midline", f"{self.work}/{self.rods}/{rid}_midline.npz",
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
            self._fetch(f"{self.work}/{self.rods}/{rid}_truth.npz", local)
        with np.load(local) as z:
            return {k: z[k] for k in z.files}

    def measure(self, rod, settings):
        rid = self.render(rod)
        rid_moved = self.render(rod, moved=True)
        rec = from_tracker_npz(self.track(rid, settings))
        moved = from_tracker_npz(self.track(rid_moved, settings))
        return Measurement(rec, moved, settings, self.truth(rid))
