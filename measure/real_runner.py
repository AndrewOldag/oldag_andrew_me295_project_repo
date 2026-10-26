"""Measurement runner for one window of a real movie: `RealRunner().measure(window, settings)`.

Same interface as the synthetic runners (measure/runner.py), so the diagnostician's Slice
(agents/executors.py) works on real windows unchanged. It runs scripts/remote/qb_track.py for the
window on the compute host with the window's midline file (net midline, decisions 2026-10-23) and the
remedy settings, then fetches the output. Outputs are cached locally by window and settings tag.

Host, folders, Python, tracker code and the per-window movie and midline paths come from
private/real_runner.yaml (git-ignored; template config/real_runner.example.yaml). A window whose midline
file is missing on the host gets its net midline built there first (`ensure_midline`, inbox item 21):
segmentation midline (scripts/remote/real_midline.py, for the frame list and mask0), the tracker's
`midline_ml/batch_midlines.py --mode tile` with the fine-tuned net2 at low 0.1 %, high 99.5 %
(decisions 2026-10-23), then scripts/remote/net_to_midline.py. `midline_weights` and `midline_tag` in the config
select another net (inbox item 22: `net2_midline_ft2.pt`, tag `ft2`); the tag goes into every net-midline, moved-copy
midline, host track and cache name, so outputs of different nets never overwrite each other. Whole-pixel copy frames do
not depend on the midline; an existing copy of the window is reused (scripts/remote/real_moved.py).

Tracked length 1000 px (spec 2026-10-24b A): the chain base, which closure takes as fixed in the world, lies past
the growth zone; at 400 px it moved 5-39 px over 2 h with growth (results/2026-10-25_closure_definition/).

VM memory (inbox item 22): before every host step the runner waits while free VM memory is below 1.5 GB.

Limits on the host, checked before every tracker run: 1 min load at most half the cores; fewer than
2 jobs of this account already running; at least `min_free_gb` free on the work disk (workstation rule,
2026-10-23). Single-thread tracker, nice 19. The net midline runs as one process with 3 compute threads
and 1 prefetch thread (4 workers at most).

Rigid invariance: the runner makes the copies on the host once (scripts/remote/real_moved.py) and tracks
them with the same settings, as RemoteRunner does for synthetic rods. Default `moved_mode="whole_pixel"`
(Andrew, 2026-10-24): a cropped reference copy and its whole-pixel-shifted twin, no resampling; the
reference is the measurement record. `"rotate"`: the synthetic rods' rotation and translation (bilinear)
against the window as is. `moved=False` skips it (rigid invariance not run).
"""
from dataclasses import dataclass, replace
import io
import json
from pathlib import Path
import shlex
import subprocess
import tarfile
import time

import yaml

from measure.record import from_tracker_npz
from measure.remedies import NotAvailable, TrackSettings
from measure.runner import Measurement

ROOT = Path(__file__).resolve().parents[1]
REAL_CONFIG = ROOT / "private" / "real_runner.yaml"
JOB_PATTERN = "qb_track.py|batch_midlines.py|sweep.py run"
# The same pattern with one letter in brackets, so that the shell running the count does not count itself
COUNT_PATTERN = "[q]b_track.py|[b]atch_midlines.py|[s]weep.py run"
# Only python processes count as jobs: the `bash -c` wrappers that launch a job carry its script name in their
# command line too, so one midline build counted as 3 jobs (2026-10-24, real-calib)
COUNT_CMD = f"ps -u $(id -u) -o comm=,args= | awk '$1 ~ /^python/' | grep -cE '{COUNT_PATTERN}'"
MIDLINE_WEIGHTS = "net2_midline_ft.pt"
MIDLINE_ARGS = ["--mode", "tile", "--lo", "0.1", "--hi", "99.5", "--workers", "1"]
MIDLINE_THREADS = 3
VM_MIN_FREE_GB = 1.5
# Tracked length on real windows (spec 2026-10-24b A): closure assumes a basal point fixed in the world, and on
# real roots the growth zone reaches 550-650 px from the tip, so a 400 px chain ends in growing tissue
TRACK_LENGTH = 1000.0


