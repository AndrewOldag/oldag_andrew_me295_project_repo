"""Batch 2 driver (spec 2026-11-04; the code that ran batch 2, Argon A5-F7). Hosts and folders come from a private file.

  python scripts/full_batch_2_driver.py [--settings private/full_batch_2.yaml] [--max-roots N]

One persistent connection to the storage host (measure/remote_link.py); every cluster command and copy is relayed
through the storage host's connection master. The storage host only stores and relays: no Python, no job, nothing left
running there. Per root, in the order of the roots file, skipping roots already collected (markers in the state dir):
  stage   whole root imgdir storage -> cluster c019/data (work folder <= 35 GB), after free VM memory >= 3 GB
  submit  one GPU job (scripts/remote/full_batch_2_root_job.sh: all steps, moved copy on w10-12, checker), ledger
          check first, at most 4 jobs queued or running (Andrew, 2026-11-04); no submit once spend + worst case
          would reach $12
  collect when the job left the queue: copy fb2/<root>/ (without moved/) to the storage host, md5 of every file on
          both ends (LF), md5.txt beside; only then delete the moved-copy frames and the staged root imgdir on the
          cluster (Andrew, 2026-10-26 and 2026-11-04), each logged in DELETED.log; copy check/<wid>.json to this machine
Before each step (stage, submit, collect): the cluster connection master check; down: stop, connection_down marker,
Needs Andrew (Argon A5-F5).

Settings (YAML, git-ignored, in private/ of the main repo folder): storage_host, cluster_alias, cluster_dir (work
folder on the cluster), storage_dir (batch-2 output folder on the storage host), roots (file: root id TAB storage
imgdir), ledger ([program, script]), code_dir, tracker_dir, env_activate, ft2_code, ft2_weights (on the cluster),
state_dir (optional; default private/fb2_state of this worktree).

Audit records (inbox items 17, 18) in the state dir, one JSON line each: audit_outputs.jsonl and audit_deletes.jsonl
carry `verified`, the time of the md5 comparison made before the deletes of the same collect() call;
audit_connection.jsonl the connection events.
"""
import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from measure.hosts import _private_dirs  # noqa: E402
from measure.real_runner import _ledger_from, vm_free_gb  # noqa: E402
from measure.remote_link import Link, LinkDown, MasterDown, Relay  # noqa: E402

JOB_SCRIPT = ROOT / "scripts" / "remote" / "full_batch_2_root_job.sh"
CHECKS = ROOT / "staging" / "full_batch_2_cluster" / "windows"
CAP_MB, LIMIT_USD, MAX_JOBS, MAX_AHEAD, VM_MIN_GB = 35840, 12.0, 4, 6, 3.0   # 4 jobs: Andrew, 2026-11-04 23:10
JOB_ENV = {"code_dir": "CODE", "tracker_dir": "QB", "env_activate": "ENV_ACTIVATE", "ft2_code": "FT2_CODE",
           "ft2_weights": "FT2_WEIGHTS"}                                   # settings key -> job script variable


def q(s):
    return "'" + s.replace("'", "'\\''") + "'"


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def load_settings(path=None):
    import yaml
    if path is None:
        path = next((d / "full_batch_2.yaml" for d in _private_dirs() if (d / "full_batch_2.yaml").exists()), None)
        if path is None:
            sys.exit("no private/full_batch_2.yaml (git-ignored settings: hosts and folders)")
    return yaml.safe_load(Path(path).read_text())


def windows_of(root):
    import full_batch as fb
    return [w for w in fb.batch_windows(2) if w.root_id == root]


