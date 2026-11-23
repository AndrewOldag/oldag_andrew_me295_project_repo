# Auditor check with planted errors: scores

Catch: the planted run flagged. False alarm: an unplanted run flagged. LLM auditor: 3 repeats, blind; rule auditor (|robust z| > 3.0 or a failed check) once. Batches of 8 good accepted freeze v4 runs.

## Catches per error kind

| Error kind | Batches | Rule | LLM r0 | LLM r1 | LLM r2 |
| :-- | --: | :-- | :-- | :-- | :-- |
| closure_relabelled | 4 | 4 / 4 | 4 / 4 | 4 / 4 | 4 / 4 |
| other_rod_track | 4 | 4 / 4 | 4 / 4 | 4 / 4 | 4 / 4 |
| wrong_unit | 4 | 4 / 4 | 0 / 4 | 0 / 4 | 0 / 4 |
| doubled_frame | 3 | 3 / 3 | 1 / 3 | 0 / 3 | 1 / 3 |
| all | 15 | 15 / 15 | 9 / 15 | 8 / 15 | 9 / 15 |

## False alarms (unplanted runs flagged / unplanted runs), by the batch's plant

| Batch plant | Batches | Rule | LLM r0 | LLM r1 | LLM r2 |
| :-- | --: | :-- | :-- | :-- | :-- |
| none | 15 | 27 / 120 | 13 / 120 | 13 / 120 | 21 / 120 |
| closure_relabelled | 4 | 7 / 28 | 0 / 28 | 0 / 28 | 0 / 28 |
| other_rod_track | 4 | 7 / 28 | 4 / 28 | 5 / 28 | 4 / 28 |
| wrong_unit | 4 | 7 / 28 | 3 / 28 | 2 / 28 | 0 / 28 |
| doubled_frame | 3 | 7 / 21 | 0 / 21 | 0 / 21 | 0 / 21 |
| all | 30 | 55 / 225 | 20 / 225 | 20 / 225 | 25 / 225 |

## Agreement across the 3 LLM repeats

- Runs decided in all 3 repeats: 240; unanimous 227 (0.95)
- Planted runs unanimous: 14 of 15
- Fleiss kappa (flag, clear, undecided): 0.836

## LLM auditor runs

- Runs 90; status report 90; steps 382; tokens in 3090685, out 307874; call time 3635 s
- Commits: ['203db47', '39da216', '3b1415a', '47e8eef', '510d287', '5874d5b', '5cbc54e', 'a8f58b7']; Claude Code ['2.1.310']; model ['claude-opus-5-5']

## Planted runs

| Batch | Row | Kind | Rule | LLM r0 | LLM r1 | LLM r2 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| b01 | v3_bend20 | doubled_frame | flag | clear | clear | clear |
| b04 | v3_still | other_rod_track | flag | flag | flag | flag |
| b05 | v3_growth_zone | other_rod_track | flag | flag | flag | flag |
| b06 | v3_still | other_rod_track | flag | flag | flag | flag |
| b09 | bad_stage_correction | closure_relabelled | flag | flag | flag | flag |
| b11 | v3_bend16 | doubled_frame | flag | clear | clear | clear |
| b13 | v3_bend16 | wrong_unit | flag | clear | clear | clear |
| b14 | v3_bend20 | other_rod_track | flag | flag | flag | flag |
| b17 | width_change | wrong_unit | flag | clear | clear | clear |
| b23 | bad_stage_correction | closure_relabelled | flag | flag | flag | flag |
| b24 | v3_growth_zone | wrong_unit | flag | clear | clear | clear |
| b25 | rigid_drift | doubled_frame | flag | flag | clear | flag |
| b26 | bad_stage_correction | closure_relabelled | flag | flag | flag | flag |
| b28 | bad_stage_correction | closure_relabelled | flag | flag | flag | flag |
| b30 | rigid_drift | wrong_unit | flag | clear | clear | clear |
