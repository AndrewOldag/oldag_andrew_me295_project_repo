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

## 00:45 Andrew's answers
- Coordinator tick is installed and running all day; the install line was stale. Coordinator item 25 clears it
- Spec-audit marks and workstation disk: Andrew, 25 Oct daytime
- Local branch worktree-coordinator-c007: drop if not needed (coordinator item 25)
- C3 option (a) and the scored v4 run approved (diag-analysis item 4): tag freeze-v4 after the seed 26-28 labels are committed, then all methods on 26-28, LLM methods 3 repeats

## 01:00 check
- No push from any session since 23:05 (dispatcher status) and none from the coordinator since its 23:50 pass, although main changed at 00:25 and 00:40; a tick pass should have followed within 10 min
- Reading: the VM, or the tick and the live sessions on it, may have stopped (known VM timeout). Not confirmed: the planning account cannot reach the VM tonight
- No new decisions. The 00:40 and 00:45 items stand and will be picked up when the tick runs again. Next check 03:00

## 03:00 check
- Still no push from any VM session or the coordinator since 23:50 (3 h). The VM is very likely stopped; it cannot be reached from the planning account
- Planning work done here instead: full-batch sizing from the manifest. 102 include-yes roots, 2368 usable hours, 1189 two-hour windows (5 trials, 11 experiment-condition groups, 55-156 windows each). GPU midlines about $3.85 in total; cluster staging about 511 GB. Storage is the limit, not spend
- Decision (real-calib item 8): rolling staging on the cluster. Sessions may delete window-frame copies that a Claude session made in the c019 cluster folder, after md5-verified outputs are on the lab server, logged in `DELETED.log`. Reason: within tonight's hard limit (Claude-written files only); without it, only about 50 more windows fit before Andrew clears the folder. Lab server and workstation stay no-delete

## 05:00 check
- No push from any VM session or the coordinator since 23:50 (5 h). Dispatcher's last push 22:44 (run started); no subset results on `wip/dispatcher`. VM not reachable from the planning account
- No work could be queued to finish by 08:00: every queued item needs the VM, the tick or a live session
- Restart order when the VM is back (resume rules in `CLAUDE.md`):
  - (1) Check `~/vm-health/uptime.log` for the gap start; check free memory and disk (Edge crash dumps, `build-vm` notes)
  - (2) Confirm the coordinator tick runs; its first pass picks up coordinator item 25 and pings sessions with changed inboxes
  - (3) dispatcher: restart the 48-window agent run; runs already in the results folder are skipped. Then item 36 (repeats, README)
  - (4) real-calib items 7-8, diag-analysis items 3-4, freeze-v31 item 9, closure-fix item 3: sessions read their inboxes on `check github`; restart any that are gone

## 14:45 correction
- The VM did not go down. Claude Code stopped the dispatcher's subset run at 00:10 for low VM memory (7.7 GB total, several idle sessions open) after 1 window. The dispatcher set `waiting on Andrew` at 00:10 but pushed it only at 14:39. The coordinator tick also pushed nothing after 23:50; cause not yet known
- The 01:00-05:00 notes that the VM was likely stopped were wrong. The planning account also sent no push notification to Andrew overnight
- dispatcher item 37: restart now, with a memory check before each window
