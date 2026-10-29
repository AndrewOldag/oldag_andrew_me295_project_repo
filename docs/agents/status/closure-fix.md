# closure-fix
Updated: 2026-10-25 19:20 (local)
Lane: course
Branch: wip/closure-fix-wo
Last inbox item done: 3
State: ready to merge
Now: item 3 done by the planning account (Andrew, 2026-10-25 18:57: "run the closure fix"); no session ran. Merge wip/closure-fix-wo
Done since last update:
- `scripts/remote/real_moved.py` write once: copy folders written in place under their final name, `<dir>.started` before the first frame, `<dir>.ok` after the last; no `.part`, no `os.rename`. A folder with `.started` and no `.ok` is refused (stopped copy). A folder with neither marker is treated as a complete copy from the rename-based version. Midline files refused if they exist
- `measure/real_runner.py` `ensure_moved`: reuses a copy only if it is complete by the same rule
- Tests: `tests/test_real_slice.py` 2 new. Full suite 310 passed, 3 skipped (planning account's environment, no cv2)
- Decisions entry (rules-2). Log entry in `docs/running_log_pending/closure-fix.md`
Needs Andrew:
- none. Hosts pick up the change when a runner next syncs its code copy; copies already on the lab server are left as they are
