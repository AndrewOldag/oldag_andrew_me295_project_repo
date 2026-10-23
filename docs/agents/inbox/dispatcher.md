# Inbox: dispatcher

1. Read `CLAUDE.md`, `docs/agents/README.md` and `docs/specs/2026-10-23_next-steps-lr2-dispatcher.md` section B. Branch `wip/dispatcher`. Task file `tasks/c010-dispatcher.md`. First status, push
2. Do B1 (proposal) and stop for Andrew on it. In parallel do B2 (tracker timing on the lab server, shared-machine limits, one sweep at a time) and B4 (cost estimate, using the B3 cluster rules). Submit nothing to the cluster
3. B5 only after Andrew approves the proposal and a budget in this inbox
4. Andrew, 2026-10-23: cluster rules in spec B3. P100 or V100 only, picked by availability. Initial trials budget $5 total (CPU and GPU), hard cap, worst case per job from the time limit
5. Andrew, 2026-10-23: initial cluster trials approved under the $5 cap (spec B3). Copy the private cluster file (spec B3) to `private/cluster.md`, read it, then run its trial plan: pull 3 roots one at a time, time them on CPU and P100/V100, record cost per job. Write only in the one cluster folder it names. Connection down or any stop condition in that file: Needs Andrew, stop the cluster part, continue B1 and B2
