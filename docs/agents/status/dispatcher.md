# dispatcher
Updated: 2026-10-24 11:37 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 21
State: working
Now: item 22: ft2 net midlines for 0708_m12, 0711_c1, 0721_m10 (4-6 h) building on the lab server as one detached chain; then the 3-root agent run
Done since last update:
- Item 22 started: runner reads `midline_weights` and `midline_tag` from its config; the tag (`ft2`) goes into every net-midline, moved-copy, host track and cache name, so nothing made with the old net is overwritten; the runner waits before each host step while VM memory is below 1.5 GB; 2 tests; suite 248 passed, 1 skipped
- Lab server: ft2 midline chain started 11:31 (one step at a time, nice 19, 3 threads, load and job-count check before each step). 0708_m12 segmentation midline done (80 frames, 34 s); its ft2 net midline running. No VM process holds the build
Needs Andrew:
- none
