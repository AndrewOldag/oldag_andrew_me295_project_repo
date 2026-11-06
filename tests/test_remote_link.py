"""Link and Relay (measure/remote_link.py) with a fake ssh transport; no real host is contacted."""
import pytest

from measure.remote_link import CommandFailed, Link, LinkDown, MasterDown, Relay


class FakeChannel:
    def __init__(self, server, fail=False):
        self.server, self.fail, self.cmd, self.stdin = server, fail, None, b""

    def exec_command(self, cmd):
        if self.fail:
            raise EOFError("dropped")
        self.cmd = cmd
        self.server.commands.append(cmd)

    def sendall(self, b):
        self.stdin += b

    def shutdown_write(self):
        out, err, code = self.server.reply(self.cmd, self.stdin)
        self._out, self._err, self._code = out, err, code

    def recv_ready(self):
        return bool(self._out)

    def recv(self, n):
        b, self._out = self._out[:n], self._out[n:]
        return b

    def recv_stderr_ready(self):
        return bool(self._err)

    def recv_stderr(self, n):
        b, self._err = self._err[:n], self._err[n:]
        return b

    def exit_status_ready(self):
        return True

    def recv_exit_status(self):
        return self._code

    def close(self):
        pass


class FakeTransport:
    def __init__(self, server):
        self.server, self.active = server, True

    def is_active(self):
        return self.active

    def open_session(self):
        fail = self.server.drop_next > 0
        if fail:
            self.server.drop_next -= 1
            self.active = False
        return FakeChannel(self.server, fail)


class FakeClient:
    def __init__(self, server):
        self.t = FakeTransport(server)

    def get_transport(self):
        return self.t

    def close(self):
        self.t.active = False


class FakeServer:
    """Replies by command; counts connects; can refuse connects or drop channels."""

    def __init__(self, refuse=0, drop_next=0):
        self.refuse, self.drop_next = refuse, drop_next
        self.connects, self.commands = 0, []
        self.master_down = False

    def connect(self, host):
        self.connects += 1
        if self.refuse > 0:
            self.refuse -= 1
            raise OSError("connection refused")
        return FakeClient(self)

    def reply(self, cmd, stdin):
        if cmd.startswith("false"):
            return b"", b"boom\n", 1
        if cmd.startswith("ssh -G "):
            return b"user u\ncontrolpath /s/sock-cluster-22\ncontrolmaster auto\n", b"", 0
        if "ssh -O check" in cmd and self.master_down:      # the check alone, or the guard in front of a command
            return b"", b"Control socket connect(/s/sock-cluster-22): No such file or directory\r\n", 255
        if cmd.startswith("ssh -O check") and "&&" not in cmd:
            return b"Master running (pid=1)\r\n", b"", 0
        if "md5sum" in cmd:
            return b"aa  ./x.npz\r\nbb  ./y.npz\r\n", b"", 0
        return b"out:" + cmd.encode() + (b"|" + stdin if stdin else b""), b"", 0


def link(server, sleeps=None):
    return Link("storage", connect=server.connect, sleep=(sleeps.append if sleeps is not None else lambda s: None))


def test_one_connection_for_many_commands():
    s = FakeServer()
    lk = link(s)
    for i in range(5):
        assert lk.run(f"echo {i}") == f"out:echo {i}".encode()
    assert s.connects == 1
    assert [e[1] for e in lk.events] == ["connected"]


def test_stdin_and_failed_command():
    s = FakeServer()
    lk = link(s)
    assert lk.run("cat > f", stdin="abc") == b"out:cat > f|abc"
    with pytest.raises(CommandFailed):
        lk.run("false")
    assert lk.run("false", check=False) == b""


def test_drop_reconnects_and_retries_with_log():
    s = FakeServer()
    lk = link(s)
    lk.run("echo 1")
    s.drop_next = 1
    assert lk.run("echo 2") == b"out:echo 2"
    assert s.connects == 2
    texts = [e[1] for e in lk.events]
    assert "reconnected" in texts and any(t.startswith("channel lost") for t in texts)


def test_backoff_then_link_down_after_three_failures():
    sleeps = []
    s = FakeServer(refuse=5)
    lk = link(s, sleeps)
    with pytest.raises(LinkDown):
        lk.run("echo 1")
    assert sleeps == [10, 30]               # two waits between three failed attempts
    assert s.connects == 3


def test_reconnect_succeeds_within_backoff():
    sleeps = []
    s = FakeServer(refuse=2)
    lk = link(s, sleeps)
    assert lk.run("echo 1") == b"out:echo 1"
    assert sleeps == [10, 30] and lk.failed_in_row == 0


def test_relay_goes_through_storage_host_only():
    s = FakeServer()
    r = Relay(link(s), "clusteralias")
    assert r.master_ok()
    r.run("squeue -u me")
    r.push("/data/root.imgdir/", "/work/data/root.imgdir/")
    r.pull("/work/out/root/", "/data/out/root/")
    assert s.connects == 1
    sent = [c for c in s.commands if not c.startswith(("ssh -O check clusteralias 2>&1", "ssh -G "))]
    guard = "ssh -O check -o ControlPath=/s/sock-cluster-22 clusteralias >/dev/null 2>&1 && "
    opts = "-o BatchMode=yes -o ControlMaster=no -o ControlPath=/s/sock-cluster-22"
    assert sent[0] == f"{guard}ssh {opts} clusteralias 'squeue -u me'"
    assert sent[1].startswith(f"{guard}rsync -a -s --bwlimit=50000 -e 'ssh {opts}' /data/root.imgdir/ clusteralias:")
    assert sent[2].startswith(f"mkdir -p /data/out/root/ && {guard}rsync -a -s -e 'ssh {opts}' clusteralias:")


def test_relay_never_opens_a_cluster_login_and_stops_when_master_down():
    """Argon A5-F5: every relayed ssh is ControlMaster=no behind the master check; master down raises MasterDown."""
    s = FakeServer()
    r = Relay(link(s), "c")
    r.run("true")
    s.master_down = True
    assert not r.master_ok()
    with pytest.raises(MasterDown):
        r.require_master()
    with pytest.raises(MasterDown):
        r.run("sbatch job.sbatch")
    with pytest.raises(MasterDown):
        r.push("/a/", "/b/")
    relayed = [c for c in s.commands if " c " in c and not c.startswith(("ssh -O check c 2>&1", "ssh -G "))]
    assert relayed and all(c.startswith("ssh -O check -o ControlPath=") and "ControlMaster=no" in c for c in relayed)


def test_md5_tree_normalizes_line_ends():
    r = Relay(link(FakeServer()), "c")
    assert r.md5_tree("storage", "/d") == "aa  ./x.npz\nbb  ./y.npz\n"
    assert r.md5_tree("cluster", "/d") == r.md5_tree("storage", "/d")
