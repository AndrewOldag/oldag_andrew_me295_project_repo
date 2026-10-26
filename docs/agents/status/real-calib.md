# real-calib
Updated: 2026-10-25 19:50 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 10
State: working
Now: item 11: full-root cluster job on 0708_c2 (segmentation, GPU midline, tracking midline, tracks for its 12 windows) as an all-step equivalence test against the first batch; then the rest of the full batch root by root
Done since last update:
- First batch done (item 7 (3)): 126 windows, 123 measured; closure pass 109, fail 10, not computable 4; 3 failed (`arange` error). `results/2026-10-25_full_batch_1/README.md`
- Item 11 (2): cluster CPU tracking equal to the lab server (2.6e-7 px; checker values equal); decisions 2026-10-25
- Cluster tracking stages the whole root imgdir: the tracker loader reads every frame file and normalizes from a whole-movie sample (decisions)
- Cost estimate for the rest of the full batch (item 11 (5)), from measured jobs: GPU midlines $0.0031 per window; tracking 97 s per window on one core. One GPU job per root (all steps, 4 cores + 1 GPU), about $0.065 per root. 91 roots left (1063 windows): about $5.9; projected total since 2026-10-23 about $7.6, under $12. Continuing
Needs Andrew:
- none
