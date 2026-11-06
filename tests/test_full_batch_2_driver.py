"""Batch-2 driver (scripts/full_batch_2_driver.py, Argon A5-F7) against a fake ssh: no real host is contacted."""
import json
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import full_batch_2_driver as drv  # noqa: E402
from measure.remote_link import CommandFailed, Relay  # noqa: E402

S = {"storage_host": "storage", "cluster_alias": "cl", "cluster_dir": "/cw", "storage_dir": "/st/fb2",
     "code_dir": "/cw/code", "tracker_dir": "/cw/qb", "env_activate": "/cw/env.sh", "ft2_code": "/cw/ft2",
     "ft2_weights": "/cw/ft2/w.pt"}
WIDS = ["r1__w0-2", "r1__w10-12"]


class W:
    def __init__(self, wid):
        self.wid, self.root_id = wid, "r1"
        a, b = wid.split("__w")[1].split("-")
        self.from_h, self.to_h = float(a), float(b)

    def id(self):
        return self.wid


def listing(bad=False):
    files = [f"./check/{w}.json" for w in WIDS] + [f"./tracks/{w}_ft2__st1__L1000.npz" for w in WIDS] + \
        [f"./tracks/r1__w10-12_ft2_wp_{k}__st1__L1000.npz" for k in ("ref", "moved")]
    return "".join(f"{'ff' if bad and i == 0 else 'aa'}{i:030d}  {f}\n" for i, f in enumerate(sorted(files)))


class FakeLink:
    """Storage commands and relayed cluster commands, in order; the master can be down."""

    def __init__(self, lab_md5_bad=False):
        self.cmds, self.master, self.lab_md5_bad = [], True, lab_md5_bad

    def run(self, cmd, stdin=None, check=True):
        self.cmds.append(cmd)
        if cmd.startswith("ssh -G "):
            return b"controlpath /s/sock\n"
        if cmd.startswith("ssh -O check") and "&&" not in cmd:
            return b"Master running (pid=1)\n" if self.master else b"Control socket connect: No such file\n"
        if cmd.startswith("ssh -O check"):
            if not self.master:
                raise CommandFailed(cmd, 255, "")
            rest = cmd.split("&& ", 1)[1]
            return b"" if rest.startswith("rsync ") else self.on_cluster(shlex.split(rest)[-1])
        return self.on_storage(cmd)

    def on_cluster(self, c):
        if c.startswith("du -sm"):
            return b"1000\t/cw\n"
        if c.startswith("ls "):
            return b"10\n"
        if c.startswith("squeue"):
            return b"0\n"
        if "sbatch --parsable" in c:
            return b"777\n"
        if c.startswith("test -f") and "job.sbatch" in c:
            return b"no\n"
        if c.startswith("test -f") and "root.done" in c:
            return b"yes\n"
        if c.startswith("cd ") and "md5sum" in c:
            return listing().encode()
        if c.startswith("if [ -e"):
            return b"2026-11-05T10:00:00-08:00 400M\n"
        return b""

    def on_storage(self, c):
        if c.startswith("du -sm"):
            return b"500\t/img\n"
        if c.startswith("ls "):
            return b"10\n"
        if c.startswith("cd ") and "md5sum" in c:
            return listing(self.lab_md5_bad).encode()
        if c.startswith("cat /st/"):
            return b"{}"
        return b""


def driver(tmp_path, link):
    led = []

    def ledger(action, *a):
        led.append(action)
        return 0, "spent 1.000 + worst case 0.252 = 1.252 (cap 15.00) -> allowed"
    d = drv.Driver(S, link, Relay(link, "cl"), ledger, tmp_path, checks=tmp_path / "checks", free_gb=lambda: 8.0,
                   windows=lambda r: [W(w) for w in WIDS], sleep=lambda s: None)
    return d, led


def run_to_end(d):
    for _ in range(5):
        r = d.loop([["r1", "/img/r1"]], once=True)
        if r != "again":
            return r


def test_deletes_follow_the_md5_check_and_only_through_the_master(tmp_path):
    link = FakeLink()
    d, led = driver(tmp_path, link)
    assert run_to_end(d) == "done"
    rm = [i for i, c in enumerate(link.cmds) if "rm -r" in c]
    md5 = [i for i, c in enumerate(link.cmds) if "md5sum" in c and "find ." in c]
    assert len(rm) == 3 and len(md5) == 2 and max(md5) < min(rm)
    dels = [json.loads(l) for l in (tmp_path / "audit_deletes.jsonl").read_text().splitlines()]
    assert [x["kind"] for x in dels] == ["moved_copy", "moved_copy", "staged_root"]
    assert all(x["verified"] for x in dels)
    assert (tmp_path / "r1.collected").exists() and led == ["check", "record", "final"]
    sub = next(c for c in link.cmds if "sbatch --parsable" in c)
    assert "ROOT=r1" in sub and "CODE=/cw/code" in sub and "FT2_WEIGHTS=/cw/ft2/w.pt" in sub
    relayed = [c for c in link.cmds if " cl:" in c or " cl " in c]
    relayed = [c for c in relayed if not c.startswith("ssh -O check cl 2>&1")]
    assert relayed and all("ControlMaster=no" in c and "ssh -O check -o ControlPath=" in c for c in relayed)


def test_md5_mismatch_keeps_frames(tmp_path):
    link = FakeLink(lab_md5_bad=True)
    d, _ = driver(tmp_path, link)
    run_to_end(d)
    assert not any("rm -r" in c for c in link.cmds)
    assert (tmp_path / "r1.error").exists() and not (tmp_path / "r1.collected").exists()


def test_master_down_stops_before_any_step(tmp_path):
    link = FakeLink()
    link.master = False
    d, led = driver(tmp_path, link)
    assert d.loop([["r1", "/img/r1"]], once=True) == "master down"
    assert (tmp_path / "connection_down").exists() and led == []
    assert not any(k in c for c in link.cmds for k in ("rsync", "sbatch", "rm -r", "du -sm"))


def test_job_script_has_no_host_or_folder_constant():
    body = drv.JOB_SCRIPT.read_text()
    for var in ("$ENV_ACTIVATE", "$FT2_CODE", "$FT2_WEIGHTS", "$CODE", "$QB", "$T/"):
        assert var in body
    assert not re.search(r"^\s*\w+=/", body, re.M) and "#SBATCH --output" not in body   # no folder constant
