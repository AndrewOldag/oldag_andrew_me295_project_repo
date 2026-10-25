# Overnight 2026-10-25

Planning account, under Andrew's delegation at 00:21: make decisions that keep the project producing measurable work overnight. Hard limits: cluster spend cap $15 total; no delete of anything a Claude session did not write on the workstation, lab server or cluster; never delete on Andrew's Mac. Checks at 01:00, 03:00, 05:00; report at 08:00.

## 00:40 decisions
- State at 00:14: dispatcher running the agent pass over the 48 real subset windows; real-calib, closure-fix, diag-analysis, freeze-v31 done and idle; cluster spend $1.03 of $15
- dispatcher (item 36): finish the subset run, then 2 repeat agent runs for agreement; README. Reason: the real-movie demo and repeated-run reliability are both required (Project Guideline; Lab report 3)
- closure-fix (item 3): make `real_moved.py` write-once. Reason: rename on the lab server breaks `CLAUDE.md` (Needs Andrew item; fix keeps the rule, no rule change)
- diag-analysis (item 3): C1, C2 and C3 option (a) behind an off-by-default switch on `wip/v4-candidate`; label unseen seeds 26-28; development check; freeze v4 candidate proposal. Reason: prepares a later freeze without touching v3 scoring; the scored run and the C3 choice stay Andrew's to approve
- freeze-v31 (item 9): refresh the Lab report 2 draft from the log. Reason: due Fri 30 Oct; the lab-report-2 session is not live
- real-calib (item 7): full-batch proposal and a first batch of real windows (midlines, tracking, checker, no agents), capped at $3 added worst-case spend and 35 GB on the cluster. Reason: project goal is all include-yes roots; measured cost is about $0.003 per window
- Not decided, left for Andrew: coord-tick elevated install; spec-audit marks; workstation disk (sessions cannot delete); local branch worktree-coordinator-c007
