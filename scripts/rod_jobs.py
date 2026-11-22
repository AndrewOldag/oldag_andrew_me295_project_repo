"""Synthetic-rod job kind for cluster tracker runs (spec 2026-11-20, Cluster for everything): the rod counterpart of
scripts/retrack_queue.py, built on its Remote, array script, ledger and states. Submit and forget; both steps can
be rerun at any time.

Rods are rendered on the VM (scripts/synth/make_rod.py) and pushed whole: VM -> storage (tar over the held link, md5
of every file checked, then `<rid>.ok`) -> cluster (rsync over the master, file count checked). One array task per
rendered rod (a rod or its moved copy) runs every tracker run that rod needs, in sequence, 1 core; an output with its
`.ok` marker is skipped and a partial output is reported, never deleted, so a resubmitted task does only what is
left. Fetch pulls each finished output to storage (md5 on both ends), reads it to the VM and caches it (with a local
`.ok`) only if its md5 matches storage. A down link or master gives `connection down` with no state change.

A job row: job (output file name), rid (rendered rod id), settings (TrackSettings as JSON), sub (cluster and local
output subfolder name; default `tracks`). Callers: scripts/synth/compound_queue.py (task c029).
"""
import hashlib
import io
import json
import shlex
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import retrack_queue as rq  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

KIND = "rods"
rq.LIMITS.setdefault(KIND, "01:00:00")        # one rendered rod's runs (about 30 runs of at most 2 min)
TASK_H = 1.0
FIELDS = ["job", "rid", "settings", "sub", "group", "array", "task", "state", "error", "md5", "fetched"]
q = shlex.quote


def worst_case_usd(rows, rate=0.012):
    """Ledger rule: 1 core x the task time limit per rendered rod."""
    return round(rate * TASK_H * len({r["rid"] for r in rows}), 3)


def task_line(work, rid, rows):
    """One shell line: every run of one rendered rod, each skipped if its output is complete."""
    parts, subs = [], sorted({r.get("sub") or "tracks" for r in rows})
    for r in rows:
        out = f"{work}/{r.get('sub') or 'tracks'}/{r['job']}"
        args = ["--imgdir", f"{work}/rods/{rid}.imgdir", "--midline", f"{work}/rods/{rid}_midline.npz",
                "--out", out] + TrackSettings(**json.loads(r["settings"])).args()
        parts.append(f"{{ test -f {q(out + '.ok')} || {{ test ! -e {q(out)} && python scripts/remote/qb_track.py "
                     + " ".join(q(a) for a in args) + f"; }} || {{ echo 'failed: {r['job']}' >&2; rc=1; }}; }}")
    return ("rc=0; mkdir -p " + " ".join(q(f"{work}/{s}") for s in subs) + "; " + "; ".join(parts) + "; exit $rc")


def rod_files(rods_dir, rid):
    rods_dir = Path(rods_dir)
    files = sorted((rods_dir / f"{rid}.imgdir").iterdir()) + [rods_dir / f"{rid}_midline.npz"]
    return {(f"{rid}.imgdir/{f.name}" if f.parent.name.endswith(".imgdir") else f.name): f for f in files}


class RodMover:
    """VM -> storage -> cluster for rendered rods, over the runner's held link and the relay."""

    def __init__(self, runner, storage_dir, rods_dir):
        self.link, self.relay, self.rods_dir = runner.link, runner.relay, Path(rods_dir)
        self.sdir = storage_dir.rstrip("/") + "/rods"
        self.cdir = runner.ccfg["work_dir"].rstrip("/") + "/rods"

    def on_storage(self, rid):
        return self.link.run(f"test -f {q(self.sdir + '/' + rid + '.ok')} && echo yes || echo no").decode().strip() == "yes"

    def upload(self, rid):
        """Tar the rod's files to storage, check every file's md5 there, then write `<rid>.ok`."""
        files = rod_files(self.rods_dir, rid)
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for name, p in files.items():
                tar.add(p, arcname=name)
        self.link.run(f"mkdir -p {q(self.sdir)} && cd {q(self.sdir)} && tar xf -", stdin=buf.getvalue())
        want = {name: hashlib.md5(p.read_bytes()).hexdigest() for name, p in files.items()}
        got = {}
        for line in self.link.run(f"cd {q(self.sdir)} && md5sum " + " ".join(q(n) for n in want)).decode().splitlines():
            h, n = line.split(None, 1)
            got[n.strip().lstrip("*")] = h
        bad = [n for n in want if got.get(n) != want[n]]
        if bad:
            raise RuntimeError(f"{rid}: md5 differs on storage for {len(bad)} files")
        self.link.run(f"set -C && : > {q(self.sdir + '/' + rid + '.ok')}")
        return len(want)

    def push(self, rids):
        """rsync the storage rod folder to the cluster (new files only), then check each rod's file count."""
        self.relay.run(f"mkdir -p {q(self.cdir)}")
        self.relay.push(self.sdir + "/", self.cdir + "/")
        for rid in rids:
            n_s = self.link.run(f"ls {q(self.sdir + '/' + rid + '.imgdir')} | wc -l").decode().strip()
            n_c = self.relay.run(f"ls {q(self.cdir + '/' + rid + '.imgdir')} | wc -l").decode().strip()
            mid = self.relay.run(f"test -s {q(self.cdir + '/' + rid + '_midline.npz')} && echo yes || echo no").decode().strip()
            if n_s != n_c or mid != "yes":
                raise RuntimeError(f"{rid}: {n_c} of {n_s} files on the cluster, midline {mid}")

    def mb(self, rids):
        return sum(sum(p.stat().st_size for p in rod_files(self.rods_dir, r).values()) for r in rids) / 2 ** 20


