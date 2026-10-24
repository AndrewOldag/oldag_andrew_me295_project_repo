# Inbox: turn-long

1. Research lane. Clone this repo to `~/coord-turn-long/`, branch `status/turn-long` from `main`, for status only. Read `docs/agents/README.md`
2. Your instructions are in the tracker repository, branch `offshoot-turn-interval2`, file `offshoot/turn_interval2/SPEC.md`. Read it and do it. Nothing from it goes into this repo
3. Status here: state, counts, pass or fail, file names only. No values, no biology, no machine names, paths or people
4. Standing rule: never delete, move or rename anything on the lab server. Other sessions use the lab server: one job of this account at a time; wait if another is running
5. New limit for the lab server. This replaces the one-job rule in the research spec.
   - Standing, Andrew 2026-10-23: lab-server jobs: at most 2 jobs of this account at once (count them before starting; start only if fewer than 2), each at most 4 single-thread workers, lowest priority, 1-min load below half the cores, at most one `sweep.py` sweep at a time. `CLAUDE.md` Rules and `docs/decisions.md` 2026-10-23
6. Andrew, 2026-10-23: ssh to the workstation is approved for when host-setup assigns you work there. Use exactly `ssh -o BatchMode=yes kinematics "<command>"` so the VM permission rule matches. Workstation rules in the private workstation file
7. Andrew, 2026-10-23 18:30: workstation disk. About 45 GB free on the whole machine; a full disk crashes it. The work folder there is capped at 20 GB in total (replaces the 40 GB of item 4). Free space must stay at least 20 GB: check `df -h / ~` before and after every copy or job; if a step would leave less than 20 GB free, do not start it and tell Andrew. Sessions cannot delete there, so space only grows: frame subsets only, one root at most per task, large outputs to the lab server. Updated private file: copy `me295/cluster/WORKSTATION.md` again into `private/workstation.md`
8. Coordinator, 2026-10-23 18:45 (spec 2026-10-23c item 6, as changed by coordinator item 13; host-setup test passed, merged b9a3a06): host assignment. All your tracker runs stay on the lab server (interval_2 frames too large for the workstation). Lab-server limit unchanged: at most 2 jobs of this account at once
