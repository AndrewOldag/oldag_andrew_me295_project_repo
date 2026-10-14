# Spec: per-branch remote code, held-out labels, single-agent baseline, first scored runs

From: planning account. Date: 2026-10-12. Status: open. Decisions by Andrew on 2026-10-12, on `docs/proposals/2026-10-12_freeze-v2.md`, `docs/proposals/2026-10-12_heldout-faults.md`, the baselines log entry and the Lab report 1 draft.

Start only after the coordinator has merged `wip/baselines`, `wip/lab-report-1`, `wip/freeze-v2` and then `heldout/faults` into `main`. Branch `wip/scored-v1` from that `main`.

## Decisions
- Freeze v2 approved as written in `docs/proposals/2026-10-12_freeze-v2.md`. Nothing in it is tuned after this point. Its one open item (real-movie `frame_quality` reference) stays open; it does not touch the synthetic scoring
- Held-out sizes approved as proposed: `second_root` 30 px, `fast_rotation` 2 deg/frame, `bad_stage_correction` 3 px, `flank_swap` 0.5, `partial_occlusion` 20 px
- `partial_occlusion`: a decline naming `low_texture` or `unknown` is correct. Any other name with a decline is a correct outcome with a wrong name
- Expected outcomes for `fast_rotation` and `bad_stage_correction` (accept after `register_frames`) are confirmed or replaced by the label sweep in item 3. Labels follow the repair criteria as before; no size changes
- Remote code: each branch syncs to its own code directory on the lab server. The one-sweep-at-a-time lock and the shared-machine limits stay as they are
- Root count: the manifest is current. 123 root positions, 102 kept (`manifest/root_manifest.csv`). The 118 in the project summary is the earlier inventory

## Limits
- Shared-machine limits as built. One sweep at a time
- Tracker runs: about 90 (item 3) plus whatever the scored runs need beyond the cache. More than 3 h of sweep wall time in total: stop and ask
- Agent runs: at most 80 in this spec (item 5 and 6). Token use is not a constraint; report it per run
- Model, Claude Code version and step limit as in freeze v2

## Work, in order

### 1. Per-branch remote code directory
- `scripts/synth/sweep.py`, `measure/runner.py` and any other script that syncs code to the lab server: sync into `<remote code base>/<branch name with / replaced by _>/` instead of the shared directory. The base path stays in `private/`
- The held-out sweep already uses its own directory; bring it onto the same rule
- Do not delete the old shared directory. List it in the log for Andrew
- Tests: two branch names give two different directories; a sync writes only inside its own directory; the lock is still one per machine
- Commit and push. Say in the log that the coordinator should merge this item to `main` early, so later branches pick it up

### 2. Tag the freeze
- Tag the current `main` commit `freeze-v2` and push the tag. The scored runs below record this tag

### 3. Held-out labels (tracker only, no agent)
- The five held-out faults at the approved sizes, seeds 0-2, through the same remedy settings and repair criteria used for the development faults. About 90 tracker runs
- Labels in the table format of `results/2026-10-11_remedy_fixes/item4_faults.md`, in `results/2026-10-12b_heldout_labels/`
- Where a label differs from the expected outcome in the held-out proposal, the label wins. Report it; do not change a size
- Commit the labels before any agent run on a held-out fault

### 4. Single-agent baseline
- Definition: the same model, prompt text, info kinds, remedies and step limit as the diagnostician, but it is not given the checker report. It must judge from the info answers alone. This measures what the deterministic checker adds
- Write the definition in `docs/proposals/2026-10-12_single-agent-baseline.md` and commit it before any run. If the existing orchestrator cannot withhold the checker report without other changes, stop and ask
- Tests: the baseline's first view contains no check values; it can request every info kind and remedy the diagnostician can

### 5. Scored runs, development faults
- Seeds 1-5 (`config/scoring_seeds.yaml`), five development faults at their frozen sizes
- Methods: fixed script, remedy tree, diagnostician, single agent. 25 runs each; the two LLM methods make 50 agent runs
- Every run records: freeze tag, commit, method, fault, seed, outcome, category, fault named, steps, remedies, roll backs, tokens in and out, call time
- No change to any prompt, threshold or tool between runs. A crash is fixed only if it is a harness bug that does not change what the agent sees; log it and re-run that run only

### 6. Scored runs, held-out faults
- Seeds 0-2, five held-out faults, same four methods. 15 runs each; 30 agent runs
- Same record as item 5

### 7. Results
- `results/2026-10-12b_scored_v1/`: one table per fault set (method x fault: correct outcomes, false accepts, unnecessary declines, terminal fault correct), totals per method, and steps, tokens and call time per method
- State results as measured. No reading of why a method did well or badly beyond what the traces show; that is for Andrew and the auditor later
- Lab report 1 draft: replace the root-count [ANDREW] mark with "123 root positions, 102 kept (manifest); the earlier inventory gave 118"

## Stop and ask Andrew
- Item 4 cannot withhold the checker report without wider changes
- More than 20 % of agent runs in item 5 or 6 end in a harness error
- More than 3 h of sweep wall time
- Any change to a frozen item