def vm_free_gb():
    """Free physical memory of this machine, GB (psutil if present, else the Windows API, else /proc/meminfo)."""
    try:
        import psutil
        return psutil.virtual_memory().available / 2 ** 30
    except ImportError:
        pass
    try:
        import ctypes

        class MS(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [
                (n, ctypes.c_ulonglong) for n in ("total", "avail", "tpage", "apage", "tvirt", "avirt", "aext")]
        m = MS()
        m.dwLength = ctypes.sizeof(MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return m.avail / 2 ** 30
    except AttributeError:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 2 ** 20
    return float("inf")


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

    def __init__(self, config=REAL_CONFIG, cache=None, track_length=TRACK_LENGTH, moved=True, moved_mode="whole_pixel"):
        cfg = yaml.safe_load(Path(config).read_text())
        self.host, self.work, self.code, self.tracker, self.python = (
            cfg["host"], cfg["work_dir"], cfg["code_dir"], cfg["tracker_code"], cfg["python"])
        self.min_free_gb = float(cfg.get("min_free_gb", 21))
        self.windows = cfg["windows"]                 # window id -> {imgdir, midline (optional)}
        self.weights = cfg.get("midline_weights", MIDLINE_WEIGHTS)
        self.tag = f"_{cfg['midline_tag']}" if cfg.get("midline_tag") else ""
        self.track_length = float(track_length)
        self.with_moved = bool(moved)
        self.moved_span = None                  # (from_h, to_h): moved copy for this span only (first batch, c022)
        self.cached_only = False                # repeat runs (item 36): cached tracks only, no tracker rerun
        self.moved_mode = moved_mode            # whole_pixel (inbox item 19) or rotate (first 2026-10-24 run)
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
        out = self._ssh(f"nproc --all; cut -d' ' -f1 /proc/loadavg; {COUNT_CMD}; "
                        f"df -BG --output=avail {q(self.work)} | tail -1").decode().split()
        return {"cores": int(out[0]), "load1": float(out[1]), "own_jobs": int(out[2]),
                "free_gb": float(out[3].rstrip("G"))}

    def wait_vm_memory(self, poll_s=60):
        """Wait while free VM memory is below VM_MIN_FREE_GB (inbox item 22)."""
        while (free := vm_free_gb()) < VM_MIN_FREE_GB:
            print(f"VM memory {free:.2f} GB free, below {VM_MIN_FREE_GB} GB; waiting", flush=True)
            time.sleep(poll_s)
        return free

    def check_host(self):
        self.wait_vm_memory()
        s = self.host_state()
        if s["load1"] > 0.5 * s["cores"]:
            raise HostBusy(f"load {s['load1']} above half of {s['cores']} cores")
        if s["own_jobs"] >= 2:
            raise HostBusy(f"{s['own_jobs']} jobs of this account running (limit 2)")
        if s["free_gb"] < self.min_free_gb:
            raise HostBusy(f"{s['free_gb']} GB free, below {self.min_free_gb} GB")
        return s

    def midline_path(self, window):
        return self.windows[window.id()].get("midline") or f"{self.work}/midline/{window.id()}{self.tag}_netmid.npz"

    def ensure_midline(self, window):
        """Build the window's net midline on the host unless the file exists. Each step skips an output that
        exists, so an interrupted build resumes."""
        q = shlex.quote
        out = self.midline_path(window)
        if self._ssh(f"test -f {q(out)} && echo yes || echo no").decode().strip() == "yes":
            return out
        wid, img = window.id(), self.windows[window.id()]["imgdir"]
        d = f"{self.work}/midline"
        seg, bm = f"{d}/{wid}_seg.npz", f"{d}/{wid}{self.tag}_bm"      # the segmentation midline does not use the net
        env = (f"OMP_NUM_THREADS={MIDLINE_THREADS} MKL_NUM_THREADS={MIDLINE_THREADS} OPENBLAS_NUM_THREADS=1 "
               f"PYTHONPATH={q(self.tracker)}:{q(self.code)}")
        before = self.check_host()
        self._ssh(f"mkdir -p {q(d)} && cd {q(self.code)} && (test -f {q(seg)} || {env} nice -n 19 {q(self.python)} "
                  f"scripts/remote/real_midline.py --imgdir {q(img)} --from-h {window.from_h:g} "
                  f"--to-h {window.to_h:g} --out {q(seg)})")
        prog = "import json,sys,numpy as np; f=np.load(sys.argv[1])['frames']; print(json.dumps([int(f[0]), int(f[-1])]))"
        frames = json.loads(self._ssh(f"{q(self.python)} -c {q(prog)} {q(seg)}").decode().strip().splitlines()[-1])
        self.check_host()
        t = self._ssh(f"test -n \"$(ls {q(bm)}/*_htpmid.npz 2>/dev/null)\" || (date +%s; {env} nice -n 19 "
                      f"{q(self.python)} {q(self.tracker)}/midline_ml/batch_midlines.py {q(img)} --out {q(bm)} "
                      + " ".join(MIDLINE_ARGS) + f" --midline-weights {q(self.weights)} --start {frames[0]} --end {frames[1] + 1} > {q(bm)}.log 2>&1;"
                      " date +%s)").decode().split()
        res = json.loads(self._ssh(f"cd {q(self.code)} && {env} nice -n 19 {q(self.python)} "
                                   f"scripts/remote/net_to_midline.py {q(self.tracker)} {q(bm)}/*_htpmid.npz "
                                   f"{q(seg)} {q(out)}").decode().strip().splitlines()[-1])
        after = self.host_state()
        self.log.append({"midline": wid, "weights": Path(self.weights).name, **res, "net_s": int(t[1]) - int(t[0]) if len(t) == 2 else None,
                         "first_frame": frames[0], "last_frame": frames[1], "load1_before": before["load1"],
                         "free_gb_before": before["free_gb"], "free_gb_after": after["free_gb"]})
        return out

    def copy_paths(self, window, which):
        """which: 'moved' or 'ref'. Whole-pixel mode (inbox item 19): cropped reference and moved copies."""
        base = f"{self.work}/moved/{window.id()}"
        if self.moved_mode == "rotate":
            return {"imgdir": f"{base}{self.tag}_moved.imgdir", "midline": f"{base}{self.tag}_moved_midline.npz"}
        # whole-pixel frames do not depend on the midline: one copy per window, shared by every net (item 22)
        return {"imgdir": f"{base}_wp_{which}.imgdir", "midline": f"{base}{self.tag}_wp_{which}_midline.npz"}

    def ensure_moved(self, window):
        """Make the rigidly moved copy (and, whole-pixel mode, the cropped reference) on the host unless they exist."""
        mv, ref = self.copy_paths(window, "moved"), self.copy_paths(window, "ref")
        w = dict(self.windows[window.id()], midline=self.midline_path(window))
        q = shlex.quote
        need = [mv] if self.moved_mode == "rotate" else [mv, ref]
        # complete copy: folder and midline present, and not a stopped write-once copy (.started without .ok)
        test = " && ".join(f"test -d {q(p['imgdir'])} && test -f {q(p['midline'])} && "
                           f"{{ test -f {q(p['imgdir'] + '.ok')} || ! test -f {q(p['imgdir'] + '.started')}; }}"
                           for p in need)
        if self._ssh(f"{test} && echo yes || echo no").decode().strip() == "yes":
            return mv
        before = self.check_host()
        args = ["--imgdir", w["imgdir"], "--midline", w["midline"], "--from-h", f"{window.from_h:g}",
                "--to-h", f"{window.to_h:g}", "--out-imgdir", mv["imgdir"], "--out-midline", mv["midline"],
                "--mode", self.moved_mode]
        if self.moved_mode == "whole_pixel":
            args += ["--out-ref-imgdir", ref["imgdir"], "--out-ref-midline", ref["midline"]]
        cmd = (f"mkdir -p {q(self.work)}/moved && cd {q(self.code)} && nice -n 19 {q(self.python)} "
               f"scripts/remote/real_moved.py " + " ".join(q(a) for a in args))
        out = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])
        after = self.host_state()
        self.log.append({"moved_copy": window.id(), **out, "free_gb_before": before["free_gb"],
                         "free_gb_after": after["free_gb"]})
        return mv

    def cache_path(self, window, settings, which="window"):
        settings = replace(settings, width_free=False)
        tag = {"window": "", "moved": "_moved" if self.moved_mode == "rotate" else "_wp_moved", "ref": "_wp_ref"}[which]
        return self.cache / f"{window.id()}{self.tag}{tag}__{settings.tag()}__L{self.track_length:g}.npz"

    def fetch_host_track(self, name, local):
        """A host track of the same name (same window, settings and length) written by an earlier run whose
        local copy is missing: fetch it instead of tracking again. qb_track never overwrites its output."""
        q = shlex.quote
        try:
            self._ssh(f"test -s {q(self.work)}/tracks/{q(name)}")
        except RuntimeError:
            return False
        local.write_bytes(self._ssh(f"cat {q(self.work)}/tracks/{q(name)}"))
        self.log.append({"track": name, "fetched": "existing host output"})
        return True

    def track(self, window, settings, which="window"):
        """which: 'window' (the movie as is), 'moved' or 'ref' (copies made by ensure_moved)."""
        settings = replace(settings, width_free=False)
        w = (dict(self.windows[window.id()], midline=self.midline_path(window)) if which == "window"
             else self.copy_paths(window, which))
        local = self.cache_path(window, settings, which)
        name = local.name
        if not local.exists() and self.fetch_host_track(name, local):
            return local
        if not local.exists():
            if self.cached_only:
                raise NotAvailable("no cached track for these settings (repeat run: cached tracks only)")
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
        """Whole-pixel mode: the record is the cropped reference copy and `moved` its shifted twin, so rigid
        invariance compares two copies cropped to the same area (inbox item 19)."""
        main = "window" if self.moved_mode == "rotate" else "ref"
        with_moved = self.with_moved and (self.moved_span is None or (window.from_h, window.to_h) == self.moved_span)
        need = [main, "moved"] if with_moved else ["window"]
        if not all(self.cache_path(window, settings, k).exists() for k in need):   # cached runs need no host step
            if self.cached_only:       # host outputs of earlier runs count as cached; track() raises if one is missing
                rec = from_tracker_npz(self.track(window, settings, need[0]), root_id=window.id())
                moved = (from_tracker_npz(self.track(window, settings, "moved"), root_id=window.id() + "_moved")
                         if with_moved else None)
                return Measurement(rec, moved, settings, {})
            self.ensure_midline(window)
            if with_moved:
                self.ensure_moved(window)
        if not with_moved:
            return Measurement(from_tracker_npz(self.track(window, settings), root_id=window.id()), None, settings, {})
        rec = from_tracker_npz(self.track(window, settings, main), root_id=window.id())
        moved = from_tracker_npz(self.track(window, settings, "moved"), root_id=window.id() + "_moved")
        return Measurement(rec, moved, settings, {})


class RunnerSet:
    """Several RealRunners, one per host config; each window goes to the runner whose config lists it (inbox
    item 27: 0711_c1 tracked on the lab server, the other roots on the workstation). The first config that lists
    a window wins. Same interface as RealRunner for the slice."""

    form = "real_window"

    def __init__(self, configs, cache=None, **kw):
        self.runners = [RealRunner(c, cache=cache, **kw) for c in configs]

    def runner_for(self, window):
        for r in self.runners:
            if window.id() in r.windows:
                return r
        raise KeyError(f"no runner config lists window {window.id()}")

    def initial_settings(self, window):
        return self.runner_for(window).initial_settings(window)

    def measure(self, window, settings):
        return self.runner_for(window).measure(window, settings)

    def sync_code(self):
        for r in self.runners:
            r.sync_code()

    def host_state(self):
        """Load of the busiest host (the dispatcher's queue load reads one value)."""
        states = [r.host_state() for r in self.runners]
        return max(states, key=lambda s: s["load1"] / s["cores"])

    @property
    def log(self):
        return [dict(e, host_config=k) for k, r in enumerate(self.runners) for e in r.log]
