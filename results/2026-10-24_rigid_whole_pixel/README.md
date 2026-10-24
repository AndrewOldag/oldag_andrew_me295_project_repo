# Rigid invariance on a real window: whole-pixel moved copy, then the profile window (inbox item 19)

0708_m12, 4-6 h, 80 frames, 400 px tracked, net midline, stage-corrected tracker 52e9bd1, uncoupled. PROVISIONAL (current fine-tuned net). Commands: `python scripts/real_slice.py --no-agent --out results/2026-10-24_rigid_whole_pixel` (step 1) and `--out results/2026-10-24_rigid_window` (step 2, after the rule was committed). Threshold 2.0 %/h, unchanged.

## Moved copy, step 1
- Whole-pixel translation only: round((0.5, 0.3) px per 90 s x t), at most (40, 24) px at the window end; no rotation, no resampling (`scripts/remote/real_moved.py --mode whole_pixel`). Both copies cropped to the common area (40 rows, 24 columns off); the cropped reference copy is the measurement record. Copy content checked exact in a test

## Results
| Run | Moved copy | Profile range | rigid_invariance %/h | Where | closure px/h |
| :-- | :-- | :-- | --: | :-- | --: |
| 2026-10-24 first (item 18) | rotation + translation, bilinear | whole chain | 8.83 FAIL | centre, s = 435 px | 0.945 |
| Step 1 | whole-pixel translation, cropped | whole chain | 7.29 FAIL | minus flank, s 400-450 px | 0.945 |
| Step 2 | whole-pixel translation, cropped | s <= 398 px (rule, decisions 2026-10-24) | 5.76 FAIL | centre, s = 375 px | 0.945 |

## Where the difference is (step 1, window-mean profiles, max |difference| per 50 px band, %/h)
| s band (px) | 0 | 50 | 100 | 150 | 200 | 250 | 300 | 350 | 400 | 450 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| centre | 0.04 | 0.26 | 0.39 | 0.55 | 0.56 | 1.96 | 2.18 | 5.76 | 5.34 | 1.45 |
| plus flank | 0.29 | 0.18 | 0.09 | 0.36 | 0.82 | 1.03 | 1.54 | 0.78 | 0.93 | 2.16 |
| minus flank | 0.35 | 0.79 | 0.18 | 0.26 | 1.01 | 0.70 | 1.66 | 2.76 | 7.29 | 4.72 |

- Without resampling and rotation, the first 250 px from the tip agree within 1.0 %/h on all three profiles (the growth zone peak is near s = 300 px, 44 %/h). The difference grows toward the basal end of the tracked chain: 2.0-2.2 %/h at 250-350 px and 5.8 %/h at 350-400 px on the centre profile
- No frozen points in either copy; chain length 398 px in both at frame 0
- Step 2 removed only the part past 398 px; the 350-400 px band stays

## Status
- Both steps fail. Stopped for Andrew (item 19, step 3). No threshold change; synthetic rods and freeze v3 unchanged
