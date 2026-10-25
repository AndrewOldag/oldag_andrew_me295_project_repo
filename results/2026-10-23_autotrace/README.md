# Net-drafted midline traces for the tracing pack (task c013)

Counts and run times only. Frames, drafts, previews and weights stay on the lab server and the cluster.

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

## Andrew's review (inbox item 12)
- 112 frames reviewed: 72 accepted, 40 rejected; 109 traced (rejected ones by hand, 10 accepted drafts edited), 3 skipped
- 28 held-out frames hand-traced

## Fine-tune net2_midline_ft2 (inbox items 12-13)
- Training list: 181 traces = 72 July (include-yes roots, inside usable windows) + 109 pack; 43 July traces refused (roots c1, c7 not included; c3, c12 unsure). No held-out frame or root. Seed 20261023. From base net2
- Recipe: the original fine-tune defaults (20 epochs, batch 6, lr 1e-4, background windows 0.3 per positive, validation 0.1, weighted MSE alpha 10, contrast 1.0-99.5, net1 frozen) with one change (Andrew, 2026-10-24): each batch of 6 runs as 2 micro-batches of 3 with gradient accumulation and one optimizer step per batch. Same batches, loss and step count; batch norm sees 3 windows per pass instead of 6
- Windows: 1290 training, 143 validation. Validation loss 0.0095 after epoch 1, best 0.0022 at epoch 20
- Cluster job 1 (P100, 16 GB, original recipe): CUDA out of memory at the first training step. 2 min 41 s, $0.008. No weights written
- Cluster job 2 (V100): estimated start 10 days later; cancelled while pending, $0
- Cluster job 3 (P100, gradient accumulation): finished, 1 h 23 min, $0.234
- Cluster spend today: $0.691 of the $5 cap

## Held-out score, 28 frames (16 roots)
- Valley maps: tile mode, contrast 0.1-99.5, CPU; same conversion for each net (valley map to midline, no end rule)
- Distances use net midline points inside the hand trace's extent (`used_med` = their fraction); `off_root` = frames where under half the hand trace lies within 10 px of the net midline; end error is along the hand trace's tip tangent, + = net runs past the hand end
- base net2: 1 frame no root, 24 of 28 off the root (coverage 0). Its distance values rest on few points and do not describe a midline on the root
- net2_midline_ft (July fine-tune, 115 traces, 43 of them from roots now excluded): 0 no root, 0 off the root; distance median 2.9 px (6.1 um), 90th percentile 7.4 px (15.6 um); net end median 28.0 px past the hand end
- net2_midline_ft2 (this fine-tune, compliant traces only): 0 no root, 0 off the root; distance median 2.4 px (5.1 um), 90th percentile 6.4 px (13.5 um); net end median 23.2 px (49 um) past the hand end, 90th percentile of the absolute error 29.9 px
- End-point offset: hand traces end about 35 px behind the root apex (landmark rule), so ft2 ends a median of about 12 px behind the apex, ft about 7 px

| net | set | frames | no_root | off_root | coverage_med | used_med | dist_med_px | dist_p90_px | dist_med_um | dist_p90_um | end_med_px | end_abs_med_px | end_abs_p90_px | end_abs_med_um |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| base | all | 28 | 1 | 24 | 0.0 | 0.0 | 5.5 | 510.8 | 11.6 | 1075.2 | 904.1 | 904.1 | 1102.7 | 1903.1 |
| base | 0711 | 7 | 1 | 6 | 0.0 | 0.0 | 595.4 | 695.1 | 1253.3 | 1463.2 | 930.2 | 930.2 | 1083.2 | 1958.1 |
| base | 0714 | 8 | 0 | 8 | 0.0 | 0.0 | 112.9 | 300.7 | 237.7 | 633.0 | 1036.5 | 1036.5 | 1116.9 | 2181.8 |
| base | 0721 | 7 | 0 | 6 | 0.0 | 0.41 | 3.9 | 496.2 | 8.2 | 1044.5 | -46.1 | 434.0 | 966.4 | 913.6 |
| base | 0727 | 6 | 0 | 4 | 0.0 | 0.0 | 1.9 | 7.3 | 4.0 | 15.4 | 900.9 | 900.9 | 1061.2 | 1896.4 |
| ft | all | 28 | 0 | 0 | 1.0 | 0.95 | 2.9 | 7.4 | 6.1 | 15.6 | 28.0 | 28.0 | 39.5 | 58.9 |
| ft | 0711 | 7 | 0 | 0 | 1.0 | 0.95 | 3.0 | 7.5 | 6.3 | 15.8 | 30.8 | 30.8 | 42.0 | 64.8 |
| ft | 0714 | 8 | 0 | 0 | 0.999 | 0.95 | 3.1 | 8.8 | 6.5 | 18.5 | 28.3 | 28.3 | 33.1 | 59.6 |
| ft | 0721 | 7 | 0 | 0 | 1.0 | 0.95 | 2.9 | 6.8 | 6.1 | 14.3 | 21.9 | 21.9 | 38.9 | 46.1 |
| ft | 0727 | 6 | 0 | 0 | 1.0 | 0.94 | 2.6 | 6.5 | 5.5 | 13.7 | 27.5 | 27.5 | 33.3 | 57.9 |
| ft2 | all | 28 | 0 | 0 | 1.0 | 0.95 | 2.4 | 6.4 | 5.1 | 13.5 | 23.2 | 23.2 | 29.9 | 48.8 |
| ft2 | 0711 | 7 | 0 | 0 | 1.0 | 0.95 | 2.2 | 6.3 | 4.6 | 13.3 | 27.6 | 27.6 | 34.1 | 58.1 |
| ft2 | 0714 | 8 | 0 | 0 | 1.0 | 0.96 | 2.6 | 7.5 | 5.5 | 15.8 | 21.1 | 21.1 | 26.4 | 44.4 |
| ft2 | 0721 | 7 | 0 | 0 | 1.0 | 0.96 | 2.5 | 6.0 | 5.3 | 12.6 | 20.5 | 20.5 | 26.3 | 43.2 |
| ft2 | 0727 | 6 | 0 | 0 | 1.0 | 0.94 | 2.3 | 4.7 | 4.8 | 9.9 | 22.1 | 22.1 | 27.4 | 46.5 |
