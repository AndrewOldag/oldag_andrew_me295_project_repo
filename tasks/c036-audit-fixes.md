---
id: c036
title: fixes for the c033 audit findings (masking, integrity gate, frame-quality reference, READMEs)
lane: course
owner: dispatcher
state: done
branch: wip/audit-fixes
host: VM
created: 2026-11-23 16:20
last_update: 2026-11-24 08:45
blocker: none
done_marker: results/2026-11-23_audit_fixes/README.md
---

Inbox item, planning 2026-11-23 16:20; findings in results/2026-11-23_audit/.

## Parts
- [x] S1-3, S1-4: mask real-root values at the tip; grep test (61 files)
- [x] S2-1: integrity gate fix, tests; report-only impact on remedied tracks
- [x] S3-1: frame_quality reference recompute, report-only impact
- [x] S6-3, S7-1, S7-2: READMEs and commands
- [x] results/2026-11-23_audit_fixes/README.md
- [x] Inbox 62 part 1: mask_bio reviewed exemption, flank-difference range unmasked, tests (ad577fe)
- [x] Inbox 62 part 2 / 63: archive copy to the lab server, md5 4 of 4 OK on the server
