# Task board

Source of truth for who is doing what (spec 2026-10-16, item 2). Agent View shows live state only and does not survive a wipe.

## Files
- One file per course-lane task: `tasks/<id>-<name>.md`. Ids `c001`, `c002`, ... Research-lane tasks use the same format in the research task folder, outside every git repo (location in `private/board.conf`). Research ids `r001`, ...
- Each session updates only its own task file, on its own branch: at start, at each commit, and at stop
- On start, a session reads its task file first

## Front matter
```
---
id: c001
title: one line
lane: course
owner: <session name> | Andrew
state: queued | working | needs-input | review | done | blocked | interrupted
branch: wip/<name> | main | none
created: YYYY-MM-DD HH:MM
last_update: YYYY-MM-DD HH:MM
blocker: none | one line
done_marker: file or check that shows the task is done
---
```
- Times are VM local time
- A task in state `working` with `last_update` older than 30 min is shown as stale
- On restart, the coordinator sets `working` tasks with no live session to `interrupted` and re-dispatches them
- Below the front matter: parts, each marked done when finished, so a restarted task skips them

## Board
- `python scripts/board.py` prints one table (id, lane, owner, state, branch, last_update, blocker) from both folders
- `python scripts/board.py --html` also writes the local page (location in `private/board.conf`). The page is never written inside a git repo
