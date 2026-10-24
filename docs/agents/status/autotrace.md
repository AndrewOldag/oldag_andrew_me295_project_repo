# autotrace
Updated: 2026-10-24 02:05 (local)
Lane: course
Branch: wip/autotrace
Last inbox item done: 11
State: working
Now: item 13, option A fine-tune (gradient accumulation, batch 3 x 2) as P100 job 5390367; then score ft2 on the 28 held-out frames
Done since last update:
- Item 13: private copy finetune_midline_acc.py (micro-batches of 3, gradients accumulated to the batch of 6, one optimizer step per batch; all else unchanged) in the cluster work folder; job 5390367 submitted. Ledger: spent 0.457 + worst case 0.336 = 0.793 of 5.00
- Item 12: Andrew's files checked: 112 reviewed (72 y, 40 n), 109 traced + 3 skipped, 28 held-out traced; key sets match the pack
- Item 12: training list 181 traces (72 July include-yes in-window + 109 pack), checked against the manifest and the held-out list (no held-out frame or root); 43 July traces refused (c1, c7, c3, c12). Keys in `train_keys.csv` in the cluster work folder; seed 20261023; recipe defaults, from base net2. 181 frames (994 MB) on the cluster
- Job 5383578 (P100 16 GB): CUDA out of memory at the first training step (15.2 GiB allocated, 0.4 GiB more needed). 2 min 41 s, $0.008. No weights written
- Job 5383707 (V100): scheduler start estimate 2026-11-03; cancelled while pending, $0. The two other V100 partitions belong to other accounts
- Cluster spend today: $0.457 of $5 (ledger updated)
- Held-out score (28 frames, 16 roots; tile, lo 0.1; same conversion for every net):
  - base net2: no root 1, off the root 24 of 28 (coverage 0)
  - current net2_midline_ft: no root 0, off the root 0; distance median 2.9 px (6.1 um), p90 7.4 px (15.6 um); net end median 28 px past the hand end
  - table and per experiment in `results/2026-10-23_autotrace/README.md`; ft2 row pending
- Earlier: items 1-11 done (drafts, previews, review tools; see results README)
Needs Andrew:
- none
