# autotrace
Updated: 2026-10-24 03:25 (local)
Lane: course
Branch: wip/autotrace
Last inbox item done: 13
State: waiting on Andrew
Now: net2_midline_ft2 trained and scored; waiting for Andrew to adopt it (or not) as the real-movie midline source
Done since last update:
- Item 13: option A fine-tune done. Private copy finetune_midline_acc.py (micro-batches of 3, gradients accumulated to the batch of 6, one optimizer step per batch; all else unchanged). P100 job 5390367: 20 epochs, validation loss 0.0095 -> best 0.0022 (epoch 20), 1 h 23 min, $0.234. Cluster spend today $0.691 of $5
- Weights net2_midline_ft2.pt with ft2_run.json (seed 20261023, recipe and change), train_keys.csv (181 keys), the training script copy and the job log: in the cluster work folder and in the lab-server work folder `me295/c013_ft2/out/` (lab data root); not on the VM, not in git. No existing weights file overwritten
- Held-out score, 28 frames (16 roots), tile, lo 0.1, same conversion for every net:
  - base net2: no root 1, off the root 24 of 28
  - net2_midline_ft: no root 0, off 0; distance median 2.9 px (6.1 um), p90 7.4 px (15.6 um); end +28.0 px past the hand end
  - net2_midline_ft2: no root 0, off 0; distance median 2.4 px (5.1 um), p90 6.4 px (13.5 um); end +23.2 px (49 um) past the hand end, |end| p90 29.9 px
  - end-point offset: hand traces end about 35 px behind the apex, so ft2 ends about 12 px behind the apex (ft about 7 px)
  - per-experiment table in `results/2026-10-23_autotrace/README.md`; score files with the run in the lab-server work folder
- Recipe change recorded in the results README; log entry `docs/running_log_pending/autotrace.md`
- Earlier: items 1-12 done (drafts, previews, review tools, training list)
Needs Andrew:
- Adopt net2_midline_ft2 as the real-movie midline source? If yes: record in decisions, and the 0708_m12 slice is rerun with it (dispatcher task)
