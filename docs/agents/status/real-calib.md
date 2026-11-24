# real-calib
Updated: 2026-11-23 20:46 (local)
Lane: course
Branch: wip/zone-reference
Last inbox item done: 31
State: waiting on Andrew
Now: inbox 32 (c035) step 4: overlays ready; still waiting for Andrew's labels (checked 20:46, labels.csv empty; no new inbox item)
Done since last update:
- Proposal (bcf0733): seed 20261123, strata 5/4/5/5/5 by condition, one window per root, threshold rule, step 1 stop rule
- Step 1 (b3e4e90): residual split into common mode and shape in `checker/zone_checks.py`. Synthetic re-run: shape flags 15 of 15 at every shift (-60 to +60 px), 0 of 18 clean, 0 of 9 repaired (synthetic shape threshold 0.0019; shifted 0.045-0.18). Stop rule met
- Step 2: 24 accepted c027 windows drawn (results/2026-11-23_zone_reference/sample.csv)
- Step 3: 24 overlays, 3 frames each (first, middle, last) plus a tip-region zoom row. Frames read from storage read-only, one window at a time, raw frames deleted after use. No residual values or flags shown
- Tests: 502 passed, 3 skipped (full suite)
Needs Andrew:
- Label the 24 windows: `python scripts/ops/label_server.py .claude/worktrees/real-calib/staging/c035_overlays` (on main, ef0636e) or the `index.html` there; it writes `labels.csv` in that folder. Then ping real-calib
