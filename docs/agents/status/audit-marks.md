# audit-marks
Updated: 2026-10-24 12:10 (local)
Lane: course
Branch: wip/audit-marks
Last inbox item done: 6
State: ready to merge
Now: items 1, 3, 4, 5, 6 done; item 2 (remote delete) waits on Andrew. The branch can be merged now; the delete does not touch it
Done since last update:
- Item 6: work moved to wip/audit-marks in its own worktree; nothing more pushed to main
- Item 3: rules-3 069d5e8, rules-5 3378952, numbers-3 to -9 af951e1, kinematics-3 and -5 0469497, specs-11 ed8279a, specs-9 and -13 3163fec (incl. autotrace status paths, item 6). Pre-push hook 0 hits on each push
- Item 1: 71 findings marked (13 handled, 17 fixed, 2 known limit, 39 no action); marks line in SUMMARY.md, d65c3df
- Item 4: MARKS_2026-10-24.md (58 ids) and PLAN_AMENDMENTS_2026-10-24.md written as new files in the research audit folder, md5 checked; nothing edited, moved or deleted there. Tracker repo docs commits 919c740 (kinematics-3) and 7f69563 (tracking-8), pushed
- Item 2: decisions entry written; the delete itself was refused by the session's permission check
- Commits on wip/audit-marks: 15c4ef0, 069d5e8, 3378952, af951e1, 0469497, ed8279a, 3163fec, d65c3df, and this status commit
- Earlier, by mistake as the coordinator, on main: 915859a, 074e102, eaaa37b (kept by Andrew)
Needs Andrew:
- Run `git push origin --delete status/gate2` (approved in item 2; refused for the session). The marks for rules-4 and specs-20 say fixed by this delete
- Lab report 2 (on wip/lab-report-2) not edited: numbers-3 to -9 wordings are in Lab report 1, the log, the summary and the background file, and were fixed there; Lab report 1 has a dated corrections section, submitted text otherwise unchanged except access wording (rules-5)
- Results READMEs unchanged (no result changes): `results/2026-10-12b_scored_v1/README.md` (5.2 steps) and `results/2026-10-13_auditor_v1/README.md` ("calls") keep the old wording
