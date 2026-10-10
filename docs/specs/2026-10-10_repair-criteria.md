# Spec: what counts as repaired

From: planning account. Date: 2026-10-10. Status: open. Approach agreed by Andrew.

## Review of build session 6
- Read: running log, decisions, `results/2026-10-10_demo_slice/` (README, sweep, trace, summary), `agents/executors.py`, `measure/remedies.py`, `measure/score.py`, the diagnostician prompt
- Item 5 of the 2026-10-09 spec is built and the slice runs end to end
- Sweep, one seed, no agent: every remedy moves the failing check the right way; none reaches three passes
- Demo: the diagnostician named the fault and halved the stride (closure 51.4 to 4.37 px/h). Two checks still failed. It then looked for a second fault, named `rigid_drift`, and registered the frames. Error went from 3.87 to 5.51 %/h. Outcome `step_limit`
- Likely cause: the prompt rule "Do not repeat a remedy that has already failed for the same fault". The first halving left checks failing, so a second halving was ruled out
- Commit f3afee9 went in with a failing test. Commit only after the tests pass

## Decision
- The approved thresholds do not move to fit the remedies
- Instead: measure what each remedy does to a clean rod, size the faults so that a correct remedy can reach a pass, let the diagnostician repeat a remedy that is working, and state the correct outcome for every rod before any agent is scored

## Work, in order

### A. Clean rods through each remedy
- No agent. Clean `growth_zone` and `bending`, 3 seeds each, each tracked twice as before
- One run per setting, applied alone to the clean rod: stride 2; patch 1.5x; patch 2x; register_frames; smooth_midline light; smooth_midline strong; crop_or_mask, both modes. Plus the unchanged run
- Report per setting: the three check values (median, min, max), centre and flank-difference error against the truth, and whether every clean run still passes the approved thresholds
- Window length: every run in this spec uses a 1 h window, as the clean basis does. If a fault needs a longer movie, add clean runs of the same length and stride and report them here
- About 110 tracker runs

### B. Fault sizes
- No agent. For `rigid_drift`, `displacement_exceeds_patch` and `midline_jitter`, sweep the injected size and apply the fitting remedy by hand, 3 seeds
- Propose one size per fault that meets all of these:
  - unremedied, at least one check fails on 3 of 3 seeds
  - after one or two steps of the fitting remedy, all three checks pass on at least 2 of 3 seeds
  - the remedied window is 1 h
- For `displacement_exceeds_patch` the rod's tip speed or the patch radius may change to keep the 1 h window. State which
- `low_texture`: keep the present size. Also look for a milder size that `enlarge_patch` repairs under the same criteria. If one exists, propose it as a second size, so that one low-texture rod is repairable and one is not
- `width_change`: do not change it. See "Open with Andrew"
- If no size of a fault meets the criteria, report that. Do not change a remedy to make it fit
- Report a table per fault: size, check values before and after, error before and after, seeds passing
- Do not adopt the sizes. Andrew approves them

### C. Correct outcome per rod
- A reported measurement is good when its error against the truth is within a tolerance. Propose the tolerance from part A: centre strain-rate RMS error and flank-difference RMS error, each set above the largest clean value under any remedy that keeps clean rods passing. Andrew approves it. It is used only for scoring and is never shown to an agent
- Each rod gets a label from the no-agent sweeps, written before any agent runs on it:
  - `repairable`: some sequence of at most two remedy steps gives three passes and a good measurement. Record the sequence
  - `not repairable`: none does
- Outcome categories, in `measure/score.py`:

  | Outcome | Rod label | Category |
  | :-- | :-- | :-- |
  | accept | measurement good | good report |
  | accept | measurement not good | false accept |
  | decline | not repairable | correct decline |
  | decline | repairable | unnecessary decline |
  | step_limit or error | any | not reported |

- Diagnosis is scored separately: the fault named in the last `apply_remedy` or `decline`, against the injected fault
- `low_texture` at the present size is expected to be `not repairable`. The correct outcome is decline. Confirm from the sweep
- Check: a test covers each row of the table with a made-up outcome

### D. Diagnostician
- Replace the rule "Do not repeat a remedy that has already failed for the same fault" with these two:
  - A remedy that lowered a failing check may be applied again or at its next setting
  - A remedy that lowered no failing check is not applied again
- After `apply_remedy`, the result shows each check's value before and after
- Roll back: if a remedy makes no failing check pass and lowers no failing check by at least a quarter, the orchestrator restores the settings from before it and says so in the result. The step still counts. Log this in `docs/decisions.md`
- No other prompt change. The line on width change stays as it is for now
- `step_limit` stays at 8. Report steps used. Do not change it in this spec
- After Andrew approves part B: run `scripts/demo_slice.py` once per development fault at the approved sizes, seed 0. At most 8 diagnostician runs in this spec. Report the outcome category, the named fault, steps and tokens for each

## Order with other specs
- This spec first. Then part C (bent rods) of `2026-10-10_bent-rods-width-change-rotation.md`. Then item 6 (freeze) of the 2026-10-09 spec
- Fault sizes, the tolerance, the outcome table and the prompt are all part of what is frozen

## Open with Andrew
Do not act on these.
- `switch_midline_source`: remove from the remedy list or not
- `use_width_free_ratio` and the correct outcome for `width_change`. The centre strain rate is unaffected by the width change (error 0.40 %/h in the sweep); only the flank difference is. Declining would discard a good elongation measurement, and width change is expected under osmotic treatment. The remedy may need to be a change in what is reported, not a tracker setting

## Stop and ask Andrew
- A clean rod fails an approved threshold after a remedy (part A)
- Any fault size, and the tolerance, before use
- Any change to the fault, remedy or info lists
- Tracker runs that would take more than two hours in total

## Report back
- One new folder under `results/`, with a table for each of A, B and C and the traces from D
- Log entry per the routine in `CLAUDE.md`, with a `Demo:` line for each part
- Note in the running log when this spec is done
