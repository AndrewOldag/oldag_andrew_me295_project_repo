# Second compute host: survey and test job

Spec 2026-10-23c, session host-setup, task c012. Machine names, addresses and paths are in `private/workstation.md`.

## Survey (workstation)
- CPU host: 14 cores, 20 threads; 62 GB RAM. No usable GPU (integrated graphics only)
- Disk: 41-46 GB free on the whole machine at survey. Work-folder cap 20 GB; at least 20 GB must stay free (Andrew, 2026-10-23)
- Tracker environment: built from `envs/qb.yml` in the work folder (micromamba, no sudo), about 3 min, 3.2 GB
- Imaging drive: not mounted at survey time
- Load at survey: 0.00; no other user's jobs

## Test job 1: synthetic v3 rod (pass)
- Rod `v3_growth_zone_clean_s10`, state st1 (`qb_track.py --stride 1`). Tracker master d5f1829; course code 47a3c47 (the commit the lab-server reference used)
- Rendered frames: byte-identical to the lab-server render (all 44 files)
- Tracks (left, centre, right), midline, stage correction, frame times, REGR profiles: max absolute difference 2.3e-13 px or less; frozen masks and NaN patterns equal. Limit 1e-6 px
- Metadata differs only in the recorded run time
- Wall time: render 4.4 s; tracker run 5.7 s, of which tracking loop 4.4 s (lab server: 6.2 s)

## Test job 2: real window, root 0708_m12, 4-6 h (pass)
- Frames: the root's montage folder without histogram files (961 frames, 5.54 GB), copied from the lab server with the workstation's upload key. The tracker loader reads every frame file and checks the count against the stage table, so a frame subset does not load
- Tracker gate2-windowed-coupling 52e9bd1 (its tracker files equal those of the lab-server reference run, stage-auxdata 888f972); course wrapper and midline of the reference run; `--movie real --from-h 4 --to-h 6`
- Tracks: max absolute difference 1.1e-12 px; REGR profiles 4.3e-12; midline and stage correction equal; frozen masks and NaN patterns equal
- Checker (course `checker/checks.py`, 023cd4b): closure 5.533 px/h on both; plane_sections 256.99 %/h on both (difference 1e-13); rigid invariance not applicable (no moved run)
- Metadata differs only in root id (folder name) and run time
- Wall time 12.2 s; tracking loop 8.8 s (lab server: 12.3 s)

## Results back to the lab server (pass)
- The workstation's upload key reaches the lab server. Test outputs, scripts, comparison tables and the done marker are in the task's own folder there (11 files)
