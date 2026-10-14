# fq-real
Updated: 2026-10-13 22:10 (local)
Lane: course
Branch: wip/fq-real
Last inbox item done: 1
State: waiting on Andrew
Now: labeling set ready; B4 starts when an inbox item says the labels are done
Done since last update:
- B1: 30 windows (20 clean candidates, 10 likely poor), ids fq01-fq30 shuffled, list in private/
- B2: 90 frames copied read-only from the lab server; view/, labels.csv, HOW_TO_LABEL.txt written; 530 MB
- B3: frame_quality for all 90 frames, in private/, hidden from the labeling set
- Log entry in docs/running_log_pending/fq-real.md
Needs Andrew:
- Label 30 windows: folder staging/fq_real_labeling/ in the main repo folder; look at view/<id>.png, write clean, not_clean or unsure in labels.csv (instructions in HOW_TO_LABEL.txt)
- Band for real frames: no real-movie midline source exists yet, so values use a band from a simple dark-root segmentation. Accept it for the real reference, or wait for the midline source that real tracking will use (the reference should use the same band)
- All 90 real frames are below the synthetic lowest on both measures. B4 says stop if any clean window falls below the synthetic lowest, so B4 will stop as written. Decide: drop that check for the real reference (real and synthetic references are separate), or keep it and stop
