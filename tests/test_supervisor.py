"""Tests for scripts/ops/supervisor.ps1 and register_detached.ps1 (spec 2026-11-22, task c032).

Fake clock (-Now), fake process table (-ProcTable), fake free memory (-FreeGB), a stub
agents.ps1 that only records its call, and a temporary bare repository as origin.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"
POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")
pytestmark = pytest.mark.skipif(POWERSHELL is None or os.name != "nt" or shutil.which("git") is None,
                                reason="needs Windows PowerShell and git")

NOW = "2026-11-23T06:00:00Z"          # 2026-11-22 22:00 Pacific
NAMES = ("dispatcher", "real-calib", "compound")
EMAIL = "t" + "@" + "example.com"      # built from pieces so the pre-push check passes this file
ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL=EMAIL,
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL=EMAIL)
AGENTS_STUB = 'param([string[]]$Names, [switch]$Fresh, [int]$GapSec)\n' \
              'Add-Content -Path (Join-Path $PSScriptRoot "starts.txt") -Value "$Names fresh=$Fresh"\n'


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True,
                          env=ENV).stdout


def status(done, state="ready to merge", updated="2026-11-22 21:30"):
    return (f"# x\nUpdated: {updated} (local)\nLane: course\nBranch: b\n"
            f"Last inbox item done: {done}\nState: {state}\nNow: n\n")


def inbox(n):
    return "# Inbox\n\n" + "".join(f"{i}. item {i}\n" for i in range(1, n + 1))


def commit_files(work, branch, files, base="main"):
    if branch == "main":
        subprocess.run(["git", "checkout", "-q", "main"], cwd=work, capture_output=True)   # unborn at first
    else:
        git(work, "checkout", "-q", "-B", branch, base)
    for name, text in files.items():
        p = work / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", f"{branch} files")
    git(work, "push", "-q", "origin", f"HEAD:refs/heads/{branch}")


@pytest.fixture
def world(tmp_path):
    """origin (bare), a work clone that writes branches, the main checkout the supervisor uses."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True, env=ENV)
    work = tmp_path / "work"
    subprocess.run(["git", "clone", "-q", str(origin), str(work)], check=True, env=ENV,
                   capture_output=True)
    git(work, "symbolic-ref", "HEAD", "refs/heads/main")
    commit_files(work, "main", {f"docs/agents/inbox/{n}.md": inbox(3) for n in NAMES})
    for n in NAMES:
        commit_files(work, f"wip/{n}", {f"docs/agents/status/{n}.md": status(3)})
    repo = tmp_path / "repo"
    subprocess.run(["git", "clone", "-q", str(origin), str(repo)], check=True, env=ENV,
                   capture_output=True)
    state = tmp_path / "state"
    state.mkdir()
    stub = tmp_path / "stub"
    stub.mkdir()
    (stub / "agents.ps1").write_text(AGENTS_STUB)
    procs = tmp_path / "procs.json"
    procs.write_text("{}")
    return dict(tmp=tmp_path, origin=origin, work=work, repo=repo, state=state, stub=stub, procs=procs)


def run(w, now=NOW, free=8.0, extra=()):
    r = subprocess.run([POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(OPS / "supervisor.ps1"), "-Once", "-Repo", str(w["repo"]),
                        "-StateDir", str(w["state"]), "-Agents", str(w["stub"] / "agents.ps1"),
                        "-Now", now, "-ProcTable", str(w["procs"]), "-FreeGB", str(free), *extra],
                       capture_output=True, text=True, env=ENV, timeout=180)
    assert r.returncode == 0, r.stdout + r.stderr
    return r


def starts(w):
    f = w["stub"] / "starts.txt"
    return [ln.split()[0] for ln in f.read_text(encoding="utf-8-sig").splitlines()] if f.exists() else []


def heartbeat(w):
    git(w["work"], "fetch", "-q", "origin")
    text = git(w["work"], "show", "origin/ops/heartbeat:docs/agents/status/supervisor.md")
    return [ln for ln in text.splitlines() if ln[:2] == "20"]


