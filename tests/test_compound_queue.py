"""c029 cluster queue (scripts/synth/compound_queue.py) with a fake cluster: no host, no link."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "synth"))
sys.path.insert(0, str(ROOT / "scripts"))
import compound_queue as cq  # noqa: E402
import retrack_queue as rq  # noqa: E402

WORK = "/cluster/c029"


class Out:
    def __init__(self, text):
        self.text = text

    def decode(self, *a, **k):
        return self.text


class FakeRelay:
    def __init__(self, ok=()):
        self.ok, self.cmds = set(ok), []

    def run(self, cmd, stdin=None, check=True):
        self.cmds.append(cmd)
        if cmd.startswith("test -f"):
            return Out("yes" if any(o in cmd for o in self.ok) else "no")
        return Out("")


class FakeRemote:
    def __init__(self, down=False, sacct=None, outputs=None, storage_bad=False, ok=()):
        self.down, self._sacct, self.outputs = down, sacct or {}, outputs or {}
        self.storage_bad, self.relay = storage_bad, FakeRelay(ok)
        self.written, self.sbatched, self.ledger_calls = {}, [], []

    def require(self):
        if self.down:
            raise rq.ConnectionDown("link down")

    def folder_mb(self):
        return 100

    def write(self, path, text):
        self.written[path] = text

    def ledger(self, *a):
        self.ledger_calls.append(a)
        return 0, "ok"

    def sbatch(self, path):
        self.sbatched.append(path)
        return "4242"

    def sacct(self, aid):
        return self._sacct

    def err_tail(self, *a):
        return "err"

    def pull(self, path, sdir):
        name = path.rsplit("/", 1)[1]
        return f"{sdir}/{name}", hashlib.md5(self.outputs[name]).hexdigest()

    def storage_cat(self, path):
        data = self.outputs[path.rsplit("/", 1)[1]]
        return data + b"x" if self.storage_bad else data


class FakeRunner:
    ccfg = {"work_dir": WORK, "cap_mb": 30 * 1024}
    code, tracker = "/cluster/code", "/cluster/tracker"
    synced = 0

    def sync_code(self):
        self.synced += 1

    class cc:
        @staticmethod
        def script(name, body, cpus=1, time_limit="", mem="16G"):
            return f"#!/bin/bash\n#SBATCH --time={time_limit}\n{body}"


class FakeMover:
    def __init__(self):
        self.uploaded, self.pushed = [], []

    def on_storage(self, rid):
        return False

    def upload(self, rid):
        self.uploaded.append(rid)
        return 3

    def push(self, rids):
        self.pushed += rids

    def mb(self, rids):
        return 20.0


def row(rid, tag, eq=""):
    st = {"stride": 1} if tag == "st1" else {"stride": 2}
    return {"job": f"{rid}__{tag}.npz", "rid": rid, "settings": json.dumps(st), "eq": eq}


@pytest.fixture
def rows():
    return [row("rodA", "st1"), row("rodA", "st2"), row("rodA_moved", "st1")]


def test_task_line_skips_finished_and_keeps_going(rows):
    line = cq.task_line(WORK, "rodA", rows[:2])
    assert line.count("qb_track.py") == 2 and line.endswith("exit $rc")
    assert f"test -f {WORK}/tracks/rodA__st1.npz.ok" in line
    assert f"--imgdir {WORK}/rods/rodA.imgdir" in line and "--stride 2" in line
    assert "rm " not in line                                 # a partial output is reported, never deleted


def test_submit_connection_down_changes_nothing(tmp_path, rows):
    r = cq.submit(FakeRunner(), FakeRemote(down=True), FakeMover(), rows, state=tmp_path, log=lambda m: None)
    assert r == "connection down" and not (tmp_path / "queue.csv").exists()


def test_submit_one_task_per_rendered_rod(tmp_path, rows):
    remote, mover, runner = FakeRemote(), FakeMover(), FakeRunner()
    r = cq.submit(runner, remote, mover, rows, state=tmp_path, log=lambda m: None)
    assert r == "submitted g001" and runner.synced == 1
    assert mover.uploaded == ["rodA", "rodA_moved"] and mover.pushed == ["rodA", "rodA_moved"]
    tasks = remote.written[f"{WORK}/jobs/c029_g001/tasks.txt"].splitlines()
    assert len(tasks) == 2 and tasks[0].count("qb_track.py") == 2
    assert "--time=01:00:00" in remote.written[f"{WORK}/jobs/c029_g001/job.sbatch"]
    assert [c[0] for c in remote.ledger_calls] == ["check", "record"]
    q = rq.read_csv(tmp_path / "queue.csv")
    assert [(x["job"], x["task"]) for x in q] == [("rodA__st1.npz", "0"), ("rodA__st2.npz", "0"),
                                                   ("rodA_moved__st1.npz", "1")]
    # rerun: everything queued, nothing new
    assert cq.submit(runner, remote, mover, rows, state=tmp_path, log=lambda m: None) == "nothing to submit"


def _queued(tmp_path, rows):
    cq.submit(FakeRunner(), FakeRemote(), FakeMover(), rows, state=tmp_path, log=lambda m: None)


def test_fetch_partial_array_pulls_finished_only(tmp_path, rows, monkeypatch):
    monkeypatch.setattr(cq.hc, "CACHE", tmp_path / "cache")
    _queued(tmp_path, rows)
    outs = {"rodA__st1.npz": b"a", "rodA__st2.npz": b"b"}
    remote = FakeRemote(sacct={0: ("COMPLETED", ""), 1: ("RUNNING", "")}, outputs=outs,
                        ok=("rodA__st1.npz.ok", "rodA__st2.npz.ok"))
    msg = cq.fetch(FakeRunner(), remote, state=tmp_path, storage_dir="/storage/c029", log=lambda m: None)
    assert msg.startswith("fetched 2, failed 0")
    assert (tmp_path / "cache" / "rodA__st1.npz").read_bytes() == b"a"
    assert (tmp_path / "cache" / "rodA__st1.npz.ok").exists()
    assert not (tmp_path / "cache" / "rodA_moved__st1.npz").exists()
    q = {x["job"]: x["state"] for x in rq.read_csv(tmp_path / "queue.csv")}
    assert q == {"rodA__st1.npz": "fetched", "rodA__st2.npz": "fetched", "rodA_moved__st1.npz": "running"}


def test_fetch_md5_mismatch_not_cached(tmp_path, rows, monkeypatch):
    monkeypatch.setattr(cq.hc, "CACHE", tmp_path / "cache")
    _queued(tmp_path, rows)
    remote = FakeRemote(sacct={0: ("COMPLETED", ""), 1: ("COMPLETED", "")},
                        outputs={r["job"]: b"z" for r in rows}, storage_bad=True,
                        ok=tuple(r["job"] + ".ok" for r in rows))
    cq.fetch(FakeRunner(), remote, state=tmp_path, storage_dir="/storage/c029", log=lambda m: None)
    assert not (tmp_path / "cache").exists() or not list((tmp_path / "cache").glob("*.npz"))
    assert all(x["state"] != "fetched" for x in rq.read_csv(tmp_path / "queue.csv"))


def test_fetch_missing_output_marked_failed(tmp_path, rows, monkeypatch):
    monkeypatch.setattr(cq.hc, "CACHE", tmp_path / "cache")
    _queued(tmp_path, rows)
    remote = FakeRemote(sacct={0: ("FAILED", ""), 1: ("TIMEOUT", "")}, outputs={})
    msg = cq.fetch(FakeRunner(), remote, state=tmp_path, storage_dir="/storage/c029", log=lambda m: None)
    assert msg.startswith("fetched 0, failed 3")


def test_fetch_connection_down(tmp_path, rows):
    _queued(tmp_path, rows)
    before = (tmp_path / "queue.csv").read_text()
    assert cq.fetch(FakeRunner(), FakeRemote(down=True), state=tmp_path, storage_dir="/s",
                    log=lambda m: None) == "connection down"
    assert (tmp_path / "queue.csv").read_text() == before


def test_worst_case_counts_tasks(rows):
    assert cq.worst_case_usd(rows) == round(0.012 * 2, 3)
