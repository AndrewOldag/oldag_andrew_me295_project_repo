# compound
Updated: 2026-11-20 23:40 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 4
State: working
Now: item 5. c029 2-rod cluster vs VM equivalence submitted (array 7417121); then 852 non-register label runs (48 array tasks, worst case $0.58). c030 auditor repeat 1 at 29 of 30, repeat 2 next (detached, one LLM run at a time)
Done since last update:
- Item 4: VM label sweep stopped; rods rendered; LLM floor 3 GB
- Merged origin/main (5874d5b): retrack_queue.py
- `scripts/synth/compound_queue.py`: synthetic-rod job kind (rods VM -> storage -> cluster with md5, one array task per rendered rod, fetch with md5 to storage and VM), own cluster code and work folders, c027 ledger and $15 stop; 8 fake-cluster tests pass
- c030 repeat 1: one run ended on the account usage limit at 15:09 (set aside, rerun); restarted 23:05
Needs Andrew:
- none
