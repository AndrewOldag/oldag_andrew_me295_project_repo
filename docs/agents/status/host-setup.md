# host-setup
Updated: 2026-10-23 18:41 (local)
Lane: course
Branch: wip/host-setup
Last inbox item done: 6
State: ready to merge
Now: done; test passed; assignment below for the coordinator
Done since last update:
- Item 6: private file copied again (20 GB cap, 20 GB free floor); `df` checked before and after every copy and run: 36 GB free after, work folder 9.9 GB
- Item 5: frame copy done by this session on the workstation with its upload key (rsync, nice 19, bwlimit 50000, `-s`): root 0708_m12 montage without histograms, 961 frames, 5.54 GB. Whole folder, not a subset: the tracker loader checks the frame count against the stage table (decisions entry)
- Item 4 / spec item 4, real window (0708_m12, 4-6 h, tracker 52e9bd1): pass. Tracks max |d| 1.1e-12 px; checker closure 5.533 px/h and plane_sections 256.99 %/h on both. Tracking loop 8.8 s vs 12.3 s on the lab server
- Spec item 4, synthetic (v3_growth_zone_clean_s10, st1): pass. Render byte-identical; tracks max |d| 2.3e-13 px. Tracking loop 4.4 s vs 6.2 s
- Upload key test: pass. Outputs, scripts, comparison tables and done marker `c012_test.done` in the task's lab-server folder (11 files)
- Records: `results/2026-10-23_host_setup/README.md`, decisions entries, `docs/running_log_pending/host-setup.md`; task c012 set to review
- Earlier: `host:` field on the board, set on every open course task; tests 10 passed, full suite 205 passed (47c4c1a); survey and synthetic test 023cd4b; full suite 205 passed again after merging main
- Assignment (spec item 6, with coordinator item 13), for the coordinator's inbox items:
  - turn-long (research): stays on the lab server (interval_2 frames too large for the workstation)
  - dispatcher: scale sweep (5-frame sweeps) and closure probes on the workstation; cluster GPU runs as before. The 0708_m12 montage is already on the workstation (host-setup work folder): reuse it, do not pull it again. At most one more root fits under the 20 GB cap
  - freeze-v3: stays on the lab server. Label sweep to the workstation only after a test that its cached outputs match
  - Limits: lab server 2 jobs; workstation 2 Claude jobs, each at most half the cores, nice 19; separate. Workstation disk: 20 GB work-folder cap, at least 20 GB free, `df -h / ~` before and after each step
  - Workstation tracker env and code: env from `envs/qb.yml`; tracker master installed, other branches by PYTHONPATH (private file)
Needs Andrew:
- Workstation disk: work folder 9.9 GB of the 20 GB cap after one root; sessions cannot delete there, so only about one more root montage fits
