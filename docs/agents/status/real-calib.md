# real-calib
Updated: 2026-11-23 15:10 (local)
Lane: course
Branch: wip/zone-checks
Last inbox item done: 30
State: waiting on Andrew
Now: c034 built and run; synthetic part does not match the spec as amended on main (6810f3a, 13:22, after this branch was cut at d943c29)
Done since last update:
- Merged origin/main (a7cd1f8); no other change
- c034 work as before: proposal e385ae2/f5cc997, checks and tests f5cc997, synthetic and thresholds 3cf728b, real report-only 3fb58c7
Needs Andrew:
- Spec 6810f3a says the shifted rods are rendered on the VM and tracked on the cluster CPU through rod_jobs.py. This branch built them by shifting the reported profile along s on the freeze v4 records (no rendering, no tracking). The original spec allowed that
- Question: what is the fault in a rendered shifted rod? Rendered with the zone moved and then tracked, the rod is a correct measurement, and the checks should pass it. Options: (a) keep on-record shifts as the fault and add rendered shifted rods as further clean rods (false-alarm set, not threshold set); (b) render the moved zone, track it, then pair the tracked points with the unmoved profile (fault = profile from the wrong zone); (c) other. Thresholds (config/zone_thresholds.yaml) come from unshifted clean tracks and do not change under (a) or (b)
- Cluster: rendering and rod_jobs.py submit need the connection master open; budget stop $15. Nothing submitted
- Merge of wip/zone-checks waits on this answer; deadline Fri 27 Nov 12:00
- wip/supervisor (c032) still ready to merge, unchanged
