"""c029 tracker runs on the cluster (spec 2026-11-20, Cluster for everything; inbox compound item 5): the
synthetic-rod job kind of scripts/retrack_queue.py. Submit and forget; both steps can be rerun at any time.

  python scripts/synth/compound_queue.py jobs [--equivalence]      # job list and worst-case cost, no submit
  python scripts/synth/compound_queue.py submit [--equivalence]
  python scripts/synth/compound_queue.py fetch
  python scripts/synth/compound_queue.py equivalence               # cluster vs VM tracks of the 2 check rods

Rods are rendered on the VM (heldout_compound.py render) and pushed whole: VM -> storage (tar over the held link,
md5 of every file checked) -> cluster (rsync over the master, file count checked). One array task per rendered
rod (the rod or its moved copy) runs every tracker run that rod needs, in sequence, 1 core, 1 h limit; an output
with its `.ok` marker is skipped, so a resubmitted task does only what is left. Fetch pulls each finished output
to storage (md5 on both ends), reads it to the VM and caches it only if its md5 matches storage.

Jobs: every label state of heldout_compound.label_states not cached, except register_frames states, held until
`register_v2` is on main (inbox item 5). `--equivalence`: the unremedied run of 2 rods already tracked on the VM,
into a separate folder; `equivalence` compares them (limit 1e-6 px, as 2026-10-23).
Settings: private/compound_cluster.yaml (own cluster work and code folders; the c027 ledger, cap and spend stop).
A down link or master prints `connection down` and exits 0 with no state change.
"""
import argparse
import hashlib
import io
import json
import shlex
import subprocess
import sys
import tarfile
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import retrack_queue as rq  # noqa: E402
import heldout_compound as hc  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

STATE = ROOT / "staging" / "c029_queue"
EQ_RODS = ("v3_growth_zone_drift_low_texture_s40", "v3_growth_zone_focus_drift_z3_s40")
EQ_DIR = STATE / "equivalence"
KIND = "c029"
rq.LIMITS[KIND] = "01:00:00"                  # one rendered rod's runs (about 26 x 2 min at most)
TASK_H = 1.0
FIELDS = ["job", "rid", "settings", "eq", "group", "array", "task", "state", "error", "md5", "fetched"]
q = shlex.quote


def config_path():
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()
    for p in (ROOT / "private" / "compound_cluster.yaml",
              (ROOT / common).resolve().parent / "private" / "compound_cluster.yaml"):
        if p.exists():
            return p
    sys.exit("private/compound_cluster.yaml missing")


# ------------------------------------------------------------------ job list

def job_rows(equivalence=False):
    """[{job, rid, settings, eq}]: one row per tracker run not cached."""
    hc.point_v3_here()
    rows = []
    if equivalence:
        st = TrackSettings(stride=1)
        for rid in EQ_RODS:
            name = f"{rid}__{st.tag()}.npz"
            if not (EQ_DIR / f"{name}.ok").exists():
                rows.append({"job": name, "rid": rid, "settings": json.dumps(asdict(st), sort_keys=True), "eq": "1"})
        return rows
    for rod in hc.scored_rods():
        states = [st for _, st in hc.label_states(rod) if st is not None]
        for st in hc.tracked([([], s) for s in states]):
            if st.register:
                continue                                      # held until register_v2 (inbox item 5)
            for moved in (False, True):
                rid = rod.id(moved)
                name = f"{rid}__{st.tag()}.npz"
                if Path(f"{hc.CACHE / name}.ok").exists():
                    continue
                rows.append({"job": name, "rid": rid, "settings": json.dumps(asdict(st), sort_keys=True), "eq": ""})
    return rows


def worst_case_usd(rows, rate=0.012):
    return round(rate * TASK_H * len({r["rid"] for r in rows}), 3)


def task_line(work, rid, rows):
    """One shell line: every run of one rendered rod, each skipped if its output is complete."""
    parts = []
    for r in rows:
        out = f"{work}/{'tracks_eq' if r['eq'] else 'tracks'}/{r['job']}"
        args = ["--imgdir", f"{work}/rods/{rid}.imgdir", "--midline", f"{work}/rods/{rid}_midline.npz",
                "--out", out] + TrackSettings(**json.loads(r["settings"])).args()
        parts.append(f"{{ test -f {q(out + '.ok')} || {{ test ! -e {q(out)} && python scripts/remote/qb_track.py "
                     + " ".join(q(a) for a in args) + f"; }} || {{ echo 'failed: {r['job']}' >&2; rc=1; }}; }}")
    return (f"rc=0; mkdir -p {q(work + '/tracks')} {q(work + '/tracks_eq')}; " + "; ".join(parts) + "; exit $rc")


# ------------------------------------------------------------------ moving rendered rods

def rod_files(rid):
    files = sorted((hc.RODS / f"{rid}.imgdir").iterdir()) + [hc.RODS / f"{rid}_midline.npz"]
    return {(f"{rid}.imgdir/{f.name}" if f.parent.name.endswith(".imgdir") else f.name): f for f in files}


