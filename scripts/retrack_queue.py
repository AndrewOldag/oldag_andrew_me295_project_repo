"""Task c027 (spec 2026-11-18 A): retracks on the cluster, submit and forget. No agent or tree step waits on the cluster.

  python scripts/retrack_queue.py seed                          # c026 cached tracks -> the c027 cache (VM copy)
  python scripts/retrack_queue.py jobs --wave 1 --out staging/c027/wave1.csv   # job list, count, worst-case cost
  python scripts/retrack_queue.py jobs --paused RUN_DIR --out staging/c027/wave2.csv   # settings paused windows need
  python scripts/retrack_queue.py submit --jobs staging/c027/wave1.csv
  python scripts/retrack_queue.py fetch

jobs    Wave 1 (A2): for the 84 batch-2 windows that fail closure, every single remedy setting of the action schema
        (agents/actions.py REMEDIES) applied to the base settings through measure/remedies.apply_remedy; a setting
        the schema cannot apply (NotAvailable) or that names no new tracker run (use_width_free_ratio) is skipped.
        Windows in the moved-copy span (10-12 h) also get the reference and moved-copy tracks of each setting. Rows
        already in the cache are left out. register_frames reads its band start from the cached base track.
submit  Jobs not in the cache and not already queued, by root, in groups whose staged roots keep the cluster folder
        under the cap (30 GB). Per group: stage each root imgdir whole (the tracker loader needs every frame file,
        decisions 2026-10-25), push the window midlines, then one Slurm array per kind: `prep` (moved copies),
        `long` (register_frames, 45 min) and `short` (15 min), 1 core each; track arrays start after `prep`
        (afterany; a task whose copy is missing fails with its reason). The ledger checks every array before
        `sbatch --parsable`. Array ids go to staging/c027/queue.csv. Groups that do not fit wait for the next submit.
fetch   sacct state of every recorded array. A finished track is pulled to storage (md5 on both ends), read to the
        VM and cached only if its md5 matches storage. Failed tasks are marked with their state and error. A group
        whose tasks are all final has its staged roots and moved copies cleared, each delete logged in DELETED.log
        of the cluster work folder (standing rule: outputs md5-checked on storage first).
Both submit and fetch can be rerun at any time. A down link or master prints `connection down` and exits 0, with
no state change; nothing waits or retries in a loop.
"""
import argparse
import csv
import datetime
import hashlib
import json
import re
import shlex
import sys
from collections import OrderedDict
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from agents.actions import REMEDIES  # noqa: E402
from measure.remedies import NotAvailable, TrackSettings, apply_remedy  # noqa: E402

STATE = ROOT / "staging" / "c027"
CONFIG = ROOT / "private" / "real_runner_c027.yaml"
C026_CACHE = ROOT / "staging" / "c026" / "tracks"
C026_TREE = ROOT / "staging" / "c026" / "tree" / "windows"
CAP_MB = 30 * 1024
LIMITS = {"prep": "00:15:00", "long": "00:45:00", "short": "00:15:00"}   # spec A1: register_frames 45 min
ARRAY_THROTTLE = 16
JOB_FIELDS = ["job", "window", "root", "from_h", "to_h", "which", "kind", "settings"]
QUEUE_FIELDS = JOB_FIELDS + ["group", "array", "task", "state", "error", "md5", "fetched"]
FINAL = ("fetched", "failed", "done")
q = shlex.quote


class ConnectionDown(RuntimeError):
    pass


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def read_csv(path):
    if not Path(path).exists():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)
    tmp.replace(path)


def settings_of(row):
    return TrackSettings(**json.loads(row["settings"]))


# ---- job lists
def single_remedies(base, base_disk_radius, record):
    """[(remedy, setting, TrackSettings)] for every single remedy in the schema that names a new tracker run."""
    out = []
    for remedy, settings in REMEDIES.items():
        for s in settings:
            try:
                new, _ = apply_remedy(base, remedy, s, base_disk_radius, record)
            except NotAvailable:
                continue
            if new.tag() != base.tag():          # use_width_free_ratio: no tracker run
                out.append((remedy, s, new))
    return out


