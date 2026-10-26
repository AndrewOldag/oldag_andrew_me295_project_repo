# First full batch of real windows (inbox real-calib items 7-11)

2026-10-25. Proposal: `docs/proposals/2026-10-25_full-batch.md` (committed before any batch value). 11 roots, one per experiment and condition (all 5 trials, all 11 groups); every dispatcher window of each: 126 windows. ft2 midline (`net2_midline_ft2.pt`, tile mode, low 0.1 %, high 99.5 %), 1000 px tracks, every frame, uncoupled, initial settings. Checker with the real profile: closure gates at 19 px/h (decisions 2026-10-24); rigid invariance and plane sections reported. No screen, no remedy, no agent.

Commands: `python scripts/full_batch.py run --config private/real_runner_fb1.yaml` (lab server, single thread, nice 19, host checks before every run; retried every 10 min while the host was busy), then `python scripts/full_batch.py summary`. Per-window files in `windows/`, `summary.json`, `table.md`, `runner_log.json`.

## Closure outcome by condition
| Condition | Windows | Pass | Fail | Not computable | Failed | Not run |
| :-- | --: | --: | --: | --: | --: | --: |
| control | 48 | 40 | 5 | 2 | 1 | 0 |
| control then control | 6 | 5 | 0 | 0 | 1 | 0 |
| mannitol | 36 | 30 | 5 | 0 | 1 | 0 |
| mannitol then control | 24 | 22 | 0 | 2 | 0 | 0 |
| mannitol then mannitol | 12 | 12 | 0 | 0 | 0 | 0 |
| all | 126 | 109 | 10 | 4 | 3 | 0 |

- Measured 123 of 126. Failed 3 in the measurement, all `ValueError: arange: cannot compute length` (0711_m1 w0-2, 0721_c2 w6-8, 0727_cc1 w0-2); the error seen on 0714_c11 in the calibration; cause not traced; not retried (proposal)
- Not computable 4: closure value not finite
- Flag 'base may be in growing tissue' (frame-0 midline shorter than 1000 px; reported, not a gate): 5 windows (0708_m1 w0-2, 0711_c3 w0-2, 0714_c5 w2-4, w4-6, w6-8)
- Rigid invariance (reported, not gating), w10-12 of each root, 11 moved copies: 3.8-184.5 %/h, median 15.0

## Compute
- Segmentation midlines and frame lists, lab server: 126 of 126, 15:03-16:08 (25-46 s each)
- ft2 GPU midlines, cluster: 4 jobs (P100), 126 of 126 windows, 64-79 s per window; 2 h 20 min GPU time; $0.391 actual; added worst case $1.344 (cap for the night $3). Spend since 2026-10-23 after the batch: $1.417 of $15
- Cluster staging, 2 fills of 75 and 51 windows; folder peak 28.7 GB (stop at 35 GB). Every output file md5-checked on the lab server before its window frames were cleared on the cluster (126 clears, each logged in the cluster folder's `DELETED.log`, inbox item 8). Folder after the batch 2.3 GB
- Tracking, lab server: 137 tracks (126 windows and 11 moved copies), 1.14 h of tracker time (13.8-40.7 s each), 11 moved copies (80.8 s in total); wall time 17:33-19:30, mostly waiting while another session's sweep held the job slots
- Lab server storage of the batch folder: 9.5 GB before tracking (moved copies on 11 windows only, inbox item 9)

## Cluster CPU tracking (inbox item 11)
- Equivalence: 0708_c2 w0-2 tracked on the cluster CPU agrees with the lab server to 2.6e-7 px; checker values equal (`cluster_equivalence.json`; decisions 2026-10-25)
- The first batch was tracked on the lab server: item 11 arrived after its window frames were cleared on the cluster
