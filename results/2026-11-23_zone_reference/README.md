# Real reference set and thresholds for the particle-path zone check (task c035, report-only)

Spec `docs/specs/2026-11-23_zone-check-real-reference.md`; proposal `docs/proposals/2026-11-23_zone-reference.md`; inbox real-calib 33-34.

## Files
- `synthetic.md`, `synthetic.csv`: step 1, residual split on the c034 freeze v4 set; shape flags 15 of 15 at every synthetic shift with the synthetic threshold (stop rule met)
- `sample.csv`: 150 accepted c027 windows (24 by seed 20261123, 126 by seed 20261124)
- `reference.csv`, `thresholds.md`: Andrew's labels (130 clean, 20 not clean), relative residuals, thresholds by the pre-committed rule
- `real_counts.md`: step 6, both thresholds on every c027 window, report-only
- `curve.md`: detection curve on the 130 clean windows (inbox 34)

## Thresholds (approved by Andrew 2026-11-23 23:20)
- `config/zone_reference_thresholds.yaml`: `pp_shape_rel` 0.14 (shape: profile misplaced along s), `pp_common_rel` 0.5 (common mode: anchoring drift). Both relative to the RMS tracked displacement
- Rule: 99.5th percentile over the 130 clean windows x 1.5, rounded up to 2 significant figures
- Reference set: shape over 0 of 130 clean, 1 of 20 not clean; common over 1 of 130 clean, 0 of 20 not clean

## Step 6: all c027 windows (`real_counts.md`), report-only
- 1,189 windows, 1,191 tracks (base, plus the accepted track of the 2 `accepted after repair` windows). Not computed: 3 (track not cached: 0721_m5__w0-2, 0727_cc7__w0-2, 0727_cc7__w2-4). Relative values n/a: 59 (58 `declined by rule`, 1 `declined by agent`)
- Accepted base tracks (1,034): shape flags 3, common flags 5, either 8
- Declined by agent (85): shape 1, common 10, either 11
- Accepted after repair (2, base and accepted track): none flagged
- No c027 outcome, threshold or scored result changes

## Detection curve plan (inbox 34), committed before the run (1a023ff)
- Windows: the 130 reference windows Andrew labelled `clean` (`reference.csv`), base track (`st1`) from the c027 track cache, read-only
- Thresholds: `config/zone_reference_thresholds.yaml`. The curve does not change them
- Shape check: the window-mean velocity profile shifted along s by -90, -60, -30, -15, +15, +30, +60, +90 px (`shifted_fields`, as in c034); tracked points unchanged. Scored by `pp_shape_rel`
- Common check: every tracked point slid along s by 0.5, 1, 2, 4 patch spacings (15 px each: 7.5, 15, 30, 60 px), both directions, growing linearly from 0 at the first frame to the full size at the last (`particle_path(slide_px=...)`, an anchoring drift); profile unchanged. Scored by `pp_common_rel`
- False alarms: both checks on the unshifted windows
- Reported: caught of computable per size and direction; smallest size caught in at least 90 % of computable windows in both directions. Counts only
- Code: `python scripts/zone_reference.py curve --cache <c027 track cache>` -> `curve.md`

## Detection curve result (`curve.md`)
- False alarms: shape 0 of 130, common 1 of 130
- Shape, profile shift: 15 and 30 px 2 of 130 each direction; 60 px 10 of 130; 90 px 101 of 130 (0.78) each direction
- Common, slide toward the tip (negative): 0.5 and 1 patch 2 and 4 of 130; 2 patches 18 of 130; 4 patches 90 of 130 (0.69)
- Common, slide away from the tip (positive): 0.5 to 2 patches 2 of 130; 4 patches 11 of 130
- Smallest size caught in at least 90 % of windows in both directions: none within the tested range, for either check
- Why the slide is one-sided: `pp_common_rel` divides by the RMS tracked displacement, and the tracked displacement points away from the tip in all 130 windows. A slide away from the tip adds to the denominator; with RMS displacement over 60 px in 122 of 130 windows, a 60 px slide away from the tip stays under 0.5 in most windows
- Reading: at the approved thresholds, both checks catch only gross faults on real windows (shape: about 90 px; common: about 4 patch spacings toward the tip). Smaller misplacements pass. The synthetic set caught 60 px shifts 15 of 15 at 0.14; the real windows have larger tracked displacement, so the same shift is a smaller relative residual

## Limits
- Report-only: neither check gates any outcome; gating is future work
- The fault models are an arc-length offset of the profile and a uniform slide of the tracked chain. They do not cover a zone misplaced by a tracker error of another kind
- Labels are one person's visual judgement on three frames per window
- Per-window values of all c027 windows stay on the VM (git-ignored); only counts, example ids and the reference windows' relative residuals are committed
