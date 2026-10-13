"""Pre-push gatekeeper: block content that must not reach the public repo.

Scans the commits being pushed: every file each commit adds or changes
(content at that commit) and each commit message. Fails if any rule hits.
Rules: private blocklist, host names, IP addresses, user-at-host, absolute
paths outside the repo, keys and tokens, image or data files, files over
5 MB, files under private/, data/ or staging/.

Output names the rule, commit, file and line only. Matched text is never
printed.

Usage:
  As a git pre-push hook: pre_push_check.py REMOTE URL  (ref lines on stdin)
  By hand: pre_push_check.py --commits main             (whole history of main)
           pre_push_check.py --commits A..B
Options: --blocklist PATH (default: private/blocklist.txt in the main repo
folder, found from the git common dir).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ZERO = "0" * 40
MAX_BYTES = 5 * 1024 * 1024
DATA_EXT = {".tif", ".tiff", ".npy", ".sldy", ".h5", ".hdf5"}
BLOCKED_DIRS = {"private", "data", "staging"}

# Public domains allowed in text. A host is allowed if it equals one of
# these or ends with "." plus one of these.
ALLOWED_DOMAINS = {
    "github.com", "githubusercontent.com", "anthropic.com", "claude.ai",
    "claude.com", "conda-forge.org", "anaconda.org", "anaconda.com",
    "python.org", "pypi.org", "doi.org", "arxiv.org", "biorxiv.org",
    "readthedocs.io", "numpy.org", "scipy.org", "matplotlib.org",
    "pytorch.org", "wikipedia.org", "example.com", "example.org",
}
# Allowed only exactly, not with a subdomain (lab hosts sit under these).
ALLOWED_HOSTS_EXACT = {"caltech.edu", "www.caltech.edu"}
ALLOWED_EMAILS = {"noreply@anthropic.com", "noreply@github.com", "git@github.com"}
ALLOWED_IPS = {"127.0.0.1", "0.0.0.0"}

TLDS = ("com|org|net|edu|gov|mil|io|ai|dev|cloud|app|info|biz|"
        "local|localdomain|lan|internal|intranet|corp|home|cluster")
HOST_RE = re.compile(
    r"(?<![\w.@/-])((?:[A-Za-z0-9-]+\.)+(?:" + TLDS + r"))(?![\w-]|\.[A-Za-z0-9])",
    re.IGNORECASE)
IP_RE = re.compile(r"(?<![\w.=-])(\d{1,3}(?:\.\d{1,3}){3})(?![\w.=-])")
EMAIL_RE = re.compile(r"(?<![\w.+%-])([\w.+%-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*)")
PATH_RE = re.compile(r"/(?:mnt|home|Users)/|(?<![\w])[A-Za-z]:[\\/](?![\\/])")
KEY_RES = [
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY( BLOCK)?-----"),
    re.compile(r"\b(?:ssh-(?:rsa|dss|ed25519)|ecdsa-sha2-nistp\d+|sk-ssh-ed25519[@]openssh\.com)"
               r" AAAA[0-9A-Za-z+/]{16,}"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}"),
    re.compile(r"\bhf_[A-Za-z0-9]{30,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|token|passw(?:or)?d)[\"']?\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']"),
]


def git(args, cwd=None, inp=None):
    r = subprocess.run(["git", *args], cwd=cwd, input=inp, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


def default_blocklist(cwd=None):
    common = Path(git(["rev-parse", "--path-format=absolute", "--git-common-dir"], cwd).decode().strip())
    return common.parent / "private" / "blocklist.txt"


def load_blocklist(path):
    pats = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            pats.append(re.compile(line, re.IGNORECASE))
        except re.error:
            raise SystemExit(f"pre-push: blocklist line {n} is not a valid regex")
    return pats


def host_allowed(host):
    h = host.lower()
    if h in ALLOWED_HOSTS_EXACT:
        return True
    return any(h == d or h.endswith("." + d) for d in ALLOWED_DOMAINS)


def ip_ok(s):
    return all(int(p) <= 255 for p in s.split("."))


def scan_text(text, blocklist):
    """Yield (line_number, rule) for each hit. One hit per rule per line."""
    for n, line in enumerate(text.splitlines(), 1):
        if any(p.search(line) for p in blocklist):
            yield n, "blocklist"
        if any(not host_allowed(m.group(1)) for m in HOST_RE.finditer(line)):
            yield n, "host name"
        if any(ip_ok(m.group(1)) and m.group(1) not in ALLOWED_IPS for m in IP_RE.finditer(line)):
            yield n, "IP address"
        for m in EMAIL_RE.finditer(line):
            e = m.group(1).rstrip(".").lower()
            if e in ALLOWED_EMAILS or e.endswith("@users.noreply.github.com"):
                continue
            yield n, "user-at-host"
            break
        if PATH_RE.search(line):
            yield n, "absolute path"
        if any(k.search(line) for k in KEY_RES):
            yield n, "key or token"


def path_hits(path, size):
    hits = []
    parts = path.replace("\\", "/").split("/")
    if any(p in BLOCKED_DIRS for p in parts[:-1]):
        hits.append("file under private/, data/ or staging/")
    if Path(path).suffix.lower() in DATA_EXT:
        hits.append("image or data file")
    if size > MAX_BYTES:
        hits.append("file over 5 MB")
    return hits


class Blobs:
    """Reads git objects through one `git cat-file --batch` process."""

    def __init__(self, cwd=None):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=cwd,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read(self, sha):
        self.p.stdin.write(sha.encode() + b"\n")
        self.p.stdin.flush()
        header = self.p.stdout.readline().split()
        if len(header) < 3:
            return None
        size = int(header[2])
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return data

    def close(self):
        self.p.stdin.close()
        self.p.wait()


def changed_files(sha, cwd=None):
    """(path, blob sha) for each file the commit adds or changes vs. its first parent."""
    parents = git(["rev-list", "--parents", "-n", "1", sha], cwd).decode().split()[1:]
    base = [parents[0], sha] if parents else ["--root", sha]
    out = git(["diff-tree", "-r", "-z", "--raw", "--no-renames", "--diff-filter=d", *base], cwd)
    fields = out.split(b"\0")
    files = []
    i = 0
    while i + 1 < len(fields):
        meta = fields[i].decode()
        if not meta.startswith(":"):
            i += 1
            continue
        _, new_mode, _, new_sha, _ = meta[1:].split(" ")
        path = fields[i + 1].decode("utf-8", errors="replace")
        if new_mode != "160000":
            files.append((path, new_sha))
        i += 2
    return files


def scan_commits(shas, blocklist, cwd=None):
    """Return a list of (commit, location, line or None, rule)."""
    hits = []
    blobs = Blobs(cwd)
    try:
        for sha in shas:
            raw = blobs.read(sha) or b""
            msg = raw.split(b"\n\n", 1)[1] if b"\n\n" in raw else b""
            for n, rule in scan_text(msg.decode("utf-8", errors="replace"), blocklist):
                hits.append((sha, "(commit message)", n, rule))
            for path, blob in changed_files(sha, cwd):
                for rule in path_hits(path, 0):
                    hits.append((sha, path, None, rule))
                data = blobs.read(blob)
                if data is None:
                    continue
                if len(data) > MAX_BYTES:
                    hits.append((sha, path, None, "file over 5 MB"))
                if b"\0" in data[:8000]:
                    continue
                for n, rule in scan_text(data.decode("utf-8", errors="replace"), blocklist):
                    hits.append((sha, path, n, rule))
    finally:
        blobs.close()
    return hits


def pushed_commits(remote, lines, cwd=None):
    shas = []
    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        _, local_sha, _, remote_sha = parts
        if local_sha == ZERO:
            continue
        args = ["rev-list", local_sha, "--not", f"--remotes={remote}"]
        if remote_sha != ZERO and subprocess.run(
                ["git", "cat-file", "-e", remote_sha], cwd=cwd, capture_output=True).returncode == 0:
            args.append(remote_sha)
        for s in git(args, cwd).decode().split():
            if s not in shas:
                shas.append(s)
    return shas


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("remote", nargs="?")
    ap.add_argument("url", nargs="?")
    ap.add_argument("--commits", nargs="+", metavar="REV", help="scan these revisions (git rev-list arguments)")
    ap.add_argument("--blocklist", help="blocklist file (default: private/blocklist.txt of the main repo folder)")
    a = ap.parse_args(argv)

    bl_path = Path(a.blocklist) if a.blocklist else default_blocklist()
    if not bl_path.is_file():
        print(f"pre-push: blocklist not found ({'--blocklist' if a.blocklist else 'private/blocklist.txt'}); "
              "push blocked", file=sys.stderr)
        return 1
    blocklist = load_blocklist(bl_path)

    if a.commits:
        shas = git(["rev-list", *a.commits]).decode().split()
    else:
        shas = pushed_commits(a.remote or "origin", sys.stdin.read().splitlines())

    hits = scan_commits(shas, blocklist)
    for sha, where, n, rule in hits:
        loc = f"{where}:{n}" if n else where
        print(f"pre-push: {rule}: {sha[:10]} {loc}", file=sys.stderr)
    print(f"pre-push: {len(shas)} commits scanned, {len(hits)} hits", file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
