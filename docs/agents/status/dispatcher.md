# dispatcher
Updated: 2026-10-24 13:30 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 27
State: working
Now: 3-root agent run (dispatcher agent -> tracker -> checker -> diagnostician -> auditor), started 13:29; 0708_m12 and 0721_m10 tracked on the workstation, 0711_c1 on the lab server
Done since last update:
- Lab server chain done 13:21 (`ft2_chain.done`): 0711_c1 4-6 h ft2 net midline, 80 frames, 3452 s, tip confidence median 0.176
- Workstation chain done 13:23 (`ws_ft2_chain.done`): 0721_m10 4-6 h ft2 net midline, 73 frames, 1663 s, tip confidence median 0.249. Work folder 18.0 GiB of 20 (about 18.9 after the 0721 rigid copies), 27 GB free
- Item 27: `scripts/real_slice.py --config` takes several runner configs; each window runs on the host whose config lists it (`RunnerSet`); test; suite 249 passed, 1 skipped (c0284e1)
- 0711_c1 on the lab server (single thread, nice 19, load and job checks): whole-pixel copies 12.7 s; ref and moved tracks 12.7 s and 15.4 s
Needs Andrew:
- none
