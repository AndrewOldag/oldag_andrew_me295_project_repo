# Held-out compound and novel faults (task c029), 2026-11-18 to 2026-11-22

Spec `docs/specs/2026-11-18_lab-report-4.md`, section D. Proposal `docs/proposals/2026-11-18_heldout-compound.md` (fa459b7), committed before any run. Labels committed before any method run (a9445d2).

## Files
- `sizing.md`, `sizing.json`: novel-fault sizes (focus_drift 3 px, illumination_flicker 0.1)
- `labels.md`, `labels.json`: labels of the 24 rods, every state of the tracker-only sweep
- `flicker.md`: why illumination_flicker 0.1 labels decline (inbox item 10, step 1)
- `cluster_equivalence.json`: cluster vs VM tracks of 2 rods before any cluster label run
- `table_metrics.md`, `metrics.json`, `scores.json`: metrics, per row, cost, per run
- `runs/`: one summary and one trace per run; `runs/usage_limit/`: 9 runs ended by the account session limit (not scored); `runs/deterministic.jsonl`: second runs of the rule methods
- `supplement/`: c029b, a separate set (inbox item 10). Reported beside c029, never merged into its numbers

## Commands
- `python scripts/synth/heldout_compound.py render`, `compound_queue.py submit|fetch`, `heldout_compound.py labels`
- `python scripts/synth/heldout_compound.py rules`; `agents --method diagnostician|single_agent --repeat 0|1|2`
- `python scripts/synth/heldout_compound.py eval` writes the tables

## Set
- 24 rods, v3_growth_zone, seeds 40-43, each with its rigidly moved copy. 4 compound faults (drift + low texture, second root + occlusion, drift + midline jitter, low texture + displacement above the patch) and 2 novel single faults (focus_drift 3 px, illumination_flicker 0.1)
- Labels: accept_repaired 4 (focus_drift, all seeds; enlarge_patch/1.5x, alone or with use_width_free_ratio), decline 20, accept_clean 0. All-decline scores 20 of 24
- Expected classes (proposal) differ from the label on 8 rods: focus_drift (expected decline) and illumination_flicker (expected accept_clean)
- Tracker runs: 1,365 outputs cached (VM before spec 2026-11-20, cluster after). Cluster vs VM equivalence: largest difference 3.5e-7 px (limit 1e-6). 5 runs failed in every cluster submit (tracker errors); they count as failing states
- Open with the TAs (spec D5): whether labels from a tracker-only sweep are acceptable for compound faults. These labels are used as they are

## Metrics (mean over 3 repeats for the LLM methods; range in brackets)

| Method | Runs | Balanced accuracy | Acc. accept_repaired | Acc. decline | Overall | False accepts per repeat | Not reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | --: |
| script | 24 | 0.00 | 0.00 | 0.00 | 0.00 | 20.0 | 0 |
| remedy_tree | 24 | 0.70 | 0.50 | 0.90 | 0.83 | 4.0 | 0 |
| diagnostician | 72 | 0.47 (0.42-0.55) | 0.08 (0.00-0.25) | 0.85 | 0.72 (0.71-0.75) | 0.7 (0.0-1.0) | 12 |
| single_agent | 72 | 0.06 (0.03-0.10) | 0.00 | 0.12 (0.05-0.20) | 0.10 (0.04-0.17) | 5.3 (4.0-7.0) | 49 |
| all_decline | 24 | 0.50 | 0.00 | 1.00 | 0.83 | 0.0 | 0 |
| all_accept | 24 | 0.00 | 0.00 | 0.00 | 0.00 | 20.0 | 0 |

- No accept_clean rods, so balanced accuracy is over 2 classes
- Not reported: the run ended at the step limit (diagnostician 12, single agent 49)
- The set does not separate the methods: all-decline (0.83 overall) equals the remedy tree and beats the diagnostician on overall accuracy; only the 4 focus_drift rods test repair. c029b adds rods a single remedy can repair

## Runs that hit a state not cached (inbox item 12)
- 3 LLM runs asked for a remedy state not in the cache; the agent got a "Missing" tool error and finished the run. They are kept and scored as written; the table above includes them
- diagnostician drift_jitter s40 repeat 1: correct decline; single agent low_texture_fast s42 repeat 1 and s43 repeat 0: step limit (not reported)
- Without them (same code, `measure/metrics.py`):

