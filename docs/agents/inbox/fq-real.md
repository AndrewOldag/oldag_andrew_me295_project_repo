# Inbox: fq-real

1. Worktree `../wt-fq-real`, branch `wip/fq-real` from current `main`. Do Task B of `docs/specs/2026-10-13_auditor-v1-real-frame-quality-labels.md`, steps B1-B3. Then status `waiting on Andrew` with the folder Andrew labels in and the number of windows. Do B4 only after an inbox item says the labels are done
2. Usable windows only (Andrew, 2026-10-13). Rule now in `CLAUDE.md`: only roots with `include` yes, only time inside `usable_from_h` to `usable_to_h`. Nothing outside is used for any labeling, training, threshold or test. Andrew found one window in the overlay grid (column 3, bottom row) traced into the dark region at the bottom of the plate
   - Check all 30 windows against the rule. Replace every window that breaks it with a new window that keeps it, new ids from `fq31`. "Likely poor" windows also come from inside usable windows only (debris, bubbles, uneven light, banding inside the usable hours)
   - Remove the replaced windows from `staging/fq_real_labeling/` (VM only) and from `labels.csv`. Keep the other ids and any labels Andrew has already written
   - Report in status: which ids were replaced and why (rule broken: `include` no, or outside usable hours), and which window is column 3, bottom row of the overlay grid
3. Band (planning decision): use the segmentation band now. Mark the real reference provisional in config. Recompute it with the midline source used by real tracking once that exists. Check every overlay by eye after step 2; a band that leaves the root goes under Needs Andrew with the id
4. B4 stop rule (planning decision): drop "any clean window below the synthetic lowest". Real and synthetic references are separate. Keep the separation check between clean and not_clean
