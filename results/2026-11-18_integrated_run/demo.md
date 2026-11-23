# c027 B5: fresh one-root demo (0708_c4)

| window | cached run | demo | closure before (px/h) cached / demo | match |
| :-- | :-- | :-- | :-- | :-- |
| 0708_c4__w0-2 | step_limit | step_limit | 103.55 / 103.55 | yes |
| 0708_c4__w2-4 | declined by agent | declined by agent | 97.69 / 97.69 | yes |
| 0708_c4__w4-6 | accepted | accepted | 4.51 / 4.51 | yes |
| 0708_c4__w6-8 | accepted | accepted | 5.83 / 5.83 | yes |
| 0708_c4__w8-10 | accepted | accepted | 3.00 / 3.00 | yes |
| 0708_c4__w10-12 | accepted | accepted | 2.00 / 2.00 | yes |
| 0708_c4__w12-14 | accepted | accepted | 1.45 / 1.45 | yes |
| 0708_c4__w14-16 | accepted | accepted | 3.12 / 3.12 | yes |
| 0708_c4__w16-18 | accepted | accepted | 1.82 / 1.82 | yes |
| 0708_c4__w18-20 | accepted | accepted | 2.62 / 2.62 | yes |
| 0708_c4__w20-22 | accepted | accepted | 2.59 / 2.59 | yes |
| 0708_c4__w22-24 | accepted | accepted | 1.42 / 1.42 | yes |

Same outcome: 12 of 12 windows.

Auditor flags: cached [('r07', 'summary_outlier')]; demo [('r07', 'summary_outlier')]; same. LLM calls: cached 4, demo 6.

| stage | wall time (min) |
| :-- | --: |
| stage the root's images to the cluster | 2.6 |
| cluster job: midline net, QC, track, checker; collect, md5 (includes queue wait) | 27.8 |
| fetch base tracks to the VM | 0.1 |
| agents and auditor | 3.5 |
