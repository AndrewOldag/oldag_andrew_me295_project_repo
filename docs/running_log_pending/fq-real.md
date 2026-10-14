## 2026-10-13 (build account, session fq-real)
- Done: Task B1-B3 of spec 2026-10-13 (real-movie frame-quality labeling set), branch wip/fq-real
- B1: 30 windows of 1 h, ids fq01-fq30 in shuffled order: 20 control roots with include yes inside usable hours, 10 likely poor (notes on lighting, focus, dark region, banding, artifacts). Experiments 0708/0711/0714/0721/0727: 6/5/8/7/4 windows. Start hours 1.7-21.7 h. List in the git-ignored private folder
- B1 deviation: 0727 has 2 control roots with include yes and no image-problem note, so it gives 2 clean-candidate windows; 0714 and 0721 give 5 each instead of 4
- B2: 90 frames (start, middle, end of each hour) from the montage image folders, read-only on the lab server: sftp at nice 19, ionice idle, 40 Mbit/s cap, load checked before each window (1 min load 0.3-0.7 of 32 cores), no other transfer running. Nothing written, moved or deleted on the server
- B2: frame step inside the windows 90-114 s; no window crosses an acquisition gap
- B2: set in staging/fq_real_labeling/ (git-ignored): frames/ (90 .npy, 12-bit, 1200 x 2280 px), view/ (30 PNG, 3 frames stacked, 12-bit range mapped to 8-bit, no auto-levels, downscaled 3x), labels.csv (30 rows, label empty), HOW_TO_LABEL.txt. 530 MB on disk (cap 5 GB)
- B3: frame_quality (texture_contrast, focus) for all 90 frames with measure.preprocess.frame_quality, band radius 45 px as in qb_track.py. Values in the private folder, not in view/ or labels.csv
- B3: no midline source exists yet for real movies, so the band follows a medial ridge of a dark-root segmentation (Gaussian 4 px, below 0.85 x smoothed background, largest component). Overlays checked by eye: the band covers the root in all 30 windows; 2-3 windows pick up small dark blobs at the image edge
- B3: all 90 real frames are below the synthetic lowest on both measures (synthetic lowest 0.155 and 0.073). Under B4 as written, any window Andrew labels clean will hit the stop condition "clean window below the synthetic lowest"
- Demo: open staging/fq_real_labeling/view/fq01.png; labels go in staging/fq_real_labeling/labels.csv
- Remaining: Andrew labels the 30 windows; then B4 (reference, separation, real: section in config/frame_quality_reference.yaml, measure/info.py picks real or synthetic reference, tests)
- Bottlenecks: labels (Andrew); midline source for the real band and the B4 synthetic-lowest stop rule (Andrew, see status)

## 2026-10-13 (build account, session fq-real, inbox items 2-4)
- Done: checked all 30 windows against the usable-window rule (CLAUDE.md, 2026-10-13). 7 broke it, all with include not yes (unsure or no); none were outside usable hours
- Replaced fq03, fq10, fq19, fq23, fq25, fq27, fq28 with fq31-fq37: likely-poor windows from include-yes roots inside usable hours, picked from manifest notes (weird lighting, second root entering, chamber edge in the image). 21 frames pulled read-only as before; frame step 96-111 s, no acquisition gap
- Replaced windows removed from staging/fq_real_labeling/ on the VM (frames/, view/) and from labels.csv. No labels had been written
- Fixed: labels.csv had held only fq01-fq04 since the first build (written while the pull was still running, then not rewritten). Now 30 rows, labels empty
- Set now: 30 windows, 90 frames, 530 MB. Experiments 0708/0711/0714/0721/0727: 4/4/5/8/9. 20 clean candidates, 10 likely poor. The likely-poor windows now come mostly from 0721 and 0727, where the include-yes roots with image-problem notes are
- Band: the dark border of some frames joined edge blobs to the root mask (band off the root in 4 windows). A 5 px border is now cleared before the largest component is taken. Values recomputed for all 90 frames; all 30 overlays checked by eye
- Band after the fix: on the root in 29 windows; in 1 window it runs past the tip and widens in a dark patch. In 2 windows the basal root under a bubble is not covered (band stays on the root)
- Planning decisions taken in: segmentation band used now, real reference marked provisional in config at B4; B4 stop rule "clean window below the synthetic lowest" dropped, clean vs not_clean separation check kept
- Demo: open staging/fq_real_labeling/view/fq31.png; labels go in staging/fq_real_labeling/labels.csv (30 rows)
- Remaining: Andrew labels the 30 windows; then B4
- Bottlenecks: labels (Andrew)
