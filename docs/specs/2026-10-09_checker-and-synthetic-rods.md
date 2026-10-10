# Spec: checker and synthetic rods, first slice with known truth

From: planning account. Date: 2026-10-09. Status: open.

## Review of build session 4
- The seven review conditions are met. Read: schema test, corrected MCP results, auditor view, launcher, orchestrator
- `python -m pytest -q tests` gives 16 passed on a second machine
- What exists is the agent loop. Every input the diagnostician has seen is made up. The next work gives it real inputs with known truth

## Goal
One slice that runs end to end with known truth: synthetic rod movie, tracker, checker, diagnostician, outcome scored against the truth. This is the Lab report 3 slice (due 13 Nov). Do it now so the later weeks go to baselines and real movies.

## Inputs
- `agents/` as merged
- Quantum Borland v1 in its own environment (`envs/qb.yml`)
- `docs/context/research_background.md` for the quantities and the mechanics relations
- `docs/context/project_summary.md` for the fault classes and the evaluation plan

## Work, in order

### 1. Housekeeping
- Delete the remote branch `wip/orchestrator`. Its code is on `main`; the only differences are the review commits
- Check: `git branch -r` lists `origin/main` only

### 2. Measurement record
- Define one record for one root over one window. It is what the tracker returns and what the checker reads: arc-length grid, velocity along the midline and on each flank, midline per frame, tip position, stage displacement from the log, frame times, pixel scale, tracking settings
- Take the fields from the tracker's real output. Do not invent a format the tracker cannot fill
- Write it up in `docs/context/measurement_record.md`
- Check: a test loads one synthetic record and one record made from tracker output

### 3. Synthetic rods
- Field level: analytic velocity fields written straight into a measurement record. Cases: rigid translation, rigid rotation, uniform strain, one growth zone (flexible logistic), bending with a set flank difference, width change. The truth is stored with the record
- Image level: a textured rod movie moved by the same fields, with a stage log. Small frames, short movies. The tracker runs on these
- Fault injectors at the image level for the development set only: `rigid_drift`, `displacement_exceeds_patch`, `midline_jitter`, `low_texture`, `width_change`
- Do not write injectors for `second_root`, `bad_stage_correction` or `fast_rotation`. See item 6
- Check: for each field-level case, integrated strain rate equals tip velocity to numerical tolerance. For a clean image-level rod, report the strain-rate error against the truth

### 4. Checker
- Three checks as plain functions of the measurement record: rigid-body invariance, tip-displacement closure against the stage log, plane-sections kinematics (flank difference = width x material curvature rate)
- Before coding, write the exact definition of each check and its cost in tracker runs in `docs/decisions.md`. If a check needs a second tracker run, say so
- Output per check: pass or fail, the value, the threshold, and where along the root it failed
- Thresholds: propose them from the field-level rods and clean image-level rods, with the basis. They are provisional until Andrew approves them
- No LLM. Check: a test fails if the checker module imports anything from `agents/`
- Check: every field-level case gives the expected pass or fail

### 5. Real executors
- `request_info`: each kind computed from the measurement record and the checker output
- `apply_remedy`: re-run the tracker with the changed setting, then re-check
- Add a table to `docs/decisions.md`: each remedy and setting, and the tracker parameter it changes. A remedy the tracker cannot carry out is removed from the list, not faked
- One runner interface with two forms: in-process for field-level rods, and a job on the machine that has the tracker. Machine details stay in `private/`
- Check: `python scripts/demo_slice.py` runs one image-level rod with one injected fault from start to finish. It prints the truth, the error before and after the remedy, and the outcome, and writes the trace to `results/`

### 6. Lists and freeze
- Development faults: the five in item 3. Proposed held-out faults: `second_root`, `bad_stage_correction`, `fast_rotation`, plus one fault not on the list, chosen later by the planning account. Pending Andrew's approval
- The fault, remedy and info lists, the diagnostician prompt and the checker thresholds are frozen together under a git tag `freeze-v1`, with a decisions entry. Andrew approves the freeze
- Held-out injectors are written only after the tag. Nothing frozen changes after a held-out result is seen
- `step_limit` and `error` outcomes are scored as not reported, in their own category, not as `decline`

## Out of scope
- Dispatcher, auditor, baselines, real movies, the cluster
- Any run over all roots. The call-budget estimate comes with the dispatcher spec

## Stop and ask Andrew
- Any threshold, before it is used to score anything
- Any change to the fault, remedy or info lists
- Tracker runs on synthetic rods that would take more than a few hours in total

## Report back
- Log entries per the routine in `CLAUDE.md`, with a `Demo:` line for each item
- In `results/`: the field-level pass/fail table, the clean image-level error, the demo slice trace
- Note in the running log when this spec is done
