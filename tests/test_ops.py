"""Tests for scripts/ops: heartbeat gap rule, backup refusals and no server delete."""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"
BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="bash not found")


def sh(*args, env_extra=None, inp=None):
    import os
    env = dict(os.environ, **(env_extra or {}))
    return subprocess.run([BASH, *map(str, args)], input=inp, capture_output=True, text=True,
                          env=env)


def beat(log, now):
    r = sh(OPS / "heartbeat.sh", log.as_posix(), env_extra={"HEARTBEAT_NOW": str(now)})
    assert r.returncode == 0, r.stderr


def test_heartbeat_lines_and_first_gap(tmp_path):
    log = tmp_path / "health" / "uptime.log"
    t0 = 1_760_000_000
    beat(log, t0)
    beat(log, t0 + 300)                      # on time
    assert not (log.parent / "FIRST_GAP").exists()
    beat(log, t0 + 300 + 1800)               # 30 min gap
    beat(log, t0 + 300 + 1800 + 3600)        # second gap, 60 min
    lines = log.read_text().splitlines()
    assert [ln.startswith("GAP") for ln in lines] == [False, False, True, False, True, False]
    assert all(" up=" in ln and " boot=" in ln for ln in lines if not ln.startswith("GAP"))
    assert "(30 min)" in lines[2]
    first = (log.parent / "FIRST_GAP").read_text()
    assert "(30 min)" in first                # first gap kept, not replaced


def test_backup_never_deletes_on_server():
    """No command sent to the lab server deletes, moves or renames (CLAUDE.md)."""
    text = (OPS / "backup_vm.sh").read_text(encoding="utf-8")
    remote_lines = [ln for ln in text.splitlines()
                    if "remote " in ln and not ln.lstrip().startswith(("#", "remote ()"))]
    assert remote_lines
    for ln in remote_lines:
        for word in ("rm ", "rmdir", "unlink", "mv ", "rsync", "find "):
            assert word not in ln, ln.strip()


def test_backup_refuses_without_conf(tmp_path):
    r = sh(OPS / "backup_vm.sh", "--conf", tmp_path / "none.conf", "run")
    assert r.returncode != 0 and "conf file not found" in r.stdout


def test_backup_refuses_incomplete_conf(tmp_path):
    conf = tmp_path / "b.conf"
    conf.write_text("HOST=example\n")
    r = sh(OPS / "backup_vm.sh", "--conf", conf.as_posix(), "run")
    assert r.returncode != 0 and "not set in conf" in r.stdout


def test_ops_scripts_name_no_location():
    """Hosts and paths come from private/backup.conf only."""
    for f in OPS.iterdir():
        text = f.read_text(encoding="utf-8")
        for bad in ("caltech", "/mnt" + "/", "Users" + "/", "vm-backup" + "/", "D:" + "/", "/d" + "/"):
            assert bad not in text, f"{f.name}: {bad}"
