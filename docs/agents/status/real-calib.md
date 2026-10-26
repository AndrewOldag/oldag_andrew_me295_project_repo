# real-calib
Updated: 2026-10-25 19:25 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 10
State: working
Now: item 11 (2): cluster CPU tracking equivalence test on 0708_c2 w0-2 (staging the root, then one 1-core job); first batch tracking finishes on the lab server meanwhile
Done since last update:
- Item 11 read. It arrived after all 126 first-batch midlines were verified and their frames cleared, so the first batch is tracked on the lab server (fallback, item 11 (4)); 85+ of 126 done
- Finding: the tracker loader lists every frame file of the imgdir and sets its normalization from a sample over the whole movie, so window-only copies cannot give identical tracks. Cluster tracking stages the whole root imgdir (5.3 GB, the same as its 12 windows)
Needs Andrew:
- none
