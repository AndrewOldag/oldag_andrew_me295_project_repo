# Batch-2 `arange: cannot compute length` crash (spec 2026-11-18 C1-C2, task c028)

2026-11-20. Code fix dc1cfe6. No track, cluster job or LLM run.

## Cause
- Not in the tracker. The tracker wrote complete tracks for these windows (md5 equal to `results/2026-10-25_full_batch_2/audit/outputs.csv`)
- In these windows the tip point of the centre chain (index 0) lies within the edge threshold (10 px) of the image border in every frame: at frame 0 the midline tip is at column 0
- `measure/record.py` `from_tracker_npz` sets edge-frozen points to NaN; `arclength` propagates NaN baseward from the tip; every arc length is NaN; `derive()` called `np.arange(0, NaN)` and raised
- Reproduced on one window (0711_c2__w0-2) with `scripts/remote/check_window.py` on its batch-2 track
- Same error: 3 batch-1 windows and the c026 tree run on 0721_c3__w2-4

## Fix
- `derive()`: with no finite arc length the grid is empty. Any other record takes the same code path as before
- Closure reads the tip point, which is NaN, so closure is not computable; by the 2026-10-26 rule this is decline (counted with fail, not-computable count beside it)
- Test `tests/test_record_tracker.py::test_tip_frozen_in_every_frame_is_not_computable`: the clean fixture with the tip frozen in every frame. Fails with the ValueError before the fix, passes after

## Equivalence (C2)
- 5 batch-2 windows that measured before, one per condition (0708_c4__w0-2, 0708_m2__w0-2, 0721_m2__w0-2, 0727_cc2__w0-2, 0727_mm2__w0-2): checker rerun on their batch-2 tracks with the fix
- 5 of 5 records identical to the batch-2 records (every key, difference 0.0); 5 of 5 track md5s match the audit
- Retracking was not needed: the fix does not touch the tracker or the tracks

## Failed batch-2 windows after the fix
- 34 failed windows: 33 with the arange error, 1 with no track (0721_m5__w0-2, logistic fit; a tracker error, not this one)
- C3 (inbox item 21): the 12 tracks that were only on storage copied to this machine, read only, md5 equal on storage, here and in the audit (12 of 12)
- All 33 checked on this machine with the fix (`scripts/check_after_fix.py`; 0714_m4__w10-12 with its moved-copy tracks, as in batch 2): 33 `measured`, outcome not computable (decline by rule)
- `results/2026-10-25_full_batch_2/windows.csv`: new column `checked_after_fix`; the 1061 batch-2 rows unchanged with the column empty; 33 rows appended with `yes`. A reader keyed by window that keeps the last row gets the row after the fix
- Not measured, listed as failure modes: 0721_m5__w0-2 (no track, tracker logistic-fit error); 0727_cc7, 2 windows (stage table 155 steps for 857 positions; C4)
- Per window: `check_after_fix.json` (2026-11-20 first pass on the 21 VM tracks; outcome and closure only)

## Commands
- C3: `QB_TRACKER=<tracker> python scripts/check_after_fix.py --tracks <folder with the batch-2 tracks>` -> `{"checked": 33, "outcomes": {"not computable": 33}}`; a rerun writes the same file
- Test: `python -m pytest tests/test_record_tracker.py`
- One window: `PYTHONPATH=<tracker>:. python scripts/remote/check_window.py --window 0711_c2__w0-2 --track <track npz> --out <json>`
