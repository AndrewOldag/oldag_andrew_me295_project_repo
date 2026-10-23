# Inbox: freeze-v3

1. Read `CLAUDE.md`, `docs/agents/README.md`, `docs/specs/2026-10-23b_freeze-v3.md` and `docs/reviews/2026-10-23_spec-audit/SUMMARY.md`. Branch `wip/freeze-v3`. Task `tasks/c011-freeze-v3.md`. First status, push
2. Write the proposal (spec item 1). Stop for Andrew (status `waiting on Andrew`)
3. After approval in this inbox: items 3-4
4. Andrew, 2026-10-23 13:41: proposal `docs/proposals/2026-10-23_freeze-v3.md` approved, with these answers. Do items 3-4 of this inbox
   - Open 1: scoring set, seeds, v3 geometry and the curvature-corrected width-free ratio: approved
   - Open 2: accept_clean correct = `good_report` whatever remedies were kept; report remedies kept per class as a separate count
   - Open 3: tracker-run cap 600 for freeze v3
   - Open 4: add a fixed non-growing rod to accept_clean, absolute centre tolerance 0.5 %/h, seeds 20-22 (3 rods; set becomes 51). Include it in the clean basis check
   - Open 5: `stage_log_missing` approved as a held-out fault
   - Stop rules in the proposal stand (clean basis failing a threshold; more than half the labelled set in decline)
   - Record this approval in `docs/decisions.md` and in the proposal header
