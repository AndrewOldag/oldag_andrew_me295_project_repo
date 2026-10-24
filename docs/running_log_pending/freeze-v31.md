## 2026-10-24 (build account, session freeze-v31)
- Done: `scripts/synth/scored_v31.py`, freeze v3.1 driver on top of `scored_v3.py` (v3 code unchanged); `tests/test_freeze_v31.py` 3 passed (1c1a548)
- Done: second_root cause from the v3 runs: only plane_sections fails; crop_or_mask leaves every value unchanged; `use_width_free_ratio` makes all applied checks pass with a good centre, so methods accept. Alternative repair: remedy tree 3 of 3, diagnostician 9 of 9, single agent 6 of 9 (`results/2026-10-24_freeze_v3.1/second_root.md`)
- Done: sizing sweep 1 on the lab server: stopped by the 10 GB work-space limit (`projected_space`) after 13 of 114 runs, 0 failed, 67 s; work space 8.06 -> 8.32 GB
- Done: partial sizing: rigid_drift 0.5 and 1.5, bad_stage_correction 3, stage_log_missing 1 fail a check on 3 of 3 seeds but measure well unremedied (rule part 2 fails)
- Demo: `python scripts/synth/scored_v31.py sizing` prints the sizing table (`results/2026-10-24_freeze_v3.1/sizing.md`)
- Remaining: rest of sizing (102 runs), labels on seeds 23-25, tag `freeze-v3.1`, rule and LLM methods, metrics side by side with v3
- Bottlenecks: lab-server work space at the 10 GB sweep limit; about 6 GB more needed; Andrew frees space or raises the limit
