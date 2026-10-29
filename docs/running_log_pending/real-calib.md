## 2026-10-25 (build account, real-calib)
- Done: full-batch proposal `docs/proposals/2026-10-25_full-batch.md` (935cfe7): 102 include-yes roots, 2368.1 usable h, 1189 windows, 88 413 frames, recomputed with `agents/dispatcher.py` windows; agrees with planning's count
- Done: first batch picked: 11 roots, one per experiment and condition, 126 windows; segmentation midlines started on the lab server 15:03, about 45 s per window
- Demo: `python -c "import sys; sys.path.insert(0,'.'); from agents.dispatcher import *; print(sum(len(make_tasks(r, load_config())) for r in manifest_rows()))"` prints 1189
- Remaining: GPU midlines (cluster), md5-checked pull, rolling staging, 1000 px tracking, checker, `results/2026-10-25_full_batch_1/`
- Bottlenecks: cluster connection master down (Andrew)