def job_rows(runner, window, settings, cache_dirs=()):
    """Rows for one window and settings: the window track, or (moved-copy span) the reference and moved copy.
    A row whose track is in the cache (or one of `cache_dirs`) is left out."""
    span = runner.moved_span is None or (window.from_h, window.to_h) == runner.moved_span
    kinds = ["ref", "moved"] if runner.with_moved and span else ["window"]
    rows = []
    for which in kinds:
        local = runner.cache_path(window, settings, which)
        if local.exists() or any((Path(d) / local.name).exists() for d in cache_dirs):
            continue
        rows.append({"job": local.name, "window": window.id(), "root": window.root_id, "from_h": f"{window.from_h:g}",
                     "to_h": f"{window.to_h:g}", "which": which, "kind": "long" if settings.register else "short",
                     "settings": json.dumps(asdict(settings), sort_keys=True)})
    return rows


def wave1(runner, windows):
    """Spec A2: every single remedy on base settings for each window; base record from the cache."""
    from measure.record import from_tracker_npz
    rows = []
    for w in windows:
        base = runner.initial_settings(w)
        main = "ref" if runner.with_moved and (w.from_h, w.to_h) == runner.moved_span else "window"
        p = runner.cache_path(w, base, main)
        if not p.exists():
            raise FileNotFoundError(f"{w.id()}: base track {p.name} not in the cache (run `seed` first)")
        rec = from_tracker_npz(p, root_id=w.id())
        r0 = int(rec.settings.get("disk_radius") or 15)            # as agents/executors.Slice
        for _, _, s in single_remedies(base, r0, rec):
            rows += job_rows(runner, w, s)
    return rows


def paused_rows(runner, run_dir):
    """Rows for the settings paused windows of a run need (RUN_DIR/paused.jsonl: window, settings dict)."""
    from measure.real_runner import RealWindow
    rows, seen = [], set()
    p = Path(run_dir) / "paused.jsonl"
    for line in (p.read_text().splitlines() if p.exists() else []):
        d = json.loads(line)
        root, span = d["window"].split("__w")
        a, b = span.split("-")
        w = RealWindow(root, float(a), float(b))
        for r in job_rows(runner, w, TrackSettings(**d["settings"])):
            if r["job"] not in seen:
                seen.add(r["job"])
                rows.append(r)
    return rows


def worst_case_usd(rows, rate=0.012):
    """Ledger rule (1 core x time limit x rate per core-hour), with one prep task per moved-copy window."""
    h = {"prep": 0.25, "long": 0.75, "short": 0.25}
    n_prep = len({r["window"] for r in rows if r["which"] != "window"})
    return round(rate * (sum(h[r["kind"]] for r in rows) + h["prep"] * n_prep), 3)


