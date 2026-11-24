# Real reference set and thresholds for the particle-path zone check (task c035, report-only)

Spec `docs/specs/2026-11-23_zone-check-real-reference.md`; proposal `docs/proposals/2026-11-23_zone-reference.md`; inbox real-calib 33-34.

Status: in progress. Steps 6 and the detection curve are not run yet.

## Detection curve plan (inbox 34), committed before the run
- Windows: the 130 reference windows Andrew labelled `clean` (`reference.csv`), base track (`st1`) from the c027 track cache, read-only
- Thresholds: `config/zone_reference_thresholds.yaml` (`pp_shape_rel` 0.14, `pp_common_rel` 0.5, approved 2026-11-23 23:20). The curve does not change them
- Shape check: the window-mean velocity profile shifted along s by -90, -60, -30, -15, +15, +30, +60, +90 px (`shifted_fields`, as in c034); tracked points unchanged. Scored by `pp_shape_rel`
- Common check: every tracked point slid along s by 0.5, 1, 2, 4 patch spacings (15 px each: 7.5, 15, 30, 60 px), both directions, growing linearly from 0 at the first frame to the full size at the last (`particle_path(slide_px=...)`, an anchoring drift); profile unchanged. Scored by `pp_common_rel`
- False alarms: both checks on the unshifted windows
- Reported: caught of computable per size and direction; smallest size caught in at least 90 % of computable windows in both directions. Counts only
- Code: `python scripts/zone_reference.py curve --cache <c027 track cache>` -> `curve.md`
