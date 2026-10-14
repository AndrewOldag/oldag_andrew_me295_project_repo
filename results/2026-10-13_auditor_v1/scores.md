# Auditor v1: scores

Cells: flagged / runs in the group, accepted runs only. False flags = good reports flagged. alt_repair: second_root runs that applied `use_width_free_ratio` and accepted a good centre; reported apart.

## Rule auditor (|z| > 3 or a failed final check)

| Set | Method | Accepted | False accepts flagged | Good reports flagged | alt_repair flagged |
| :-- | :-- | --: | :-- | :-- | :-- |
| dev | script | 25 | 10 / 10 | 15 / 15 | - |
| dev | remedy_tree | 14 | - | 6 / 14 | - |
| dev | diagnostician | 15 | - | 7 / 15 | - |
| dev | single_agent | 6 | - | 0 / 6 | - |
| heldout | script | 15 | 12 / 12 | 3 / 3 | - |
| heldout | remedy_tree | 9 | 3 / 3 | 0 / 3 | 0 / 3 |
| heldout | diagnostician | 5 | - | 0 / 2 | 0 / 3 |
| heldout | single_agent | 6 | - | 2 / 3 | 0 / 3 |

## LLM auditor, per run

| Run | Commit | Status | Steps | Undecided | False accepts flagged | Good reports flagged | alt_repair flagged | Tokens in | Tokens out | Call time (s) |
| :-- | :-- | :-- | --: | --: | :-- | :-- | :-- | --: | --: | --: |
| dev_diagnostician_1 | 8a01264 | report | 5 | 0 | - | 7 / 15 | - | 70399 | 4562 | 50.4 |
| dev_diagnostician_2 | b1055da | report | 8 | 0 | - | 5 / 15 | - | 124760 | 5686 | 65.0 |
| dev_diagnostician_3 | aa8483a | report | 5 | 0 | - | 0 / 15 | - | 72673 | 5034 | 57.3 |
| dev_remedy_tree_1 | 8a01264 | report | 4 | 0 | - | 4 / 14 | - | 55097 | 3907 | 44.0 |
| dev_remedy_tree_2 | b1055da | report | 5 | 0 | - | 0 / 14 | - | 73322 | 4264 | 48.5 |
| dev_remedy_tree_3 | aa8483a | report | 11 | 0 | - | 0 / 14 | - | 170561 | 6981 | 82.2 |
| dev_script_1 | 8a01264 | report | 5 | 0 | 10 / 10 | 15 / 15 | - | 69479 | 2793 | 33.0 |
| dev_script_2 | b1055da | report | 5 | 0 | 10 / 10 | 15 / 15 | - | 70423 | 2924 | 33.5 |
| dev_script_3 | aa8483a | report | 5 | 0 | 10 / 10 | 15 / 15 | - | 70536 | 2998 | 33.5 |
| dev_single_agent_1 | 8a01264 | report | 4 | 0 | - | 5 / 6 | - | 55610 | 2747 | 29.8 |
| dev_single_agent_2 | b1055da | report | 4 | 0 | - | 0 / 6 | - | 57102 | 5625 | 58.3 |
| dev_single_agent_3 | aa8483a | report | 5 | 0 | - | 5 / 6 | - | 72689 | 4284 | 47.5 |
| heldout_diagnostician_1 | 23d93ef | report | 10 | 0 | - | 2 / 2 | 0 / 3 | 119061 | 6714 | 77.8 |
| heldout_diagnostician_2 | 23d93ef | report | 11 | 0 | - | 0 / 2 | 0 / 3 | 131062 | 4699 | 56.2 |
| heldout_diagnostician_3 | 23d93ef | report | 10 | 0 | - | 0 / 2 | 0 / 3 | 118660 | 5471 | 64.3 |
| heldout_remedy_tree_1 | 23d93ef | report | 5 | 0 | 2 / 3 | 0 / 3 | 0 / 3 | 53078 | 3578 | 39.3 |
| heldout_remedy_tree_2 | 23d93ef | report | 5 | 0 | 2 / 3 | 0 / 3 | 0 / 3 | 53154 | 4522 | 50.2 |
| heldout_remedy_tree_3 | 23d93ef | report | 5 | 0 | 2 / 3 | 0 / 3 | 0 / 3 | 53131 | 3583 | 37.6 |
| heldout_script_1 | 23d93ef | report | 5 | 0 | 12 / 12 | 3 / 3 | - | 51610 | 2777 | 29.2 |
| heldout_script_2 | 23d93ef | report | 5 | 0 | 12 / 12 | 3 / 3 | - | 51311 | 2735 | 33.3 |
| heldout_script_3 | 23d93ef | report | 5 | 0 | 12 / 12 | 3 / 3 | - | 51349 | 2790 | 32.7 |
| heldout_single_agent_1 | 23d93ef | report | 3 | 0 | - | 2 / 3 | 0 / 3 | 29734 | 1798 | 24.4 |
| heldout_single_agent_2 | 23d93ef | report | 5 | 0 | - | 2 / 3 | 0 / 3 | 52854 | 3508 | 42.5 |
| heldout_single_agent_3 | 23d93ef | report | 5 | 0 | - | 2 / 3 | 0 / 3 | 52911 | 4535 | 52.3 |
