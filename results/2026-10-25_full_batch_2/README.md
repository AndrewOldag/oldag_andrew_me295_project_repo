# Full batch, batch 2: every other include-yes root (inbox real-calib items 11-17; spec 2026-11-04)

2026-10-25 to 2026-11-05. Proposal: `docs/proposals/2026-10-25_full-batch.md`. 91 roots (all include-yes roots not in batch 1), 1063 windows by the dispatcher rule. One GPU job per root on cluster nodes: segmentation midline, ft2 net midline (GPU), tracking midline, 1000 px tracks, the w10-12 whole-pixel moved copy and its tracks, and the checker (`scripts/remote/check_window.py`; real profile: closure gates at 19 px/h; not computable counts as decline, Andrew 2026-10-26). No remedy, no agent. Outputs copied to storage with md5 checks on both ends. All check values here come from the cluster checker (Work 4 and 6: equal to the earlier checker).

Public outputs: `table.md`, `summary.json`, `windows.csv` (outcome and check values only), `cluster_checker_equivalence.json`, `audit/`. Full per-window records stay git-ignored.

## Decision by condition
| Condition | Windows | Accept | Decline | of which not computable | Failed | Not run |
| :-- | --: | --: | --: | --: | --: | --: |
| control | 369 | 328 | 28 | 3 | 13 | 0 |
| control then control | 49 | 37 | 6 | 0 | 4 | 2 |
| mannitol | 309 | 261 | 37 | 11 | 11 | 0 |
| mannitol then control | 276 | 250 | 22 | 2 | 4 | 0 |
| mannitol then mannitol | 60 | 49 | 9 | 2 | 2 | 0 |
| all | 1063 | 925 | 102 | 18 | 34 | 2 |

- Failed 34: 33 with the tracker's `arange: cannot compute length` (the error seen in calibration and batch 1); 0721_m5 w0-2 (tracker: not enough valid data points for the logistic fit; no track)
- Not run 2: 0727_cc7 (both windows). The tracker's loader rejects its stage-tracking table (155 steps for 857 stage positions); its manifest notes a gap. Its staged frames are kept on the cluster; open for Andrew
- Rigid invariance (reported, not gating): w10-12 moved copies on 85 roots. 0714_c11 and 0714_m8 have none (their copies had not been made when the lab server stopped); 0727_cc roots with fewer than 6 windows have no w10-12 window
- Flag 'base may be in growing tissue' (reported): 33 windows

## Compute
- 90 of 91 roots finished. Roots 1-50: lab-server staging relay, tracking in the cluster job, checker first on this machine (2026-10-25/26); roots 51-90: v2 driver (2026-11-04/05), checker in the cluster job; the 590 windows of roots 1-50 were checked again on the cluster (Work 6): 570 records identical to the earlier checker, 20 had no earlier record
- Per root about 22-28 min on one P100 with 4 cores; up to 2, then 4 jobs at a time (Andrew, 2026-11-04 23:10)
- Spend since 2026-10-23 after the batch: $7.24 of $15 (actual from `sacct`); per job in `audit/ledger.csv`
- Stops: lab server down 2026-10-26 to 2026-11-04 (restarted under the storage-only rules); VM memory stops 2026-10-26 and 2026-11-04 (resumed from markers, no job lost); one dropped lab-server connection 2026-11-05 (reconnected)

## Audit (inbox item 17)
- `audit/deletes.csv`: 170 cluster deletes of this batch: 90 staged root copies, 80 moved-copy frame folders (40 v2 roots), each after its outputs were md5-verified on storage
- `audit/outputs.csv`: per window, track and check-JSON md5 and the time verified on storage
- `audit/ledger.csv`: per cluster job since the batch start
- `audit/connection.csv`: connects and reconnects of the persistent connection; failed master checks (none)
- `audit/reverify.md`: a fresh md5 pass on storage: 1060 of 1060 tracks and 1063 of 1063 check JSONs match
- Not in `deletes.csv`: on 2026-10-27 another session deleted the cluster copies of batch-2 outputs ('Andrew asked in chat'), after they were on storage; they were not this batch's staging
