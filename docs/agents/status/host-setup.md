# host-setup
Updated: 2026-10-23 15:24 (local)
Lane: course
Branch: wip/host-setup
Last inbox item done: 1
State: waiting on Andrew
Now: item 2 done except the real-window test (spec item 4); item 3 waits on it
Done since last update:
- Spec item 1: key login to the workstation works (BatchMode); ssh config entry added; private file copied
- Spec item 2: survey in the private file. Counts: 14 cores, 20 threads, 62 GB RAM, 0 usable GPUs, 46 GB free disk, imaging drive not mounted, load 0.00, no other user's jobs. Tracker code and env were absent. Upload key to the lab server: not tested (see Needs Andrew)
- Spec item 3: tracker env built from `envs/qb.yml` in the work folder (micromamba, nice 19). Tracker code as git archives made on the VM: master d5f1829 (installed; = lab-server checkout), gate2-windowed-coupling 52e9bd1, stage-auxdata 888f972. No git run on the lab server
- Spec item 4, synthetic: pass. Rod v3_growth_zone_clean_s10, st1. Render byte-identical (44 files); tracks max |d| 2.3e-13 px (limit 1e-6). Tracking loop 4.4 s vs 6.2 s on the lab server
- Spec item 4, real window: not run (see Needs Andrew). Code ready: 52e9bd1 tracker files equal those of the lab-server reference run
- Spec item 5: `host:` field on the board, set on every open course task; tests 10 passed; full suite 205 passed (commit on this branch)
- Spec item 7: decisions entries, pending log entry, `results/2026-10-23_host_setup/README.md`
Needs Andrew:
- Real-window test needs the 0708_m12 t3 frames (about 80 frames, 0.46 GB) on the workstation. My permission check refused both routes: (1) running the workstation's upload key to the lab server, (2) streaming lab-server files through the VM to the workstation. Allow one of them (a permission rule, or run the copy yourself), then `check github`
- Workstation free disk is 46 GB, below the 100 GB work-folder cap. Keep the cap, or set a lower one?
- Upload key (results back to the lab server) is untested for the same reason as (1); the spec's rsync of results needs it
- Research task files (r00x) have no `host:` line; I did not edit other sessions' files outside the repo
