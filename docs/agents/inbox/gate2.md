# Inbox: gate2

1. Clone this repo to `~/coord-gate2/` if not there; create branch `status/gate2` from `main`. Read `docs/agents/README.md`. Write your first status: what of your task (prompt 8 in the planning account's parallel-agents list) is done, running or blocked, as file names, counts and pass or fail only. Push it. Then continue your task
2. Standing rule: never delete, move or rename anything on the lab server (`CLAUDE.md`). If your task's steps need it, stop and put it under Needs Andrew
3. Order (planning, 2026-10-14): finish the code change and the synthetic validation first (your task, sections 2 and 4 of the plan). Post status when validation is done, pass or fail, counts only
4. Full run (Andrew approved, 2026-10-14), after item 3:
   - Starts on its own if the uncoupled pipeline passes validation. Fails: stop, Needs Andrew
   - Settings: uncoupled. Part 3: report the ratio with both the root width and the measured flank-line distance; name the one closer to truth in validation as primary
   - Runs on the lab server, where the data is. No further pulls to the VM. Code synced to its own folder on the server, as the course sweeps do
   - Server limits: at most 4 single-thread workers, lowest priority (nice 19, ionice idle), 1-min load checked before each job and every 10 min; above half the cores, pause. One sweep at a time: check the course sweep lock (path in the course repo `private/`) before starting and between roots; do not start while it is held, and hold it while you run
   - Write only new files in a new output folder on the server. Never delete, move, rename or overwrite anything there
   - Pilot first: stimulated_1 alone. From it, estimate output size and wall time for all 7 roots. Over 50 GB of output or over 48 h of wall time: stop, Needs Andrew. Otherwise run the other 6 roots one at a time
   - Frame flags and event handling as the plan says
   - Report: a note "Gate 2 Results - <date>.md" in the vault folder next to the validation note, per root and pooled, in the plan's format. Status here: roots done, counts, pass or fail only. No result values in this repo
5. Answers (planning, 2026-10-14):
   - Where to run: validation on the VM. Install `scikit-image` and `tifffile` into the tracker env first; if the install fails, run validation on the server instead. Full run on the server as in item 4. Server work: read raw data, write only to a new gate2 work folder, nice 19 / ionice idle, shared limits, course sweep lock respected
   - Pushes from `~/coord-gate2` to `status/gate2` are allowed
   - The zero-growth phantom and delta-REGR choices: not received by the planning account. Put them under Needs Andrew in your status, one line each, and continue with your proposed choices in the meantime
6. Answers (Andrew, 2026-10-14):
   - Zero-growth phantom: rebuild it with the same construction on a frame from this dataset, and say so in the validation note and the report
   - Delta-REGR: score against the true value at the tracked flank lines. Add a dated clarification to the plan file
   - Drop contact: Andrew checks by eye. Write tip crops of the last 20 frames of interval 3 of stimulated_1, plus 3 evenly spaced earlier frames, as PNGs to `~/gate2/review/drop_contact/` on the VM, with the drop rim visible. Not in this repo. Status: the folder and the frame count under Needs Andrew. Do not exclude anything unless a later item says so; the pilot may proceed
   - Sweep lock left in place at exit: accepted
   - Plan section 6 comparisons: skip. Record in the plan as not run, by decision
   - Vault: write the notes to the gate2 folder on the VM; Andrew copies them
7. Andrew, 2026-10-14: drop contact checked by eye on the crops; no contact in any frame. No exclusion. Record it in the plan as a dated note. Validation keeps running on the VM; do not move or restart it
