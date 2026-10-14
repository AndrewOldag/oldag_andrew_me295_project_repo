# Auditor v1 on the scored runs v1, 2026-10-13

Spec `docs/specs/2026-10-13_auditor-v1-real-frame-quality-labels.md`, Task A. Definition `docs/proposals/2026-10-13_auditor-v1.md` (99d70bd, before any auditor run). No tracker runs: all 160 final records read from the scored runs' caches.

## Files
- `views/<set>_<method>.json`: what an auditor sees per batch (batch table with robust z, run records)
- `id_map.json`: opaque run id -> scored-v1 run, for scoring only
- `rule/<set>_<method>.json`: rule auditor decisions and reasons
- `llm/<set>_<method>_<n>_trace.jsonl`, `_result.json`: LLM auditor runs (decisions, report text, tokens, call time, commit)
- `scores.md`: per batch and per run, both auditors
- Commands: `python scripts/synth/auditor_v1.py views | rule | llm --set S [--method M] [--repeat K] | eval`

## Runs
- 8 batches: 4 methods x (dev 25 runs, held-out 15 runs)
- Rule auditor: flags an accepted run on a failed final check or |robust z| > 3 (cutoff fixed, Andrew, 2026-10-14)
- LLM auditor: `claude-opus-5-5`, Claude Code 2.1.293, effort high, step limit 20 per batch
- Dev: 3 prompt rounds x 4 batches = 12 calls (of 40). Prompt changes per round in the proposal
- Held-out: prompt of aa8483a (system prompt sha256 prefix `2541926380a9e924` in all 74 held-out calls), 4 batches x 3 = 12 calls. 24 auditor calls in all (limit 52). One call = one auditor run on one batch
- All 24 LLM runs ended with `report`; 0 undecided accepted runs; 0 errors
- Dev round 1 runs record commit 8a01264 (a status-file commit made while they ran; code and prompt as 99d70bd)

## Held-out, accepted runs only
Cells: flagged / runs in the group. alt_repair: `second_root` runs that applied `use_width_free_ratio` and accepted a good centre (reported apart).

| Method | Accepted | Rule: false accepts | Rule: good reports | Rule: alt_repair | LLM: false accepts (3 runs) | LLM: good reports (3 runs) | LLM: alt_repair (3 runs) |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- |
| script | 15 | 12 / 12 | 3 / 3 | - | 12, 12, 12 / 12 | 3, 3, 3 / 3 | - |
| remedy_tree | 9 | 3 / 3 | 0 / 3 | 0 / 3 | 2, 2, 2 / 3 | 0, 0, 0 / 3 | 0, 0, 0 / 3 |
| diagnostician | 5 | - | 0 / 2 | 0 / 3 | - | 2, 0, 0 / 2 | 0, 0, 0 / 3 |
| single_agent | 6 | - | 2 / 3 | 0 / 3 | - | 2, 2, 2 / 3 | 0, 0, 0 / 3 |

- False accepts flagged, held-out total: rule 15 / 15; LLM 14 / 15 in each of 3 runs
- LLM miss: remedy tree `partial_occlusion` s1, all checks pass, profile shape like the batch, centre REGR peak 48.9 %/h against a batch median near 43 (z 6.7). Cleared in 3 of 3 runs, citing the round 2 prompt rule that a REGR peak unlike the batch with a normal shape is a faster root. The rule auditor flags it on the z alone
- Good reports flagged, held-out total: rule 5 / 11; LLM 7, 5, 5 / 11. Script good reports fail a final check and are flagged by both
- alt_repair: flagged by neither auditor (0 / 9 rule; 0 / 9 in each LLM run)

## Dev, accepted runs only

| Method | Accepted | Rule: false accepts | Rule: good reports | LLM round 1 | LLM round 2 | LLM round 3 |
| :-- | --: | :-- | :-- | :-- | :-- | :-- |
| script | 25 | 10 / 10 | 15 / 15 | 10 / 10, 15 / 15 | 10 / 10, 15 / 15 | 10 / 10, 15 / 15 |
| remedy_tree | 14 | - | 6 / 14 | 4 / 14 | 0 / 14 | 0 / 14 |
| diagnostician | 15 | - | 7 / 15 | 7 / 15 | 5 / 15 | 0 / 15 |
| single_agent | 6 | - | 0 / 6 | 5 / 6 | 0 / 6 | 5 / 6 |

LLM cells for the script: false accepts flagged, good reports flagged. Other methods have no dev false accepts; cells are good reports flagged.

## Tokens and call time (LLM auditor)

| Set | Runs | Steps | Tokens in (mean) | Tokens out | Call time, s (mean) |
| :-- | --: | --: | :-- | --: | :-- |
| dev | 12 | 66 | 962651 (80221) | 51805 | 583.1 (48.6) |
| held-out | 12 | 74 | 817915 (68160) | 46710 | 539.9 (45.0) |

Per run in `scores.md`.

## Known limits
- On dev only the script batch has false accepts (10); on held-out, script 12 and remedy tree 3. The false-accept rates rest on 25 runs, 22 of them from the script, whose false accepts all fail a final check
- Synthetic rods in one batch are near-identical, so batch MADs are small (dev centre REGR peak MAD 0.27 %/h). The rule's false flags on dev (tree 6, diagnostician 7) are the `displacement_exceeds_patch` rods, which grow twice as fast by design, and runs with small differences in width-free ratio or flank-difference position
- The prompt rule that removed those dev false flags (round 2) is the cause of the one held-out LLM miss
- The view has no flank-spacing rate: width-change runs under the width-free ratio were flagged in some dev runs and cleared in others (single-agent batch)
- Control vs stressed comparison not done (synthetic batches have no condition)
