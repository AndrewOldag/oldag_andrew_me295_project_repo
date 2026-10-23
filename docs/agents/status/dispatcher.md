# dispatcher
Updated: 2026-10-23 13:10 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 2
State: waiting on Andrew
Now: item 7 done except the cluster run; item 6 cluster jobs blocked (job script refused by this session's permission check)
Done since last update:
- Item 7: tracker repo branch `stage-auxdata` 888f972, pushed, not merged; tracker tests 46 passed, 9 skipped
- Item 7: validation on 0708_m12: background drift t3 84.6 -> 2.6, t2 80.1 -> 1.1 px/h (pass, limit 5); rule: sign +, step i = move after frame i; full note in the lab-server work folder (VALIDATION.md)
- Item 7: course checker after the fix: closure t3 76.5 -> 5.53, t2 68.2 -> 11.2 px/h (still fail, threshold 1.0); plane_sections 257, 366 %/h (unchanged, fail)
- Item 7: scan of 122 montage folders: 121 OK; 0727_cc7 mismatch (155 steps, 857 frames); Andrew: continue, flag it
- Item 7: private runner copy on the cluster with 888f972; root listing OK; loader confirmed on 0708_m12
- Item 6: configs (CPU, P100) and ledger check ready; nothing submitted; spent today $0.23; no compute node used
Needs Andrew:
- Cluster: writing the job script (`qb-submit` without `--submit`) was refused by this session's permission check. Add a permission rule, or write and submit the two jobs yourself (configs in the trials configs folder; worst case $0.19 CPU, $0.17 P100)
- 0727_cc7: stage-tracking log covers about 4 h of 9.5 usable h. Shorten its usable window, exclude it, or another rule
- Closure after the fix: residual = motion of the most basal tracked point; 400 px tracked length ends inside the growth zone. Longer track length or a different base rule? (checker and freeze unchanged until you decide)
- plane_sections 257-366 %/h on real windows, not from stage correction; cause not checked
- Dispatcher proposal approval (window 2 h, round limit 200, 2 retries)
- Merge of tracker branch `stage-auxdata` (yours)
