# real-calib
Updated: 2026-10-24 17:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 1
State: waiting on Andrew
Now: item 2 (section B): calibration script ready; the 16 calibration windows do not fit in the 30 GB cluster work folder after section C's windows, so their ft2 midlines cannot be built yet
Done since last update:
- Calibration set and rule committed before any compute: `docs/proposals/2026-10-24_real-calibration.md` (16 windows: 0708_c8, 0708_c9, 0711_c5, 0711_c7, 0714_c4, 0714_c9, 0721_c5, 0721_c6; 7-9 h and 15-17 h); replacement list holds no section C root (agreed with dispatcher)
- Fixed non-growing roots checked: other rig, about 0.84 um/px; not used
- Windows queued in the dispatcher's c019 chain (seg midline and frame lists on the lab server now; cluster GPU through its ledger)
- `scripts/real_calib.py` (screen, measure, checks, per-window resume files, 95th percentile rounded up to 2 s.f.); `tip_apex_probe.py` takes an optional frame count (default unchanged); tests `tests/test_real_calib.py` pass. $0 cluster spend by this session
Needs Andrew:
- Cluster work folder: section C uses about 26 of 30 GB (frames cannot be deleted); the 16 calibration windows need about 7 GB more. Options (same as in the dispatcher's status): (a) raise the cap to about 40 GB; (b) let the GPU job unpack gzip'd frames on node-local disk (a write outside the trials folder); (c) build the 16 calibration midlines on the lab server CPU, one at a time, 3 threads, nice 19 (about 30 min each, 8 h total; heavier than "light"). Answer in either inbox; the two sessions pass it on
