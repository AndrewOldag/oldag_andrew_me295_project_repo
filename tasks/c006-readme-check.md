---
id: c006
title: Check README setup steps 1-6 from a fresh clone (Lab report 1 "README checked on")
lane: course
owner: readme-check
state: done
branch: wip/readme-check
created: 2026-10-16 18:40
last_update: 2026-10-17 16:00
blocker: none
done_marker: running log entry "session readme-check" with steps 1-6 results and test count
---

Instructions: `docs/agents/inbox/readme-check.md`, item 1.

## Parts
- [x] df checked
- [x] Fresh clone of origin/main (commit recorded)
- [x] Step 1 Miniforge version recorded
- [x] Step 2 env me295-readme created
- [x] Step 3 Claude Code version matches config/models.yaml (checked: does not match, 2.1.302 vs 2.1.293)
- [x] Step 4 check_cli.py (first run: FAIL on version gate, no agent call; after re-pin to 2.1.302: OK)
- [x] Step 5 full test suite
- [x] Step 6 hook install without blocklist
- [x] README text fixes, if any, on wip/readme-check (251383d)
- [x] Log entry and status ready to merge
- [x] Fresh clone and me295-readme env removed
