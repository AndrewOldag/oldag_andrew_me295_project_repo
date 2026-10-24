## 2026-10-23 (build account, session autotrace)
- Done: task c013. Landmark rule from 9 July hand traces: drafts end 35 px (74 um) behind the root apex; July traces run tip to base
- Done: net drafts for all 140 tracing-pack frames on the workstation (tile mode, fine-tuned midline net): 140 drafted, 0 with no root; net 2338 s, conversion 81 s, previews 36 s
- Done: 140 previews (28 held out, labelled and skipped), index, held-out list and worklist, review tool and apply step in the pack's `review/` folder on the lab server; tested headless on 3 frames. Counts in `results/2026-10-23_autotrace/README.md`
- Demo: `python review_traces.py . --backend MacOSX` in the review folder shows frame 1 of 112 and saves each y/n to `review.csv`
- Remaining: Andrew reviews 112 drafts (y/n), runs `apply_review.py`, hand-traces rejected and the 28 held-out frames; then fine-tune
- Bottlenecks: review and hand tracing, on Andrew
