---
id: c005
title: Decide whether the nightly backup may delete copies older than 7 nights on the lab server
lane: course
owner: Andrew
state: needs-input
branch: none
created: 2026-10-16 18:05
last_update: 2026-10-16 18:05
blocker: spec 2026-10-16 item 3 asks for it; CLAUDE.md forbids server deletes by a Claude-written script
done_marker: PRUNE set in private/backup.conf and CLAUDE.md updated, or the rule left as is in docs/decisions.md
---

- Built in `scripts/ops/backup_vm.sh`, off (`PRUNE=no`). It only touches dated folders that carry `.made-by-backup_vm`
- Nothing is due before 2026-10-24 (7 nightly copies from 2026-10-17)