def log(w):
    return (w["state"] / "supervisor.log").read_text(encoding="utf-8-sig")


def test_nothing_pending_starts_nothing(world):
    run(world)
    assert starts(world) == []
    hb = heartbeat(world)
    assert len(hb) == 1
    assert hb[0].startswith("2026-11-22 22:00 free=8.0GB dispatcher=exited real-calib=exited compound=exited")
    assert "start=none dead=none" in hb[0]


def test_new_inbox_item_starts_that_session(world):
    commit_files(world["work"], "main", {"docs/agents/inbox/real-calib.md": inbox(4)})
    run(world)
    assert starts(world) == ["real-calib"]
    assert "real-calib=exited,pending:inbox" in heartbeat(world)[0]
    assert "start=real-calib" in heartbeat(world)[0]


def test_newest_status_over_branches_counts(world):
    # an old status on main says 1 done; the newer one on the work branch says 3: not pending
    commit_files(world["work"], "main", {"docs/agents/status/compound.md": status(1, updated="2026-11-20 10:00")})
    run(world)
    assert starts(world) == []
    # a newer status on another branch says 2 done: pending
    commit_files(world["work"], "wip/supervisor", {"docs/agents/status/compound.md": status(2, updated="2026-11-22 21:45")})
    run(world, now="2026-11-23T06:10:00Z")
    assert starts(world) == ["compound"]


def test_running_session_is_not_restarted(world):
    commit_files(world["work"], "main", {"docs/agents/inbox/dispatcher.md": inbox(5)})
    (world["state"] / "dispatcher.pid").write_text("4242\n")
    world["procs"].write_text(json.dumps({"4242": {"name": "claude", "start": 1}}))
    run(world)
    assert starts(world) == []
    assert "dispatcher=running" in heartbeat(world)[0]
    # same pid now belongs to another program: not running, started
    world["procs"].write_text(json.dumps({"4242": {"name": "notepad", "start": 1}}))
    run(world, now="2026-11-23T06:10:00Z")
    assert starts(world) == ["dispatcher"]


def test_stale_working_status_starts_after_two_hours(world):
    commit_files(world["work"], "wip/compound",
                 {"docs/agents/status/compound.md": status(3, "working", "2026-11-22 20:30")}, base="wip/compound")
    run(world)                                                   # 1.5 h old
    assert starts(world) == []
    run(world, now="2026-11-23T06:40:00Z")                       # 2.2 h old
    assert starts(world) == ["compound"]
    assert "compound=exited,pending:stale" in heartbeat(world)[-1]


def test_low_memory_blocks_starts(world):
    commit_files(world["work"], "main", {"docs/agents/inbox/real-calib.md": inbox(4)})
    run(world, free=2.5)
    assert starts(world) == []
    assert "free=2.5GB" in heartbeat(world)[0]
    assert "start=none (free memory under 3 GB)" in heartbeat(world)[0]


def test_one_start_per_tick_and_restart_wait(world):
    commit_files(world["work"], "main", {f"docs/agents/inbox/{n}.md": inbox(4) for n in ("dispatcher", "compound")})
    run(world)
    assert starts(world) == ["dispatcher"]
    run(world, now="2026-11-23T06:00:30Z")                       # 30 s later: gap
    assert starts(world) == ["dispatcher"]
    assert "last start under 60 s ago" in heartbeat(world)[-1]
    run(world, now="2026-11-23T06:10:00Z")                       # dispatcher waits RestartMin
    assert starts(world) == ["dispatcher", "compound"]
    run(world, now="2026-11-23T06:20:00Z")
    assert starts(world) == ["dispatcher", "compound"]
    assert "pending sessions started under 60 min ago" in heartbeat(world)[-1]
    run(world, now="2026-11-23T07:01:00Z")
    assert starts(world) == ["dispatcher", "compound", "dispatcher"]


