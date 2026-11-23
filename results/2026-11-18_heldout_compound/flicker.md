# Why illumination_flicker 0.1 labels decline (inbox item 10, step 1)

Expected accept_clean (proposal section 3). All four rods label decline. Not a generator bug; nothing re-rendered.

- Base outcome against truth (`labels.md`, state `none`): REGR error 6.8-9.9 %/h (limit 1.35), flank-difference error 5.4-17.1 %/h (limit 1.00). Not good on any seed
- Checks that fail on the base run: rigid-body invariance on 4 of 4 (8.7-66.7), plane sections on 4 of 4 (17.5-51.4), tip closure on 3 of 4 (s42 passes at 0.84)
- Best single remedy, `enlarge_patch/2x`: errors 1.6-2.4 and 2.8-5.2 %/h; checks still fail. No state of one or two steps passes and is good
- Generator (`measure/render_compound.py`): one gain per rendered frame, on background and root, before blur and camera noise; geometry unchanged (`test_flicker_changes_brightness_not_geometry`). On the analysis frames of seeds 40-43 the gain spans 0.73-1.23; consecutive frames differ by 7-13 % (median) and up to 37 %. No pixel saturates (frame 0 maximum about 5,400 of 65,535). The fault is applied as the proposal defines it
- Cause: the tracker's point matcher is affine Lucas-Kanade on raw intensity. Frames are scaled by one fixed divisor, not per frame, and the match has no gain or offset term. A frame-to-frame gain change enters the residual and is fitted as displacement. The proposal's premise ("the tracker's correlation is normalised") holds for the quiescent-centre stabiliser (NCC), not for the strain-rate tracker
- Consequence for c029: the expected class was wrong, not the label. The label stays decline, by the freeze v4 truth rule. c029b uses the same generator at milder flicker sizes
