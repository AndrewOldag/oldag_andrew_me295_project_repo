"""Tests for scripts/hooks/pre_push_check.py on temporary git repos.

Strings that would trip the checker are built from pieces so this file
itself passes the checker.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "hooks" / "pre_push_check.py"
INSTALL = ROOT / "scripts" / "hooks" / "install.sh"
SECRET_WORD = "zebra" + "quartz"


def git(repo, *args, inp=None):
    return subprocess.run(["git", *args], cwd=repo, input=inp, capture_output=True,
                          text=True, check=True).stdout


def commit(repo, files, msg="change"):
    for name, content in files.items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
        git(repo, "add", "-f", name)
    git(repo, "commit", "-q", "-m", msg)
    return git(repo, "rev-parse", "HEAD").strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    git(r, "config", "user.name", "Test")
    git(r, "config", "user.email", "test")
    git(r, "config", "core.autocrlf", "false")
    commit(r, {"README.md": "base\n"}, "base")
    return r


@pytest.fixture
def blocklist(tmp_path):
    p = tmp_path / "blocklist.txt"
    p.write_text("# comment\n\n" + SECRET_WORD + r"\d+" + "\n", encoding="utf-8")
    return p


def run_check(repo, blocklist, revs=("main~1..main",)):
    return subprocess.run([sys.executable, str(CHECK), "--blocklist", str(blocklist), "--commits", *revs],
                          cwd=repo, capture_output=True, text=True)


CLEAN = (
    "# Notes\n"
    "- Run `python scripts/demo_slice.py --out results/x`\n"
    "- Server at http://localhost:8295 and 127.0.0.1\n"
    "- Repo on github.com; mail noreply@anthropic.com\n"
    "- Pinned lib=1.2.16.1 and opencv==5.0.0.93; ratio 0.797\n"
    "- Copy config/runner.example.yaml to private/runner.yaml\n"
    "- Use `x @ y` and @dataclass\n"
)


def test_clean_commit_passes(repo, blocklist):
    commit(repo, {"docs/notes.md": CLEAN, "src/a.py": "import numpy as np\nx = np.zeros(3)\n"},
           "Add notes\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
    r = run_check(repo, blocklist)
    assert r.returncode == 0, r.stderr
    assert "0 hits" in r.stderr


TEXT_CASES = {
    "blocklist": "see " + SECRET_WORD + "42 here\n",
    "host name": "ssh to gpu01.lab-cluster" + ".caltech" + ".edu now\n",
    "host name ": "node " + "box7" + ".internal\n",
    "IP address": "server " + "10.12" + ".0.7 port 22\n",
    "user-at-host": "login as " + "jdoe" + "@" + "labbox\n",
    "absolute path": "data in " + "/m" + "nt/scratch/x\n",
    "absolute path ": "cd " + "/ho" + "me/jdoe\n",
    "absolute path  ": "python at " + "C:" + "\\Python\\python.exe\n",
    "absolute path   ": "open " + "/Us" + "ers/jdoe/x\n",
    "key or token": "-----BEGIN " + "OPENSSH PRIVATE" + " KEY-----\n",
    "key or token ": "ssh-" + "ed25519 AAAA" + "C3NzaC1lZDI1NTE5AAAAIabcdefgh jdoe\n",
    "key or token  ": "aws " + "AKIA" + "ABCDEFGHIJKLMNOP\n",
    "key or token   ": "gh" + "p_" + "a" * 36 + "\n",
    "key or token    ": "sk-" + "ant-" + "api03-" + "b" * 30 + "\n",
    "key or token     ": 'api_' + 'key = "' + "c" * 20 + '"\n',
}


@pytest.mark.parametrize("rule", list(TEXT_CASES))
def test_text_rule_fails(repo, blocklist, rule):
    commit(repo, {"docs/notes.md": CLEAN + TEXT_CASES[rule]})
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert f"{rule.strip()}: " in r.stderr
    assert "docs/notes.md:8" in r.stderr


def test_blocklist_match_not_printed(repo, blocklist):
    commit(repo, {"a.txt": SECRET_WORD + "7\n"})
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert SECRET_WORD not in r.stdout + r.stderr
    assert "a.txt:1" in r.stderr


def test_commit_message_fails(repo, blocklist):
    commit(repo, {"a.txt": "ok\n"}, "Ran on " + "box7" + ".internal")
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert "(commit message):1" in r.stderr


@pytest.mark.parametrize("ext", [".tif", ".tiff", ".npy", ".sldy", ".h5"])
def test_data_file_fails(repo, blocklist, ext):
    commit(repo, {"results/x" + ext: b"\x00\x01"})
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert "image or data file" in r.stderr


def test_large_file_fails(repo, blocklist):
    commit(repo, {"results/big.txt": "a" * (5 * 1024 * 1024 + 1)})
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert "file over 5 MB" in r.stderr


@pytest.mark.parametrize("d", ["private", "data", "staging"])
def test_blocked_dir_fails(repo, blocklist, d):
    commit(repo, {d + "/notes.txt": "ok\n"})
    r = run_check(repo, blocklist)
    assert r.returncode == 1
    assert "file under private/, data/ or staging/" in r.stderr


def test_missing_blocklist_fails(repo, tmp_path):
    commit(repo, {"a.txt": "ok\n"})
    r = run_check(repo, tmp_path / "none.txt")
    assert r.returncode == 1
    assert "blocklist not found" in r.stderr


def find_sh():
    for name in ("sh", "bash"):
        p = shutil.which(name)
        if p and "system32" not in p.lower():
            return p
    exec_path = subprocess.run(["git", "--exec-path"], capture_output=True, text=True).stdout.strip()
    for up in Path(exec_path).parents:
        cand = up / "bin" / "sh.exe"
        if cand.is_file():
            return str(cand)
    return None


@pytest.mark.skipif(find_sh() is None, reason="no sh to run install.sh")
def test_installed_hook_blocks_push(repo, tmp_path, blocklist):
    remote = tmp_path / "remote.git"
    git(tmp_path, "init", "-q", "--bare", str(remote))
    git(repo, "remote", "add", "origin", str(remote))
    # The hook runs the checker from the pushing checkout, as in the real repo.
    (repo / "scripts" / "hooks").mkdir(parents=True)
    shutil.copy(CHECK, repo / "scripts" / "hooks" / "pre_push_check.py")
    (repo / "private").mkdir()
    shutil.copy(blocklist, repo / "private" / "blocklist.txt")
    env = dict(os.environ, PYTHON=sys.executable)
    subprocess.run([find_sh(), str(INSTALL)], cwd=repo, env=env, check=True, capture_output=True)

    git(repo, "add", "scripts/hooks/pre_push_check.py")
    git(repo, "commit", "-q", "-m", "add checker")
    r = subprocess.run(["git", "push", "-q", "origin", "main"], cwd=repo, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    commit(repo, {"a.txt": "server " + "10.12" + ".0.7\n"})
    r = subprocess.run(["git", "push", "origin", "main"], cwd=repo, env=env, capture_output=True, text=True)
    assert r.returncode != 0
    assert "IP address" in r.stderr

    # A clean commit on top of an already pushed one: only new commits are scanned.
    git(repo, "reset", "-q", "--hard", "HEAD~1")
    commit(repo, {"b.txt": "ok\n"})
    r = subprocess.run(["git", "push", "origin", "main"], cwd=repo, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "1 commits scanned, 0 hits" in r.stderr

    # Re-running the installer replaces its own hook; a foreign hook is kept.
    r = subprocess.run([find_sh(), str(INSTALL)], cwd=repo, env=env, capture_output=True)
    assert r.returncode == 0
    hook = Path(git(repo, "rev-parse", "--git-path", "hooks").strip())
    if not hook.is_absolute():
        hook = repo / hook
    (hook / "pre-push").write_text("#!/bin/sh\nexit 0\n")
    r = subprocess.run([find_sh(), str(INSTALL)], cwd=repo, env=env, capture_output=True)
    assert r.returncode == 1
