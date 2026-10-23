# dispatcher
Updated: 2026-10-23 02:20 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 2
State: waiting on Andrew
Now: item 6 held before submit: stage correction must go into the tracker repo and the cluster runner first (Andrew, 2026-10-23)
Done since last update:
- Item 6: cluster data copy of 0708_m12 checked (1931 files, sizes identical to the lab-server copy)
- Item 6: CPU and P100 configs and the ledger check written (outside the repo); spent today $0.23, nothing submitted by this session
- Item 6: the runner reads no stage-tracking table; probe with cumulative stage-tracking moves on t3: closure 76.5 -> 5.5 px/h (sign +); plane_sections unchanged, 254 -> 256 %/h. `results/2026-10-23_tracker_timing/README.md`
- Decision recorded (`docs/decisions.md`): correction goes into the tracker repo loader, then the runner; no dispatching before
Needs Andrew:
- Stage correction in the tracker repo loader and the cluster runner install (you or the research lane). Rule: positions = stage-position table + cumulative per-frame moves from the stage-tracking table, sign +. Then say `check github`; the two cluster jobs (CPU 8 cpus 2 h, P100 4 cpus 1 h; worst case $0.19 and $0.17) go next
- Approve or change the dispatcher proposal (window 2 h and last-window rule, round limit 200, 2 retries per task)
- After the fix: closure still 5.5 px/h (threshold 1.0) and plane_sections 256 %/h (threshold 3.25) on t3. Likely the provisional midline and the flank term; not checked
- Lab-server probe scripts, preview images and probe outputs left in the timing work folder there (no deletes by sessions)
