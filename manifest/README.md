# Root manifest

`root_manifest.csv`: one row per root position in the 24 h drought and recovery movies. Reviewed by Andrew Oldag on 2026-10-08.

## How it was made
1. `scripts/manifest/scan_imgdirs.py` read the SlideBook metadata of all 192 `.imgdir` folders and grouped them by experiment and chamber code (123 positions)
2. Andrew reviewed each position in the review app (`scripts/manifest/open_review.bat`): keep, drop or unsure; condition; notes; usable window
3. `scripts/manifest/export_manifest.py` checked the answers and wrote this file

## Columns
| Column | Meaning |
| :-- | :-- |
| `id` | Experiment date (MMDD) and chamber code, e.g. `0708_c5` |
| `condition` | Confirmed by Andrew. Drought folders: `control`, `mannitol`. Recovery: `control`, `mannitol then control`, `control then control`, `mannitol then mannitol` |
| `include` | `yes`, `no` or `unsure` |
| `usable_from_h`, `usable_to_h` | Part of the movie to track, in hours from the first frame |
| `notes` | Andrew's review notes |
| `flags` | Automatic checks from the scan (missing montage, gaps, odd names) |
| `montage_imgdir` | Stitched 2400x1200 movie, relative to the experiment folder |
| `raw_imgdir` | Unstitched capture, two stage positions alternating (drought folders only) |
| `start_time`, `n_timepoints`, `duration_h`, `step_s`, `max_step_s` | From the metadata. `step_s` is the median time between frames |
| `stage_tracking_log` | Whether the folder holds the XYZ stage-tracking table |

## Known features of the data
- 27 Jul roots each have one gap of about 40 min (`max_step_s`), likely the transfer
- 21 Jul `test1.dir` holds no capture folders; only `test2.dir` exists
- `0714_m6` has no stitched montage (dropped)
