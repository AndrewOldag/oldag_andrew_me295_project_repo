# Inbox: audit-marks

Lane: course (items 1-3) and research (item 4). Branch `wip/audit-marks`. Task `tasks/c015-audit-marks.md`. Read `CLAUDE.md` and `docs/agents/README.md` first.

1. Andrew, 2026-10-24: mark every finding in `docs/reviews/2026-10-23_spec-audit/` (specs, rules, numbers, kinematics, bending-and-tracking, evaluation). Fill each `- Andrew:` line with `accepted`, plus one of: `handled (freeze v3 / v3.1)`, `fixed (<commit>)`, `known limit (report)`, `no action`. Rules:
   - The 17 design-choice findings: accepted, handled (freeze v3 or v3.1); evaluation-7 and -8: accepted, known limit (report)
   - rules-1: accepted, no action (Andrew 2026-10-12 decision stands)
   - rules-4 and specs-20: accepted, fixed (branch `status/gate2` removed, item 2)
   - evaluation-11: accepted, no action (syllabus lists reports 1-4)
   - All others: accepted; fix the cheap ones in item 3, the rest no action
   - Add a line to SUMMARY.md: marked by Andrew 2026-10-24 (written by this session at his direction)
2. Andrew, 2026-10-24: remove the branch `status/gate2` from the GitHub remote: `git push origin --delete status/gate2`. Andrew approved this delete. Nothing else is deleted. Record it in `docs/decisions.md` (reason: spec audit rules-4 and specs-20, a VM path and research-lane outcomes on the public remote)
3. Small fixes, one commit each, pre-push hook on: rules-3 and rules-5 (paths and access details in tracked files: replace with role names; private copy stays in `private/`), numbers-3 to -9 (wording in `docs/reports/2026-10-30_lab-report-2.md` and the log notes it cites), kinematics-3 and -5 (doc wording in `docs/context/research_background.md`), specs-9, -11, -13 (missing spec-done notes in the log, stale status and roster lines, freeze v2 header). No code, threshold or result changes
4. Research audit, Andrew 2026-10-24 (all decisions accepted as recommended). Server work folder of the research spec audit (lab data root, `spec_audit_20261023/reviews/`): write a NEW file `MARKS_2026-10-24.md` beside `SUMMARY.md` (do not edit or overwrite existing files). One line per finding id: `accepted` plus action:
   - gate2-threshold-1, -2, -3, -5, -6: closed by decision (T dropped, Andrew 2026-10-23)
   - plan-1: report Gate 2 as measured with the uncoupled tracker; deviation stated; no coupled rerun now
   - plan-2: keep the flank-line spacing D; add the reason (dREGR measured at the flank lines, so their separation is the lever arm; under full width the validation would fail, 0.476 / 0.522)
   - plan-5: report both readings (0.18 and 4.83 %/h against 0.8)
   - kinematics-4: state in the turn and ST reports that the primary DGCR route is base-relative; call unchanged
   - kinematics-3: fix the CONVENTIONS sign text to match the code (tracker repo, new commit on `offshoot-structure-tensor`, docs only)
   - tracking-3: on Andrew's check-the-paper list (Chavarria-Krauser 2008)
   - tracking-8: add the origin move (QC to apex) to the METHOD deviation list (tracker repo, docs only)
   - rules-3: fixed in the course repo (coordinator inbox item on `sweep.py` locks)
   - everything else: accepted, no action
   Also write `PLAN_AMENDMENTS_2026-10-24.md` in the same folder: the plan-2 reason and the plan-5 two readings, as text Andrew copies into his Analysis Plan
5. Status ready to merge with the list of commits. No server deletes, moves or renames
6. Andrew, 2026-10-24 12:05: keep the three commits (option 1); the coordinator records them. From now on act only as audit-marks: work on `wip/audit-marks` in your own worktree, never on main. Then do items 1-5. Add to item 3: `docs/agents/status/autotrace.md` line 11 names lab-server paths; replace with role names ("the dispatcher's tracker weights folder on the lab server")
