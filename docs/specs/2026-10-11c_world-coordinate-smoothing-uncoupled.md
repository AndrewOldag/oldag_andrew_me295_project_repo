# Spec: smoothing in world coordinates, uncoupled system, remaining items of 11b

From: planning account. Date: 2026-10-11. Status: open. Decisions by Andrew on 2026-10-11, on the question of build session 9.

## Review of build session 9
- Read: running log, decisions, `results/2026-10-11b_padding_tolerance_coupling/` (README, `b1_smoothing.md`, `b4_coupling_weight.md`)
- The item 1 stop was correct. The cause is a coordinate error, not a tuning question: the midline is smoothed over time in image coordinates, where the stage steps make the tip path a sawtooth
- Item 4 is done. No coupling weight keeps the growth profile and also removes most of the noise on these rods. The loss at the peak grows with tip speed, and the flank-difference error on the bent rods grows fastest
- Shared-machine limits held: 324 runs, 11.5 min, 1 min load at most 6.22

## Decisions
- `smooth_midline` smooths over time in world coordinates. This is the final change to the remedy. Whatever the result, the remedy is not changed again
- The system is uncoupled. No further coupled runs are made in this project
- Andrew's reading of the coupled result: it may come from how the synthetic rods are generated. That question belongs to other work and is not pursued here

## Limits
- Shared-machine limits as built. About 160 tracker runs and 4 diagnostician runs. More than 1 h of wall time in total: stop and ask

## Work, in order

### 1. `smooth_midline` in world coordinates
- Add the stage log to the midline, smooth over time, subtract the stage log. Fitted-line padding, sigmas and levels unchanged. New run tag
- Tests:
  - the two existing ones still pass
  - new: a jitter-free midline that translates steadily in the world while the stage steps every few frames (a sawtooth in image coordinates) is unchanged to 0.01 px at both levels
- Re-run clean `growth_zone` and `bending`, 3 seeds, light and strong; and `midline_jitter` at 0.5, 1, 2 and 3 px, light and strong. About 72 tracker runs
- Then, with no further change to the remedy:
  - If a clean rod still fails an approved threshold after `strong`: the `strong` level is withdrawn from the remedy settings and `light` stays. Log it as a list change decided here
  - If a clean rod fails after `light`: stop and ask Andrew
  - If a `midline_jitter` size meets the criteria of the 2026-10-10 spec: propose it. Do not adopt it
  - If none does: `midline_jitter` is not repairable. It keeps its present size of 3 px and decline is its correct outcome, as for `low_texture` at 0.03. No approval needed for that
- Report as in `b1_smoothing.md`

### 2. Items 2 and 3 of `2026-10-11b_padding-flank-tolerance-coupling-weight.md`
- As written there: the flank-difference tolerance from the basis rule with the bent rods in the clean set (about 84 runs), then one diagnostician run each for the four faults with an approved size
- In item 2, use the smoothing levels that item 1 leaves on the list
- If item 1 ends with `midline_jitter` not repairable at 3 px, add a fifth diagnostician run for it. At most 5 runs here

### 3. Uncoupled system
- `couple` stays a recorded run setting, false everywhere. `--couple-lambda` and `--couple-mu` stay in `qb_track.py`; nothing calls them
- README: one line saying the system runs uncoupled and where the coupled tables are
- The coupled tables in `results/` stay as data

### 4. Freeze list, for approval
- Do not tag. Write `docs/proposals/2026-10-11_freeze-v1.md`: every item that the freeze fixes, with its value and the decision that set it
  - fault list and sizes, with the label of each rod
  - remedy list and settings
  - info kinds
  - diagnostician prompt (by commit)
  - checker thresholds
  - scoring tolerance
  - run settings: uncoupled, disk radius, spacing, stride, step limit
- Mark anything still open, with whom it waits on
- Andrew approves the freeze from that file

## Stop and ask Andrew
- A clean rod fails an approved threshold after `light` smoothing, or after any other remedy
- The basis rule gives a flank tolerance other than 0.75 %/h, or a centre error above 2.5 % of the peak
- A proposed fault size, before use
- Any change to the fault, remedy or info lists other than the one named in item 1

## Report back
- One new folder under `results/`, with a README and a table per item, and the diagnostician traces
- Log entry per the routine in `CLAUDE.md`, with a `Demo:` line for each item
- Note in the running log when this spec and 11b are done
