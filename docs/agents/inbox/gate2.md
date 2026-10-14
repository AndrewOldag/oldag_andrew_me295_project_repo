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
