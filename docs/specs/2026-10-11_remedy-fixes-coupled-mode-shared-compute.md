# Spec: remedy fixes, coupled tracking mode, shared-compute limits

From: planning account. Date: 2026-10-11. Status: open. Decisions by Andrew on 2026-10-11.

## Review of build session 7
- Read: running log, decisions, `results/2026-10-10_repair_criteria/` (README, parts A, B, C), `measure/preprocess.py`, `measure/score.py`, `scripts/synth/sweep.py`, `scripts/synth/repair_sweep.py`
- Parts A to C of `2026-10-10_repair-criteria.md` are done. The part A stop was correct
- `register_frames` adds about 1.1 px/h of closure residual to a clean rod. `smooth_midline` adds about 1 px/h (light) and 3 px/h (strong)
- Every tracker run so far is uncoupled (`--couple` is never passed)

## Decisions
- Both remedies are fixed. They are not kept as they are, and the thresholds do not move
- Tolerance approved: centre REGR RMS error at most 2.5 % of the rod's true peak REGR; flank-difference RMS error at most 0.5 %/h
- Sizes approved: `displacement_exceeds_patch` 2x6 and `width_change` 1/400. `low_texture` at contrast 0.03 is the decline case
- Coupled tracking is added as a run setting and the rods are run in both modes
- Coupled results may be committed to this repository
- All jobs on the shared tracker machine follow the limits in part 1

## Work, in order

### 1. Shared-compute limits
The tracker machine is shared with other people. These limits apply to every job this project starts there, now and later. Build them into `scripts/synth/sweep.py` and the sweep starters, not into a habit.

- Before a sweep starts, read and log: core count, the 1, 5 and 15 min load averages, available memory, free disk in the work directory, and this account's own running processes
- Start only if the 1 min load average is at most half the core count. If not, wait 15 min and try again, three times at most. Then stop and tell Andrew
- At most 4 worker processes, and never more than one eighth of the cores
- One thread per worker. Set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and `NUMEXPR_NUM_THREADS` to 1 in the worker environment, and set the OpenCV and PyTorch thread counts to 1 in `scripts/remote/qb_track.py`
- Lowest priority: start the sweep under `nice -n 19`, and `ionice -c 3` where it exists
- Between runs, read the load average again. Above three quarters of the core count: start no new run until it is back under half
- One sweep at a time. A lock file in the work directory; `start` refuses while a sweep is running
- A `stop` command that ends the sweep and its workers cleanly
- Time the first 10 runs and print the projected wall time. More than 2 h for one sweep, or more than 4 h for this spec in total: stop and ask Andrew
- Work directory at most 10 GB. Report its size before and after. If it would go over, stop and ask
- No GPU. No installs and no system changes there. Nothing is written outside the work and code directories
- End of sweep: `status` shows no process of the sweep left. Log the load average before and after, the peak number of workers and the wall time
- Check: run 8 clean runs under the new limits. Report the CPU share of one worker (it should be near one core), the time per run, and the load average before, during and after
- Log entries give numbers only. No machine name, account or path

### 2. Fix `smooth_midline`
- Cause: the smoothing over time pads both ends of the window with the end value. The tip moves steadily, so the padded ends pull the tip path short, and closure sees the shortfall
- Required property: a midline that moves at constant velocity, with no jitter, comes out unchanged
- One way: smooth over time in a tip-anchored frame (subtract the tip position of each frame, smooth the shape, add the tip back). Another: pad by linear extrapolation. Pick one and log it
- The spatial sigmas and the levels (`light`, `strong`) stay as they are
- Test: a jitter-free midline translating at 1.5 px per frame is unchanged to 0.01 px after `light` and after `strong`

