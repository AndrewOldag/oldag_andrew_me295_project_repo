"""Storage-only host rules (spec 2026-11-04): no compute is started on the storage host; cluster compute goes through
the relay as Slurm jobs, with the ledger checked before every submit. Fake link only; no real host."""
import re

import pytest

from measure import hosts
from measure.real_runner import RealRunner, RealWindow
from measure.remedies import TrackSettings
from measure.runner import RemoteRunner

ALIAS = "clusteralias"
CP = "/s/sock-cluster-22"
RELAY = (f"ssh -O check -o ControlPath={CP} {ALIAS} >/dev/null 2>&1 && "
         f"ssh -o BatchMode=yes -o ControlMaster=no -o ControlPath={CP} {ALIAS} ")
STORAGE_ALLOWED = re.compile(r"^(test |ls |du |cat |mkdir -p |rsync |ssh -O check |ssh -G |if \[ -d |cd \S+ && find )")


class FakeLink:
    """Answers storage and relayed cluster commands from a small scripted state."""

    def __init__(self):
        self.storage_cmds, self.cluster_cmds, self.submitted = [], [], []
        self.cluster_files = set()
        self.staged = False

    def run(self, cmd, stdin=None, check=True):
        if cmd.startswith(RELAY):
            inner = cmd[len(RELAY):].strip("'").replace("'\\''", "'")
            self.cluster_cmds.append(inner)
            return self.on_cluster(inner, stdin)
        self.storage_cmds.append(cmd)
        if cmd.startswith("ssh -G "):
            return f"controlpath {CP}\n".encode()
        if "rsync " in cmd and f"{ALIAS}:" in cmd.split()[-1]:
            self.staged = True
        if cmd.startswith("ssh -O check"):
            return b"Master running\n"
        if cmd.startswith("test -f") and "_netmid.npz" in cmd:
            return b"yes\n"                                    # midline already on storage
        if cmd.startswith("test -s"):
            raise RuntimeError("no such track on storage")
        if cmd.startswith("ls "):
            return b"961\n"
        if cmd.startswith("du -sm"):
            return b"5300\t.\n"
        if cmd.startswith("if [ -d"):
            return b"abc  -\n"
        if cmd.startswith("cat "):
            return b"TRACKBYTES"
        return b""

    def on_cluster(self, cmd, stdin):
        if cmd.startswith("test -e"):
            path = cmd.split()[2]
            return b"yes\n" if path in self.cluster_files else b"no\n"
        if cmd.startswith("ls "):
            return b"961\n" if self.staged else b"0\n"
        if cmd.startswith("du -sm"):
            return b"1000\t.\n"
        if cmd.startswith("sbatch"):
            self.submitted.append(cmd)
            return b"4242\n"
        if "squeue -j" in cmd:
            return b"0\n"
        if cmd.startswith("sacct"):
            return b"COMPLETED\n"
        if cmd.startswith("if [ -d"):
            return b"abc  -\n"
        return b""


def cluster_cfg(tmp_path):
    return {"compute": "cluster", "storage_host": "storage", "work_dir": "/store/fb", "midline_tag": "ft2",
            "windows": {"r1__w0-2": {"imgdir": "/store/movies/r1.imgdir", "midline": "/store/fb/midline/r1__w0-2_ft2_netmid.npz"}},
            "cluster": {"alias": ALIAS, "work_dir": "/cl/work", "stage_dir": "/cl/work/data", "code_dir": "/cl/code",
                        "tracker_code": "/cl/qb", "env": "/cl/env.sh", "cpu_partition": "cpu", "gpu_partition": "gpu",
                        "gpu_gres": "gpu:p100:1", "midline_weights": "/cl/w.pt", "cap_mb": 35840}}


