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

Storage and compute (spec 2026-11-04, Andrew): with `compute: cluster` in the config, `storage_host` holds movies,
midlines and tracks and only relays; every compute step (segmentation and net midline, moved copy, tracking) runs as
a Slurm job on cluster nodes (measure/cluster_compute.py), reached through the storage host's connection master over
one persistent connection held by this runner (measure/remote_link.py). The root imgdir is staged whole on the
cluster; outputs are copied back to storage with md5 checks; this machine receives the track files only. The
lab-server load and job-count checks do not apply there. Without `compute: cluster` the runner works as before on
its `host` (the workstation), and refuses any compute on a storage-only host (measure/hosts.py).
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

from measure.cluster_compute import ClusterCompute
from measure.hosts import refuse_storage_host
from measure.record import from_tracker_npz
from measure.remedies import NotAvailable, TrackSettings
from measure.remote_link import Link, Relay
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


def _ledger_from(cfg):
    """The spend-ledger command from the private config (`ledger: [program, script]`): called as
    `program script check|record|final ...`; returns (exit code, last output line)."""
    import os
    cmd = cfg.get("ledger")
    if not cmd:
        raise ValueError("cluster compute needs a `ledger` command in the config (spend check before every submit)")

    def ledger(action, *args):
        p = subprocess.run([*cmd, action, *args], capture_output=True, text=True,
                           env={**os.environ, "MSYS_NO_PATHCONV": "1"})
        lines = [l for l in p.stdout.splitlines() if l.strip()]
        return p.returncode, (lines[-1] if lines else p.stderr.strip()[-300:])
    return ledger


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

    def __init__(self, config=REAL_CONFIG, cache=None, track_length=TRACK_LENGTH, moved=True, moved_mode="whole_pixel",
                 link=None, ledger=None, sleep=time.sleep):
        cfg = yaml.safe_load(Path(config).read_text()) if not isinstance(config, dict) else config
        self.cluster_mode = cfg.get("compute") == "cluster"
        if cfg.get("compute") not in (None, "cluster"):
            raise ValueError(f"compute: {cfg['compute']!r}; only 'cluster' is allowed (spec 2026-11-04)")
        if self.cluster_mode:
            c = cfg["cluster"]
            self.host = cfg["storage_host"]
            self.link = link or Link(self.host)
            self.relay = Relay(self.link, c["alias"])
            self.cc = ClusterCompute(self.relay, c, ledger or _ledger_from(cfg), sleep=sleep)
            self.ccfg = c
            self.work, self.code, self.tracker, self.python = (
                cfg["work_dir"], c["code_dir"], c["tracker_code"], "python")
        else:
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
        if self.cluster_mode:                  # a channel on the one held storage-host connection
            try:
                return self.link.run(cmd, stdin)
            except Exception as e:             # same failure type as the subprocess path for callers
                if type(e).__name__ == "LinkDown":
                    raise
                raise RuntimeError(str(e)) from e
        # keepalive: a silently dropped connection fails in about 2 min instead of hanging (c022 run 2)
        p = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=4",
                            self.host, cmd], input=stdin, capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"host command failed ({p.returncode}): "
                               f"{p.stderr.decode(errors='replace').strip().splitlines()[-1:]}")
        return p.stdout

    def sync_code(self):
        buf = io.BytesIO()
        # cluster jobs also run the checker (spec 2026-11-04): it needs checker/, agents/, config/ and scripts/
        dirs = ("measure", "scripts", "checker", "agents", "config", "manifest") if self.cluster_mode \
            else ("measure", "scripts/remote")
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for d in dirs:
                tar.add(ROOT / d, arcname=d, filter=lambda ti: None if "__pycache__" in ti.name else ti)
        q = shlex.quote
        if self.cluster_mode:                  # streamed through the storage host; nothing is written there
            self.relay.run(f"mkdir -p {q(self.code)} && cd {q(self.code)} && tar xf -", stdin=buf.getvalue())
            return
        self._ssh(f"mkdir -p {q(self.code)} && cd {q(self.code)} && tar xf -", stdin=buf.getvalue())

    def host_state(self):
        q = shlex.quote
        if self.cluster_mode:                  # no jobs on the storage host: report the cluster queue instead
            n = self.cc.own_jobs()
            return {"cores": int(self.ccfg.get("max_jobs", 2)), "load1": float(n), "own_jobs": n,
                    "free_gb": float("inf")}
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
        if self.cluster_mode:                  # the queue and the ledger limit cluster jobs; nothing runs on storage
            return {"load1": None, "free_gb": None}
        refuse_storage_host(self.host, "a tracker or midline run")
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

    # ---- cluster mode (spec 2026-11-04): every compute step is a Slurm job; storage keeps the outputs
    def _cpath(self, kind, name):
        return f"{self.ccfg['work_dir']}/{kind}/{name}"

    def _ctest(self, path):
        return self.relay.run(f"test -e {shlex.quote(path)} && echo yes || echo no").decode().strip() == "yes"

    def _staged(self, window):
        return self.cc.stage_root(window.root_id, self.windows[window.id()]["imgdir"])

    def _cluster_midline(self, window):
        """The window's tracking midline on the cluster: pushed from storage, or built there (segmentation on the
        GPU job's CPUs, net midline on its GPU) and copied back to storage."""
        q = shlex.quote
        sm, wid = self.midline_path(window), window.id()
        cm = self._cpath("midline", f"{wid}{self.tag}_netmid.npz")
        if self._ctest(cm):
            return cm
        if self._ssh(f"test -f {q(sm)} && echo yes || echo no").decode().strip() == "yes":
            self.cc.push_file(sm, cm)
            return cm
        img = self._staged(window)
        seg, bm = self._cpath("midline", f"{wid}_seg.npz"), self._cpath("midline", f"{wid}{self.tag}_bm")
        body = (f"mkdir -p {q(self._cpath('midline', ''))} && cd {q(self.code)}\n"
                f"export PYTHONPATH={q(self.tracker)}:{q(self.code)}\n"
                f"test -f {q(seg)} || python scripts/remote/real_midline.py --imgdir {q(img)} --from-h {window.from_h:g} "
                f"--to-h {window.to_h:g} --out {q(seg)} || exit 1\n"
                f"se=$(python -c \"import sys,numpy as np; f=np.load(sys.argv[1])['frames']; print(int(f[0]), int(f[-1])+1)\" {q(seg)})\n"
                f"set -- $se\n"
                f"test -n \"$(ls {q(bm)}/*_htpmid.npz 2>/dev/null)\" || python {q(self.tracker)}/midline_ml/batch_midlines.py "
                f"{q(img)} --out {q(bm)} --mode tile --lo 0.1 --hi 99.5 --workers 3 "
                f"--midline-weights {q(self.ccfg['midline_weights'])} --start $1 --end $2 || exit 1\n"
                f"PYTHONPATH={q(self.tracker)}:{q(self.code)}:{q(self.code)}/scripts/remote python scripts/remote/net_to_midline.py "
                f"{q(self.tracker)} {q(bm)}/*_htpmid.npz {q(seg)} {q(cm)}")
        self.cc.run(f"mid_{wid}", body, cpus=4, gpu=True, time_limit="01:00:00", mem="32G")
        self.cc.pull(cm, sm.rsplit("/", 1)[0])
        self.log.append({"midline": wid, "where": "cluster"})
        return cm

    def _cluster_moved(self, window):
        q = shlex.quote
        wid = window.id()
        mv = {k: self._cpath("moved", f"{wid}_wp_{k}.imgdir") for k in ("moved", "ref")}
        mm = {k: self._cpath("moved", f"{wid}{self.tag}_wp_{k}_midline.npz") for k in ("moved", "ref")}
        if all(self._ctest(mv[k] + ".ok") and self._ctest(mm[k]) for k in mv):
            return mv["moved"]
        cm, img = self._cluster_midline(window), self._staged(window)
        args = ["--imgdir", img, "--midline", cm, "--from-h", f"{window.from_h:g}", "--to-h", f"{window.to_h:g}",
                "--out-imgdir", mv["moved"], "--out-midline", mm["moved"], "--mode", self.moved_mode,
                "--out-ref-imgdir", mv["ref"], "--out-ref-midline", mm["ref"]]
        body = (f"mkdir -p {q(self._cpath('moved', ''))} && cd {q(self.code)} && PYTHONPATH={q(self.tracker)}:{q(self.code)} "
                f"python scripts/remote/real_moved.py " + " ".join(q(a) for a in args))
        self.cc.run(f"moved_{wid}", body, cpus=1, time_limit="00:30:00")
        self.log.append({"moved_copy": wid, "where": "cluster"})
        return mv["moved"]

    def _cluster_track(self, window, settings, which, local):
        q = shlex.quote
        wid, name = window.id(), local.name
        if which == "window":
            img, mid = self._staged(window), self._cluster_midline(window)
        else:
            img = self._cpath("moved", f"{wid}_wp_{which}.imgdir")
            mid = self._cpath("moved", f"{wid}{self.tag}_wp_{which}_midline.npz")
        ct = self._cpath("tracks", name)
        if not self._ctest(ct):
            args = (["--imgdir", img, "--midline", mid, "--out", ct, "--movie", "real", "--from-h", f"{window.from_h:g}",
                     "--to-h", f"{window.to_h:g}", "--track-length", f"{self.track_length:g}"] + settings.args())
            body = (f"mkdir -p {q(self._cpath('tracks', ''))} && cd {q(self.code)} && PYTHONPATH={q(self.tracker)}:{q(self.code)} "
                    f"python scripts/remote/qb_track.py " + " ".join(q(a) for a in args))
            self.cc.run(f"track_{name[:-4]}", body, cpus=1, time_limit="01:00:00")
        stored = self.cc.pull(ct, f"{self.work}/tracks")
        local.write_bytes(self._ssh(f"cat {q(stored)}"))
        self.log.append({"track": name, "where": "cluster"})
        return local

    def ensure_midline(self, window):
        """Build the window's net midline on the host unless the file exists. Each step skips an output that
        exists, so an interrupted build resumes."""
        q = shlex.quote
        out = self.midline_path(window)
        if self.cluster_mode:
            self._cluster_midline(window)
            return out
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
        if self.cluster_mode:
            if self.moved_mode != "whole_pixel":
                raise ValueError("cluster compute makes whole-pixel copies only")
            return self._cluster_moved(window)
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
            if self.cluster_mode:
                self.wait_vm_memory()
                return self._cluster_track(window, settings, which, local)
            before = self.check_host()
            q = shlex.quote
            args = (["--imgdir", w["imgdir"], "--midline", w["midline"], "--out", f"{self.work}/tracks/{name}",
                     "--movie", "real", "--from-h", f"{window.from_h:g}", "--to-h", f"{window.to_h:g}",
                     "--track-length", f"{self.track_length:g}"] + settings.args())
            cmd = (f"mkdir -p {q(self.work)}/tracks && cd {q(self.code)} && "
                   f"OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 "
                   f"PYTHONPATH={q(self.tracker)}:{q(self.code)} nice -n 19 {q(self.python)} "
                   f"scripts/remote/qb_track.py " + " ".join(q(a) for a in args))
            try:
                out = json.loads(self._ssh(cmd).decode().strip().splitlines()[-1])
            except RuntimeError:            # connection lost: the host may have finished the track anyway
                if self.fetch_host_track(name, local):
                    return local
                raise
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
