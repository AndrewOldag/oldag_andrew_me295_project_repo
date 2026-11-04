# diag-analysis
Updated: 2026-11-03 21:18 (local)
Lane: course
Branch: wip/v4-audit-fixes
Last inbox item done: 6
State: ready to merge
Now: item 6 done; Argon audit fixes on freeze v4, no scored result changed
Done since last update:
- A2-F1: per-method v3 outcomes on stage_log_missing in decompose text and v4 README; tables unchanged (9cfa8c0)
- A2-F2: labels.md header seeds 26, 27, 28; labels.json byte-identical (d9d006c)
- A2-F3: remedy-kept metric counts any status; accepted-only counts single agent v3 9, v4 14 (match Argon) (97b2700)
- Known limits in the v4 README, counts verified from traces: (a) second_root 8/9 accept_on_decline (diagnostician); (b) single agent check_report 153/153, 0/171 remedy results with numbers; (c) single agent bad_stage_correction 7/9 accepts with closure failing; (d) 7 diagnostician runs with a remedy and no failing check (inbox said 2: those are the accept_clean ones; 3 accept_repaired and 2 second_root also) (e959700)
- decisions: triage entry and frozen single-agent limit; A2-F4 not acted on (scoring already falls back to the file name)
- tests 351 passed, 2 skipped
Needs Andrew:
- merge of `wip/v4-audit-fixes`
