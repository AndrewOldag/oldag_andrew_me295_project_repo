# real-calib
Updated: 2026-10-26 09:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 13
State: working
Now: item 11: batch 2 running root by root on the cluster (2 GPU jobs at a time); this morning's GPU queue is slow (one job pending on priority); checker passes every 10 min
Done since last update:
- Item 13 (98711a2): not computable counts as decline, its count kept beside; public outputs `windows.csv`, `table.md`, `summary.json` carry outcome and check values only; full per-window records (detail strings, closure terms, basal speeds) moved to git-ignored `staging/full_batch_<N>/` and removed from the tree
- Batch 1 under the rule: accept 109, decline 14 (4 not computable), failed 3
- Batch 2 at 09:10: 37 of 91 roots collected (md5 verified, staged frames cleared), 0 errors; 437 windows checked: accept 371, decline 49 (9 not computable), failed 17. Interim tables in `results/2026-10-25_full_batch_2/`
- Spend since 2026-10-23: about $4.03 of $15; projection for all 91 roots about $7.6
Needs Andrew:
- Merging main into this branch is refused by the pre-push blocklist: main's `docs/agents/inbox/real-calib.md` lines 18, 19 and 24 name the cluster, and the hook scans every file a pushed commit changes. Not bypassed; this branch is not merged with main (the coordinator merges it into main as usual)
