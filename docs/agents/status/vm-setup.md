# vm-setup
Updated: 2026-10-16 18:05 (local)
Lane: course
Branch: wip/vm-setup
Last inbox item done: none (spec 2026-10-16 given in chat)
State: ready to merge
Now: items 1-3 of spec 2026-10-16 done; stopped as the spec asks
Done since last update:
- Spec saved (08d7302)
- Item 1 restore check passed: no hash or checksum mismatch; lit-review folder missing (was missing before the wipe)
- Item 2 task board (00da4f4)
- Item 3 heartbeat, resume rules, nightly backup; test backup verified on the server (this commit)
Needs Andrew:
- Backup pruning: the spec asks the script to delete copies older than 7 nights on the lab server; CLAUDE.md forbids server deletes by a Claude-written script. Built but off (PRUNE=no). Say yes to turn it on and add the exception to CLAUDE.md
- Scheduled tasks run only while you are logged on (this session is not elevated). For always-on, run `install_schedule.ps1 -S4U` from an elevated shell
- Delete when convenient: the `2026-10-16_test` backup folder on the server, and `_verify/` from the 2026-10-16 backup