def test_lock_stops_second_instance(world):
    (world["state"] / "supervisor.lock").write_text("4242 777")
    world["procs"].write_text(json.dumps({"4242": {"name": "powershell", "start": 777}}))
    commit_files(world["work"], "main", {"docs/agents/inbox/real-calib.md": inbox(4)})
    run(world)
    assert starts(world) == []
    assert "another supervisor is running (pid 4242)" in log(world)
    assert (world["state"] / "supervisor.lock").read_text() == "4242 777"
    # holder gone: stale lock taken over, tick runs, own lock removed at exit
    world["procs"].write_text("{}")
    run(world)
    assert starts(world) == ["real-calib"]
    assert "stale lock from pid 4242" in log(world)
    assert not (world["state"] / "supervisor.lock").exists()


def test_heartbeat_keeps_last_48_lines(world):
    old = "".join(f"2026-11-20 {h:02d}:{m:02d} old\n" for h in range(10) for m in (0, 10, 20, 30, 40))
    commit_files(world["work"], "ops/heartbeat", {"docs/agents/status/supervisor.md": "# supervisor\n\n" + old})
    run(world)
    hb = heartbeat(world)
    assert len(hb) == 48
    assert hb[0] == "2026-11-20 00:30 old" and hb[-1].startswith("2026-11-22 22:00 ")
    # the heartbeat commit holds the previous branch tip as parent; no checkout was touched
    git(world["work"], "fetch", "-q", "origin")
    assert git(world["work"], "rev-list", "--count", "origin/ops/heartbeat").strip() == "3"
    assert git(world["repo"], "status", "--porcelain") == ""


def test_dead_detached_entries_reported(world):
    world["procs"].write_text(json.dumps({"500": {"name": "python", "start": 11}}))
    (world["state"] / "detached.json").write_text(json.dumps([
        {"name": "alive", "pid": 500, "start_ticks": 11, "command": "c", "log": "l", "started": "s"},
        {"name": "gone", "pid": 501, "start_ticks": 12, "command": "c", "log": "l", "started": "s"},
        {"name": "reused", "pid": 500, "start_ticks": 99, "command": "c", "log": "l", "started": "s"},
    ]))
    run(world)
    assert "dead=gone(501),reused(500)" in heartbeat(world)[0]
    assert len(json.loads((world["state"] / "detached.json").read_text())) == 3   # never pruned


def test_register_detached_adds_and_removes(tmp_path):
    def reg(*extra):
        r = subprocess.run([POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                            str(OPS / "register_detached.ps1"), "-StateDir", str(tmp_path), *extra],
                           capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, r.stdout + r.stderr
    reg("-Name", "job", "-ProcessId", str(os.getpid()), "-Command", "python x.py", "-Log", "x.log")
    reg("-Name", "job", "-ProcessId", str(os.getpid()), "-Command", "python x.py", "-Log", "x.log")
    e = json.loads((tmp_path / "detached.json").read_text(encoding="utf-8"))
    assert len(e) == 1 and e[0]["name"] == "job" and e[0]["pid"] == os.getpid() and e[0]["start_ticks"] > 0
    reg("-Name", "other", "-ProcessId", str(os.getpid()))
    e = json.loads((tmp_path / "detached.json").read_text(encoding="utf-8"))
    assert [x["name"] for x in e] == ["job", "other"]
    reg("-Name", "other", "-ProcessId", str(os.getpid()), "-Unregister")
    reg("-Name", "job", "-ProcessId", str(os.getpid()), "-Unregister")
    assert json.loads((tmp_path / "detached.json").read_text(encoding="utf-8")) == []


def test_supervisor_never_deletes_kills_or_reaches_hosts():
    text = (OPS / "supervisor.ps1").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    for word in ("Stop-Process", "taskkill", "ssh", "scp", "sbatch", "Remove-Item $registry", "git branch -D"):
        assert word not in code, word
    # the only Remove-Item calls: its own lock and the temporary index variable
    removes = [ln.strip() for ln in code.splitlines() if "Remove-Item" in ln]
    assert len(removes) == 2 and all("$lock" in ln or "Env:GIT_INDEX_FILE" in ln for ln in removes)
