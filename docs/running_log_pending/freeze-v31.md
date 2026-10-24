## 2026-10-24 (build account, session freeze-v31)
- Done: `scripts/synth/scored_v31.py`, freeze v3.1 driver on top of `scored_v3.py` (v3 code unchanged); `tests/test_freeze_v31.py` 3 passed (1c1a548)
- Done: second_root cause from the v3 runs: only plane_sections fails; crop_or_mask leaves every value unchanged; `use_width_free_ratio` makes all applied checks pass with a good centre, so methods accept. Alternative repair: remedy tree 3 of 3, diagnostician 9 of 9, single agent 6 of 9 (`results/2026-10-24_freeze_v3.1/second_root.md`)
- Done: sizing sweep 1 on the lab server: stopped by the 10 GB work-space limit after 13 of 114 runs, 0 failed. Lab server then set to storage only (Andrew); tracker runs moved to the workstation
- Done: runner settings `rods_dir`, `max_gb` (95764c7); cache-match test on the workstation passed: renders identical 44 of 44 files, tracks within 3.4e-13 px (`cache_match.md`, ec9c589)
- Done: sizing sweeps 2-3 on the workstation: 108 runs, 0 failed; outputs on the lab server, verified by count and sha256 (460 files). New tracker runs 120 of 300
- Done: sizing (`sizing.md`): no fault qualifies at the tested sizes; at most bad_stage_correction can (register_frames repairs 1 of 3 at 5 px). Spec stop rule met (fewer than 3 faults)
- Demo: `python scripts/synth/scored_v31.py sizing` prints the sizing table
- Remaining: Andrew's choice at the stop rule; then labels, tag, methods, metrics if v3.1 continues
- Bottlenecks: stop rule, waiting on Andrew
