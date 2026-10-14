# fq-real
Updated: 2026-10-13 (local)
Lane: course
Branch: wip/fq-real
Last inbox item done: 5
State: ready to merge
Now: B4 done; real frame_quality reference written, provisional
Done since last update:
- Item 5: `real:` section in config/frame_quality_reference.yaml, provisional, from 24 clean windows (72 frames); limits recorded in config and docs/decisions.md (c8eeedd)
- measure/info.py gives the real reference for records with settings movie: real; qb_track.py --movie writes it (default synthetic). Synthetic output unchanged (c8eeedd)
- tests/test_frame_quality_reference.py: 3 passed. Full suite 172 passed, 0 skipped
- Log entry in docs/running_log_pending/fq-real.md
Needs Andrew:
- 90 staged frames (530 MB) in staging/fq_real_labeling/ on the VM: delete now per the staging rule, or keep until the reference is recomputed with the real-tracking midline source
