# real-calib
Updated: 2026-11-23 21:50 (local)
Lane: course
Branch: wip/zone-reference
Last inbox item done: 33
State: waiting on Andrew
Now: c035: all 150 overlays exist; waiting for labels of windows 25-150
Done since last update:
- Overlays for windows 25-150 made by the detached job: 150 of 150, none failed; raw frames deleted after each window (`_raw` empty)
- Index `staging/c035_overlays/index.html` and `staging/c035_overlays/labels.csv` (in the real-calib worktree, not pushed): 150 rows in sample order; first 24 labels kept as written (21 clean, 3 not clean), rows 25-150 blank
- No threshold computed
Needs Andrew:
- Label windows 25-150: `python scripts/ops/label_server.py .claude/worktrees/real-calib/staging/c035_overlays` (from the main checkout), then open http://127.0.0.1:8765. Then start me again
