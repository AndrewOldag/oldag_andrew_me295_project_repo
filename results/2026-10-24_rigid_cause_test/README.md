# Rigid invariance on a real window: cause test (dispatcher inbox item 20, step A)

`python scripts/rigid_cause_test.py` on the cached tracks of 0708_m12, 4-6 h (net midline, provisional; 400 px tracked; uncoupled). Output `step_a.json`. Controls made on the compute host with `scripts/remote/real_moved.py --shift-scale 0` (zero shift) and `--pad` (no crop). Threshold 2.0 %/h.

| Pair | rigid_invariance %/h | Where |
| :-- | --: | :-- |
| Zero-shift control (reference vs identical copy) | 0.000 | - |
| Whole-pixel shift, cropped to the common area | 7.286 | minus flank, s = 420 px |
| Whole-pixel shift, not cropped (padded with background) vs the window as is | 7.286 | minus flank, s = 420 px |

- Basal points (mean s > 250 px; 12 of 27 per chain): smallest distance to a frame edge 520-575 px in both copies and all three chains; margin (largest shift 40 px + disk radius 14 px) 54 px; point-frames within the margin: 0
- Edge-frozen basal points: 0 in both copies
- Valid frame pairs per s, identical in both copies: 79 of 79 at s = 100-375 px; 74 at 400, 62 at 425, 52 at 450, 41 at 475 px
- Reading: the excess is at well-covered points far from any edge; cropping does not cause it. Step B, second branch: rigid invariance on real windows is reported, not gating (decisions 2026-10-24, planning account under Andrew's delegation)