| Method | Runs | Balanced accuracy | Acc. accept_repaired | Acc. decline | Overall | False accepts per repeat | Not reported |
| :-- | --: | :-- | :-- | :-- | :-- | :-- | --: |
| diagnostician | 71 | 0.47 (0.42-0.55) | 0.08 (0.00-0.25) | 0.85 (0.84-0.85) | 0.72 (0.70-0.75) | 0.7 (0.0-1.0) | 12 |
| single_agent | 70 | 0.06 (0.03-0.11) | 0.00 | 0.12 (0.05-0.21) | 0.10 (0.04-0.17) | 5.3 (4.0-7.0) | 47 |

- No conclusion above changes. c029b sets such runs aside (`supplement/runs/missing_state/`) and redoes them once the state is fetched

## Per row (correct runs / runs)

| Row | Label | script | remedy_tree | diagnostician | single_agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| drift_low_texture | decline | 0 / 4 | 4 / 4 | 12 / 12 | 0 / 12 |
| second_root_occlusion | decline | 0 / 4 | 2 / 4 | 8 / 12 | 1 / 12 |
| drift_jitter | decline | 0 / 4 | 4 / 4 | 12 / 12 | 0 / 12 |
| low_texture_fast | decline | 0 / 4 | 4 / 4 | 11 / 12 | 5 / 12 |
| focus_drift | accept_repaired | 0 / 4 | 2 / 4 | 1 / 12 | 0 / 12 |
| illumination_flicker | decline | 0 / 4 | 4 / 4 | 8 / 12 | 1 / 12 |

## Agreement across repeats

| Method | Unanimous rods | Fleiss kappa |
| :-- | :-- | :-- |
| diagnostician | 15 of 24 | 0.460 |
| single_agent | 15 of 24 | 0.448 |

- Rule methods: second runs from the cache identical on 48 of 48

## Cost (all repeats)
- Agent runs: 144 scored (72 per LLM method) plus 9 ended by the session limit; 153 of the cap of 450
- `claude -p` calls (agent steps): diagnostician 499, single agent 532. Tokens in / out: diagnostician 2.46 M / 0.29 M; single agent 2.48 M / 0.29 M. Call time 3,095 s and 3,160 s
- Remedy tree: 113 steps, no LLM

## Flicker (inbox item 10, step 1; detail in `flicker.md`)
illumination_flicker 0.1 was expected to label accept_clean and labels decline on all four seeds. The unremedied run fails rigid-body invariance and plane sections on 4 of 4 and tip closure on 3 of 4; its REGR error is 6.8-9.9 %/h against a limit of 1.35. The generator applies the fault as defined: one gain per frame on the whole image, geometry unchanged, no saturation; consecutive analysis frames differ in gain by 7-13 % (median). The cause is the tracker: its point matcher is affine Lucas-Kanade on raw intensity with no gain or offset term, so a frame-to-frame gain change is fitted as displacement. The proposal's premise of a normalised correlation was wrong for the strain-rate tracker. Not a generator bug; c029's rods and labels are unchanged.

## Run record
- Rule methods 2026-11-22 17:15 (47 of 48; the paused remedy-tree run on drift_jitter s41 needed a 3-step state, fetched from the cluster and redone from step 0 at 21:15)
- LLM methods 17:15-21:10, one run at a time on the VM. Stopped at 18:34 by the account session limit (9 runs set aside), restarted 20:06; stopped at 20:14 by an uncommitted tracked file and restarted 20:18
- Runs record commits 960cf04 to 043f8eb. Across them only `measure/render_compound.py` changed (new c029b entries; c029 entries unchanged, no render during method runs); agents, checker, prompts and config unchanged
- Option A integrity gate at every remedy step (`Slice.apply_remedy`) for the tree and the diagnostician; not applied to labels (inbox item 7)

## Known limits
- 20 of 24 rods decline: the set measures declining, not repair
- Labels come from a tracker-only sweep of states of one or two steps; a 3-step repair is not a label state
- 2 expected classes were wrong (focus_drift, illumination_flicker); the labels, not the expectations, are scored
