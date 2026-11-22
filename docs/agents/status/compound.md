# compound
Updated: 2026-11-21 10:50 (local)
Lane: course
Branch: wip/rod-jobs
Last inbox item done: 6
State: ready to merge
Now: branch wip/rod-jobs (inbox item 6): the synthetic-rod job kind only, for real-calib R5. c029 continues on wip/compound
Done since last update:
- `scripts/rod_jobs.py`: rendered rods VM -> storage (tar, md5 per file, `<rid>.ok`) -> cluster (rsync, file count); one Slurm array task per rendered rod running all its tracker runs (1 core, 1 h, finished outputs skipped, partial outputs reported, never deleted); fetch to storage with md5 on both ends, to the VM only on md5 match; down link or master: `connection down`, no state change. Built on retrack_queue.py (Remote, array script, ledger)
- `tests/test_rod_jobs.py`: 8 fake-cluster tests; with tests/test_retrack_queue.py 21 passed
- In use for c029 on wip/compound: 2-rod cluster vs VM equivalence 3.5e-7 and 1.5e-12 px (limit 1e-6); 329 of 852 label runs fetched
Needs Andrew:
- none on this branch
