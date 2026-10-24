"""Run a plan of rods x tracker settings on the shared machine that has the tracker. No agent.

  python scripts/synth/sweep.py run    --plan plan.json --work DIR [--tracks tracks] [--rods DIR] [--workers 4]
  python scripts/synth/sweep.py status --work DIR
  python scripts/synth/sweep.py stop   --work DIR

plan.json: {"rods": [{"id": rod id, "options": [make_rod.py options],
                      "runs": [{"tag": t, "args": [qb_track.py options]}]}]}
Each rod is rendered once as is and once rigidly moved (skipped if present),
and each run is tracked on both into DIR/<tracks>/<id>__<tag>.npz (skipped
if present). One JSON line per tracker run on stdout. Run with the tracker
environment's Python. Plans are written by the sweep starters
(scripts/synth/repair_sweep.py, scripts/synth/fix_sweep.py).

Limits for the shared machine (docs/decisions.md, 2026-10-11), all built in:
- preflight: cores, load averages, available memory, free disk, size of the
  work space, this account's processes; logged as one JSON line
- start only if the 1 min load <= half the cores; else wait 15 min, three
  retries at most, then stop with status "load_too_high"
- at most 4 workers and never more than one eighth of the cores; one thread
  per worker (thread variables below); lowest CPU and I/O priority
- before each run: load above 3/4 of the cores holds new runs until it is
  under half
- one sweep at a time (lock file DIR/sweep.lock); `stop` ends the sweep and
  its workers
- after 10 runs: projected wall time; over --max-hours the sweep stops
- the space under --size-root is kept under --max-gb (checked before each
  run and projected after 10 runs)
- end: load before and after, peak workers, wall time, space before and after
Log lines hold numbers only: no host name, account or path.
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path

HERE = Path(__file__).resolve().parent
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
MAX_WORKERS = 4
LOAD_START, LOAD_PAUSE = 0.5, 0.75      # fractions of the core count
RETRY_S, RETRIES = 900, 3
PAUSE_POLL_S = 60
PROJECT_AFTER = 10


def single_thread_env():
    for v in THREAD_VARS:
        os.environ[v] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = ""          # no GPU


def lowest_priority():
    """Own process group, nice 19 and the idle I/O class; workers and tracker runs inherit all three."""
    os.setpgid(0, 0)
    os.setpriority(os.PRIO_PROCESS, 0, 19)
    if shutil.which("ionice"):
        subprocess.run(["ionice", "-c", "3", "-p", str(os.getpid())], capture_output=True, check=False)


def cores():
    return os.cpu_count() or 1


def load():
    return [round(x, 2) for x in os.getloadavg()]


def mem_available_gb():
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return round(int(line.split()[1]) / 2 ** 20, 1)
    except OSError:
        pass
    return None


def dir_bytes(path):
    total = 0
    for dp, _, files in os.walk(path):
        for f in files:
            try:
                total += os.lstat(os.path.join(dp, f)).st_size
            except OSError:
                pass
    return total


def own_processes():
    """This account's processes: count, and the command names (no arguments, so no paths)."""
    p = subprocess.run(["ps", "-u", str(os.getuid()), "-o", "comm="], capture_output=True, text=True)
    names = [n.strip() for n in p.stdout.splitlines() if n.strip() and n.strip() != "ps"]
    return {"n": len(names), "names": sorted(set(names))}


