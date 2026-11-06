# Batch 2 audit files

Inbox items 17 and 18 (Argon audit `docs/reviews/2026-11-05_argon-batch2/review.md`, A5-F1 to F4). Built by a private
script from the cluster `DELETED.log`, the `md5.txt` beside each root's outputs on the lab server, the driver records,
the spend ledger and `sacct`. No track or check was rerun. All times carry their offset (Pacific).

| File | Rows | Content |
| :-- | --: | :-- |
| `deletes.csv` | 170 | one row per cluster delete: 90 staged roots, 80 moved-copy frame folders |
| `outputs.csv` | 1143 | 1063 window tracks (`kind` track), 40 `moved_copy_ref`, 40 `moved_copy_moved` |
| `ledger.csv` | 98 | every cluster job from the batch-1 tail (job 5466204) to the end of batch 2 |
| `connection.csv` | 7 | persistent-connection events and driver connection errors |
| `reverify.md` | - | fresh md5 pass over every output on the lab server, against `outputs.csv` |

## A5-F2: did each delete follow its md5 check?

Yes. All 170 deletes ran after a lab-server md5 check of the outputs they were checked against. No delete ran before
its check. In both drivers one `collect()` call does, in this order: copy the root's outputs to the lab server; md5 of
every file on both ends; compare; on a mismatch stop with `error` and delete nothing; write `md5.txt` on the lab server;
then the `rm`s.

- Driver v2 (2026-11-04 to 05, 120 rows; committed as `scripts/full_batch_2_driver.py`, same logic):
  - md5 on both ends `scripts/full_batch_2_driver.py:180-181`; compare and stop on mismatch `:182-185`
  - `md5.txt` written `:186`; check time taken `:187`
  - deletes only after that: moved copies `:213`, staged root `:218`; the `rm` itself `:165`
- Driver v1 (2026-10-25 to 26, 50 rows; private, not committed; superseded by v2): same order in its `collect()`:
  md5 on both ends, compare, return on mismatch, write `md5.txt`, then one `if [ -d <staged root> ]; then ... rm -r ...`

Why the old `outputs_verified` was later than `deleted`: the old builder took it from the driver's "collected" log
line, written after the deletes. It now records the time of the pre-delete check (`verified_from` names the source):

| Rows | Driver | `verified_from` | Source of the check time | Check before delete |
| :-- | :-- | :-- | :-- | :-- |
| 50 staged roots | v1 | `md5.txt mtime` | mtime of `md5.txt` on the lab server (written after the compare, before the `rm`) | 10-17 s |
| 38 staged roots, 75 moved copies | v2 | `delete record` | check time stored with the delete by the driver | 4-26 s |
| 7 (0721_c6 x3, 0721_m6 x3, 0721_c8 first moved copy) | v2 | `collection record` | per-collection output record of the same `collect()` call | 4-10 s |

- The 7 rows: 0721_c6 and 0721_m6 hit an audit-helper `TypeError` right after each `rm` (driver log, 2026-11-04
  19:01-19:14). The driver retried `collect()` every 2.5 min; each retry repeated the copy and md5 compare before its
  next delete. So each of the 3 deletes per root has its own check, 4-10 s before it
- 0721_c8: check 00:31:49, first moved-copy delete 00:31:53, then the connection hung until 08:17. At 08:20 a new
  `collect()` repeated the md5 compare (08:20:27) before the other moved copy and the staged root were deleted
- Every check covers every file of the root's output folder except `moved/`: tracks, moved-copy tracks, midlines,
  check JSONs, logs

## A5-F1: moved-copy tracks and the empty-file md5

- The 80 moved-copy tracks (`<root>__w10-12_ft2_wp_ref` and `_wp_moved`, 40 roots) are now rows of `outputs.csv`
  (`kind` `moved_copy_ref`, `moved_copy_moved`). All 80 are on the lab server; md5 matches `deletes.csv` and the fresh
  pass for 80 of 80 (`reverify.md`). None missing or different
- `d41d8cd98f00b204e9800998ecf8427e` is the md5 of an empty file. The tracker writes an empty `<track>.npz.ok` beside each
  finished track (`scripts/remote/qb_track.py:54`, created once, marks the track complete). The staged-root rows list
  every file under `tracks/` that is not a moved-copy track, so each window contributes its track md5 and one empty
  marker md5 (1060 of each). The markers carry no data; they are not rows of `outputs.csv`

## A5-F3: 0727_cc7

- Its stage-tracking table was rejected by the tracker's loader, so no window was tracked and its staged root was not
  deleted. The per-root job still ran the checker step: each of the 2 windows got a check JSON with `status: failed`
  and a missing-track error. These 2 JSONs are on the lab server; their md5 is kept in `outputs.csv` and matches
- `outputs.csv` says so in `note`; `summary.json` counts these 2 windows as `not run` (1063 planned, 1061 files)
- 0721_m5 w0-2: tracker error (logistic fitting); its check JSON records `status: failed`; counted as failed

## A5-F4: ledger

- Added the 3 jobs of 2026-10-25 between the batch-1 tail and batch 2, left out before by a time-text filter: 5468233
  (cluster CPU tracking equivalence, 1 CPU, 1:54), 5468687 (first per-root chain job on 0708_c2: every segmentation step failed, 10 s; resubmitted as 5469410), 5469410 (per-root chain
  equivalence on 0708_c2, 23:46; actual from `sacct`, $0.067; the ledger had none). Rows are now selected by job id
- `time` is the ledger stamp with its offset; 2 rows were stamped in UTC by the machine that wrote them and are
  converted (each read as local or UTC, whichever is nearer the `sacct` Submit time). `submit_sacct` is added
- Actual spend: the 98 rows sum to $5.979; with $1.263 before job 5466204 the total since 2026-10-23 is $7.24 of $15