# ---- cluster side
class Remote:
    """The cluster and storage steps submit and fetch need, over the runner's one held link and the relay."""

    def __init__(self, runner):
        self.r = runner
        self.cc, self.relay, self.link = runner.cc, runner.relay, runner.link
        self.work = runner.ccfg["work_dir"]
        self.storage = runner.work

    def require(self):
        """Link and master up, else ConnectionDown."""
        try:
            ok = self.relay.master_ok()
        except Exception as e:                                       # noqa: BLE001 - LinkDown or a dropped channel
            raise ConnectionDown(f"{type(e).__name__}: {e}") from e
        if not ok:
            raise ConnectionDown("cluster master down")

    def folder_mb(self):
        return self.cc.folder_mb()

    def root_mb(self, imgdir):
        return int(self.link.run(f"du -sm {q(imgdir)} | cut -f1").decode().split()[0])

    def stage(self, root, imgdir):
        return self.cc.stage_root(root, imgdir)

    def push_midline(self, storage_path, cluster_path):
        if self.relay.run(f"test -s {q(cluster_path)} && echo yes || echo no").decode().strip() != "yes":
            self.cc.push_file(storage_path, cluster_path)

    def write(self, path, text):
        self.relay.run(f"mkdir -p {q(path.rsplit('/', 1)[0])} && cat > {q(path)}", stdin=text)

    def ledger(self, *args):
        return self.cc.ledger(*args)

    def sbatch(self, path):
        jid = self.relay.run(f"sbatch --parsable {q(path)}").decode().strip().split(";")[0]
        if not jid.isdigit():
            raise RuntimeError(f"sbatch said {jid!r}")
        return jid

    def sacct(self, array):
        """{task index: (state, elapsed)} for one array; pending tasks may show as one line `ID_[a-b]`."""
        out = self.relay.run(f"sacct -j {q(array)} -X -n -P -o JobID,State,Elapsed", check=False).decode()
        res = {}
        for line in out.splitlines():
            p = line.strip().split("|")
            if len(p) < 3:
                continue
            m = re.fullmatch(rf"{array}_(\d+)", p[0])
            if m:
                res[int(m.group(1))] = (p[1].split()[0], p[2])
        return res

    def err_tail(self, name, array, task):
        return self.relay.run(f"tail -3 {q(self.work)}/logs/{q(name)}_{array}_{task}.err 2>/dev/null",
                              check=False).decode(errors="replace").strip()[-300:]

    def pull(self, cluster_path, storage_dir):
        """Copy to storage; md5 on both ends (raises on mismatch). Returns (storage path, md5)."""
        stored = self.cc.pull(cluster_path, storage_dir)
        return stored, self.storage_md5(stored)

    def storage_md5(self, path):
        return self.link.run(f"md5sum < {q(path)}").decode().split()[0]

    def storage_cat(self, path):
        return self.link.run(f"cat {q(path)}")

    def cluster_md5(self, path):
        out = self.relay.run(f"md5sum < {q(path)} 2>/dev/null", check=False).decode().split()
        return out[0] if out else None

    def delete(self, path, why):
        """Delete one cluster path (own work folder only) and log it; returns the log line or ''."""
        if not path.startswith(self.work + "/"):
            raise ValueError(f"refused: {path} is outside the c027 work folder")
        return self.relay.run(f"if [ -e {q(path)} ]; then s=$(du -sh {q(path)} | cut -f1); t=$(date -Is); "
                              f"rm -r {q(path)} && echo \"$t deleted {path} $s; {why}\" >> {q(self.work)}/DELETED.log "
                              f"&& echo \"$t $s\"; fi").decode().strip()


def cluster_paths(work, tag, row):
    """Input image folder, midline and output of one row on the cluster."""
    wid = row["window"]
    if row["which"] == "window":
        return f"{work}/data/{row['root']}.imgdir", f"{work}/midline/{wid}{tag}_netmid.npz", f"{work}/tracks/{row['job']}"
    k = row["which"]
    return (f"{work}/moved/{wid}_wp_{k}.imgdir", f"{work}/moved/{wid}{tag}_wp_{k}_midline.npz",
            f"{work}/tracks/{row['job']}")


def task_command(runner, row):
    """One shell line for an array task (run in the code folder with PYTHONPATH set)."""
    work, tag = runner.ccfg["work_dir"], runner.tag
    if row["which"] == "prep":
        wid = row["window"]
        mv = {k: f"{work}/moved/{wid}_wp_{k}.imgdir" for k in ("moved", "ref")}
        mm = {k: f"{work}/moved/{wid}{tag}_wp_{k}_midline.npz" for k in ("moved", "ref")}
        args = ["--imgdir", f"{work}/data/{row['root']}.imgdir", "--midline", f"{work}/midline/{wid}{tag}_netmid.npz",
                "--from-h", row["from_h"], "--to-h", row["to_h"], "--out-imgdir", mv["moved"], "--out-midline",
                mm["moved"], "--mode", "whole_pixel", "--out-ref-imgdir", mv["ref"], "--out-ref-midline", mm["ref"]]
        done = " && ".join(f"test -f {q(mv[k] + '.ok')} && test -f {q(mm[k])}" for k in mv)
        return f"{{ {done}; }} || python scripts/remote/real_moved.py " + " ".join(q(a) for a in args)
    img, mid, out = cluster_paths(work, tag, row)
    args = (["--imgdir", img, "--midline", mid, "--out", out, "--movie", "real", "--from-h", row["from_h"],
             "--to-h", row["to_h"], "--track-length", f"{runner.track_length:g}"] + settings_of(row).args())
    need = f"test -f {q(img + '.ok')} || {{ echo 'moved copy missing: {row['window']} {row['which']}' >&2; exit 3; }}; " \
        if row["which"] != "window" else ""
    return f"{need}test -s {q(out)} || python scripts/remote/qb_track.py " + " ".join(q(a) for a in args)


