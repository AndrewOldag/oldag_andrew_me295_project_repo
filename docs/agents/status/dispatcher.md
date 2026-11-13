# dispatcher
Updated: 2026-11-12 18:20 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 44
State: waiting on Andrew
Now: item 45 (task c026): ready to run the remedy tree; blocked on the cluster connection master (down since at least 16:00). Checking every 10 min; the tree starts when it is up
Done since last update:
- Proposal `docs/proposals/2026-11-12_batch2-agents.md` committed before any run (f2ec5be)
- Adapter (37d108b): the tree reads the slice's gating checks; on real windows without a moved copy (81 of 84) rigid invariance had counted as failing. $12 spend stop in the ledger wrapper; one staged root at a time with md5-checked clears
- Fix (ca66ae6): `Link.run` cut large outputs (606 520-byte track came back as 212 992 bytes); now read to EOF. Caught by the fetch md5 check
- Fix (`real_slice.py --audit-only`): rebuilds multi-window roots from root_id and window_h
- 87 batch-2 tracks of the 84 windows fetched from storage, md5 checked, own cache. VM checker equals batch-2 closure on all 84 (max difference 4.9e-5 px/h); closure the only failing gate on each
- Report step written and tested. Suite: 393 passed, 2 skipped (before the last 3 tests; 13 c026 tests pass)
Needs Andrew:
- Open the cluster connection master on the lab server. Every remedy retrack needs it; deadline for the README Sat 14 Nov 20:00
