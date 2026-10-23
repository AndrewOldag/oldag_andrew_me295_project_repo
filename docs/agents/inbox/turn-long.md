# Inbox: turn-long

1. Research lane. Clone this repo to `~/coord-turn-long/`, branch `status/turn-long` from `main`, for status only. Read `docs/agents/README.md`
2. Your instructions are in the tracker repository, branch `offshoot-turn-interval2`, file `offshoot/turn_interval2/SPEC.md`. Read it and do it. Nothing from it goes into this repo
3. Status here: state, counts, pass or fail, file names only. No values, no biology, no machine names, paths or people
4. Standing rule: never delete, move or rename anything on the lab server. Other sessions use the lab server: one job of this account at a time; wait if another is running
5. New limit for the lab server. This replaces the one-job rule in the research spec.
   - Standing, Andrew 2026-10-23: lab-server jobs: at most 2 jobs of this account at once (count them before starting; start only if fewer than 2), each at most 4 single-thread workers, lowest priority, 1-min load below half the cores, at most one `sweep.py` sweep at a time. `CLAUDE.md` Rules and `docs/decisions.md` 2026-10-23
