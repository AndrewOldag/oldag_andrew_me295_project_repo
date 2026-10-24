# freeze-v31
Updated: 2026-10-24 12:55 (local)
Lane: course
Branch: wip/freeze-v31
Last inbox item done: 8
State: ready to merge
Now: done. v3.1 ended at its stop rule (Andrew, option a); results in `results/2026-10-24_freeze_v3.1/README.md`; log entry in `docs/running_log_pending/freeze-v31.md`
Done since last update:
- Item 8: README with the sizing sweeps (faults, sizes, seeds, per-seed outcome against the three rule parts, run counts, storage), the second_root cause and the finding; README section for the driver
- Storage: lab-server c014 folder, 464 files, count and sha256 equal to the workstation copies (incl. the 2 cache-match runs)
- Delete exception used once: 3,660 render files (1.74 GB) of the 78 sweep rods in the workstation c014/renders, each after its rod's files matched the verified checksums; every path logged in c014/DELETED.log (3,738 lines), copy on the lab server. 2 cache-match rods' renders kept. Workstation after: work folder 14 GB, 32 GB free
- Main merged (9310c35; decisions conflict: both entries kept). Full suite 256 passed
- Task c014 done
Needs Andrew:
- Main checkout `private/workstation.md` is the old copy; refreshed copy with the delete exception is in this worktree's `private/`
- Decisions entry 2026-10-24 (v3.1 ended) says "no listed fault both degrades the measurement and is repaired by a listed remedy". As run it is narrower: no fault met the rule on 3 of 3 seeds; bad_stage_correction 5 px was repaired on 1 of 3 (seed 12 good but rigid_invariance 3.02 against 2.0); 6-8 px registration not run. Suggest wording it "fewer than 3 of 5 faults qualify on 3 of 3 seeds" in the entry and the paper. Not edited here (your entry). The README states the narrow form
