# Proposal: remedy tree and diagnostician over the 84 batch-2 windows that fail closure (task c026)

Spec `docs/specs/2026-11-12_batch2-agents.md` (Andrew, 2026-11-12). Dispatcher inbox item 45. Committed before any run. Nothing here changes after the first result is seen.

## Windows
- The 84 windows of `results/2026-10-25_full_batch_2/windows.csv` with `outcome = fail` (closure above 19 px/h): 50 roots; 25 control, 6 control then control, 26 mannitol, 20 mannitol then control, 7 mannitol then mannitol
- 3 of the 84 are 10-12 h windows with a whole-pixel moved copy (rigid invariance reported); the other 81 have none
- Not in scope: 18 not-computable windows (declined by rule), 34 failed and 2 not-run windows, 925 passes
- List: `python scripts/batch2_agents.py windows`. Closure is the batch-2 value from the cluster checker

## Methods
Same windows, same tracks, same remedy executors (`agents/executors.py` `Slice.apply_remedy`, `measure/remedies.py`), same checker and real profile (closure gates at 19 px/h; rigid invariance and plane sections reported). Every method starts from the batch-2 track of the window (1000 px, stride 1, ft2 net midline), copied from storage with md5 checks (`batch2_agents.py fetch`).

1. Fixed script: no remedy; closure fail -> decline. The batch-2 result as it stands. No run
2. Remedy tree: `agents/baselines.py` `run_tree`, step limit 8, through `scripts/batch2_agents.py tree`. Rule 1 list for closure: register_frames, change_frame_stride half (skipped at stride 1), enlarge_patch 1.5x, enlarge_patch 2x, smooth_midline light; then decline. Roll back as in the Slice (no failing check passes and none falls by a quarter)
   - Adapter (37d108b): the tree reads the slice's gating checks, so on real windows only closure can fail. Before, rigid invariance without a moved copy counted as failing (decisions 2026-11-12). Synthetic rods unchanged (all three checks gate)
   - Window errors (tracker or job failure) are recorded as `error` for the window; a budget stop or a lost connection stops the run
3. Diagnostician: `scripts/real_slice.py` with cached tracks, dispatcher agent -> checker -> diagnostician, in 4 groups of at most 21 windows in root order (`batch2_agents.py agents`), then one auditor run over all 84 (`real_slice.py --audit-only`). Model `claude-opus-5-5`, Claude Code 2.1.310 (`config/models.yaml`). One run
- Order: the tree first. Retracks are cached by window and settings tag, so the diagnostician reuses every retrack the tree made; a remedy combination the tree did not make is tracked new, the same way

## Compute and caps
- Remedy retracks: one Slurm CPU job each (1 core, 1 h limit, worst case $0.012) on cluster nodes, through the storage host's connection master (`compute: cluster`). Outputs copied to storage, md5 on both ends; the VM receives the track file
- A 10-12 h window needs the moved copy again for a retrack (one CPU job, 30 min limit) and two tracks per remedy
- Upper bound for the tree: 81 x 4 + 3 x 9 = 351 jobs, worst case $4.21; expected actual well under $1 (tracks of 20-33 s on the lab server in c022)
- Ledger check before every submit; `spend_stop_usd: 12` refuses a submit once the projected total since 2026-10-23 reaches $12 (now $7.24 of $15): stop, Needs Andrew
- Staging: one root at a time in the cluster folder (35 GB cap). Before staging a root, any other staged root is cleared; the tree clears each root after its last window. A clear needs every cluster track of that root md5-equal on storage; each delete goes to DELETED.log in the task folder
- No compute on the lab server; no delete there
- LLM calls: cap 700 in total. A group starts only if the calls so far, plus 8 per window of the group, plus 30 for the auditor and dispatcher, stay within the cap. Diagnostician step limit 8; expected about 4 calls per window (c022: 34 calls on 10 failing windows)
- Free VM memory at least 3 GB before each window
- A group whose traces hold the seat's session-limit message is set aside and run again, not recorded (as in c023)

