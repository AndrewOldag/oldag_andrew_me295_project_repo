## 2026-10-23 (build account, session autotrace)
- Done: task c013. Landmark rule from 9 July hand traces: drafts end 35 px (74 um) behind the root apex; July traces run tip to base
- Done: net drafts for all 140 tracing-pack frames on the workstation (tile mode, fine-tuned midline net): 140 drafted, 0 with no root; net 2338 s, conversion 81 s, previews 36 s
- Done: 140 previews (28 held out, labelled and skipped), index, held-out list and worklist, review tool and apply step in the pack's `review/` folder on the lab server; tested headless on 3 frames. Counts in `results/2026-10-23_autotrace/README.md`
- Demo: `python review_traces.py . --backend MacOSX` in the review folder shows frame 1 of 112 and saves each y/n to `review.csv`

## 2026-10-24 (build account, session autotrace)
- Done: Andrew's review checked (72 y, 40 n; 109 traced, 3 skipped; 28 held-out hand-traced)
- Done: training list of 181 compliant traces (72 July include-yes in-window + 109 pack; 43 July traces refused; no held-out frame or root), seed 20261023
- Failed: cluster P100 job with the original recipe ran out of GPU memory at the first step ($0.008); V100 job cancelled while pending (start estimate 10 days out, $0)
- Done: cluster P100 job with gradient accumulation (batch 3 x 2, Andrew's option A): net2_midline_ft2, 20 epochs, best validation loss 0.0022, 1 h 23 min, $0.234; spend today $0.691 of $5
- Done: held-out score (28 frames, 16 roots): base net2 off the root on 24; net2_midline_ft distance median 2.9 px, p90 7.4 px, end +28 px; net2_midline_ft2 distance median 2.4 px, p90 6.4 px, end +23 px; 0 no root and 0 off the root for both fine-tuned nets
- Demo: the score table in `results/2026-10-23_autotrace/README.md`
- Remaining: Andrew decides whether to adopt net2_midline_ft2 as the real-movie midline source; then the 0708_m12 slice is rerun with it
- Bottlenecks: adoption decision, on Andrew
