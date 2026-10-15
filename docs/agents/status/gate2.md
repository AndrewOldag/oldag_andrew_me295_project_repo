# gate2
Updated: 2026-10-14 17:15 (local)
Lane: research
Branch: status/gate2
Last inbox item done: 7
State: working
Now: item 3, synthetic validation moved to the tracker machine (Andrew, direct instruction): 4 single-thread processes, nice 19 / ionice idle; growth 64 of 80 windows per tracker, bend 2 of 80
Done since last update:
- VM run stopped; all gate2 processes on the VM ended, CPU freed. Slowness cause: two earlier validation processes kept running on the VM after their runs were stopped
- Finished windows (132) and both phantoms copied to a new folder on the tracker machine; checksums pass; all 132 window files load; resumed there, no window recomputed
Needs Andrew:
- none
