# compound
Updated: 2026-11-20 14:57 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 3
State: waiting on dispatcher
Now: item 4. c030 auditor repeats 1-2 running detached on the VM (one LLM run at a time, 3 GB floor). c029 waits for `retrack_queue.py` on main; VM tracking stopped
Done since last update:
- Items 2-3 noted: READMEs due Thu 26 Nov 20:00; caps count agent runs, calls and tokens reported beside
- c029 VM label sweep stopped (session ended; no process left). Cached: 16 sizing runs and 42 of 48 unremedied label runs, 0 failed. Left: unremedied runs of illumination_flicker s41-s43 (6 runs), then the remedied states
- c029 sizes from the sizing rule: focus_drift 3 px, illumination_flicker 0.1 (510d287)
- c029 all 24 scored rods and moved copies rendered on the VM (64 rods with sizing); driver refuses VM tracker runs; `render` command
- c030 repeat 0: 30 of 30 runs ended with a report (510d287). Repeat 1: 8 of 30 before the restart, rest running
Needs Andrew:
- c029 register_frames label states: use `register_v2` once on main (tracks with the old tag never reused, spec 2026-11-20 R2), or the old remedy as frozen in v4? I plan `register_v2` for the labels and the methods if it is on main before I submit; else the old remedy, stated in the README
- c029 cluster runs: `retrack_queue.py` takes real windows (root imgdir, window midline). I will add a synthetic-rod job kind (rendered rod folder pushed whole, about 20 MB per rod, 48 rods about 1 GB) unless dispatcher or planning prefers otherwise
