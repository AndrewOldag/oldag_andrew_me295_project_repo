# Second compute host: survey and test job

Spec 2026-10-23c, session host-setup, task c012. Machine names, addresses and paths are in `private/workstation.md`.

## Survey (workstation)
- CPU host: 14 cores, 20 threads; 62 GB RAM. No usable GPU (integrated graphics only)
- Free disk in the home folder: 46 GB (95 % used). The 100 GB work-folder cap cannot be reached; plan for about 40 GB
- Python environment for the tracker: built from `envs/qb.yml` in the work folder (micromamba, no sudo), about 3 min
- Imaging drive: not mounted at survey time
- Load at survey: 0.00; no other user's jobs

## Test job 1: synthetic v3 rod (pass)
- Rod `v3_growth_zone_clean_s10`, state st1 (`qb_track.py --stride 1`). Tracker master d5f1829; course code 47a3c47 (the commit the lab-server reference used)
- Rendered frames: byte-identical to the lab-server render (all 44 files)
- Tracks (left, centre, right), midline, stage correction, frame times, REGR profiles: max absolute difference 2.3e-13 px or less; frozen masks and NaN patterns equal. Limit 1e-6 px
- Metadata differs only in the recorded run time
- Wall time: render 4.4 s; tracker run 5.7 s, of which tracking loop 4.4 s (lab server: 6.2 s)

## Test job 2: real window, root 0708_m12, 4-6 h (not run)
- Needs about 80 frames of the montage on the workstation. Both transfer routes were refused by the build session's permission check: the workstation's own upload key, and a stream through the VM
- Tracker code for it is in place: gate2-windowed-coupling 52e9bd1, whose tracker files equal those of the lab-server reference run (stage-auxdata 888f972)
