# dispatcher
Updated: 2026-10-25 21:45 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 39
State: ready to merge
Now: task c022 done: agent run over the 126 first-batch windows, results README; ready to merge
Done since last update:
- Item 39: run 4 (reported), wall 1892 s: 114 accepted, 9 declined at closure (bad stage correction 8, midline jitter 1), 3 not collected (tracker 'arange' error, real-calib's same 3); auditor 91 cleared, 23 flagged (summary outlier 20, other 3). results/2026-10-25_full_batch_1_agents/ (outcome counts only; traces and summary.json in staging, git-ignored, because the auditor's text quotes REGR values)
- Runs 1-3 failed on run-code faults, each fixed with a test and a decisions entry: collect error now fails one window only; ssh keepalive and fetch of a finished host track; summary.json written before printing
- Found: 4 windows with no computable closure were accepted with no gating check; the auditor flagged all 4
- Suite 317 passed, 1 skipped
Needs Andrew:
- A window with no computable gating check (closure not finite) is accepted by the current rule. Keep, or decline such windows? (4 of 126 here; the auditor caught them)
- results/2026-10-25_real_subset/ on main (c019, before the 2026-10-25 rule) has REGR, growth-zone and flank values in tables.md and its README. Keep, or strip them?
