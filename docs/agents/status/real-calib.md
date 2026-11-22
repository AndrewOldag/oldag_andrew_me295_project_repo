# real-calib
Updated: 2026-11-22 14:50 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 25
State: waiting on server job
Now: item 26. R5 done; R1 job 7841039 running (fetch on next ping); flagged window v2 track not fetched by dispatcher yet
Done since last update:
- Merged origin/main (f12675c). c031 cluster work in its own work, code and stage folders (not dispatcher's)
- R5: 6 freeze v4 register rods + moved copies re-rendered here (truth equal within 1e-12), 12 runs in one cluster array (7840638), 12 fetched, 0 failed, worst case $0.144
- R5 result: v1 repairs 6 of 6, register_v2 3 of 6. v2 closure lower on all 6; v2 rigid invariance higher on all 6, over the synthetic 2.0 %/h on 3. All 12 measurements good against truth; option A gate passes all 12. results/2026-11-20_registration_fix/regression.md
- R1: root 0711_c5 staged (10.7 GB, c031 stage folder), job 7841039 submitted 14:3x, RUNNING at 14:45
Needs Andrew:
- R5: register_v2 repairs fewer synthetic rods than v1 (3 vs 6) because rigid invariance rises; closure and truth error are fine. On real windows rigid invariance is reported, not gating. Keep register_v2 as the remedy, or something else? No change made (fixed remedy list)
- Cluster folder: the staged root holds 10.7 GB of the 30 GB cap until R1 is fetched and the root cleared (next ping)