def array_script(runner, name, tasks_path, n, kind, after=None):
    cc = runner.cc
    body = (f"cd {q(runner.code)} && export PYTHONPATH={q(runner.tracker)}:{q(runner.code)}\n"
            f"cmd=$(sed -n \"$((SLURM_ARRAY_TASK_ID + 1))p\" {q(tasks_path)})\n"
            f"test -n \"$cmd\" || {{ echo 'no task line' >&2; exit 2; }}\n"
            f"bash -c \"$cmd\"")
    text = cc.script(name, body, cpus=1, time_limit=LIMITS[kind])
    extra = [f"#SBATCH --array=0-{n - 1}%{ARRAY_THROTTLE}"] + ([f"#SBATCH --dependency=afterany:{after}"] if after else [])
    lines = text.replace("%x_%j.", "%x_%A_%a.").split("\n")
    return "\n".join(lines[:2] + extra + lines[2:])


def pack_groups(roots_mb, room_mb):
    """[(root, MB)] in order -> groups of whole roots; the first groups that fit in `room_mb` are returned, the
    rest wait. A root bigger than the room alone is left for later."""
    groups, cur, used = [], [], 0
    for root, mb in roots_mb:
        if used + mb > room_mb:
            break
        cur.append(root)
        used += mb
    if cur:
        groups.append(cur)
    return groups


def submit(runner, remote, job_rows_, state=STATE, cap_mb=CAP_MB, log=print):
    """Returns a one-line status. See the module docstring."""
    try:
        remote.require()
    except ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    queue = read_csv(state / "queue.csv")
    queued = {r["job"] for r in queue if r["state"] != "failed"}
    todo = [r for r in job_rows_ if r["job"] not in queued and not runner.cache_path_from_name(r["job"]).exists()]
    if not todo:
        log("nothing to submit")
        return "nothing to submit"
    by_root = OrderedDict()
    for r in todo:
        by_root.setdefault(r["root"], []).append(r)
    live_groups = {r["group"] for r in queue if r["state"] not in FINAL}
    try:
        room = cap_mb - remote.folder_mb()
        sizes = [(root, remote.root_mb(runner.windows[rows[0]["window"]]["imgdir"])) for root, rows in by_root.items()]
        groups = pack_groups(sizes, room)
        if not groups:
            log(f"no room: {room} MB free under the {cap_mb} MB cap; {len(todo)} jobs wait ({len(live_groups)} "
                "groups still on the cluster; fetch clears finished groups)")
            return "no room"
        work, tag = runner.ccfg["work_dir"], runner.tag
        gid = f"g{1 + max([int(r['group'][1:]) for r in queue] or [0]):03d}"
        rows = [r for root in groups[0] for r in by_root[root]]
        for root in groups[0]:
            remote.stage(root, runner.windows[by_root[root][0]["window"]]["imgdir"])
        for wid in sorted({r["window"] for r in rows}):
            remote.push_midline(runner.midline_path(_window(wid)), f"{work}/midline/{wid}{tag}_netmid.npz")
        prep = [{**{k: r[k] for k in ("window", "root", "from_h", "to_h")}, "job": f"prep_{r['window']}",
                 "which": "prep", "kind": "prep", "settings": ""}
                for r in {r["window"]: r for r in rows if r["which"] != "window"}.values()]
        arrays, prep_id = [], None
        for kind, rs in (("prep", prep), ("long", [r for r in rows if r["kind"] == "long"]),
                         ("short", [r for r in rows if r["kind"] == "short"])):
            if not rs:
                continue
            name = f"c027_{gid}_{kind}"
            job_dir = f"{work}/jobs/{name}"
            remote.write(f"{job_dir}/tasks.txt", "".join(task_command(runner, r) + "\n" for r in rs))
            remote.write(f"{job_dir}/job.sbatch", array_script(runner, name, f"{job_dir}/tasks.txt", len(rs), kind,
                                                                 after=prep_id if kind != "prep" else None))
            rc, msg = remote.ledger("check", job_dir)
            if rc != 0:
                log(f"ledger refused {name}: {msg}")
                _save_submitted(state, queue, arrays)
                return f"budget stop: {msg}"
            aid = remote.sbatch(f"{job_dir}/job.sbatch")
            remote.ledger("record", job_dir, aid)
            if kind == "prep":
                prep_id = aid
            arrays += [{**r, "group": gid, "array": aid, "task": str(i), "state": "submitted", "error": "",
                        "md5": "", "fetched": ""} for i, r in enumerate(rs)]
            log(f"{name}: array {aid}, {len(rs)} tasks")
    except ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    except Exception as e:                                           # noqa: BLE001 - lost link mid-submit
        if type(e).__name__ in ("LinkDown", "MasterDown"):
            _save_submitted(state, queue, arrays)
            log(f"connection down ({type(e).__name__}: {e}); submitted arrays recorded")
            return "connection down"
        raise
    _save_submitted(state, queue, arrays)
    waiting = len(todo) - len(rows)
    log(f"group {gid}: {len(groups[0])} roots, {len(rows)} track tasks, {len(prep)} prep tasks; {waiting} jobs wait")
    return f"submitted {gid}"


