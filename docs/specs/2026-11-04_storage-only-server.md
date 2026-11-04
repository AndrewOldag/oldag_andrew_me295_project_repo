# Spec: lab server for storage only; all compute on cluster nodes; one connection

From: planning account. Date: 2026-11-04. Decisions by Andrew 2026-11-04. Lane: course. Owner: real-calib (task c018, inbox items 15-16).

## Rules (Andrew, 2026-11-04)
- Lab server: storage, queue state and relay only. Allowed there: list, test, stat, `md5sum`, `mkdir`, copying files in and out (`rsync`, `cat`), small text state files written by the VM driver, and relaying commands to the cluster through the existing connection. Not allowed: any Python, tracker, midline, checker or `sweep.py` run, any `nice`d job, any process left running after a command returns. No deletes, moves or renames (unchanged)
- Compute: cluster compute nodes, through Slurm only. CPU nodes for segmentation midlines, tracking, moved copies and the checker; GPU (P100 or V100, by availability) only for the net midlines. Job arrays are fine. Login node: light commands only (`sbatch`, `squeue`, `sacct`, `sinfo`, `ls`, `md5sum`)
- Budget: $15 since 2026-10-23, unchanged; ledger check before every submit; projected total above $12: stop, Needs Andrew. CPU core-hour = 1 unit ($0.012)
- Supersedes: "Tracking runs on the lab compute server by default" and the lab-server job limits of 2026-10-11 and 2026-10-23 (`CLAUDE.md` Rules). The workstation is unchanged

## One pipe
- Today: each VM call opens a new ssh connection to the lab server (`measure/real_runner.py` `_ssh`; Windows OpenSSH has no connection sharing). The lab server reaches the cluster through one connection master that Andrew opens (`ControlPersist`)
- Target: two links, one connection each
  - VM -> lab server: one persistent ssh connection held by the driver (Python `paramiko` Transport, keepalive 30 s), every command a channel on it. On a drop: reconnect with backoff (10 s, 30 s, 60 s, then every 5 min), log each reconnect with time in the run log, at most 3 failed reconnects in a row then stop and Needs Andrew
  - Lab server -> cluster: the existing connection master only. Every cluster command and every file copy to or from the cluster runs from the lab server through it (`ssh <cluster alias> ...`, `rsync -e ssh ...` with the same ControlPath). Nothing opens a second cluster login. Before each batch step: `ssh -O check <cluster alias>` on the lab server; fails: stop, `State: waiting on Andrew`, Needs Andrew: open the cluster connection on the lab server
- Data path: frames lab server -> cluster job folder (copy through the master), outputs cluster -> lab server, md5 checked on both ends; the VM receives only small result files (checker JSON, run summaries)

## Work (real-calib)
1. `git fetch origin`; new `wip/real-calib` from `origin/main`
2. After the re-upload: check that batch 2's 50 collected roots are on the lab server with the md5 values in the driver's records (`private/fb2_state/`). Report counts. Anything missing or different: list it, Needs Andrew, do not rerun it
3. Code, with tests using a fake ssh (no real host in tests):
   - `measure/real_runner.py`: storage host and compute host are separate settings; compute host may only be the cluster; one persistent connection as above; the lab-server load and job-count checks are removed (no jobs there)
   - Checker step of the batch-2 driver and of `scripts/full_batch.py`: runs inside the per-root cluster job (CPU) after tracking; writes the check JSON next to the tracks
   - `scripts/synth/sweep.py` and any lab-server runner path refuse to start a job on the lab server (clear error)
4. Equivalence, one CPU job: run the checker on the cluster for 5 batch-2 windows already checked on the lab server; values equal (difference at most 1e-9). Record in decisions. Fails: stop, report
5. Resume batch 2 from its markers: 41 roots, about $2.9; projected total about $7.6 of $15. Status every 10 roots; free VM memory 3 GB before each staging step
6. Then the checker over every batch-2 window on the cluster; counts in `results/2026-10-25_full_batch_2/` (outcome counts and check values only)
7. Decisions, log, `State: ready to merge`

## Limits
- No deletes on the lab server. Cluster deletes only as approved before (copies a Claude session staged, after md5 check, logged in `DELETED.log`)
- No machine names, accounts or paths in tracked files
