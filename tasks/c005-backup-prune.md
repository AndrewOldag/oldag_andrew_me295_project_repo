---
id: c005
title: Decide whether the backup may delete old copies on the lab server
lane: course
owner: Andrew
state: done
branch: none
created: 2026-10-16 18:05
last_update: 2026-10-16 18:15
blocker: none
done_marker: docs/decisions.md 2026-10-16 "never deletes anything on the lab server"
---

- Decided (Andrew, 2026-10-16): never. Pruning code removed from `scripts/ops/backup_vm.sh`; `tests/test_ops.py` fails if a server command in it deletes, moves or renames
- Also decided: no scheduled backup; `backup_vm.sh` is run by hand only
