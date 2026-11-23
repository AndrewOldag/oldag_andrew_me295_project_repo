# c027 failure modes (from the run)

| failure mode | count | example |
| :-- | --: | :-- |
| tracker error in the batch run (no base track) | 4 | 0711_m1__w0-2 |
| window not measured in any batch | 2 | 0727_cc7__w0-2 |
| declined by rule (gating check not computable) | 58 | 0708_c10__w20-22 |
| diagnostician step limit | 6 | 0708_c4__w0-2 |
| tree step limit | 0 | - |
| window error in the run | 0 | - |
| paused at the cut-off (track not cached) | 4 | 0708_m9__w10-12 |
| rolled-back remedy that made closure worse (diagnostician) | 33 | 0708_c10__w0-2 |
| rolled-back remedy that made closure worse (tree) | 76 | 0708_c10__w0-2 |
| auditor flag | 240 | 0708_c10: r02 |
| retrack task failed on the cluster | 28 | 0708_c4__w0-2_ft2__st2__L1000.npz (FileNotFoundError: [Errno 2] No such file or directory: '0708_c4__w0-2_ft2__st2__L1000.npz') |
| link or master down (queue) | 1 | {"status": "connection down"} |

Synthetic findings (spec section C) are reported by task c029 and c030 in their own results.

