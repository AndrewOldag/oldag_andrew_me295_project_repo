# real-calib
Updated: 2026-11-04 18:25 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 17
State: working
Now: spec 2026-11-04 Work 5: batch 2 resumed with the v2 driver (one persistent connection, cluster relay only, checker and w10-12 moved copy inside each root's cluster job, audit records for item 17); first v2 job submitted 18:20
Done since last update:
- Work 1: branch rebuilt on `origin/main` with the old tip merged into it; fast-forward push, no force
- Work 2: the 50 collected roots are on the lab server, every file equal to its recorded md5 (590 windows, 589 tracks; the one missing track is the known 0721_m5 w0-2 tracker error). The cluster copies of these outputs were deleted on 2026-10-27 by another session ('Andrew asked in chat' in `DELETED.log`); the lab-server copies are the only ones
- Work 3: `measure/remote_link.py` (one persistent connection, reconnect backoff, relay through the master), `measure/cluster_compute.py` (Slurm jobs, ledger check before each submit), `RealRunner` `compute: cluster` (storage and compute hosts separate; lab-server load and job-count checks gone), `measure/hosts.py` refuses any compute or Python on a storage-only host (RealRunner, RemoteRunner incl. sweeps), `scripts/remote/check_window.py` (checker inside the cluster job); fake-ssh tests; 376 passed, 2 skipped
- Work 4: cluster checker equal to the local checker on 5 windows (every difference 0.0); decisions
- Item 17: moved copies deleted on the cluster right after the md5 check of their tracks on the lab server (done per root by the batch driver as soon as the job's outputs are verified; logged in `DELETED.log`); audit records collected for `results/2026-10-25_full_batch_2/audit/`
- Spend since 2026-10-23: $4.57 of $15 before the first v2 job
Needs Andrew:
- Free VM memory is about 2.5 GB of 7.75 GB; the spec needs 3 GB before each staging step, so staging of new roots waits (the 3 staged roots run). Closing idle sessions on the VM would let it go on
