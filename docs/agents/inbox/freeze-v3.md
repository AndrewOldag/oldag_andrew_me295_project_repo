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
5. Andrew, 2026-10-23 14:50: work space freed. The planning account (one-time approval by Andrew) deleted the 804 v2 rendered rods in the shared rods folder (every entry without the `v3_` prefix), 4.9 GB. The 240 `v3_` entries and all track caches are untouched. List kept next to the rods folder as `deleted_v2_rods_20261023.txt`. Work space now about 4.8 GB of 10 GB. Sessions still may not delete on the lab server. Continue with held-out sizing, labels and the method runs. v2 results stay valid from their committed caches; if a v2 rod is ever needed again it is re-rendered from code and seed
6. New limit for the lab server.
   - Standing, Andrew 2026-10-23: lab-server jobs: at most 2 jobs of this account at once (count them before starting; start only if fewer than 2), each at most 4 single-thread workers, lowest priority, 1-min load below half the cores, at most one `sweep.py` sweep at a time. `CLAUDE.md` Rules and `docs/decisions.md` 2026-10-23
7. Andrew, 2026-10-23 18:15: stop on `v3_bend30_clean_s20`: option (a). Keep it as accept_clean (correct outcome accept). Report it as a checker false alarm in the results README. `displacement_exceeds_patch` 2x6 labels win as you wrote (accept_repaired 12). Continue: tag `freeze-v3`, rule methods, LLM methods x 3 repeats, metrics, results README