class Driver:
    def __init__(self, s, link, relay, ledger, state, checks=CHECKS, free_gb=vm_free_gb, windows=windows_of,
                 sleep=time.sleep):
        self.s, self.link, self.relay, self.ledger = s, link, relay, ledger
        self.state, self.checks, self.free_gb, self.windows_of, self.sleep = Path(state), Path(checks), free_gb, \
            windows, sleep
        self.T, self.LAB = s["cluster_dir"], s["storage_dir"]
        self.jobdir = f"{self.T}/fb2/jobs/root_v2"

    # ---- records
    def log(self, msg):
        line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
        print(line, flush=True)
        with open(self.state / "driver.log", "a") as f:
            f.write(line + "\n")

    def audit(self, log_kind, **row):
        with open(self.state / f"audit_{log_kind}.jsonl", "a") as f:
            f.write(json.dumps(row) + "\n")

    def link_log(self, msg):
        self.log(msg)
        m = re.match(r"(\S+) link \S+: (.*)", msg)
        if m:
            self.audit("connection", time=m.group(1), event="persistent connection", outcome=m.group(2))

    def mark(self, root, step, text=""):
        (self.state / f"{root}.{step}").write_text(text or now())

    def has(self, root, step):
        return (self.state / f"{root}.{step}").exists()

    def lab(self, cmd, stdin=None, check=True):
        return self.link.run(cmd, stdin, check).decode(errors="replace")

    def cl(self, cmd, stdin=None, check=True):
        return self.relay.run(cmd, stdin, check).decode(errors="replace")

    # ---- steps
    def install_job(self):
        """The committed job script in the cluster job folder; an existing different script is not overwritten."""
        body = JOB_SCRIPT.read_bytes().replace(b"\r\n", b"\n")
        p = f"{self.jobdir}/job.sbatch"
        if self.cl(f"test -f {p} && echo yes || echo no").strip() == "yes":
            import hashlib
            if self.cl(f"md5sum {p}").split()[0] != hashlib.md5(body).hexdigest():
                raise RuntimeError("job.sbatch in the job folder differs from the committed job script; use a new folder")
            return
        self.cl(f"mkdir -p {self.jobdir} {self.T}/fb2/logs && cat > {p}", stdin=body)

    def stage(self, root, img):
        self.relay.require_master()
        if (free := self.free_gb()) < VM_MIN_GB:          # skip this round; staged roots still get submitted
            self.log(f"VM memory {free:.1f} GB free, below {VM_MIN_GB} GB; staging of {root} waits")
            return False
        need = int(self.lab(f"du -sm {q(img)} | cut -f1").split()[0])
        used = int(self.cl(f"du -sm {self.T} | cut -f1").split()[0])
        if used + need > CAP_MB:
            return False
        self.log(f"{root}: staging {need} MB (folder {used} MB)")
        dest = f"{self.T}/c019/data/{root}.imgdir"
        self.cl(f"mkdir -p {dest} {self.T}/fb2/{root}")
        self.relay.push(img.rstrip("/") + "/", dest + "/")
        n_lab, n_cl = self.lab(f"ls {q(img)} | wc -l").strip(), self.cl(f"ls {dest} | wc -l").strip()
        if n_lab != n_cl:
            raise RuntimeError(f"{root}: {n_cl} files staged, {n_lab} expected")
        self.cl(f"cat > {self.T}/fb2/{root}/windows.tsv",
                stdin="".join(f"{w.id()} {w.from_h:g} {w.to_h:g}\n" for w in self.windows_of(root)))
        self.mark(root, "staged", f"{n_cl} files, {need} MB")
        return True

    def jobs_live(self):
        return int(self.cl("squeue -u \"$(whoami)\" -h | wc -l").strip() or 0)

    def submit(self, root):
        self.relay.require_master()
        rc, msg = self.ledger("check", self.jobdir)
        m = re.search(r"= ([\d.]+) \(cap", msg)
        if rc or not m or float(m.group(1)) >= LIMIT_USD:
            self.log(f"{root}: not submitted: {msg}")
            return "stop"
        env = ",".join(f"{v}={self.s[k]}" for k, v in JOB_ENV.items())
        logs = f"{self.T}/fb2/logs"
        jid = self.cl(f"cd {self.jobdir} && sbatch --parsable -o {logs}/%x_%j.out -e {logs}/%x_%j.err "
                      f"--export=ALL,ROOT={root},T={self.T},{env} job.sbatch").strip().split(";")[0]
        if not jid.isdigit():
            raise RuntimeError(f"{root}: sbatch said {jid!r}")
        self.ledger("record", self.jobdir, jid)
        self.mark(root, "submitted", jid)
        self.log(f"{root}: job {jid} ({msg})")
        return jid

    def delete_logged(self, path, why, root, kind, md5s, verified):
        T = self.T
        out = self.cl(f"if [ -e {path} ]; then s=$(du -sh {path} | cut -f1); t=$(date -Is); rm -r {path} && "
                      f"echo \"$t deleted {path} $s; {why}\" >> {T}/c019/DELETED.log && echo \"$t $s\"; fi").strip()
        if out:
            t, size = out.split()[:2]
            self.audit("deletes", root=root, kind=kind, size=size, time=t, checked_md5=";".join(md5s), verified=verified)

    def collect(self, root):
        T, LAB = self.T, self.LAB
        jid = (self.state / f"{root}.submitted").read_text().strip()
        self.relay.require_master()
        if self.cl(f"squeue -j {jid} -h | wc -l").strip() != "0":
            return False
        self.ledger("final", jid)
        self.relay.pull(f"{T}/fb2/{root}/", f"{LAB}/{root}/", exclude=("moved/",))
        md5 = "find . -type f ! -path './moved/*' ! -name md5.txt | sort | xargs md5sum"
        a = self.cl(f"cd {T}/fb2/{root} && {md5}").replace("\r\n", "\n")
        b = self.lab(f"cd {LAB}/{root} && {md5}").replace("\r\n", "\n")
        if not a or a != b:
            self.mark(root, "error", "md5 mismatch after copy; frames kept")
            self.log(f"{root}: md5 mismatch; frames kept")
            return True
        self.lab(f"cat > {LAB}/{root}/md5.txt", stdin=b.encode())
        verified = now()                                  # the md5 comparison above; every delete below follows it
        md5_of = {l.split(None, 1)[1].strip(): l.split()[0] for l in b.splitlines() if l.strip()}
        for wd in self.windows_of(root):
            self.audit("outputs", root=root, window=wd.id(),
                       track_md5=md5_of.get(f"./tracks/{wd.id()}_ft2__st1__L1000.npz", ""),
                       check_md5=md5_of.get(f"./check/{wd.id()}.json", ""), on_lab_server="yes", verified=verified)
        tracks = [l for l in b.splitlines() if l.endswith("__st1__L1000.npz") and "_wp_" not in l]
        done = self.cl(f"test -f {T}/fb2/{root}/root.done && echo yes || echo no").strip() == "yes"
        if not done:
            missing = [w.id() for w in self.windows_of(root) if f"tracks/{w.id()}_ft2__st1__L1000.npz" not in b]
            errs = []
            for wid in missing:
                tail = self.cl(f"tail -1 {T}/fb2/{root}/log/{wid}_track.log 2>/dev/null", check=False).strip()
                if re.match(r"^\w+(Error|Exception): ", tail):
                    errs.append(f"{wid}: {tail[:120]}")
            done = len(errs) == len(missing)
            if done:
                self.lab(f"cat > {LAB}/{root}/tracker_errors.txt", stdin=("\n".join(errs) + "\n").encode())
                self.log(f"{root}: {len(missing)} window(s) without a track, tracker error: {'; '.join(errs)}")
        if not done:
            self.mark(root, "error", f"job {jid} ended with {len(tracks)} tracks; frames kept")
            self.log(f"{root}: job {jid} ended with {len(tracks)} tracks of {len(self.windows_of(root))}; frames kept")
            return True
        w = f"{root}__w10-12"
        if f"tracks/{w}_ft2_wp_moved__st1__L1000.npz" in b and f"tracks/{w}_ft2_wp_ref__st1__L1000.npz" in b:
            for k in ("moved", "ref"):
                self.delete_logged(f"{T}/fb2/{root}/moved/{w}_wp_{k}.imgdir",
                                   f"root {root}: moved-copy frames; its track md5-verified on the lab server; "
                                   "Andrew 2026-11-04",
                                   root, "moved_copy", [md5_of.get(f"./tracks/{w}_ft2_wp_{k}__st1__L1000.npz", "")],
                                   verified)
        self.delete_logged(f"{T}/c019/data/{root}.imgdir",
                           f"root {root}: outputs ({len(tracks)} tracks) md5-verified on the lab server; "
                           "Andrew 2026-10-26",
                           root, "staged_root", [l.split()[0] for l in tracks], verified)
        self.checks.mkdir(parents=True, exist_ok=True)
        n = 0
        for wd in self.windows_of(root):
            if f"check/{wd.id()}.json" in b:
                (self.checks / f"{wd.id()}.json").write_bytes(self.link.run(f"cat {LAB}/{root}/check/{wd.id()}.json"))
                n += 1
        self.mark(root, "collected", f"job {jid}, {len(tracks)} tracks, {n} checks")
        self.log(f"{root}: collected ({len(tracks)} tracks, {n} checks), md5 verified, frames cleared")
        return True

    def down(self, why):
        self.audit("connection", time=now(), event="cluster master check", outcome="failed")
        self.log(f"{why}: stopping (Needs Andrew)")
        (self.state / "connection_down").write_text(now())

    def loop(self, roots, once=False):
        has = self.has
        (self.state / "connection_down").unlink(missing_ok=True)
        stop_submit = False
        while True:
            try:
                self.relay.require_master()
                for root, _ in roots:
                    if has(root, "submitted") and not has(root, "collected") and not has(root, "error"):
                        self.collect(root)
                ahead = [r for r, _ in roots if has(r, "staged") and not has(r, "collected") and not has(r, "error")]
                for root, img in roots:
                    if len(ahead) >= MAX_AHEAD or stop_submit:
                        break
                    if not has(root, "staged") and not has(root, "collected"):
                        if not self.stage(root, img):
                            break
                        ahead.append(root)
                for root, _ in roots:
                    if stop_submit or self.jobs_live() >= MAX_JOBS:
                        break
                    if has(root, "staged") and not has(root, "submitted"):
                        if self.submit(root) == "stop":
                            stop_submit = True
                pending = [r for r, _ in roots if not has(r, "collected") and not has(r, "error")]
                live = [r for r, _ in roots if has(r, "submitted") and not has(r, "collected") and not has(r, "error")]
                if not pending or (stop_submit and not live):
                    self.log(f"end: {sum(has(r, 'collected') for r, _ in roots)} collected, "
                             f"{sum(has(r, 'error') for r, _ in roots)} errors, {len(pending)} not done")
                    (self.state / "driver.done").write_text(now())
                    return "done"
            except MasterDown as e:
                self.down(f"cluster connection down ({e})")
                return "master down"
            except LinkDown as e:
                self.down(f"lab server connection lost: {e}")
                return "link down"
            except Exception as e:                                      # noqa: BLE001 - log, wait, retry
                self.log(f"error: {type(e).__name__}: {str(e)[:300]}")
            if once:
                return "again"
            self.sleep(120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--settings")
    ap.add_argument("--max-roots", type=int, default=999)
    a = ap.parse_args()
    s = load_settings(a.settings)
    state = Path(s.get("state_dir") or ROOT / "private" / "fb2_state")
    state.mkdir(parents=True, exist_ok=True)
    roots = [l.split("\t") for l in Path(s["roots"]).read_text().splitlines() if l.strip()][:a.max_roots]
    holder = {}
    link = Link(s["storage_host"], log=lambda m: holder["d"].link_log(m))
    relay = Relay(link, s["cluster_alias"])
    d = holder["d"] = Driver(s, link, relay, _ledger_from(s), state)
    d.install_job()
    print(d.loop(roots))
    link.close()


if __name__ == "__main__":
    main()