## Metrics (computed in code, `batch2_agents.py report`)
- Per method: accepted after a kept remedy (closure passes on the recheck), declined, step limit, errors
- Remedies tried, kept, rolled back, not available; retracks run; cluster jobs and spend
- Diagnostician: LLM calls, tokens in and out, call time; fault named per window
- Agreement per window, diagnostician vs tree: same outcome; same remedy kept
- Disagreement list: every window where the two differ, with closure before and after each remedy tried
- Auditor flags on windows accepted after repair
- Real windows have no ground truth. "Recovered" means the checker passes after a kept remedy; nothing more

## Outputs
- `results/2026-11-12_batch2_agents/`: README, `windows.csv` (outcome and check values only), `example_traces.md` (one window with a kept remedy, one declined; REGR, growth-zone and flank values masked)
- Traces, records and summaries stay in `staging/c026/` (git-ignored)
- Deadline for the README: Sat 14 Nov 20:00 local; whatever has finished then is reported

## Windows (batch-2 closure)
| # | Root | Condition | Window (h) | Closure (px/h) | Moved copy |
| --: | :-- | :-- | :-- | --: | :-- |
| 1 | 0708_c4 | control | 0-2 | 103.5 | no |
| 2 | 0708_c4 | control | 2-4 | 97.7 | no |
| 3 | 0711_c1 | control | 0-2 | 34.6 | no |
| 4 | 0711_m2 | mannitol | 6-8 | 25.0 | no |
| 5 | 0714_c4 | control | 0-2 | 60.0 | no |
| 6 | 0721_c1 | control | 4-6 | 32.1 | no |
| 7 | 0721_m2 | mannitol then control | 20-22 | 28.6 | no |
| 8 | 0727_mm2 | mannitol then mannitol | 12-14 | 20.1 | no |
| 9 | 0727_mm2 | mannitol then mannitol | 14-16 | 42.7 | no |
| 10 | 0711_m3 | mannitol | 12-14 | 29.3 | no |
| 11 | 0711_m3 | mannitol | 14-16 | 25.2 | no |
| 12 | 0714_c6 | control | 0-2 | 20.6 | no |
| 13 | 0714_m4 | mannitol | 12-14 | 40.3 | no |
| 14 | 0721_c3 | control | 2-4 | 149.4 | no |
| 15 | 0721_m3 | mannitol then control | 4-6 | 24.7 | no |
| 16 | 0721_m3 | mannitol then control | 6-8 | 42.2 | no |
| 17 | 0721_m3 | mannitol then control | 16-18 | 40.0 | no |
| 18 | 0721_m3 | mannitol then control | 18-20 | 36.4 | no |
| 19 | 0721_m3 | mannitol then control | 20-22 | 40.7 | no |
| 20 | 0721_m3 | mannitol then control | 22-23.99 | 27.9 | no |
| 21 | 0727_cc3 | control then control | 20-22 | 25.8 | no |
| 22 | 0727_cc3 | control then control | 22-23.63 | 23.7 | no |
| 23 | 0727_mm3 | mannitol then mannitol | 20-22 | 20.5 | no |
| 24 | 0727_mm3 | mannitol then mannitol | 22-23.64 | 29.9 | no |
| 25 | 0708_c6 | control | 0-2 | 19.4 | no |
| 26 | 0708_c6 | control | 2-4 | 28.2 | no |
| 27 | 0708_m6 | mannitol | 14-16 | 58.8 | no |
| 28 | 0711_m4 | mannitol | 2-4 | 24.5 | no |
| 29 | 0714_c9 | control | 2-4 | 55.5 | no |
| 30 | 0714_c9 | control | 10-12 | 29.0 | yes |
| 31 | 0714_c9 | control | 12-14 | 47.5 | no |
| 32 | 0714_c9 | control | 16-18 | 69.0 | no |
| 33 | 0721_m4 | mannitol then control | 0-2 | 179.7 | no |
| 34 | 0721_m4 | mannitol then control | 14-16 | 28.3 | no |
| 35 | 0727_mc4 | mannitol then control | 0-2 | 34.6 | no |
| 36 | 0708_m7 | mannitol | 12-14 | 26.2 | no |
| 37 | 0711_c5 | control | 6-8 | 22.8 | no |
| 38 | 0711_c5 | control | 12-14 | 56.6 | no |
| 39 | 0711_m6 | mannitol | 0-2 | 25.7 | no |
| 40 | 0711_m6 | mannitol | 2-4 | 39.3 | no |
| 41 | 0714_m7 | mannitol | 0-2 | 34.8 | no |
| 42 | 0714_m7 | mannitol | 18-20 | 19.7 | no |
| 43 | 0714_m7 | mannitol | 22-23.89 | 21.7 | no |
| 44 | 0721_m5 | mannitol then control | 20-22 | 23.5 | no |
| 45 | 0727_cc5 | control then control | 12-14 | 36.0 | no |
| 46 | 0727_cc5 | control then control | 14-16 | 53.1 | no |
| 47 | 0727_mc5 | mannitol then control | 16-18 | 21.6 | no |
| 48 | 0727_mm6 | mannitol then mannitol | 20-22 | 20.1 | no |
| 49 | 0727_mm6 | mannitol then mannitol | 22-23.64 | 23.1 | no |
| 50 | 0708_c9 | control | 18-20 | 20.9 | no |
| 51 | 0708_c9 | control | 20-22 | 23.7 | no |
| 52 | 0708_m8 | mannitol | 0-2 | 19.6 | no |
| 53 | 0708_m8 | mannitol | 4-6 | 47.7 | no |
| 54 | 0708_m8 | mannitol | 6-8 | 39.2 | no |
| 55 | 0708_m8 | mannitol | 18-20 | 43.0 | no |
| 56 | 0727_cc6 | control then control | 8-10 | 61.2 | no |
| 57 | 0727_cc6 | control then control | 10-12 | 66.8 | yes |
| 58 | 0727_mc6 | mannitol then control | 4-6 | 30.6 | no |
| 59 | 0727_mm7 | mannitol then mannitol | 20-22 | 20.0 | no |
| 60 | 0708_c10 | control | 0-2 | 76.1 | no |
| 61 | 0708_c10 | control | 2-4 | 36.7 | no |
| 62 | 0708_m9 | mannitol | 0-2 | 38.3 | no |
| 63 | 0708_m9 | mannitol | 10-12 | 329.1 | yes |
| 64 | 0708_m9 | mannitol | 12-14 | 376.7 | no |
| 65 | 0708_m9 | mannitol | 16-18 | 24.0 | no |
| 66 | 0721_c7 | control | 22-24 | 394.4 | no |
| 67 | 0721_m7 | mannitol then control | 18-20 | 27.9 | no |
| 68 | 0708_c11 | control | 0-2 | 56.2 | no |
| 69 | 0711_c8 | control | 8-10 | 90.0 | no |
| 70 | 0711_m10 | mannitol | 0-2 | 184.6 | no |
| 71 | 0714_m10 | mannitol | 18-20 | 40.6 | no |
| 72 | 0708_m11 | mannitol | 0-2 | 49.1 | no |
| 73 | 0708_m11 | mannitol | 2-4 | 45.5 | no |
| 74 | 0721_c9 | control | 4-6 | 24.7 | no |
| 75 | 0721_c9 | control | 8-10 | 307.8 | no |
| 76 | 0721_c9 | control | 14-16 | 412.1 | no |
| 77 | 0714_m13 | mannitol | 0-2 | 58.0 | no |
| 78 | 0721_m10 | mannitol then control | 18-20 | 43.3 | no |
| 79 | 0714_m14 | mannitol | 0-2 | 30.7 | no |
| 80 | 0721_m11 | mannitol then control | 22-24 | 39.3 | no |
| 81 | 0727_mc11 | mannitol then control | 18-20 | 52.0 | no |
| 82 | 0721_m12 | mannitol then control | 16-18 | 67.4 | no |
| 83 | 0727_mc14 | mannitol then control | 0-2 | 19.3 | no |
| 84 | 0727_mc14 | mannitol then control | 20-22 | 48.4 | no |

Closure over the 84: median 36.6, min 19.3, max 412.1 px/h
