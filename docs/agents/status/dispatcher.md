# dispatcher
Updated: 2026-11-23 22:30 (local)
Lane: course
Branch: wip/audit-fixes
Last inbox item done: 61
State: waiting on Andrew
Now: inbox 62 part 1 done (ad577fe); part 2 (archive copy) waits for the archive folder path: none is listed in private/
Done since last update:
- Inbox 62 part 1: `scripts/mask_bio.py` reviewed exemption list `EXEMPT` (file, exact phrase, decision date); one entry, the flank-difference range in docs/proposals/2026-10-23_real-midline-smoothing.md, unmasked from the pre-mask text; tests: exemption matches exactly one place, covers only its phrase in its file; grep test still covers everything else; suite 508 passed, 3 skipped (ad577fe)
- Inbox 62 part 2 prepared on the VM (git-ignored staging/archive_inbox62/, nothing sent): 4 tars, md5:
  - real_subset_035e8fc.tar (git archive of results/2026-10-25_real_subset/ at 035e8fc, 21 entries) 8f8d1f269da5d3ab90f0f3c3be6a6087
  - real_subset_2ea98bd.tar (same at 2ea98bd, 9 entries) 1c7c1671577ca40d2b8302f8fa801e3a
  - real_subset_97f2eb0.tar (same at 97f2eb0, 14 entries) fdcffd795d2be52b0bdc174ca6f6f0c5
  - real_subset_runs_vm.tar (VM staging/c019/real_subset_runs/, 16 entries) cfc5c6b7c87bc01697283e383949a8ac
Needs Andrew:
- Inbox 62 part 2: no private archive folder on the lab server is listed in private/ (only the VM backup folder, which is not named as your archive). Add the folder to private/paths.md, then `check github`: I copy the 4 tars there over the existing connection, check md5 on the server, no delete or rename
