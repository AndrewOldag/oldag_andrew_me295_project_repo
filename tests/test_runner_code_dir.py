"""Code directory per branch and commit on the tracker machine (spec 2026-10-12b, item 1; freeze v3, no
overwrite or rename on the lab server). No remote calls."""
import io
import tarfile

import pytest
import yaml

from measure import runner
from measure.runner import RemoteRunner, branch_code_dir
from scripts.synth import sweep


def make(tmp_path, branch, have=(), jobs=0):
    """have: remote paths that exist (for `test -e` probes). jobs: running jobs of the account."""
    cfg = tmp_path / "runner.yaml"
    cfg.write_text(yaml.safe_dump({"host": "h", "work_dir": "/base/work", "code_dir": "/base/code/",
                                   "python": "py"}))
    r = RemoteRunner(cfg, cache=tmp_path / "cache", branch=branch)
    r.calls = []
    r._code_committed = lambda: True

    def ssh(cmd, stdin=None):
        r.calls.append((cmd, stdin))
        if cmd.startswith("test -e"):
            return b"yes\n" if any(h in cmd for h in have) else b"no\n"
        if cmd.startswith("ps -u"):
            return f"{jobs}\n".encode()
        return b'{"running": false}\n'
    r._ssh = ssh
    return r


def head():
    return runner.RemoteRunner._git("rev-parse", "--short=12", "HEAD").decode().strip()


def test_two_branches_two_directories(tmp_path):
    a, b = make(tmp_path, "wip/scored-v1"), make(tmp_path, "heldout/faults")
    assert a.code_branch == "/base/code/wip_scored-v1"
    assert b.code_branch == "/base/code/heldout_faults"
    assert a.code_branch != b.code_branch
    assert branch_code_dir("/base/code", "main") == "/base/code/main"


def test_bad_branch_names_refused():
    for bad in ("", ".", ".."):
        with pytest.raises(ValueError):
            branch_code_dir("/base/code", bad)


def test_default_branch_is_checked_out_branch(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "current_branch", lambda root=runner.ROOT: "wip/x")
    cfg = tmp_path / "runner.yaml"
    cfg.write_text(yaml.safe_dump({"host": "h", "work_dir": "/w", "code_dir": "/c", "python": "py"}))
    assert RemoteRunner(cfg, cache=tmp_path / "cache").code_branch == "/c/wip_x"


def test_sync_writes_a_new_commit_folder_once(tmp_path):
    r = make(tmp_path, "wip/scored-v1")
    assert r.sync_code() == f"/base/code/wip_scored-v1/{head()}"
    (probe, _), (cmd, data) = r.calls
    assert probe.startswith("test -e")
    d = f"/base/code/wip_scored-v1/{head()}"
    assert cmd == f"mkdir -p /base/code/wip_scored-v1 && mkdir {d} && cd {d} && tar xkf - && set -C && : > .ok"
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        names = tar.getnames()
        assert any(n.startswith("measure/") for n in names) and any(n.startswith("scripts/remote/") for n in names)
        for ti in tar.getmembers():
            assert not ti.name.startswith("/") and ".." not in ti.name.split("/")
            assert not (ti.issym() or ti.islnk())


def test_sync_reuses_a_finished_folder(tmp_path):
    r = make(tmp_path, "wip/scored-v1", have=(f"{head()}/.ok",))
    r.sync_code()
    assert len(r.calls) == 1                                  # the probe only; nothing written


def test_sync_refuses_uncommitted_code(tmp_path):
    r = make(tmp_path, "wip/scored-v1")
    r._code_committed = lambda: False
    with pytest.raises(RuntimeError, match="commit first"):
        r.sync_code()


def test_scripts_run_from_commit_directory(tmp_path):
    r = make(tmp_path, "wip/scored-v1")
    assert (r._py("scripts/synth/sweep.py", ["status"]).split()[1]
            == f"/base/code/wip_scored-v1/{head()}/scripts/synth/sweep.py")


def test_sweep_start_never_overwrites(tmp_path):
    r = make(tmp_path, "wip/a")
    r.start_detached = lambda cmd: r.calls.append((cmd, None))
    log = r.sweep_start({"rods": []}, "x")
    plan_cmd = next(c for c, _ in r.calls if "plan_x_" in c and "cat >" in c)
    start_cmd = r.calls[-1][0]
    assert "set -C" in plan_cmd and "set -C" in start_cmd and f"> {log}" in start_cmd
    assert log.startswith("sweep_x_") and log.endswith(".log")


def test_at_most_two_jobs(tmp_path):
    r = make(tmp_path, "wip/a", jobs=2)
    r.start_detached = lambda cmd: r.calls.append((cmd, None))
    with pytest.raises(RuntimeError, match="at most 2"):
        r.sweep_start({"rods": []}, "x")
    assert make(tmp_path, "wip/a", jobs=1).account_jobs() == 1


def test_lock_is_one_per_machine(tmp_path):
    a, b = make(tmp_path, "wip/a"), make(tmp_path, "wip/b")
    assert a.work == b.work
    a.sweep_status(); b.sweep_status()
    wa, wb = (next(c for c, _ in x.calls if "--work " in c).split("--work ")[1] for x in (a, b))
    assert wa == wb == "/base/work"
    assert sweep.lock_path(wa) == sweep.lock_path(wb)
    # the 10 GB limit still covers the shared work and code base, not one branch
    assert a.size_root == b.size_root == "/base"


def test_no_rename_or_overwrite_on_the_server():
    """The code that runs on the tracker machine renames nothing and writes outputs once."""
    root = runner.ROOT
    qb = (root / "scripts" / "remote" / "qb_track.py").read_text()
    assert "os.replace" not in qb and "os.rename" not in qb and '"xb"' in qb and "O_EXCL" in qb
    sw = (root / "scripts" / "synth" / "sweep.py").read_text()
    assert "os.replace" not in sw and "os.rename" not in sw
    rn = (root / "measure" / "runner.py").read_text()
    assert "tar xf -" not in rn and "tar xkf -" in rn
