"""scripts/retrack_queue.py with a fake relay: no host is contacted (spec 2026-11-18 A1)."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import retrack_queue as RQ  # noqa: E402
from measure.cluster_compute import ClusterCompute, JobFailed  # noqa: E402
from measure.real_runner import RealRunner  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

WORK = "/cl/c027"


class FakeRunner:
    def __init__(self, cache):
        self.ccfg = {"work_dir": WORK, "cpu_partition": "cpu", "gpu_partition": "gpu", "gpu_gres": "gpu:1",
                     "env": "/cl/env.sh"}
        self.cc = ClusterCompute(None, self.ccfg, ledger=None)
        self.work, self.code, self.tracker, self.tag, self.track_length = "/st/c027", "/cl/code", "/cl/qb", "_ft2", 1000.0
        self.windows = {f"r{i}__w{a}-{a + 2}": {"imgdir": f"/st/movies/r{i}.imgdir", "midline": f"/st/mid/r{i}_{a}.npz"}
                        for i in (1, 2, 3) for a in (0, 10)}
        self.cache = Path(cache)
        self.moved_span, self.with_moved, self.moved_mode = (10.0, 12.0), True, "whole_pixel"

    cache_path = RealRunner.cache_path                             # the real cache names

    def cache_path_from_name(self, name):
        return self.cache / name

    def midline_path(self, w):
        return self.windows[w.id()]["midline"]


class FakeRemote:
    """In-memory cluster: tracks written by 'finished' tasks; md5 and link faults switchable."""

    def __init__(self, down=False, folder_mb=0, root_mb=5000, ledger_ok=True):
        self.down, self._folder, self._root, self.ledger_ok = down, folder_mb, root_mb, ledger_ok
        self.cluster_files, self.storage_files, self.states = {}, {}, {}
        self.calls, self.deleted, self.next_id = [], [], 100
        self.corrupt_vm, self.corrupt_storage = set(), set()

    def require(self):
        if self.down:
            raise RQ.ConnectionDown("link down")

    def folder_mb(self):
        return self._folder

    def root_mb(self, imgdir):
        return self._root

    def stage(self, root, imgdir):
        self.calls.append(("stage", root))

    def push_midline(self, src, dst):
        self.calls.append(("midline", dst))

    def write(self, path, text):
        self.cluster_files[path] = text.encode()

    def ledger(self, action, *args):
        self.calls.append(("ledger", action) + args)
        return (0, "ok") if self.ledger_ok or action != "check" else (1, "spent 11.9 + worst case 0.2 = 12.1 (cap")

    def sbatch(self, path):
        self.next_id += 1
        self.calls.append(("sbatch", path))
        return str(self.next_id)

    def sacct(self, array):
        return {t: (s, "00:02:00") for (a, t), s in self.states.items() if a == array}

    def err_tail(self, name, array, task):
        return "Traceback: boom"

    def pull(self, cluster_path, storage_dir):
        name = cluster_path.rsplit("/", 1)[1]
        if cluster_path not in self.cluster_files:
            raise JobFailed(f"missing {name}")
        if name in self.corrupt_storage:
            raise JobFailed(f"md5 mismatch after copying {name} to storage")
        stored = f"{storage_dir}/{name}"
        self.storage_files[stored] = self.cluster_files[cluster_path]
        return stored, hashlib.md5(self.storage_files[stored]).hexdigest()

    def storage_cat(self, path):
        data = self.storage_files[path]
        return data[:-1] if path.rsplit("/", 1)[1] in self.corrupt_vm else data

    def cluster_md5(self, path):
        return hashlib.md5(self.cluster_files[path]).hexdigest() if path in self.cluster_files else None

    def delete(self, path, why):
        self.deleted.append(path)
        return f"t deleted {path}"


def rows_for(runner, windows, settings=(TrackSettings(stride=2), TrackSettings(stride=1, register=True,
                                                                                 register_from_px=900))):
    out = []
    for wid in windows:
        for s in settings:
            out += RQ.job_rows(runner, RQ._window(wid), s)
    return out


@pytest.fixture
def setup(tmp_path):
    runner = FakeRunner(tmp_path / "cache")
    runner.cache.mkdir()
    return runner, tmp_path / "state"


def test_job_rows_moved_span_and_cache(setup):
    runner, _ = setup
    rows = rows_for(runner, ["r1__w0-2", "r1__w10-12"])
    assert [r["which"] for r in rows] == ["window", "window", "ref", "moved", "ref", "moved"]
    assert {r["kind"] for r in rows if '"register": true' in r["settings"]} == {"long"}
    (runner.cache / rows[0]["job"]).write_bytes(b"x")              # cached: left out
    assert len(rows_for(runner, ["r1__w0-2", "r1__w10-12"])) == 5


def test_single_remedies_from_schema():
    out = RQ.single_remedies(TrackSettings(stride=1), 15, record=None)
    names = {(r, s) for r, s, _ in out}
    # stride half: not available at stride 1; register: no record here; width-free: no tracker run
    assert names == {("change_frame_stride", "double"), ("smooth_midline", "light"),
                     ("crop_or_mask", "crop_to_main_root"), ("crop_or_mask", "mask_second_root"),
                     ("enlarge_patch", "1.5x"), ("enlarge_patch", "2x")}


def test_down_link_exit_0_no_state_change(setup, capsys):
    runner, state = setup
    up = FakeRemote()
    RQ.submit(runner, up, rows_for(runner, ["r1__w0-2"]), state=state, log=print)
    before = (state / "queue.csv").read_bytes()
    down = FakeRemote(down=True)
    assert RQ.fetch(runner, down, state=state) == "connection down"
    assert RQ.submit(runner, down, rows_for(runner, ["r2__w0-2"]), state=state) == "connection down"
    assert (state / "queue.csv").read_bytes() == before
    assert not list(runner.cache.iterdir())
    assert "connection down" in capsys.readouterr().out


def test_submit_groups_by_room_and_arrays(setup):
    runner, state = setup
    rem = FakeRemote(folder_mb=20000, root_mb=5000)                # room for 2 roots under 30 GB
    rows = rows_for(runner, ["r1__w0-2", "r2__w0-2", "r3__w10-12"])
    assert RQ.submit(runner, rem, rows, state=state) == "submitted g001"
    q = RQ.read_csv(state / "queue.csv")
    assert {r["root"] for r in q} == {"r1", "r2"}                  # r3 waits for room
    assert [c[1] for c in rem.calls if c[0] == "stage"] == ["r1", "r2"]
    assert {r["kind"] for r in q} == {"long", "short"}
    script = rem.cluster_files[f"{WORK}/jobs/c027_g001_long/job.sbatch"].decode()
    assert "#SBATCH --array=0-1%16" in script and "#SBATCH --time=00:45:00" in script and "%x_%A_%a.err" in script
    assert "--time=00:15:00" in rem.cluster_files[f"{WORK}/jobs/c027_g001_short/job.sbatch"].decode()
    tasks = rem.cluster_files[f"{WORK}/jobs/c027_g001_long/tasks.txt"].decode().splitlines()
    assert len(tasks) == 2 and all("--register-from-px 900" in t and t.startswith("test -s ") for t in tasks)
    # rerun: queued jobs are not submitted again; r3 goes into the next group
    rem._folder = 0
    assert RQ.submit(runner, rem, rows, state=state) == "submitted g002"
    q = RQ.read_csv(state / "queue.csv")
    assert len(q) == len(rows) + 1                                 # + one prep task for r3 w10-12
    prep = [r for r in q if r["kind"] == "prep"]
    assert len(prep) == 1 and f"--dependency=afterany:{prep[0]['array']}" in \
        rem.cluster_files[f"{WORK}/jobs/c027_g002_short/job.sbatch"].decode()
    assert RQ.submit(runner, rem, rows, state=state) == "nothing to submit"


def test_budget_stop_submits_nothing_more(setup):
    runner, state = setup
    rem = FakeRemote(ledger_ok=False)
    assert RQ.submit(runner, rem, rows_for(runner, ["r1__w0-2"]), state=state).startswith("budget stop")
    assert not [c for c in rem.calls if c[0] == "sbatch"]
    assert not (state / "queue.csv").exists()


def _run_group(runner, state, rem, windows):
    rows = rows_for(runner, windows)
    RQ.submit(runner, rem, rows, state=state)
    return RQ.read_csv(state / "queue.csv")


def test_partial_array_only_finished_pulled(setup):
    runner, state = setup
    rem = FakeRemote()
    q = _run_group(runner, state, rem, ["r1__w0-2", "r2__w0-2"])
    short = [r for r in q if r["kind"] == "short"]
    a = short[0]["array"]
    rem.cluster_files[f"{WORK}/tracks/{short[0]['job']}"] = b"track0"
    rem.states[(a, 0)] = "COMPLETED"
    rem.states[(a, 1)] = "RUNNING"
    long_ = [r for r in q if r["kind"] == "long"]
    rem.states[(long_[0]["array"], 0)] = "TIMEOUT"
    msg = RQ.fetch(runner, rem, state=state)
    assert msg.startswith("fetched 1, failed 1")
    assert sorted(p.name for p in runner.cache.iterdir()) == [short[0]["job"]]
    assert (runner.cache / short[0]["job"]).read_bytes() == b"track0"
    q2 = {r["job"]: r for r in RQ.read_csv(state / "queue.csv")}
    assert q2[short[1]["job"]]["state"] == "running"
    assert q2[long_[0]["job"]]["state"] == "failed" and q2[long_[0]["job"]]["error"].startswith("TIMEOUT")
    assert q2[long_[1]["job"]]["state"] == "pending"
    assert rem.deleted == []                                        # group not final: nothing cleared


def test_md5_mismatch_not_cached(setup):
    runner, state = setup
    rem = FakeRemote()
    q = _run_group(runner, state, rem, ["r1__w0-2"])
    short = [r for r in q if r["kind"] == "short"][0]
    long_ = [r for r in q if r["kind"] == "long"][0]
    for r in (short, long_):
        rem.cluster_files[f"{WORK}/tracks/{r['job']}"] = b"data-" + r["job"].encode()
        rem.states[(r["array"], 0)] = "COMPLETED"
    rem.corrupt_vm.add(short["job"])                               # storage -> VM copy differs
    rem.corrupt_storage.add(long_["job"])                          # cluster -> storage copy differs
    RQ.fetch(runner, rem, state=state)
    assert not list(runner.cache.iterdir())
    q2 = {r["job"]: r for r in RQ.read_csv(state / "queue.csv")}
    assert q2[short["job"]]["state"] == "completed" and "md5 mismatch" in q2[short["job"]]["error"]
    assert q2[long_["job"]]["state"] == "failed" and "md5 mismatch" in q2[long_["job"]]["error"]
    assert rem.deleted == []                                        # a completed-not-cached task keeps the group live
    rem.corrupt_vm.clear()                                          # fetch again: cached now
    RQ.fetch(runner, rem, state=state)
    assert [p.name for p in runner.cache.iterdir()] == [short["job"]]


def test_group_cleared_once_all_final(setup):
    runner, state = setup
    rem = FakeRemote()
    q = _run_group(runner, state, rem, ["r1__w10-12"])
    for r in q:
        if r["kind"] != "prep":
            rem.cluster_files[f"{WORK}/tracks/{r['job']}"] = r["job"].encode()
        rem.states[(r["array"], int(r["task"]))] = "COMPLETED"
    msg = RQ.fetch(runner, rem, state=state)
    assert msg.endswith("groups cleared g001")
    assert rem.deleted == [f"{WORK}/data/r1.imgdir", f"{WORK}/moved/r1__w10-12_wp_moved.imgdir",
                           f"{WORK}/moved/r1__w10-12_wp_ref.imgdir"]
    assert len((state / "deletes.jsonl").read_text().splitlines()) == 3
    RQ.fetch(runner, rem, state=state)                             # rerun: nothing deleted twice
    assert len(rem.deleted) == 3


def test_delete_refuses_outside_work():
    class R:
        cc = relay = link = None
        ccfg = {"work_dir": WORK}
        work = "/st"
    with pytest.raises(ValueError):
        RQ.Remote(R()).delete("/cl/other/data", "x")


def test_worst_case():
    rows = [{"kind": "short", "which": "window", "window": "a"}] * 4 + \
           [{"kind": "long", "which": "ref", "window": "b"}, {"kind": "long", "which": "moved", "window": "b"}]
    assert RQ.worst_case_usd(rows) == round(0.012 * (4 * 0.25 + 2 * 0.75 + 0.25), 3)


def test_paused_rows(setup, tmp_path):
    runner, _ = setup
    d = tmp_path / "run"
    d.mkdir()
    s = TrackSettings(stride=2, midline_smooth="light")
    (d / "paused.jsonl").write_text("\n".join(json.dumps({"window": w, "settings": s.to_dict()})
                                              for w in ("r1__w0-2", "r1__w0-2", "r2__w10-12")))
    rows = RQ.paused_rows(runner, d)
    assert [(r["window"], r["which"]) for r in rows] == [("r1__w0-2", "window"), ("r2__w10-12", "ref"),
                                                         ("r2__w10-12", "moved")]
