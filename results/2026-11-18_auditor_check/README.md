# Auditor check with planted errors (task c030)

Spec `docs/specs/2026-11-18_lab-report-4.md`, section E. Proposal `docs/proposals/2026-11-18_auditor-check.md`, committed with the plant list before any auditor run (6150856). VM only, no tracker runs.

## Setup
- 30 batches of 8 good, accepted freeze v4 runs, each batch from one row of the v4 set (as the windows of one root); seed 1118
- One planted error in 15 batches: `closure_relabelled` 4, `other_rod_track` 4, `wrong_unit` 4, `doubled_frame` 3 (definitions in the proposal, section 2)
- LLM auditor: `audit/llm.py`, prompt `agents/prompts/auditor.md` (unchanged, as in the integrated run), `claude-opus-5-5`, Claude Code 2.1.310, blind (batch view only, opaque run ids, no tools). 3 repeats
- Rule auditor (`audit/rule.py`: a failed check or |robust z| > 3) on the same views, once
- Commands: `python scripts/synth/auditor_check.py plan` (once), `views`, `rule`, `llm --repeat K`, `score` (same as `eval`)

## Files
- `batches.json`, `plants.json`, `run_map.json` (opaque id -> run or plant, for scoring only)
- `views/bNN.json`: what the auditor saw; `rule/bNN.json`; `llm/bNN_rK_result.json` and `_trace.jsonl`
- `scores.md`, `scores.json`: catches, false alarms, agreement, per planted run

## Runs
- 90 LLM auditor runs (cap 150), all ended with a report; 382 `claude -p` calls (steps); tokens in 3,090,685, out 307,874; call time 3,635 s
- 1 further run ended on the account usage limit (b24, repeat 1, 2026-11-20 15:09): set aside in `llm/usage_limit/`, rerun, not scored
- Runs record 8 commits (status and result commits made while the runs went on); auditor code and prompt unchanged across them

## Catches (planted run flagged / planted runs)

| Error kind | Batches | Rule | LLM r0 | LLM r1 | LLM r2 |
| :-- | --: | :-- | :-- | :-- | :-- |
| closure_relabelled | 4 | 4 / 4 | 4 / 4 | 4 / 4 | 4 / 4 |
| other_rod_track | 4 | 4 / 4 | 4 / 4 | 4 / 4 | 4 / 4 |
| wrong_unit | 4 | 4 / 4 | 0 / 4 | 0 / 4 | 0 / 4 |
| doubled_frame | 3 | 3 / 3 | 1 / 3 | 0 / 3 | 1 / 3 |
| all | 15 | 15 / 15 | 9 / 15 | 8 / 15 | 9 / 15 |

## False alarms (unplanted runs flagged / unplanted runs)

| Batches | Rule | LLM r0 | LLM r1 | LLM r2 |
| :-- | :-- | :-- | :-- | :-- |
| 15 with no plant | 27 / 120 | 13 / 120 | 13 / 120 | 21 / 120 |
| 15 with a plant | 28 / 105 | 7 / 105 | 7 / 105 | 4 / 105 |
| all 30 | 55 / 225 | 20 / 225 | 20 / 225 | 25 / 225 |

## Agreement across the 3 LLM repeats
- 240 runs decided in all 3 repeats; 227 unanimous (0.95); Fleiss kappa 0.836 (flag, clear, undecided)
- Planted runs: 14 of 15 unanimous. The one split: b25 (rigid_drift, doubled_frame) flagged in r0 and r2, cleared in r1

## Findings
- `closure_relabelled`: the LLM auditor flags 12 of 12, reason `check_failed_but_accepted`, evidence closure: it reads the value above its threshold despite `passed: true`. The rule auditor reads only `passed`; it flags these runs on a summary outlier (centre REGR peak, growth-zone length or flank-difference position), not on the relabel
- `other_rod_track`: both flag 4 of 4 (12 of 12 LLM runs)
- `wrong_unit` (velocities x 2.105): the LLM auditor clears 12 of 12. Example b13 r0: centre REGR peak 111.61 %/h against a batch median near 53 (robust z 3,952); the report calls it "about 2.1x the batch" and clears it because the peak position and profile shape match the batch. b24 r0: "This looks like a faster root with the same profile shape, not a fault." This is the prompt rule found in auditor v1 (a REGR peak unlike the batch with a normal shape is a faster root), which caused auditor v1's one held-out miss. The rule auditor flags 4 of 4 on z
- `doubled_frame`: checks pass on the doubled records; the centre REGR peak drops about 2.5 % (z -46 to -90, batch MAD 0.01-0.02 %/h). LLM 2 of 9 runs flag it (b25 only); the reports call the others a slightly slower root. The rule flags 3 of 3 on z
- False alarms: rule 55 of 225 unplanted runs, LLM 20-25. In near-identical synthetic batches the MAD is 0.01-0.3 %/h, so the rule's z cutoff flags differences of 0.04 %/h or 11 um; the LLM reports name these as small absolute differences and clear most of them

## Known limits
- Synthetic batches of one row are near-identical, so robust z is extremely sensitive. The rule's 15 of 15 catches rest on that: its false-alarm rate is 0.24. On real batches (more spread) z is less sensitive
- `wrong_unit` scales the reported fields only; the checks are those computed before the scaling. A unit error made before the checker would also change the check values
- `doubled_frame` with the last frame dropped changes window means by about 1/40; whether it should be caught from summaries alone is open
- 15 planted runs in all: per-kind counts are 3-4 per repeat
- No prompt or threshold was changed for this check (spec limits). The `wrong_unit` miss is reported, not fixed
