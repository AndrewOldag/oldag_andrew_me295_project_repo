---
id: c036
title: fixes for the c033 audit findings (masking, integrity gate, frame-quality reference, READMEs)
lane: course
owner: dispatcher
state: blocked
branch: wip/audit-fixes
host: VM
created: 2026-11-23 16:20
last_update: 2026-11-23 22:30
blocker: inbox 62 part 2 needs Andrew's archive folder path
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
- [ ] Inbox 62 part 2: archive copy to the lab server (tars and md5 ready on the VM; folder path needed)