def submit(runner, remote, mover, rows, state, prefix="rods", log=print):
    """Upload the rods the rows need, then one Slurm array (one task per rod). Returns a one-line status."""
    state = Path(state)
    try:
        remote.require()
    except rq.ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    queue = rq.read_csv(state / "queue.csv")
    queued = {r["job"] for r in queue if r["state"] != "failed"}
    todo = [r for r in rows if r["job"] not in queued]
    if not todo:
        log("nothing to submit")
        return "nothing to submit"
    by_rid = {}
    for r in todo:
        by_rid.setdefault(r["rid"], []).append(r)
    work = runner.ccfg["work_dir"]
    gid = f"g{1 + max([int(r['group'][1:]) for r in queue] or [0]):03d}"
    arrays = []
    try:
        room = int(runner.ccfg.get("cap_mb", rq.CAP_MB)) - remote.folder_mb()
        if mover.mb(by_rid) + 50 > room:
            log(f"no room: {room} MB free under the cap; {len(todo)} jobs wait")
            return "no room"
        runner.sync_code()
        n_up = sum(mover.upload(rid) > 0 for rid in by_rid if not mover.on_storage(rid))
        mover.push(list(by_rid))
        name = f"{prefix}_{gid}"
        job_dir = f"{work}/jobs/{name}"
        rids = list(by_rid)
        remote.write(f"{job_dir}/tasks.txt", "".join(task_line(work, rid, by_rid[rid]) + "\n" for rid in rids))
        remote.write(f"{job_dir}/job.sbatch", rq.array_script(runner, name, f"{job_dir}/tasks.txt", len(rids), KIND))
        rc, msg = remote.ledger("check", job_dir)
        if rc != 0:
            log(f"ledger refused {name}: {msg}")
            return f"budget stop: {msg}"
        aid = remote.sbatch(f"{job_dir}/job.sbatch")
        remote.ledger("record", job_dir, aid)
        for i, rid in enumerate(rids):
            arrays += [{**r, "group": gid, "array": aid, "task": str(i), "state": "submitted", "error": "",
                        "md5": "", "fetched": ""} for r in by_rid[rid]]
        log(f"{name}: array {aid}, {len(rids)} tasks, {len(todo)} tracker runs; rods uploaded {n_up}")
    except rq.ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    except Exception as e:                                           # noqa: BLE001 - lost link mid-submit
        if type(e).__name__ in ("LinkDown", "MasterDown"):
            rq.write_csv(state / "queue.csv", queue + arrays, FIELDS)
            log(f"connection down ({type(e).__name__}: {e}); submitted arrays recorded")
            return "connection down"
        raise
    rq.write_csv(state / "queue.csv", queue + arrays, FIELDS)
    return f"submitted {gid}"


def fetch(runner, remote, state, storage_dir, local_dir, prefix="rods", log=print):
    """Pull finished outputs. local_dir(row) -> the VM folder for that row's output."""
    state = Path(state)
    queue = rq.read_csv(state / "queue.csv")
    if not queue:
        log("queue empty")
        return "queue empty"
    try:
        remote.require()
    except rq.ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    work = runner.ccfg["work_dir"]
    sdir = storage_dir.rstrip("/") + "/tracks"
    counts = {"fetched": 0, "failed": 0, "running": 0}

    def save():
        rq.write_csv(state / "queue.csv", queue, FIELDS)

    try:
        for aid in sorted({r["array"] for r in queue if r["state"] not in rq.FINAL}):
            states = remote.sacct(aid)
            for r in queue:
                if r["array"] != aid or r["state"] in rq.FINAL:
                    continue
                st, _ = states.get(int(r["task"]), ("PENDING", ""))
                if st in ("PENDING", "RUNNING", "REQUEUED", "CONFIGURING", "SUSPENDED", "COMPLETING"):
                    r["state"] = st.lower()
                    counts["running"] += 1
                    continue
                out = f"{work}/{r.get('sub') or 'tracks'}/{r['job']}"
                if remote.relay.run(f"test -f {q(out + '.ok')} && echo yes || echo no").decode().strip() != "yes":
                    tail = remote.err_tail(f"{prefix}_{r['group']}", aid, r["task"])
                    r["state"], r["error"] = "failed", f"{st}: no output; {tail}"
                    counts["failed"] += 1
                    continue
                try:
                    stored, md5 = remote.pull(out, sdir)
                except Exception as e:                               # noqa: BLE001 - md5 mismatch
                    if type(e).__name__ in ("LinkDown", "MasterDown"):
                        raise
                    r["state"], r["error"] = "failed", f"pull: {str(e)[:200]}"
                    counts["failed"] += 1
                    continue
                data = remote.storage_cat(stored)
                if hashlib.md5(data).hexdigest() != md5:
                    r["error"] = "md5 mismatch storage -> VM; not cached (fetch again)"
                    continue
                local = Path(local_dir(r)) / r["job"]
                local.parent.mkdir(parents=True, exist_ok=True)
                tmp = local.with_suffix(".part")
                tmp.write_bytes(data)
                tmp.replace(local)
                Path(f"{local}.ok").touch()
                r["state"], r["md5"], r["fetched"], r["error"] = "fetched", md5, rq.now(), ""
                counts["fetched"] += 1
                if counts["fetched"] % 25 == 0:
                    save()                                       # a dropped link later loses nothing fetched
    except Exception as e:                                           # noqa: BLE001
        if type(e).__name__ in ("LinkDown", "MasterDown", "ConnectionDown"):
            save()
            log(f"connection down ({type(e).__name__}: {e}); fetched so far recorded")
            return "connection down"
        raise
    save()
    left = sum(r["state"] not in rq.FINAL for r in queue)
    msg = f"fetched {counts['fetched']}, failed {counts['failed']}, not finished {left}"
    log(msg)
    return msg
