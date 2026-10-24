# dispatcher
Updated: 2026-10-24 12:58 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 26
State: waiting on server job
Now: items 22-26: waiting for markers `ft2_chain.done` (lab server, task folder c010/midline: 0711_c1 ft2 net midline, the step running before item 25) and `ws_ft2_chain.done` or `.failed` (workstation, c010: 0721_m10 ft2 net midline); checked every 10 min. Then tracking of 0708_m12 and 0721_m10 on the workstation and the agent run
Done since last update:
- Item 22: runner takes `midline_weights` and `midline_tag` (ft2) from its config; tag in every net-midline, moved-copy midline, host track and cache name; VM memory wait (1.5 GB) before each host step (089a340)
- Item 22, lab server (started 11:31, before item 25): 0708_m12 4-6 h ft2 net midline done (80 frames, 2939 s, tip confidence median 0.572); 0711_c1 ft2 net midline running since 12:23. The chain's 0721_m10 step was replaced in place by a no-op (item 25), so the chain ends after 0711_c1 and writes its marker; nothing killed or deleted
- Items 25-26: one dispatcher session live (this one). Workstation chain started 12:54: ft2 weights and the 0708_m12 ft2 midline copied there; 0721_m10 montage copied (832 frames, no HistogramData); segmentation midline done (73 frames); ft2 net midline running (3 threads, nice 19). Disk after copy: 27 GB free, work folder 18 GB of 20
- Whole-pixel rigid copies reused across nets (frames do not depend on the midline; only the midline files carry the tag): no new copy for 0708_m12; test added; suite 248 passed, 1 skipped
Needs Andrew:
- 0711_c1 tracking: its full montage (5.2 GB; the tracker loader needs every frame) does not fit on the workstation next to 0721_m10 (work folder 18 GB of the 20 GB cap). Options: (a) track 0711_c1 on the lab server (single thread, about 10 s per run, 2 runs plus remedies); (b) raise the workstation cap to 26 GB (free space stays above 20 GB: now 27 GB, about 21 GB after); (c) run the slice on 0708_m12 and 0721_m10 only (no control root). Until then the 3-root agent run waits; 0708_m12 and 0721_m10 tracks are made on the workstation
