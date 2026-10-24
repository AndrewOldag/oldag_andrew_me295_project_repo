# dispatcher
Updated: 2026-10-24 03:32 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 20
State: waiting on Andrew
Now: item 21: root 2 of 3 (0711_c1) stopped partway; the VM's Claude Code killed the local run for low memory. Restart needs Andrew's go-ahead
Done since last update:
- Item 21 roots: 0711_c1 (control, 0711 drought experiment) and 0721_m10 (mannitol then control, 0721 recovery experiment); include-yes, montage, no notes or flags, stage-tracking table, not held-out; window 4-6 h as `0708_m12` t3
- 1f759e9: `scripts/real_slice.py --windows ... --config`; `RealRunner.ensure_midline` builds a missing net midline on the host (seg midline, tile-mode net2 lo 0.1, `scripts/remote/net_to_midline.py`); cached runs need no host step; own-job count no longer counts its own shell; condition in the real-movie auditor view, comparison asked in the auditor task (prompt unchanged); suite 246 passed, 1 skipped
- Lab server: tracker 52e9bd1 with net weights copied to the c010 task folder; 0708_m12 t3 midline files copied there
- 0711_c1 4-6 h on the lab server: segmentation midline done (80 frames); net midline done, 80 frames in 1876 s (19.0 s per frame, 3 threads). Not done: net_to_midline, moved copy, tracking, checks
Needs Andrew:
- Restart of the 0711_c1 run (it resumes after the net step). Claude Code stopped the local run because the VM was low on memory; its notice says not to restart without being asked
