# diag-analysis
Updated: 2026-11-02 14:22 (local)
Lane: course
Branch: wip/v4-decompose (wip/diag-analysis and wip/v4-candidate merged and deleted)
Last inbox item done: 5
State: ready to merge
Now: v3-to-v4 split into relabelling and agent change, on `wip/v4-decompose`
Done since last update:
- `results/2026-10-25_freeze_v4/decompose_v3_v4.md` and a README section; `python scripts/synth/scored_v4.py decompose`; from cached runs, no tracker or LLM runs
- C3 (a) relabels stage_log_missing (3 rods per seed set) from accept_repaired to decline; every v3 method declined them, so those declines now score correct with no behaviour change; all-decline 21 -> 24 of 51
- diagnostician balanced accuracy: v3 0.69; v3 runs under C3 (a) labels 0.75 (relabelling); v4 0.93. Unchanged rows (48 rods): v3 0.74, v4 0.92
- remedy tree (unchanged method): 0.81 -> 0.90 by relabelling, 0.93 in v4 (seed draw)
- single agent unchanged rows: v3 0.67, v4 0.64
Needs Andrew:
- merge of `wip/v4-decompose` (results note, driver command, status, log); no code path used by v3 or v4 runs changed
