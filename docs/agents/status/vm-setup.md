# vm-setup
Updated: 2026-10-16 18:24 (local)
Lane: course
Branch: wip/vm-setup
Last inbox item done: none (spec 2026-10-16 given in chat)
State: done
Now: items 1-3 of spec 2026-10-16 done, with Andrew's changes; stopped as the spec asks
Done since last update:
- Spec saved (08d7302); item 1 restore check passed, no mismatch; item 2 task board (00da4f4); item 3 heartbeat and resume rules (129b1a5)
- Andrew's changes (this commit): no server deletes in the backup; no scheduled backup (task unregistered, script by hand only); heartbeat task re-installed by Andrew with -S4U
- Old sibling worktrees removed (9), caches moved into the main checkout's staging/, auditor views rebuild and match
Needs Andrew:
- Delete when convenient: the `2026-10-16_test` backup folder on the server, and `_verify/` from the 2026-10-16 backup
- none else; merged into main by this session (Andrew, 2026-10-16)