def max_workers(requested):
    return max(1, min(requested, MAX_WORKERS, cores() // 8))


def preflight(work, size_root):
    return {"preflight": True, "cores": cores(), "load_1_5_15": load(), "mem_available_gb": mem_available_gb(),
            "disk_free_gb": round(shutil.disk_usage(work).free / 2 ** 30, 1),
            "work_gb": round(dir_bytes(size_root) / 2 ** 30, 2), "own_processes": own_processes()}


# ------------------------------------------------------------------ lock

def lock_path(work):
    return Path(work) / "sweep.lock"


def read_lock(work):
    """The running sweep's lock dict, or None. A lock whose process is gone is stale and is ignored."""
    p = lock_path(work)
    if not p.exists():
        return None
    try:
        info = json.loads(p.read_text())
        os.kill(info["pid"], 0)
        return info
    except (ValueError, KeyError, ProcessLookupError, PermissionError):
        return None


def take_lock(work, plan_name):
    if read_lock(work):
        return False
    p = lock_path(work)
    p.unlink(missing_ok=True)                        # stale
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as fh:
        fh.write(json.dumps({"pid": os.getpid(), "pgid": os.getpgid(0), "plan": plan_name,
                             "started": time.strftime("%Y-%m-%d %H:%M:%S")}))
    return True


def release_lock(work):
    info = read_lock(work)
    if info is None or info["pid"] == os.getpid():
        lock_path(work).unlink(missing_ok=True)


# ------------------------------------------------------------------ worker

def wait_for_load():
    """Hold a new run while the 1 min load is above 3/4 of the cores, until it is under half."""
    n = cores()
    held = 0.0
    if os.getloadavg()[0] > LOAD_PAUSE * n:
        t0 = time.time()
        while os.getloadavg()[0] >= LOAD_START * n:
            time.sleep(PAUSE_POLL_S)
        held = time.time() - t0
    return round(held, 1)


def output_done(path):
    """A tracker output is complete when <path>.ok exists (qb_track.py writes it after the output; nothing on
    the lab server is renamed or overwritten, CLAUDE.md, spec audit rules-2)."""
    return Path(f"{path}.ok").exists()


def rod_done(rods, rid):
    """A rendered rod is complete when <rid>.ok exists (make_rod.py), or, for rods rendered before the .ok
    marker, when its truth file (written last) exists."""
    return (rods / f"{rid}.ok").exists() or (rods / f"{rid}_truth.npz").exists()


class Partial(Exception):
    """A file from a stopped run is in the way. It is left in place (no delete or overwrite) for Andrew."""


def _render(rods, options, rid):
    """Render a rod unless present. A per-rod file lock keeps two workers from rendering the same rod."""
    import fcntl
    with open(rods / f"{rid}.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        if not (rods / f"{rid}.imgdir").exists():
            subprocess.run([sys.executable, str(HERE / "make_rod.py"), "--out", str(rods)] + options,
                           check=True, capture_output=True, text=True)
        elif not rod_done(rods, rid):
            raise Partial(f"partial render left in place: {rid}")
    (rods / f"{rid}.lock").unlink(missing_ok=True)


def run_one(task):
    """One tracker run. task: rid, options, tag, args, rods, tracks."""
    rods, tracks = Path(task["rods"]), Path(task["tracks"])
    rid, name = task["rid"], f"{task['rid']}__{task['tag']}.npz"
    rec = {"id": rid, "tag": task["tag"]}
    if output_done(tracks / name):
        rec["cached"] = True
        return rec
    if (tracks / name).exists():
        rec.update(ok=False, partial=True, error=[f"partial output left in place, not overwritten: {name}"])
        return rec
    import resource
    rec["held_s"] = wait_for_load()
    try:
        _render(rods, task["options"], rid)
    except Partial as e:
        (rods / f"{rid}.lock").unlink(missing_ok=True)
        rec.update(ok=False, partial=True, error=[str(e)])
        return rec
    load0 = os.getloadavg()[0]
    ru0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    p = subprocess.run([sys.executable, str(HERE.parent / "remote" / "qb_track.py"),
                        "--imgdir", str(rods / f"{rid}.imgdir"),
                        "--midline", str(rods / f"{rid}_midline.npz"),
                        "--out", str(tracks / name)] + task["args"],
                       capture_output=True, text=True)
    wall = time.time() - t0
    ru1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (ru1.ru_utime - ru0.ru_utime) + (ru1.ru_stime - ru0.ru_stime)
    rec.update(ok=p.returncode == 0, s=round(wall, 1), cpu_s=round(cpu, 1),
               cpu_share=round(cpu / max(wall, 1e-9), 2), peak_mem_mb=round(ru1.ru_maxrss / 1024),
               load1_at_start=round(load0, 2), out_bytes=(tracks / name).stat().st_size if (tracks / name).exists() else 0)
    if p.returncode:
        rec["error"] = p.stderr.strip().splitlines()[-1:]
    return rec


def _init_worker():
    single_thread_env()
    signal.signal(signal.SIGINT, signal.SIG_IGN)


# ------------------------------------------------------------------ commands

def emit(d):
    print(json.dumps(d), flush=True)


def tasks_of(plan, rods, tracks):
    out = []
    for item in plan["rods"]:
        for moved in (False, True):
            opts = item["options"] + (["--moved"] if moved else [])
            rid = item.get("id")
            if rid is None:
                rid = json.loads(subprocess.run(
                    [sys.executable, str(HERE / "make_rod.py"), "--out", str(rods)] + opts + ["--dry-run"],
                    check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1])["id"]
            elif moved:
                rid = rid + "_moved"
            for run in item["runs"]:
                out.append({"rid": rid, "options": opts, "tag": run["tag"], "args": run["args"],
                            "rods": str(rods), "tracks": str(tracks)})
    return out


def cmd_run(a):
    single_thread_env()
    work = Path(a.work)
    tracks = work / a.tracks
    rods = Path(a.rods) if a.rods else work / "rods"
    size_root = Path(a.size_root) if a.size_root else work
    lowest_priority()
    if not take_lock(work, Path(a.plan).name):
        emit({"status": "refused", "reason": "another sweep is running"})
        return 2
    rods.mkdir(parents=True, exist_ok=True)
    tracks.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    stop = {"why": None}

    def on_term(signum, frame):
        raise SystemExit(f"signal {signum}")
    signal.signal(signal.SIGTERM, on_term)

    ex = None
    summary = {}
    try:
        pre = preflight(work, size_root)
        emit(pre)
        n = cores()
        tries = 0
        while pre["load_1_5_15"][0] > LOAD_START * n:
            if tries == RETRIES:
                emit({"status": "load_too_high", "load_1_5_15": load(), "cores": n, "tries": tries + 1})
                return 3
            tries += 1
            emit({"waiting_for_load_s": RETRY_S, "load_1_5_15": pre["load_1_5_15"], "try": tries})
            time.sleep(RETRY_S)
            pre = preflight(work, size_root)
            emit(pre)
        max_bytes = a.max_gb * 2 ** 30
        if pre["work_gb"] * 2 ** 30 > max_bytes:
            emit({"status": "space_limit", "work_gb": pre["work_gb"], "max_gb": a.max_gb})
            return 4
        plan = json.loads(Path(a.plan).read_text())
        tasks = tasks_of(plan, rods, tracks)
        todo = [t for t in tasks if not output_done(tracks / f"{t['rid']}__{t['tag']}.npz")]
        workers = max_workers(a.workers)
        summary.update(load_before=pre["load_1_5_15"], work_gb_before=pre["work_gb"], workers=workers,
                       runs_planned=len(tasks), runs_to_do=len(todo))
        emit({"start": True, "workers": workers, "runs_planned": len(tasks), "cached": len(tasks) - len(todo)})

        used = pre["work_gb"] * 2 ** 30
        rendered = set(p.name[:-7] for p in rods.glob("*.imgdir"))
        ex = ProcessPoolExecutor(workers, initializer=_init_worker)
        pending, queue = set(), list(todo)
        done_runs, t_runs, peak, samples = 0, time.time(), 0, []
        while queue or pending:
            while queue and len(pending) < workers and stop["why"] is None:
                if used > max_bytes:
                    stop["why"] = "space_limit"
                    break
                pending.add(ex.submit(run_one, queue.pop(0)))
            if not pending:
                break
            finished, pending = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
            peak = max(peak, len(pending) + len(finished))
            samples.append(os.getloadavg()[0])
            for f in finished:
                rec = f.result()
                emit(rec)
                if rec.get("cached"):
                    continue
                done_runs += 1
                used += rec.get("out_bytes", 0)
                if rec["id"] not in rendered and (rods / f"{rec['id']}.imgdir").exists():
                    rendered.add(rec["id"])
                    used += dir_bytes(rods / f"{rec['id']}.imgdir")
                if done_runs == PROJECT_AFTER:
                    per_run = (time.time() - t_runs) / PROJECT_AFTER
                    proj_h = per_run * len(todo) / 3600
                    grown = used - pre["work_gb"] * 2 ** 30
                    proj_gb = (used + grown / PROJECT_AFTER * (len(todo) - PROJECT_AFTER)) / 2 ** 30
                    emit({"projection": True, "runs_timed": PROJECT_AFTER, "wall_s_per_run": round(per_run, 1),
                          "projected_wall_h": round(proj_h, 2), "projected_work_gb": round(proj_gb, 2)})
                    if proj_h > a.max_hours:
                        stop["why"] = "projected_wall_time"
                    elif proj_gb > a.max_gb:
                        stop["why"] = "projected_space"
            if stop["why"] and queue:
                queue.clear()
        summary.update(status=stop["why"] or "done", runs_done=done_runs, peak_workers_busy=peak,
                       load1_during_max=round(max(samples), 2) if samples else None,
                       load1_during_median=round(sorted(samples)[len(samples) // 2], 2) if samples else None)
        return 0 if stop["why"] is None else 5
    except (SystemExit, BrokenProcessPool) as e:
        summary.update(status="stopped", reason=str(e) or type(e).__name__)
        return 6
    finally:
        if ex is not None:
            ex.shutdown(wait=summary.get("status") != "stopped", cancel_futures=True)
        if summary:
            summary.update(end=True, wall_s=round(time.time() - t_start), load_after=load(),
                           work_gb_after=round(dir_bytes(size_root) / 2 ** 30, 2))
            emit(summary)
        release_lock(work)


def sweep_processes(pgid):
    """Processes of the sweep's process group: pid and command name."""
    p = subprocess.run(["ps", "-u", str(os.getuid()), "-o", "pid=,pgid=,comm="], capture_output=True, text=True)
    out = []
    for line in p.stdout.splitlines():
        parts = line.split(None, 2)
        if len(parts) == 3 and int(parts[1]) == pgid:
            out.append({"pid": int(parts[0]), "comm": parts[2].strip()})
    return out


def cmd_status(a):
    info = read_lock(a.work)
    st = {"running": info is not None, "load_1_5_15": load(), "cores": cores()}
    if info:
        st.update(plan=info["plan"], started=info["started"], processes=len(sweep_processes(info["pgid"])))
    elif lock_path(a.work).exists():
        st["stale_lock"] = True
    emit(st)
    return 0


def cmd_stop(a):
    info = read_lock(a.work)
    if not info:
        emit({"stopped": False, "reason": "no sweep running"})
        return 0
    try:
        os.killpg(info["pgid"], signal.SIGTERM)          # main process logs the end; workers and tracker runs end
    except ProcessLookupError:
        pass
    for _ in range(30):
        if not sweep_processes(info["pgid"]):
            break
        time.sleep(1)
    left = sweep_processes(info["pgid"])
    for p in left:                                       # anything still alive in the sweep's group
        try:
            os.kill(p["pid"], signal.SIGKILL)
        except ProcessLookupError:
            pass
    time.sleep(1)
    if read_lock(a.work) is None:
        lock_path(a.work).unlink(missing_ok=True)
    emit({"stopped": True, "killed_after_30s": len(left), "left": len(sweep_processes(info["pgid"]))})
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--plan", required=True)
    r.add_argument("--work", required=True)
    r.add_argument("--tracks", default="tracks", help="tracker outputs, under --work")
    r.add_argument("--rods", default=None, help="rendered rods (default --work/rods)")
    r.add_argument("--size-root", default=None, help="directory whose size is limited (default --work)")
    r.add_argument("--workers", type=int, default=MAX_WORKERS)
    r.add_argument("--max-hours", type=float, default=2.0)
    r.add_argument("--max-gb", type=float, default=10.0)
    for name in ("status", "stop"):
        s = sub.add_parser(name)
        s.add_argument("--work", required=True)
    a = ap.parse_args()
    return {"run": cmd_run, "status": cmd_status, "stop": cmd_stop}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
