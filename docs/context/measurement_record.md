# Measurement record

One record holds one root over one window. The tracker's output is converted into it, and the checker reads it. Code: `measure/record.py`.

## Source of each field
The fields come from what Quantum Borland v1 returns from `run_two_side(..., track_centre=True)` and from its `RootRecording`:

| Record field | Shape | Tracker source |
| :-- | :-- | :-- |
| `centre` | (T, M, 2) | `TwoSideResult.centre_track`, (M, 2, T), world frame |
| `plus`, `minus` | (T, M, 2) | `left_track`, `right_track`; assigned to plus or minus by the side of frame 0 (below) |
| `stage_px` | (T, 2) | `cumulative_correction_px(recording)`: stage log in image pixels, zero at frame 0 |
| `frame_times_s` | (T,) | `recording.elapsed_s` |
| `pixel_um` | scalar | `recording.pixel_size_um` |
| `midline` | (T, K, 2) | Per-frame midline from the midline source, image coordinates plus `stage_px`. Tip first. Padded with NaN |
| `settings` | dict | Tracker arguments: disk radius, spacing, half fraction, couple, threshold, frame stride, midline source |
| NaN in a chain | | Positions frozen by the tracker's edge guard (`edge_frozen_mask`), set to NaN |

- The three chains are seeded from the same resampled frame-0 midline (`split_midline`), so index j is the same cross-section in all three
- The tracker's logistic fits (`velocity_profile`, `strain_profile`) are not used. Strain rates come from the tracked chains, as `research_background.md` asks for flank profiles
- For synthetic image-level rods the midline source is the true midline, with jitter added for the `midline_jitter` fault. The ML midline net is not run on synthetic textures

## Conventions
- Coordinates (row, col), pixels. World = image + `stage_px`
- Chains run tip to base; index 0 is the tip
- Tangent t points tip to base; angle phi = atan2(dcol, drow); curvature kappa = dphi/ds
- N = t rotated +90 degrees in (row, col), N = (-t_col, t_row). `plus` is the flank on the +N side
- For a flank at offset n, the length element is (1 - kappa n) ds. With constant flank half-spacing h, plus minus minus = -2h Dkappa/Dt (plane sections; the factor 1/(1 - kappa^2 h^2) is ignored)

## Derived fields
`derive(record)` returns, per frame pair, on the grid `s_grid` (spacing `grid_px`, default 5 px):

| Field | Unit | Definition |
| :-- | :-- | :-- |
| `v_mid` | px/s | change in arc length from the tip of each centre point, over dt |
| `regr_mid`, `regr_plus`, `regr_minus` | 1/s | log ratio of each chain segment's length in the two frames, over dt |
| `spacing` | px | distance between the plus and minus points of the same index (2h) |
| `kappa` | 1/px | curvature of the midline source at the arc length of each tracked centre point |
| `kappa_rate` | 1/(px s) | change of that curvature over the frame pair, following the tracked point (material derivative) |

- Each value sits at the mean arc length of the two frames and is interpolated onto `s_grid`. Outside the tracked range it is NaN
- Curvature smoothing `curvature_smooth_px` is a setting (default 0: none)
- Multiply strain rates by 3.6e5 for %/h

## Files
- `record.save(path)` writes one compressed `.npz`: the arrays above, the derived fields (`field_*`), the truth for synthetic rods (`truth_*`) and a JSON `meta` entry (root id, source, pixel scale, settings)
- `MeasurementRecord.load(path)` reads it back
- `from_tracker_npz(path)` builds a record from the raw arrays written by `scripts/remote/qb_track.py`