def _save_submitted(state, queue, arrays):
    if arrays:
        write_csv(state / "queue.csv", queue + arrays, QUEUE_FIELDS)
        with open(state / "groups.jsonl", "a") as f:
            f.write(json.dumps({"group": arrays[0]["group"], "time": now(),
                                "roots": sorted({r["root"] for r in arrays}),
                                "arrays": sorted({r["array"] for r in arrays})}) + "\n")


def _window(wid):
    from measure.real_runner import RealWindow
    root, span = wid.split("__w")
    a, b = span.split("-")
    return RealWindow(root, float(a), float(b))


def fetch(runner, remote, state=STATE, log=print):
    """Returns a one-line status. See the module docstring."""
    queue = read_csv(state / "queue.csv")
    if not queue:
        log("queue empty")
        return "queue empty"
    try:
        remote.require()
    except ConnectionDown as e:
        log(f"connection down ({e})")
        return "connection down"
    work = runner.ccfg["work_dir"]
    counts = {"fetched": 0, "failed": 0, "running": 0}
    try:
        for aid in sorted({r["array"] for r in queue if r["state"] not in FINAL}):
            states = remote.sacct(aid)
            for r in queue:
                if r["array"] != aid or r["state"] in FINAL:
                    continue
                st, _ = states.get(int(r["task"]), ("PENDING", ""))
                if st in ("PENDING", "RUNNING", "REQUEUED", "CONFIGURING", "SUSPENDED", "COMPLETING"):
                    r["state"] = st.lower()
                    counts["running"] += 1
                    continue
                name = f"c027_{r['group']}_{r['kind']}"
                if st != "COMPLETED":
                    r["state"], r["error"] = "failed", f"{st}: {remote.err_tail(name, aid, r['task'])}"
                    counts["failed"] += 1
                    continue
                if r["which"] == "prep":
                    r["state"], r["fetched"] = "done", now()
                    continue
                try:
                    stored, md5 = remote.pull(f"{work}/tracks/{r['job']}", f"{runner.work}/tracks")
                except Exception as e:                               # noqa: BLE001 - md5 mismatch or missing output
                    if type(e).__name__ in ("LinkDown", "MasterDown"):
                        raise
                    r["state"], r["error"] = "failed", f"pull: {str(e)[:200]}"
                    counts["failed"] += 1
                    continue
                data = remote.storage_cat(stored)
                if hashlib.md5(data).hexdigest() != md5:
                    r["state"], r["error"] = "completed", "md5 mismatch storage -> VM; not cached (fetch again)"
                    continue
                local = runner.cache_path_from_name(r["job"])
                tmp = local.with_suffix(".part")
                tmp.write_bytes(data)
                tmp.replace(local)
                r["state"], r["md5"], r["fetched"], r["error"] = "fetched", md5, now(), ""
                counts["fetched"] += 1
        cleared = clear_groups(remote, queue, state, work)
    except Exception as e:                                           # noqa: BLE001
        if type(e).__name__ in ("LinkDown", "MasterDown", "ConnectionDown"):
            write_csv(state / "queue.csv", queue, QUEUE_FIELDS)      # what was fetched before the drop is kept
            log(f"connection down ({type(e).__name__}: {e}); fetched so far recorded")
            return "connection down"
        raise
    write_csv(state / "queue.csv", queue, QUEUE_FIELDS)
    left = sum(r["state"] not in FINAL for r in queue)
    msg = (f"fetched {counts['fetched']}, failed {counts['failed']}, not finished {left}; groups cleared "
           f"{', '.join(cleared) or 'none'}")
    log(msg)
    return msg