def test_cluster_track_runs_as_slurm_job_and_nothing_on_storage(tmp_path):
    link, calls = FakeLink(), []
    ledger = lambda action, *a: (calls.append(action) or (0, "allowed"))  # noqa: E731
    r = RealRunner(cluster_cfg(tmp_path), cache=tmp_path, moved=False, link=link, ledger=ledger, sleep=lambda s: None)
    local = r.track(RealWindow("r1", 0, 2), TrackSettings(stride=1))
    assert local.read_bytes() == b"TRACKBYTES"
    assert calls == ["check", "record", "final"]                  # one tracking job, ledger around it
    assert len(link.submitted) == 1
    for c in link.storage_cmds:                                    # storage host: storage and relay commands only
        assert STORAGE_ALLOWED.match(c), c
        assert "python" not in c and "nice" not in c and "sbatch" not in c
    assert any(c.startswith(RELAY.split("&&")[0]) and " rsync " in c and f"{ALIAS}:/cl/work/data/r1.imgdir/" in c
               for c in link.storage_cmds)


def test_cluster_submit_refused_by_ledger(tmp_path):
    from measure.cluster_compute import BudgetStop
    link = FakeLink()
    r = RealRunner(cluster_cfg(tmp_path), cache=tmp_path, moved=False, link=link,
                   ledger=lambda action, *a: (1, "REFUSED"), sleep=lambda s: None)
    with pytest.raises(BudgetStop):
        r.track(RealWindow("r1", 0, 2), TrackSettings(stride=1))
    assert link.submitted == []


def test_only_cluster_compute_allowed(tmp_path):
    cfg = cluster_cfg(tmp_path)
    cfg["compute"] = "labserver"
    with pytest.raises(ValueError):
        RealRunner(cfg, cache=tmp_path, link=FakeLink(), ledger=lambda *a: (0, ""))


def test_storage_host_refused_for_legacy_real_runner(tmp_path, monkeypatch):
    monkeypatch.setattr(hosts, "storage_only_hosts", lambda paths=None: {"lab"})
    cfg = {"host": "lab", "work_dir": "/w", "code_dir": "/c", "tracker_code": "/t", "python": "py",
           "windows": {"r1__w0-2": {"imgdir": "/m", "midline": "/w/m.npz"}}}
    r = RealRunner(cfg, cache=tmp_path, moved=False)
    monkeypatch.setattr(r, "_ssh", lambda cmd, stdin=None: (_ for _ in ()).throw(RuntimeError("no file")))
    monkeypatch.setattr(r, "wait_vm_memory", lambda: 99.0)
    with pytest.raises(hosts.StorageOnlyHost):
        r.track(RealWindow("r1", 0, 2), TrackSettings(stride=1))


def test_storage_host_refused_for_sweeps_and_synthetic_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(hosts, "storage_only_hosts", lambda paths=None: {"lab"})
    p = tmp_path / "runner.yaml"
    p.write_text("host: lab\nwork_dir: /w\ncode_dir: /c\npython: py\n")
    rr = RemoteRunner(p, cache=tmp_path)
    with pytest.raises(hosts.StorageOnlyHost):
        rr._py("scripts/synth/sweep.py", ["status", "--work", "/w"])


def test_sweep_start_refused_before_code_sync(tmp_path, monkeypatch):
    """Argon A5-F6: no ssh command (mkdir, tar) reaches a storage-only host before the refusal."""
    monkeypatch.setattr(hosts, "storage_only_hosts", lambda paths=None: {"lab"})
    p = tmp_path / "runner.yaml"
    p.write_text("host: lab\nwork_dir: /w\ncode_dir: /c\npython: py\n")
    rr = RemoteRunner(p, cache=tmp_path)
    sent = []
    monkeypatch.setattr(rr, "_ssh", lambda cmd, stdin=None: sent.append(cmd) or b"")
    monkeypatch.setattr(rr, "sync_code", lambda: sent.append("sync_code"))
    with pytest.raises(hosts.StorageOnlyHost):
        rr.sweep_start([], "plan")
    assert sent == []


def test_storage_list_file(tmp_path):
    (tmp_path / hosts.LIST_NAME).write_text("# comment\nlab\n\n")
    assert hosts.storage_only_hosts([tmp_path]) == {"lab"}
    with pytest.raises(hosts.StorageOnlyHost):
        hosts.refuse_storage_host("lab", paths=[tmp_path])
    hosts.refuse_storage_host("workstation", paths=[tmp_path])
