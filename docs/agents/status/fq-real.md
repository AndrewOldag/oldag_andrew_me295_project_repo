# fq-real
Updated: 2026-10-14 (local)
Lane: course
Branch: wip/fq-real
Last inbox item done: 6
State: ready to merge
Now: waiting for the coordinator to merge wip/fq-real; no further work until a new item
Done since last update:
- Item 6: 90 staged frames kept on the VM in staging/fq_real_labeling/ until the reference is recomputed with the real-tracking midline source. Nothing deleted
- Item 5: `real:` section in config/frame_quality_reference.yaml, provisional, from 24 clean windows (72 frames); limits recorded in config and docs/decisions.md (c8eeedd)
- measure/info.py gives the real reference for records with settings movie: real; qb_track.py --movie writes it (default synthetic). Synthetic output unchanged (c8eeedd)
- tests/test_frame_quality_reference.py: 3 passed. Full suite 172 passed, 0 skipped
- Log entry in docs/running_log_pending/fq-real.md
Needs Andrew:
- none
