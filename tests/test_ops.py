"""Tests for scripts/ops: heartbeat gap rule, backup refusals, no server delete, coordinator tick."""

import json
import os
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


# Coordinator tick (scripts/ops/coordinator_tick.ps1): git and claude are stubs

POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")
needs_ps = pytest.mark.skipif(POWERSHELL is None or os.name != "nt", reason="needs Windows PowerShell")

GIT_STUB = r"""@echo off
echo %* >> "%STUB_LOG%"
echo %* | findstr /C:"ls-remote" >nul && (type "%STUB_REFS%" & exit /b 0)
echo %* | findstr /C:"rev-parse" >nul && (echo 0123456789abcdef & exit /b 0)
exit /b 0
"""

CLAUDE_STUB = r"""@echo off
echo called >> "%STUB_CLAUDE%"
echo {"result":"done\nPINGED: none; TO PING: none","usage":{"input_tokens":5,"output_tokens":7},"num_turns":2}
"""

REFS_A = "aaa1\trefs/heads/main\nbbb2\trefs/heads/wip/x\n"


def tick(tmp_path, refs):
    """One tick with stubbed git and claude. Returns (result, claude calls so far)."""
    stubs = tmp_path / "stubs"
    stubs.mkdir(exist_ok=True)
    (stubs / "git.cmd").write_text(GIT_STUB)
    (stubs / "claude.cmd").write_text(CLAUDE_STUB)
    (tmp_path / "refs.txt").write_text(refs)
    calls = tmp_path / "claude_calls.txt"
    env = dict(os.environ, STUB_LOG=str(tmp_path / "git.log"), STUB_REFS=str(tmp_path / "refs.txt"),
               STUB_CLAUDE=str(calls))
    r = subprocess.run([POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(OPS / "coordinator_tick.ps1"), "-Repo", str(tmp_path),
                        "-Conf", str(tmp_path / "none.conf"), "-TickDir", str(tmp_path / "tick"),
                        "-Git", str(stubs / "git.cmd"), "-Claude", str(stubs / "claude.cmd")],
                       capture_output=True, text=True, env=env, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    return r, (len(calls.read_text().splitlines()) if calls.exists() else 0)


def tick_log(tmp_path):
    return (tmp_path / "tick" / "tick.log").read_text(encoding="utf-8-sig")


@needs_ps
def test_tick_skips_claude_when_refs_unchanged(tmp_path):
    assert tick(tmp_path, REFS_A)[1] == 1                     # no state yet: full pass
    assert tick(tmp_path, REFS_A)[1] == 1                     # same refs, < 60 min: skip
    log = tick_log(tmp_path)
    assert "skip: refs unchanged" in log
    assert "exit: 0" in log and "commit: main=0123456789abcdef" in log
    assert "tokens in=5 out=7" in log and "pings: PINGED: none; TO PING: none" in log
    assert not (tmp_path / "tick" / "tick.lock").exists()


@needs_ps
def test_tick_hash_ignores_order_and_sees_changes(tmp_path):
    tick(tmp_path, REFS_A)
    reordered = "".join(reversed(REFS_A.splitlines(keepends=True)))
    assert tick(tmp_path, reordered)[1] == 1                  # same refs, other order: skip
    assert tick(tmp_path, REFS_A + "ccc3\trefs/heads/wip/y\n")[1] == 2   # new ref: full pass


@needs_ps
def test_tick_full_pass_after_an_hour_and_live_lock(tmp_path):
    tick(tmp_path, REFS_A)
    sf = tmp_path / "tick" / "state.json"
    state = json.loads(sf.read_text(encoding="utf-8-sig"))
    state["last_full"] -= 61 * 60
    sf.write_text(json.dumps(state))
    assert tick(tmp_path, REFS_A)[1] == 2                     # unchanged but 61 min old
    # a lock held by a live process (this one): no pass, lock left alone
    ticks = subprocess.run([POWERSHELL, "-NoProfile", "-Command",
                            f"(Get-Process -Id {os.getpid()}).StartTime.Ticks"],
                           capture_output=True, text=True).stdout.strip()
    lock = tmp_path / "tick" / "tick.lock"
    lock.write_text(f"{os.getpid()} {ticks}")
    assert tick(tmp_path, REFS_A + "ddd4\trefs/heads/z\n")[1] == 2
    assert "previous tick still running" in tick_log(tmp_path)
    assert lock.exists()
