"""Compute on cluster nodes through Slurm, reached through the storage host's relay (spec 2026-11-04).

`ClusterCompute(relay, cfg, ledger)` writes one batch script per step into the cluster work folder, checks the spend
ledger before every submit (`ledger("check", job_dir)` must return 0; then `record` with the job id and `final`
after it ends), submits it, waits until it has left the queue and reports its Slurm state. Data move through the
storage host only: `stage_root` copies a whole root imgdir from storage to the cluster (the tracker reads every frame
file of a root, decisions 2026-10-25), `pull` copies outputs back to storage and checks md5 on both ends.

Config keys (private runner yaml, `cluster:` section): work_dir, stage_dir, env (file to source), cpu_partition,
gpu_partition, gpu_gres, cap_mb (work folder cap), max_jobs. No machine name or path is in this file.
"""
import shlex
import time

q = shlex.quote


class BudgetStop(RuntimeError):
    """The ledger refused the submit (spend cap): stop and ask Andrew."""


class JobFailed(RuntimeError):
    pass


class ClusterCompute:
    def __init__(self, relay, cfg, ledger, sleep=time.sleep, poll_s=30, log=None):
        self.relay, self.cfg, self.ledger = relay, cfg, ledger
        self.work = cfg["work_dir"]
        self.stage = cfg.get("stage_dir", f"{cfg['work_dir']}/data")
        self.sleep, self.poll_s = sleep, poll_s
        self.log = log if log is not None else []

    # ---- jobs
    def script(self, name, body, cpus=1, gpu=False, time_limit="01:00:00", mem="16G"):
        c = self.cfg
        head = ["#!/bin/bash", f"#SBATCH --job-name={name}",
                f"#SBATCH --partition={c['gpu_partition'] if gpu else c['cpu_partition']}",
                f"#SBATCH --cpus-per-task={cpus}", f"#SBATCH --mem={mem}", f"#SBATCH --time={time_limit}",
                f"#SBATCH --output={self.work}/logs/%x_%j.out", f"#SBATCH --error={self.work}/logs/%x_%j.err"]
        if gpu:
            head.append(f"#SBATCH --gres={c['gpu_gres']}")
        env = [f"source {q(c['env'])}", f"export OMP_NUM_THREADS={cpus} MKL_NUM_THREADS={cpus} "
               "OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1", "set -uo pipefail"]
        return "\n".join(head + env + [body, ""])

    def submit(self, name, body, **kw):
        job_dir = f"{self.work}/jobs/{name}"
        self.relay.run(f"mkdir -p {q(job_dir)} {q(self.work)}/logs && cat > {q(job_dir)}/job.sbatch",
                       stdin=self.script(name, body, **kw))
        rc, msg = self.ledger("check", job_dir)
        if rc != 0:
            raise BudgetStop(f"{name}: ledger refused: {msg}")
        jid = self.relay.run(f"sbatch --parsable {q(job_dir)}/job.sbatch").decode().strip().split(";")[0]
        if not jid.isdigit():
            raise JobFailed(f"{name}: sbatch said {jid!r}")
        self.ledger("record", job_dir, jid)
        self.log.append({"job": name, "id": jid})
        return jid

    def wait(self, jid):
        while self.relay.run(f"squeue -j {jid} -h | wc -l").decode().strip() != "0":
            self.sleep(self.poll_s)
        state = self.relay.run(f"sacct -j {jid} -X -n -P -o State").decode().strip().splitlines()
        self.ledger("final", jid)
        return state[0].split()[0] if state else "UNKNOWN"

    def run(self, name, body, **kw):
        """Submit, wait, and raise JobFailed unless Slurm reports COMPLETED."""
        jid = self.submit(name, body, **kw)
        state = self.wait(jid)
        self.log[-1]["state"] = state
        if state != "COMPLETED":
            err = self.relay.run(f"tail -5 {q(self.work)}/logs/{name}_{jid}.err 2>/dev/null", check=False).decode()
            raise JobFailed(f"{name} job {jid}: {state}: {err.strip()[-300:]}")
        return jid

    def own_jobs(self):
        return int(self.relay.run("squeue -u \"$(whoami)\" -h | wc -l").decode().strip() or 0)

    # ---- data
    def folder_mb(self):
        return int(self.relay.run(f"du -sm {q(self.work)} | cut -f1").decode().split()[0])

    def stage_root(self, root, storage_imgdir):
        """Copy a whole root imgdir from storage to the cluster unless a complete copy is there (same file count)."""
        dest = f"{self.stage}/{root}.imgdir"
        n_s = self.relay.link.run(f"ls {q(storage_imgdir)} | wc -l").decode().strip()
        n_c = self.relay.run(f"ls {q(dest)} 2>/dev/null | wc -l", check=False).decode().strip()
        if n_s == n_c:
            return dest
        need = int(self.relay.link.run(f"du -sm {q(storage_imgdir)} | cut -f1").decode().split()[0])
        cap = int(self.cfg.get("cap_mb", 35840))
        if self.folder_mb() + need > cap:
            raise JobFailed(f"{root}: staging {need} MB would pass the {cap} MB cluster folder cap")
        self.relay.run(f"mkdir -p {q(dest)}")
        self.relay.push(storage_imgdir.rstrip("/") + "/", dest + "/")
        n_c = self.relay.run(f"ls {q(dest)} | wc -l").decode().strip()
        if n_s != n_c:
            raise JobFailed(f"{root}: {n_c} files staged, {n_s} expected")
        self.log.append({"staged": root, "files": int(n_s), "mb": need})
        return dest

    def push_file(self, storage_path, cluster_path):
        self.relay.run(f"mkdir -p {q(cluster_path.rsplit('/', 1)[0])}")
        self.relay.push(storage_path, cluster_path)

    def pull(self, cluster_path, storage_dir):
        """Copy a cluster file or folder into `storage_dir` and check md5 of every file on both ends."""
        name = cluster_path.rstrip("/").rsplit("/", 1)[1]
        self.relay.pull(cluster_path.rstrip("/"), storage_dir.rstrip("/") + "/")
        src = self._md5("cluster", cluster_path)
        dst = self._md5("storage", f"{storage_dir.rstrip('/')}/{name}")
        if not src or src != dst:
            raise JobFailed(f"md5 mismatch after copying {name} to storage")
        return f"{storage_dir.rstrip('/')}/{name}"

    def _md5(self, where, path):
        cmd = (f"if [ -d {q(path)} ]; then cd {q(path)} && find . -type f | sort | xargs md5sum; "
               f"else md5sum < {q(path)}; fi")
        out = self.relay.link.run(cmd) if where == "storage" else self.relay.run(cmd)
        return out.decode().replace("\r\n", "\n")