def md5s(files):
    return {name: hashlib.md5(p.read_bytes()).hexdigest() for name, p in files.items()}


class RodMover:
    """VM -> storage -> cluster for rendered rods, over the runner's held link and the relay."""

    def __init__(self, runner, storage_dir):
        self.link, self.relay = runner.link, runner.relay
        self.sdir = storage_dir.rstrip("/") + "/rods"
        self.cdir = runner.ccfg["work_dir"].rstrip("/") + "/rods"

    def on_storage(self, rid):
        return self.link.run(f"test -f {q(self.sdir + '/' + rid + '.ok')} && echo yes || echo no").decode().strip() == "yes"

    def upload(self, rid):
        """Tar the rod's files to storage, check every file's md5 there, then write `<rid>.ok`."""
        files = rod_files(rid)
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for name, p in files.items():
                tar.add(p, arcname=name)
        self.link.run(f"mkdir -p {q(self.sdir)} && cd {q(self.sdir)} && tar xf -", stdin=buf.getvalue())
        want = md5s(files)
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
        return sum(sum(p.stat().st_size for p in rod_files(r).values()) for r in rids) / 2 ** 20


# ------------------------------------------------------------------ submit and fetch

def submit(runner, remote, mover, rows, state=STATE, log=print):
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
        name = f"c029_{gid}"
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


def local_path(row):
    return (EQ_DIR if row["eq"] else hc.CACHE) / row["job"]


def fetch(runner, remote, state=STATE, storage_dir=None, log=print):
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
                out = f"{work}/{'tracks_eq' if r['eq'] else 'tracks'}/{r['job']}"
                if remote.relay.run(f"test -f {q(out + '.ok')} && echo yes || echo no").decode().strip() != "yes":
                    tail = remote.err_tail("c029_" + r["group"], aid, r["task"])
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
                local = local_path(r)
                local.parent.mkdir(parents=True, exist_ok=True)
                tmp = local.with_suffix(".part")
                tmp.write_bytes(data)
                tmp.replace(local)
                Path(f"{local}.ok").touch()
                r["state"], r["md5"], r["fetched"], r["error"] = "fetched", md5, rq.now(), ""
                counts["fetched"] += 1
    except Exception as e:                                           # noqa: BLE001
        if type(e).__name__ in ("LinkDown", "MasterDown", "ConnectionDown"):
            rq.write_csv(state / "queue.csv", queue, FIELDS)
            log(f"connection down ({type(e).__name__}: {e}); fetched so far recorded")
            return "connection down"
        raise
    rq.write_csv(state / "queue.csv", queue, FIELDS)
    left = sum(r["state"] not in rq.FINAL for r in queue)
    msg = f"fetched {counts['fetched']}, failed {counts['failed']}, not finished {left}"
    log(msg)
    return msg


def equivalence():
    """Cluster tracks of the 2 check rods against their VM tracks."""
    from local_equivalence import compare
    out = []
    for rid in EQ_RODS:
        name = f"{rid}__{TrackSettings(stride=1).tag()}.npz"
        a, b = EQ_DIR / name, hc.CACHE / name
        if not a.exists():
            out.append({"rod": rid, "result": "cluster track not fetched"})
            continue
        c = compare(a, b)
        out.append({"rod": rid, "max_abs_diff": c["max_abs_diff"], "arrays": c["arrays"], "pass": c["max_abs_diff"] <= 1e-6})
    return out


def main(argv=None):
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["jobs", "submit", "fetch", "equivalence"])
    ap.add_argument("--equivalence", action="store_true")
    a = ap.parse_args(argv)
    STATE.mkdir(parents=True, exist_ok=True)
    if a.step == "equivalence":
        res = equivalence()
        (STATE / "equivalence.json").write_text(json.dumps(res, indent=1))
        print(json.dumps(res))
        return 0
    if a.step == "jobs":
        rows = job_rows(a.equivalence)
        print(f"{len(rows)} tracker runs, {len({r['rid'] for r in rows})} array tasks; worst case ${worst_case_usd(rows)}")
        return 0
    cfg = config_path()
    runner = rq.make_runner(cfg)
    remote = rq.Remote(runner)
    sdir = yaml.safe_load(cfg.read_text())["c029_storage_dir"]
    if a.step == "submit":
        if not a.equivalence and not (STATE / "equivalence.json").exists():
            sys.exit("equivalence first: submit --equivalence, fetch, equivalence")
        if not a.equivalence and not all(r.get("pass") for r in json.loads((STATE / "equivalence.json").read_text())):
            sys.exit("equivalence failed: stop, Needs Andrew")
        print(submit(runner, remote, RodMover(runner, sdir), job_rows(a.equivalence)))
    else:
        print(fetch(runner, remote, storage_dir=sdir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
