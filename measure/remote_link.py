"""One persistent ssh connection from this machine to the storage host, and the relay to the cluster through it.

Spec 2026-11-04 (Andrew): the lab server is storage and relay only; every VM command to it is a channel on one
connection held for the whole run (`Link`); the lab server reaches the cluster only through the connection master
Andrew opens there (`Relay`). Nothing here opens a second login to the cluster or starts a job on the storage host.

`Link(host)`: a paramiko Transport with a 30 s keepalive. A command that fails because the connection dropped
reconnects with backoff (10 s, 30 s, 60 s, then every 5 min) and is retried; each reconnect is logged with its time;
after 3 failed reconnects in a row `LinkDown` is raised (stop; Needs Andrew). Host name, user and key come from the
ssh config of this machine (`~/.ssh/config`), so no tracked file names them.

Tests pass `connect=` a fake factory; no real host is ever contacted from the tests.
"""
import datetime
import os
import shlex
import time
from pathlib import Path

BACKOFF_S = (10, 30, 60)      # then every REPEAT_S
REPEAT_S = 300
MAX_FAILED_RECONNECTS = 3
KEEPALIVE_S = 30


class LinkDown(RuntimeError):
    """The storage-host connection could not be re-established: stop and ask Andrew."""


class CommandFailed(RuntimeError):
    def __init__(self, cmd, code, stderr):
        super().__init__(f"remote command failed ({code}): {stderr.strip().splitlines()[-1:] if stderr else ''}")
        self.cmd, self.code, self.stderr = cmd, code, stderr


def _paramiko_connect(host):
    """A connected paramiko Transport for `host`, resolved through ~/.ssh/config (HostName, User, IdentityFile)."""
    import paramiko
    cfg = paramiko.SSHConfig()
    p = Path(os.path.expanduser("~/.ssh/config"))
    if p.exists():
        with open(p) as fh:
            cfg.parse(fh)
    h = cfg.lookup(host)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(h.get("hostname", host), port=int(h.get("port", 22)), username=h.get("user"),
                   key_filename=h.get("identityfile"), timeout=30, banner_timeout=30, auth_timeout=30,
                   allow_agent=True, look_for_keys=True)
    t = client.get_transport()
    t.set_keepalive(KEEPALIVE_S)
    return client


class Link:
    """Every `run` is a channel on one held connection; reconnects as described in the module docstring."""

    def __init__(self, host, connect=None, sleep=time.sleep, log=None):
        self.host = host
        self._connect = connect or _paramiko_connect
        self._sleep = sleep
        self.events = []                 # (iso time, text): connects, drops, reconnects
        self._log = log
        self._client = None
        self.failed_in_row = 0

    def _note(self, text):
        e = (datetime.datetime.now().isoformat(timespec="seconds"), text)
        self.events.append(e)
        if self._log:
            self._log(f"{e[0]} link {self.host}: {text}")

    def _alive(self):
        t = self._client.get_transport() if self._client else None
        return bool(t and t.is_active())

    def connect(self):
        """Connect, or reconnect after a drop, with the backoff schedule. Raises LinkDown after 3 failures in a row."""
        attempt = 0
        while True:
            try:
                self._client = self._connect(self.host)
                self._note("connected" if not self.events else "reconnected")
                self.failed_in_row = 0
                return
            except Exception as e:                       # noqa: BLE001 - any connect error counts as a failure
                self.failed_in_row += 1
                self._note(f"connect failed ({type(e).__name__}: {str(e)[:120]})")
                if self.failed_in_row >= MAX_FAILED_RECONNECTS:
                    raise LinkDown(f"{self.host}: {self.failed_in_row} failed reconnects in a row") from e
                self._sleep(BACKOFF_S[attempt] if attempt < len(BACKOFF_S) else REPEAT_S)
                attempt += 1

    def run(self, cmd, stdin=None, check=True):
        """Run `cmd` on the storage host as one channel; returns stdout bytes. A dropped connection is reconnected
        and the command run again (commands sent here are idempotent: tests, listings, copies that skip done work).
        A command whose channel is lost 3 times in a row raises LinkDown."""
        lost = 0
        while True:
            if lost >= MAX_FAILED_RECONNECTS:
                raise LinkDown(f"{self.host}: channel lost {lost} times in a row on one command")
            if not self._alive():
                if self._client is not None:
                    self._note("connection dropped")
                self.connect()
            try:
                chan = self._client.get_transport().open_session()
                chan.exec_command(cmd)
                if stdin is not None:
                    chan.sendall(stdin if isinstance(stdin, bytes) else stdin.encode())
                chan.shutdown_write()
                out, err = bytearray(), bytearray()
                while True:
                    if chan.recv_ready():
                        out += chan.recv(65536)
                    elif chan.recv_stderr_ready():
                        err += chan.recv_stderr(65536)
                    elif chan.exit_status_ready() and not chan.recv_ready() and not chan.recv_stderr_ready():
                        break
                    else:
                        self._sleep(0.01)
                code = chan.recv_exit_status()
                chan.close()
            except (EOFError, OSError, ConnectionError) as e:
                lost += 1
                self._note(f"channel lost ({type(e).__name__})")
                try:
                    self._client.close()
                except Exception:                           # noqa: BLE001 - already broken
                    pass
                self._client = None
                continue
            if check and code != 0:
                raise CommandFailed(cmd, code, err.decode(errors="replace"))
            return bytes(out)

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None


class Relay:
    """Commands and copies to the cluster, run from the storage host through its existing connection master only."""

    def __init__(self, link, alias):
        self.link, self.alias = link, alias

    def master_ok(self):
        out = self.link.run(f"ssh -O check {shlex.quote(self.alias)} 2>&1", check=False).decode(errors="replace")
        return "Master running" in out

    def run(self, cmd, stdin=None, check=True):
        return self.link.run(f"ssh -o BatchMode=yes {shlex.quote(self.alias)} {shlex.quote(cmd)}", stdin, check)

    def push(self, src, dest, bwlimit_kbs=50000):
        """Copy a folder or file on the storage host to the cluster (rsync over the master)."""
        return self.link.run(f"rsync -a -s --bwlimit={bwlimit_kbs} -e 'ssh -o BatchMode=yes' "
                             f"{shlex.quote(src)} {shlex.quote(self.alias)}:{shlex.quote(dest)}")

    def pull(self, src, dest):
        """Copy a folder or file on the cluster to the storage host (rsync over the master)."""
        return self.link.run(f"mkdir -p {shlex.quote(dest)} && rsync -a -s -e 'ssh -o BatchMode=yes' "
                             f"{shlex.quote(self.alias)}:{shlex.quote(src)} {shlex.quote(dest)}")

    def md5_tree(self, where, path):
        """md5 of every file under `path` (sorted, LF line ends); where = 'storage' or 'cluster'."""
        cmd = f"cd {shlex.quote(path)} && find . -type f ! -name md5.txt | sort | xargs md5sum"
        out = self.link.run(cmd) if where == "storage" else self.run(cmd)
        return out.decode().replace("\r\n", "\n")