def clear_groups(remote, queue, state, work):
    """Clear staged roots and moved copies of groups whose tasks are all final, once every fetched output is
    md5-equal on the cluster and on storage. A root still used by a live group is kept."""
    done_path = state / "cleared.txt"
    done = set(done_path.read_text().split()) if done_path.exists() else set()
    groups = OrderedDict()
    for r in queue:
        groups.setdefault(r["group"], []).append(r)
    live_roots = {r["root"] for g, rs in groups.items() for r in rs if any(x["state"] not in FINAL for x in rs)}
    cleared = []
    for g, rs in groups.items():
        if g in done or any(r["state"] not in FINAL for r in rs):
            continue
        for r in rs:
            if r["state"] == "fetched" and remote.cluster_md5(f"{work}/tracks/{r['job']}") not in (r["md5"], None):
                raise RuntimeError(f"{g}: {r['job']} differs between cluster and storage; staged copies kept")
        why = f"c027 group {g}: outputs md5-checked on storage (spec 2026-11-18 A1)"
        lines = []
        for root in sorted({r["root"] for r in rs} - live_roots):
            lines.append(remote.delete(f"{work}/data/{root}.imgdir", why))
        for wid in sorted({r["window"] for r in rs if r["which"] == "prep"}):
            for k in ("moved", "ref"):
                lines.append(remote.delete(f"{work}/moved/{wid}_wp_{k}.imgdir", why))
        with open(state / "deletes.jsonl", "a") as f:
            for line in filter(None, lines):
                f.write(json.dumps({"group": g, "log": line}) + "\n")
        with open(done_path, "a") as f:
            f.write(g + "\n")
        cleared.append(g)
    return cleared


# ---- runner
def make_runner(config=CONFIG):
    import yaml
    from measure.real_runner import RealRunner
    from measure.remote_link import Link
    cfg = yaml.safe_load(Path(config).read_text())
    runner = RealRunner(cfg, link=Link(cfg["storage_host"], sleep=lambda s: None))   # never wait on a down link
    runner.moved_span = (10.0, 12.0)
    runner.cache_path_from_name = lambda name: runner.cache / name
    return runner


def seed(runner, src=C026_CACHE):
    n = 0
    for p in sorted(Path(src).glob("*.npz")):
        dst = runner.cache / p.name
        if not dst.exists():
            dst.write_bytes(p.read_bytes())
            n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["seed", "jobs", "submit", "fetch"])
    ap.add_argument("--config", default=str(CONFIG))
    ap.add_argument("--wave", type=int)
    ap.add_argument("--paused", help="jobs: a run folder with paused.jsonl")
    ap.add_argument("--jobs", nargs="+", help="submit: job list CSV files")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    runner = make_runner(a.config)
    if a.step == "seed":
        print(f"seeded {seed(runner)} tracks from the c026 cache")
        return 0
    if a.step == "jobs":
        if a.wave == 1:
            from batch2_agents import failing_windows
            ws = [w for w, _ in failing_windows()]
            reached = {p.stem for p in C026_TREE.glob("*.json")}
            rows = wave1(runner, ws)
            n_new = sum(r["window"] not in reached for r in rows)
            print(f"windows: {len(ws)} ({len(ws) - len(reached)} not reached by the c026 tree)")
            print(f"jobs: {len(rows)} ({n_new} for unreached windows, {len(rows) - n_new} for reached windows); "
                  f"long {sum(r['kind'] == 'long' for r in rows)}, moved-copy windows "
                  f"{len({r['window'] for r in rows if r['which'] != 'window'})}")
        else:
            rows = paused_rows(runner, a.paused)
            print(f"jobs: {len(rows)} from {a.paused}")
        print(f"worst case: ${worst_case_usd(rows):.3f} (1 core x time limit x $0.012 per core-hour)")
        write_csv(a.out, rows, JOB_FIELDS)
        return 0
    remote = Remote(runner)
    if a.step == "submit":
        rows = [r for p in a.jobs for r in read_csv(p)]
        status = submit(runner, remote, rows)
    else:
        status = fetch(runner, remote)
    with open(STATE / "queue_log.jsonl", "a") as f:
        f.write(json.dumps({"time": now(), "step": a.step, "status": status,
                            "link": [list(e) for e in runner.link.events]}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
