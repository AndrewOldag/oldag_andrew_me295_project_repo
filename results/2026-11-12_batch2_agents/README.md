# Remedy tree over the batch-2 windows that fail closure (task c026)

Spec `docs/specs/2026-11-12_batch2-agents.md`; proposal `docs/proposals/2026-11-12_batch2-agents.md` (committed before any run, f2ec5be). 2026-11-12 to 2026-11-14.

## What ran and what did not
- Fixed script (no remedy; closure fail -> decline): all 84 windows, by definition (the batch-2 result)
- Remedy tree: 38 of the 84 windows, in the file's root order, before the run stopped
- Diagnostician: not run. Andrew, 2026-11-14 13:20: report what ran on the cluster; no diagnostician run this time. So there is no agent-vs-tree agreement or disagreement list here; the run code is in place (`batch2_agents.py agents`)
- Why the tree stopped at 38: the cluster connection master on the lab server was down 2026-11-12 from at least 16:00 until Andrew reopened it; Claude Code stopped the background run for low VM memory about 00:10 on 2026-11-13 (window 21; restarted from Andrew's terminal 10:52); a silently dead lab-server connection held one window from 15:37 to 19:28; the master went down again about 23:10 on 2026-11-13 and the run stopped at window 38 (`MasterDown`)

## Setup
- Windows: the 84 windows of `results/2026-10-25_full_batch_2/windows.csv` with outcome fail (closure above 19 px/h), 50 roots
- Start: each window's batch-2 track (1000 px, stride 1, ft2 net midline), copied from storage with md5 checks. The checker on this machine gives the batch-2 closure on all 84 (largest difference 4.9e-5 px/h); closure is the only failing gate on every window
- Remedy tree: `agents/baselines.py` `run_tree`, step limit 8, through the diagnostician's Slice, remedies and checker (real profile: closure gates at 19 px/h; rigid invariance and plane sections reported). Closure list: register_frames, change_frame_stride half (skipped at stride 1), enlarge_patch 1.5x, enlarge_patch 2x, smooth_midline light, then decline. Roll back as in the Slice: a remedy that makes no failing check pass and lowers none by a quarter is undone
- Adapter (37d108b): on real windows the tree reads the profile's gating checks; before, rigid invariance without a moved copy (81 of 84 windows) counted as failing (decisions 2026-11-12)
- Retracks: one Slurm CPU job each on cluster nodes (1 core, 1 h limit), through the lab server's connection master; outputs to storage with md5 checks; the track file to this machine. Checker on this machine (Andrew, 2026-11-12, decisions)
- Staging: one root at a time; a staged root copy deleted only after every cluster track of the root was md5-equal on storage; 24 deletes, each in DELETED.log on the cluster

## Run
```
python scripts/batch2_agents.py fetch
python scripts/batch2_agents.py tree --out staging/c026/tree --stop-at 2026-11-14T08:00
python scripts/batch2_agents.py report --tree staging/c026/tree --agents staging/c026/agents --out results/2026-11-12_batch2_agents
```
- Records, trace and retracks in `staging/c026/` (git-ignored). A restart skips finished windows
- Median 21 min per window (4 retracks; queue wait under a minute; registration jobs 17-24 min, other tracks about 2 min)

## Result (`tables.md`, `windows.csv`)
| Method | Windows | Run | Accepted after repair | Declined | Error | Not run |
| :-- | --: | --: | --: | --: | --: | --: |
| fixed script | 84 | 84 | 0 | 84 | 0 | 0 |
| remedy tree | 84 | 38 | 9 | 28 | 1 | 46 |

- "Accepted after repair" means closure passes on the recheck after a kept remedy. Real windows have no ground truth: it does not say the repaired measurement is right
- Kept remedy on the 9: light midline smoothing 5 (0711_m3 14-16 h, 0721_m3 4-6 and 6-8 h, 0727_mm2 12-14 and 14-16 h), frame registration 2 (0711_c5 6-8 h, 0711_m4 2-4 h), disk radius 1.5x 1 (0714_c6 0-2 h), disk radius 2x 1 (0714_c9 12-14 h)
- Remedies tried 142 on 38 windows: kept 14, rolled back 127, not available 1. 4 declined windows kept a remedy that lowered closure by a quarter or more but not below 19 px/h
- Faults named by the tree on declined windows: rigid_drift 24, midline_jitter 4 (the tree names the fault of the first remedy tried, or of the last kept one)
- Error 1: 0721_c3 2-4 h, a retrack failed with the tracker's `arange: cannot compute length` (the error that left 33 batch-2 windows without a track)
- Frame registration often made closure much worse before it was rolled back (for example 19.4 -> 20125 px/h on 0708_c6 0-2 h): the registration band start comes from the window's own strain-rate profile, which is unreliable on a failing window
- Retracks: 148 new track files (including moved-copy pairs on the one 10-12 h window reached). Spend since 2026-10-23: $7.24 at the start, $7.37 at the restart on 2026-11-13 20:34; the final figure could not be read (the ledger reaches the cluster on its own connection, which was down). Under the $12 stop

## Example traces
`example_traces.md`: the tree on one window with a kept remedy (0711_c5 6-8 h) and one declined (0708_c4 0-2 h): each action, its arguments and rule, the check values before and after. Plane-sections values masked

## Known limits
- 38 of 84 windows, the first in root order, not a sample: by condition, the tree reached 15 of 25 control, 2 of 6 control then control, 7 of 26 mannitol, 10 of 20 mannitol then control, 4 of 7 mannitol then mannitol
- No diagnostician run, so no agent comparison on these windows
- Real-movie profile: closure is the only gate; rigid invariance computed on one window reached here (0714_c9 10-12 h)
- A staged root copy may remain on the cluster from the window the run stopped on (the master was down); cleared on the next run or by hand, after an md5 check
