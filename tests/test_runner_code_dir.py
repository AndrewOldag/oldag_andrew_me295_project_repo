"""Per-branch code directory on the tracker machine (spec 2026-10-12b, item 1). No remote calls."""
import io
import tarfile

import pytest
import yaml

from measure import runner
from measure.runner import RemoteRunner, branch_code_dir
from scripts.synth import sweep


def make(tmp_path, branch):
    cfg = tmp_path / "runner.yaml"
    cfg.write_text(yaml.safe_dump({"host": "h", "work_dir": "/base/work", "code_dir": "/base/code/",
                                   "python": "py"}))
    r = RemoteRunner(cfg, cache=tmp_path / "cache", branch=branch)
    r.calls = []

    def ssh(cmd, stdin=None):
        r.calls.append((cmd, stdin))
        return b'{"running": false}\n'
    r._ssh = ssh
    return r


def test_two_branches_two_directories(tmp_path):
    a, b = make(tmp_path, "wip/scored-v1"), make(tmp_path, "heldout/faults")
    assert a.code == "/base/code/wip_scored-v1"
    assert b.code == "/base/code/heldout_faults"
    assert a.code != b.code
    assert branch_code_dir("/base/code", "main") == "/base/code/main"


def test_bad_branch_names_refused():
    for bad in ("", ".", ".."):
        with pytest.raises(ValueError):
            branch_code_dir("/base/code", bad)


def test_default_branch_is_checked_out_branch(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "current_branch", lambda root=runner.ROOT: "wip/x")
    cfg = tmp_path / "runner.yaml"
    cfg.write_text(yaml.safe_dump({"host": "h", "work_dir": "/w", "code_dir": "/c", "python": "py"}))
    assert RemoteRunner(cfg, cache=tmp_path / "cache").code == "/c/wip_x"


def test_sync_writes_only_inside_its_directory(tmp_path):
    r = make(tmp_path, "wip/scored-v1")
    r.sync_code()
    (cmd, data), = r.calls
    assert cmd == "mkdir -p /base/code/wip_scored-v1 && cd /base/code/wip_scored-v1 && tar xf -"
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        names = tar.getnames()
        assert names
        for ti in tar.getmembers():
            assert not ti.name.startswith("/") and ".." not in ti.name.split("/")
            assert not (ti.issym() or ti.islnk())


def test_scripts_run_from_branch_directory(tmp_path):
    r = make(tmp_path, "wip/scored-v1")
    assert r._py("scripts/synth/sweep.py", ["status"]).split()[1] == "/base/code/wip_scored-v1/scripts/synth/sweep.py"


def test_lock_is_one_per_machine(tmp_path):
    a, b = make(tmp_path, "wip/a"), make(tmp_path, "wip/b")
    assert a.work == b.work
    a.sweep_status(); b.sweep_status()
    wa, wb = (c[0].split("--work ")[1] for c in (a.calls[0], b.calls[0]))
    assert wa == wb == "/base/work"
    assert sweep.lock_path(wa) == sweep.lock_path(wb)
    # the 10 GB limit still covers the shared work and code base, not one branch
    assert a.size_root == b.size_root == "/base"
