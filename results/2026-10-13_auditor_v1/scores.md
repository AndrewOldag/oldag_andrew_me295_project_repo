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