### 3. Fix `register_frames`
- Likely cause, calculated by the planning account and not run: the registration band is 60 to 100 % of the tracked length, which is 240 to 400 px from the tip on these rods. The growth zone has not ended there. Tissue at 240 px moves 4.3 px/h and the band mean is 0.97 px/h. Registration removes that as if it were drift. From 80 to 100 % the band mean is 0.19 px/h
- First confirm the cause: on one clean rod, run the band at 0.6, 0.8 and 0.9 and report the closure value for each
- If confirmed, set the band so that it holds non-growing tissue only. Choose between a fixed fraction and a band taken from the measured strain-rate profile of the current record (for example, where it is under 5 % of its peak). The truth is never read
- If not confirmed, report what was found and stop
- Log the new definition in `docs/decisions.md`. This is a change to how a remedy is carried out, not to the remedy list
- Note for real movies: the non-growing tissue in frame is short. The band has to come from the record, not from a number that fits these rods

### 4. Uncoupled re-run
- Clean `growth_zone` and `bending`, 3 seeds, through `register_frames`, `smooth_midline` light and `smooth_midline` strong. Stop condition as in the earlier spec: a clean rod that fails an approved threshold after a remedy
- `rigid_drift` at the four sizes and `midline_jitter` at the four sizes, with the fixed remedies
- `low_texture` at contrast 0.2 and 0.25, unremedied and with `enlarge_patch` 1.5x and 2x
- About 150 tracker runs
- Report in the form of parts A and B of `results/2026-10-10_repair_criteria/`. Propose one size each for `rigid_drift`, `midline_jitter` and a repairable `low_texture`, under the criteria of the earlier spec. Do not adopt them

### 5. Tolerance
- Replace the absolute centre tolerance with the approved form. The peak comes from `truth_summary` for that rod
- Put both numbers in a config file, marked approved, with the date and basis. Used for scoring only. Never shown to an agent
- Recompute the labels in part C with it. Report any label that changes
- Test: the 2x6 rods and a clean rod, each just inside and just outside the tolerance

### 6. Coupled mode
- `couple` becomes a field of the run settings, passed to `qb_track.py --couple`, written into the record's settings and into the run tag, so that coupled and uncoupled outputs never share a file name
- It is a run setting. It is not a remedy and it is not on any list an agent can choose from
- First, time one clean rod coupled against uncoupled: run time and peak memory. If coupled is more than 5 times slower, stop and ask before the sweep
- Coupled runs, in this order:

  | Set | Rods | Runs, about |
  | :-- | :-- | --: |
  | Clean basis | the 15 clean rods behind the approved thresholds | 30 |
  | Remedies on clean rods | part A with the fixed remedies | 110 |
  | Faults | the part B sizes, plus the `low_texture` sizes of item 4, with the fitting remedy | 280 |
  | Rotation | `rigid_rotation` at 0.1, 0.03 and 0.01 degrees per frame | 18 |

- Report every table with coupled and uncoupled side by side: the three check values, centre and flank-difference error, runs failed, time per run
- Do not change or propose thresholds. State whether each clean coupled rod passes the approved ones. If one fails, stop and ask
- Results go in `results/` as usual
- The course report still makes no claim about which mode is better. These tables are data

### 7. Bent rods, both modes
- Part C of `2026-10-10_bent-rods-width-change-rotation.md` (`bend_continue`, `bend_reverse`), run uncoupled and coupled. About 24 runs
- Expected: all three checks pass in both cases, in both modes. Report the values

### 8. Diagnostician, part D of the earlier spec
- The prompt rules, the before-and-after check values and the roll back can be built now
- The diagnostician runs wait for Andrew's approval of the sizes from item 4

## Not decided
- Which mode the system uses on the real movies. Andrew decides from the tables of item 6. `couple` is part of what is frozen

## Stop and ask Andrew
- Any limit in part 1 that cannot be met
- A clean rod that fails an approved threshold after a fixed remedy, or in coupled mode
- The registration cause is not confirmed
- Fault sizes, before use
- Any change to the fault, remedy or info lists

## Report back
- One new folder under `results/`, with a README and the tables of items 4, 6 and 7
- The numbers of part 1 for every sweep
- Log entry per the routine in `CLAUDE.md`, with a `Demo:` line for each item
- Note in the running log when this spec is done
