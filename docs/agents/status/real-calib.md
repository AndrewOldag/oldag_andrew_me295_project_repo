# real-calib
Updated: 2026-11-04 15:50 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 16
State: working
Now: spec 2026-11-04 Work 3: code (separate storage and compute hosts, one persistent connection, checker inside the cluster job, no jobs on the lab server)
Done since last update:
- Item 16: cluster connection master on the lab server is running (checked 15:16); no wait
- Item 14 replaced by item 15 (spec 2026-11-04)
- Work 1: branch rebuilt from `origin/main` with the old tip (only the 2026-11-02 pause commit was not in main) merged into it; fast-forward push, no force
- Work 2: the 50 collected batch-2 roots are on the lab server, every file equal to the md5 list recorded at collection (590 windows, 589 tracks; the one missing track is the known 0721_m5 w0-2 tracker error). Nothing missing or different
- The cluster copies of these outputs (`fb2/<root>/`, 55 folders) were deleted on 2026-10-27 by another session ('Andrew asked in chat' in `DELETED.log`), so the lab-server copies are now the only ones. The 4 roots staged and not submitted are still on the cluster (0721_c6, 0721_m6, 0727_cc6, 0727_mc6)
- The stored md5 lists have CRLF line ends (written through Windows text-mode stdin); the check strips CR. Fixed in the new driver
Needs Andrew:
- none
