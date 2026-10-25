# diag-analysis
Updated: 2026-10-24 16:50 (local)
Lane: course
Branch: wip/diag-analysis
Last inbox item done: 2
State: ready to merge
Now: section D done; proposal written; nothing applied
Done since last update:
- item 2: `docs/proposals/2026-10-25_diagnostician-repair-misses.md` and `scripts/synth/repair_misses.py` (read-only table); from v3 traces only, 0 tracker runs, 0 LLM calls
- accept_repaired: diagnostician 16 of 36, 20 declines; remedy tree 9 of 12
- group A, 11 runs: declined with no remedy tried, believing no remedy fits a stage-correction error; `register_frames` repairs all 6 rods
- group B, 9 runs (stage_log_missing): `register_frames` rolled back because closure becomes not computable; the label rule drops that check, the roll-back rule does not
- log entry in `docs/running_log_pending/diag-analysis.md`; task c020 done
Needs Andrew:
- C1 (prompt fault-to-remedy map) and C2 (stage_log_summary per-pair spread): approve, edit or reject for a later freeze
- C3: roll-back and label rules disagree on a not-computable check: option (a) labels count it as failing, or (b) roll-back counts it as resolved
