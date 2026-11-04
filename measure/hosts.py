"""Storage-only hosts (spec 2026-11-04, Andrew): no Python, tracker, midline, checker or sweep run is started there.

The aliases are listed one per line in `private/storage_only_hosts.txt` of the main repo folder (git-ignored, so no
tracked file names a machine). Every runner that would start compute on an ssh host calls `refuse_storage_host`
first; a listed host raises `StorageOnlyHost` with a clear message.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIST_NAME = "storage_only_hosts.txt"


class StorageOnlyHost(RuntimeError):
    pass


def _private_dirs():
    out = [ROOT / "private"]
    try:                                       # a worktree: the main repo folder holds private/
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=ROOT,
                                capture_output=True, text=True, timeout=10).stdout.strip()
        if common:
            out.append(Path(common).parent / "private")
    except (OSError, subprocess.SubprocessError):
        pass
    return out


def storage_only_hosts(paths=None):
    hosts = set()
    for d in (paths or _private_dirs()):
        p = Path(d) / LIST_NAME
        if p.exists():
            hosts |= {l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith("#")}
    return hosts


def refuse_storage_host(host, what="a job", paths=None):
    if host in storage_only_hosts(paths):
        raise StorageOnlyHost(f"refused: {what} on host '{host}', which is storage and relay only (spec 2026-11-04); "
                              "compute runs on cluster nodes through Slurm")
