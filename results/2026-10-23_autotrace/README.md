# Net-drafted midline traces for the tracing pack (task c013)

Counts and run times only. Frames, drafts and previews stay on the lab server, in the pack's `review/` folder.

## Landmark rule (inbox item 2)
- 10 hand-traced July frames from include-yes roots; 1 excluded (root mask merged with a bubble at the tip)
- July traces run tip to base (all 115)
- Offset from the trace's tip end to the root-mask apex: median 35.3 px (74 um at 2.105 um/px), range 23.4-63.5 px, n = 9
- Rule: every draft ends on its midline 35 px behind the apex

## Drafts (inbox item 3)
- Net: tile mode, fine-tuned midline weights, contrast percentiles 0.1 and 99.5, CPU, nice 19, 10 threads
- 140 frames in 84 folders: 2338 s for the net (16.7 s per frame), 81 s for the conversion, 36 s for the previews
- Drafts: 140 of 140. Net found no root: 0
- Component choice: nearest the net tip in 107 frames, largest in 33
- Apex: net tip in 104 frames, root mask in 36. Net tip vs mask apex where both exist: median 5.0 px, 90th percentile 9.0 px (n = 104)
- End adjustment against the net midline end: median -10.1 px, 10th to 90th percentile -15.9 to +3.9 px
- Flags: skeleton end curled back and trimmed 5; mask apex far ahead of the net midline 2
- Points per draft: 8-14, base to tip, original pixel coordinates

## Review set (inbox items 4-6, 9)
- 140 previews; 28 held-out frames (16 roots) labelled `HELDOUT_TRACE-BY-HAND`, red border, skipped by the review tool
- 112 frames for y/n
- Review tool and apply step tested headless on 3 frames plus 1 held-out frame: resume, last decision wins, held-out frames skipped and listed, hand traces kept on re-apply, both output files open in the tracing tool. The macOS backend was not tested
